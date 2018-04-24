import tkinter as tk

window = tk.Tk()

canvas = tk.Canvas(window, bg="white", width=300, height=300)

canvas.pack()

canvas.create_oval((0, 0, 300, 300), fill="yellow")

canvas.create_arc((50, 100, 100, 150), extent=180, fill="black")

canvas.create_arc((200, 100, 250, 150), extent=180, fill="black")

canvas.create_line((50, 200, 110, 240), fill="red", width=5)
canvas.create_line((110, 240, 190, 240), fill="red", width=5)
canvas.create_line((190, 240, 250, 200), fill="red", width=5)

window.mainloop()
