import random
import os
from pathlib import Path


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def Hangman():
    path = Path('russian.txt')
    
    contents = path.read_text()
    
    words = [word.strip().lower() for word in contents.split('\n') if word.strip()]
    
    secret_word = random.choice(words)
    secret_word_lower = secret_word.lower()
    
    word_letters = set(secret_word_lower)
    
    alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    
    used_letters = set()
    
    lives = 6
    
    word_display = ['_'] * len(secret_word)
    
    hangman_art = [
        '''
        ------
        |    |
        |    O
        |   /|\\
        |   / \\
        |
        ''',
        '''
        ------
        |    |
        |    O
        |   /|\\
        |   / 
        |
        ''',
        '''
        ------
        |    |
        |    O
        |   /|\\
        |
        |
        ''',
        '''
        ------
        |    |
        |    O
        |   /|
        |
        |
        ''',
        '''
        ------
        |    |
        |    O
        |    |
        |
        |
        ''',
        '''
        ------
        |    |
        |    O
        |
        |
        |
        ''',
        '''
        ------
        |    |
        |
        |
        |
        |
        '''
    ]
    
    print("=" * 50)
    print("ИГРА 'HANGMAN'")
    print("=" * 50)
    print(f"Слово: {''.join(word_display)}")
    print(f"Длина слова: {len(secret_word)} букв")
    print("У вас есть 6 попыток")
    print("=" * 50)
    
    while lives > 0 and '_' in word_display:
        clear_screen()
        print("\n" + hangman_art[lives])
        print("Слово: " + ''.join(word_display))
        print(f"Использованные буквы: {', '.join(sorted(used_letters)) if used_letters else 'пока нет'}")
        print(f"Осталось попыток: {lives}")
        
        guess = input("\nВведите букву: ").lower().strip()
        
        if len(guess) != 1:
            print("Пожалуйста, введите только одну букву!")
            continue
            
        if guess not in alphabet:
            print("Пожалуйста, введите русскую букву!")
            continue
            
        if guess in used_letters:
            print("Вы уже называли эту букву!")
            continue
        
        used_letters.add(guess)
        
        if guess in secret_word_lower:
            print(f"Буква '{guess}' есть в слове!")
            
            for i, letter in enumerate(secret_word_lower):
                if letter == guess:
                    word_display[i] = secret_word[i] 
                    
        else:
            lives -= 1
            print(f"Буквы '{guess}' нет в слове.")
    
    print("\n" + "=" * 50)
    
    if '_' not in word_display:
        print("ПОЗДРАВЛЯЕМ! ВЫ ВЫИГРАЛИ!")
        print(f"Загаданное слово: {secret_word}")
        print(f"Вы угадали слово с {6 - lives} ошибками!")
    else:
        print(hangman_art[0])
        print("ВЫ ПРОИГРАЛИ")
        print(f"Загаданное слово было: {secret_word}")
        
        print(f"Вы угадали: {''.join(word_display)}")
    
    print("=" * 50)

def main():
    print("ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'ВИСЕЛИЦА'!")
    print("Правила: Угадайте слово, называя буквы по одной.")
    print("За каждую ошибку будет рисоваться часть виселицы.")
    print("У вас есть 6 попыток.\n")
    clear_screen()
    
    while True:
        Hangman()
        
        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower().strip()
        if play_again not in ['да', 'д', 'yes', 'y', '+']:
            print("\nСпасибо за игру! До новых встреч!")
            break

if __name__ == "__main__":
    main()