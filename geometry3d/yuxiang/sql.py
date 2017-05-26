import MySQLdb as mdb
import sys
def yuxiangConnectMySql(host='localhost',username='ysong',userpassword='ysong',db='jg'):
    try:
        con = mdb.connect(host,username,userpassword,db)
        return con
    except:
        print("error:can't connect to database")

def yuxiangCreateTalbe(connection,tablename,headerList=[],typeList=[],optionList=[]):
    cur = connection.cursor()
    cur.execute("DROP TABLE IF EXISTS %s"%tablename)
    temp="CREATE TABLE Writers("
    size=len(headerList)
    for i in range(size):
        temp+=headerList[i]
        try:
            temp+=" "+typeList[i]
        except IndexError:
            temp+=" "+"VARCHAR(25)"
        try:
            temp+=" "+optionList[i]
        except IndexError:
            print("no optioin")
        if i!=size-1:
            temp+=","
    temp+=")"
    cur.execute(temp)


def yuxiangAppendData(connection,table,colName,value):
    cur = connection.cursor()
    temp="INSERT INTO %s(%s) VALUES(\'%s\')"%(table,colName,value)
    cur.execute(temp)
    cur.execute("SELECT * FROM Writers")
    rows = cur.fetchall()
    print(rows)