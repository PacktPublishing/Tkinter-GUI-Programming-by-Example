import itertools
import tkinter as tk

style_1 = {'fg': 'red', 'bg': 'black', 'activebackground': 'gold', 'activeforeground': 'dim gray'}
style_2 = {'fg': 'yellow', 'bg': 'grey', 'activebackground': 'chocolate', 'activeforeground': 'blue4'}
style_cycle = itertools.cycle([style_1, style_2])


def switch_style():
    style = next(style_cycle)
    button_1.configure(**style)


win = tk.Tk()

button_1 = tk.Button(win, text="style switch", command=switch_style)
button_1.pack(padx=50, pady=50)

win.mainloop()
