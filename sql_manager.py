import threading


class SqlManager:
    def __init__(self, db):
        self.mutex = threading.Lock()
        self.db = db
