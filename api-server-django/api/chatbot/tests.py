import unittest

from api.chatbot.agent import fix_sql, get_user_friendly_error_message


class FixSqlBranchTests(unittest.TestCase):
    def test_rewrites_branch_fields_to_dim_objet(self):
        query = (
            "SELECT d.Branche, COUNT(*) "
            "FROM dwh.dim_client c "
            "JOIN dwh.dim_police p ON c.id_client = p.id_client "
            "JOIN dwh.dim_risque d ON p.id_objet = d.id_risque "
            "GROUP BY d.Branche"
        )

        rewritten = fix_sql(query, "Combien de clients par branche")

        self.assertIn("dim_objet.type_objet", rewritten)
        self.assertNotIn("d.Branche", rewritten)
        self.assertIn("dwh.dim_objet", rewritten)
        self.assertIn("p.id_objet", rewritten)

    def test_strips_literal_branche_filter_and_adds_group_by(self):
        query = (
            "SELECT COUNT(DISTINCT dwh.dim_police.id_police) "
            "FROM dwh.dim_police "
            "JOIN dwh.dim_objet ON dwh.dim_police.id_objet = dwh.dim_objet.id_objet "
            "WHERE dwh.dim_objet.type_objet LIKE '%branche%'"
        )

        rewritten = fix_sql(query, "total number of polices by branche")

        self.assertNotIn("branche%", rewritten)
        self.assertNotIn("LIKE", rewritten.upper())
        self.assertIn("GROUP BY", rewritten.upper())
        self.assertIn("dwh.dim_objet.type_objet", rewritten)

    def test_returns_friendly_message_for_sql_errors(self):
        message = get_user_friendly_error_message("SQL execution failed: invalid column 'id_risque'")

        self.assertIn("database query failed", message.lower())
        self.assertIn("rephrase", message.lower())
