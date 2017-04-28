from geometry3D import *




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


output=open("./result/output.csv",'w')
# output.write("id,x,y,z,heading,slope,crossfall,low_vegetation_left_nearestPointHeight,low_vegetation_left_nearestPointDistance,low_vegetation_left_highestestPointHeight,low_vegetation_left_highestestPointDistance,low_vegetation_right,medium_vegetation_left,medium_vetetaion_right,high_vegetation_left,high_vegetation_right,building_left,building_right\n")
output.write("id,x,y,z,heading,slope,crossfall,class,nearestD_left,nearestH_left,highestD_left,highestH_left,nearestD_right,nearestH_right,highestD_right,highestH_right,class,nearestD_left,nearestH_left,highestD_left,highestH_left,nearestD_right,nearestH_right,highestD_right,highestH_right,class,nearestD_left,nearestH_left,highestD_left,highestH_left,nearestD_right,nearestH_right,highestD_right,highestH_right,class,nearestD_left,nearestH_left,highestD_left,highestH_left,nearestD_right,nearestH_right,highestD_right,highestH_right\n")

rail1=yuxiangLoadPointCloud("101")
rail2=yuxiangLoadPointCloud("102")
# rail3=yuxiangLoadPointCloud("103")
# rail4=yuxiangLoadPointCloud("104")
#
vegetation_low=yuxiangLoadPointCloud("3")
#
vegetation_medium=yuxiangLoadPointCloud("4")
vegetation_high =yuxiangLoadPointCloud("5")
building=yuxiangLoadPointCloud("6")
rail1.saveToFile("test.csv")
rail1.resample(3)
print(rail1)

rail1.updateTangents()

rail1.saveToFile("./result/cloud101.csv")
middleTrack12,crossfall12=yuxiangFindMiddleTrack(rail1,rail2)
middleTrack12.updateTangents()
middleTrack12.saveToFile("./result/middle.csv")

distanceVegetationLow=yuxiangGetNearestPoints(middleTrack12,vegetation_low)
# print(distanceVegetationLow)
distanceVegetationMedium=yuxiangGetNearestPoints(middleTrack12,vegetation_medium)
distanceVegetationHigh=yuxiangGetNearestPoints(middleTrack12,vegetation_high)
distanceBuilding=yuxiangGetNearestPoints(middleTrack12,building)
#
# # vL1=PointsCloud()
# # vL2=PointsCloud()
# # vM1=PointsCloud()
# # vM2=PointsCloud()
# # vH1=PointsCloud()
# # vH2=PointsCloud()
# # b1=PointsCloud()
# # b2=PointsCloud()
out_vegLow=yuxiangExtraireNearestPointInfo(distanceVegetationLow)
out_vegMedium=yuxiangExtraireNearestPointInfo(distanceVegetationMedium)
out_vegLHigh=yuxiangExtraireNearestPointInfo(distanceVegetationHigh)
out_building=yuxiangExtraireNearestPointInfo(distanceBuilding)
# # vL1.saveToFile("result/vL1.csv")
# # vL2.saveToFile("result/vL2.csv")
# # vM1.saveToFile("result/vM1.csv")
# # vM2.saveToFile("result/vM2.csv")
# # vH1.saveToFile("result/vH1.csv")
# # vH2.saveToFile("result/vH2.csv")
# # b1.saveToFile("result/b1.csv")
# # b2.saveToFile("result/b2.csv")
# print(out_vegLHigh)
for i in range(middleTrack12.length()):
    out=""
    out+="%d,%f,%f,%f,%f,%f,%f,"%(i+1,middleTrack12[i].x,middleTrack12[i].y,middleTrack12[i].z,middleTrack12.tangent[i],middleTrack12.slope[i],crossfall12[i])
    # out+="%s,%s,%s,%s,%s,%s,%,%s"%(str(distanceVegetationLow[i][1]),str(distanceVegetationLow[i][3]),str(distanceVegetationMedium[i][1]),str(distanceVegetationMedium[i][3]),str(distanceVegetationHigh[i][1]),str(distanceVegetationHigh[i][3]),str(distanceBuilding[i][1]),str(distanceBuilding[i][3]))
    out += "3"+  ","
    out += str(out_vegLow[1][i]) + ","
    out += str(out_vegLow[2][i]) + ","
    out += str(out_vegLow[4][i]) + ","
    out += str(out_vegLow[5][i]) + ","
    out += str(out_vegLow[7][i]) + ","
    out += str(out_vegLow[8][i]) + ","
    out += str(out_vegLow[10][i]) + ","
    out += str(out_vegLow[11][i]) + ","
    out += "4" + ","
    out += str(out_vegMedium[1][i]) + ","
    out += str(out_vegMedium[2][i]) + ","
    out += str(out_vegMedium[4][i]) + ","
    out += str(out_vegMedium[5][i]) + ","
    out += str(out_vegMedium[7][i]) + ","
    out += str(out_vegMedium[8][i]) + ","
    out += str(out_vegMedium[10][i]) + ","
    out += str(out_vegMedium[11][i]) + ","
    out += "5" + ","
    out += str(out_vegLHigh[1][i]) + ","
    out += str(out_vegLHigh[2][i]) + ","
    out += str(out_vegLHigh[4][i]) + ","
    out += str(out_vegLHigh[5][i]) + ","
    out += str(out_vegLHigh[7][i]) + ","
    out += str(out_vegLHigh[8][i]) + ","
    out += str(out_vegLHigh[10][i]) + ","
    out += str(out_vegLHigh[11][i]) + ","
    out += "6" + ","
    out += str(out_building[1][i]) + ","
    out += str(out_building[2][i]) + ","
    out += str(out_building[4][i]) + ","
    out += str(out_building[5][i]) + ","
    out += str(out_building[7][i]) + ","
    out += str(out_building[8][i]) + ","
    out += str(out_building[10][i]) + ","
    out += str(out_building[11][i]) + "\n"
#
    output.write(out)
output.close()