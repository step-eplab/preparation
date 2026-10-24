#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 18:56:04 2025

@author: fedora
"""


import os
import numpy as np
import pandas as pd

from astropy.coordinates import SkyCoord
import astropy.units as un

from astroquery.vizier import Vizier
import astropy.coordinates as coord

def hms2d(h, m, s):
    H = h + m/60 + s/3600
    return H / 24 * 360

def dms2d(d, m, s):
    if d!=0:
        k = d/abs(d)
    else:
        k=1
    return k * (abs(d) + m/60 + s/3600)

def rd(s):
    x = s.split(' ')
    ra = hms2d(int(x[0]), int(x[1]), float(x[2]))
    dec = dms2d(int(x[3]), int(x[4]), float(x[5]))
    return ra, dec

    return ra, dec

def q_reg(D, alp_min, alp_max, dec_min, dec_max, cols=[]):
    if len(cols)==0:
        ra_c = 'RAJ2000'
        dec_c = 'DEJ2000'
    else:
        ra_c, dec_c = cols
    u = (D[ra_c] > alp_min) & (D[ra_c] < alp_max) & (D[dec_c] > dec_min) & (D[dec_c] < dec_max)
    inx = D.index[u]
    return inx


dir_cat = '/home/catalogs/'
D = pd.read_csv('/home/catalogs/fields.csv')
width = [[2.54, 1.6], [4.97,1.63], [2.66, 1.57], [1.65,1.54], [4.12,1.55]]

cats_long = ['B/gcvs/gcvs_cat', 'B/vsx/vsx',  'II/366/catalog', 
             'J/AcA/62/219/list_var', 'J/ApJS/249/18/table2', 
             'J/ApJS/249/18/table3', 
            'I/358/vclassre', 'J/ApJS/240/16/table4' #'II/328/allwise',
            ]

cats_short = ['GCVS', 'VSX', 'ASAS-SN', 'OGLE-IV', 'ZTFv', 'ZTFsv',  
              'GAIA3v', 'Zhang' #'ALLWISE',  
              ]

Cat1 = dict(zip(cats_long, cats_short))
Cat2 = dict(zip(cats_short, cats_long))

Cats = {}
for cat in cats_long:
    Cats[cat] = pd.DataFrame()

Fields = []
for f in range(1,6): 
    Fields.append(f'F{f}')

Fs = []
for f in Fields:
    F = pd.read_csv(dir_cat + 'GAIA/' + f + '.list', sep=' ', 
                    names=['ra', 'dec', 'mag', 'source_id'], index_col=0)
    Fs.append(F)


f_params = []
for F, d in zip(Fs, width):
    ra_c, dec_c = F['ra'].mean().item(), F['dec'].mean().item()
    ra = [ra_c - d[0], ra_c + d[0]]
    dec = [dec_c - d[1], dec_c + d[1]]

    f_params.append([ra_c, dec_c, d[0], d[1], ra, dec])
    

for ij, params, F in zip(D.index, f_params, Fs):
    f, ra_0_6, dec_0_6 = D.loc[ij, ['Field', 'ra', 'dec']]
    print(f)
    coord_0 = SkyCoord(ra_0_6, dec_0_6, unit=(un.hourangle, un.deg), frame='icrs')    
    
    ra_0, dec_0, d_ra, d_dec, ra, dec = params
    ra_min, ra_max = ra
    dec_min, dec_max = dec
    width = max(d_ra, d_dec)

    v = Vizier(catalog=cats_long, row_limit=40000)
    result = v.query_region(coord.SkyCoord(ra=ra_0, dec=dec_0,
                                            unit=(un.deg, un.deg),
                                            frame='icrs'), 
                                            width=d_ra * un.deg, 
                                            height=d_dec * un.deg)
    cats_win = result.keys()
    
    dir_var = dir_cat + f + '/'
    if not os.path.isdir(dir_var):
        os.mkdir(dir_var)
    

    for cat in cats_win:
        name = Cat1[cat]
        r = result[cat].to_pandas()
        print(r.columns)
        if ~np.isin('RAJ2000', r.columns):
            r['RAJ2000'] = r['RA_ICRS']
            r['DEJ2000'] = r['DE_ICRS']
        if type(r.loc[0, 'RAJ2000'])==str:
            for j in r.index:
                s = r.loc[j, 'RAJ2000'] + ' ' + r.loc[j, 'DEJ2000']
                r.loc[j, ['RAJ2000', 'DEJ2000']] = rd(s) 
            
        r.to_csv(dir_var + name + '.csv', index_label='inx')

    dir_ver1 = dir_var + 'ver1/'
    if not os.path.isdir(dir_ver1):
        os.mkdir(dir_ver1)
    
    for cat in cats_win:
        name = Cat1[cat]
        r = pd.read_csv(dir_var + name + '.csv', index_col='inx')
        r = r.loc[q_reg(r, ra_min, ra_max, dec_min, dec_max)]
        r.to_csv(dir_ver1 + name + '_1.csv', index_label='inx')

    cats_win = []
    files_cat = os.listdir(dir_ver1)
    Cats = {}
    for file in files_cat:
        cat = Cat2[file[:-6]]
        cats_win.append(cat)
        r = pd.read_csv(dir_ver1 + file, index_col='inx')
        Cats[cat] = r
        
    VC = []
    cols=['g_inx', 'cat_id', 'ra', 'dec', 'ro', 'cat']
    Vcat = pd.DataFrame(columns=cols)
    for cat in cats_win:    
        r = Cats[cat]    
        name = Cat1[cat]

        for cat_id in r.index:             
            RA, DEC = r.loc[cat_id, ['RAJ2000', 'DEJ2000']]
            ro = ((F.ra - RA)**2 + (F.dec - DEC)**2)**0.5
            inx_min = np.argmin(ro)
            g_inx = F.index[inx_min] 
    
            R = pd.DataFrame({'g_inx':[g_inx], 'cat_id':[cat_id],
                              'ra':[RA], 'dec':[DEC], 'cat':[name]})
            Vcat = pd.concat((Vcat, R)) # !!!!!! -> [], np.concatenate
        VC.append(r)
    
    Vcat.index = np.arange(len(Vcat))
    Vcat.to_csv(dir_cat + 'Vcat_' + f + '.csv', index_label='inx')




























