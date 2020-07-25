import threading

def p():
    print('hello')

timer = threading.Timer(3,p)
timer.start()