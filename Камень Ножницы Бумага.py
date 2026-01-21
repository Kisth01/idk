import random
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

variants_dict = {
    "1": "Ножницы",
    "2": "Бумага", 
    "3": "Камень"
}

variants = ["Камень", "Ножницы", "Бумага"]
win = 0
total_game = 0

while True:
    clear_screen()
    bot_choice = random.choice(["Камень", "Ножницы", "Бумага"])
    
    print("\nКамень, Ножницы, Бумага!")
    print("1. Ножницы")
    print("2. Бумага")
    print("3. Камень")
    print("0. Выйти из игры")
    
    user_input = input("\nВведите номер варианта (1-3): ")
    
    if user_input == "0":
        print(f"\nИгра окончена! Игр сыграно: {total_game}")
        if total_game > 0:
            print(f"Побед: {win}")
            print(f"Win rate: {win/total_game:.2%}")
        break
    
    if user_input not in ["1", "2", "3"]:
        input("Неверный ввод! Нажмите Enter чтобы попробовать снова...")
        continue
    
    user_choice = variants_dict[user_input]
    total_game += 1
    
    print(f"\nВы выбрали: {user_choice}")
    print(f"Компьютер выбрал: {bot_choice}")
    
    if user_choice == bot_choice:
        print("Ничья!")
    
    elif (user_choice == "Ножницы" and bot_choice == "Бумага") or \
        (user_choice == "Бумага" and bot_choice == "Камень") or \
        (user_choice == "Камень" and bot_choice == "Ножницы"):
        print("Вы выиграли!")
        win += 1
    
    else:
        print("Вы проиграли!")
    
    print("\nСтатистика:")
    print(f"Сыграно игр: {total_game}")
    print(f"Побед: {win}")
    
    if total_game > 0:
        win_rate = win / total_game
        print(f"Процент побед: {win_rate:.2%}")
    
    input("\nНажмите Enter для следующего раунда...")