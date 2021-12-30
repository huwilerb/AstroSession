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
    
    def get_meta(self, save:bool=False)->dict:
        return astro_tools.read_fits_header(self.path, restricted=Image.config.Restricted_headers)
        
        
    def populate_meta(self)->None:
        data = self.get_meta()
        if Image.config.Headers_attribute_as_list == True:
            self.headers = data
        if Image.config.Headers_as_attributes == True:
            for key in data.keys():
                self.__setattr__(key, data[key])
                

    def read_image(self):
        pass

    def __exists(self):
        if not astro_tools.check_path(self.path):
            print(f'The file {self.path} do not exists')
    
