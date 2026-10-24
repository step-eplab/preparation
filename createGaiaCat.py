#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 12:43:46 2026

@author: fedora
"""

import os
import json

from astropy import units as un
from astropy.coordinates import SkyCoord
from astropy.io import fits

from astroquery.gaia import Gaia


config_name_paths = '../paths_F5.json'   

with open(config_name_paths, 'r') as file:
    configs_paths = json.load(file)
dir_configs = configs_paths['dir_configs']
dir_cat = configs_paths['dir_cat']
cat_name = configs_paths['cat_name']
catalog_path = dir_cat + cat_name

Gaia.ROW_LIMIT = -1
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"

config_name = dir_configs + 'create_cat.json'

with open(config_name, 'r') as file:
    configs = json.load(file)   
ra = configs['ra']
dec = configs['dec']


cat0_path = dir_cat + 'image-radec.fits'
if os.path.isfile(cat0_path):
    with fits.open(cat0_path) as f:
        cat0 = f[1].data
    d_ra = 1.2 * (max(cat0.ra) - min(cat0.ra))
    d_dec = 1.2 * (max(cat0.dec) - min(cat0.dec))
else:
    d_ra = configs['d_ra']
    d_dec = configs['d_dec']
    

width =  d_ra * un.deg
height =  d_dec * un.deg

coord_0 = SkyCoord(ra * un.deg, dec * un.deg, frame='icrs')

print(f'request {[ra, d_ra.item(), dec, d_dec.item()]}')
input()
r = Gaia.query_object_async(coordinate=coord_0, width=width, height=height,
                       columns = ['source_id',
                                  'ra',
                                  'dec',
                                  'phot_g_mean_mag',
                                  ])

GAIA = r.to_pandas()
GAIA = GAIA[['ra','dec','phot_g_mean_mag','source_id']]
GAIA.to_csv(catalog_path, encoding='ascii', index_label='g_inx', sep=' ', header=None)



'''
import matplotlib.pyplot as plt
F = pd.read_csv(catalog_path, sep=' ', names=['ra', 'dec', 'mag', 'source_id'])
plt.plot(F.ra, F.dec, '.')

plt.plot(GAIA.ra, GAIA.dec, '.')
plt.plot(cat0.ra, cat0.dec, '.')

'''




