import pyautogui
import keyboard
import time
click_interval = 0
running = False
print('Нажмите "z" для запуска автокликера и "x" для остановки')
while True:
    if running:
        pyautogui.click()
        time.sleep(click_interval)
    if keyboard.is_pressed('z'):
        running = True
    elif keyboard.is_pressed('x'):
        running = False
    elif keyboard.is_pressed('q'):
        print('Выход из программы')
        break