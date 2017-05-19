from geometry3D import *

def yuxiangLimitDecimal(number,decimalnumber=2):
    number=str(number)
    out="None"
    if number!='None':
        pos=number.find('.')
        if pos<0:
            number=number+".00"
        elif len(number)-pos<2:
            number=number+"0"
        try:
            out=number[:pos+3]
        except:
            out=number
    return out
def yuxiangExtraireNearestPointInfo(out):
    nearestPt1=[]
    nearestPt2=[]
    nearestD1=[]
    nearestD2=[]
    nearestH1=[]
    nearestH2=[]
    highestPt1=[]
    highestPt2=[]
    highestD1=[]
    highestD2=[]
    highestH1=[]
    highestH2=[]

    for i in out:
        nearestPt1.append(i[0])
        nearestD1.append(i[1])
        nearestH1.append(i[2])
        highestPt1.append(i[3])
        highestD1.append(i[4])
        highestH1.append(i[5])
        nearestPt2.append(i[6])
        nearestD2.append(i[7])
        nearestH2.append(i[8])
        highestPt2.append(i[9])
        highestD2.append(i[10])
        highestH2.append(i[11])
    return nearestPt1, nearestD1, nearestH1,highestPt1, highestD1, highestH1, nearestPt2, nearestD2, nearestH2, highestPt2, highestD2, highestH2






