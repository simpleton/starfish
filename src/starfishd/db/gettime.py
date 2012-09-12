import time
import socket
class gettime:
    def __init__(self):
        self.now = time.time()
        
    def get(self):
        return str(int(self.now))

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("www.soso.com",80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    
if __name__ == '__main__':
    print gettime().get_ip()
