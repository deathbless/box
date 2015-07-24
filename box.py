import sqlite3
import os
import time
import urllib2
dbisdel = False
def deldb(dir):
    global dbisdel
    for file in os.listdir(dir):
        if os.path.isfile(file) and file == "db.sqlite3":
            os.remove(os.path.join(dir, file))
            print "del success!"
        dbisdel = True


def syncdb():
    print "download"
    global dbisdel
    a = urllib2.urlopen("http://10.180.87.93:8001/db.sqlite3")
    data = a.read()
    code = open("db.sqlite3.bak", "wb")
    code.write(data)
    dbisdel = False
    code.close()
    deldb(".")
    while dbisdel == False:
        pass
    if dbisdel == True:
        os.rename("db.sqlite3.bak", "db.sqlite3")
        dbisdel = False


def updatedb():
    print "update..."
    syncdb()

start_time = time.time()
if __name__ == "__main__":
    while True:
        now_time = time.time()
        if now_time - start_time >= 10:
            updatedb()
            start_time = now_time

