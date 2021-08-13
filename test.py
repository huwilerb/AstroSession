#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 20:17:24 2021

@author: blaise
"""

from AstroSession import Session

session = Session()
session.set_root('/home/blaise/Pictures/Astro/M81')
session.populate_types()
session.darks.populate_fits_headers()
print(session.darks.data.columns)
