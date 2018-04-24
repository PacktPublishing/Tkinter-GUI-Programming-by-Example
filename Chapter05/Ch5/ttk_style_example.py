import itertools
import tkinter as tk
import tkinter.ttk as ttk

win = tk.Tk()
style = ttk.Style()

style_1 = {'foreground': 'red', 'background': 'black'}
style_2 = {'foreground': 'yellow', 'background': 'grey'}

mapping_1 = {'background': [('pressed', 'gold'), ('active', 'magenta')]}
mapping_2 = {'background': [('pressed', 'chocolate'), ('active', 'blue4')]}

style_cycle = itertools.cycle([style_1, style_2])
mapping_cycle = itertools.cycle([mapping_1, mapping_2])

def switch_style():
    style_choice = next(style_cycle)
    mapping_choice = next(mapping_cycle)
    style.configure('TButton', **style_choice)
    style.map('TButton', **mapping_choice)
    # button.configure(style="TButton")

button = ttk.Button(win, text="style switch", command=switch_style)
button.pack(padx=50, pady=50)

win.mainloop()
