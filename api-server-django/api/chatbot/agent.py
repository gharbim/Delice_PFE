import os
import re
import logging
import pyodbc
from pathlib import Path
import pandas as pd

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from .vector import retriever

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

DB_CONFIG = {
    "server": os.getenv("DWH_DB_SERVER", "LAPTOP-402BL468"),
    "port": os.getenv("DWH_DB_PORT", "1433"),
    "database": os.getenv("DWH_DB_NAME", "DWH_DB"),
    "driver": os.getenv("DWH_DB_DRIVER", "ODBC Driver 17 for SQL Server"),
    "uid": os.getenv("DWH_DB_USER", "KEYRUS_PFE"),
    "pwd": os.getenv("DWH_DB_PASSWORD", "keyrus"),
    "login_timeout": int(os.getenv("DWH_DB_LOGIN_TIMEOUT", "10")),
    "query_timeout": int(os.getenv("DWH_DB_QUERY_TIMEOUT", "30")),
}

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "lm-studio")


def get_connection():
    parts = [
        f"DRIVER={{{DB_CONFIG['driver']}}}",
        # Force explicit TCP + port instead of a bare hostname: letting the ODBC driver
        # auto-negotiate the transport (shared memory / named pipes / TCP) can hang for
        # a long time on some machines instead of failing fast or connecting.
        f"SERVER=tcp:{DB_CONFIG['server']},{DB_CONFIG['port']}",
        f"DATABASE={DB_CONFIG['database']}",
        f"UID={DB_CONFIG['uid']}",
        f"PWD={DB_CONFIG['pwd']}",
    ]
    # Login/query timeouts aren't valid connection-string keywords for this driver —
    # they have to be set via pyodbc's own timeout params, otherwise a bad connection
    # can hang indefinitely instead of failing fast.
    conn = pyodbc.connect(";".join(parts), autocommit=True, timeout=DB_CONFIG["login_timeout"])
    conn.timeout = DB_CONFIG["query_timeout"]
    return conn


def is_timeout_error(error: str) -> bool:
    lowered = str(error or "").lower()
    return "hyt00" in lowered or "timeout" in lowered or "délai d'attente" in lowered


def get_user_friendly_error_message(error: str) -> str:
    detail = str(error or "")
    lowered = detail.lower()

    if is_timeout_error(detail):
        return (
            "The database took too long to respond and the query timed out. "
            "This usually means the database server is under heavy load right now, "
            "not that the question was invalid — please try again in a moment."
        )

    if "column" in lowered or "invalid" in lowered or "nom de colonne" in lowered:
        return (
            "The database query failed because the schema mapping was invalid. "
            "Please rephrase the question or try a simpler version."
        )

    if "blocked" in lowered:
        return "I blocked that request because it was not a safe read-only query."

    return (
        "I hit a database issue while answering your question. "
        "Please rephrase the request and try again."
    )


def run_sql(query: str, max_rows: int = 50) -> str:
    forbidden = ["drop", "delete", "truncate", "insert", "update", "alter"]
    for word in forbidden:
        if re.search(rf"\b{word}\b", query.lower()):
            return f"Blocked: {word.upper()} is not allowed."
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            columns = [column[0] for column in cursor.description] if cursor.description else []
            rows = cursor.fetchmany(max_rows + 1)

        if not rows:
            return "No rows returned."

        result_rows = rows[:max_rows]
        lines = []
        if columns:
            header = ' | '.join(columns)
            lines.append(header)
            lines.append('-' * len(header))
        for row in result_rows:
            lines.append(' | '.join(str(value) for value in row))

        if len(rows) > max_rows:
            lines.append(f"... ({max_rows} of more than {len(rows)} rows shown)")

        return '\n'.join(lines)
    except Exception as e:
        raise RuntimeError(f"SQL execution failed: {e}")


