# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 14:50:56 2018

@author: Yuhao Huang
"""


import pydicom
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import pylab


PR = pydicom.dcmread("Demo/PR_Demo.dcm")

MGUID = PR.ReferencedSeriesSequence[0].ReferencedImageSequence[0].ReferencedSOPInstanceUID
MG = pydicom.dcmread("Demo/MG_Demo.dcm")

Row = MG.Rows
Column = MG.Columns

class GraphicObj:
    unit = ""
    numOfPoints = 0
    data = []
    objType = ""
    filled = False

GraphicObjs = PR.GraphicAnnotationSequence[0].GraphicObjectSequence
GraphicObjCnt = len(GraphicObjs)

ListOfObjs = []
for i in range(0, GraphicObjCnt, 1):
    cur = GraphicObj()
    cur.unit = GraphicObjs[i].GraphicAnnotationUnits
    cur.numOfPoints = GraphicObjs[i].NumberOfGraphicPoints
    cur.data = GraphicObjs[i].GraphicData
    cur.type = GraphicObjs[i].GraphicType
    cur.filled = (GraphicObjs[i].GraphicFilled == "Y")
    ListOfObjs.append(cur)
    
coor = ListOfObjs[0].data

centerx = int(np.rint((coor[0]+coor[2]) / 2))           # Coordinates of the cenrter
centery = int(np.rint((coor[1]+coor[3]) / 2))

longR = int(np.rint(np.sqrt(np.square(coor[0] - coor[2]) + np.square(coor[1] - coor[3])) / 2))      # Length of major / minor radius
shortR = int(np.rint(np.sqrt(np.square(coor[4] - coor[6]) + np.square(coor[5] - coor[7])) / 2))

if ((coor[0] - coor[2]) == 0):
    angle = 0
else:
    angle = np.arctan((coor[1] - coor[3]) / (coor[0] - coor[2])) *180 / np.pi   # Rotation angle
    
img = np.zeros((Row, Column))
white = (255, 255, 255)
img = cv2.ellipse(img, (centerx, centery), (longR, shortR), angle, 0, 360, white, -1)
image = Image.fromarray(img).convert('RGB')
#image.save("PR_Overlay_Mask.png")        #Uncomment if want to save the image

black = (0, 0, 0)
img_1 = MG.pixel_array
img_1 = cv2.ellipse(img_1, (centerx,centery),(longR,shortR),angle,0,360,black, 5)


plt.figure(figsize=(20, 10))
plt.subplot(1,2,1),plt.imshow(img_1, cmap=pylab.cm.gray), plt.title('Mammography with Overlay')
plt.xticks([]), plt.yticks([])
plt.subplot(1,2,2),plt.imshow(image, cmap=pylab.cm.gray),plt.title('Overlay Mask')
plt.xticks([]), plt.yticks([])
plt.show()


