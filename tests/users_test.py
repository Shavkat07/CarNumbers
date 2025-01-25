import unittest
import sqlite3
from users import User
import os

class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db = "test_user_data.db"

    def setUp(self):
        self.user = User(db_name=self.test_db)

        # Clear and set up tables for testing
        self._clear_tables()
        self.user._create_users_table()

        # Add initial test data
        self.user.add_user("Test User", "Test Address")

    def tearDown(self):
        self.user.close_connection()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def _clear_tables(self):
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        conn.commit()
        conn.close()

    def test_add_user(self):
        self.user.add_user("Another User", "Another Address")
        users = self.user.list_users()
        self.assertEqual(len(users), 2)  # Including the initial test user

    def test_edit_user(self):
        user_id = 1  # ID of "Test User"
        self.user.edit_user(user_id, name="Updated Name", address="Updated Address")

        user = self.user.get_user(user_id)
        self.assertEqual(user["name"], "Updated Name")
        self.assertEqual(user["address"], "Updated Address")

    def test_delete_user(self):
        user_id = 1  # ID of "Test User"
        self.user.delete_user(user_id)

        users = self.user.list_users()
        self.assertEqual(len(users), 0)

    def test_get_user(self):
        user_id = 1  # ID of "Test User"
        user = self.user.get_user(user_id)

        self.assertEqual(user["id"], user_id)
        self.assertEqual(user["name"], "Test User")
        self.assertEqual(user["address"], "Test Address")

    def test_list_users(self):
        users = self.user.list_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0][1], "Test User")



