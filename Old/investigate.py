#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 23:48:38 2021

@author: fred
"""

from astropy.io import fits
import matplotlib.pyplot as plt

import numpy as np
from pathlib import Path as path


path_='/home/blaise/Pictures/test_cam/Light/' 
path_1='/home/blaise/Pictures/test_cam/Dark/' 
# dark
dark = fits.getdata('/home/blaise/Pictures/Astro/test_dark/Light/Light_180_secs_001.fits')

dark_name = 'dark_Light_10_secs_001.fits'
dark2 = fits.getdata(path_+dark_name)

dark_name_3 = 'dark_Dark_10_secs_001.fits'
dark3 = fits.getdata(path_1+dark_name_3)
# light
light = fits.getdata('/home/blaise/Pictures/Astro/M101/lights/Arcturus_Light_180_secs_2021-04-24T00-44-49_001.fits')

light_name = 'Light_Light_10_secs_001.fits'
light2 = fits.getdata(path_+light_name)
## flat
#flat = fits.getdata('flats/Flat_0.038_secs_2021-04-22T19-02-16_001.fits')
#
#image = (light - dark/100) / flat


#for dark in glob("dark/*.fits"):
#    newname = dark.replace('.fits', '') + '_rescaled.fits'
#    dark = (fits.getdata(dark)/ 100.)
#    
#    fits.writeto(newname, dark)
fig, axs = plt.subplots(3,1)
ax1, ax2, ax3 = axs
ax1.hist(dark2.flatten(),bins=400, label='dark2')
ax2.hist(dark3.flatten(), bins=400, label='dark3')    
ax3.hist(light2.flatten(), bins=400, label='light2')  

for ax in axs:
#    ax.set_xlim((1500,5000))
    ax.legend()

#plt.legend()