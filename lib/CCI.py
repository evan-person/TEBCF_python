"""
This module contains the code for calculating the contrast code image.
Python rewrite of the MATLAB code by the same name.

MATLAB header info here: 
% Function to calculate the contrast code image (CCI), first proposed in
% the work titled "A Contrast-Guided Approach for the Enhancement 
% of Low-Lighting Underwater Images" by Tunai P. Marques, Alexandra
% Branzan-Albu and Maia Hoeberechts
% By Tunai Porto Marques, 2020 (tunaimarques.com)
%
% Inputs:
% image - the RGB image whose the CCI is calculated upon
% tolerance - parameter that defines the priority that bigger patch sizes
% will have.
%
% Outputs: 
% CCI - a 1-D matrix with the same dimensions as "image" composed, in each
% location x, by the contrast code c that specifies the patch size that 
% generated the smallest local standard deviation considering 7 patch
% sizes.
"""

import cv2
import numpy as np
from scipy.ndimage.filters import generic_filter



def CCI_Calc(image, tolerance):
    # ensure image is stored as double
    image = image.astype(float)
    # define patch sizes
    patch_sizes = [3, 5, 7, 9, 11, 13, 15]
    # create an image with padding big enough to allocate all the dynamic patch sizes 
    # when computing dark channel and transmision maps
    biggest_patch = max(patch_sizes)
    patch_size_range_biggest = round(biggest_patch/2) - 1;

    # assign different patch sizes to be tested
    patch_sizes_2 = [3, 5, 7, 9, 11, 13, 15]

    # determine tolerance factor (weight decay)
    tol = 1-tolerance/100

    # create a tolerance array to proportionally increase priority of bigger patch sizes
    # lowest stdev will determine patch size chosen, so lowering this increases relevance 
    tolerance_array = [1*((tol)^6), 1*((tol)^5), 1*((tol)^4), 1*((tol)^3), 1*((tol)^2), 1*((tol)^1), 1]
    # reshape this into a 3d array with dim3=7 (original code called this a 7-d array)
    tolerance_array = tolerance_array.reshape(1,1,7)
    # replicate the array to match elements of the stdev results image
    tolerance_matrix = np.tile(tolerance_array, (image.shape[0], image.shape[1], 1))


    # create a score image. note that the number of dims is given by number of stdev scores for each pixel,
    # which correspond to number of different window sizes tested
    score_image = np.zeros((image.shape[0], image.shape[1], len(patch_sizes_2)))

    # compute grayscale image calculations
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = gray_image.astype(float)
    for i in range(len(patch_sizes_2)):
        # compute local standard deviation for each patch size
        stdev_image = generic_filter(gray_image, np.std, size=patch_sizes_2[i])  
 
    #do an element-wise multiplication of the stdev image with the tolerance matrix
    score_temp = np.multiply(stdev_image, tolerance_matrix)

    return min(score_temp, 3)

#might need to work the return statement a bit more, here's the last lines of the MATLAB code I'm trying to replicate
# % do an element-wise multiplication with the tolerance matrix so all the
# % std. dev. for higher patch sizes are prioritized (i.e., their values are lowered).
# % note that using tolerance=0 will assign the same priority to the 
# % std. dev. results of all patch sizes. 
# score_temp = score_temp .* tolerance_matrix; 

# % the dimension with lowest value indicates the approapriate patch size (the one 
# % that generated the lowest std. dev. result.  

# % disp("Contrast code image calculated.");
# [~, CCI] = min(score_temp,[],3);