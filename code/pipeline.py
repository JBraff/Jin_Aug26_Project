'''
Author: Jin Zhu
'''
from tool import Tool
import tqdm
import os
import numpy as np
import glob
import time
import cv2

class Pipeline():
    def __init__(self, out_img_dir=None):
        # tool for processing one frame and save the frame when the ball is released to out_img_dir
        self.tool = Tool(out_img_dir)

    def process_video(self, video_path):
        '''
        Process one video, write the frame ID for when the ball was released to the log file
        :param video_path: path to the video of a baseball pitch
        '''

        cap = cv2.VideoCapture(video_path)

        video_base_name = self.tool.get_base(video_path)

        # process videos frame by frame, from the first to the last frame
        frame_indices = np.arange(1, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        for i in tqdm.tqdm(frame_indices):
            success, frame = cap.read()
            if success:
                # stop the program after finding the frame where ball was released, and record the frame index
                found_ball = self.tool.find_ball(i, frame, video_base_name)

                if found_ball:
                    frame_ball_release = i
                    break

        # save results to log file
        self.parse_log_file.write('Ball released at frame {} for video {}\n'
                                  .format(frame_ball_release, video_base_name))
        self.parse_log_file.flush()

    def process_all_video(self, video_dir, parse_log):
        '''
        Process all videos in a directory
        :param video_dir: Directory containing all videos to be processed
        :param parse_log: Log file that records the frame index where the ball was released
        '''

        self.parse_log_file = open(parse_log, "w")
        # get a list of video paths, in the alphabetical order of file names
        video_paths = sorted(glob.glob(video_dir + "*.mp4"), 
                            key=self.tool.get_base)

        for video_path in video_paths:
            # process each video and write the frame index where the ball was released to  parse_log_file
            self.process_video(video_path)
        self.parse_log_file.close()

def main():
    video_dir = "../data/video/"
    out_img_dir = "../data/frames/" # use None if do not want to visualize the frames when ball is released
    parse_log = "../data/log.txt"
    video_tool = Pipeline(out_img_dir)
    video_tool.process_all_video(video_dir, parse_log)

if __name__ == '__main__':
    main()




