import tkinter as tk
import time
import threading


class WorkThread(threading.Thread):
    def run(self):
        label.configure(text="Doing work")
        time.sleep(5)
        label.configure(text="Finished")

        return


win = tk.Tk()
win.geometry("200x150")

counter = tk.IntVar()
label = tk.Label(win, text="Ready to Work")
counter_label = tk.Label(win, textvar=counter)


def increase_counter():
    counter.set(counter.get() + 1)


def work():
    thread = WorkThread()
    thread.start()


counter_button = tk.Button(win, text="Increase Counter", command=increase_counter)
work_button = tk.Button(win, text="Work", command=work)

label.pack()
counter_label.pack()

counter_button.pack()
work_button.pack()

win.mainloop()