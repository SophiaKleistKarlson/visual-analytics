# import modules
import os
import pandas as pd
import sys
sys.path.append(os.path.join(".."))
import cv2
import numpy as np
import glob
import re
from utils.imutils import jimshow
from utils.imutils import jimshow_channel
import matplotlib.pyplot as plt


# define plot function be be used later
def plot_n_lines(df, x_axis, save = True):
    fig = plt.figure(figsize = (10.0, 3.0))
    ax = fig.add_subplot(1,2,1) # 1 row , (space for) 2 columns, 1st column position
    ax.set_xlabel(f"{x_axis}") # label for the x-axis
    ax.set_ylabel("number of lines") # label for the y-axis    
    ax.bar(df[x_axis], df["N_Lines"]) # plot generation on the x-axis and n_lines on the y-axis    
    plt.title(f"Development of number of lines over {x_axis}") # title
    fig.tight_layout()
    # save and show figure
    if save == True:
        plt.savefig("n_lines_plot.png")
    plt.show()
    
    
def main(x_axis):
    
    #### Get data #### 
    
    # unzip the zipfile with the images
    # define path to the zip file
    zip_path = os.path.join("..", "data", "img") 

    # set working directory to the zip path
    os.chdir(zip_path)
    print(zip_path)

    # unzip the zipfile
    !unzip 'all_drawings.zip'

    # make a list of all the drawings
    img_path = os.path.join("..", "data", "img", "all_drawings")
    print(img_path)

    # get all png images in the path
    img_list = glob.glob(img_path + "/*.png")
    img_list.sort() # sort the list alphabetically
    #print(img_list)
    #print(len(img_list)) # look at the length of the list

    
    # define path to csv with drawing experiment data
    path_to_csv = os.path.join("..", "data", "df_for_visual_analytics.csv")

    # read the csv
    drawing_df = pd.read_csv(path_to_csv)
    
    
    #### count edges in the images #### 
    
    # make empty lists to be filled in the for loop below
    Drawing_ID = []
    N_Lines = []

    for img_id in img_list: 

        # read image
        image = cv2.imread(img_id) # read image

        # get rid of path and ".png"
        image_name = re.findall('../data/img/all_drawings/(Chain_\d+_Gen_\d+_Cond_\d+_Source_\d+).png', img_id)[0]

        # blur the image using the Gaussian method, thus removing high frequency edges
        blurred = cv2.GaussianBlur(image, (5, 5), 0)

        # do canny edge detection on the blurred image
        canny = cv2.Canny(blurred, 30, 150) 

        # show the canny edge detection image
        #jimshow_channel(canny) 

        # find contours of the canny object
        (cnts, _) = cv2.findContours(canny.copy(), 
                                     cv2.RETR_EXTERNAL, 
                                     cv2.CHAIN_APPROX_SIMPLE)

        # how many contours do we have
        N_Lines.append(len(cnts))
        Drawing_ID.append(image_name)

        ## the next 6 lines you can do if you want to check how the contours look
        # draw contours 
        #image_lines = cv2.drawContours(image.copy(), cnts, -1, (0, 255, 0), 2)
        # show the final image with highlighted lines
        #jimshow(image_lines) 
        # save the image with highlighted lines
        #cv2.imwrite("../data/img/stim_2_contours.jpg", image_lines)

        
    #### merge the data into one dataframe ####
    
    print(len(N_Lines))#1680
    print(len(Drawing_ID))#1680

    # make empty df to be filled with the two lists
    columns = ['Drawing_ID', 'N_Lines']
    index = np.arange(0)
    n_lines_df = pd.DataFrame(columns=columns, index = index)

    for i in range(len(Drawing_ID)):
        # append lists to the n_lines_df
        n_lines_df = n_lines_df.append({
            'Drawing_ID': Drawing_ID[i],
            'N_Lines': N_Lines[i]
        }, ignore_index=True)


    # merge the two dataframes by "Drawing_ID"
    df_merged = pd.merge(drawing_df, n_lines_df, on="Drawing_ID")

        
    #### plot the number of lines on the y-axis with the chosen x-axis ####
    plot_n_lines(df_merged, x_axis=x_axis)
    
    
    #### save the merged df as csv ####
    # output filename
    out_file_name = "n_lines_df_merged"

    # create directory called out, if it doesn't exist
    if not os.path.exists("out"):
        os.mkdir("out")

    # output filepath
    outfile = os.path.join("out", out_file_name)

    # save the DATA panda as a csv file
    df_merged.to_csv(outfile)
    
    
    
# declare namespace
if __name__=="__main__":
    main()
