import sqlite3
import json

class User:
	def __init__(self, db_name="data.db"):
		"""Инициализация и подключение к базе данных"""
		self.conn = sqlite3.connect(db_name)
		self.cursor = self.conn.cursor()
		self._create_users_table()

	def _create_users_table(self):
		"""Создание таблицы пользователей, если ее нет"""
		self.cursor.execute("""
	           CREATE TABLE IF NOT EXISTS users (
	               id INTEGER PRIMARY KEY AUTOINCREMENT,
	               name TEXT NOT NULL,
	               address TEXT NOT NULL,
	               purchased_plates TEXT
	           )
	       """)
		self.conn.commit()

	def add_user(self, name, address,):
		"""Добавить нового пользователя"""
		self.cursor.execute("""
	        INSERT INTO users (name, address, purchased_plates) 
	        VALUES (?, ?, ?)
	    """, (name, address, '[]'))
		self.conn.commit()
		print(f"Mijoz {name} qo'shildi.")

	def edit_user(self, user_id, name=None, address=None):
		"""Редактировать данные пользователя"""
		if name:
			self.cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
		if address:
			self.cursor.execute("UPDATE users SET address = ? WHERE id = ?", (address, user_id))
		self.conn.commit()
		print(f"ID {user_id} dagi mijoz ma'lumotlari yanglinadi.")

	def delete_user(self, user_id):
		"""Удалить пользователя"""
		self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
		self.conn.commit()
		print(f"ID {user_id} dagi mijoz o'chirildi.")

	def get_user(self, user_id) -> dict:
		self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
		user = self.cursor.fetchone()
		if user:
			# Преобразуем JSON-строку обратно в список, если поле не пустое
			purchased_plates = json.loads(user[3]) if user[3] else []
			return {
				"id": user[0],
				"name": user[1],
				"address": user[2],
				"purchased_plates": purchased_plates
			}


	def list_users(self) -> list[dict]:
		"""Вывести список пользователей"""
		self.cursor.execute("SELECT * FROM users")
		users = self.cursor.fetchall()
		return users

	def close_connection(self):
		"""Закрыть соединение с базой данных"""
		self.conn.close()
