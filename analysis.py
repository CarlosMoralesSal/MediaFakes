import cv2,os
import numpy as np
from PIL import ImageChops
import PIL.Image
from PIL.ExifTags import TAGS

    
def level2(imageTesting,path):
    #window.title("Level 2 Testing")
    elareturns=[]
    for k in range(3):
        elareturns.append(0)
    print("En ELA")
    print("Doing ELA  analysis....Please wait for a minute")
    #lab['text'] = "Doing ELA analysis ... Please wait for a minute"
    #window.update_idletasks()
    TEMP = path+'/temp.jpg'
    SCALE = 10
    #original = PIL.Image.open(r"C:\Users\Carlos\Desktop\TFM\MediaFakes\tana_vox\downloadsimages20200704-140651\BSC_104_Unit_00379R2.0.jpg")
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
        #lab['text'] = lab['text'] + "\nDoing Histogram Analysis ..."
        print("Doing Histogram Analysis....")
        #window.update_idletasks()
        rec = cv2.face.LBPHFaceRecognizer_create()
        rec.read("TrainedDataFolder\TraningData.yml") 
        imggray = PIL.Image.open(path+"/img.jpg").convert('L') 
        print(imggray)
        gray = np.array(imggray,'uint8')
        print(gray)
        #lab['text'] = lab['text'] + "\nResult : "
        print("\nResult:")
        id,conf = rec.predict(gray) 
        print(id,conf)
        if(id == 2):
                #lab['text'] = lab['text'] + "\nREAL "
                print("\nREAL")
                #lab['text'] = lab['text'] + str(100 - conf)
                print(str(100-conf))
                elareturns[0]=str(100-conf)
                elareturns[1]=0
        else:
                #lab['text'] = lab['text'] + "\nFAKE "
                print("\nFAKE")
                #lab['text'] = lab['text'] + str(100 - conf)
                print(str(100 -conf ))
                elareturns[0]=str(100-conf)
                elareturns[1]=1
        #b1.pack_forget()

    except Exception as e:
        print("\nFailed to Load Image: "+str(e))
        return elareturns
    try:
        f=1
        #img = PIL.Image.open(r"C:\Users\Carlos\Desktop\TFM\13.jpg")
        img = PIL.Image.open(imageTesting)
        info = img._getexif()
        print(info)
        if info:
            for (tag, value) in info.items():
                if "Software" == TAGS.get(tag, tag):
                        #lab['text'] = lab['text'] + "\nFake Image"
                        #lab['text'] = lab['text'] + "\nFound Software Signature : " + value
                        print("\Fake Image")
                        print("\nFound Software Signature: "+value)
                        elareturns[2]=value
                        f=0
    
        if f:
            #lab['text'] = lab['text'] + "\nNo Software Signature Found"
            #lab['text'] = lab['text'] + "\nLooks like Real"
            print("\nNo Software Signature Found")
            print("\nLooks like Real")
            elareturns[2]="1"
        #b1 = Button(window, text="Continue",command = level2)
        #b2 = Button(window, text="Exit",command = win_dest)
        #b1.pack()
        #b2.pack()  
        return elareturns          
    except Exception as e:
        #lab['text'] = lab['text'] +"\nFailed to Load Metadata : "+str(e)
        #b3 = Button(window, text = "Exit", command = win_dest)
        #b3.pack()
        print("\nFailed to Load Metadata: "+str(e))
    
#window.mainloop()
#level2()