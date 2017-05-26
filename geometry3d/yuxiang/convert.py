import numpy as np
####
###------------Convert Unity---------------###
####
class yuxiangConvert:
    def yuxiangRadian2Gradian(radian):
        gradian=radian*np.pi/200
        return gradian
    def yuxiangDegree2Gradian(degree):
        gradian=degree*10/9
        return gradian
    def yuxiangDegree2Radian(degree):
        radian=degree/180*np.pi
        return radian

    # convert coordinates from cartesian to spheric
    def yuxiangCartesian2Spheric(x, y, z):
        x = float(x)
        y = float(y)
        z = float(z)
        phi = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        omiga = np.arccos(z / phi)
        if y >= 0:
            delta = np.arccos((x / np.sqrt(x ** 2 + y ** 2)))
            return phi, omiga, delta
        else:
            delta = 2 * np.pi - np.arccos((x / np.sqrt(x ** 2 + y ** 2)))
            return phi, omiga, delta

    # convert coordinates from spheric to cartesian
    def yuxiangSpheric2Cartesian(ro, phi, theta):
        x = ro * np.sin(phi) * np.cos(theta)
        y = ro * np.sin(phi) * np.sin(theta)
        z = ro * np.cos(phi)
        return x, y, z