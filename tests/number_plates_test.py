import unittest
import os
from number_plates import CarPlate


class TestCarPlate(unittest.TestCase):
	def setUp(self):
		"""Создаем тестовую базу данных перед каждым тестом."""
		self.db_name = "test_data.db"
		self.car_plate = CarPlate(db_name=self.db_name)

	def tearDown(self):
		"""Удаляем тестовую базу данных после каждого теста."""
		self.car_plate.close_connection()
		if os.path.exists(self.db_name):
			os.remove(self.db_name)

	def test_add_number_plate(self):
		"""Тестируем добавление номерного знака."""
		self.car_plate.add_number_plate("01 A 123 AA", 1000.0, "available")
		plates = self.car_plate.list_plates()
		self.assertEqual(len(plates), 1)  # Проверяем, что добавлена одна запись
		self.assertEqual(plates[0][1], "01 A 123 AA")  # Проверяем, что номер совпадает
		self.assertEqual(plates[0][2], 1000.0)  # Проверяем цену
		self.assertEqual(plates[0][3], "available")  # Проверяем статус

	def test_edit_plate(self):
		"""Тестируем редактирование номерного знака."""
		self.car_plate.add_number_plate("01 A 123 AA", 1000.0, "available")
		plate = self.car_plate.list_plates()[0]
		plate_id = plate[0]
		self.car_plate.edit_plate(plate_id, price=2000.0, status="sold")
		updated_plate = self.car_plate.get_plate_by_id(plate_id)
		self.assertEqual(updated_plate["price"], 2000.0)  # Проверяем обновленную цену
		self.assertEqual(updated_plate["status"], "sold")  # Проверяем обновленный статус

	def test_delete_number_plate(self):
		"""Тестируем удаление номерного знака."""
		self.car_plate.add_number_plate("01 A 123 AA", 1000.0, "available")
		plate = self.car_plate.list_plates()[0]
		plate_id = plate[0]
		self.car_plate.delete_number_plate(plate_id)
		plates = self.car_plate.list_plates()
		self.assertEqual(len(plates), 0)  # Проверяем, что запись удалена

	def test_get_numbers_by_region(self):
		"""Тестируем фильтрацию по региону."""
		self.car_plate.add_number_plate("01 A 123 AA", 1000.0, "available")
		self.car_plate.add_number_plate("02 B 456 BB", 1200.0, "sold")
		self.car_plate.add_number_plate("01 C 789 CC", 900.0, "available")
		plates = self.car_plate.get_numbers_by_region("01")
		self.assertEqual(len(plates), 2)  # Проверяем, что найдено 2 доступных номера
		self.assertEqual(plates[0][1], "01 A 123 AA")  # Проверяем первый номер

	def test_get_plate_by_id(self):
		"""Тестируем поиск номера по ID."""
		self.car_plate.add_number_plate("01 A 123 AA", 1000.0, "available")
		plate = self.car_plate.list_plates()[0]
		plate_id = plate[0]
		result = self.car_plate.get_plate_by_id(plate_id)
		self.assertEqual(result["plate_number"], "01 A 123 AA")
		self.assertEqual(result["price"], 1000.0)
		self.assertEqual(result["status"], "available")

	def test_get_plate_by_number(self):
		"""Тестируем поиск номера по plate_number."""
		self.car_plate.add_number_plate("01 A 123 AA", 1000.0, "available")
		result = self.car_plate.get_plate_by_number("01 A 123 AA")
		self.assertEqual(result["plate_number"], "01 A 123 AA")
		self.assertEqual(result["price"], 1000.0)
		self.assertEqual(result["status"], "available")

	def test_list_plates(self):
		"""Тестируем вывод всех номерных знаков."""
		self.car_plate.add_number_plate("01 A 123 AA", 1000.0, "available")
		self.car_plate.add_number_plate("02 B 456 BB", 1200.0, "sold")
		plates = self.car_plate.list_plates()
		self.assertEqual(len(plates), 2)  # Проверяем, что добавлено 2 записи
