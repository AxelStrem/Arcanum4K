import os
import subprocess
from PIL import Image
import numpy as np

for root, dirs, files in os.walk('bmps_in'):
    for name in dirs:
        dirname = os.path.join('bmps_preprocessed',root[8:],name)
        borname = os.path.join('borders_in',root[8:],name)
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        if not os.path.isdir(borname):
            os.mkdir(borname)
    for name in files:
        if name[-3:].upper()=='BMP':
            print (str("preprocessing ")+os.path.join(root[8:],name[:-4]))
            dstname = os.path.join('bmps_preprocessed',root[8:],name)
            brdname = os.path.join('borders_in',root[8:],name)
            srcname = os.path.join(root,name)
            #subprocess.call(["ArtConverter.exe",srcname,dstname])
            img = Image.open(srcname)
            palette = img.getpalette()
            if palette!=None:
                subprocess.call(["BMPFace.exe",srcname,dstname])
                alpha = palette[0:3]
                palette[0:3] = (0,0,0)
                #img.putpalette(palette)
                #img.save(dstname)
                palette[3:(256*3)] = (255,255,255)*255
                img.putpalette(palette)
                img.save(brdname)
            else:
                img.save(dstname)