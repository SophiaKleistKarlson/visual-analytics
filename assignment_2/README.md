## Assignment 2 - Simple image search

### DESCRIPTION

Creating a simple image search script

Download the Oxford-17 flowers image data set, available at this link:

https://www.robots.ox.ac.uk/~vgg/data/flowers/17/


Choose one image in your data that you want to be the 'target image'. Write a Python script or Notebook which does the following:

Use the cv2.compareHist() function to compare the 3D color histogram for your target image to each of the other images in the corpus one-by-one.
In particular, use chi-square distance method, like we used in class. Round this number to 2 decimal places.
Save the results from this comparison as a single .csv file, showing the distance between your target image and each of the other images. The .csv file should show the filename for every image in your data except the target and the distance metric between that image and your target. Call your columns: filename, distance.
Print the filename of the image which is 'closest' to your target image


### General instructions

For this exercise, you can upload either a standalone script OR a Jupyter Notebook
Save your script as image_search.py OR image_search.ipynb
If you have external dependencies, you must include a requirements.txt
You can either upload the script here or push to GitHub and include a link - or both!
Your code should be clearly documented in a way that allows others to easily follow along
Similarly, remember to use descriptive variable names! A name like hist is more readable than h.
The filenames of the saved images should clearly relate to the original image


### Purpose

This assignment is designed to test that you have a understanding of:

how to make extract features from images based on colour space;
how to compare images for similarity based on their colour histogram;
how to combine these skills to create an image 'search engine'
