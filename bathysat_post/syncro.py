import yuxiangDataArray
def getSecond(time):
    h,m,s=time.split(':')
    return float(h)*60*60+float(m)*60+float(s)

def resampleData(gpsStart,gpsEnd,gpsData,bathyStart,bathyEnd,bathyData,gap):
    gpsNewData=[]
    bathyNewData=[]
    gps_bathy=[]
    for i in gpsData:
        if float(i[2])>=float(gpsStart) and float(i[2])<=float(gpsEnd):
            gpsNewData.append(i)
    for i in bathyData:
        if float(i[1])>=float(bathyStart) and float(i[1])<=float(bathyEnd):
            i[1]=float(i[1]-gap)
            bathyNewData.append(i)
    for i in gpsNewData:
        for j in bathyNewData:
            if float(i[2])==float(j[1]) and float(j[2])!=0:
                gps_bathy.append([i[0],i[2],i[3],i[4],i[5],j[2]])
    print(gpsNewData)
    print(bathyNewData)
    print(gps_bathy)
    return gps_bathy
def save(list,filename):
    file=open(filename,'w')
    for i in list:
        for j in i:
            file.write(str(j)+';')
        file.write('\n')

bathy=open("bathy2.txt",'r')
gps=open("gps2.txt",'r')
bathy=bathy.readlines()
bathy_elements=[]
for i in bathy:
    bahty_element=i.split('|') [:-1]

    if len(bahty_element)==6:
        bahty_element[1] = getSecond(bahty_element[1])
        bathy_elements.append(bahty_element)


gps=gps.readlines()
gps_elements=[]
for i in gps:
    gps_element=i.split('|') [:-1]

    if len(gps_element)==6:
        gps_element[2] = getSecond(gps_element[2])
        gps_elements.append(gps_element)


gps_bathy1=resampleData(getSecond("10:44:06"),getSecond("11:07:10"),gps_elements,getSecond("12:27:40"),getSecond("12:50:40"),bathy_elements,getSecond("1:43:30"))
save(gps_bathy1,"gps_bathy2")

