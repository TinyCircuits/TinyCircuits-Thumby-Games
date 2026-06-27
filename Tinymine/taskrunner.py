from time import sleep
from sys import print_exception
from _thread import start_new_thread

inEmulator = False
try:
    import emulator
    inEmulator = True
except ImportError:
    pass

threadTasks = []
crashlogdir = ''

def logException( x ):
    if inEmulator:
        print_exception( x )
    else:
        if crashlogdir:
            with open( crashlogdir + '/taskrunnercrash.log', 'w', encoding="utf-8" ) as f:
                print_exception( x, f )

def taskRunner():
    try:
        i = 0;
        while True:
            if len( threadTasks ) > i:
                task = threadTasks[ i ]
                threadTasks[ i ] = None
                task()
                i = i + 1
            else:
                sleep( 1 )
    except Exception as x:
        logException( x )

def addTask( task ):
    if inEmulator:
        task()
    else:
        threadTasks.append( task )

def startTaskRunner( dir ):
    global crashlogdir
    if dir:
        crashlogdir = dir
    try:
        if inEmulator:
            print( "Emulator detected - tasks will execute on the main thread." )
            return False
        else:
            start_new_thread( taskRunner, () )
            return True
    except Exception as x:
        logException( x )
        return False
