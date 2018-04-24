import tkinter as tk

win = tk.Tk()
current_index = tk.StringVar()
text = tk.Text(win, bg="white", fg="black")
lab = tk.Label(win, textvar=current_index)


def update_index(event=None):
    cursor_position = text.index(tk.INSERT)
    cursor_position_pieces = str(cursor_position).split('.')

    cursor_line = cursor_position_pieces[0]
    cursor_char = cursor_position_pieces[1]

    current_index.set('line: ' + cursor_line + ' char: ' + cursor_char + ' index: ' + str(cursor_position))


text.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
lab.pack(side=tk.BOTTOM, fill=tk.X, expand=1)

text.bind('<KeyRelease>', update_index)

win.mainloop()
