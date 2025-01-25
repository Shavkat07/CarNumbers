import unittest
import sqlite3
from sales import Sale
from users import User
from number_plates import CarPlate
import os

class TestSale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db = "test_data.db"

    def setUp(self):
        self.sale = Sale(db_name=self.test_db)
        self.user = User(db_name=self.test_db)
        self.plate_manager = CarPlate(db_name=self.test_db)

        # Clear and set up tables for testing
        self._clear_tables()
        self.user._create_users_table()
        self.plate_manager._create_plates_table()
        self.sale._create_sales_table()

        # Add initial test data
        self.user.add_user("Test User", "Test Address")
        self.plate_manager.add_number_plate("01 A 123 AA", 5000, "available")

    def tearDown(self):
        self.sale.close_connection()
        self.user.close_connection()
        self.plate_manager.close_connection()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def _clear_tables(self):
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS sales")
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS number_plates")
        conn.commit()
        conn.close()

    def test_add_sale(self):
        user_id = 1  # The ID of "Test User"
        plate_id = 1  # The ID of "01 A 123 AA"
        sale_date = "2025-01-01"

        self.sale.add_sale(plate_id, user_id, sale_date, self.plate_manager)
        sales = self.sale.list_sales()
        self.assertEqual(len(sales), 1)

    def test_add_sale_plate_already_sold(self):
        user_id = 1
        plate_id = 1
        sale_date = "2025-01-01"

        # First sale
        self.sale.add_sale(plate_id, user_id, sale_date, self.plate_manager)

        # Attempt to sell the same plate again
        self.sale.add_sale(plate_id, user_id, sale_date, self.plate_manager)
        sales = self.sale.list_sales()
        self.assertEqual(len(sales), 1)

    def test_delete_sale(self):
        user_id = 1
        plate_id = 1
        sale_date = "2025-01-01"

        self.sale.add_sale(plate_id, user_id, sale_date, self.plate_manager)
        sales = self.sale.list_sales()
        self.assertEqual(len(sales), 1)

        sale_id = sales[0][0]
        self.sale.delete_sale(sale_id)

        sales = self.sale.list_sales()
        self.assertEqual(len(sales), 0)

    def test_get_sale(self):
        user_id = 1
        plate_id = 1
        sale_date = "2025-01-01"

        self.sale.add_sale(plate_id, user_id, sale_date, self.plate_manager)
        sales = self.sale.list_sales()
        sale_id = sales[0][0]

        sale = self.sale.get_sale(sale_id)
        self.assertEqual(sale["plate_id"], plate_id)
        self.assertEqual(sale["user_id"], user_id)
        self.assertEqual(sale["sale_date"], sale_date)

    def test_get_sales_by_user_id(self):
        user_id = 1
        plate_id = 1
        sale_date = "2025-01-01"

        self.sale.add_sale(plate_id, user_id, sale_date, self.plate_manager)

        sales = self.sale.get_sales_by_user_id(user_id)
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0][1], plate_id)

if __name__ == "__main__":
    unittest.main()
