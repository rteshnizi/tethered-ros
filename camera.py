# import cv2
# import numpy as np
# import base64
# import json
# import pickle
# from PIL import Image

# #image = cv2.imread('first.jpg')

# img = cv2.imread('first.jpg', cv2.IMREAD_UNCHANGED)
 
# # get dimensions of image
# dimensions = img.shape
 
# # height, width, number of channels in image
# height = img.shape[0]
# width = img.shape[1]
# channels = img.shape[2]
 
# print('Image Dimension    : ',dimensions)
# print('Image Height       : ',height)
# print('Image Width        : ',width)
# print('Number of Channels : ',channels) 
# # original = image.copy()
# # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # blurred = cv2.GaussianBlur(gray, (3, 3), 0)
# # canny = cv2.Canny(blurred, 120, 255, 1)
# # kernel = np.ones((5,5),np.uint8)
# # dilate = cv2.dilate(canny, kernel, iterations=1)


# # Find contours
# # cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# # cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# # # Iterate thorugh contours and filter for ROI
# # image_number = 0
# # for c in cnts:
# #     x,y,w,h = cv2.boundingRect(c)
# #     cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
# #     ROI = original[y:y+h, x:x+w]
# #     #cv2.imwrite("ROI_{}.png".format(image_number), ROI)
# #     image_number += 1

# # cv2.imshow('image', image)
# # cv2.waitKey(0)


# # img_file = open("first.jpg", "r")
# # data = img_file.read()        

# # # build JSON object
# # outjson = {}
# # outjson['img'] = data.encode('base64')   # data has to be encoded base64 and decode back in the Android app base64 as well
# # outjson['leaf'] = "leaf"
# # json_data = json.dumps(outjson)


# # # close file pointer and send data
# # img_file.close()

# # print json_data

# # px = img[100,100]
# # print px


# # blue = img[100,100,0]
# # print blue


# # for i in range (5):
# #     img[10,i] = [164,98,189]
# #print img[100,100]
