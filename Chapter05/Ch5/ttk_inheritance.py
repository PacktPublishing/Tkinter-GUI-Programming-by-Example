import tkinter as tk
import tkinter.ttk as ttk

win = tk.Tk()

regular_button = ttk.Button(win, text="regular button")
small_button = ttk.Button(win, text="small button", style="small.TButton")
big_button = ttk.Button(win, text="big button", style="big.TButton")
big_dangerous_button = ttk.Button(win, text="big dangerous", style="danger.big.TButton")
small_dangerous_button = ttk.Button(win, text="small dangerous", style="danger.small.TButton")

style = ttk.Style()

style.configure('TButton', foreground="blue4")
style.configure('small.TButton', font=(None, 7))
style.configure('big.TButton', font=(None, 20))
style.configure('danger.small.TButton', foreground="red")
style.configure('danger.big.TButton', foreground="dark red")

regular_button.pack(padx=50, pady=50)
small_button.pack(padx=50, pady=50)
big_button.pack(padx=50, pady=50)
big_dangerous_button.pack(padx=50, pady=50)
small_dangerous_button.pack(padx=50, pady=50)

win.mainloop()
