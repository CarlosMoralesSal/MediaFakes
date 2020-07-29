import cv2,os
import numpy as np
from PIL import ImageChops
import PIL.Image
from PIL.ExifTags import TAGS

    
def level2(imageTesting,path):

    elareturns=[]
    for k in range(3):
        elareturns.append(0)
    print("En ELA")
    print("Doing ELA  analysis....Please wait for a minute")

    TEMP = path+'/temp.jpg'
    SCALE = 10
   
    try:
        original = PIL.Image.open(imageTesting);
        original.save(TEMP, quality=90)
        temporary = PIL.Image.open(TEMP)
        diff = ImageChops.difference(original, temporary)
        d = diff.load()
        WIDTH, HEIGHT = diff.size
        for x in range(WIDTH):
                for y in range(HEIGHT):
                        d[x, y] = tuple(k * SCALE for k in d[x, y])
    
        diff.save(path+"/img.jpg")
        
        print("Doing Histogram Analysis....")
   
        rec = cv2.face.LBPHFaceRecognizer_create()
        rec.read("TrainedDataFolder\TraningData.yml") 
        imggray = PIL.Image.open(path+"/img.jpg").convert('L') 
        print(imggray)
        gray = np.array(imggray,'uint8')
        print(gray)
        
        print("\nResult:")
        id,conf = rec.predict(gray) 
        print(id,conf)
        if(id == 2):
                
                print("\nREAL")
                
                print(str(100-conf))
                elareturns[0]=str(100-conf)
                elareturns[1]=0
        else:
                
                print("\nFAKE")
                
                print(str(100 -conf ))
                elareturns[0]=str(100-conf)
                elareturns[1]=1
       

    except Exception as e:
        print("\nFailed to Load Image: "+str(e))
        return elareturns
    try:
        f=1
        
        img = PIL.Image.open(imageTesting)
        info = img._getexif()
        print(info)
        if info:
            for (tag, value) in info.items():
                if "Software" == TAGS.get(tag, tag):

                        print("\Fake Image")
                        print("\nFound Software Signature: "+value)
                        elareturns[2]=value
                        f=0
    
        if f:
           
            print("\nNo Software Signature Found")
            print("\nLooks like Real")
            elareturns[2]="1"
        
        return elareturns          
    except Exception as e:

        print("\nFailed to Load Metadata: "+str(e))
    
