import sqlite3

def init():
    cx = sqlite3.connect("./db.sqlite3")
    cu = cx.cursor()
    # cu.execute('CREATE TABLE foo (o_id INTEGER PRIMARY KEY, fruit VARCHAR(20), veges VARCHAR(30))')
    print cu.execute("select * from openshop_order").fetchall()
    # print cu.execute("select name from sqlite_master where type='table' order by name").fetchall()


init()