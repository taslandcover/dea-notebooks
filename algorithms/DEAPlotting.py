## DEAPlotting.py
'''
This file contains a set of python functions for plotting DEA data.
Available functions:

    three_band_image
    three_band_image_subplots

Last modified: March 2018
Author: Claire Krause
Modified by: Robbi Bishop-Taylor

'''

# Load modules
import numpy as np
from skimage import exposure
import matplotlib.pyplot as plt


def three_band_image(ds, bands, time = 0, figsize = [10,10], contrast_enhance = False, title = 'My Plot', projection = 'projected'):
    '''
    threeBandImage takes three spectral bands and plots them on the RGB bands of an 
    image. 
    
    Last modified: March 2018
    Author: Mike Barnes
    Modified by: Claire Krause, Cate Kooymans

    Inputs: 
    ds -   Dataset containing the bands to be plotted
    bands - list of three bands to be plotted
    
    Optional:
    time - Index value of the time dimension of ds to be plotted
    figsize - dimensions for the output figure
    contrast_enhance - determines the transformation for plotting onto RGB. If contrast_enhance = true, 
                       exposure.equalize_hist is used to trasnform the data. Else, the data are standardised relative
                       to reflectance = 5000.
    title - string for the plot title. If nothing is given, it will print the names of the
            bands being plotted.
    projection - options are 'projected' or 'geographic'. To determine if the image is 
    in degrees or northings
    '''
    try:
    	t, y, x = ds[bands[0]].shape
    	rawimg = np.zeros((y,x,3), dtype = np.float32)
    	for i, colour in enumerate(bands):
            rawimg[:,:,i] = ds[colour][time].values
    except ValueError:
        y, x = ds[bands[0]].shape
        rawimg = np.zeros((y,x,3), dtype = np.float32)
        for i, colour in enumerate(bands):
       	    rawimg[:,:,i] = ds[colour].values
    rawimg[rawimg == -999] = np.nan
    if contrast_enhance == True:
    	img_toshow = exposure.equalize_hist(rawimg, mask = np.isfinite(rawimg))
    else:
    	img_toshow = rawimg / 5000
    fig = plt.figure(figsize = figsize)
    plt.imshow(img_toshow)
    ax = plt.gca()
    try:
        ax.set_title(str(ds.time[time].values), fontweight = 'bold', fontsize = 16)
    except:
        ax.set_title(title, fontweight = 'bold', fontsize = 16)
    ax.set_xticklabels(ds.x.values)
    ax.set_yticklabels(ds.y.values)
    if projection == 'geographic':
        ax.set_xlabel('Longitude', fontweight = 'bold')
        ax.set_ylabel('Latitude', fontweight = 'bold')
    else:
        ax.set_xlabel('Eastings', fontweight = 'bold')
        ax.set_ylabel('Northings', fontweight = 'bold')
    return plt, fig

def three_band_image_subplots(ds, bands, num_cols, contrast_enhance = False, figsize = [10,10], 
                              projection = 'projected', left  = 0.125, 
                              right = 0.9, bottom = 0.1, top = 0.9, 
                              wspace = 0.2, hspace = 0.4):
    '''
    threeBandImage_subplots takes three spectral bands and multiple time steps, 
    and plots them on the RGB bands of an image. 

    Last modified: March 2018
    Author: Mike Barnes
    Modified by: Claire Krause
    
    Inputs: 
    ds -   Dataset containing the bands to be plotted
    bands - list of three bands to be plotted
    num_cols - number of columns for the subplot
    
    Optional:
    contrast_enhance - determines the transformation for plotting onto RGB. If contrast_enhance = true, 
                       exposure.equalize_hist is used to trasnform the data. Else, the data are standardised relative
                       to reflectance = 5000.
    figsize - dimensions for the output figure
    projection - options are 'projected' or 'geographic'. To determine if the image 
                 is in degrees or northings
    left  - the space on the left side of the subplots of the figure
    right - the space on the right side of the subplots of the figure
    bottom - the space on the bottom of the subplots of the figure
    top - the space on the top of the subplots of the figure
    wspace - the amount of width reserved for blank space between subplots
    hspace - the amount of height reserved for white space between subplots
    '''
    # Find the number of rows/columns we need, based on the number of time steps in ds
    timesteps = ds.time.size
    num_rows = int(np.ceil(timesteps//num_cols))
    fig, axes = plt.subplots(num_rows, num_cols, figsize = figsize)
    fig.subplots_adjust(left  = left, right = right, bottom = bottom, top = top, 
                        wspace = wspace, hspace = hspace)
    numbers = 0
    try:
        for ax in axes.flat:
            t, y, x = ds[bands[0]].shape
            rawimg = np.zeros((y,x,3), dtype = np.float32)
            for i, colour in enumerate(bands):
                rawimg[:,:,i] = ds[colour][numbers].values
            rawimg[rawimg == -999] = np.nan
	    if contrast_enhance == True:
	    	img_toshow = exposure.equalize_hist(rawimg, mask = np.isfinite(rawimg))
	    else:
	    	img_toshow = rawimg / 5000
            ax.imshow(img_toshow)
            ax.set_title(str(ds.time[numbers].values), fontweight = 'bold', fontsize = 12)
            ax.set_xticklabels(ds.x.values, fontsize = 8, rotation = 20)
            ax.set_yticklabels(ds.y.values, fontsize = 8)
            if projection == 'geographic':
                ax.set_xlabel('Longitude', fontweight = 'bold', fontsize = 10)
                ax.set_ylabel('Latitude', fontweight = 'bold', fontsize = 10)
            else:
                ax.set_xlabel('Eastings', fontweight = 'bold', fontsize = 10)
                ax.set_ylabel('Northings', fontweight = 'bold', fontsize = 10)
            numbers = numbers + 1
    except IndexError:
        # This error will pop up if there are not enough scenes to fill the number of 
        # rows x columns, so we can safely ignore it
        fig.delaxes(ax)
        plt.draw()    


