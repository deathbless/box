import sys
import time
import logging
import imp
import re
from watchdog.observers import Observer
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler



class CreatedEventHandler(FileSystemEventHandler):
 
    def __init__(self):
        FileSystemEventHandler.__init__(self)
 
 
    def on_created(handler,event):
        file_name = event.src_path[2:]
        print '--'+file_name
 
        moduleName = ''
        for key in parse_map.keys():
            if(re.match(key,file_name)):
                moduleName = parse_map[key]
                break
        if(moduleName != ''):
            try:
                parseModule =  imp.load_module(moduleName,*imp.find_module(moduleName,['./scripts/']))
                print '  load module: ' + moduleName
                parseModule.parse(file_name)
            except Exception,e:
                print e
 

parse_map={
            '^test.xlsx$':'test',
            '^emt_finance.*\.xlsx':'emt_finance'
}
 
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = CreatedEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print 'Watching...'
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()