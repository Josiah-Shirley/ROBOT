import time
import _thread, threading

class ThreadExample:
    
    def __init__(self):
        self.count = 100
        self.message = "0"

    def firstThread(self):
        for i in range(self.count):
            print("##" + str(i))
            if(i > 75):
                self.message = "######   I am over 75"

    def mainThread(self):
        for j in range(self.count):
            print("$$" + str(j))
            time.sleep(.02)
            if(self.message != "0"):
                print(self.message)
           
    def secondThread(self):
        for k in range(self.count):
            print("**" + str(k))
             
    def timedFunction(self):
        print("                1 seconds is up")


        
inst = ThreadExample()

t = threading.Timer(1.0, inst.timedFunction)
t.start()
##inst.firstThread()
##inst.secondThread()
try:
    _thread.start_new_thread(inst.firstThread,())
except:
   print ("Error: unable to start thread")
try:
    _thread.start_new_thread(inst.secondThread,())
except:
   print ("Error: unable to start thread")
inst.mainThread()
print("We are done")

