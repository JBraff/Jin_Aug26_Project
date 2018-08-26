'''
Author: Jin Zhu
'''

import cv2
import tqdm
import os
import numpy as np
import glob
import time

class Tool():
    def __init__(self, out_img_dir):
        # save the frame when the ball is released to self.out_img_dir
        self.out_img_dir = out_img_dir

    @staticmethod
    def get_base(video_full_path):
        '''
        obtain the video name without its directory path and the suffix
        :param video_full_path: full path to a video
        :return: video name without its directory path and the suffix
        '''
        base_with_extension = os.path.basename(video_full_path)
        base_without_extension = os.path.splitext(base_with_extension)[0]
        return base_without_extension

    def save_image(self, frame_idx):
        '''
        Save the frame with contour drawn around the ball and the binary image representing grass and non-grass
        :param frame_idx: index for the frame to be saved
        '''
        if not os.path.exists(self.out_img_dir):
            os.makedirs(self.out_img_dir)
        # save the binary image representing grass and non-grass
        cv2.imwrite(self.out_img_dir + self.video_name + "_"+ str(frame_idx) + "_mask.jpg", self.mask)
        # save the frame with contour drawn around the ball and the binary image
        cv2.imwrite(self.out_img_dir + self.video_name + "_" + str(frame_idx) + "_mask_contour.jpg", self.frame)

    def mask_green(self):
        '''
        construct a binary image representing grass and non-grass,
        where grass region have pixel values 255, and non-grass region have pixel values 0
        '''
        # resize the frame, blur it, and convert it to the HSV color space
        blurred = cv2.GaussianBlur(self.frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        # construct a mask for the color "green"
        # this is the parameter for lower bound and upper bound of green color in hsv space
        lower =(29, 86, 6)
        upper =(64, 255, 255)
        # perform a series of dilations and erosions to remove any small blobs left in the mask
        self.mask = cv2.inRange(hsv, lower, upper)
        self.mask = cv2.erode(self.mask, None, iterations=2)
        self.mask = cv2.dilate(self.mask, None, iterations=2)

    def contour_is_ball(self,contour):
        '''
        Determine whether the contour is a baseball by checking the properties of the contour
        :param contour: contour that is potentially a baseball
        :return: True if the contour is baseball
        '''
        # 1.
        # A contour is not a ball if it's too large or too small

        area = cv2.contourArea(contour)
        # minimum and maximum area to consider a contour as a ball
        min_area = 500
        max_area = 1000

        if area < min_area or area > max_area:
            return False

        # 2.
        # A contour cannot be a ball if its centroid is in the region of grass
        grass_mask_val = 255
        # image_moments is a dictionary of all moment values
        image_moments = cv2.moments(contour)
        # (cX, cY) is the centroid of a contour
        cX = int(image_moments["m10"] / image_moments["m00"])
        cY = int(image_moments["m01"] / image_moments["m00"])
        # draw blue circle at the center of contour for visualization
        cv2.circle(self.frame, (cX, cY), 7, (255, 0, 0), -1)
        # a contour is considered as ball if its centroid is in the region of non-grass
        # and if the contour has aspect ratio close to 1
        if (self.mask[cY][cX] == grass_mask_val):
            return False

        # 3.
        # A contour is not a ball if the ratio of width to height of bounding rect of the object
        # differes from aspect ratio 1 by the amount of aspect_ratio_thresh
        aspect_ratio_thresh = 0.5

        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        if (abs(aspect_ratio - 1) > aspect_ratio_thresh):
            return False

        # Contour is a valid ball if the above checks passed
        return True


    def find_ball(self, frame_idx, frame, video_name):
        '''
        Detect the ball if it's released from the pitcher's hand in a single frame
        :param frame_idx: index for the currently processed frame
        :param frame: RGB color image of the currently processed frame
        :param video_name: name of the video that is being processed
        :return: found_ball is True if a released ball is detected in the frame
        '''

        self.frame = frame
        self.video_name = video_name
        # construct a binary image representing grass and non-grass,
        # where grass region have pixel values 255, and non-grass region have pixel values 0
        self.mask_green()
        # found_ball becomes True when a ball is detected
        found_ball = False
        # find a contour using a copy of the mask, since cv2.findContours will modify the input image
        _, contours, _ = cv2.findContours(np.copy(self.mask), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


        for contour in contours:
            if self.contour_is_ball(contour):
                # draw a red contour around the ball for visualization
                cv2.drawContours(self.frame, contour, -1, (0, 0, 255), thickness=5)
                # a ball is found in the frame
                found_ball = True
        # save the frame where a ball is detected as released from the pitcher
        if (found_ball and self.out_img_dir):
            self.save_image(frame_idx)

        return found_ball



