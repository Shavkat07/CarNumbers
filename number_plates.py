import sqlite3


class CarPlate:
	def __init__(self, db_name="data.db"):
		self.conn = sqlite3.connect(db_name)
		self.cursor = self.conn.cursor()
		self._create_plates_table()

	def _create_plates_table(self):
		self.cursor.execute("""
			-- Создание таблицы для номерных знаков
			 CREATE TABLE IF NOT EXISTS number_plates (
			     id INTEGER PRIMARY KEY AUTOINCREMENT, -- Уникальный идентификатор номерного знака
			     plate_number TEXT NOT NULL UNIQUE,           -- Номер (например, "01 A 123 AA")
			     price REAL NOT NULL,                  -- Цена номерного знака
			     status TEXT NOT NULL                  -- Статус (например, "доступен", "продан", "забронирован")
			 );
			""")

	def edit_plate(self, plate_id, price=None, status=None):
		""" Raqam ma'lumotlari yanglinadi """
		if price:
			self.cursor.execute("UPDATE number_plates SET price = ? WHERE id = ?", (price, plate_id))
		if status:
			if status not in ["available", "sold"]:
				print("Bunaqa raqam mavjud emas.")
				return
			self.cursor.execute("UPDATE number_plates SET status = ? WHERE id = ?", (status, plate_id))
		self.conn.commit()
		print(f"ID {plate_id} dagi mijoz ma'lumotlari yanglinadi.")


	def add_number_plate(self, plate_number: str, price: str, status="available"):
		self.cursor.execute("""
		INSERT INTO number_plates (plate_number, price, status)
		VALUES (?, ?, ?)
		""", (plate_number.strip(), price, status.strip()))
		self.conn.commit()
		print("Avtomobil raqami qo'shildi.")

	def delete_number_plate(self, plate_id):
		self.cursor.execute("DELETE FROM number_plates where id = ?", (plate_id,))
		self.conn.commit()
		print(f"ID {plate_id} dagi raqam o'chirildi.")

	def get_numbers_by_region(self, region):
		self.cursor.execute("SELECT * FROM number_plates WHERE plate_number LIKE ? and status = ?;", (region + "%", "available"))
		plates = self.cursor.fetchall()
		return plates

	def get_plate_by_id(self, plate_id) -> dict:
		self.cursor.execute("SELECT * FROM number_plates where id = ?", (plate_id,))
		plate = self.cursor.fetchone()
		if plate:
			return {
				"id": plate[0],
				"plate_number": plate[1],
				"price": plate[2],
				"status": plate[3]
			}
	def get_plate_by_number(self, plate_number) -> dict:
		if plate_number.isupper():
			self.cursor.execute("SELECT * FROM number_plates where plate_number = ?", (plate_number,))
			plate = self.cursor.fetchone()
			if plate:
				return {
					"id": plate[0],
					"plate_number": plate[1],
					"price": plate[2],
					"status": plate[3]
				}
		else:
			print("Avtomobil raqami katta harflarda bo'lishi kerak.")

	def list_plates(self) -> list[dict]:
		self.cursor.execute("SELECT * FROM number_plates")
		plates = self.cursor.fetchall()
		return plates

	def close_connection(self):
		self.conn.close()




