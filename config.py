#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 14:13:09 2021

@author: blaise
"""

from pathlib import Path
import json

class Config:
    """
    Configuration object for AstroSession project
    """
    
    def __init__(self):
        self.__dir = Path.cwd()
        self.__config_file_name ='config.json'
        self.__get_config()
        
        
    
    def __get_config(self):
        """
        generate the config from the json file

        """
        data = self.__read_config()
        for x in data:
            setattr(self, x, data[x])
    
    def __read_config(self):
        """
        Read the data from the json config file

        Returns
        -------
        data : dict
            dictionnary with all the parameters in the config.json file

        """
        with open(self.__dir.joinpath(self.__config_file_name), 'r') as f:
            data = json.load(f)
        return data
    
    
    def __write_config(self, data):
        """
        Write into the json config file
        input:
            data: dictionnary with the key and values of the config file -> dict
        """
        with open(self.__dir.joinpath(self.__config_file_name),'w') as f:
            json.dump(data, f)
            
    
    def __add_config(self, key, value):
        """
        Add a new entry to the configuration file

        Parameters
        ----------
        key : string
            key name of the new configuration 
        value : sting/list
            value of the new configuration

        Returns
        -------
        None.

        """
        try:            
            data = self.__read_config()
            data[key]=value
            self.__write_config(data)
            success= True
        except:
            print(f'Impossible to add {key} to the config file. ')
            success = False
        
        if success:
            self.__get_config()      
             
    def __remove_config(self, key):
        """
        remove one specific key from the configuration file

        Parameters
        ----------
        key : string
            key to remove from the json file

        Returns
        -------
        None.

        """
        try:
            data = self.__read_config()
            data.pop(key, None)
            self.__write_config(data)
            success = True
        
        except:
            print(f'Impossible to remove {key} from the config file. ')
            success = False
            
        if success:
            self.__dict__.pop(key, None)
            
            
            

    
        

        