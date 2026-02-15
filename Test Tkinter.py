import tkinter as tk

clicks = 0
addClicks = 1
needClicks = 10
def press_button():
    global clicks
    clicks += addClicks
    label2.config(text=str(clicks))

def rebirth():
    global clicks, addClicks, needClicks
    if clicks >= needClicks:
        clicks = 0
        addClicks += 1
        needClicks *= 2
        button2.config(text=f"Rebirth, {str(round(needClicks))}")

root = tk.Tk()
root.title("Clicker")
root.geometry("250x200")

label = tk.Label(root, text="Press button")
label.pack()

button = tk.Button(root, text="Click me", command=press_button)
button.pack()
button2 = tk.Button(root, text=f"Rebirth, {needClicks}", command=rebirth)
button2.pack()



label2 = tk.Label(root, text=clicks)
label2.pack()
label2.place(x = 120, y = 75)

root.mainloop()