import random
from pathlib import Path


def game():
    path = Path('txt-cities-russia.txt')
    contents = path.read_text(encoding='utf-8')
    lines = contents.splitlines()
    while True:
        try:
            skip_letters = ['Ь', 'Ъ', 'Ы']


            user_input = str(input("Введите Город: ").strip().upper())
            if user_input.title() not in lines:
                print('Введите существующий город!')
                continue
            else:
                user_city = user_input

            last_letter = user_city[-1]

            if last_letter in skip_letters and len(user_city) > 1:
                last_letter = user_city[-2]

            possible_ai_cities = []
            for city in lines:
                if city[0] == last_letter:
                    possible_ai_cities.append(city)

            if possible_ai_cities:
                ai_city = random.choice(possible_ai_cities)
                print(ai_city)
        except:
            print('Произошла ошибка, пожайлуста попробуйте снова')

if __name__ == '__main__':
    game()
