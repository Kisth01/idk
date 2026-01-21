import random
import time

title_list = []

name = str(input("Введи Имя: "))
password = int(input("Пароль: "))
if name.title() == "Kisth" and password == 456996752:
    win_in_easy = 999
    win_in_medium = 999
    win_in_hard = 999
    win_in_impossible = 999
    win_in_mod = 999
    streak = 999
    Id = 9
    beststreak = 999
    totallvl = 999
    listTitle = ['Разработчик']
else:
    win_in_easy = 0
    win_in_medium = 0
    win_in_hard = 0
    win_in_impossible = 0
    win_in_mod = 0
    streak = 0
    Id = random.randint(1000000000, 9999999999)
    beststreak = 0
    totallvl = 0
    listTitle = []


print(f'\n\t\t{name.title()}, добро пожаловать в "Угадай число!"' + "\tРазработчик Kisth")
while True:
    print("\nВыберите сложность игры:" + "\tПобеды:" + f"\t\t\tВаша серия выйграшных игр(сбрасывается при перезапуске!): {streak}" + "🔥" + f"\t\t Ваше Имя: {name.title()}")
    print("1. Легкая (до 10 чисел)" + f"\t\t   {win_in_easy}" + f"\t\t\t\t\t\t\t\t\t\t\t\t Айди Игрока: {Id}")
    print("2. Средняя (до 30 чисел)" + f"           {win_in_medium}" + f"\t\t\t\t\t\t\t\t\t\t\t\t Лучшая серия выйграшных игр: {beststreak}")
    print("3. Сложная (до 50 чисел)" + f"           {win_in_hard}" +  f"\t\t\t\t\t\t\t\t\t\t\t\t Сыграно игр: {totallvl}")
    print("4. Невозможно (до 1000 чисел)" + f"      {win_in_impossible}" + f"\t\t\t\t\t\t\t\t\t\t\t\t Титул: {title_list}")
    print("5. Своя настройка" + f"\t\t   {win_in_mod}")
    print("6. Титулы")
    time.sleep(1)
    con_num = int(input("Введите цифру для продолжения: "))

    if con_num == 1:
        guess_num_for_easy = random.randint(1, 10)
        mystery_num = 0
        att = 0
        while mystery_num != guess_num_for_easy:
            mystery_num = int(input("\nВведи число: "))
            if att == 5:
                time.sleep(1)
                print("Ты проиграл!:(")
                print(f"Загадочное число: {guess_num_for_easy}")
                totallvl += 1
                streak -= streak
                break
            elif mystery_num < guess_num_for_easy:
                time.sleep(1)
                print("Слишком мало, попробуй снова")
                att += 1
            elif mystery_num > guess_num_for_easy:
                time.sleep(1)
                print("Слишком много, попробуй снова")
                att += 1
            elif mystery_num == guess_num_for_easy:
                time.sleep(1)
                print("Ты угадал!")
                win_in_easy +=1
                streak += 1
                beststreak += 1
                totallvl +=1
    elif con_num == 2:
        guess_num_for_medium = random.randint(1, 30)
        mystery_num = 0
        while mystery_num != guess_num_for_medium:
            mystery_num = int(input("\nВведи число: "))
            att = 0
            if att == 15:
                time.sleep(1)
                print("Ты проиграл!:(")
                print(f"Загадочное число: {guess_num_for_medium}")
                totallvl += 1
                streak -= streak
                break
            elif mystery_num < guess_num_for_medium:
                time.sleep(1)
                print("Слишком мало, попробуй снова")
                att += 1
            elif mystery_num > guess_num_for_medium:
                time.sleep(1)
                print("Слишком много, попробуй снова")
                att += 1
            elif mystery_num == guess_num_for_medium:
                time.sleep(1)
                print("Ты угадал!")
                win_in_medium += 1
                streak += 1
                beststreak += 1
                totallvl += 1
    elif con_num == 3:
        guess_num_for_hard = random.randint(1, 50)
        mystery_num = 0
        while mystery_num != guess_num_for_hard:
            mystery_num = int(input("\nВведи число: "))
            att = 0
            if att == 15:
                time.sleep(1)
                print("Ты проиграл!:(")
                print(f"Загадочное число: {guess_num_for_hard}")
                totallvl += 1
                streak -= streak
                break
            elif mystery_num < guess_num_for_hard:
                time.sleep(1)
                print("Слишком мало, попробуй снова")
                att += 1
            elif mystery_num > guess_num_for_hard:
                time.sleep(1)
                print("Слишком много, попробуй снова")
                att += 1
            elif mystery_num == guess_num_for_hard:
                time.sleep(1)
                print("Ты угадал!")
                win_in_hard += 1
                streak += 1
                beststreak += 1
                totallvl += 1
    elif con_num == 4:
        guess_num_for_impossible = random.randint(1, 1000)
        mystery_num = 0
        while mystery_num != guess_num_for_impossible:
            mystery_num = int(input("\nВведи число: "))
            att = 0
            if att == 50:
                time.sleep(1)
                print("Ты проиграл!:(")
                print(f"Загадочное число: {guess_num_for_impossible}")
                totallvl += 1
                streak -= streak
                break
            elif mystery_num < guess_num_for_impossible:
                time.sleep(1)
                print("Слишком мало, попробуй снова")
                att += 1
            elif mystery_num > guess_num_for_impossible:
                time.sleep(1)
                print("Слишком много, попробуй снова")
                att += 1
            elif mystery_num == guess_num_for_impossible:
                time.sleep(1)
                print("Ты угадал!")
                win_in_impossible += 1
                streak += 1
                beststreak += 1
                totallvl += 1
    elif con_num == 5:
        pol_setting = int(input("Введите число до какого числа вы хотите: "))
        guess_num_for_mod = random.randint(1, pol_setting)
        mystery_num = 0
        while mystery_num != guess_num_for_mod:
            mystery_num = int(input("\nВведи число: "))
            att = 0
            if att == 100:
                time.sleep(1)
                print("Ты проиграл!:(")
                print(f"Загадочное число: {guess_num_for_mod}")
                totallvl += 1
                streak -= streak
                break
            elif mystery_num < guess_num_for_mod:
                time.sleep(1)
                print("Слишком мало, попробуй снова")
                att += 1
            elif mystery_num > guess_num_for_mod:
                time.sleep(1)
                print("Слишком много, попробуй снова")
                att += 1
            elif mystery_num == guess_num_for_mod:
                time.sleep(1)
                print("Ты угадал!")
                win_in_mod += 1
                streak += 1
                beststreak += 1
                totallvl += 1
    elif con_num == 6:
        if win_in_easy >= 9 and win_in_medium >= 9 and win_in_hard >= 9 and win_in_impossible >= 9:
            listTitle.append("9, 9 и еще раз 9")
        if streak >= 50:
            listTitle.append("Маг огня")
        if totallvl >= 10:
            listTitle.append("Новичок")
        if beststreak >= 50:
            listTitle.append("Огонь который никогда не потухнет")
        print("Ваши титулы: ")
        for index, list in enumerate(listTitle):
            print(index +1, list)
        num_for_title = int(input("Введите цифру для титула:"))
        title_list = listTitle[num_for_title - 1]
