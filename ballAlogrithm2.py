'''
 Author: Alejandro(Steven)
 Date: April.20-2022
 File Name: ballAlgorithm2.py
 File Description: 
    Using motion detection an image with only the objects that moved will be show in the new image.
    With the use of findcontours the center of the ball will be used to ge the ball location in the image
    Output the real world X,Y,& Z of the ball and if in or out of bound
'''

import cv2
import numpy as np
import math
from findContours import findContours

def motionDetectionContours(imgLeft,imgRight,imageFrameWidthDimensions):
    # Testing - Taking in a video for now
    # cap = cv2.VideoCapture(0)
    path = 'videos/bounces/orangeBallBouncePingPongTable1.mov'
    path1 = 'videos/bounds/orangeBallMiddleBound2.mov'
    path2 = 'videos/bounds/orangeBallRightBound2.mov'
    cap = cv2.VideoCapture(path2)
    posListX, posListY, positions = [], [], []
    xList = [item for item in range(0, imageFrameWidthDimensions)]

    substractor = cv2.createBackgroundSubtractorMOG2()
    
    inbound = True
    while True:
        success, video = cap.read()
        
        videoGray = cv2.cvtColor(video,cv2.COLOR_BGR2GRAY)
        
        imgMotionDetection = substractor.apply(videoGray)

        # Find object external outline points
        imgContours, contours = cvzone.findContours(videoGray, imgMotionDetection, minArea=1000)

        # Add the x and y centers of the ball in the two array list

        if contours:
            posListX.append(contours[0]['center'][0])
            posListY.append(contours[0]['center'][1])
        if posListX:
            # Testing - Getting rid of bad first ball read
            print(posListX)
            # del posListX[0]
            # del posListY[0]

            # Polynomial Regression y = Ax^2 + Bx + C
            # Find the Coefficients
            A, B, C = np.polyfit(posListX, posListY, 2)

            # Draws the line and dot of the centroid of the ball
            for imageFrame, (posX, posY) in enumerate(zip(posListX, posListY)):
                pos = (posX, posY)
                cv2.circle(imgContours, pos, 10, (0, 255, 0), cv2.FILLED)
                if imageFrame == 0:
                    cv2.line(imgContours, pos, pos, (0, 255, 0), 5)
                else:
                    cv2.line(imgContours, pos, (posListX[imageFrame - 1], posListY[imageFrame - 1]), (0, 255, 0), 5)
            
            # Create the dot of the Center of the ball
            for x in xList:
                y = int(A * x ** 2 + B * x + C)
                cv2.circle(imgContours, (x, y), 2, (255, 0, 255), cv2.FILLED)
    
            # Prediction
            if len(posListX) < 10:
                # X values 330 to 430  Y 590
                a = A                                                                       
                b = B
                c = C - 590
    
                x = int((-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a))
    
                prediction = 330 < x < 430
                # Covernting Camera to Real World
                #*************** Hard Code Numbers From Intrinsic ***********
                # Camera Demenisons: 752 x 480 pixels
                cxLeft = 752 # width
                cyLeft = 480 # height
                b = 60; # baseline [mm]
                f = 6; # focal length [mm]
                pixelSize = .006; # pixel size [mm]

                # This will be coming from the position list 
                # of the two images being processed
                xLeft = float(5)
                yLeft = float(5)
                xRight = float(6)
                yLeft = float(6)
                centerxLeft = float(xLeft/2)
                centerxRight = float(xRight/2)
                Z = (b * f)/(abs((xLeft-centerxLeft)-(xRight-centerxRight))*pixelSize)
                X = (Z * (xLeft-cxLeft)*pixelSize)/f
                Y = (Z * (yLeft-cyLeft)*pixelSize)/f
                frame = [X, Y, Z]
                positions.append(frame)
        # Display
        # videoGray = cv2.resize(videoGray, (0,0), None, 0.25,0.25) # Resized the img to fourth its size
        # cv2.imshow("Video Gray",videoGray)
        imgMotionDetection = cv2.resize(imgMotionDetection, (0,0), None, 0.25,0.25) # Resized the img to fourth its size
        cv2.imshow("Motion Detection", imgMotionDetection)
        imgColor = cv2.resize(imgContours, (0,0), None, 0.25,0.25) # Resized the img to fourth its size
        cv2.imshow("ImageColor", imgColor) # Makes the img appear on new window

        cv2.waitKey(50)
        # Return variables
        # return positions,inbound

# This is a mock up of the real time loop for image processing
def main():
    # Testing Numbers
    imageFrameWidthDimensions = 2436 #4k
    
    # This is where Framgrabber will be called
    # frameLeft,frameRight = camera.getStereoRGB()
    frameLeft = None #cv2.imread(imageFilePath,0)
    frameRight = None #cv2.imread(imageFilePath,1)
    
    # Testing - Manual Input of Images
    # cv2.imwrite("left.jpg", frameLeft)
    # cv2.imwrite("right.jpg", frameRight)
    positions,inbound = motionDetectionContours(frameLeft,frameRight,imageFrameWidthDimensions)
    print(positions, inbound)

if __name__ == "__main__":
    main()