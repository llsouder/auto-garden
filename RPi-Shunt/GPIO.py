BOARD = 1
OUT = 1
IN = 1
BCM = 1 
HIGH = 1
LOW = 0
PUD_UP = 0

def input(pin):
    print("input", pin)

def setmode(a):
   print ("set mode", a)

def setup(a, b, initial=0):
   print("setup",a)

def output(a, b):
   print("output", a)

def cleanup():
   print('clean up')

def setwarnings(flag):
   print ('False')