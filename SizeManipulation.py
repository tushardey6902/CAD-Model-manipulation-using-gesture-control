import pygame
from math import *
import cv2
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math


detector = HandDetector(detectionCon=0.7)
cap = cv2.VideoCapture(0)
cap.set(3, 460)
cap.set(4, 480)


WINDOW_SIZE =  800
ROTATE_SPEED = 0.02
window = pygame.display.set_mode( (WINDOW_SIZE, WINDOW_SIZE) )
clock = pygame.time.Clock()

projection_matrix = [[1,0,0],
                     [0,1,0],
                     [0,0,0]]

cube_points = [n for n in range(8)]
cube_points[0] = [[-1], [-1], [1]]
cube_points[1] = [[1],[-1],[1]]
cube_points[2] = [[1],[1],[1]]
cube_points[3] = [[-1],[1],[1]]
cube_points[4] = [[-1],[-1],[-1]]
cube_points[5] = [[1],[-1],[-1]]
cube_points[6] = [[1],[1],[-1]]
cube_points[7] = [[-1],[1],[-1]]

###############################################################################################
def multiply_m(a, b):
    a_rows = len(a)
    a_cols = len(a[0])

    b_rows = len(b)
    b_cols = len(b[0])
    # Dot product matrix dimentions = a_rows x b_cols
    product = [[0 for _ in range(b_cols)] for _ in range(a_rows)]

    if a_cols == b_rows:
        for i in range(a_rows):
            for j in range(b_cols):
                for k in range(b_rows):
                    product[i][j] += a[i][k] * b[k][j]
    else:
        print("INCOMPATIBLE MATRIX SIZES")
    return product        


def connect_points(i, j, points):
    pygame.draw.line(window, (255, 255, 255), (points[i][0], points[i][1]) , (points[j][0], points[j][1]))
###################################################################################################################
# Main Loop
scale = 200
angle_x = angle_y = angle_z = 0

while True:
    clock.tick(100)
    window.fill((0,0,0))
    rotation_x = [[1, 0, 0],
                    [0, cos(angle_x), -sin(angle_x)],
                    [0, sin(angle_x), cos(angle_x)]]

    rotation_y = [[cos(angle_y), 0, sin(angle_y)],
                    [0, 1, 0],
                    [-sin(angle_y), 0, cos(angle_y)]]

    rotation_z = [[cos(angle_z), -sin(angle_z), 0],
                    [sin(angle_z), cos(angle_z), 0],
                    [0, 0, 1]]

    points = [0 for _ in range(len(cube_points))]
    i = 0
    for point in cube_points:
        rotate_x = multiply_m(rotation_x, point)
        rotate_y = multiply_m(rotation_y, rotate_x)
        rotate_z = multiply_m(rotation_z, rotate_y)
        point_2d = multiply_m(projection_matrix, rotate_z)
    
        x = (point_2d[0][0] * scale) + WINDOW_SIZE/2
        y = (point_2d[1][0] * scale) + WINDOW_SIZE/2

        points[i] = (x,y)
        i += 1
        pygame.draw.circle(window, (255, 0, 0), (x, y), 5)

    connect_points(0, 1, points)
    connect_points(0, 3, points)
    connect_points(0, 4, points)
    connect_points(1, 2, points)
    connect_points(1, 5, points)
    connect_points(2, 6, points)
    connect_points(2, 3, points)
    connect_points(3, 7, points)
    connect_points(4, 5, points)
    connect_points(4, 7, points)
    connect_points(6, 5, points)
    connect_points(6, 7, points)

    success,img = cap.read()
    hands,img = detector.findHands(img)

    if hands:

        hand = hands[0]
        lmList = hand["lmList"]


        x1,y1 = lmList[4][0], lmList[4][1]
        x2,y2 = lmList[8][0], lmList[8][1]
        cx, cy = (x1+x2)//2,(y1+y2)//2

        cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255, 0, 255), 3)

        length = math.hypot(x2-x1, y2-y1)

        scale = 30 + (2/3)*(length-20)

    cv2.imshow("IMG",img)
    cv2.waitKey(1)

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
        
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_r]:
    #         angle_y = angle_x = angle_z = 0
    #     if keys[pygame.K_a]:
    #         angle_y += ROTATE_SPEED
    #     if keys[pygame.K_d]:
    #         angle_y -= ROTATE_SPEED      
    #     if keys[pygame.K_w]:
    #         angle_x += ROTATE_SPEED
    #     if keys[pygame.K_s]:
    #         angle_x -= ROTATE_SPEED
    #     if keys[pygame.K_q]:
    #         angle_z -= ROTATE_SPEED
    #     if keys[pygame.K_e]:
    #         angle_z += ROTATE_SPEED      
          
    pygame.display.update()