#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 13:07:58 2021

@author: blaise

Comparison of fits in a specific folder

"""
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd
import astro_tools

class AstroSession:
      
    def __init__(self):
        self.types = []
        # self.root = Path('/home/blaise/Pictures/Astro/america/Session 1')
        # self.populate_types(restricted=['process', 'rescaled', 'old'])
       
        
    
    def set_root(self, root_path):
        self.root = Path(root_path)
    
    def _is_root(self):
        if not hasattr(self, "root"):
            raise NameError('root path for images is missing')
        elif not Path.exists(self.root):
            raise NameError(f'root path for images is wrong: {self.root}')
                  
    
    def populate_types(self, restricted =[]):
        self._is_root()
        for path in Path(self.root).iterdir():
            if path.is_dir() and path.parts[-1] not in restricted:
                self.types.append(path.parts[-1])
                setattr(self,path.parts[-1].lower(), self.Images(path))
                
    
    def remove_type(self, type_to_remove):
        if type_to_remove in self.types:
            self.types.remove(type_to_remove)
        else:
            print(f"E: can't remove '{type_to_remove}', this type is not in types")
            print(f'W: The available types are: {self.types}')

    class Images:    
        def __init__(self, path):
            self.path = path
            self.datatype = "images"  
            self.populate_data_image()
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
        
        def populate_fits_headers(self):
            for file in self.data.Path:
                headers = astro_tools.read_fits_header(file)
                for header in headers:
                    self.data[header]= headers[header]
        
        def populate_fits_data(self):
            self.data["Fits"] = self.data.apply(
                lambda row: fits.getdata(row.Path), axis=1)
            self.data["Mean"] = self.data.apply(
                lambda row: np.mean(row.Fits), axis=1)
            self.data["Max"] = self.data.apply(
                lambda row: np.nanmax(row.Fits), axis=1)
            self.data["Min"] = self.data.apply(
                lambda row: np.nanmin(row.Fits), axis=1)
            
def main():
    # s1 = AstroSession()
    # s1.set_root('/home/blaise/Pictures/Astro/america/Session 1')
    # s1.populate_types(restricted=['process', 'rescaled', 'old', 'misc'])
    
    # s2 = AstroSession()
    # s2.set_root('/home/blaise/Pictures/Astro/ZWO294MC_PRO/darks/m10degC/300s')
    # s2.populate_types(restricted=['process', 'rescaled', 'old', 'misc'])
    
    # s_test = AstroSession()
    # s_test.set_root('/home/blaise/Pictures/test_cam/test 2')
    # s_test.populate_types()
    
    # print(s2.lights.data['Mean'][0])
    # print(s_test.lights.data['Mean'][0])
    # print(s_test.darks.data['Mean'][0])
    

    # fig, ax = plt.subplots()
    # ax.plot(s1.darks.data['Mean'], label='darks 5 min')
    # ax.plot(s2.darks.data['Mean'], label='darks 10 min')  
    # ax.set_title(f"Mean pixels values comparison, 5 & 10 minutes")
    # ax.legend()
    # ax.set_xlabel('Image number')
    # ax.set_ylabel('Pixel mean value [ADU]')

    # fig, ax = plt.subplots()
    # darks = (np.mean(s2.darks.data['Mean']), s_test.darks.data['Mean'],
    #             s_test.lights.data['Mean'])
    # names = ('bad dark', '"dark" dark', '"light" dark')
    
    # plt.bar(names, darks)
    # ax.bar(darks,names)
    # # ax.plot(s2.darks.data['Mean'], label='darks mean bad')
    # # ax.plot(s_test.darks.data['Mean'], label='dark dark mean')
    # # ax.plot(s_test.lights.data['Mean'], label='dark lights mean')    
    # ax.set_title(f"Mean pixels values comparison, {s2.root.parts[-1]}")
    # ax.legend()
    # ax.set_xlabel('Image number')
    # ax.set_ylabel('Pixel mean value [ADU]')
    pass
    



main()