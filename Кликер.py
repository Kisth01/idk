import tkinter as tk

clicks = 0
needClicks = 10
addClicks = 1

def open_shop():
    global clicks, needClicks, addClicks
    shop_window = tk.Toplevel(root)
    shop_window.title("Магазин")
    shop_window.geometry("300x200")

    label = tk.Label(shop_window, text="Добро пожаловать в магазин!")
    label.pack(pady=10)

    label_item = tk.Label(shop_window, text="Умножение кликов на 2!")
    label_item.pack(pady=5)

    btn_buy = tk.Button(shop_window, text=f"Купить за {needClicks}")
    btn_buy.pack(pady=5)
    if clicks >= needClicks:
        print("Куплено!")
        clicks -= needClicks
        addClicks += 1
        needClicks *= 2


    btn_close = tk.Button(shop_window, text="Закрыть", command=shop_window.destroy)
    btn_close.pack(pady=5)

def total_clicks():
    global clicks
    clicks += addClicks
    label.config(text=str(clicks))


root = tk.Tk()
root.title("Основное окно")
root.geometry("400x300")

label = tk.Label(root, text="Нажимай на кнопки!")
label.pack(pady=20)

btn_click = tk.Button(root, text="Кликни меня", command=total_clicks)
btn_click.pack(pady=5)

btn_shop = tk.Button(root, text="Магазин", command=open_shop)
btn_shop.pack(pady=5)

root.mainloop()