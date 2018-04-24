import arrow
import threading
import time

from requester import Requester


class ListeningThread(threading.Thread):
    def __init__(self, master, user_one, user_two):
        super().__init__()
        self.master = master
        self.user_one = user_one
        self.user_two = user_two
        self.requester = Requester()
        self.running = True
        self.last_checked_time = arrow.now().timestamp

    def run(self):
        while self.running:
            new_messages = self.requester.get_new_messages(self.last_checked_time, self.user_one, self.user_two)
            self.last_checked_time = arrow.now().timestamp
            for message in new_messages['messages']:
                self.master.receive_message(message["author"], message["message"])

            time.sleep(3)

        del self.master.listening_thread

        return
