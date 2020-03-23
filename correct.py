import cv2
import numpy as np


def getHowFar (img,hsv,inputSelf, text):
    if "orange" in text:
        low = np.array([5, 50, 50],np.uint8) #orange
        high = np.array([15, 255, 255],np.uint8)#orange
    else:
        low = np.array([5, 50, 50],np.uint8) #orange
        high = np.array([15, 255, 255],np.uint8)#orange
    
    image_mask = cv2.inRange(hsv, low, high)
    zero = cv2.findNonZero(image_mask)
    cv2.imshow("Image", image_mask)
    cv2.waitKey(0)


def determine_how_close(inputSelf, inputOther, text):
    img = cv2.imread("photos/gother.png")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low = np.array([40, 50, 50]) #green
    high = np.array([80, 255, 255]) # green
    image_mask = cv2.inRange(hsv, low, high)
    zero = cv2.findNonZero(image_mask)
    low = np.array([5, 50, 50],np.uint8) #orange
    high = np.array([15, 255, 255],np.uint8)#orange
    image_mask_orange = cv2.inRange(hsv, low, high)
    zero_orange = cv2.findNonZero(image_mask_orange)

    iself = inputSelf.split(', ') 
    iarr = [int(iself[0]),int(iself[1])]
    oself = inputOther.split(', ')
    oarr = [int(oself[0]),int(oself[1])]
    iret = []
    oret = []

    tgreen = []
    for row in zero:
        img[row[0][1]+10, row[0][0]+10] = [0,0,0]
        img[row[0][1]+10, row[0][0]-10] = [0,0,0]
        img[row[0][1]-10, row[0][0]+10] = [0,0,0]
        img[row[0][1]-10, row[0][0]-10] = [0,0,0]
        tgreen.append([row[0][0]+10,row[0][1]+10])
        tgreen.append([row[0][0]-10,row[0][1]+10])
        tgreen.append([row[0][0]+10,row[0][1]-10])
        tgreen.append([row[0][0]-10,row[0][1]-10])

    torange = []
    for row in zero_orange:
        img[row[0][1]+10, row[0][0]+10] = [131,76,16]
        img[row[0][1]+10, row[0][0]-10] = [131,76,16]
        img[row[0][1]-10, row[0][0]+10] = [131,76,16]
        img[row[0][1]-10, row[0][0]-10] = [131,76,16]
        torange.append([row[0][0]+10,row[0][1]+10])
        torange.append([row[0][0]-10,row[0][1]+10])
        torange.append([row[0][0]+10,row[0][1]-10])
        torange.append([row[0][0]-10,row[0][1]-10])

    if "orange" in text:
        if iarr not in torange:
            iret = getHowFar (img,hsv,iarr,text)
        else:
            iret = ["You are fine"]
        if oarr not in tgreen:
            oret = ['Other is wrong']
        else:
            oret = ["Other is fine"]
    else:    
        if iarr not in tgreen :
            iret = getHowFar (img,hsv,iarr,text)
        else:
            iret = ["You are fine"]
        if oarr not in torange:
            oret = ['Other is wrong']
        else:
            oret = ["Other is fine"]
    


    # cv2.imshow("Image", img)
    # cv2.waitKey(0)
    return iret,oret

if __name__ == '__main__':
    # test1.py executed as script
    # do something
    print(determine_how_close("187, 134","412, 180", "green"))