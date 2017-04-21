from geometry3D import *



p1=Point3D(1,2,3)
p2=Point3D(2,3,4)
p3=Point3D(3,4,4)
pointcloud=PointsCloud([p1,p2,p3])
line=Line3D(Point3D(2,2,2),Point3D(3,6,8))
plane=Plane3D()
plane.pointFitting(pointcloud)

vector=line.toVector()
print(vector)
print(plane.normal)
result=yuxiangAxeMirror(vector,plane.normal)
print(result)
result2=yuxiangAxeMirror(result,plane.normal)
print(result2)
fig=plt.figure()
ax=fig.gca(projection='3d')
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)
ax.plot(x, y, z)
# ax.legend()

plt.show()