import os

def yuxiangGetFiles(root,isFile=True,keyword=None):
    if root[-1]!="/":
        root=root+"/"
    dirList = os.listdir(root)
    out = []
    for i in dirList:
        if isFile==True :
            if os.path.isfile(root + i):
                if keyword!=None:
                    if i.find(keyword):
                        out.append(root+i)
                else:
                    out.append(root + i)
        else:
            if os.path.isdir(root + i):
                if keyword!=None:
                    if i.find(keyword):
                        out.append(i)
                else:
                    out.append(root + i)
    return out