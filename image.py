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
        __exists()

    def get_meta(self):
        

    def __exists(self):
        if not astro_tools.check_path(self.path):
            raise ValueError(f'The file {self.path} do not exists')
    
