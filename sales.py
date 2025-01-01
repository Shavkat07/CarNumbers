import sqlite3
import json

class Sale:
	def __init__(self, db_name="data.db"):
		self.conn = sqlite3.connect(db_name)
		self.cursor = self.conn.cursor()
		self._create_sales_table()

	def _create_sales_table(self):
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS sales (
			id INTEGER PRIMARY KEY AUTOINCREMENT, -- Уникальный идентификатор продажи
			plate_id INTEGER NOT NULL,            -- Идентификатор номерного знака (связь с таблицей number_plates)
			user_id INTEGER NOT NULL,             -- Идентификатор пользователя (связь с таблицей users)
			sale_date TEXT NOT NULL,              -- Дата продажи в формате строки (например, "YYYY-MM-DD")
			FOREIGN KEY (plate_id) REFERENCES number_plates(id) ON DELETE CASCADE,
			FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE)
		""")
		self.conn.commit()

	def add_sale(self, plate_id, user_id, sale_date):
		try:
			""" проверка для доступности номера для продажи  """
			self.cursor.execute("""
			SELECT * FROM number_plates WHERE id = ?
			""", (plate_id,))

			plate = self.cursor.fetchone()
			print(plate)
			if plate:
				if plate[3] == "sold":
					print("Ошибка: Номерной знак уже продан.")
					return
			else:
				print("такой номерной знак не существует")
				return

			""" проверка есть ли пользователь """

			self.cursor.execute("""
			SELECT * FROM users WHERE id = ?
			""", (user_id,))
			user = self.cursor.fetchone()
			if not user:
				print("Ошибка: Пользователь не существует")
				return

			purchased_plates = json.loads(user[3]) if user[3] else []

			self.cursor.execute("""
		    INSERT INTO sales (plate_id, user_id, sale_date) 
		    VALUES (?, ?, ?)
		    """, (plate_id, user_id, sale_date))

			self.cursor.execute("""
		    UPDATE number_plates
		    SET status = 'sold'
		    WHERE id = ?
		    """, (plate_id,))

			self.cursor.execute("""
			UPDATE users 
			SET purchased_plates = ? 
			WHERE id = ?
			""", (json.dumps(purchased_plates + [plate[1]]), user_id))

			self.conn.commit()

		except sqlite3.Error as e:
			self.conn.rollback()
			print(f"Ошибка при добавлении продажи: {e}")

		self.conn.commit()
		print("Продажа успешно добавлен.")

	def delete_sale(self, sale_id):


		self.cursor.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
		self.conn.commit()
		print(f"Продажа с ID {sale_id} удален.")

	def get_sale(self, sale_id):
		self.cursor.execute("SELECT * FROM sales WHERE id = ?", (sale_id,))
		sale = self.cursor.fetchone()
		if sale:
			return {
				"id": sale[0],
				"plate_id": sale[1],
				"user_id": sale[2],
				"sale_date": sale[3]
			}
		return None

	def get_sales_by_user_id(self, user_id):
		self.cursor.execute("SELECT * FROM sales WHERE user_id = ?", (user_id,))
		sales = self.cursor.fetchall()
		for sale in sales:
			print(f"ID: {sale[0]}, ID номерного знака: {sale[1]}, ID Пользователя: {sale[2]}, Дата продажи: {sale[3]}")

	def list_sales(self):
		self.cursor.execute("SELECT * FROM sales")
		sales = self.cursor.fetchall()
		for sale in sales:
			print(f"ID: {sale[0]}, ID номерного знака: {sale[1]}, ID Пользователя: {sale[2]}, Дата продажи: {sale[3]}")

	def close_connection(self):
		"""Закрыть соединение с базой данных"""
		self.conn.close()
