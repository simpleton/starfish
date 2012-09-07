class channel:
    def __init__(self, classify='cctv'):
        
        cctv = ['cctv1', 'cctv2', 'cctv3', 'cctv4', 'cctveurope',  \
                'cctvamericas', 'cctv5', 'cctv6', 'cctv7', 'cctv8' ,\
                'cctv9d', 'CCTV9ducumentary', 'cctv10', 'cctv11', 'cctv12' \
                'cctvchildren', 'cctvmusic', 'cctv9']
                     
        if (classify == 'cctv'):
            self.program_list = cctv
        self.index = -1
        
    def next(self):
        self.index += 1
        if (self.index == len(self.program_list)):
            raise StopIteration
        return self.program_list[self.index]
    
    def __iter__(self):
        return self

if __name__ == '__main__':
    ch = channel()
    for elem in ch:
        print 'test',elem
