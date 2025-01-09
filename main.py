from menu import MainMenu, AdminMenu
from number_plates import CarPlate
from sales import Sale
from users import User

# Данные для входа администратора
ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "12345"

def main():
    # Создание экземпляров менеджеров
    user_manager = User()
    plate_manager = CarPlate()
    sale_manager = Sale()

    # Главное меню
    main_menu = MainMenu(ADMIN_LOGIN, ADMIN_PASSWORD)

    while True:
        choice = main_menu.display()

        if choice == "1":
            # Вход в меню администратора/менеджера
            admin_menu = AdminMenu(user_manager, plate_manager, sale_manager)
            admin_menu.display()

        elif choice == "0":
            print("Dasturdan chiqish.")
            break

    sale_manager.close_connection()
    plate_manager.close_connection()
    user_manager.close_connection()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDasturdan chiqildi.")
