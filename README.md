# Project Summary
Take a video for a pitch as input and output the frame where the ball was released from the pitcher’s hand, 
implemented using Python 3 and OpenCV. 

[//]: # (Image References)
[video1_mask]: ./data/readme_images/test1_446_mask.jpg
[video1_contour]: ./data/readme_images/test1_446_mask_contour.jpg
[edge_case_contour]: ./data/readme_images/edge_case.jpg

# Method
Summary: 
When the ball is released by the pitcher, the pixels for the ball is no longer connected with the pitcher
and forms an indivisual contour. </br>

Step 1. Obtain a binary image for grass and non-grass regions. 

This mask for the color "green" is constructed by converting the original image to HSV color model and setting
the piexels in the range of green grass color as the grass region with pixel values equal to 255. 
The rest of pixels are non-grass region and got pixel values as 0. 

For example, the ball and pitcher would have pixel values as 0. 
        
![alt text][video1_mask]

Step 2. Find the contours and determine if the contours contain a baseball
Contours are filtered by contour areas to remove too large and too small areas. 
If the contour centroid is in the grass region, the contour is not a baseball. 
In addition, a contour is not a ball if the ratio of width to height of bounding rect of the object
is not close to 1, this handels the cases shown below, where contour is marked with a green boundary.
![alt text][edge_case_contour]


Step 3. If a baseball is detected, the frame index is saved to file and this video is finished processing.
Following is an example of a baseball detected and marked with red boundary. The centroid is marked as blue. 
![alt text][video1_contour]


# Files 
```
project
│   README.md
└───code
|   │   pipeline.py             Contains main function for processing videos 
|   │   tool.py                 Helper functions for processing a single frame 
└───data
|   │   log.txt                 Contains final result of the frame where the ball was released for each video
|   │   environment.yml         Anaconda environment file for reproduing the result. 
|   └───frames/                 Visualize mask and contour of the ball, named as videoName _frameId
│   └───video/                  Directory containing *.mp4 videos 
│   └───readme_images/          Images used in this README.md file  
```

# Usage

Run demo use the following line: 
```
python pipeline.py
```