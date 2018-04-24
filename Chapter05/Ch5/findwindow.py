import tkinter as tk
import tkinter.ttk as ttk


class FindWindow(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs  )

        self.geometry('350x100')
        self.title('Find and Replace')

        self.text_to_find = tk.StringVar()
        self.text_to_replace_with = tk.StringVar()

        top_frame = tk.Frame(self)
        middle_frame = tk.Frame(self)
        bottom_frame = tk.Frame(self)

        find_entry_label = tk.Label(top_frame, text="Find: ")
        self.find_entry = ttk.Entry(top_frame, textvar=self.text_to_find)

        replace_entry_label = tk.Label(middle_frame, text="Replace: ")
        self.replace_entry = ttk.Entry(middle_frame, textvar=self.text_to_replace_with)

        self.find_button = ttk.Button(bottom_frame, text="Find", command=self.on_find)
        self.replace = ttk.Button(bottom_frame, text="Replace", command=self.on_replace)
        self.cancel_button = ttk.Button(bottom_frame, text="Cancel", command=self.destroy)

        find_entry_label.pack(side=tk.LEFT, padx=(20, 0))
        self.find_entry.pack(side=tk.LEFT, fill=tk.X, expand=1)

        replace_entry_label.pack(side=tk.LEFT)
        self.replace_entry.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.find_button.pack(side=tk.LEFT, padx=(85, 0))
        self.cancel_button.pack(side=tk.RIGHT, padx=(0, 30))

        top_frame.pack(side=tk.TOP, expand=1, fill=tk.X, padx=30)
        middle_frame.pack(side=tk.TOP, expand=1, fill=tk.X, padx=30)
        bottom_frame.pack(side=tk.TOP, expand=1, fill=tk.X)

    def on_find(self):
        self.master.find(self.text_to_find.get())

    def on_replace(self):
        self.master.replace(self.text_to_find.get(), self.text_to_replace_with.get())


if __name__ == '__main__':
    mw = tk.Tk()
    fw = FindWindow(mw)
    mw.mainloop()
