# import necessary libraries
import os
import sys
import glob
import pandas as pd
import re

sys.path.append(os.path.join("..")) # to be able to use the jimshow function

# display utils
from utils.imutils import jimshow
import matplotlib.pyplot as plt

# image processing
import cv2
import numpy as np



# Define main function
def main():
    
    ### __initial stuff__ ###
    
    # define path to the zip file
    zip_path = os.path.join("..", "assignment_2", "data", "img") 

    # set working directory to the zip path
    os.chdir(zip_path)
    #print(zip_path)

    # unzip the zipfile into the working directory (img folder)
    !unzip 'flower_images.zip'
    
    # define filepath
    filepath = os.path.join("..", "data", "img", "flower_images")
    #print(filepath)

    # prepare panda to write logs
    columns = ['filename', 'distance']
    index = np.arange(0)
    distance_data = pd.DataFrame(columns=columns, index = index)
    
    
    ### __read in images and create 3D histogram of target image__ ###
    
    # make a list of all the images
    images = glob.glob(filepath + "/*.jpg")

    # sort the images alphabetically
    images.sort()

    # chose target image - I just take the first one
    target = images[0]

    # remove target image from the list
    images.remove(images[0])

    # print the length of the list to check it's gone
    print(len(images))
    #print(images)

    # read target image
    img_target = cv2.imread(target)

    # look at the target image
    jimshow(img_target)

    # define the range list for the histograms
    range_hist = [0, 256, 0, 256, 0, 256]

    # make 3D histogram of target image
    target_hist = cv2.calcHist([img_target], [0, 1, 2], None, [8, 8, 8], range_hist)

    # normalize histogram
    target_hist_normalized = cv2.normalize(target_hist,target_hist,0,255,cv2.NORM_MINMAX)

    # define plot function for plotting the target image histogram
    def plot_3D_hist(input_image):
        # initialize figure
        plt.figure()
        # plot histogram
        plt.hist(target_hist_normalized.flatten(), 256, [0,256])
        # give plot a title
        plt.title("Target 3D histogram")
        # create x labels
        plt.xlabel("Bin number")
        # create y labels 
        plt.ylabel("Number of pixels")
        # show plot
        plt.show()

    # plot target histogram
    plot_3D_hist(img_target)

    
    ### __compare histograms of target image and all the other images__ ###

    # for each image
    for image in images:

        # read the image
        img = cv2.imread(image)

        # create 3D histogram of image 
        image_hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], range_hist)

        # normalize histogram
        image_hist_normalized = cv2.normalize(image_hist,image_hist,0,255,cv2.NORM_MINMAX)

        # compare histograms with the chi-square distance method
        chi_squared = cv2.compareHist(target_hist_normalized, image_hist_normalized, cv2.HISTCMP_CHISQR)

        # round distance to two decimals
        distance_rounded = round(chi_squared, 2)

        # use a dummy variable to isolate the image name (and leave out the path)        
        _, image_id = os.path.split(image) 

        # if I also wanted to leave out the ".jpg"
        #image_id = re.split('\.jpg', image_id)[0]  

        # write output to pandas
        distance_data = distance_data.append({
            'filename': image_id,
            'distance': distance_rounded
        }, ignore_index=True)
        
    # print distance_data
    print(distance_data)

    
    ### __find image closest to the target__ ###
    
    # to find the image that is closest to the target, first get the index of the row where the minimum distance appears
    min_distance_indx = distance_data[['distance']].idxmin() 

    # then print the row with that index
    print(distance_data.loc[[int(min_distance_indx)]]) 
    # output:
    #           filename  distance
    #595  image_0597.jpg   1241.81

    
    ### __save outfile__ ###
    
    # output filename
    out_file_name = "image_search"

    # create directory called out, if it doesn't exist
    if not os.path.exists("out"):
        os.mkdir("out")

    # output filepath
    outfile = os.path.join("out", out_file_name)

    # save the distance_data panda as a csv file
    distance_data.to_csv(outfile)
    
    
# Define behaviour when called from command line
if __name__=="__main__":
    main()
