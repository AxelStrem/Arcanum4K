import os
import subprocess
from PIL import Image
import numpy as np

def quantizetopalette(silf, palette, dither=False):
    """Convert an RGB or L mode image to use a given P image's palette."""

    silf.load()

    # use palette from reference image
    palette.load()
    if palette.mode != "P":
        raise ValueError("bad mode for palette image")
    if silf.mode != "RGB" and silf.mode != "L":
        raise ValueError(
            "only RGB or L mode images can be quantized to a palette"
            )
    im = silf.im.convert("P", 1 if dither else 0, palette.im)
    # the 0 above means turn OFF dithering
    return silf._makeself(im)


for root, dirs, files in os.walk('bmps_out'):
    for name in dirs:
        dirname = str('x30_out/')+os.path.join(root[9:],name)
        dirname2 = str('x15_out/')+os.path.join(root[9:],name)
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        if not os.path.isdir(dirname2):
            os.mkdir(dirname2)
    for name in files:
        if name[-3:].upper()=='BMP':
            print (str("applying alpha: ")+os.path.join(root[9:],name[:-4]))
            dstname = str('x30_out/')+os.path.join(root[9:],name)
            dstname2 = str('x15_out/')+os.path.join(root[9:],name)
            brdname = str('border_out/')+os.path.join(root[9:],name)
            origname = str('bmps_in/')+os.path.join(root[9:],name)
            srcname = os.path.join(root,name)
            #subprocess.call(["ArtConverter.exe",srcname,dstname])
            img = Image.open(srcname)
            if img.size[0]<=3 or img.size[1]<=3:
                continue
            smallsize = ((img.size[0] + 1)//2, (img.size[1] + 1)//2)
            img2 = img.resize(smallsize, Image.ANTIALIAS)
            orig = Image.open(origname)
            palette = orig.getpalette()
            if palette!=None:
                img.save(dstname)
                img2.save(dstname2)
                
                subprocess.call(["Quantizer.exe",origname,dstname])
                subprocess.call(["Quantizer.exe",origname,dstname2])
                
                alpha  = palette[0:3]
                border = Image.open(brdname)
                img = Image.open(dstname)
                pix = np.array(img,dtype='uint8')
                apix = np.array(border,dtype='uint8')
                pix.flags.writeable=True
                pix[apix==0]=0
                img = Image.fromarray( np.asarray( np.clip(pix,0,255), dtype="uint8"), "P" )
                
                img2 = Image.open(dstname2)
                pix = np.array(img2,dtype='uint8')
                border = border.resize(smallsize, Image.NEAREST)
                apix = np.array(border,dtype='uint8')
                pix.flags.writeable=True
                pix[apix==0]=0
                img2 = Image.fromarray( np.asarray( np.clip(pix,0,255), dtype="uint8"), "P" )
                
                img.putpalette(palette)
                img.save(dstname)

                img2.putpalette(palette)
                img2.save(dstname2)
            else:
                img.save(dstname)
                img2.save(dstname2)
