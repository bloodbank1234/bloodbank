import pymysql

def connect():
    con=pymysql.connect(host='localhost', user='root', password='root', database='bloodbank', charset='utf8')
    return con