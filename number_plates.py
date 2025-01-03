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
			     plate_number TEXT NOT NULL,           -- Номер (например, "01 A 123 AA")
			     price REAL NOT NULL,                  -- Цена номерного знака
			     status TEXT NOT NULL                  -- Статус (например, "доступен", "продан", "забронирован")
			 );
			""")

	def add_number_plate(self, plate_number, price, status="available"):
		self.cursor.execute("""
		INSERT INTO number_plates (plate_number, price, status)
		VALUES (?, ?, ?)
		""", (plate_number, price, status))
		self.conn.commit()
		print("Номерной знак успешно добавлен.")

	def delete_number_plate(self, plate_id):
		self.cursor.execute("DELETE FROM number_plates where id = ?", (plate_id,))
		self.conn.commit()
		print(f"Номерной знак с ID {plate_id} удален.")

	def get_number_plate_by_id(self, plate_id):
		self.cursor.execute("SELECT * FROM number_plates where id = ?", (plate_id,))
		plate = self.cursor.fetchone()
		if plate:
			return {
				"id": plate[0],
				"plate_number": plate[1],
				"price": plate[2],
				"status": plate[3]
			}
	def get_number_plate_by_number(self, plate_number):
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
			print("Номерной знак должен быть с заглавными буквами.")

	def list_number_plates(self):
		self.cursor.execute("SELECT * FROM number_plates")
		plates = self.cursor.fetchall()
		for plate in plates:
			print(f"ID: {plate[0]}, Номерной знак: {plate[1]}, Цена: {plate[2]}, Статус: {plate[3]}")

	def close_connection(self):
		self.conn.close()




