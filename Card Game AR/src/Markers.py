import cv2
import cv2.aruco as aruco
import numpy as np

class Markers:
    def loadAugImage(self, path, imgPath):
        imgAug = cv2.imread(f'{path}/{imgPath}') 
        return imgAug

    def findArucoMarkers(self, img, markerSize=6, totalMarkers=250):
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        key = getattr(aruco,f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
        arucoDict = aruco.Dictionary_get(key)
        arucoParam = aruco.DetectorParameters_create()
        bboxs, ids, _ = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
        return [bboxs, ids]

    def draw(self, img, imgpts, imgAug):
        imgpts = np.int32(imgpts).reshape(-1,2)
        base = np.array([np.array([imgpts[0], imgpts[1], imgpts[3], imgpts[2]])])
        top = np.array([np.array([imgpts[4], imgpts[5], imgpts[7], imgpts[6]])])
        h, w, _ = imgAug.shape
        imgAugPts = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        # draw ground floor in blue
        img = cv2.drawContours(img, base, -1, (255), 3)
        # draw pillars in blue color
        for i,j in zip(range(4),range(4,8)):
            img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
        # draw top layer with imgAug
        matrix, _ = cv2.findHomography(imgAugPts, top)
        imgOut = cv2.warpPerspective(imgAug, matrix, (img.shape[1], img.shape[0]))
        cv2.fillConvexPoly(img, top.astype(int), (0, 0, 0))
        imgOut = img + imgOut
        return imgOut