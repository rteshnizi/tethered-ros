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
img = cv2.imread("fill.png")
#img = cv2.resize(img1, (0,0), fx=0.15, fy=0.15) 
original = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
canny = cv2.Canny(blurred, 120, 255, 1)
kernel = np.ones((5,5),np.uint8)
dilate = cv2.dilate(canny, kernel, iterations=2)
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

##FINDING OBSTACLES
low = np.array([140, 150, 0])
high = np.array([180, 255, 255])
image_mask = cv2.inRange(hsv, low, high )
zero = cv2.findNonZero(image_mask)
temp = [] 
t = zero[0]
for x in np.nditer(t):
    temp.append(str(x))
t2 = zero[len(zero)-1]
for x in np.nditer(t2):
    temp.append(str(x))
obst = []
o = str(temp[0]) + ', ' + str(temp[1])
obst.append(o)
o = str(temp[2]) + ', ' + str(temp[1])
obst.append(o)
o = str(temp[0]) + ', ' + str(temp[3])
obst.append(o)
o = str(temp[2]) + ', ' + str(temp[3])
obst.append(o)
output.addObstacles(obst)
#cv2.imshow("Image mask-red", image_mask)

##FINDING Cable
low = np.array([40, 50, 50])
high = np.array([80, 255, 255])
image_mask = cv2.inRange(hsv, low, high)
zero = cv2.findNonZero(image_mask)
temp = [] 
t = zero[0]
for x in np.nditer(t):
    temp.append(str(x))
t2 = zero[len(zero)-1]
for x in np.nditer(t2):
    temp.append(str(x))
cab = []
o = str(temp[0]) + ', ' + str(temp[1])
cab.append(o)
o = str(temp[2]) + ', ' + str(temp[3])
cab.append(o)
output.cable = cab
output.cableLength = int(temp[2]) - int(temp[0]) 
#cv2.imshow("Image mask-green", image_mask)

## Finding destinations
low = np.array([100, 50, 50])
high = np.array([140, 255, 255])
image_mask = cv2.inRange(hsv, low, high)
zero = cv2.findNonZero(image_mask)
dest = []
while (zero is not None):
    zero_copy = zero
    temp = [] 
    t = zero_copy[0]
    for x in np.nditer(t):
        temp.append(str(x))
    countHeight = 0
    countWidth = 0
    for row in zero_copy:
        if (row[0][0] == int(temp[0])): # does whole height
            countHeight = countHeight+1
        if (row[0][1] == int(temp[1])): # does whole width
            countWidth = countWidth+1

# img[int(temp[1])+countHeight-1, int(temp[0])] = [205,82,57] #BOTTOM LEFT
# img[int(temp[1]), int(temp[0])] = [30,186,134] # TOP LEFT
# img[int(temp[1]), int(temp[0])+countWidth-1] = [144,37,100] #TOP RIGHT
# img[int(temp[1])+countHeight-1, int(temp[0])+countWidth-1] = [30,186,134] #BOTTOM RIGHT


    dest.append(str(int(temp[0])+countWidth-1))
    dest.append(str(int(temp[1])+countHeight-1))

    j = 0
    for row in zero_copy:
        if ( ((row[0][0] >= int(temp[0]) and row[0][1] >= int(temp[1])) and (row[0][0] <= int(temp[0])+countWidth-1 and row[0][1] <= int(temp[1])+countHeight-1)) and j < len(zero_copy)):
            img[row[0][1],row[0][0]] = [0,0,0]
        j = j + 1
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    image_mask = cv2.inRange(hsv, low, high)
    zero = cv2.findNonZero(image_mask)

output.destinations = dest
cv2.imshow("Image mask-blue", image_mask)



s = json.dumps(output.__dict__) 

with open('inputJson.json', 'w') as outfile:
    outfile.write(s)
outfile.close()

cv2.imshow('image', img)
cv2.waitKey(0)
