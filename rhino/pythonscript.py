pt = rs.AddPoint(x,y,z)
if not rs.IsLayer("Test"):
    rs.AddLayer("Test")
rs.ObjectLayer(pt,"Test")