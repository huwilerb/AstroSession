#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:19:21 2021

@author: blaise
"""

import pandas as pd
import numpy as np

from astropy.io import fits
from pathlib import Path
import pathlib # 

import astro_tools
from config import Config

class img():
    
    def __init__(self, ImPath, ImType):
        self.type = 'Image'
        self.ImType = ImType
        self.config = Config()
        self.path = ImPath

    def populate_exifs(self):
        headers = ""

class ImagesSet():
    
    def __init__(self, path):
        self.imtype = 'Images_set'
        self.path = Path(path)
        self.config = Config()
        
    def populate_data_image(self): 
        
        files = [x for x in self.path.iterdir() if x.is_file()]
        
        if len(files) > 0:
            self.number = len(files)
            self.data=pd.DataFrame({'Path': files})
            self.data['Name']= self.data.apply(
                lambda row: row.Path.parts[-1], axis=1)
            self.data['Extension'] = self.data.apply(
                lambda row: row.Name.split(".")[-1], axis=1)
            self.data['Size'] = self.data.apply(
                lambda row: Path(row.Path).stat().st_size, axis=1)
        
    def return_headers(self, headers, key): #to test
        return {path:headers[path][key] for path in headers}
        
    def populate_fits_headers(self): # to test
        headers = {path:astro_tools.read_fits_header(path) for path in self.data.Path}
        for key in headers[self.data.Path[0]]:
            self.data[key] = self.data["Path"].map(self.return_headers(headers,
                                                                       key))
    
    def images_statistics(self, ratio = 0.2, mini =10): #to test
        dataset_len = self.data.shape[0]
        
        if dataset_len < mini:
            analysis_len = dataset_len
            analysis_type = 'full'
            self.analysis_type = analysis_type #to remove
        elif dataset_len*ratio < mini:
            analysis_len = dataset_len
            analsis_type = 'full'
            self.analysis_type = analysis_type #to remove
        else:
            analysis_len = dataset_len
            analysis_type = 'statistical'
            self.analysis_type = analysis_type #to remove
        
        if analysis_type == 'full':
            image_set_stat = imgs.data.Path[:].to_list()
            
        
    def _get_fits_values(self, path): # -> tested
        data = fits.getdata(path)
        return data
    
    def _get_fits_mean(self, data, data_type='data'): # -> tested
        if data_type == 'data' and type(data) == np.ndarray:
            return np.mean(data) 
        elif data_type == 'path':
            return np.mean(self._get_fits_values(data))
        else:
            raise ValueError(
                f'The choise {data_type} is not matching data type: {type(data)}',
                'Please chosse between data: numpy.ndarray and path: PosixPath')
    
    def _get_fits_max(self, data, data_type='data'): # -> tested
        if data_type == 'data' and type(data) == np.ndarray:
            return np.max(data)
        elif data_type == 'path':
            return np.max(self._get_fits_values(data))
        else:
            raise ValueError(
                 f'The choise {data_type} is not matching data type: {type(data)}',
                'Please chosse between data: numpy.ndarray and path: PosixPath')
    
    def _get_fits_std_dev(self, data, data_type='data'): # -> tested
        if data_type == 'data' and type(data) == np.ndarray:
            return np.std(data)
        elif data_type == 'path' and type(data) == pathlib.PosixPath:
            return np.std(self._get_fits_values(data))
        else:
            raise ValueError(
                f'The choise {data_type} is not matching data type: {type(data)}',
                'Please chosse between data: numpy.ndarray and path: PosixPath')
            
        
        
        
    
        
    

        

class Dark(ImagesSet):

    def __init__ (self,path):
        super().__init__(path)
        self.imtype = 'dark'


class Offset(ImagesSet):
    
    def __init__ (self, path):
        super().__init__()
        self.imtype = 'offset'

        
class Flat(ImagesSet):
    
    def __init__(self, path):
        super().__init__()
        self.imtype = 'flat'


class Light(ImagesSet):
    
    def __init__(self, path):
        super().__init__()
        self.imtpye = 'light'
        
         
