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
        self.Type = ''
        self.path = path 
        self.__exists()

    def get_meta(self, save:bool=False)->dict:
        data = astro_tools.read_fits_header(self.path, restricted=Image.config.Restricted_headers)
        if save:
            self.headers_dict = data
        return data
    


    def add_meta_to_object(self):
        pass

    def read_image(self):
        pass

    def __exists(self):
        if not astro_tools.check_path(self.path):
            print(f'The file {self.path} do not exists')
    
