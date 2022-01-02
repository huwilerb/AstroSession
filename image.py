import pandas as pd
import numpy as np

from astropy.io import fits
from pathlib import Path
import pathlib # 

import astro_tools
from config import Config

class Image():
    config = Config(Path.joinpath(Path.cwd(), 'config'),'Image_config.json')
    
    def __init__(self:None, path)->None:
        self.ObjectType = 'Image'
        self.path = path 
        self.__exists()
    
    def get_meta(self)->dict:
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
        return astro_tools.read_fits_header(self.path, restricted=Image.config.Restricted_headers)
        
        
    def populate_meta(self)->None:
        """
        populate the metadata in the object regarding to the image configuration file

        Options
        -------
        the following options for the metadata in the object, to be changed in the configuration file:
            Set a list of the headers as a new attribute : Headers_attribute_as_list == True
            Set each header as a new attribute: Headers_as_ attributes == True 

        """
        data = self.get_meta()
        if Image.config.Headers_attribute_as_list == True:
            self.headers = data
        if Image.config.Headers_as_attributes == True:
            for key in data.keys():
                self.__setattr__(key, data[key])
                

    def read_image(self):
        data = fits.getdata(self.path)
        if image.config.data_as_attribute == True:
            self.__setattr__("data", data)
        return data
    
    

    def __exists(self):
        """
        Check if an image exists
        """
        if not astro_tools.check_path(self.path):
            print(f'The file {self.path} do not exists')
    
