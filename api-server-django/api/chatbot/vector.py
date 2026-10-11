"""vector.py — DWH Schema Embeddings
Source: full DWH documentation (galaxy schema, 7 facts, 18 dims)  
"""
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DB_LOCATION = str(BASE_DIR / "chroma_dwh_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "mxbai-embed-large")

SCHEMA_DOCUMENTS = [
    {
        "id": "fact_emission",
        "title": "DWH_FACT_EMISSION",
        "content": (
            "Table dwh.DWH_FACT_EMISSION stores insurance policy issuances and premiums. "
            "Primary key: ID_EMISSION. "
            "Connected dimensions (foreign keys): "
            "id_agent (-> dim_agent), id_client (-> dim_client), id_police (-> dim_police), "
            "id_produit (-> dim_produit), id_usage (-> dim_usage), id_periode (-> dim_periode), "
            "id_etat_quittance (-> dim_etat_quittance), id_nature_quittance (-> dim_nature_quittance). "
            "Measures: PRIME_NETTE (net premium), PRIME_TOTAL (total premium), TAXE (tax), "
            "TIMBRE (stamp duty), FGA (guarantee fund contribution), "
            "COMMISSION (agent commission), BONUS_MALUS (bonus-malus coefficient). "
            "This is the revenue table: 'chiffre d'affaires', 'revenue', 'turnover', and 'primes émises' "
            "all mean SUM(PRIME_TOTAL) from this table, grouped by the relevant dimension (agent, product, branch...). "
            "Do NOT use DWH_FACT_IMPAYE for revenue/chiffre d'affaires questions — that table is unpaid premiums, not revenue. "
            "Use for premium analysis, commission reports, emission KPIs, and portfolio monitoring."
        ),
        "table_type": "fact",
        "subject": "emission, premium, prime, issuance, quittance, commission, bonus malus, chiffre d'affaires, revenue, turnover, CA, primes émises, commission totale, nouvelle affaire, renouvellement, taxe"
    },
    {
        "id": "fact_emission_detail",
        "title": "DWH_FACT_EMISSION_DETAIL",
        "content": (
            "Table dwh.DWH_FACT_EMISSION_DETAIL stores premium amounts broken down by guarantee. "
            "Primary key: ID_DET_QUITTANCE. "
            "Connected dimensions: id_garantie (-> dim_garantie), id_police (-> dim_police). "
            "Parent fact: ID_EMISSION (-> DWH_FACT_EMISSION). "
            "Measures: MT_PRIME (premium amount per guarantee). "
            "Use to analyze which guarantees (RC, Vol, Incendie, etc.) contribute most to premium volume. "
            "JOIN with DWH_FACT_EMISSION on ID_EMISSION to get full emission context."
        ),
        "table_type": "fact",
        "subject": "prime par garantie, emission detail, garantie, MT_PRIME"
    },
    {
        "id": "fact_annulation",
        "title": "DWH_FACT_ANNULATION",
        "content": (
            "Table dwh.DWH_FACT_ANNULATION stores policy cancellation events. "
            "Primary key: id_annulation. "
            "Connected dimensions (foreign keys): "
            "id_agent (-> dim_agent), id_client (-> dim_client), id_police (-> dim_police), "
            "id_produit (-> dim_produit), id_usage (-> dim_usage), id_periode (-> dim_periode), "
            "id_nature_quittance (-> dim_nature_quittance), "
            "id_nature_annulation (-> dim_nature_annulation — cancellation reason, NOT 'id_nature'), "
            "id_situation_annulation (-> dim_situation_annulation — cancellation status, NOT 'id_situation'). "
            "Columns: ANN02 (annulation year), MOI02 (annulation month), annee_emission, mois_emission, DATEMIS. "
            "Do not use DATE_ANNULATION because it does not exist in this table. "
            "Measures: PNN01 (net cancelled premium), PTT01 (total cancelled premium), "
            "COM01 (cancelled commission), FGA01, BONUSMAL, FRATTES (late fees), TAXFRATTES. "
            "Use to analyze cancellations, churn rate, and cancellation reasons. "
            "'Taux d'annulation' / 'cancellation rate' is COUNT(DISTINCT id_police) from this table divided by "
            "COUNT(DISTINCT id_police) from DWH_FACT_EMISSION, for the same period/grouping."
        ),
        "table_type": "fact",
        "subject": "annulation, cancellation, resiliation, churn, prime annulée, taux d'annulation, cancellation rate, churn rate"
    },
    {
        "id": "fact_annulation_detail",
        "title": "DWH_FACT_ANNULATION_DETAIL",
        "content": (
            "Table dwh.DWH_FACT_ANNULATION_DETAIL stores cancellation amounts by guarantee. "
            "Primary key: ID_DET_ANNULATION. "
            "Connected dimensions: id_garantie (-> dim_garantie), id_police (-> dim_police). "
            "Parent fact: id_annulation (-> DWH_FACT_ANNULATION). "
            "Measures: MT_PRIME (cancelled premium amount per guarantee). "
            "Use to break down cancelled premiums by guarantee type."
        ),
        "table_type": "fact",
        "subject": "annulation detail, garantie, prime annulée par garantie"
    },
    {
        "id": "fact_impaye",
        "title": "DWH_FACT_IMPAYE",
        "content": (
            "Table dwh.DWH_FACT_IMPAYE stores unpaid premium records. "
            "Primary key: ID_IMPAYE. "
            "Connected dimensions (foreign keys): "
            "id_agent (-> dim_agent), id_client (-> dim_client), "
            "id_police (-> dim_police), id_produit (-> dim_produit). "
            "Measures: MT_PRIME_NETTE (unpaid net premium), MT_PRIME_TOTALE (unpaid total premium), "
            "MT_TAXE (unpaid tax), MT_COMMISSION (unpaid commission), MT_ACP. "
            "This table is NOT revenue and must NOT be used for 'chiffre d'affaires', 'revenue', or 'turnover' "
            "questions — those must use DWH_FACT_EMISSION.PRIME_TOTAL instead. "
            "Use for unpaid premium analysis, collection risk scoring, and impayé rate by product/agent."
        ),
        "table_type": "fact",
        "subject": "impayé, unpaid, non-paiement, recouvrement, prime non payée, MT_PRIME_NETTE"
    },
    {
        "id": "fact_sinistre",
        "title": "DWH_FACT_SINISTRE",
        "content": (
            "Table dwh.DWH_FACT_SINISTRE stores insurance claims. "
            "Primary key: id_sinistre. "
            "Connected dimensions (foreign keys): "
            "id_agent (-> dim_agent), id_police (-> dim_police), "
            "id_usage (-> dim_usage), id_garantie (-> dim_garantie), "
            "id_sinistre (-> DIM_SINISTRE — claim characteristics). "
            "Important: id_garantie is in DWH_FACT_SINISTRE, not in DIM_SINISTRE. "
            "Use DWH_FACT_SINISTRE to join to dim_garantie for guarantee breakdowns. "
            "Measures: RGLSIN (settled amount), RGCSIN (counter-settled), RFRSIN (franchise deductible), "
            "INDSIN (indemnity), HONSIN (honorarium), RECSIN (recovery), CLMSIN (total claimed). "
            "Use to analyze claim frequency, severity, and settlement rates by agent/product/guarantee. "
            "The 'ratio S/P' (ratio sinistre/prime, loss ratio, sinistralité) is SUM(RGLSIN) from this table "
            "divided by SUM(PRIME_NETTE) from DWH_FACT_EMISSION, for the same grouping dimension. "
            "'Montant des sinistres' / 'claims amount' is SUM(RGLSIN). 'Indemnisation' / 'indemnity paid' is SUM(INDSIN). "
            "'Fréquence de sinistre' / 'claim frequency' is COUNT(id_sinistre) divided by COUNT(DISTINCT id_police) from DWH_FACT_EMISSION. "
            "'Coût moyen d'un sinistre' / 'average claim cost' / 'severity' is AVG(RGLSIN)."
        ),
        "table_type": "fact",
        "subject": "sinistre, claim, accident, indemnité, sinistralité, RGLSIN, CLMSIN, ratio S/P, loss ratio, ratio sinistre prime, montant des sinistres, claims amount, indemnisation, fréquence de sinistre, claim frequency, coût moyen, average claim cost, severity"
    },
    {
        "id": "fact_reglement",
        "title": "FACT_REGLEMENT",
        "content": (
            "Table dwh.FACT_REGLEMENT stores claim settlement and reimbursement details. "
            "Primary key: id_reglement. "
            "Connected dimensions (foreign keys): "
            "id_sinistre (-> DIM_SINISTRE), id_agent_payeur (-> dim_agent), id_agent_gestionnaire (-> dim_agent), "
            "id_police (-> dim_police), id_usage (-> dim_usage), id_garantie (-> dim_garantie). "
            "Note: there is no id_agent column in FACT_REGLEMENT; use id_agent_payeur or id_agent_gestionnaire. "
            "Measures: brut (gross settlement amount), retenue (withholding), taux (rate), "
            "INDREG (indemnity payment), HONREG (honorarium), AUXREG (auxiliary), "
            "PRCREG (procedure cost), VIDREG, REDREG (recovery). "
            "Use for settlement breakdown, reimbursement analysis, and claims payment reports. "
            "Chain: DWH_FACT_SINISTRE -> DIM_SINISTRE -> FACT_REGLEMENT. "
            "'Montant réglé' / 'règlement' / 'reimbursement amount' means SUM(brut) (gross settlement)."
        ),
        "table_type": "fact",
        "subject": "règlement, settlement, paiement, remboursement, indemnisation, brut, montant réglé, reimbursement amount"
    },
    {
        "id": "dim_agent",
        "title": "dim_agent",
        "content": (
            "Table dwh.dim_agent stores insurance agent/broker information. "
            "Primary key: id_agent. "
            "Columns: code_agent, type_agent (broker/agent/direct channel), "
            "prenom_agent, tel_agent, email_agent, localite_agent, adresse_agent, code_postal, etat_agent, "
            "longitude_agent, latitude_agent (geographical coordinates — NOT 'lat'/'lon', those column names do not exist). "
            "No column named 'nom' or 'agence' exists in dim_agent. "
            "Referenced by: DWH_FACT_EMISSION, DWH_FACT_ANNULATION, DWH_FACT_IMPAYE, "
            "DWH_FACT_SINISTRE, FACT_REGLEMENT via id_agent. "
            "Use for agent performance analysis, distribution network mapping, and commission reports. "
            "Do not assume a column named 'agence' exists unless present in the schema."
        ),
        "table_type": "dimension",
        "subject": "agent, courtier, broker, intermediaire, réseau distribution, locality"
    },
    {
        "id": "dim_client",
        "title": "dim_client",
        "content": (
            "Table dwh.dim_client stores policyholder/customer information. "
            "Primary key: id_client. "
            "Columns: cin_mf (national ID or tax number), nom (last name), prenom (first name), "
            "adresse (address), ville (city), code_postal, sexe (gender — NOT 'genre', that column name does not exist), "
            "date_naissance (birth date, date type), type_client (individual or corporate). "
            "Referenced by: DWH_FACT_EMISSION, DWH_FACT_ANNULATION, DWH_FACT_IMPAYE via id_client. "
            "Also referenced by dim_police.id_client. "
            "For branch grouping, dim_police joins directly to dim_objet (dim_police.id_objet = dim_objet.id_objet); "
            "only join dim_client as well if the question also needs a client-level attribute, filter, or count of distinct clients. "
            "If the user mentions branche, branche/branch-like grouping, or any business branch concept, always use dim_objet.type_objet and never dim_risque.Branche or dim_risque.Sous_Branche. "
            "Avoid using DWH_FACT_SINISTRE unless the question explicitly mentions claims or sinistre data. "
            "'Nombre de clients' / 'number of clients' means COUNT(DISTINCT id_client). "
            "Use for customer segmentation, demographics, and client profiling."
        ),
        "table_type": "dimension",
        "subject": "client, customer, assuré, preneur, personne, démographie, ville, genre, nombre de clients, number of clients"
    },
    {
        "id": "dim_police",
        "title": "dim_police",
        "content": (
            "Table dwh.dim_police stores insurance contract/policy details. "
            "Primary key: id_police. "
            "Foreign keys: id_client (-> dim_client), id_objet (-> dim_objet). "
            "Columns: num_police (contract number), date_effet, type_police (contract type — NOT 'type_contrat'), "
            "num_dernier_avenant, type_duree (duration type — NOT 'duree'), "
            "periodicite_paiement (payment frequency — NOT 'frequence_paiement'), "
            "date_echeance_principale, date_debut_str, date_fin_str, "
            "situation_commerciale (commercial status), situation_comptable (accounting status), hors_taxe, "
            "code_usage_vehicule (NOT 'code_usage'), garantie_assistant, garantie_dommage_collision (specific guarantee flags, not a generic 'guarantees list'). "
            "Referenced by all fact tables via id_police. "
            "'Nombre de polices' / 'number of policies' / 'portfolio size' means COUNT(DISTINCT id_police). "
            "Use for contract portfolio analysis, payment frequency breakdown, and policy status reports."
        ),
        "table_type": "dimension",
        "subject": "police, contrat, contract, portfolio, portefeuille, fréquence paiement, nombre de polices, number of policies, portfolio size"
    },
    {
        "id": "dim_produit",
        "title": "dim_produit",
        "content": (
            "Table dwh.dim_produit stores insurance product definitions. "
            "Primary key: id_produit. "
            "Foreign keys: id_risque (-> dim_risque — product belongs to a risk family). "
            "Columns: code_produit, lib_produit (product label/name). "
            "Referenced by: DWH_FACT_EMISSION, DWH_FACT_ANNULATION, DWH_FACT_IMPAYE via id_produit. "
            "Use for product mix analysis and premium breakdown by product line."
        ),
        "table_type": "dimension",
        "subject": "produit, product, assurance, ligne produit, code produit"
    },
    {
        "id": "dim_risque",
        "title": "dim_risque",
        "content": (
            "Table dwh.dim_risque contains the insurance risk hierarchy. "
            "Primary key: id_risque. "
            "Columns: Code_Risque, Famille_Risque (risk family), Code_Sous_Branche, "
            "Sous_Branche (sub-branch), Branche (top-level branch: Auto, Vie, IRD, Santé). "
            "Referenced by dim_produit.id_risque. "
            "Hierarchy: Branche > Sous_Branche > Famille_Risque > Code_Risque. "
            "However, when the user asks about branche/branch grouping for clients, do not use this table; use dim_objet.type_objet instead."
        ),
        "table_type": "dimension",
        "subject": "risque, branche, sous-branche, famille risque, auto, vie, IRD, santé, hiérarchie"
    },
    {
        "id": "dim_usage",
        "title": "dim_usage",
        "content": (
            "Table dwh.dim_usage stores vehicle usage categories. "
            "Primary key: id_usage. "
            "Columns: code_usage, lib_usage (e.g. Particulier, Taxi, Transport en commun, Utilitaire). "
            "Referenced by: DWH_FACT_EMISSION, DWH_FACT_ANNULATION, DWH_FACT_SINISTRE, FACT_REGLEMENT. "
            "Use to segment auto insurance portfolio and claims by vehicle usage type."
        ),
        "table_type": "dimension",
        "subject": "usage, utilisation véhicule, taxi, particulier, transport, utilitaire"
    },
    {
        "id": "dim_garantie",
        "title": "dim_garantie",
        "content": (
            "Table dwh.dim_garantie stores insurance guarantee/coverage types. "
            "Primary key: id_garantie. "
            "Columns: code_garantie, lib_garantie (label e.g. RC Civile, Vol, Incendie, "
            "Bris de glace, Corporel, Dommages matériels), type_garantie. "
            "Referenced by: DWH_FACT_SINISTRE, FACT_REGLEMENT, "
            "DWH_FACT_EMISSION_DETAIL, DWH_FACT_ANNULATION_DETAIL via id_garantie. "
            "Use to break down premiums, claims, and settlements by coverage type."
        ),
        "table_type": "dimension",
        "subject": "garantie, couverture, RC, vol, incendie, bris de glace, corporel, dommages"
    },
    {
        "id": "dim_periode",
        "title": "dim_periode",
        "content": (
            "Table dwh.dim_periode stores insurance period categories. "
            "Primary key: id_periode. "
            "Columns: code_periode, lib_periode (period label). "
            "Referenced by: DWH_FACT_EMISSION, DWH_FACT_ANNULATION via id_periode. "
            "Use to filter emission and cancellation facts by insurance period type."
        ),
        "table_type": "dimension",
        "subject": "période, period, durée assurance"
    },
    {
        "id": "dim_etat_quittance",
        "title": "dim_etat_quittance",
        "content": (
            "Table dwh.dim_etat_quittance describes the payment status of a receipt (quittance). "
            "Primary key: id_etat_quittance. "
            "Columns: code_etat_quittance, lib_etat_quittance (e.g. Payée, Impayée, Annulée, En attente). "
            "Referenced by: DWH_FACT_EMISSION via id_etat_quittance. "
            "Use to filter emission records by payment status (paid vs unpaid vs cancelled)."
        ),
        "table_type": "dimension",
        "subject": "état quittance, statut paiement, payé, impayé, annulé, receipt status"
    },
    {
        "id": "dim_nature_quittance",
        "title": "dim_nature_quittance",
        "content": (
            "Table dwh.dim_nature_quittance describes the type/nature of a receipt. "
            "Primary key: id_nature_quittance. "
            "Columns: code_nature_quittance, lib_nature_quittance "
            "(e.g. Nouvelle affaire, Renouvellement, Avenant, Ristourne). "
            "Referenced by: DWH_FACT_EMISSION and DWH_FACT_ANNULATION via id_nature_quittance. "
            "Use to distinguish between new business, renewals, endorsements, and refunds."
        ),
        "table_type": "dimension",
        "subject": "nature quittance, type quittance, nouvelle affaire, renouvellement, avenant, ristourne"
    },
    {
        "id": "dim_nature_annulation",
        "title": "dim_nature_annulation",
        "content": (
            "Table dwh.dim_nature_annulation stores reasons for policy cancellation. "
            "Primary key: id_nature. Column: nature_annulation (the reason label). "
            "Referenced by: DWH_FACT_ANNULATION via id_nature_annulation (NOT 'id_nature'). "
            "Use to classify and count cancellations by reason (e.g. non-payment, client request, expiry)."
        ),
        "table_type": "dimension",
        "subject": "nature annulation, motif annulation, raison résiliation, cause annulation"
    },
    {
        "id": "dim_situation_annulation",
        "title": "dim_situation_annulation",
        "content": (
            "Table dwh.dim_situation_annulation stores the processing status of a cancellation. "
            "Primary key: id_situation. Column: situation_annulation (the status label). "
            "Referenced by: DWH_FACT_ANNULATION via id_situation_annulation (NOT 'id_situation'). "
            "Use to track whether a cancellation is pending, confirmed, or reversed."
        ),
        "table_type": "dimension",
        "subject": "situation annulation, statut annulation, traitement résiliation"
    },
    {
        "id": "dim_sinistre",
        "title": "DIM_SINISTRE",
        "content": (
            "Table dwh.DIM_SINISTRE describes claim characteristics. "
            "Primary key: id_sinistre. "
            "Columns: branche (insurance branch of the claim), "
            "nature_sinistre (claim type: accident, theft, fire, etc.), "
            "status_sinistre (claim status: open, closed, pending), "
            "OUVSIT (opening date, integer YYYYMMDD), BARSIN (closing date, integer YYYYMMDD). "
            "Referenced by: DWH_FACT_SINISTRE and FACT_REGLEMENT via id_sinistre. "
            "Claim chain: DWH_FACT_SINISTRE -> DIM_SINISTRE -> FACT_REGLEMENT."
        ),
        "table_type": "dimension",
        "subject": "sinistre dimension, nature sinistre, statut sinistre, ouverture, clôture"
    },
    {
        "id": "dim_objet",
        "title": "dim_objet",
        "content": (
            "Table dwh.dim_objet stores the insured object information. "
            "Primary key: id_objet. "
            "Columns: code_objet, type_objet (e.g. Véhicule, Immeuble, Personne). "
            "Referenced by: dim_police.id_objet. "
            "Parent of dim_vehicule, dim_objet_irds, dim_objet_sante (specialized subtypes). "
            "If you need branch or object-type grouping for clients, use dim_objet.type_objet as the preferred path. "
            "This is faster and easier to reach than DWH_FACT_SINISTRE for client branch analysis. "
            "Use to identify what is being insured under each policy."
        ),
        "table_type": "dimension",
        "subject": "objet assuré, bien assuré, type objet, véhicule, immeuble"
    },
    {
        "id": "dim_objet_irds",
        "title": "dim_objet_irds",
        "content": (
            "Table dwh.dim_objet_irds stores object details for IRDS branch (Incendie, Risques Divers, Santé). "
            "Primary key: id_objet_irds. "
            "Columns: risk family and branch information specific to IRDS objects. "
            "Use for IRDS branch object classification and non-auto risk analysis."
        ),
        "table_type": "dimension",
        "subject": "IRDS, incendie, risques divers, objet IRD, branche non-auto"
    },
    {
        "id": "dim_objet_sante",
        "title": "dim_objet_sante",
        "content": (
            "Table dwh.dim_objet_sante stores object details for health insurance (Santé). "
            "Primary key: id_objet_sante. "
            "Columns: risk family and branch information for health objects. "
            "Use for health insurance object classification and santé branch analysis."
        ),
        "table_type": "dimension",
        "subject": "santé, health, assurance santé, objet santé, branche santé"
    },
    {
        "id": "dim_vehicule",
        "title": "dim_vehicule",
        "content": (
            "Table dwh.dim_vehicule stores insured vehicle details. "
            "Primary key: id_vehicule. "
            "Columns: serie (chassis/serial number — NOT 'num_serie'), immatriculation (licence plate), "
            "date_mise_circulation, marque (brand/make), type_vehicule (vehicle type), genre_vehicule, categorie_tarifaire, "
            "puissance (engine power in CV), nb_place (number of seats — NOT 'nb_places'), charge_utile, "
            "poids_total (weight — NOT 'poids'). "
            "Subtype of dim_objet, used for auto insurance branch. "
            "Use for vehicle fleet analysis, auto risk segmentation, and vehicle profiling."
        ),
        "table_type": "dimension",
        "subject": "vehicule, voiture, auto, immatriculation, marque, puissance, flotte automobile"
    },
    {
        "id": "dim_date",
        "title": "DimDate",
        "content": (
            "Table dwh.DimDate is the shared calendar dimension for all time-based analysis. "
            "Primary key: DateKey (integer YYYYMMDD). "
            "Columns: Day, Week, Month, Quarter, Year, MonthYear, "
            "first day of period, last day of period. "
            "All date foreign keys in fact tables (e.g. in dim_periode or directly on facts) "
            "can be joined to DateKey. "
            "Use for time-series analysis, monthly/quarterly trends, YoY comparisons, "
            "and period-over-period reporting."
        ),
        "table_type": "dimension",
        "subject": "date, calendrier, mois, trimestre, année, tendance, évolution, période, DateKey"
    }
]

embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

add_documents = not os.path.exists(DB_LOCATION)

vector_store = Chroma(
    collection_name="dwh_schema",
    persist_directory=DB_LOCATION,
    embedding_function=embeddings,
)

if add_documents:
    documents = []
    ids = []
    for entry in SCHEMA_DOCUMENTS:
        doc = Document(
            page_content=entry["title"] + " — " + entry["content"],
            metadata={
                "table": entry["title"],
                "type": entry["table_type"],
                "subject": entry["subject"],
            },
            id=entry["id"],
        )
        documents.append(doc)
        ids.append(entry["id"])
    vector_store.add_documents(documents=documents, ids=ids)
    print(f"Embedded {len(documents)} table descriptions into ChromaDB.")
else:
    print(f"ChromaDB loaded from {DB_LOCATION}.")

retriever = vector_store.as_retriever(
    search_kwargs={"k": 4}
)
