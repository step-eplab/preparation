#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 20:02:26 2024

@author: fedora
"""

import json

def readConfig(config_name, keys=[], save_path=''):
    print(f'Read: {config_name}')
    with open(config_name, 'r') as file:
        configs = json.load(file)

    if keys==[]:
        keys = configs.keys()

    V = []
    for k in keys:
        V.append(configs[k])

    return V