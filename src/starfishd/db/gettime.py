from datetime import datetime

class gettime:
    def __init__(self):
        self.now = datetime.now()
        
    def get(self):
        return str(self.now)
