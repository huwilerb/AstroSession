#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 13:07:58 2021

@author: blaise

Tool to manage all the data of an astrophotography session:
- Fits : create object specifically for darks, offsets flats and lights 
- Guiding stats
- Kstars analyse

"""
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd
import astro_tools
from config import Config

class Session:
    
    CONFIG = Config()
      
    def __init__(self):
        pass

    def set_root(self, root_path):
        self.root = Path(root_path)
    
    def _is_root(self):
        if not hasattr(self, "root"):
            raise NameError('root path for images is missing')
        elif not Path.exists(self.root):
            raise NameError(f'root path for images is wrong: {self.root}')
            
    def _crate_inner(self):
        return(self.Images_Set(self))
    
    def populate_images_sets(self):
        sets = self.config.images_set_types
        sets_path = {set: astro_tools.iter_dir_name(self.root, set) 
                     for set in sets}
        for path in sets_path:
            if sets_path[path] is not None:
                setattr(self, path, self.Images_Set(sets_path[path]))
                
    
    def remove_type(self, type_to_remove):
        if type_to_remove in self.types:
            self.types.remove(type_to_remove)
        else:
            print(f"E: can't remove '{type_to_remove}', this type is not in types")
            print(f'W: The available types are: {self.types}')

    class Images_Set:    
        def __init__(self, path):
            self.config = Session().config
            self.datatype = "image"  
            self.populate_data_image()
            # self.populate_fits_headers()
            # self.solve_data_image()
            
        def populate_data_image(self):
            files = [x for x in self.path.iterdir() if x.is_file()]
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
            headers = self.outer.config.Headers_keys
            for key in headers[self.data.Path[0]]:
                self.data[key] = self.data["Path"].map(self.return_headers(headers, key))
        
        def populate_fits_data(self):
            self.data["Fits"] = self.data.apply(
                lambda row: fits.getdata(row.Path), axis=1)
            self.data["Mean"] = self.data.apply(
                lambda row: np.mean(row.Fits), axis=1)
            self.data["Max"] = self.data.apply(
                lambda row: np.nanmax(row.Fits), axis=1)
            self.data["Min"] = self.data.apply(
                lambda row: np.nanmin(row.Fits), axis=1)
            


    

