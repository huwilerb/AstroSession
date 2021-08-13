#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 19:02:49 2021

@author: fred
"""


import   sys
from     astropy.io          import  fits
import   astroalign          as      aa
import   matplotlib.pyplot   as      plt


from     config              import  config

class Aligner():
    """
    Tool that takes a session and aligns its preprocessed Images_Set
    """
    
    def __init__(self, session):
        self.session = session
            
            
    def _makeName(self, path):
        """ a systematic way of naming the aligned images """
        alignedDir = self.session.root / "registered"
        alignedDir.mkdir(parents=1, exist_ok=1)
        return alignedDir / path.name
        
        
    
    def _checkPreProcessed(self):
        """ Exits if the preprocessing is not complete  """
        try:
            #TODO replace session.light with session.preprocessedlight!
            self.paths = self.session.light.data.Path
        except AttributeError as error:
            print(f"Error: {error}. The preprocessing must first be completed")
            sys.exit()
            
    def _adjustHeader(self, hdu, refpath):
        """ Adds a reminder to the header that the new file has been registered """
        hdu.header['HISTORY'] = f"Aligned to match the data at {refpath}"
        hdu.update_header()
        
        
        
    def _plotAlign(self, image, target):
        """" use for debug """
        fig, axs = plt.subplots(1,2)
        axs[0].imshow(image)
        axs[1].imshow(target)
        plt.waitforbuttonpress()
        
    def align(self, referenceindex=0):
        """
        Aligns the preprocessed stack of images of a Session with respect
        to a reference. The aligned images are saved to a new subdirectory:
            Session.root/registered
        
        TODO: improve the selection of the reference. Can use criteria like
         -- best PSF
         -- largest number of stars of a certain magnitude 

        Parameters
        ----------
        referenceindex : Integer, optional
            DESCRIPTION. Selects the reference image. Default is zero.
        """
        
        # check that the Session has a stack of preprocessed images.
        self._checkPreProcessed()
        
        # explicit the reference to the target image.
        refpath = self.paths[referenceindex]
        ref = fits.getdata(refpath)
        
        # align each image w.r.t. the reference image
        for path in self.paths:
            aligned_hdu = fits.open(path)[0] 
            if path == refpath:
                pass
            else:
                if config.debug:
                    self._plotAlign(aligned_hdu.data, ref)
                aligned_hdu.data, _ = aa.register(aligned_hdu.data, ref)
                
            self._adjustHeader(aligned_hdu, refpath)
            aligned_hdu.writeto(self._makeName(path))
            
            