import time

class gettime:
    def __init__(self):
        self.now = time.time()
        
    def get(self):
        return str(int(self.now))
