import threading
from threading import Thread
from django.conf import settings

from django.core.mail import EmailMessage

class EmailThread(threading.Thread):
    def __init__(self, msg):
        self.msg = msg
        threading.Thread.__init__(self)

    def run(self):
        self.msg.send()
