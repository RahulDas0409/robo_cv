import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)
whT = 320
hT = 320
confThreshold = 0.5
nmsThreshold = 0.3

classesFile = "coco.names"
classNames = []
with open(classesFile,"rt") as f:
    classNames = f.read().rstrip('\n').split('\n')
#print(classNames)
#print(len(classNames))

modelConfiguration = 'yolov4.cfg'
modelWeights = 'yolov4.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObjects(ouputs,img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w,h = int(det[2]*wT), int(det[3]*hT)
                x,y = int((det[0]*wT) - w/2), int((det[1]*hT)-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))
    indices = cv2.dnn.NMSBoxes(bbox,confs,confThreshold,nmsThreshold)
    #print(indices)
    for i in indices:
        box = bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]
        if classNames[classIds[i]] == 'apple':
            d = (((x+w)-x)**2 + ((y+h)-y)**2)
            distance = math.sqrt(d)
            c = ((((x+w)+x)//2), ((y+h)+y)//2)
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
            cv2.putText(img,f'{classNames[classIds[i]]} {int(confs[i]*100)}% {(x,y)} {(x+w,y+h)}',(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,255),2)

while True:
    success, img = cap.read()
    
    blob = cv2.dnn.blobFromImage(img,1/255,(whT,hT),[0,0,0],1,crop=False)
    net.setInput(blob)
    
    layerNames = net.getLayerNames()
    #print(layerNames)
    #print(len(layerNames))
    #print(net.getUnconnectedOutLayers())
    outputNames = [layerNames[i-1] for i in net.getUnconnectedOutLayers()]
    #print(outputNames)
    outputs = net.forward(outputNames)
    #print(len(outputs))
    #print(type(outputs))
    #print(outputs[0])
    #print(outputs[0].shape)
    #print(outputs[1].shape)
    #print(outputs[2].shape)
    #print(outputs[0][0])
    findObjects(outputs, img)
    cv2.imshow("Image", img)
    k = cv2.waitKey(1)
    if k == 27:
        break
    
cv2.destroyAllWindows()