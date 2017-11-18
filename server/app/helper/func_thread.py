import threading

class FuncThread(threading.Thread):
    def __init__(self, target):
        threading.Thread.__init__(self)
        self._target = target

    def run(self):
        self._target()