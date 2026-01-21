import random
import time
import os
import json

DEV_PASSWORD = "456996752"

def save_credentials(username, password, win_in_easy, win_in_medium, win_in_hard, win_in_impossible, win_in_mod, best_streak):
    credentials = {
        "username": username,
        "password": password,
        "winEasy": win_in_easy,
        "winMedium": win_in_medium,
        "winHard": win_in_hard,
        "winImpossible": win_in_impossible,
        "winMod": win_in_mod,
        "Streak": best_streak
    }
    
    with open("credentials.json", "w", encoding="utf-8") as file:
        json.dump(credentials, file, ensure_ascii=False, indent=4)
    
    print("Данные сохранены!")

def load_credentials():

    try:
        with open("credentials.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            
            return (
                data.get("username"),
                data.get("password"),
                data.get("winEasy", 0),
                data.get("winMedium", 0),
                data.get("winHard", 0),
                data.get("winImpossible", 0),
                data.get("winMod", 0),
                data.get("Streak", 0)
            )
    except FileNotFoundError:
        print("Файл с данными не найден!")
        return None, None, 0, 0, 0, 0, 0 
    except (KeyError, json.JSONDecodeError):
        print("Файл поврежден или имеет неверный формат!")
        return None, None, 0, 0, 0, 0, 0

def activate_dev_mode():
    
    username = "Kisth"
    password = DEV_PASSWORD
    win_in_easy = 999
    win_in_medium = 999
    win_in_hard = 999
    win_in_impossible = 999
    win_in_mod = 999
    best_streak = 999
    lst_ttl = "👑 Разработчик"
    
    save_credentials(username, password, win_in_easy, win_in_medium, win_in_hard, win_in_impossible, win_in_mod, best_streak)
    
    return username, password, win_in_easy, win_in_medium, win_in_hard, win_in_impossible, win_in_mod, lst_ttl, best_streak

def game_1(user_input, mystery_num):
    while user_input != mystery_num:
        
        if user_input < mystery_num:
            print("Слишком мало, попробуй снова.")
            return user_input
        
        elif user_input > mystery_num:
            print("Слишком много, попробуй снова.")
            return user_input
    return print("Поздравляю, ты выйграл!")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

random_num = None
lst_ttl = None
can_exit = True
att = 0
print("Добро пожаловать! Пожайлуста зарегистрируйтесь или войдите в аккаунт.")
choice_in_game = int(input('Введите "1" для входа или "2" для регистрации: '))
if choice_in_game == 9:
    secret_password = input("Введите секретный код разработчика: ")
    if secret_password == DEV_PASSWORD:
        username, password, win_in_easy, win_in_medium, win_in_hard, win_in_impossible, win_in_mod, lst_ttl, best_streak = activate_dev_mode()
    else:
        print("Неверный код разработчика!")
        choice_in_game = int(input('Введите "1" для входа или "2" для регистрации: '))

if choice_in_game == 1 and not ('username' in locals() and username == "Kisth"):
    
    input_username = str(input("Имя: "))
    input_password = input("Пароль: ")
    
    
    if input_username.lower() == "kisth" and input_password == DEV_PASSWORD:
        username, password, win_in_easy, win_in_medium, win_in_hard, win_in_impossible, win_in_mod, lst_ttl, best_streak = activate_dev_mode()
    else:
        username, password, win_in_easy, win_in_medium, win_in_hard, win_in_impossible, win_in_mod,best_streak = load_credentials()
        
        
        if username != input_username or str(password) != input_password:
            print("Неверное имя пользователя или пароль!")
        
            win_in_easy = win_in_medium = win_in_hard = win_in_impossible = win_in_mod = best_streak = 0
            username = input_username
            password = input_password
            lst_ttl = None
        elif username == "Kisth" and str(password) == DEV_PASSWORD:
            lst_ttl = "👑 Разработчик"

elif choice_in_game == 2:
    
    username = str(input("Имя: "))
    password = input("Пароль: ")
    
    
    if username.lower() == "Kisth" and password == DEV_PASSWORD:
        username, password, win_in_easy, win_in_medium, win_in_hard, win_in_impossible, win_in_mod, lst_ttl, best_streak = activate_dev_mode()
    else:
        win_in_easy = win_in_medium = win_in_hard = win_in_impossible = win_in_mod = best_streak = 0
        lst_ttl = None
        save_credentials(username, password, win_in_easy, win_in_medium, win_in_hard, win_in_impossible, win_in_mod, best_streak)

while can_exit:
    print("\t\t\t\t\t╔══════════════════════════════════════════╗")
    print("\t\t\t\t\t║  ❔ Игра 'УГАДАЙ ЧИСЛО' ❔   by Kisth    ║")
    print("\t\t\t\t\t╚══════════════════════════════════════════╝")
    print("\tМеню:")
    print("1. 🎮 НАЧАТЬ ИГРАТЬ")
    print("2. 👤 Профиль")
    print("3. 🎫 Титулы")
    print("4. ❔ Как играть?")
    print("5. 🚪 Выход")
    if username == "Kisth":
        print("9. 💻 Панель разработчика")
    choice = int(input("Введите число что бы продолжить (1-5): "))
    clear_screen()
    
    
    if choice == 1:
        print("Меню режима:")
        print("1. 🟢 Легко (До 50 чисел)")
        print("2. 🟡 Среднее (До 100 чисел)")
        print("3. 🔴 Сложная (До 250 чисел)")
        print("4. ⚫ Невозможно (До 1000 чисел)")
        print("5. 🖥️  Своя настройка")
        print("6. 🔙 Назад к меню")
        if username == "Kisth":
            print("7. 💎 Режим разработчика (мгновенная победа)")
        
        choice_gamemod = int(input("Введи число для продолжения: "))
        clear_screen()
        
        if choice_gamemod == 7 and username == "Kisth":
            mystery_num = random.randint(1, 1000)
            print(f"Загаданное число: {mystery_num} (режим разработчика)")
            user_input = mystery_num 
            print("Поздравляю, ты выиграл! (Режим разработчика)")
            time.sleep(2)
            continue
        
        
        if choice_gamemod == 1:
            mystery_num = random.randint(1, 50)
            user_input = 0
            start = time.time()
            
            while user_input != mystery_num:
                start_time = time.time()    
                user_input = int(input("\nВведите число: "))
                game_1(user_input, mystery_num)
                att += 1
                
                if att == 10:
                    print("\nВы проиграли!")
                    print(f"Загадочное число было: {mystery_num}")
                    best_streak -= best_streak
                    break
            
            win_in_easy += 1
            best_streak += 1
            print(f"Вы угадали число за: {time.time() - start:.2f} сек.")
            time.sleep(5)
        
        elif choice_gamemod == 2:
            mystery_num = random.randint(1, 100)
            user_input = 0
            start = time.time()
            
            while user_input != mystery_num:
                user_input = int(input("\nВведите число: "))
                game_1(user_input, mystery_num)
                att += 1
                
                if att == 15:
                    print("\nВы проиграли!")
                    print(f"Загадочное число было: {mystery_num}")
                    best_streak -= best_streak
                    break
            
            win_in_medium += 1
            best_streak += 1
            print(f"Вы угадали число за: {time.time() - start:.2f} сек.")
            time.sleep(5)

        elif choice_gamemod == 3:
            mystery_num = random.randint(1, 250)
            user_input = 0
            start = time.time()
            
            while user_input != mystery_num:
                user_input = int(input("\nВведите число: "))
                game_1(user_input, mystery_num)
                att += 1
                
                if att == 20:
                    print("\nВы проиграли!")
                    print(f"Загадочное число было: {mystery_num}")
                    best_streak -= best_streak
                    break
            
            win_in_hard += 1
            best_streak += 1
            print(f"Вы угадали число за: {time.time() - start:.2f} сек.")
            time.sleep(5)

        elif choice_gamemod == 4:
            mystery_num = random.randint(1, 1000)
            user_input = 0
            start = time.time()
            
            while user_input != mystery_num:
                user_input = int(input("\nВведите число: "))
                game_1(user_input, mystery_num)
                att += 1
                
                if att == 30:
                    print("\nВы проиграли!")
                    print(f"Загадочное число было: {mystery_num}")
                    best_streak -= best_streak
                    break
            
            win_in_impossible += 1
            best_streak += 1
            print(f"Вы угадали число за: {time.time() - start:.2f} сек.")
            time.sleep(5)

        elif choice_gamemod == 5:
            random_choice = int(input("Задайте число до которого хотите играть: "))
            mystery_num = random.randint(1, random_choice)
            user_input = 0
            start = time.time()
            
            while user_input != mystery_num:
                user_input = int(input("\nВведите число: "))
                game_1(user_input, mystery_num)
                att += 1
                
                if att == 50:
                    print("\nВы проиграли!")
                    print(f"Загадочное число было: {mystery_num}")
                    best_streak -= best_streak
                    break
            
            win_in_mod += 1
            best_streak += 1
            print(f"Вы угадали число за: {time.time() - start:.2f} сек.")
            time.sleep(5)
        
        elif  choice_gamemod == 6:
            clear_screen()
        
    elif choice == 2:
        print("\tВаш профиль:")
        print(f"Ваше имя: {username}")
        print("Ваши победы в каждом режиме: ")
        print(f"🟢 Легкий:           {win_in_easy}")
        print(f"🟡 Среднее:          {win_in_medium}")
        print(f"🔴 Сложно:           {win_in_hard}")
        print(f"⚫ Невозможно:       {win_in_impossible}")
        print(f"🖥️  Своя настройка:   {win_in_mod}")
        print(f"🕹️  Cерия выйграшных игр:  {best_streak}🔥")
        print(f"🏆 Всего побед: {win_in_easy + win_in_medium + win_in_hard + win_in_impossible + win_in_mod}")
        print(f"🎫 Титул: {lst_ttl}")
        input("\n🔙 Нажмите Enter чтобы продолжить...")
        clear_screen()
    
    elif choice == 3:
        list_title = []
        
        if username == "Kisth":
            list_title.append("👑 Разработчик")
            list_title.append("💻 Создатель игры")
            list_title.append("🏆 Всемогущий")
            list_title.append("⭐ Легенда навсегда")
        
        if win_in_easy >= 1:
            list_title.append("Первая победа")
        
        if win_in_impossible >= 1:
            list_title.append("Это вообще возможно?")
        
        if win_in_easy >= 5:
            list_title.append("Эксперт легкого режима")
        
        if win_in_medium >= 5:
            list_title.append("Эксперт среднего режима")
        
        if win_in_hard >= 5:
            list_title.append("Эксперт сложного режима")
        
        if win_in_impossible >= 3:
            list_title.append("Невозможное возможно")
        
        if best_streak >= 5:
            list_title.append("Горячая серия")
        
        total_wins = win_in_easy + win_in_medium + win_in_hard + win_in_impossible + win_in_mod
        if total_wins >= 10:
            list_title.append("Десяточка")
        if total_wins >= 25:
            list_title.append("Ветеран")
        if total_wins >= 50:
            list_title.append("Легенда")
        
        if list_title:
            for index, title in enumerate(list_title, 1):
                print(f"{index}. {title}")
            
            try:
                num_for_title = int(input("Введи число для выбора титула (0 чтобы не менять): "))
                if 1 <= num_for_title <= len(list_title):
                    lst_ttl = list_title[num_for_title - 1]
                    print(f"Титул установлен: {lst_ttl}")
                elif num_for_title != 0:
                    print("Неверный номер!")
            except ValueError:
                print("Введите число!")
        else:
            print("У вас еще нет титулов!")
        
        input("\nНажмите Enter чтобы продолжить...")
        clear_screen()
    
    elif choice == 4:
        print("Как играть?")
        print("1. Выберите режим игры")
        print("2. Компьютер загадывает случайное число")
        print("3. Вы пытаетесь угадать это число")
        print("4. Компьютер подсказывает 'Слишком мало' или 'Слишком много'")
        print("5. У вас ограниченное количество попыток")
        print("6. Выигрывайте игры, получайте титулы и улучшайте статистику!")
        
        input("\n🔙 Нажмите Enter чтобы продолжить...")
        clear_screen()

    elif choice == 5:
        can_exit = False

    elif choice == 9 and username == "Kisth":
        clear_screen()
        print("╔══════════════════════════════════════════╗")
        print("║          ПАНЕЛЬ РАЗРАБОТЧИКА             ║")
        print("╚══════════════════════════════════════════╝")
        print("1. Сбросить всю статистику")
        print("2. Установить максимальные победы")
        print("3. Установить конкретные значения")
        print("4. Вернуться в меню")
        
        dev_choice = int(input("Выберите действие: "))
        
        if dev_choice == 1:
            win_in_easy = win_in_medium = win_in_hard = win_in_impossible = win_in_mod = best_streak = 0
            print("Статистика сброшена!")
        elif dev_choice == 2:
            win_in_easy = win_in_medium = win_in_hard = win_in_impossible = win_in_mod = best_streak = 999
            print("Максимальная статистика установлена!")
        elif dev_choice == 3:
            win_in_easy = int(input("Победы в легком режиме: "))
            win_in_medium = int(input("Победы в среднем режиме: "))
            win_in_hard = int(input("Победы в сложном режиме: "))
            win_in_impossible = int(input("Победы в невозможном режиме: "))
            win_in_mod = int(input("Победы в своем режиме: "))
            best_streak = int(input("Серия выйграшных игр: "))
            print("Статистика обновлена!")
        
        input("\nНажмите Enter чтобы продолжить...")
    
    
    save_credentials(username, password, win_in_easy, win_in_medium, win_in_hard, win_in_impossible, win_in_mod, best_streak)
    clear_screen()

print("Спасибо за игру! Ваша статистика сохранена.")