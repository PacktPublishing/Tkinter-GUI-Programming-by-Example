import random
import tkinter as tk

win = tk.Tk()
sv = tk.StringVar()
sv.set('You are walking around with an open wallet...')
lab = tk.Label(win, textvar=sv)


def user_found_money(event=None):
    amount = event.x
    sv.set('You found £' + str(amount))


def user_lost_money(event=None):
    amount = event.x
    sv.set('You dropped £' + str(amount))


def emit_custom_event():
    choices = ['find', 'lose']
    choice = random.choice(choices)

    if choice == 'find':
        win.event_generate("<<Find>>", x=random.randint(0, 50))
    else:
        win.event_generate("<<Lose>>", x=random.randint(0, 50))

    win.after(2000, emit_custom_event)


lab.pack(padx=50, pady=50)

win.bind("<<Find>>", user_found_money)
win.bind("<<Lose>>", user_lost_money)

win.after(2000, emit_custom_event)

win.mainloop()


