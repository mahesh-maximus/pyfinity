import sys
import watchdog.events
import watchdog.observers
import time
import subprocess
from threading import Thread, Lock

mutex = Lock()

class PyFinity:
    process = None
    processStarted = True

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.py', '*.txt'], ignore_directories=True, case_sensitive=False)
        
    # def on_created(self, event):
    
    # def on_modified(self, event):
    
    def on_any_event(self, event):
        colorPrint('1','31', '44', "Watchdog received an file system event - % s." % event.src_path)
        PyFinity.process.kill()
        startVulcan()

def startVulcan():
    Thread(target=runPython3Interpreter).start()

def runPython3Interpreter():
    if mutex.locked():
        colorPrint('1','31', '44', "In progress of spawning a new Python3 interpreter instance ...")
        return None

    mutex.acquire()
    try:
        colorPrint('1','31', '44', "Starting Valcan python3 interpreter ...")
        print(sys.argv[2])
        PyFinity.process = subprocess.Popen(["python3", sys.argv[2]])
        PyFinity.process.wait()
        colorPrint('1','31', '44', "Stopped Valcan! python3 interpreter ...")
    finally:
        mutex.release()

# 
# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
#
def colorPrint(style, fg, bg, msg):
    print('\x1b[{};{};{}m'.format(style, fg, bg) + msg + '\x1b[0m') 

def run():
    startVulcan()
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=sys.argv[1], recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

run()