import pyproj
####
###------------Projection---------------###
####
def yuxiangCC2WGS84(x1,y1,z1,zone):
        wgs = pyproj.Proj(init='epsg:4326')
        cc = pyproj.Proj(init="epsg:39%s" % (str(zone)))
        lon, lat, elevation = pyproj.transform(cc, wgs, x1,y1,z1)
        return lon, lat, elevation