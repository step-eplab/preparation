#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 12:43:46 2026

@author: fedora
"""

import json
from astropy import units as un
from astropy.coordinates import SkyCoord

from astroquery.gaia import Gaia

Gaia.ROW_LIMIT = -1
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"


config_name = 'main.json'
config_name_paths = '../paths.json'   

with open(config_name, 'r') as file:
    configs = json.load(file)   
ra = configs['ra']
dec = configs['dec']
d_ra = configs['d_ra']
d_dec = configs['d_dec']
mag_min = configs['mag_min']
max_max = configs['max_max']
name = configs['name']

with open(config_name_paths, 'r') as file:
    configs_paths = json.load(file)
catalog_path = configs['catalog_path']

width =  d_ra * un.deg
height =  d_dec * un.deg

coord_0 = SkyCoord(ra * un.deg, dec * un.deg, frame='icrs')

r = Gaia.query_object_async(coordinate=coord_0, width=width, height=height,
                       columns = ['source_id',
                                  'ra',
                                  'dec',
                                  'phot_g_mean_mag',
                                  ])

GAIA = r.to_pandas()
GAIA = GAIA[['ra','dec','phot_g_mean_mag','source_id']]
GAIA.to_csv(catalog_path, encoding='ascii', index_label='g_inx', sep=' ', header=None)
