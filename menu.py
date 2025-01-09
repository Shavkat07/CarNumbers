import json
from datetime import datetime
import time
import os

from number_plates import CarPlate
from sales import Sale
from users import User

Viloyatlar = {
	"Toshkent shahri": '10',
	"Toshkent viloyati": '01',
	"Samarqand": '30',
	"Sirdaryo": '20',
	"Jizzax": "25",
	"Fargʻona": "40",
	"Namangan": "50",
	"Andijon": "60",
	"Qashqadaryo": "70",
	"Surxondaryo": "75",
	"Buxoro": "80",
	"Navoiy": "85",
	"Xorazm": "90",
	"Qoraqalpogʻiston Respublikasi": "95",
}

class Menu:
	def clear_console(self):
		command = 'cls' if os.name == 'nt' else 'clear'
		os.system(command)


	def back_to_menu(self):
		while True:
			choice = int(input("Enter 0 to return to the menu: "))
			if choice == 0:
				break

class MainMenu(Menu):
	def __init__(self, admin_login, admin_password):
		self.admin_password = admin_password
		self.admin_login = admin_login
		self.plate_manager = CarPlate()

	def display(self):
		self.clear_console()
		print("=== Asosiy Menu ===")
		print("1. Admin yoki Xodim sifatida kirish")
		print("2. Oddiy Foydalanuvchi")
		print("0. Chiqish")
		tanlov = input("Menu ni tanlang: ")

		if tanlov == "1":
			print("=== Admin/Xodim Menusi ===")
			login = input("Loginnni kiriting: ")
			password = input("Parolni kiriting: ")
			if login == self.admin_login and password == self.admin_password:
				print("Admin/Xodim kirildi")
				return tanlov
			else:
				print("Login yoki parol noto'g'ri")
				self.display()

		elif tanlov == "2":
			for i, j in Viloyatlar.items():
				print(f"Hudud: {i}".ljust(40), "|   Kod: " + j)

			kod = input("Viloyat kodini kiriting: ")
			if kod in Viloyatlar.values():
				plates = self.plate_manager.get_numbers_by_region(region=kod)
				for plate in plates:
					print(f'Raqam: {plate[1]}     |    Narxi: {plate[2]}$')
				self.back_to_menu()
			else:
				print("Kod noto'g'ri")
				time.sleep(1)
				self.display()

		elif tanlov == "0":
			return tanlov
		else:
			print("Noto'g'ri tanlov.")
			self.display()

class AdminMenu(Menu):
	def __init__(self, user_manager, plate_manager, sale_manager):
		self.user_menu = UserMenu(user_manager)
		self.plate_menu = PlateMenu(plate_manager)
		self.sale_menu = SaleMenu(sale_manager)


	def display(self):
		while True:
			self.clear_console()

			print("\n=== Main Menu ===")
			print("1. User Management")
			print("2. License Plate Management")
			print("3. Sales Management")
			print("0. Exit")
			choice = input("Select an option: ")

			if choice == "1":
				self.user_menu.display()
			elif choice == "2":
				self.plate_menu.display()
			elif choice == "3":
				self.sale_menu.display()
			elif choice == "0":
				print("Exiting the program...")
				break
			else:
				print("Invalid choice. Try again.")
				time.sleep(1)


class UserMenu(Menu):
	def __init__(self, user_manager):
		self.user_manager = user_manager


	def display(self):
		while True:
			self.clear_console()
			print("\n=== User Menu ===")
			print("1. Add User")
			print("2. View User Details")
			print("3. Edit User")
			print("4. Delete User")
			print("5. List Users")
			print("0. Back")
			choice = input("Select an option: ")

			if choice == "1":
				name = input("Enter Name: ")
				address = input("Enter Address: ")
				self.user_manager.add_user(name, address)
			elif choice == "2":
				user_id = int(input("Enter User ID: "))
				user = self.user_manager.get_user(user_id)
				print(f"ID: {user[0]}, Name: {user[1]}, Address: {user[2]}, Purchased Plates: {user[3]}")
			elif choice == "3":
				user_id = int(input("Enter User ID: "))
				name = input("New Name (press Enter to skip): ")
				address = input("New Address (press Enter to skip): ")
				self.user_manager.edit_user(user_id, name or None, address or None)
			elif choice == "4":
				user_id = int(input("Enter User ID: "))
				self.user_manager.delete_user(user_id)
			elif choice == "5":
				users = self.user_manager.list_users()
				for user in users:
					purchased_plates = json.loads(user[3]) if user[3] else []
					print(f"ID: {user[0]}, Name: {user[1]}, Address: {user[2]}, Purchased Plates: {purchased_plates}")
				self.back_to_menu()
			elif choice == "0":
				break
			else:
				print("Invalid choice. Try again.")
			time.sleep(1)