def mainThales(dataPath="data.csv",outputPath="./result/output3.csv",leftRailClass="101",rightRailClass="102",clockwiseRailDirection=False):
    output = open(outputPath, 'w')
    # output.write("id,x,y,z,heading,slope,crossfall,low_vegetation_left_nearestPointHeight,low_vegetation_left_nearestPointDistance,low_vegetation_left_highestestPointHeight,low_vegetation_left_highestestPointDistance,low_vegetation_right,medium_vegetation_left,medium_vetetaion_right,high_vegetation_left,high_vegetation_right,building_left,building_right\n")
    output.write(
        "id,lon(rad),lat(rad),elevation(m),cap(rad),slope,crossfall,hasBridge,hasSwitch,hasTermination,class,nearestD_left,nearestH_left,highestD_left,highestH_left,nearestD_right,nearestH_right,highestD_right,highestH_right,class,nearestD_left,nearestH_left,highestD_left,highestH_left,nearestD_right,nearestH_right,highestD_right,highestH_right,class,nearestD_left,nearestH_left,highestD_left,highestH_left,nearestD_right,nearestH_right,highestD_right,highestH_right,class,nearestD_left,nearestH_left,highestD_left,highestH_left,nearestD_right,nearestH_right,highestD_right,highestH_right\n")

    rail1 = yuxiangLoadPointCloud(leftRailClass)
    rail2 = yuxiangLoadPointCloud(rightRailClass)
    # rail3=yuxiangLoadPointCloud("103")
    # rail4=yuxiangLoadPointCloud("104")
    #
    vegetation_low = yuxiangLoadPointCloud("3",dataPath)
    #
    vegetation_medium = yuxiangLoadPointCloud("4",dataPath)
    vegetation_high = yuxiangLoadPointCloud("5",dataPath)
    building = yuxiangLoadPointCloud("6",dataPath)
    bridge = yuxiangLoadPointCloud("601",dataPath)
    rail1.resample(3)
    rail1.sort(clockwiseRailDirection)
    rail1.updateTangents()

    middleTrack12, crossfall12 = yuxiangFindMiddleTrack(rail1, rail2)
    middleTrack12.sort(clockwiseRailDirection)
    middleTrack12.updateTangents()
    middleTrack12.saveToFile("./result/middle.csv")
    distanceVegetationLow = yuxiangGetNearestPoints(middleTrack12, vegetation_low)
    distanceVegetationMedium = yuxiangGetNearestPoints(middleTrack12, vegetation_medium)
    distanceVegetationHigh = yuxiangGetNearestPoints(middleTrack12, vegetation_high)
    distanceBuilding = yuxiangGetNearestPoints(middleTrack12, building)
    out_vegLow = yuxiangExtraireNearestPointInfo(distanceVegetationLow)
    out_vegMedium = yuxiangExtraireNearestPointInfo(distanceVegetationMedium)
    out_vegLHigh = yuxiangExtraireNearestPointInfo(distanceVegetationHigh)
    out_building = yuxiangExtraireNearestPointInfo(distanceBuilding)

    for i in range(middleTrack12.length()):
        out = ""
        lon, lat, elev = yuxiangProjection.yuxiangCC2WGS84(middleTrack12[i].x, middleTrack12[i].y, middleTrack12[i].z,
                                                           '48')
        lon = yuxiangConvert.yuxiangDegree2Radian(lon)
        lat = yuxiangConvert.yuxiangDegree2Radian(lat)
        # out += "%d,%f,%f,%f,%f,%f,%f," % (
        # i + 1, middleTrack12[i].x,middleTrack12[i].y,middleTrack12[i].z, middleTrack12.tangent[i], middleTrack12.slope[i], crossfall12[i])
        out += "%d,%.16f,%.16f,%f,%.16f,%f,%f," % (
        i + 1, lon, lat, elev, middleTrack12.cap[i], middleTrack12.slope[i], -crossfall12[i])
        if yuxiangPointCloudOverlap(middleTrack12.data[i], bridge):
            out += "true" + ","
        else:
            out += "false" + ","
        out += "false" + ","  # has switch
        out += "false" + ","  # has termination
        out += "3" + ","
        out += yuxiangLimitDecimal(out_vegLow[1][i]) + ","
        out += yuxiangLimitDecimal(out_vegLow[2][i]) + ","
        out += yuxiangLimitDecimal(out_vegLow[4][i]) + ","
        out += yuxiangLimitDecimal(out_vegLow[5][i]) + ","
        out += yuxiangLimitDecimal(out_vegLow[7][i]) + ","
        out += yuxiangLimitDecimal(out_vegLow[8][i]) + ","
        out += yuxiangLimitDecimal(out_vegLow[10][i]) + ","
        out += yuxiangLimitDecimal(out_vegLow[11][i]) + ","
        out += "4" + ","
        out += yuxiangLimitDecimal(out_vegMedium[1][i]) + ","
        out += yuxiangLimitDecimal(out_vegMedium[2][i]) + ","
        out += yuxiangLimitDecimal(out_vegMedium[4][i]) + ","
        out += yuxiangLimitDecimal(out_vegMedium[5][i]) + ","
        out += yuxiangLimitDecimal(out_vegMedium[7][i]) + ","
        out += yuxiangLimitDecimal(out_vegMedium[8][i]) + ","
        out += yuxiangLimitDecimal(out_vegMedium[10][i]) + ","
        out += yuxiangLimitDecimal(out_vegMedium[11][i]) + ","
        out += "5" + ","
        out += yuxiangLimitDecimal(out_vegLHigh[1][i]) + ","
        out += yuxiangLimitDecimal(out_vegLHigh[2][i]) + ","
        out += yuxiangLimitDecimal(out_vegLHigh[4][i]) + ","
        out += yuxiangLimitDecimal(out_vegLHigh[5][i]) + ","
        out += yuxiangLimitDecimal(out_vegLHigh[7][i]) + ","
        out += yuxiangLimitDecimal(out_vegLHigh[8][i]) + ","
        out += yuxiangLimitDecimal(out_vegLHigh[10][i]) + ","
        out += yuxiangLimitDecimal(out_vegLHigh[11][i]) + ","
        out += "6" + ","
        out += yuxiangLimitDecimal(out_building[1][i]) + ","
        out += yuxiangLimitDecimal(out_building[2][i]) + ","
        out += yuxiangLimitDecimal(out_building[4][i]) + ","
        out += yuxiangLimitDecimal(out_building[5][i]) + ","
        out += yuxiangLimitDecimal(out_building[7][i]) + ","
        out += yuxiangLimitDecimal(out_building[8][i]) + ","
        out += yuxiangLimitDecimal(out_building[10][i]) + ","
        out += yuxiangLimitDecimal(out_building[11][i]) + "\n"
        # out += str(out_building[11][i]) + "\n"

        out = out.replace("None", "NaN")

        #
        output.write(out)
    output.close()

mainThales()