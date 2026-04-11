import tkinter as tk

window = tk.Tk()


def test_handler(event):
    print(event.char)

window.bind("<Key>", test_handler)

window.mainloop()