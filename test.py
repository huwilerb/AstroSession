#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 20:17:24 2021

@author: blaise
"""

from AstroSession import Session
from config import Config
from images import ImagesSet


images = ImagesSet('/home/blaise/Documents/Astro/Astrosession/test/misc_images')
images.populate_data_image()
images.populate_fits_headers()

# session = Session()
# session.set_root('/home/blaise/Documents/Astro/Astrosession/test/misc_images')
# session.populate_images_sets()
# session.darks.populate_fits_headers()

# config = Config()
# config.add_config('test', 'test2')
# config.remove_config('test')

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