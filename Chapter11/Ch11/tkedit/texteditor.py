import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from pathlib import Path

import yaml

from tkinter import filedialog

from textarea import TextArea
from linenumbers import LineNumbers
from highlighter import Highlighter
from findwindow import FindWindow
from colourchooser import ColourChooser
from fontchooser import FontChooser


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Python Text Editor v3')
        self.geometry('800x600')

        self.foreground = 'black'
        self.background = 'lightgrey'
        self.text_foreground = 'black'
        self.text_background='white'

        self.config_dir = os.path.join(str(Path.home()), '.tkedit')

        self.default_scheme_path = os.path.join(self.config_dir, 'schemes/default.yaml')
        self.python_language_path = os.path.join(self.config_dir, 'languages/python.yaml')
        self.font_scheme_path = os.path.join(self.config_dir, 'schemes/font.yaml')
        self.create_config_directory_if_needed()

        self.load_scheme_file(self.default_scheme_path)
        self.configure_ttk_elements()

        self.font_size = 15
        self.font_family = "Ubuntu Mono"
        self.load_font_file(self.font_scheme_path)

        self.text_area = TextArea(self, bg=self.text_background, fg=self.text_foreground, undo=True,
                                  font=(self.font_family, self.font_size))

        self.scrollbar = ttk.Scrollbar(orient="vertical", command=self.scroll_text)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)

        self.line_numbers = LineNumbers(self, self.text_area, bg="grey", fg="white", width=1)
        self.highlighter = Highlighter(self.text_area, self.python_language_path)

        self.menu = tk.Menu(self, bg=self.background, fg=self.foreground)
        self.all_menus = [self.menu]

        sub_menu_items = ["file", "edit", "tools", "help"]
        self.generate_sub_menus(sub_menu_items)
        self.configure(menu=self.menu)

        self.right_click_menu = tk.Menu(self, bg=self.background, fg=self.foreground, tearoff=0)
        self.right_click_menu.add_command(label='Cut', command=self.edit_cut)
        self.right_click_menu.add_command(label='Copy', command=self.edit_copy)
        self.right_click_menu.add_command(label='Paste', command=self.edit_paste)
        self.all_menus.append(self.right_click_menu)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.bind_events()

        self.open_file = ''

    def bind_events(self):
        self.text_area.bind("<MouseWheel>", self.scroll_text)
        self.text_area.bind("<Button-4>", self.scroll_text)
        self.text_area.bind("<Button-5>", self.scroll_text)
        self.text_area.bind("<Button-3>", self.show_right_click_menu)

        self.bind('<Control-f>', self.show_find_window)

        self.bind('<Control-n>', self.file_new)
        self.bind('<Control-o>', self.file_open)
        self.bind('<Control-s>', self.file_save)

        self.bind('<Control-h>', self.help_about)

        self.bind('<Control-m>', self.tools_change_syntax_highlighting)
        self.bind('<Control-g>', self.tools_change_colour_scheme)
        self.bind('<Control-l>', self.tools_change_font)

        self.line_numbers.bind("<MouseWheel>", lambda e: "break")
        self.line_numbers.bind("<Button-4>", lambda e: "break")
        self.line_numbers.bind("<Button-5>", lambda e: "break")

    def scroll_text(self, *args):
        if len(args) > 1:
            self.text_area.yview_moveto(args[1])
            self.line_numbers.yview_moveto(args[1])
        else:
            event = args[0]
            if event.delta:
                move = -1 * (event.delta / 120)
            else:
                if event.num == 5:
                    move = 1
                else:
                    move = -1

            self.text_area.yview_scroll(int(move), "units")
            self.line_numbers.yview_scroll(int(move) * 3, "units")

    def show_find_window(self, event=None):
        FindWindow(self.text_area)

    def show_right_click_menu(self, event):
        x = self.winfo_x() + self.text_area.winfo_x() + event.x
        y = self.winfo_y() + self.text_area.winfo_y() + event.y
        self.right_click_menu.post(x, y)

    def generate_sub_menus(self, sub_menu_items):
        window_methods = [method_name for method_name in dir(self)
                          if callable(getattr(self, method_name))]
        tkinter_methods = [method_name for method_name in dir(tk.Tk)
                           if callable(getattr(tk.Tk, method_name))]

        my_methods = [method for method in set(window_methods) - set(tkinter_methods)]
        my_methods = sorted(my_methods)

        for item in sub_menu_items:
            sub_menu = tk.Menu(self.menu, tearoff=0, bg=self.background, fg=self.foreground)
            matching_methods = []
            for method in my_methods:
                if method.startswith(item):
                    matching_methods.append(method)

            for match in matching_methods:
                actual_method = getattr(self, match)
                method_shortcut = actual_method.__doc__.strip()
                friendly_name = ' '.join(match.split('_')[1:])
                sub_menu.add_command(label=friendly_name.title(), command=actual_method, accelerator=method_shortcut)

            self.menu.add_cascade(label=item.title(), menu=sub_menu)
            self.all_menus.append(sub_menu)

    def show_about_page(self):
        msg.showinfo("About", "My text editor, version 2, written in Python3.6 using tkinter!")

    def load_syntax_highlighting_file(self):
        syntax_file = filedialog.askopenfilename(filetypes=[("YAML file", ("*.yaml", "*.yml"))])
        if syntax_file:
            self.highlighter.clear_highlight()
            self.highlighter = Highlighter(self.text_area, syntax_file)
            self.highlighter.force_highlight()

    def load_scheme_file(self, scheme):
        with open(scheme, 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as error:
                print(error)
                return

        self.foreground = config['foreground']
        self.background = config['background']
        self.text_foreground = config['text_foreground']
        self.text_background = config['text_background']

    def load_font_file(self, file_path):
        with open(file_path, 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as error:
                print(error)
                return

        self.font_family = config['family']
        self.font_size = config['size']

    def change_colour_scheme(self):
        ColourChooser(self)

    def apply_colour_scheme(self, foreground, background, text_foreground, text_background):
        self.text_area.configure(fg=text_foreground, bg=text_background)
        self.background = background
        self.foreground = foreground
        for menu in self.all_menus:
            menu.configure(bg=self.background, fg=self.foreground)
        self.configure_ttk_elements()

    def configure_ttk_elements(self):
        style = ttk.Style()
        style.configure('editor.TLabel', foreground=self.foreground, background=self.background)
        style.configure('editor.TButton', foreground=self.foreground, background=self.background)

    def change_font(self):
        FontChooser(self)

    def update_font(self):
        self.load_font_file(self.font_scheme_path)
        self.text_area.configure(font=(self.font_family, self.font_size))

    def create_config_directory_if_needed(self):
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)
            os.mkdir(os.path.join(self.config_dir, 'schemes'))
            os.mkdir(os.path.join(self.config_dir, 'languages'))

        self.create_default_scheme_if_needed()
        self.create_font_scheme_if_needed()
        self.create_python_language_if_needed()

    def create_default_scheme_if_needed(self):
        if not os.path.exists(self.default_scheme_path):
            yaml_file_contents = f"background: 'lightgrey'\n" \
                             + f"foreground: 'black'\n" \
                             + f"text_background: 'white'\n" \
                             + f"text_foreground: 'black'\n"

            with open(self.default_scheme_path, 'w') as yaml_file:
                yaml_file.write(yaml_file_contents)

    def create_font_scheme_if_needed(self):
        if not os.path.exists(self.font_scheme_path):
            yaml_file_contents = f"family: Ubuntu Mono\n" \
                               + f"size: 14"

            with open(self.font_scheme_path, 'w') as yaml_file:
                yaml_file.write(yaml_file_contents)

    def create_python_language_if_needed(self):
        if not os.path.exists(self.python_language_path):
            yaml_file_contents = """
categories:
  keywords:
    colour: orange
    matches: [for, def, while, from, import, as, with, self]

  variables:
    colour: red4
    matches: ['True', 'False', None]

  conditionals:
    colour: green
    matches: [try, except, if, else, elif]

  functions:
    colour: blue4
    matches: [int, str, dict, list, set, float]

numbers:
  colour: purple

strings:
  colour: '#e1218b'
"""
            with open(self.python_language_path, 'w') as yaml_file:
                yaml_file.write(yaml_file_contents)







    # =========== Menu Functions ==============

    def file_new(self, event=None):
        """
        Ctrl+N
        """
        self.text_area.delete(1.0, tk.END)
        self.open_file = None
        self.line_numbers.force_update()

    def file_open(self, event=None):
        """
        Ctrl+O
        """
        file_to_open = filedialog.askopenfilename()
        if file_to_open:
            self.open_file = file_to_open

            self.text_area.display_file_contents(file_to_open)
            self.highlighter.force_highlight()
            self.line_numbers.force_update()

    def file_save(self, event=None):
        """
        Ctrl+S
        """
        current_file = self.open_file if self.open_file else None
        if not current_file:
            current_file = filedialog.asksaveasfilename()

        if current_file:
            contents = self.text_area.get(1.0, tk.END)
            with open(current_file, 'w') as file:
                file.write(contents)

    def edit_cut(self, event=None):
        """
        Ctrl+X
        """
        self.text_area.event_generate("<Control-x>")
        self.line_numbers.force_update()

    def edit_paste(self, event=None):
        """
        Ctrl+V
        """
        self.text_area.event_generate("<Control-v>")
        self.line_numbers.force_update()
        self.highlighter.force_highlight()

    def edit_copy(self, event=None):
        """
        Ctrl+C
        """
        self.text_area.event_generate("<Control-c>")

    def edit_select_all(self, event=None):
        """
        Ctrl+A
        """
        self.text_area.event_generate("<Control-a>")

    def edit_find_and_replace(self, event=None):
        """
        Ctrl+F
        """
        self.show_find_window()

    def help_about(self, event=None):
        """
        Ctrl+H
        """
        self.show_about_page()

    def tools_change_syntax_highlighting(self, event=None):
        """
        Ctrl+M
        """
        self.load_syntax_highlighting_file()

    def tools_change_colour_scheme(self, event=None):
        """
        Ctrl+G
        """
        self.change_colour_scheme()

    def tools_change_font(self, event=None):
        """
        Ctrl+L
        """
        self.change_font()

def main():
    mw = MainWindow()
    mw.mainloop()

if __name__ == '__main__':
    mw = MainWindow()
    mw.mainloop()

