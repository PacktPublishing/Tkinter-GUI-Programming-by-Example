import tkinter as tk
import tkinter.ttk as ttk
from tkinter.colorchooser import askcolor


class ColourChooser(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)
        self.master = master

        self.transient(self.master)
        self.geometry('400x300')
        self.title('Colour Scheme')
        self.configure(bg=self.master.background)

        self.chosen_background_colour = tk.StringVar()
        self.chosen_foreground_colour = tk.StringVar()
        self.chosen_text_background_colour = tk.StringVar()
        self.chosen_text_foreground_colour = tk.StringVar()

        self.chosen_background_colour.set(self.master.background)
        self.chosen_foreground_colour.set(self.master.foreground)
        self.chosen_text_background_colour.set(self.master.text_background)
        self.chosen_text_foreground_colour.set(self.master.text_foreground)

        window_frame = tk.Frame(self, bg=self.master.background)
        window_foreground_frame = tk.Frame(window_frame, bg=self.master.background)
        window_background_frame = tk.Frame(window_frame, bg=self.master.background)

        text_frame = tk.Frame(self, bg=self.master.background)
        text_foreground_frame = tk.Frame(text_frame, bg=self.master.background)
        text_background_frame = tk.Frame(text_frame, bg=self.master.background)

        self.all_frames = [window_frame, window_foreground_frame, window_background_frame,
                           text_frame, text_foreground_frame, text_background_frame]

        window_label = ttk.Label(window_frame, text="Window:", anchor=tk.W, style="editor.TLabel")
        foreground_label = ttk.Label(window_foreground_frame, text="Foreground:", anchor=tk.E, style="editor.TLabel")
        background_label = ttk.Label(window_background_frame, text="Background:", anchor=tk.E, style="editor.TLabel")

        text_label = ttk.Label(text_frame, text="Editor:", anchor=tk.W, style="editor.TLabel")
        text_foreground_label = ttk.Label(text_foreground_frame, text="Foreground:", anchor=tk.E, style="editor.TLabel")
        text_background_label = ttk.Label(text_background_frame, text="Background:", anchor=tk.E, style="editor.TLabel")

        foreground_colour_chooser = ttk.Button(window_foreground_frame, text="Change Foreground Colour", width=26, style="editor.TButton",
                                               command=lambda sv=self.chosen_foreground_colour: self.set_colour(sv))
        background_colour_chooser = ttk.Button(window_background_frame, text="Change Background Colour", width=26,
                                               style="editor.TButton",
                                               command=lambda sv=self.chosen_background_colour: self.set_colour(sv))
        text_foreground_colour_chooser = ttk.Button(text_foreground_frame, text="Change Text Foreground Colour",
                                                    width=26, style="editor.TButton",
                                                    command=lambda sv=self.chosen_text_foreground_colour: self.set_colour(sv))
        text_background_colour_chooser = ttk.Button(text_background_frame, text="Change Text Background Colour",
                                                    width=26, style="editor.TButton",
                                                    command=lambda sv=self.chosen_text_background_colour: self.set_colour(sv))

        foreground_colour_preview = ttk.Label(window_foreground_frame, textvar=self.chosen_foreground_colour,
                                              style="editor.TLabel")
        background_colour_preview = ttk.Label(window_background_frame, textvar=self.chosen_background_colour,
                                              style="editor.TLabel")
        text_foreground_colour_preview = ttk.Label(text_foreground_frame, textvar=self.chosen_text_foreground_colour,
                                                   style="editor.TLabel")
        text_background_colour_preview = ttk.Label(text_background_frame, textvar=self.chosen_text_background_colour,
                                                   style="editor.TLabel")


        window_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
        window_label.pack(side=tk.TOP, fill=tk.X)

        window_foreground_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
        window_background_frame.pack(side=tk.TOP, fill=tk.X, expand=1)

        foreground_label.pack(side=tk.LEFT, padx=30, pady=10)
        foreground_colour_chooser.pack(side=tk.LEFT)
        foreground_colour_preview.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=(15, 0))

        background_label.pack(side=tk.LEFT, fill=tk.X, padx=(30, 27))
        background_colour_chooser.pack(side=tk.LEFT)
        background_colour_preview.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=(15, 0))

        text_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
        text_label.pack(side=tk.TOP, fill=tk.X)

        text_foreground_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
        text_background_frame.pack(side=tk.TOP, fill=tk.X, expand=1)

        text_foreground_label.pack(side=tk.LEFT, padx=30, pady=10)
        text_foreground_colour_chooser.pack(side=tk.LEFT)
        text_foreground_colour_preview.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=(15, 0))

        text_background_label.pack(side=tk.LEFT, fill=tk.X, padx=(30, 27))
        text_background_colour_chooser.pack(side=tk.LEFT)
        text_background_colour_preview.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=(15, 0))

        save_button = ttk.Button(self, text="save", command=self.save, style="editor.TButton")
        save_button.pack(side=tk.BOTTOM, pady=(0, 20))

    def set_colour(self, sv):
        choice = askcolor()[1]
        sv.set(choice)

    def save(self):
        yaml_file_contents = f"background: '{self.chosen_background_colour.get()}'\n" \
                             + f"foreground: '{self.chosen_foreground_colour.get()}'\n" \
                             + f"text_background: '{self.chosen_text_background_colour.get()}'\n" \
                             + f"text_foreground: '{self.chosen_text_foreground_colour.get()}'\n"

        with open(self.master.default_scheme_path, "w") as yaml_file:
            yaml_file.write(yaml_file_contents)

        self.master.apply_colour_scheme(self.chosen_foreground_colour.get(), self.chosen_background_colour.get(),
                                        self.chosen_text_foreground_colour.get(), self.chosen_text_background_colour.get())
        for frame in self.all_frames:
            frame.configure(bg=self.chosen_background_colour.get())

        self.configure(bg=self.chosen_background_colour.get())



