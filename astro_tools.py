"""
Some usefull tools for astrophotography 
written by: blaiseH
date: Aug 12 2021
"""

from astropy.io import fits
from pathlib import Path
import json


def read_fits_header(file):
    """
    read the headers from a fits file

    Parameters
    ----------
    file : .fits
        a fits image

    Returns
    -------
    h : dict
        a dictionnary with the headers as key 

    """
    file_o = fits.open(file)
    h = {str(i): str(file_o[0].header[i]) for i in file_o[0].header}
    return h

def iter_dir_name(path, dirname):
    """
    iter true directories to find the correct names 

    Parameters
    ----------
    path : PosixPath object
        Path to check.
    dirname : string
        name of the specific folder in low cases without 's'.

    Returns
    -------
    dirname : PosixPath
        the correct folder name with or without s and capitalize first letter.

    """
    dirs =  [dirname, dirname + 's', dirname.capitalize(),
             dirname.capitalize() + 's']
    for dir in dirs:
        if Path.is_dir(path.joinpath(dir)):
            return path.joinpath(dir)
    return None


def main ():
    p = Path('/home/blaise/Documents/Astro/Astrosession/test/misc_images/Darks')
    file_name = 'Cignus_Light_300_secs_2021-06-11T23-42-32_001.fits'
    headers = read_fits_header(p.joinpath(file_name))
    config = {"Headers_keys": list(headers.keys())}
    print(config)
    with open('config.json', 'w') as f:
        json.dump(config, f)


if __name__ == "__main__":
    main()
