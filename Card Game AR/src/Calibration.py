import cv2
import numpy as np
import glob

class Calibration:
    def __init__(self, checkerboard, checkerboardPath):
        self.checkerboard = checkerboard
        self.checkerboardPath = checkerboardPath

    def calibrate(self):
        # stop the iteration when specified
        # accuracy, epsilon, is reached or
        # specified number of iterations are completed.
        criteria = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        threedpoints = [] # Vector for 3D points

        twodpoints = [] # Vector for 2D points


        #  3D points real world coordinates
        objectp3d = np.zeros((1, self.checkerboard[0]
                              * self.checkerboard[1],
                              3), np.float32)
        objectp3d[0, :, :2] = np.mgrid[0:self.checkerboard[0],
                                       0:self.checkerboard[1]].T.reshape(-1, 2)
        prev_img_shape = None

        images = glob.glob(self.checkerboardPath + '*.jpg') # Get all checkerboard jpg images

        for filename in images: # For each checkerboard image
            image = cv2.imread(filename) # Read the image
            grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Get a gray image of it

            # Find the chess board corners
            # If desired number of corners are
            # found in the image then ret = true
            ret, corners = cv2.findChessboardCorners(
                            grayColor, self.checkerboard,
                            cv2.CALIB_CB_ADAPTIVE_THRESH
                            + cv2.CALIB_CB_FAST_CHECK +
                            cv2.CALIB_CB_NORMALIZE_IMAGE)

            # If desired number of corners can be detected then,
            # refine the pixel coordinates and display
            # them on the images of checker board
            if ret == True:
                threedpoints.append(objectp3d)

                corners2 = cv2.cornerSubPix( # Refining pixel coordinates for given 2d points.
                    grayColor, corners, (11, 11), (-1, -1), criteria)

                twodpoints.append(corners2)

                image = cv2.drawChessboardCorners(image, self.checkerboard, corners2, ret) # Draw and display the corners

        cv2.destroyAllWindows()

        h, w = image.shape[:2]


        # Perform camera calibration by
        # passing the value of above found out 3D points (threedpoints)
        # and its corresponding pixel coordinates of the
        # detected corners (twodpoints)
        self.ret, self.matrix, self.distortion, self.r_vecs, self.t_vecs = cv2.calibrateCamera(
            threedpoints, twodpoints, grayColor.shape[::-1], None, None)

        return self.ret, self.matrix, self.distortion, self.r_vecs, self.t_vecs

    def print(self): # Display camera calibration output
        print(" Camera matrix:")
        print(self.matrix)

        print("\n Distortion coefficient:")
        print(self.distortion)

        print("\n Rotation Vectors:")
        print(self.r_vecs)

        print("\n Translation Vectors:")
        print(self.t_vecs)
