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
        # command = 'cls' if os.name == 'nt' else 'clear'
        # os.system(command)
        pass

    def back_to_menu(self):
        while True:
            choice = int(input("Menu ga qaytish uchun 0 ni kiriting: "))
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
            login = input("Loginni kiriting: ")
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
        self.sale_menu = SaleMenu(sale_manager, plate_manager)


    def display(self):
        while True:
            self.clear_console()

            print("\n=== Asosiy Menu ===")
            print("1. Mijozlarni boshqarish")
            print("2. Avtomobil raqamlarini boshqarish")
            print("3. Savdolarni boshqarish")
            print("0. Chiqish")
            choice = input("Biror tanlovni tanlang: ")

            if choice == "1":
                self.user_menu.display()
            elif choice == "2":
                self.plate_menu.display()
            elif choice == "3":
                self.sale_menu.display()
            elif choice == "0":
                print("Dasturdan chiqilmoqda...")
                break
            else:
                print("Noto'g'ri tanlov. Qaytadan urinib ko'ring.")
                time.sleep(1)


class UserMenu(Menu):
    def __init__(self, user_manager):
        self.user_manager = user_manager


    def display(self):
        while True:
            self.clear_console()
            print("\n=== Mijozlar Menyusi ===")
            print("1. Mijozlarni qo'shish")
            print("2. Mijozlar ma'lumotlarini ko'rish")
            print("3. Mijozlarni tahrirlash")
            print("4. Mijozlarni o'chirish")
            print("5. Mijozlar ro'yxati")
            print("0. Orqaga")
            choice = input("Biror tanlovni tanlang: ")

            if choice == "1":
                name = input("Ismni kiriting: ")
                address = input("Manzilni kiriting: ")
                self.user_manager.add_user(name, address)
            elif choice == "2":
                user_id = int(input("Mijoz ID sini kiriting: "))
                user = self.user_manager.get_user(user_id)
                print(f"ID: {user[0]}, Ism: {user[1]}, Manzil: {user[2]}, Xarid qilingan raqamlar: {user[3]}")
            elif choice == "3":
                user_id = int(input("Mijoz ID sini kiriting: "))
                name = input("Yangi ism (o'kazib yuborish uchun Enter bosing): ")
                address = input("Yangi manzil (o'tkazib yuborish uchun Enter bosing): ")
                self.user_manager.edit_user(user_id, name or None, address or None)
            elif choice == "4":
                user_id = int(input("Mijoz ID sini kiriting: "))
                self.user_manager.delete_user(user_id)
            elif choice == "5":
                users = self.user_manager.list_users()
                for user in users:
                    purchased_plates = json.loads(user[3]) if user[3] else []
                    print(f"ID: {user[0]}, Ism: {user[1]}, Manzil: {user[2]}, Xarid qilingan raqamlar: {purchased_plates}")
                self.back_to_menu()
            elif choice == "0":
                break
            else:
                print("Noto'g'ri tanlov. Qaytadan urinib ko'ring.")
            time.sleep(1)


class PlateMenu(Menu):
    def __init__(self, plate_manager):
        self.plate_manager = plate_manager

    def display(self):
        while True:
            self.clear_console()
            print("\n=== Avtomobil Raqamlari Menyusi ===")
            print("1. Raqam qo'shish")
            print("2. Raqamni o'chirish")
            print("3. Raqamni ID bo'yicha ko'rish")
            print("4. Raqamlar ro'yxati")
            print("0. Orqaga")
            choice = input("Biror tanlovni tanlang: ")

            if choice == "1":
                plate_number = input("Raqamni kiriting: ").upper().strip()
                price = float(input("Narxini kiriting: "))
                self.plate_manager.add_number_plate(plate_number, price)
            elif choice == "2":
                plate_id = int(input("Raqam ID sini kiriting: "))
                self.plate_manager.delete_number_plate(plate_id)
            elif choice == "3":
                plate_id = int(input("Raqam ID sini kiriting: "))
                plate = self.plate_manager.get_plate_by_id(plate_id)
                if plate:
                    print(f"ID: {plate['id']}, Raqam: {plate['plate_number']}, Narxi: {plate['price']}, Holati: {plate['status']}")
                    self.back_to_menu()
                else:
                    print("Raqam topilmadi.")
            elif choice == "4":
                plates = self.plate_manager.list_plates()
                for plate in plates:
                    print(f"ID: {plate[0]}, Raqam: {plate[1]}, Narx: {plate[2]}, Holati: {plate[3]}")
                self.back_to_menu()
            elif choice == "0":
                break
            else:
                print("Noto'g'ri tanlov. Qaytadan urinib ko'ring.")
            time.sleep(1)


class SaleMenu(Menu):
    def __init__(self, sale_manager, plate_manager):
        self.sale_manager = sale_manager
        self.plate_manager = plate_manager

    def display(self):
        while True:
            self.clear_console()
            print("\n=== Savdolar Menyusi ===")
            print("1. Savdo qo'shish")
            print("2. Savdolar ro'yxati")
            print("3. Mijoz bo'yicha savdolar ro'yxati")
            print("4. Savdoni ID bo'yicha ko'rish")
            print("5. Savdoni o'chirish")
            print("0. Orqaga")
            choice = input("Biror tanlovni tanlang: ")

            if choice == "1":
                plate_id = int(input("Raqam ID sini kiriting: "))
                user_id = int(input("Mijoz ID sini kiriting: "))
                sale_date = input("Savdo sanasi (dd-mm-yyyy) (Bugungi sana uchun ENTER bosing): ")
                self.sale_manager.add_sale(plate_id, user_id, plate_manager=self.plate_manager,
                                           sale_date=sale_date if sale_date else datetime.now().strftime("%d-%m-%Y"))
            elif choice == "2":
                sales = self.sale_manager.list_sales()
                for sale in sales:
                    print(f"ID: {sale[0]}, Raqam ID: {sale[1]}, Mijoz ID: {sale[2]}, Sana: {sale[3]}")
                self.back_to_menu()
            elif choice == "3":
                user_id = int(input("Mijoz ID sini kiriting: "))
                sales = self.sale_manager.get_sales_by_user_id(user_id=user_id)
                for sale in sales:
                    print(f"ID: {sale[0]}, Raqam ID: {sale[1]}, Mijoz ID: {sale[2]}, Sana: {sale[3]}")
                self.back_to_menu()
            elif choice == "4":
                sale_id = int(input("Savdo ID sini kiriting: "))
                sale = self.sale_manager.get_sale(sale_id)
                if sale:
                    print(f"ID: {sale['id']}, Raqam ID: {sale['plate_id']}, Mijoz ID: {sale['user_id']}, Sana: {sale['sale_date']}")
                    self.back_to_menu()
                else:
                    print("Savdo topilmadi.")
            elif choice == "5":
                sale_id = int(input("Savdo ID sini kiriting: "))
                self.sale_manager.delete_sale(sale_id)
            elif choice == "0":
                break
            else:
                print("Noto'g'ri tanlov. Qaytadan urinib ko'ring.")
            time.sleep(1)
