import pymysql
import sqlite3

def connect():
    #con=pymysql.connect(host='localhost', user='root', password='root', database='bloodbank', charset='utf8')
    con = sqlite3.connect("BloodBank.db")
    return con
