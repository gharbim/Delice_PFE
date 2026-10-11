"""summary.py — Accueil home page: static stats for the "Vos données" cards.

The DWH connection (SQL Server on a laptop host) proved unreliable —
connection attempts and the aggregate query itself were timing out
intermittently — so these figures are hardcoded from the last known-good
snapshot instead of being queried live. No DWH connection is made here.
"""

# Original live-DWH implementation, kept for reference / rollback:
#
# from datetime import date
#
# from django.core.cache import cache
#
# from api.chatbot.agent import get_connection
#
# CACHE_KEY = "dwh_summary"
# CACHE_TTL_SECONDS = None  # never expire — re-fetch only via force_refresh
#
# _SUMMARY_QUERY = """
#     SELECT
#         (SELECT COUNT(*) FROM dwh.dim_police) AS total_policies,
#         (SELECT COUNT(*) FROM dwh.dim_client) AS total_clients,
#         (SELECT COUNT(*) FROM dwh.DWH_FACT_SINISTRE) AS total_claims,
#         e.total_policies_issued,
#         e.total_premium,
#         e.min_date,
#         e.max_date
#     FROM (
#         SELECT COUNT(*) AS total_policies_issued, SUM(PRIME_TOTAL) AS total_premium,
#                MIN(Date_Emission) AS min_date, MAX(Date_Emission) AS max_date
#         FROM dwh.DWH_FACT_EMISSION
#     ) e
# """
#
#
# def _format_date_key(date_key):
#     if date_key is None:
#         return None
#     s = str(int(date_key))
#     return date(int(s[:4]), int(s[4:6]), int(s[6:8])).isoformat()
#
#
# def get_dwh_summary() -> dict:
#     cached = cache.get(CACHE_KEY)
#     if cached is not None:
#         return cached
#
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(_SUMMARY_QUERY)
#     total_policies, total_clients, total_claims, total_policies_issued, total_premium, min_date, max_date = cursor.fetchone()
#
#     result = {
#         "success": True,
#         "total_policies": int(total_policies),
#         "total_clients": int(total_clients),
#         "total_claims": int(total_claims),
#         "total_premium": float(total_premium) if total_premium is not None else 0.0,
#         "total_quittances": int(total_policies_issued),
#         "data_from": _format_date_key(min_date),
#         "data_to": _format_date_key(max_date),
#     }
#     cache.set(CACHE_KEY, result, CACHE_TTL_SECONDS)
#     return result

_STATIC_SUMMARY = {
    "success": True,
    "total_policies": 50000,
    "total_clients": 49982,
    "total_claims": 14675,
    "total_premium": 86920271.0,
}


def get_dwh_summary() -> dict:
    return _STATIC_SUMMARY
