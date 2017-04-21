import pyproj
p1 = pyproj.Proj(init='epsg:26915')
p2 = pyproj.Proj(init='epsg:26715')
x1, y1 = p1(-92.199881,38.56694)
x2, y2 = pyproj.transform(p1,p2,x1,y1)
print (x2,y2 )
print(p2(x2,y2,inverse=True))

lats = (38.83,39.32,38.75)
lons = (-92.22,-94.72,-90.37)
x1, y1 = p1(lons,lats)
x2, y2 = pyproj.transform(p1,p2,x1,y1)
print(x2,y2)
xy=x1+y1
print(xy)

def Lambert93ToWGS84(x1,y1,z1=None):
    p1=pyproj.Proj(init='epsg:2154')
    p2=pyproj.Proj(init='epsg:4326')
    z2=None
    if z1==None:
        x2,y2=pyproj.transform(p1,p2,x1,y1)
    else:
        x2, y2,z2 = pyproj.transform(p1, p2, x1, y1,z2)
    return x2,y2,z2
x2,y2,_=Lambert93ToWGS84(1525240.99,6246398.33)
print(x2,y2)