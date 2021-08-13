"""
Some usefull tools for astrophotography 
written by: blaiseH
date: Aug 12 2021
"""

from astropy.io import fits
from pathlib import Path



# p = Path('/home/blaise/Pictures/test_cam/test 2/Darks')

# file_name = 'Dark_300_secs_001.fits'

# file = fits.open(p.joinpath(file_name))



def read_fits_header(file):
    file_o = fits.open(file)
    h = {str(i): str(file_o[0].header[i]) for i in file_o[0].header}
    return h

# headers = read_fits_header(file)



