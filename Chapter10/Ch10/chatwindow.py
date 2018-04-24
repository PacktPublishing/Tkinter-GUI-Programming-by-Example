import json
import os

import tkinter as tk
import tkinter.ttk as ttk

from listeningthread import ListeningThread
from smilieselect import SmilieSelect


class ChatWindow(tk.Toplevel):
    def __init__(self, master, friend_name, friend_username, friend_avatar, **kwargs):
        super().__init__(**kwargs)
        self.master = master
        self.title(friend_name)
        self.geometry('540x640')
        self.minsize(540, 640)

        self.friend_username = friend_username

        self.right_frame = tk.Frame(self)
        self.left_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self.left_frame)

        self.messages_area = tk.Text(self.left_frame, bg="white", fg="black", wrap=tk.WORD, width=30)
        self.scrollbar = ttk.Scrollbar(self.left_frame, orient='vertical', command=self.messages_area.yview)
        self.messages_area.configure(yscrollcommand=self.scrollbar.set)

        self.text_area = tk.Text(self.bottom_frame, bg="white", fg="black", height=3, width=30)
        self.text_area.smilies = []
        self.send_button = ttk.Button(self.bottom_frame, text="Send", command=self.send_message, style="send.TButton")

        self.smilies_image = tk.PhotoImage(file="smilies/mikulka-smile-cool.png")
        self.smilie_button = ttk.Button(self.bottom_frame, image=self.smilies_image, command=self.smilie_chooser, style="smilie.TButton")

        self.profile_picture = tk.PhotoImage(file="images/avatar.png")
        self.friend_profile_picture = tk.PhotoImage(file=friend_avatar)

        self.profile_picture_area = tk.Label(self.right_frame, image=self.profile_picture, relief=tk.RIDGE)
        self.friend_profile_picture_area = tk.Label(self.right_frame, image=self.friend_profile_picture, relief=tk.RIDGE)

        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.messages_area.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.messages_area.configure(state='disabled')

        self.right_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.profile_picture_area.pack(side=tk.BOTTOM)
        self.friend_profile_picture_area.pack(side=tk.TOP)

        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.smilie_button.pack(side=tk.LEFT, pady=5)
        self.text_area.pack(side=tk.LEFT, fill=tk.X, expand=1, pady=5)
        self.send_button.pack(side=tk.RIGHT, pady=5)

        self.configure_styles()
        self.bind_events()
        self.load_history()
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.listening_thread = None
        self.listen()

    def bind_events(self):
        self.bind("<Return>", self.send_message)
        self.text_area.bind("<Return>", self.send_message)

        self.text_area.bind('<Control-s>', self.smilie_chooser)

    def load_history(self):
        history = self.master.requester.prepare_conversation(self.master.username, self.friend_username)

        if len(history['history']):
            for message in history['history']:
                self.receive_message(message['author'], message['message'])

    def listen(self):
        self.listening_thread = ListeningThread(self, self.master.username, self.friend_username)
        self.listening_thread.start()

    def close(self):
        if hasattr(self, "listening_thread"):
            self.listening_thread.running = False
            self.after(100, self.close)
        else:
            self.destroy()


    def send_message(self, event=None):
        message = self.text_area.get(1.0, tk.END)

        if message.strip() or len(self.text_area.smilies):
            self.master.requester.send_message(
                self.master.username,
                self.friend_username,
                message,
            )

            message = "Me: " + message
            self.messages_area.configure(state='normal')
            self.messages_area.insert(tk.END, message)

            if len(self.text_area.smilies):
                last_line_no = self.messages_area.index(tk.END)
                last_line_no = str(last_line_no).split('.')[0]
                last_line_no = str(int(last_line_no) - 2)

                for index, file in self.text_area.smilies:
                    char_index = str(index).split('.')[1]
                    char_index = str(int(char_index) + 4)
                    smilile_index = last_line_no + '.' + char_index
                    self.messages_area.image_create(smilile_index, image=file)

            self.text_area.smilies = []

            self.messages_area.configure(state='disabled')

            self.text_area.delete(1.0, tk.END)

        return "break"

    def smilie_chooser(self, event=None):
        SmilieSelect(self)

    def add_smilie(self, smilie):
        smilie_index = self.text_area.index(self.text_area.image_create(tk.END, image=smilie))
        self.text_area.smilies.append((smilie_index, smilie))

    def receive_message(self, author, message):
        self.messages_area.configure(state='normal')

        if author == self.master.username:
            author = "Me"

        message_with_author = author + ": " + message

        self.messages_area.insert(tk.END, message_with_author)

        self.messages_area.configure(state='disabled')

    def configure_styles(self):
        style = ttk.Style()
        style.configure("send.TButton", background='#dddddd', foreground="black", padding=16)


if __name__ == '__main__':
    w = tk.Tk()
    c = ChatWindow(w, 'friend', 'friend', 'images/avatar.png')
    c.protocol("WM_DELETE_WINDOW", w.destroy)
    w.mainloop()
