import tkinter as tk
import tkinter.ttk as ttk

win = tk.Tk()
name_frame = ttk.Frame(win)
address_frame = ttk.Frame(win)

name_label_frame = ttk.LabelFrame(name_frame, text="Name")
address_label = ttk.Label(win, text="Address")
address_label_frame = ttk.LabelFrame(address_frame, labelwidget=address_label)

first_name = ttk.Entry(name_label_frame)
last_name = ttk.Entry(name_label_frame)

first_name.pack(side=tk.TOP)
last_name.pack(side=tk.BOTTOM)

name_label_frame.pack(fill=tk.BOTH, expand=1)
name_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

address_1 = ttk.Entry(address_label_frame)
address_2 = ttk.Entry(address_label_frame)
address_3 = ttk.Entry(address_label_frame)

address_1.pack(side=tk.TOP)
address_2.pack(side=tk.TOP)
address_3.pack(side=tk.TOP)

address_label_frame.pack(fill=tk.BOTH, expand=1)
address_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

win.mainloop()