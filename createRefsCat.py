#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 19:06:25 2026

@author: fedora
"""

import os
import sys    
import json
import pandas as pd
import numpy as np

from funcs import readConfig

def calcRo(g_inx, Cat):
    d_ra = Cat.ra - Cat.loc[g_inx, 'ra']
    d_dec = Cat.dec - Cat.loc[g_inx, 'dec']
    ro = (d_ra**2 + d_dec**2)**0.5
    ro.loc[g_inx] = 1
    return ro

def run(field, cat_path, save_path, mag_st_min, mag_st_max, mag_low, mag_high,  G_var = []):
    F = pd.read_csv(cat_path, sep=' ', names=['ra', 'dec', 'mag', 'source_id'], index_col=0)
    print(G_var)
    #### cut by mags
    u_mag = (F.mag < mag_st_max) & (F.mag > mag_st_min)
    St_inx = F[u_mag].index
    St = pd.DataFrame(index=St_inx)
    
    #### drop Vars
    #G_var = [] # !TODO
    St = St[~np.isin(St.index, G_var)]
    #### add min distance
    mag_0 = F.mag.min()
    
    # only bright star
    u_high = F.mag < mag_high
    # without bright and faint stars
    u_mid = (F.mag < mag_low) & (~u_high)
    
    print('calc min distance')
    print('len(St) = ' + str(len(St)))
    for i, g_inx in enumerate(St.index):
        mag = F.loc[g_inx, 'mag']
    
        ro = calcRo(g_inx, F) 
        ro_min = np.min(ro)
        ro_min_mid = np.min(ro[u_mid])
    
        if sum(u_high)==0:
            u_mag_high = F.mag <= mag_0
            ro_min_high = np.min(ro[u_mag_high])
        else:
            ro_min_high = np.min(ro[u_high])
        if mag==mag_0:
            ro_min_high = 0
    
        St.loc[g_inx, ['ro_min', 'ro_min_mid', 'ro_min_high']] = ro_min, ro_min_mid, ro_min_high
    
        if i%10==0:
            print(i, end=', ')
    print()
    print('len Refs = ' + str(len(St)))
    
    St.to_csv(save_path + f'Refs_{field}.csv', float_format='%.6f')


if len(sys.argv)>1:
    config_name_paths = sys.argv[1]
else:
    config_name_paths = '../configs/paths_F5.json'
#############################################################
# Preparation
#############################################################
#### read configs
dir_configs, dir_vars, dir_cat, cat_name = readConfig(config_name_paths, 
                                                      keys=['dir_configs', 'dir_vars',
                                                            'dir_cat', 'cat_name'])
config_name = dir_configs + 'createRefsCat.json'
Vcat_name, index_col, mag_st_max, mag_st_min, mag_high, mag_low = readConfig(config_name)

vars_path = dir_vars + Vcat_name

if os.path.isfile(vars_path):
    V = pd.read_csv(vars_path, index_col=0)
    G_var = V[index_col].values
else:
    G_var = []

catalog_path = dir_cat + cat_name
field = cat_name[:-5]

run(field, catalog_path, dir_cat, mag_st_min, mag_st_max, mag_low, mag_high, G_var)




















