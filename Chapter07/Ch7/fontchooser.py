import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import families


class FontChooser(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)
        self.master = master

        self.transient(self.master)
        self.geometry('500x250')
        self.title('Choose font and size')

        self.configure(bg=self.master.background)

        self.font_list = tk.Listbox(self, exportselection=False)

        self.available_fonts = sorted(families())

        for family in self.available_fonts:
            self.font_list.insert(tk.END, family)

        current_selection_index = self.available_fonts.index(self.master.font_family)
        if current_selection_index:
            self.font_list.select_set(current_selection_index)
            self.font_list.see(current_selection_index)

        self.size_input = tk.Spinbox(self, from_=0, to=99, value=self.master.font_size)

        self.save_button = ttk.Button(self, text="Save", style="editor.TButton", command=self.save)

        self.save_button.pack(side=tk.BOTTOM, fill=tk.X, expand=1, padx=40)
        self.font_list.pack(side=tk.LEFT, fill=tk.Y, expand=1)
        self.size_input.pack(side=tk.BOTTOM, fill=tk.X, expand=1)

    def save(self):
        font_family = self.font_list.get(self.font_list.curselection()[0])
        yaml_file_contents = f"family: {font_family}\n" \
                           + f"size: {self.size_input.get()}"

        with open(self.master.font_file, 'w') as file:
            file.write(yaml_file_contents)

        self.master.update_font()

