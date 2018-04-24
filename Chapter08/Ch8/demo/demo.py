import tkinter as tk

win = tk.Tk()
canvas = tk.Canvas(win)
frame = tk.Frame(canvas)

scroll = tk.Scrollbar(win, orient='vertical', command=canvas.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scroll.set)
canvas.pack(fill=tk.BOTH, expand=1)
canvas.create_window((0, 0), window=frame, anchor='nw')


def on_frame_resized(self, event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


win.bind('<Configure>', on_frame_resized)

for _ in range(30):
    tk.Label(frame, text="big label").pack(pady=20)

win.mainloop()