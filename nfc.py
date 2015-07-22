import os
import binascii
import logging
import time
import sqlite3
import urllib2
import urllib
import win32file
import win32con

ACTIONS = {
  1 : "Created",
  2 : "Deleted",
  3 : "Updated",
  4 : "Renamed from something",
  5 : "Renamed to something"
}

FILE_LIST_DIRECTORY = win32con.GENERIC_READ | win32con.GENERIC_WRITE
path_to_watch = "d:/"
hDir = win32file.CreateFile (
  path_to_watch,
  FILE_LIST_DIRECTORY,
  win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
  None,
  win32con.OPEN_EXISTING,
  win32con.FILE_FLAG_BACKUP_SEMANTICS,
  None
)

dumps = []
dbisdel = False
start_time = 0

def init():
    global start_time
    start_time = time.time()

def readindata(filename):
    f = open(filename, 'rb')
    a = f.read()
    print binascii.b2a_hex(a)

def deldb(dir):
    global dbisdel
    for file in os.listdir(dir):
        targetFile = os.path.join(dir,file)
        if os.path.isfile(targetFile) and file == "db.sqlite3":
            os.remove(targetFile)

def syncdb(url):
    urllib.urlretrieve(url, "db.sqlite3")

def database():
    cx = sqlite3.connect("./db.sqlite3")
    cu = cx.cursor()
    order = cu.execute("SELECT * FROM openshop_order").fetchall()


def updatedb():


def query(filename):
    print filename

if __name__ == "__main__":
    flag = False
    init()
    while True:
        now_time = time.time()
        if now_time - start_time >= 10:
            updatedb()
            now_time = 0
        results = win32file.ReadDirectoryChangesW (
                                       hDir,  #handle: Handle to the directory to be monitored. This directory must be opened with the FILE_LIST_DIRECTORY access right.
                                       1024,  #size: Size of the buffer to allocate for the results.
                                       True,  #bWatchSubtree: Specifies whether the ReadDirectoryChangesW function will monitor the directory or the directory tree.
                                       win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                                        win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                                        win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                                        win32con.FILE_NOTIFY_CHANGE_SIZE |
                                        win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                                        win32con.FILE_NOTIFY_CHANGE_SECURITY,
                                       None,
                                       None)
        for action, file in results:
            filename = os.path.join(path_to_watch, file)
            if ACTIONS.get(action, "Unknown") == "Created":
                dumps.append(filename)
                flag = True
            elif ACTIONS.get(action, "Unknown") == "Updated":
                while flag == False:
                    pass
                if filename in dumps:
                    query(filename)
                flag = False






