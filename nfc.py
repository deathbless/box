import os
import binascii
import time
import sqlite3
import urllib2
import urllib
import win32file
import win32con
import easygui
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
marked = []
allbox = {}
ordertobox = {}
isset = []

def init():
    global start_time
    global allbox
    start_time = time.time()
    for i in range(0, 100):
        allbox[i] = 0
    print "start"

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
        dbisdel = True

def syncdb(url):
    urllib.urlretrieve(url, "db.sqlite3")
    dbisdel = False

def updatedb():
    deldb(".")
    while dbisdel == False:
        pass
    if dbisdel == True:
        syncdb("http://10.180.95.217:8001/db.sqlite3")

def savebox(orderid):
    global marked
    global allbox
    global ordertobox
    if orderid in ordertobox:
        return
    for i in allbox:
        if allbox[i] == False:
            ordertobox[orderid] = i
            allbox[i] = True
            url = "http://10.180.95.217:8000/openshop/set?box_id=%d&order_id=%d"%(i,orderid)
            urllib2.urlopen(url)
            marked.append(orderid)
            break

def delbox(orderid):
    global allbox
    global ordertobox
    allbox[ordertobox[orderid]] = True

def query(filename):
    global marked
    global allbox
    global isset
    print filename
    cardid = filename.split(' ')[1]
    cx = sqlite3.connect("./db.sqlite3")
    cu = cx.cursor()
    orderall = cu.execute("SELECT * FROM openshop_order").fetchall()
    for order in orderall:
        orderid = order[0]
        seller = order[1]
        is_set = order[3]
        is_complete = order[5]
        nfc_buy = order[-1]
        nfc_sell = order[-2]
        type = ""
        if is_complete == False:
            if nfc_buy == cardid:
                type = "buy"
            if nfc_sell == cardid:
                type = "sell"
        elif orderid in marked:
            delbox(orderid)

        if type == "buy" and is_set == False and orderid not in marked:
            easygui.msgbox(msg="尊敬的买家(卡号%s)，您订单号为%d(卖家姓名为%s)的商品暂时还未收录！"%(cardid,orderid,seller),title = "中转箱")
        if type == "buy" and ((is_set == True and orderid in ordertobox > 0) or orderid in marked):
            easygui.msgbox(msg="尊敬的买家(卡号%s)，您订单号为%d(卖家姓名为%s)的商品在第%d号箱子里！"%(cardid,orderid,seller,ordertobox [orderid]), title="中转箱")
        if type == "sell":
            easygui.msgbox(msg="尊敬的卖家(卡号%s)，请放入您订单号为%d(卖家姓名为%s)的商品！"%(cardid,orderid,seller),title="中转箱")
            savebox(orderid)


if __name__ == "__main__":
    flag = False
    init()
    while True:
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
        continue




