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


def highlight_line(event=None):
    start = str(text.index(tk.INSERT)) + " linestart"
    end = str(text.index(tk.INSERT)) + " lineend"
    text.tag_add("sel", start, end)

    return "break"


def highlight_word(event=None):
    word_pos = str(text.index(tk.INSERT))
    start = word_pos + " wordstart"
    end = word_pos + " wordend"
    text.tag_add("sel", start, end)

    return "break"


def down_three_lines(event=None):
    current_cursor_index = str(text.index(tk.INSERT))
    new_position = current_cursor_index + "+3l"
    text.mark_set(tk.INSERT, new_position)

    return "break"


def back_four_chars(event=None):
    current_cursor_index = str(text.index(tk.INSERT))
    new_position = current_cursor_index + "-4c"
    text.mark_set(tk.INSERT, new_position)

    return "break"


def tag_alternating(event=None):
    for i in range(0, 27, 2):
        index = '1.' + str(i)
        end = index + '+1c'
        text.tag_add('odd', index, end)

    text.tag_configure('odd', foreground='orange')

    return "break"


def raise_selected(event=None):
    text.tag_configure('raise', offset=5)
    selection = text.tag_ranges("sel")
    text.tag_add('raise', selection[0], selection[1])

    return "break"


def underline_selected(event=None):
    text.tag_configure('underline', underline=1)
    selection = text.tag_ranges("sel")
    text.tag_add('underline', selection[0], selection[1])

    return "break"


text.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
lab.pack(side=tk.BOTTOM, fill=tk.X, expand=1)

text.bind('<KeyRelease>', update_index)
text.bind('<Control-h>', highlight_line)
text.bind('<Control-w>', highlight_word)
text.bind('<Control-d>', down_three_lines)
text.bind('<Control-b>', back_four_chars)

text.bind('<Control-t>', tag_alternating)
text.bind('<Control-r>', raise_selected)
text.bind('<Control-u>', underline_selected)

win.mainloop()
