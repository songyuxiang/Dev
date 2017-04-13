def clear(text):
    text=str(text)
    if text[0]==" ":
        text=text[1:]
    out="#"+text.replace("\n","").replace("\"","")
    return out
filename="10.1.1.1-2017.log"

with open(filename,'r') as file:
    data=file.readlines()
result={}
pos=data[0].find('#')
temp=data[0][:pos]
result[0]=clear(temp)
number=filename.split("/")[-1].split("-")[0]
result[3]=clear(number)
for i in data:
    if i.count("Copyright")>0:
        try:
            temp=i.split("by",1)[-1]
            result[1]=clear(temp)
        except IndexError:
            result[1]="#NA"
    elif i.count("snmp-server location")>0:
        temp = i.split(" ")[-1]
        result[2]=clear(temp)
    elif i.count("System image file is")>0:
        temp = i.split(":")[-1]
        result[4] = clear(temp)
    elif i.count("Model number") > 0:
        temp = i.split(":")[-1]
        result[5] = clear(temp)
    elif i.count("System serial number ") > 0 or i.count("System Serial Number ") > 0:
        temp = i.split(":")[-1]
        result[6] = clear(temp)
out=open("out.log",'w')
out.close()
out=open("out.log",'a')
for i in range(7):
    if result.get(i):
        out.write(result[i])
        out.write("\n")
    else:
        out.write("#NA")
        out.write("\n")
out.close()
