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

import astro_tools
from config import Config

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
        
    def return_headers(self, headers, key):
        return {path:headers[path][key] for path in headers}
        
    def populate_fits_headers(self):
        headers = {path:astro_tools.read_fits_header(path) for path in self.data.Path}
        for key in headers[self.data.Path[0]]:
            self.data[key] = self.data["Path"].map(self.return_headers(headers,
                                                                       key))
    
    def images_statistics(self, ratio = 0.2, min =10):
        dataset_len = self.data.shape[0]
        
        if dataset_len < min:
            analysis_len = dataset_len
            analysis_type = 'full'
            self.analysis_type = analysis_type #to remove
        elif dataset_len*ratio < min:
            analysis_len = dataset_len
            analsis_type = 'full'
            self.analysis_type = analysis_type #to remove
        else:
            analysis_len = dataset_len
            analysis_type = 'statistical'
            self.analysis_type = analysis_type #to remove
        
        if analysis_type == 'full':
            pass
        
    def _get_fits_values(self, path): #to test
        data = fits.getdata(path)
        return data
    
    def _get_fits_mean(self, data, data_type='data'): #to test
        if data_type == 'data':
            return np.max(data)
        elif data_type == 'path':
            return np.max(self._get_fits_values(data))
        else:
            raise ValueError(
                f'The choise {data_type} is not availble. Available choises: data, path')
    
    def _get_fits_mean(self, data, data_type='data'): # to test
        if data_type == 'data':
            return np.max(data)
        elif data_type == 'path':
            return np.max(self._get_fits_values(data))
        else:
            raise ValueError(
                f'The choise {data_type} is not availble. Available choises: data, path')
        
    
        
    

        

class Dark(ImagesSet):

    def __init__ (self,path):
        super().__init__()
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
        
         
