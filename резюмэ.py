import time
print("Привет, как тебя зовут?")
name = str(input())
time.sleep(2)
if name == "Глеб":
    time.sleep(2)
    print("Эй, это имя разработчика")
elif name == "Макс":
    time.sleep(2)
    print("Это же не приложение мне пишет?")
else:
    time.sleep(2)
    print("Запомнил")    

time.sleep(2)
print("Сколько тебе лет?") 
age = int(input())

if age >= 18:
    time.sleep(2)
    print("Ого, ты взрослый")
elif age == 14:
    time.sleep(2)
    print("Ты уже получил паспорт?")
    havepasport = str(input())
    if havepasport == "Да":
        time.sleep(2)
        print("Ого, это круто!")
    else:
        time.sleep(2)
        print("Печально:(")
elif age<=7:
    time.sleep(2)
    print("Ты совсем маленький...")
else:
    time.sleep(2)
    print("Ага, понял")                 

time.sleep(2)
print("Когда у тебя день рождения?")
date = int(input("Число: "))
month = int(input("Месяц: "))
year = int(input("Год: "))


time.sleep(2)
print("Так, дальше, где ты живешь?")
print("Если не хочешь писать то напиши: ""Нет" )
print("Если хочешь продолжить то напиши: ""Да" )
YesOrNo = str(input())
if YesOrNo == "Да":
    time.sleep(2)
    adress = str(input("Адрес: "))
else:
    time.sleep(2)
    print("Ну ладно:( ") 


time.sleep(2)
print("Какая твоя любимая еда?")
favoriteEat = str(input())
time.sleep(2)
print("Какое твое любимое животное?")
favoritePet = str(input())

time.sleep(2)
print("У тебя есть домашний питомец?")
havePet = str(input())
if havePet == "Да":
    print("Кто это? И как зовут Его/Её?")
    pet = str(input("Питомец: "))
    namePet = str(input("Имя питомца: "))
else:
    time.sleep(2)
    print("Печально")

time.sleep(2)
print("Хочешь покажу твое резюме?")
NoOrYes = str(input())
if NoOrYes == "Да":
    print(f"Ваше имя: {name}")
    print(f"Ваш возраст: {age}")
    print(f"Ваш день рождения: {date}.{month}.{year}")
    print(f"Ваша любимая еда: {favoriteEat}")
    print(f"Ваше любимое животное: {favoritePet}")
    if havePet == "Да":
        print(f"Ваш домашний питомец: {pet}{namePet}")
        if adress == "Да":
            print(f"Ваш адрес: {adress}")