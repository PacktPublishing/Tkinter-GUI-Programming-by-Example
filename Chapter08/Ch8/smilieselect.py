import os

import tkinter as tk
import tkinter.ttk as ttk


class SmilieSelect(tk.Toplevel):
    smilies_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'smilies/'))

    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)
        self.master = master
        self.transient(master)
        self.position_window()

        smilie_files = [file for file in os.listdir(self.smilies_dir) if file.endswith(".png")]

        self.smilie_images = []

        for file in smilie_files:
            full_path = os.path.join(self.smilies_dir, file)
            image = tk.PhotoImage(file=full_path)
            self.smilie_images.append(image)

        for index, file in enumerate(self.smilie_images):
            row, col = divmod(index, 3)
            button = ttk.Button(self, image=file, command=lambda s=file: self.insert_smilie(s))
            button.grid(row=row, column=col, sticky='nsew')

        for i in range(3):
            tk.Grid.columnconfigure(self, i, weight=1)
            tk.Grid.rowconfigure(self, i, weight=1)

    def position_window(self):
        master_pos_x = self.master.winfo_x()
        master_pos_y = self.master.winfo_y()

        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()

        my_width = 100
        my_height = 100

        pos_x = (master_pos_x + (master_width // 2)) - (my_width // 2)
        pos_y = (master_pos_y + (master_height // 2)) - (my_height // 2)

        geometry = f"{my_width}x{my_height}+{pos_x}+{pos_y}"
        self.geometry(geometry)

    def insert_smilie(self, smilie):
        self.master.add_smilie(smilie)
        self.destroy()


if __name__ == '__main__':
    w = tk.Tk()
    s = SmilieSelect(w)
    w.mainloop()