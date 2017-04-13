from PyQt5.Qt import *
ba=QByteArray(1,"t")
ba.append(QByteArray(2,"e"))
data=""
for i in ba:
    data+=i
file=open("test.txt",'a')
file.write(data)
file.close()
print(data)
print(ba.data())