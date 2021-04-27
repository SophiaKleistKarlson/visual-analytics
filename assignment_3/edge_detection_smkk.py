# we need to include the home directory in our path in order to read in our own module
import os
import sys
sys.path.append(os.path.join(".."))
import cv2
import numpy as np
from utils.imutils import jimshow
from utils.imutils import jimshow_channel
import matplotlib.pyplot as plt


# define the main() function
def main():
    
    # read image
    image = cv2.imread("../data/img/_We_Hold_These_Truths__at_Jefferson_Memorial_IMG_4729.jfif") # read image

    # show the original and grey scale image
    #jimshow(image) 
    #jimshow_channel(grey) 

    # to draw a rectangle around the region of interest, I first look at the dimensions of the image
    print(image.shape)

    # and then try around until I find a rectangle that works 
    image_with_ROI = cv2.rectangle(image, (1370, 870), (2890, 2790), (0,255,0), 1)

    # show image with ROI as a green rectangle
    #jimshow(ROI_rectangle) 

    # cut the ROI out of the image 
    # I cut off 1 pixel of each side to not include the outline of the rectangle (which else is included for some reason)
    ROI = image[871:2789, 1371:2889] 

    # show the cropped image
    #jimshow(ROI) 

    # save the cropped image
    cv2.imwrite("../data/img/image_cropped.jpg", ROI)

    # save the image with ROI
    cv2.imwrite("../data/img/image_with_ROI.jpg", image_with_ROI)


    # make the cropped image intro grey scale
    grey = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)

    # show grey scale cropped image
    #jimshow_channel(grey) 

    # create a histogram to see how the frequencies are distributed
    plt.hist(grey.flatten(),256,[0,256])

    # show histogram
    plt.show()

    # blur the image using the Gaussian method, thus removing high frequency edges
    blurred = cv2.GaussianBlur(grey, (5, 5), 0)

    # set the threshold to 110-200, to filter away all the background and lighter edges of the stones
    (T, thres) = cv2.threshold(blurred, 110, 200, cv2.THRESH_BINARY)

    # show threshold image
    #jimshow_channel(thres)

    # do canny edge detection on the thres image
    canny = cv2.Canny(thres, 30, 150)

    # show the canny edge detection image
    #jimshow_channel(canny) 


    # find contours of the canny object
    (cnts, _) = cv2.findContours(canny.copy(), 
                                 cv2.RETR_EXTERNAL, 
                                 cv2.CHAIN_APPROX_SIMPLE)

    # how many contours do we have
    print(len(cnts)) # 1319

    # draw contours 
    image_letters = cv2.drawContours(ROI.copy(), cnts, -1, (0, 255, 0), 2)

    # show the final image with highlighted letters and punctuation
    jimshow(image_letters) 

    # save the image with highlighted letters
    cv2.imwrite("../data/img/image_letters.jpg", image_letters)

    
    
# declare namespace
if __name__=="__main__":
    main()