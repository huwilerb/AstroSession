from astropy.io import fits
from pathlib import Path
import json

p = Path('U:\Hb_499001\Python\Misc_Tools')

file_name = 'test.fits'

file = fits.open(p.joinpath(file_name))

# for hdu in file:
#     for header in hdu.header :
#         print(f'{hdu}, {header}:  {hdu.header[header]}')


h = {str(i): str(file[0].header[i]) for i in file[0].header}



with open(p.joinpath('headers_dict.json'), 'w') as outfile:
    json.dump(h, outfile, indent=4)

