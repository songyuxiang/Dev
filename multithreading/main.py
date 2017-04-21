import threading
import time
class myThread(threading.Thread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.name=name
        self.counter=counter
    def run(self):
        threading.Lock().acquire()
        self.method()
        threading.Lock().release()

    def method(self):
        for i in range(10000):
            print("do somethings"+self.name)
            time.sleep(1)
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)
thread1.start()
thread2.start()
thread1.join()
thread2.join()