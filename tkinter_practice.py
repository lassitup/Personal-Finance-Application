import tkinter as tk

window = tk.Tk()
greeting = tk.Label(text="Enter Expense Type", fg= "blue", bg = "yellow", width=50, height=20)
#greeting.pack()
button1 = tk.Button(text="Click Here!", bg = "blue", highlightbackground = "blue", fg = "orange", width = 50, height = 20)
#button1.pack()

entry = tk.Entry(fg="yellow", bg="blue", width=50)
#entry.pack()

text_box = tk.Text()
#text_box.pack()

#response = text_box.get("1.0", tk.END)

# frame_a = tk.Frame(relief = tk.SUNKEN, borderwidth=3)
# frame_b = tk.Frame(relief = tk.RAISED, borderwidth=3)


# label_a = tk.Label(master=frame_a, text = "I'm in Frame A")
# label_a.pack()
# label_b = tk.Label(master=frame_b, text = "I'm in Frame B")
# label_b.pack()

# frame_b.pack(side=tk.LEFT)
# frame_a.pack(side=tk.RIGHT)


# border_effects = {
#     "flat": tk.FLAT,
#     "sunken": tk.SUNKEN,
#     "raised": tk.RAISED,
#     "groove": tk.GROOVE,
#     "ridge": tk.RIDGE,
# }

# window = tk.Tk()

# for relief_name, relief in border_effects.items():
#     frame = tk.Frame(master=window, relief=relief, borderwidth=5)
#     frame.pack(side=tk.LEFT)
#     label = tk.Label(master=frame, text=relief_name)
#     label.pack()


# frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
# frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# frame2 = tk.Frame(master=window, width=100, bg="yellow")
# frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# frame3 = tk.Frame(master=window, width=50, bg="blue")
# frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
frame1.pack(fill=tk.BOTH, expand=True)
frame1.pack()
label1 = tk.Label(master=frame1, text="Where does this go!?")
label1.pack()

frame2 = tk.Frame(master=window, width=200, height=100, bg="blue", relief=tk.RAISED, borderwidth=1)
frame2.pack(fill=tk.BOTH, expand=True)
frame2.pack()

for i in range(3):
    frame2.rowconfigure(i, weight=1, minsize=50)

    for j in range(3):
        frame2.columnconfigure(i, weight=1, minsize=75)
        frame = tk.Frame(master=frame2, width=200, height=100, bg="blue", relief=tk.RAISED, borderwidth=1)
        frame.grid(row=i, column=j, padx=5, pady=5)
        label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
        label.pack()


def event_test(event):
    response = text_box.get("1.0", tk.END).strip()
    print("Success!")
    print(response)

text_box = tk.Text()
text_box.pack(fill=tk.BOTH, expand=True)

#response = text_box.get("1.0", tk.END)



button_test = tk.Button(master=window, text="Push Me!")
button_test.bind("<Button-1>", event_test)
button_test.pack(fill=tk.BOTH, expand=True)




window.mainloop()
