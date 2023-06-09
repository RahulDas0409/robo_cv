import cv2
import math
import pyrealsense2
from a import *
from realsense_config import *

rc = RealsenseCamera()

theta = 0
point = (320, 240)

def get_distance(event, x, y, args, params):
    global point
    #print(x, y)
    point = (x, y)

def generate_global_coordinates(x,y,d):
    intr = rc.get_intrinsic()                   # cx,cy,fx,fy = 321.936, 236.083, 382.121, 382.121
    Xtemp = (d*((x-intr[0])/intr[2]))           # depth*((x-ppx)/fx)
    Ytemp = (d*((y-intr[1])/intr[3]))           # depth*((y-ppy)/fy)
    Ztemp = d
    
    Xtarget = Xtemp - 35                        # 35 is RGB camera module offset from the center of the realsense
    Ytarget = -(Ztemp*math.sin(theta) + Ytemp*math.cos(theta))
    Ztarget = Ztemp*math.cos(theta) + Ytemp*math.sin(theta)
    
   # print(Xtarget, Ytarget, Ztarget)
    # Xtarget = Xtarget/1000
    # Ytarget = Ytarget/1000
    # Ztarget = Ztarget/1000
    Xg, Yg, Zg ,Xa ,Ya , Za=-(Xtarget-270-120),-(Ztarget-421-160), Ytarget+960-35+70, 0, 90, -90
     #   Xg, Yg, Zg ,Xa ,Ya , Za= Ztarget-310, -(Xtarget-210), Ytarget+1101-85, 0, 90, 0

    #y=71
    gCoord = (Xg, Yg, Zg, Xa, Ya, Za)
    # a1 = 225
    # a2 = 200
    # a3 = 448
    # a4 = 295
    # a5 = 170
    # a6 = 273
    
    # r1 = math.sqrt((Xg**2)+(Yg**2))
    # r2 = Zg - a1
    # r3 = math.sqrt((r1**2)+(r2**2))
    
    # value1 = r2/r1
    # phi1 = math.atan(value1)
    # value2 = (a2**2+r3**2-a3**2)/(2*a2*r3)
    # phi2 = math.acos(value2)
    # value3 = (a2**2+a3**2-r3**2)/(2*a2*a3)
    # phi3 = math.acos(value3)
    # theta0 = math.atan2(Yg,Xg)
    # theta1 = -(phi1+phi2)
    # theta2 = math.pi - phi3
    
    # R03 = [
    #     [-math.sin(theta1+theta2), -math.cos(theta1+theta2), 0],
    #     [math.sin(theta0)*math.cos(theta1+theta2), -math.sin(theta0)*math.sin(theta1+theta2), -math.cos(theta0)],
    #     [math.cos(theta0)*math.cos(theta1+theta2), -math.cos(theta0)*math.sin(theta1+theta2), math.sin(theta0)]
    # ]
    
    # R06 = [
    #     [-1, 0, 0],
    #     [0, -1, 0],
    #     [0, 0, 1]
    # ]
    
    # invR03 = np.linalg.inv(R03)
    # R36 = np.dot(invR03, R06)
    
    # theta4 = np.arccos(R36[2][2])
    # theta5 = np.arccos(-R36[2][0]/np.sin(theta4))
    # theta3 = np.arccos(R36[1][2]/np.sin(theta4))
    
    # ROLL = theta3
    # PITCH = theta4
    # YAW = theta5
    
    # gCoord = (Xg, Yg, Zg, ROLL, PITCH, YAW)
    # print(f"X = {gCoord[0]} Y = {gCoord[1]} Z = {gCoord[2]} ROLL = {gCoord[3]} PITCH = {gCoord[4]} YAW = {gCoord[5]}")
    return gCoord

cv2.namedWindow("Color Frame")
cv2.setMouseCallback("Color Frame", get_distance)
# 	gotoxyzE()r Frame", get_distance)

while True:
    _, depth_frame, color_frame = rc.get_frame()

    #point = (400, 300)
    #cv2.circle(color_frame, point, 4, (0, 0, 255))
    #distance = depth_frame[point[1], point[0]]
    #print(distance)
    
    distance = depth_frame[point[1], point[0]]
    
    cv2.putText(color_frame, "{} mm".format(distance), (point[0], point[1]), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
    cv2.putText(color_frame, "{}".format(point), (point[0], point[1]+20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)

    # cv2.imshow("Depth Frame", depth_frame)
    cv2.imshow("Color Frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
    
    elif key==32:
        #print(point, distance)
        gCoord = generate_global_coordinates(x=point[0], y=point[1], d=distance)
        print(gCoord)
        startmain()
        gohome()
        opengripper()
        gotoxyzE(gCoord)
        gotoxyzLE(gCoord)
        closegripper()
        gotoxyzE(gCoord)
        gohome()
        gotoxyzstore()
        opengripper()
        gohome()