def extract_sql(text: str) -> str:
    match = re.search(r"```sql\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        candidate = match.group(1).strip()
    else:
        match = re.search(r"```\s*(SELECT\s+.+?)```", text, re.DOTALL | re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
        else:
            match = re.search(r"(SELECT\s+.+)", text, re.DOTALL | re.IGNORECASE)
            candidate = match.group(1).strip() if match else ""

    if not candidate:
        return ""

    # The model sometimes appends a trailing natural-language explanation after
    # the actual statement (e.g. "...ORDER BY x DESC;\n\nThis query will return...").
    # A semicolon reliably marks the end of the statement, so drop everything after it.
    semicolon_index = candidate.find(";")
    if semicolon_index != -1:
        candidate = candidate[: semicolon_index + 1]

    # Fallback for the same problem when no semicolon is present: a blank line
    # followed by prose with no SQL keywords is almost certainly commentary.
    blank_line_match = re.search(r"\n\s*\n", candidate)
    if blank_line_match:
        tail = candidate[blank_line_match.end():]
        if tail.strip() and not re.search(r"\b(SELECT|FROM|WHERE|JOIN|GROUP\s+BY|ORDER\s+BY|HAVING)\b", tail, re.IGNORECASE):
            candidate = candidate[: blank_line_match.start()]

    return candidate.strip()


def question_mentions_year(question: str) -> bool:
    return bool(re.search(r"\b(?:19|20)\d{2}\b", question))


def remove_unasked_year_filters(query: str, question: str) -> str:
    if question_mentions_year(question):
        return query

    query = re.sub(
        r"(?i)\bWHERE\b\s+[^;]*\b(?:ANNEE_ECHEANCE|ANNEE_EMISSION|ANNEE)\b[^;]*\b=\s*(?:19|20)\d{2}\b\s*(?:;|$)",
        "",
        query,
    )
    query = re.sub(
        r"(?i)\s*\bAND\b\s+[^;]*\b(?:ANNEE_ECHEANCE|ANNEE_EMISSION|ANNEE)\b[^;]*\b=\s*(?:19|20)\d{2}\b\s*(?:;|$)",
        "",
        query,
    )
    query = re.sub(r"(?i)\bWHERE\b\s*(?:;|$)", "", query)
    return query.strip()


_SQL_KEYWORDS = (
    "ON|WHERE|GROUP|ORDER|HAVING|JOIN|INNER|LEFT|RIGHT|FULL|OUTER|CROSS|UNION"
)


def extract_table_alias(query: str, table_name: str) -> str:
    match = re.search(
        rf"\b(?:FROM|JOIN)\s+dwh\.{table_name}\b\s+(?:AS\s+)?(?!(?:{_SQL_KEYWORDS})\b)([A-Za-z_][A-Za-z0-9_]*)\b",
        query,
        re.IGNORECASE,
    )
    return match.group(1) if match else ""


def ensure_table_alias(query: str, table_name: str, alias: str) -> str:
    pattern = rf"\b((?:FROM|JOIN)\s+dwh\.{table_name})\b(?!\s+AS?\s+[A-Za-z_][A-Za-z0-9_]*)"
    return re.sub(pattern, rf"\1 {alias}", query, flags=re.IGNORECASE)


def qualify_unqualified_column(query: str, column_name: str, alias: str) -> str:
    if not alias:
        return query
    pattern = rf"(?<![\w\.]){column_name}(?![\w\.])"
    return re.sub(pattern, f"{alias}.{column_name}", query, flags=re.IGNORECASE)


def fix_fact_reglement_reference(query: str) -> str:
    query = re.sub(r"\bdwh\.DWH_FACT_REGLEMENT\b", "dwh.FACT_REGLEMENT", query, flags=re.IGNORECASE)
    query = re.sub(r"\bDWH_FACT_REGLEMENT\b", "FACT_REGLEMENT", query, flags=re.IGNORECASE)

    if re.search(r"\bFROM\s+(?:dwh\.)?FACT_REGLEMENT\b", query, re.IGNORECASE):
        query = re.sub(
            r"\bFROM\s+(?:dwh\.)?FACT_REGLEMENT\b",
            "FROM dwh.FACT_REGLEMENT AS fact",
            query,
            flags=re.IGNORECASE,
        )

    if re.search(r"\bJOIN\s+(?:dwh\.)?FACT_REGLEMENT\b", query, re.IGNORECASE):
        query = re.sub(
            r"\bJOIN\s+(?:dwh\.)?FACT_REGLEMENT\b",
            "JOIN dwh.FACT_REGLEMENT AS fact",
            query,
            flags=re.IGNORECASE,
        )

    query = re.sub(r"\bFACT_REGLEMENT\.(\w+)\b", r"fact.\1", query, flags=re.IGNORECASE)
    query = re.sub(r"\bfact\.id_agent\b", "fact.id_agent_payeur", query, flags=re.IGNORECASE)
    query = re.sub(r"\bdim_agent\.(?:nom|agence)\b", "dim_agent.code_agent", query, flags=re.IGNORECASE)
    query = re.sub(r"\bDATE_ANNULATION\b", "ANN02", query, flags=re.IGNORECASE)

    return query


def qualify_ambiguous_columns(query: str) -> str:
    """Auto-qualifies bare column references that the model left ambiguous.

    Several dimension/fact tables in this schema share column names
    (id_agent, id_client, id_police...). If a column shows up qualified with
    two different tables anywhere in the query (e.g. in the JOIN condition),
    any bare occurrence of that column elsewhere (SELECT/GROUP BY/ORDER BY)
    is genuinely ambiguous to SQL Server. Since the join condition equates
    both sides, qualifying with the query's primary FROM table is safe and
    produces identical results either way.
    """
    qualified_refs = re.findall(r"\b((?:dwh\.)?[A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)\b", query)
    column_to_tables = {}
    for table, column in qualified_refs:
        column_to_tables.setdefault(column.lower(), set()).add(table.lower())

    ambiguous_columns = [col for col, tables in column_to_tables.items() if len(tables) > 1]
    if not ambiguous_columns:
        return query

    from_match = re.search(r"\bFROM\s+((?:dwh\.)?[A-Za-z_][A-Za-z0-9_]*)\b", query, re.IGNORECASE)
    if not from_match:
        return query
    primary_table = from_match.group(1)

    for col in ambiguous_columns:
        pattern = rf"(?<![\w.]){col}\b(?!\s*\.)(?!\s*\()"
        query = re.sub(pattern, f"{primary_table}.{col}", query, flags=re.IGNORECASE)

    return query


def fix_garantie_sinistre_join(query: str) -> str:
    if re.search(r"\bdwh\.dim_garantie\b", query, re.IGNORECASE) and re.search(r"\bdwh\.DIM_SINISTRE\b", query, re.IGNORECASE):
        if re.search(r"\bdim_garantie\.id_garantie\b", query, re.IGNORECASE) and re.search(r"\bDIM_SINISTRE\.id_garantie\b", query, re.IGNORECASE):
            query = re.sub(r"\bdwh\.DIM_SINISTRE\b", "dwh.DWH_FACT_SINISTRE", query, flags=re.IGNORECASE)
            query = re.sub(r"\bDIM_SINISTRE\b", "DWH_FACT_SINISTRE", query, flags=re.IGNORECASE)
    return query


_TYPE_OBJET_LITERAL_BRANCHE_COND = (
    r"(?:[\w.]*\.)?type_objet\s*"
    r"(?:=\s*'[^']*(?:branche|branch)[^']*'|LIKE\s*'%[^']*(?:branche|branch)[^']*%')"
)


def fix_branche_literal_filter(query: str, question: str) -> str:
    """Small local models sometimes read "by branche"/"par branche" as an
    instruction to FILTER on the literal word "branche" (e.g.
    WHERE type_objet LIKE '%branche%') instead of GROUPING by
    dim_objet.type_objet. "branche"/"branch" is never an actual value in the
    database (real values are Véhicule/Immeuble/Personne), so any such filter
    always yields zero rows. Strip it, and if the question asked for a
    per-branch breakdown, add the missing GROUP BY so the result reflects
    that intent instead of silently collapsing to an unfiltered total.
    """
    if not re.search(r"\bbranche\b|\bbranch\b", question, re.IGNORECASE):
        return query

    had_filter = bool(re.search(_TYPE_OBJET_LITERAL_BRANCHE_COND, query, re.IGNORECASE))
    if not had_filter:
        return query

    query = re.sub(rf"(?i)\bAND\s+{_TYPE_OBJET_LITERAL_BRANCHE_COND}", "", query)
    query = re.sub(rf"(?i){_TYPE_OBJET_LITERAL_BRANCHE_COND}\s+AND\s+", "", query)
    query = re.sub(rf"(?i)\bWHERE\s+{_TYPE_OBJET_LITERAL_BRANCHE_COND}", "", query)
    query = re.sub(r"(?i)\bWHERE\s*(?=GROUP\s+BY|ORDER\s+BY|$)", "", query).strip()

    wants_breakdown = re.search(r"\b(?:by|per|par)\b", question, re.IGNORECASE)
    if wants_breakdown and not re.search(r"\bGROUP\s+BY\b", query, re.IGNORECASE):
        alias = extract_table_alias(query, "dim_objet")
        objet_ref = f"{alias}.type_objet" if alias else "dwh.dim_objet.type_objet"
        query = re.sub(r"(?i)\bSELECT\b", f"SELECT {objet_ref},", query, count=1)
        query = query.rstrip() + f" GROUP BY {objet_ref}"

    return query


def fix_sql(query: str, question: str) -> str:
    query = query.rstrip("; \n\t")
    query = fix_fact_reglement_reference(query)
    query = fix_garantie_sinistre_join(query)

    if re.search(r"\bbranche\b|\bbranch\b", question, re.IGNORECASE):
        query = re.sub(r"\b(?:d|dim_risque)\.branche\b", "dim_objet.type_objet", query, flags=re.IGNORECASE)
        query = re.sub(r"\b(?:d|dim_risque)\.sous_branche\b", "dim_objet.type_objet", query, flags=re.IGNORECASE)
        query = re.sub(r"\b(?:d|dim_risque)\.famille_risque\b", "dim_objet.type_objet", query, flags=re.IGNORECASE)
        query = re.sub(r"\bFROM\s+dwh\.dim_risque\b", "FROM dwh.dim_objet", query, flags=re.IGNORECASE)
        query = re.sub(r"\bJOIN\s+dwh\.dim_risque\b", "JOIN dwh.dim_objet", query, flags=re.IGNORECASE)
        query = re.sub(r"\bJOIN\s+dim_risque\b", "JOIN dwh.dim_objet", query, flags=re.IGNORECASE)
        query = re.sub(r"\bFROM\s+dim_risque\b", "FROM dwh.dim_objet", query, flags=re.IGNORECASE)
        query = re.sub(r"\bdwh\.dim_risque\b", "dwh.dim_objet", query, flags=re.IGNORECASE)
        query = re.sub(r"\bdim_risque\b", "dim_objet", query, flags=re.IGNORECASE)
        query = fix_branche_literal_filter(query, question)

    limit_match = re.search(r"\bLIMIT\s+(\d+)\b", query, re.IGNORECASE)
    if limit_match:
        n = limit_match.group(1)
        query = re.sub(r"\bLIMIT\s+\d+\b", "", query, flags=re.IGNORECASE).strip()
        query = re.sub(r"\bSELECT\b", f"SELECT TOP {n}", query, count=1, flags=re.IGNORECASE)

    top_end_match = re.search(r"(.*?)\s+TOP\s+(\d+)\s*;?\s*$", query, re.IGNORECASE | re.DOTALL)
    if top_end_match:
        body = top_end_match.group(1).strip()
        n = top_end_match.group(2)
        if not re.search(r"^\s*SELECT\s+TOP\b", body, re.IGNORECASE):
            query = re.sub(r"\bSELECT\b", f"SELECT TOP {n}", body, count=1, flags=re.IGNORECASE)

    if re.search(r"^\s*SELECT\s+TOP\s+\d+\b", query, re.IGNORECASE):
        if (
            re.search(
                r"\bCOUNT\s*\(|\bSUM\s*\(|\bAVG\s*\(|\bMIN\s*\(|\bMAX\s*\(|\bDISTINCT\b|\bGROUP\s+BY\b|\bHAVING\b|\bUNION\b|\bINTERSECT\b|\bEXCEPT\b|\bFROM\s+information_schema\b",
                query,
                re.IGNORECASE,
            )
            and not re.search(r"\bORDER\s+BY\b", query, re.IGNORECASE)
        ):
            query = re.sub(r"^\s*(SELECT)\s+TOP\s+\d+\s+", r"\1 ", query, flags=re.IGNORECASE)

    query = re.sub(
        r"\b(FROM|JOIN)\s+(?!dwh\.|information_schema\.|sys\.|#)([A-Za-z_][A-Za-z0-9_]*)\b",
        lambda m: f"{m.group(1)} dwh.{m.group(2)}",
        query,
        flags=re.IGNORECASE,
    )

    query = qualify_ambiguous_columns(query)

    if re.search(r"\bd\.id_client\b", query, re.IGNORECASE) and re.search(r"\bFROM\b.*\bf\b", query, re.IGNORECASE) and not re.search(r"\bd\b\s+AS\b", query, re.IGNORECASE):
        query = re.sub(r"\bd\.id_client\b", "f.id_client", query, flags=re.IGNORECASE)

    if not re.search(r"\bSELECT\s+TOP\b", query, re.IGNORECASE):
        if not re.search(r"\bCOUNT\s*\(|\bSUM\s*\(|\bAVG\s*\(|\bMIN\s*\(|\bMAX\s*\(|\bDISTINCT\b|\bGROUP\s+BY\b|\bHAVING\b|\bUNION\b|\bINTERSECT\b|\bEXCEPT\b|\bFROM\s+information_schema\b",
                         query,
                         re.IGNORECASE,
        ):
            query = re.sub(r"\bSELECT\b", "SELECT TOP 50", query, count=1, flags=re.IGNORECASE)

    query = re.sub(r"\bschema_name\s*=", "TABLE_SCHEMA =", query, flags=re.IGNORECASE)
    query = remove_unasked_year_filters(query, question)
    return query.strip()


model = ChatOpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    temperature=0,
)

# Domain (insurance) business terminology, split into categories so only the
# categories relevant to a given question are injected into the prompt (this
# block was measured at ~860 tokens — over half the static prompt — and was
# the single biggest lever for cutting prompt-processing latency on constrained
# local-LLM hardware).
_BUSINESS_RULES_HEADER = (
    "8. INSURANCE BUSINESS TERMINOLOGY — these mappings are fixed, apply them "
    "even if the retrieved schema above doesn't repeat them:\n"
)

_REVENUE_PREMIUM_RULES = """
   Revenue & premium:
   - "chiffre d'affaires", "revenue", "turnover", "CA", or "primes émises" (for an agent, product, branch, or overall) means SUM(dwh.DWH_FACT_EMISSION.PRIME_TOTAL), grouped by the relevant dimension. NEVER use dwh.DWH_FACT_IMPAYE for these questions — that table only holds unpaid/outstanding premiums, not revenue.
   - "prime nette" / "net premium" means dwh.DWH_FACT_EMISSION.PRIME_NETTE.
   - "taxe" / "tax amount" means dwh.DWH_FACT_EMISSION.TAXE.
   - "commission totale" / "total commission" / "commission d'agent" / "agent commission" means SUM(dwh.DWH_FACT_EMISSION.COMMISSION), grouped by dim_agent for per-agent breakdowns.
   - "bonus-malus" means dwh.DWH_FACT_EMISSION.BONUS_MALUS.
   - "nouvelle affaire" / "new business" means DWH_FACT_EMISSION filtered where dim_nature_quittance.lib_nature_quittance = 'Nouvelle affaire' (join via id_nature_quittance).
   - "renouvellement" / "renewal" means DWH_FACT_EMISSION filtered where dim_nature_quittance.lib_nature_quittance = 'Renouvellement' (join via id_nature_quittance).
"""

_CANCELLATION_RULES = """
   Cancellations:
   - "prime annulée" / "cancelled premium" means dwh.DWH_FACT_ANNULATION.PTT01 (total) or PNN01 (net), NOT PRIME_TOTAL/PRIME_NETTE (those belong to DWH_FACT_EMISSION).
   - "taux d'annulation", "cancellation rate", or "churn rate" means COUNT(DISTINCT dwh.DWH_FACT_ANNULATION.id_police) divided by COUNT(DISTINCT dwh.DWH_FACT_EMISSION.id_police) for the same period/grouping (ratio of cancelled to issued policies). Use NULLIF(denominator, 0).
"""

_CLAIMS_LOSS_RATIO_RULES = """
   Claims & loss ratio:
   - "ratio S/P", "ratio sinistre/prime", "loss ratio", or "sinistralité" means SUM(dwh.DWH_FACT_SINISTRE.RGLSIN) divided by SUM(dwh.DWH_FACT_EMISSION.PRIME_NETTE), computed for the same grouping dimension and any period filters given in the question. Compute the two sums separately (two aggregated CTEs or subqueries joined on the grouping key) and divide using NULLIF(denominator, 0) to avoid division by zero.
   - "montant des sinistres", "claims amount", or "claims cost" means SUM(dwh.DWH_FACT_SINISTRE.RGLSIN) (the settled claim amount).
   - "indemnisation" / "indemnity paid" means SUM(dwh.DWH_FACT_SINISTRE.INDSIN).
   - "fréquence de sinistre" / "claim frequency" means COUNT(dwh.DWH_FACT_SINISTRE.id_sinistre) divided by COUNT(DISTINCT dwh.DWH_FACT_EMISSION.id_police), i.e. claims per policy. Use NULLIF(denominator, 0).
   - "coût moyen d'un sinistre", "average claim cost", or "severity" means AVG(dwh.DWH_FACT_SINISTRE.RGLSIN).
   - "montant réglé", "règlement", or "reimbursement amount" means SUM(dwh.FACT_REGLEMENT.brut) (gross settlement), following the chain DWH_FACT_SINISTRE -> DIM_SINISTRE -> FACT_REGLEMENT.
"""

_PORTFOLIO_COUNTS_RULES = """
   Portfolio & counts:
   - "impayé", "unpaid", "arriérés", or "outstanding premium" means dwh.DWH_FACT_IMPAYE measures (MT_PRIME_NETTE, MT_PRIME_TOTALE, MT_TAXE, MT_COMMISSION, MT_ACP) — only use this table when the question is specifically about unpaid or outstanding amounts, never for revenue/turnover/chiffre d'affaires questions.
   - "nombre de polices", "number of policies", or "portfolio size" means COUNT(DISTINCT dwh.dim_police.id_police) (or COUNT(DISTINCT id_police) on DWH_FACT_EMISSION if filtering by emission activity).
   - "nombre de clients" / "number of clients" means COUNT(DISTINCT dwh.dim_client.id_client).
"""

_BUSINESS_RULE_CATEGORIES = [
    (_REVENUE_PREMIUM_RULES, re.compile(
        r"chiffre d.affaire|\bca\b|revenue|turnover|prime nette|net premium|primes? émises?|\btaxe\b|tax amount|"
        r"commission|bonus.?malus|nouvelle affaire|new business|renouvellement|renewal|\bprime\b|premium",
        re.IGNORECASE
    )),
    (_CANCELLATION_RULES, re.compile(r"annul|cancel|résiliation|resiliation|churn", re.IGNORECASE)),
    (_CLAIMS_LOSS_RATIO_RULES, re.compile(
        r"sinistr|ratio s.?p|loss ratio|indemni|règlement|reglement|claim|severity|co[uû]t moyen",
        re.IGNORECASE
    )),
    (_PORTFOLIO_COUNTS_RULES, re.compile(
        r"impay|unpaid|arriér|arriere|outstanding|portfolio|portefeuille|"
        r"(?:nombre|combien) de (?:polices?|clients?)|(?:number|how many) (?:of )?(?:polic|client)",
        re.IGNORECASE
    )),
]


def build_business_rules(question: str) -> str:
    """Only include the business-terminology categories relevant to this question.

    Falls back to including every category if none match, so an unrecognized
    phrasing never silently loses guidance — it just costs the full token price
    on that one call instead of guessing wrong.
    """
    matched = [text for text, pattern in _BUSINESS_RULE_CATEGORIES if pattern.search(question)]
    if not matched:
        matched = [text for text, _ in _BUSINESS_RULE_CATEGORIES]
    return _BUSINESS_RULES_HEADER + "".join(matched)

sql_template = """
You are a T-SQL expert working with a SQL Server data warehouse called DWH_DB.

Relevant schema:
{schema}

STRICT RULES — follow exactly:

1. Use ONLY SQL Server syntax.
2. NEVER use LIMIT.
3. Always prefix tables with dwh.
4. Dates are stored as integers YYYYMMDD.
4b. Whenever the query joins more than one table, qualify EVERY column reference (in SELECT, GROUP BY, ORDER BY, WHERE, and HAVING — not just the JOIN ON clause) with its table name or alias. Several tables share column names such as id_agent, id_client, and id_police, and leaving any of them unqualified causes a SQL Server "ambiguous column name" error.
4c. Only join a dimension table when the question needs one of its columns, and when you do, SELECT and GROUP BY only the specific column(s) you actually need to answer the question (typically the id and one human-readable label, e.g. dim_agent.code_agent) — never SELECT or GROUP BY every column of a joined table "to be safe." Extra unused columns in GROUP BY change the grouping granularity and risk referencing a column name that does not exist.
4d. Every fact table already carries its dimension foreign keys directly (id_client, id_police, id_agent, id_produit, etc. all live on the fact table itself). If the question only needs to group or aggregate by one of these ids — not a human-readable label or other attribute from the dimension — read the id straight off the fact table and do NOT join the dimension table at all. Example: "top 5 polices par primes totales" needs SUM(PRIME_TOTAL) grouped by id_police, and id_police is already on DWH_FACT_EMISSION, so the correct query is `SELECT TOP 5 id_police, SUM(PRIME_TOTAL) AS total FROM dwh.DWH_FACT_EMISSION GROUP BY id_police ORDER BY total DESC` with no join to dim_police at all. Joining a dimension table purely to re-read an id that is already available on the fact table adds an unnecessary join and slows the query down for no benefit.

5. VERY IMPORTANT RULE (NO ASSUMPTIONS):
   - NEVER assume filters such as YEAR, DATE, REGION, PRODUCT, CLIENT.
   - Only apply filters explicitly mentioned in the user's question.
   - If the user does NOT mention a time period, DO NOT add any WHERE clause on date/year fields.
   - Do not invent filters on fields such as ANNEE_ECHEANCE or ANNEE_EMISSION.
   - Do not invent column names or table columns not present in the provided schema.
   - If the table is DWH_FACT_ANNULATION, use ANN02 and MOI02 for cancellation year/month, not DATE_ANNULATION.
   - If you need guarantee breakdowns, do not join dim_garantie directly to DIM_SINISTRE; use DWH_FACT_SINISTRE as the bridge for id_garantie.
   - Do not use DWH_FACT_SINISTRE for client branch counts unless the user explicitly asks about claims, sinistre, or settlement data.
   - IMPORTANT: whenever the user mentions branche, branch, or branch-like grouping, you MUST use dim_objet.type_objet (join dim_police directly to dim_objet via dim_police.id_objet = dim_objet.id_objet) and MUST NOT use dim_risque.Branche, dim_risque.Sous_Branche, or any other branch column from dim_risque. Only add dim_client to the query if it also needs a client-level attribute or filter (e.g. client name, client segment, client count) — never include dim_client solely to reach dim_objet.
   - CRITICAL: "branche"/"branch" is NEVER a literal data value — it is the NAME of the grouping, not something to filter on. When the question says "by branche"/"par branche"/"by branch", you MUST put dim_objet.type_objet in the SELECT list and GROUP BY it. You MUST NOT write WHERE dim_objet.type_objet = 'branche' or WHERE dim_objet.type_objet LIKE '%branche%' — type_objet's real values are Véhicule, Immeuble, Personne, so filtering on the word "branche" itself always returns zero rows. Example: "total number of policies by branche" -> `SELECT dim_objet.type_objet, COUNT(DISTINCT dim_police.id_police) FROM dwh.dim_police JOIN dwh.dim_objet ON dim_police.id_objet = dim_objet.id_objet GROUP BY dim_objet.type_objet`.
   - DO NOT guess "current year", "2024", or any default period.

6. If aggregation is requested (SUM, COUNT, AVG), compute on ALL available data unless filters are explicitly provided.

7. In INFORMATION_SCHEMA, use TABLE_NAME and TABLE_SCHEMA.

{business_rules}

9. Output ONLY the SQL query.
   - No explanation
   - No markdown
   - No comments

Question: {question}

SQL query:
"""

explain_template = """
You are a Business Intelligence (BI) analyst for an insurance company.

The user asked:
{question}

SQL executed:
{sql}

Real results from the database:
{results}

INSTRUCTIONS:
1. Explain what the result means in simple business terms.
2. Use ONLY information present in the results.
3. Do NOT add external facts (currency, assumptions, missing context).
4. If units or currency are not provided, do NOT add them.
5. Do NOT assume dollars, cents, euros, or any monetary unit.
6. You may rephrase the metric in natural language (e.g. "total premiums", "sum of values").
7. Be concise and helpful.

Return a clear business interpretation strictly based on the data.
"""

repair_template = """
You are a T-SQL expert fixing a broken query for a SQL Server data warehouse called DWH_DB.

Relevant schema:
{schema}

The user's original question was:
{question}

This query was generated but failed to execute:
{sql}

Database error:
{error}

Fix the query so it executes successfully against the schema above, keeping the
same intent as the original question. Do not invent columns or tables that are
not present in the schema.

{business_rules}

Output ONLY the corrected SQL query — no explanation, no markdown, no comments.

Corrected SQL query:
"""

sql_prompt = ChatPromptTemplate.from_template(sql_template)
explain_prompt = ChatPromptTemplate.from_template(explain_template)
repair_prompt = ChatPromptTemplate.from_template(repair_template)
sql_chain = sql_prompt | model
explain_chain = explain_prompt | model
repair_chain = repair_prompt | model


def run_agent(question: str, max_rows: int = 50) -> dict:
    if not question or not question.strip():
        raise ValueError("Question must not be empty.")

    schema_docs = retriever.invoke(question)
    schema_context = "\n\n".join([doc.page_content for doc in schema_docs])
    business_rules = build_business_rules(question)

    sql_response = sql_chain.invoke({"schema": schema_context, "question": question, "business_rules": business_rules})
    sql_text = getattr(sql_response, "content", str(sql_response))
    sql_query = extract_sql(sql_text)
    if not sql_query:
        sql_query = sql_text.strip()

    sql_query = fix_sql(sql_query, question)

    try:
        db_results = run_sql(sql_query, max_rows=max_rows)
    except RuntimeError as first_error:
        logger.warning("Chatbot SQL failed on first attempt (question=%r, sql=%r): %s", question, sql_query, first_error)

        # A timeout means the query never got a chance to prove itself valid or
        # invalid — the SQL is not the problem, so sending it to the repair LLM
        # ("here's a broken query, fix it") only prompts it to hallucinate an
        # unrelated change to a query that was already correct. Fail fast instead.
        if is_timeout_error(str(first_error)):
            raise RuntimeError(get_user_friendly_error_message(str(first_error))) from first_error

        # One self-repair attempt: show the model its own broken query and the
        # database's exact error, and let it correct it (handles hallucinated
        # columns/tables that no regex-based fix can safely guess a replacement for).
        repair_response = repair_chain.invoke({
            "schema": schema_context,
            "question": question,
            "sql": sql_query,
            "error": str(first_error),
            "business_rules": business_rules,
        })
        repair_text = getattr(repair_response, "content", str(repair_response))
        repaired_query = extract_sql(repair_text) or repair_text.strip()
        repaired_query = fix_sql(repaired_query, question)

        try:
            db_results = run_sql(repaired_query, max_rows=max_rows)
            sql_query = repaired_query
        except RuntimeError as second_error:
            logger.error(
                "Chatbot SQL failed after repair attempt (question=%r, sql=%r): %s",
                question, repaired_query, second_error,
            )
            raise RuntimeError(get_user_friendly_error_message(str(second_error))) from second_error

    explain_response = explain_chain.invoke({
        "question": question,
        "sql": sql_query,
        "results": db_results,
    })
    answer = getattr(explain_response, "content", str(explain_response))

    return {
        "success": True,
        "question": question,
        "sql": sql_query,
        "results": db_results,
        "answer": answer,
    }
