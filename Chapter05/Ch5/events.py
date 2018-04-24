import tkinter as tk

win = tk.Tk()

can = tk.Canvas(win, width=300, height=300)
strvar = tk.StringVar()
lab = tk.Label(win, textvar=strvar)
strvar.set("Press a key")


def on_click(event=None):
    can.create_oval((event.x - 5, event.y - 5, event.x + 5, event.y + 5), fill="red")


def on_key_down(event=None):
    strvar.set(event.keysym)


def on_ctrl_d(event=None):
    top = tk.Toplevel(win)
    top.geometry("200x200")
    sv = tk.StringVar()
    sv.set("Hover the mouse over me")
    label = tk.Label(top, textvar=sv)
    label.bind("<Enter>", lambda e, sv=sv: sv.set("Hello mouse!"))
    label.bind("<Leave>", lambda e, sv=sv: sv.set("Goodbye mouse!"))
    label.pack(expand=1, fill=tk.BOTH)


can.bind('<Button-1>', on_click)
win.bind('<Control-d>', on_ctrl_d)
win.bind('<KeyPress>', on_key_down)
win.bind('<e>', lambda e, s=lab: lab.configure(font=(None, 18)))

can.pack()
lab.pack(side=tk.BOTTOM)

win.mainloop()
