import base64
import os
from PIL import Image
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

avatar_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "images/avatar.png"))


class AvatarWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__()

        self.master = master
        self.transient(master)

        self.title("Change Avatar")
        self.geometry("350x200")

        self.image_file_types = [
            ("Png Images", ("*.png", "*.PNG")),
        ]

        self.current_avatar_image = tk.PhotoImage(file=avatar_file_path)

        self.current_avatar = ttk.Label(self, image=self.current_avatar_image)
        choose_file_button = ttk.Button(self, text="Choose File", command=self.choose_image)

        self.current_avatar.pack()
        choose_file_button.pack()

    def choose_image(self):
        image_file = filedialog.askopenfilename(filetypes=self.image_file_types)

        if image_file:
            avatar = Image.open(image_file)
            avatar.thumbnail((128, 128))
            avatar.save(avatar_file_path, "PNG")

            img_contents = ""
            img_b64 = ""
            with open(avatar_file_path, "rb") as img:
                img_contents = img.read()
                img_b64 = base64.urlsafe_b64encode(img_contents)

            self.master.requester.update_avatar(self.master.username, img_b64)

            self.current_avatar_image = tk.PhotoImage(file=avatar_file_path)
            self.current_avatar.configure(image=self.current_avatar_image)


if __name__ == "__main__":
    win = tk.Tk()
    aw = AvatarWindow(win)
    win.mainloop()