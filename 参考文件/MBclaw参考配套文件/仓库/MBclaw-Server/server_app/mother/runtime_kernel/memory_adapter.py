class MemoryAdapter:

    def __init__(self):

        self.store = []

    def write(self, record):

        self.store.append(record)

    def query(self):

        return self.store[-20:]
