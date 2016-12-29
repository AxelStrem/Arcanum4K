import os
import subprocess
from shutil import copyfile

for root, dirs, files in os.walk('bmps_in/wall'):
    for name in dirs:
        dirname = str('x15_art')+os.path.join(root[7:],name)
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        dirname2 = str('x30_art')+os.path.join(root[7:],name)
        if not os.path.isdir(dirname2):
            os.mkdir(dirname2)
    for name in files:
        if name[-3:].upper()=='INI' and name[:7].upper()!='DESKTOP':
            print(str("converting ")+os.path.join(root[7:],name[:-4]))
            dstname1 = str('x15_art')+os.path.join(root[7:],name[:-4])+'.art'
            dstname2 = str('x30_art')+os.path.join(root[7:],name[:-4])+'.art'
            origname = os.path.join(root,name)
            srcname1 = str('x15_out')+os.path.join(root[7:],name)
            copyfile(origname,srcname1)
            srcname2 = str('x30_out')+os.path.join(root[7:],name)
            copyfile(origname,srcname2)
            subprocess.call(["ArtConverter.exe",srcname1,dstname1])
            subprocess.call(["ArtConverter.exe",srcname2,dstname2])
