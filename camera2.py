import cv2
import numpy as np
import json

class OutputForRoute:
    def __init__(self):
        self.obstacles = []
        self.cable = []
        self.destinations = []
        self.cableLength = 0
    def addObstacles(self, arr):
        self.obstacles.append(arr)
        
output = OutputForRoute()
img1 = cv2.imread("prac1.jpg")
img = cv2.resize(img1, (0,0), fx=0.20, fy=0.20) 
original = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
canny = cv2.Canny(blurred, 120, 255, 1)
kernel = np.ones((5,5),np.uint8)
dilate = cv2.dilate(canny, kernel, iterations=2)
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# hsv = cv2.cvtColor(cnts[0], cv2.COLOR_BGR2HSV)
#print (hsv)

#print cnts

# Iterate thorugh contours and filter for ROI
image_number = 0
for c in cnts:
    # print ("HERE")
    temp = []
    x,y,w,h = cv2.boundingRect(c)
    area = cv2.contourArea(c)
   # print (area)
    if ( area > 1000 ) :
        s = str(y) + ', ' + str(x)
        temp.append(s)
        s = str(y) + ', ' + str(x+w)
        temp.append(s)
        s = str(y+h) + ', ' + str(x)
        temp.append(s)
        s = str(y+h) + ', ' + str(x+w)
        temp.append(s)
        output.addObstacles(temp)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,0), 2)
        ROI = original[y:y+h, x:x+w]
        # cv2.imwrite("ROI_{}.png".format(image_number), ROI)
        #print ("here:" + str(ROI))
        image_number += 1

output.cable = ['50, 100', '50, 450']
output.cableLength = 350
output.destinations = ["200, 150","330, 520"]
s = json.dumps(output.__dict__) 

# with open('inputJson.json', 'w') as outfile:
#     outfile.write(s)
# outfile.close()

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
