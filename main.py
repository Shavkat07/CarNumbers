from users import User
from number_plates import CarPlate
from sales import Sale
import os
import time
from datetime import datetime
import json

def clear_console():
	command = 'cls' if os.name == 'nt' else 'clear'
	os.system(command)


def back_to_menu():
	while True:
		choice = int(input("Enter 0 to back to the menu: "))
		if choice == 0:
			break


def main_menu():
	print("\n=== Главное меню ===")
	print("1. Управление пользователями")
	print("2. Управление номерными знаками")
	print("3. Управление продажами")
	print("0. Выход")
	choice = input("Выберите действие: ")
	return choice


def user_menu(user_manager):
	while True:
		clear_console()
		print("\n=== Меню пользователей ===")
		print("1. Добавить пользователя")
		print("2. Данные одного пользователя")
		print("3. Редактировать пользователя")
		print("4. Удалить пользователя")
		print("5. Список пользователей")
		print("0. Назад")
		choice = input("Выберите действие: ")

		if choice == "1":
			name = input("Введите имя: ")
			address = input("Введите адрес: ")
			user_manager.add_user(name, address)
		elif choice == "2":
			user_id = int(input("Введите ID пользователя: "))
			user = user_manager.get_user(user_id)
			print(f"ID: {user[0]}, Имя: {user[1]}, Адрес: {user[2]}, Купленные номера: {user[3]}")
		elif choice == "3":
			user_id = int(input("Введите ID пользователя: "))
			name = input("Новое имя (нажмите Enter, чтобы пропустить): ")
			address = input("Новый адрес (нажмите Enter, чтобы пропустить): ")
			user_manager.edit_user(user_id, name or None, address or None)
		elif choice == "4":
			user_id = int(input("Введите ID пользователя: "))
			user_manager.delete_user(user_id)
		elif choice == "5":
			users = user_manager.list_users()
			for user in users:
				purchased_plates = json.loads(user[3]) if user[3] else []
				print(f"ID: {user[0]}, Имя: {user[1]}, Адрес: {user[2]}, Купленные номера: {purchased_plates}")
			back_to_menu()
		elif choice == "0":
			break

		else:
			print("Неверный выбор. Попробуйте снова.")

		time.sleep(3)


def plate_menu(plate_manager):
	while True:
		clear_console()
		print("\n=== Меню номерных знаков ===")
		print("1. Добавить номерной знак")
		print("2. Удалить номерной знак")
		print("3. Просмотреть номерной знак по ID")
		print("4. Список номерных знаков")
		print("0. Назад")
		choice = input("Выберите действие: ")

		if choice == "1":
			plate_number = input("Введите номерной знак: ").upper().strip()
			price = float(input("Введите цену: "))
			plate_manager.add_number_plate(plate_number, price)

		elif choice == "2":
			plate_id = int(input("Введите ID номерного знака: "))
			plate_manager.delete_number_plate(plate_id)

		elif choice == "3":
			plate_id = int(input("Введите ID номерного знака: "))
			plate = plate_manager.get_plate_by_id(plate_id)
			if plate:
				print(
					f"ID: {plate['id']}, Номер: {plate['plate_number']}, Цена: {plate['price']}, Статус: {plate['status']}")
				back_to_menu()
			else:
				print("Номерной знак не найден.")

		elif choice == "4":
			plates = plate_manager.list_plates()
			for plate in plates:
				print(f"ID: {plate[0]}, Номерной знак: {plate[1]}, Цена: {plate[2]}, Статус: {plate[3]}")
			back_to_menu()

		elif choice == "0":
			break
		else:
			print("Неверный выбор. Попробуйте снова.")
		time.sleep(2)


def sale_menu(sale_manager):
	while True:
		clear_console()
		print("\n=== Меню продаж ===")
		print("1. Добавить продажу")
		print("2. Список продаж")
		print("3. Список продаж конкретного пользователя")
		print("4. Просмотреть продажу по его ID")
		print("5. Удалить продажу")
		print("0. Назад")
		choice = input("Выберите действие: ")

		if choice == "1":
			plate_id = int(input("Введите ID номерного знака: "))
			user_id = int(input("Введите ID пользователя: "))
			sale_date = input("Введите дату продажи (dd-mm-yyyy) (нажмите ENTER для сегодняшнего числа): ")
			sale_manager.add_sale(plate_id, user_id,
			                      sale_date=sale_date if sale_date else datetime.now().strftime("%d-%m-%Y"))

		elif choice == "2":
			sales = sale_manager.list_sales()
			for sale in sales:
				print(
					f"ID: {sale[0]}, ID номерного знака: {sale[1]}, ID Пользователя: {sale[2]}, Дата продажи: {sale[3]}")
			back_to_menu()

		elif choice == "3":
			user_id = int(input("Введите ID пользователя: "))
			sales = sale_manager.get_sales_by_user_id(user_id=user_id)
			for sale in sales:
				print(
					f"ID: {sale[0]}, ID номерного знака: {sale[1]}, ID Пользователя: {sale[2]}, Дата продажи: {sale[3]}")

			back_to_menu()

		elif choice == "4":
			sale_id = int(input("Введите ID продажи: "))
			sale = sale_manager.get_sale(sale_id)
			if sale:
				print(
					f"ID: {sale['id']}, ID номерного знака: {sale['plate_id']}, ID пользователя: {sale['user_id']}, Дата продажи: {sale['sale_date']}")
				back_to_menu()
			else:
				print("Продажа не найдена.")

		elif choice == "5":
			sale_id = int(input("Введите ID продажи: "))
			sale_manager.delete_sale(sale_id)

		elif choice == "0":
			break
		else:
			print("Неверный выбор. Попробуйте снова.")

		time.sleep(2)


def main():
	user_manager = User()
	plate_manager = CarPlate()
	sale_manager = Sale()

	while True:
		clear_console()
		choice = main_menu()
		if choice == "1":
			user_menu(user_manager)
		elif choice == "2":
			plate_menu(plate_manager)
		elif choice == "3":
			sale_menu(sale_manager)
		elif choice == "0":
			print("Выход из программы...")
			user_manager.close_connection()
			plate_manager.close_connection()
			sale_manager.close_connection()
			break
		else:
			print("Неверный выбор. Попробуйте снова.")
			time.sleep(1)


if __name__ == "__main__":
	main()
