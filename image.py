import pandas as pd
import numpy as np

from astropy.io import fits
from pathlib import Path
import pathlib # 

import astro_tools
from config import Config

class Data:

        def __init__(self, data):
            self.populate(data)
        
        def populate(self, data):
            self.__setattr__("AS_min", int(np.min(data)))
            self.__setattr__("AS_max", int(np.max(data)))
            self.__setattr__("AS_mean", np.mean(data))
            self.__setattr__("AS_std", np.std(data))

        def __str__(self):
            return f'Data stats: min -> {self.AS_min}, max -> {self.AS_max}, mean -> {self.AS_mean}, std -> {self.AS_std}'

class Image():
    config = Config(Path.joinpath(Path.cwd(), 'config'),'Image_config.json')
    
    def __init__(self:None, path: pathlib.Path, autoFill:bool=True)->None:
        self.ObjectType = 'Image'
        self.path = path 
        self.__exists()
        if autoFill:
            self.__autoComplet()   
    
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
        

    def read_image(self):
        """
        read the data of the image and return them 

        """
        ext = Image.config.HDU_location        
        return fits.getdata(self.path, ext=ext)

    def __autoComplet(self):
        meta = self.__populate_meta().keys()
        cstm = Image.config.Data_type_list
        if not all(x in meta for x in cstm):
            self.__populate_data()
            self.__add_stats_to_meta()
            self.populate_data()


    def __populate_meta(self)->dict:
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
        return data       

    def __populate_data(self)->None:
        d = self.read_image()
        self.__setattr__("data", Data(d))
        return None

    
    def __add_stats_to_meta(self)->None:
        for attribute, value in self.data.__dict__.items():
            self.__modify_header(attribute, str(value))
        return None
    
    def __modify_header(self, header:str, value:str)->None:
        fits.setval(self.path, header, value=value)
        return None   
    
    def __exists(self):
        """
        Check if an image exists
        """
        if not astro_tools.check_path(self.path):
            raise ValueError()
    
    @classmethod
    def image_informations_in_HDU_check(cls, update=True):
        """
        Check if the image information are located in the correct HDU according to the configuration file
        
        TO BE COMPLETED
        """

        HDU_in_config = cls.config.HDU_location
        pass
    
    def __str__(self):
        return f'instance of Image'


    
    
