from multiprocessing import Pool
import os
from PIL import Image,ImageDraw,ImageFont
import cv2

path1 = "dbNudeDetection"
path2 = "data"

listing = os.listdir(path1)    
for file in listing:
    
    # im = Image.open(path1 +'/'+ file)    
    # im.resize((50,50))               
    # im.save(path2 + '/'+file, "JPEG")
    
    img = cv2.imread(path1+'/'+file)

    # Get original height and width
    #img = print(f"Original Dimensions : {img.shape}")

    # resize image by specifying custom width and height
    try :
        resized = cv2.resize(img, (100, 100))
        cv2.imwrite(path2+'/'+file, resized)
    except:
        print('err')
    #cv2.imshow("test",resized)
   

