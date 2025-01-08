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
		choice = int(input("Enter 0 to return to the menu: "))
		if choice == 0:
			break

def main_menu():
	print("\n=== Main Menu ===")
	print("1. User Management")
	print("2. License Plate Management")
	print("3. Sales Management")
	print("0. Exit")
	choice = input("Select an option: ")
	return choice

def user_menu(user_manager):
	while True:
		clear_console()
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
			user_manager.add_user(name, address)
		elif choice == "2":
			user_id = int(input("Enter User ID: "))
			user = user_manager.get_user(user_id)
			print(f"ID: {user[0]}, Name: {user[1]}, Address: {user[2]}, Purchased Plates: {user[3]}")
		elif choice == "3":
			user_id = int(input("Enter User ID: "))
			name = input("New Name (press Enter to skip): ")
			address = input("New Address (press Enter to skip): ")
			user_manager.edit_user(user_id, name or None, address or None)
		elif choice == "4":
			user_id = int(input("Enter User ID: "))
			user_manager.delete_user(user_id)
		elif choice == "5":
			users = user_manager.list_users()
			for user in users:
				purchased_plates = json.loads(user[3]) if user[3] else []
				print(f"ID: {user[0]}, Name: {user[1]}, Address: {user[2]}, Purchased Plates: {purchased_plates}")
			back_to_menu()
		elif choice == "0":
			break
		else:
			print("Invalid choice. Try again.")
		time.sleep(3)

def plate_menu(plate_manager):
	while True:
		clear_console()
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
			plate_manager.add_number_plate(plate_number, price)
		elif choice == "2":
			plate_id = int(input("Enter License Plate ID: "))
			plate_manager.delete_number_plate(plate_id)
		elif choice == "3":
			plate_id = int(input("Enter License Plate ID: "))
			plate = plate_manager.get_plate_by_id(plate_id)
			if plate:
				print(f"ID: {plate['id']}, Plate: {plate['plate_number']}, Price: {plate['price']}, Status: {plate['status']}")
				back_to_menu()
			else:
				print("License plate not found.")
		elif choice == "4":
			plates = plate_manager.list_plates()
			for plate in plates:
				print(f"ID: {plate[0]}, License Plate: {plate[1]}, Price: {plate[2]}, Status: {plate[3]}")
			back_to_menu()
		elif choice == "0":
			break
		else:
			print("Invalid choice. Try again.")
		time.sleep(2)

def sale_menu(sale_manager):
	while True:
		clear_console()
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
			sale_manager.add_sale(plate_id, user_id, sale_date=sale_date if sale_date else datetime.now().strftime("%d-%m-%Y"))
		elif choice == "2":
			sales = sale_manager.list_sales()
			for sale in sales:
				print(f"ID: {sale[0]}, License Plate ID: {sale[1]}, User ID: {sale[2]}, Sale Date: {sale[3]}")
			back_to_menu()
		elif choice == "3":
			user_id = int(input("Enter User ID: "))
			sales = sale_manager.get_sales_by_user_id(user_id=user_id)
			for sale in sales:
				print(f"ID: {sale[0]}, License Plate ID: {sale[1]}, User ID: {sale[2]}, Sale Date: {sale[3]}")
			back_to_menu()
		elif choice == "4":
			sale_id = int(input("Enter Sale ID: "))
			sale = sale_manager.get_sale(sale_id)
			if sale:
				print(f"ID: {sale['id']}, License Plate ID: {sale['plate_id']}, User ID: {sale['user_id']}, Sale Date: {sale['sale_date']}")
				back_to_menu()
			else:
				print("Sale not found.")
		elif choice == "5":
			sale_id = int(input("Enter Sale ID: "))
			sale_manager.delete_sale(sale_id)
		elif choice == "0":
			break
		else:
			print("Invalid choice. Try again.")
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
			print("Exiting the program...")
			user_manager.close_connection()
			plate_manager.close_connection()
			sale_manager.close_connection()
			break
		else:
			print("Invalid choice. Try again.")
			time.sleep(1)

if __name__ == "__main__":
	main()