class PlateMenu(Menu):
	def __init__(self, plate_manager):
		self.plate_manager = plate_manager

	def display(self):
		while True:
			self.clear_console()
			print("\n=== License Plate Menu ===")
			print("1. Add License Plate")
			print("2. Delete License Plate")
			print("3. View License Plate by ID")
			print("4. List License Plates")
			print("0. Back")
			choice = input("Select an option: ")

			if choice == "1":
				plate_number = input("Enter License Plate: ").upper().strip()
				price = float(input("Enter Price: "))
				self.plate_manager.add_number_plate(plate_number, price)
			elif choice == "2":
				plate_id = int(input("Enter License Plate ID: "))
				self.plate_manager.delete_number_plate(plate_id)
			elif choice == "3":
				plate_id = int(input("Enter License Plate ID: "))
				plate = self.plate_manager.get_plate_by_id(plate_id)
				if plate:
					print(
						f"ID: {plate['id']}, Plate: {plate['plate_number']}, Price: {plate['price']}, Status: {plate['status']}")
					self.back_to_menu()
				else:
					print("License plate not found.")
			elif choice == "4":
				plates = self.plate_manager.list_plates()
				for plate in plates:
					print(f"ID: {plate[0]}, License Plate: {plate[1]}, Price: {plate[2]}, Status: {plate[3]}")
				self.back_to_menu()
			elif choice == "0":
				break
			else:
				print("Invalid choice. Try again.")
			time.sleep(1)


class SaleMenu(Menu):
	def __init__(self, sale_manager):
		self.sale_manager = sale_manager

	def display(self):
		while True:
			self.clear_console()
			print("\n=== Sales Menu ===")
			print("1. Add Sale")
			print("2. List Sales")
			print("3. List Sales by User")
			print("4. View Sale by ID")
			print("5. Delete Sale")
			print("0. Back")
			choice = input("Select an option: ")

			if choice == "1":
				plate_id = int(input("Enter License Plate ID: "))
				user_id = int(input("Enter User ID: "))
				sale_date = input("Enter Sale Date (dd-mm-yyyy) (press ENTER for today): ")
				self.sale_manager.add_sale(plate_id, user_id,
				                           sale_date=sale_date if sale_date else datetime.now().strftime("%d-%m-%Y"))
			elif choice == "2":
				sales = self.sale_manager.list_sales()
				for sale in sales:
					print(f"ID: {sale[0]}, License Plate ID: {sale[1]}, User ID: {sale[2]}, Sale Date: {sale[3]}")
				self.back_to_menu()
			elif choice == "3":
				user_id = int(input("Enter User ID: "))
				sales = self.sale_manager.get_sales_by_user_id(user_id=user_id)
				for sale in sales:
					print(f"ID: {sale[0]}, License Plate ID: {sale[1]}, User ID: {sale[2]}, Sale Date: {sale[3]}")
				self.back_to_menu()
			elif choice == "4":
				sale_id = int(input("Enter Sale ID: "))
				sale = self.sale_manager.get_sale(sale_id)
				if sale:
					print(
						f"ID: {sale['id']}, License Plate ID: {sale['plate_id']}, User ID: {sale['user_id']}, Sale Date: {sale['sale_date']}")
					self.back_to_menu()
				else:
					print("Sale not found.")
			elif choice == "5":
				sale_id = int(input("Enter Sale ID: "))
				self.sale_manager.delete_sale(sale_id)
			elif choice == "0":
				break
			else:
				print("Invalid choice. Try again.")
			time.sleep(1)

