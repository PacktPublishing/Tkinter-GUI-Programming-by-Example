import tkinter as tk

import yaml


class Highlighter:
    def __init__(self, text_widget, syntax_file):
        self.text_widget = text_widget
        self.syntax_file = syntax_file
        self.categories = None
        self.numbers_colour = "blue"
        self.strings_colour = "red"

        self.disallowed_previous_chars = ["_", "-", "."]

        self.parse_syntax_file()

        self.text_widget.bind('<KeyRelease>', self.on_key_release)

    def on_key_release(self, event=None):
        self.highlight()

    def parse_syntax_file(self):
        with open(self.syntax_file, 'r') as stream:
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as error:
                print(error)
                return

        self.categories = config['categories']
        self.numbers_colour = config['numbers']['colour']
        self.strings_colour = config['strings']['colour']

        self.configure_tags()

    def configure_tags(self):
        for category in self.categories.keys():
            colour = self.categories[category]['colour']
            self.text_widget.tag_configure(category, foreground=colour)

        self.text_widget.tag_configure("number", foreground=self.numbers_colour)
        self.text_widget.tag_configure("string", foreground=self.strings_colour)

    def highlight(self, event=None):
        length = tk.IntVar()
        for category in self.categories:
            matches = self.categories[category]['matches']
            for keyword in matches:
                start = 1.0
                keyword = keyword + "[^A-Za-z_-]"
                idx = self.text_widget.search(keyword, start, stopindex=tk.END, count=length, regexp=1)
                while idx:
                    char_match_found = int(str(idx).split('.')[1])
                    line_match_found = int(str(idx).split('.')[0])
                    if char_match_found > 0:
                        previous_char_index = str(line_match_found) + '.' + str(char_match_found - 1)
                        previous_char = self.text_widget.get(previous_char_index, previous_char_index + "+1c")

                        if previous_char.isalnum() or previous_char in self.disallowed_previous_chars:
                            end = f"{idx}+{length.get() - 1}c"
                            start = end
                            idx = self.text_widget.search(keyword, start, stopindex=tk.END, regexp=1)
                        else:
                            end = f"{idx}+{length.get() - 1}c"
                            self.text_widget.tag_add(category, idx, end)

                            start = end
                            idx = self.text_widget.search(keyword, start, stopindex=tk.END, regexp=1)
                    else:
                        end = f"{idx}+{length.get() - 1}c"
                        self.text_widget.tag_add(category, idx, end)

                        start = end
                        idx = self.text_widget.search(keyword, start, stopindex=tk.END, regexp=1)

        self.highlight_regex(r"(\d)+[.]?(\d)*", "number")
        self.highlight_regex(r"[\'][^\']*[\']", "string")
        self.highlight_regex(r"[\"][^\']*[\"]", "string")

    def highlight_regex(self, regex, tag):
        length = tk.IntVar()
        start = 1.0
        idx = self.text_widget.search(regex, start, stopindex=tk.END, regexp=1, count=length)
        while idx:
            end = f"{idx}+{length.get()}c"
            self.text_widget.tag_add(tag, idx, end)

            start = end
            idx = self.text_widget.search(regex, start, stopindex=tk.END, regexp=1, count=length)

    def force_highlight(self):
        self.highlight()

    def clear_highlight(self):
        for category in self.categories:
            self.text_widget.tag_remove(category, 1.0, tk.END)


if __name__ == '__main__':
    w = tk.Tk()
    h = Highlighter(tk.Text(w), 'languages/python.yaml')
    w.mainloop()



