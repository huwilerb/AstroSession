#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 13:07:58 2021

@author: blaise

Comparison of fits in a specific folder

"""
import   sys
from     pathlib             import  Path
import   numpy               as      np
import   pandas              as      pd
from     astropy.io          import  fits
import   astroalign          as      aa
import   matplotlib.pyplot   as      plt



import   astro_tools

debug = 0

class Session:
    IMAGES_SET_TYPES =['Dark', 'Light', 'Offset', 'Flat', 'PreprocessedLight', 'Registered']
      
    def __init__(self):
        self.types = []

    def set_root(self, root_path):
        self.root = Path(root_path)
    
    def _is_root(self):
        if not hasattr(self, "root"):
            raise NameError('root path for images is missing')
        elif not Path.exists(self.root):
            raise NameError(f'root path for images is wrong: {self.root}')
                  
    
    def populate_types(self, restricted=[]):
        self._is_root()
        for path in Path(self.root).iterdir():
            numberfiles = len(list(path.glob('*')))
            if numberfiles and path.is_dir() and path.parts[-1] not in restricted:
                self.types.append(path.parts[-1])
                setattr(self, path.parts[-1].lower(), self.Images_Set(path))
                
    
    def remove_type(self, type_to_remove):
        if type_to_remove in self.types:
            self.types.remove(type_to_remove)
        else:
            print(f"E: can't remove '{type_to_remove}', this type is not in types")
            print(f'W: The available types are: {self.types}')

    class Images_Set:    
        def __init__(self, path):
            self.path = path
            self.datatype = "images"  
            self.populate_data_image()
            self.populate_fits_headers()
            
        def populate_data_image(self):
            files = [x for x in self.path.iterdir() if x.is_file()]
            self.number = len(files)
            self.data = pd.DataFrame({'Path': files})
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
                if debug:
                    self._plotAlign(aligned_hdu.data, ref)
                aligned_hdu.data, _ = aa.register(aligned_hdu.data, ref)
                
            self._adjustHeader(aligned_hdu, refpath)
            aligned_hdu.writeto(self._makeName(path))
            
            
    
    
    
    
    

if __name__ == "__main__":
    # main()
    path1 = "/run/media/fred/84a0af0d-182c-45e9-bea9-7fc1fedc8654/home/fred/Blaise/data"
    s1 = Session()
    s1.set_root(path1)
    s1.populate_types(restricted=['process', 'rescaled', 'old', 'misc'])
    
    aligner = Aligner(s1)
    aligner.align()

    
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
    




