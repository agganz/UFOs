# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:44:13 2023

@author: Alejandro Gonzalez Ganzabal


ChangeLog

    0.1 (AG): First version (GIT)
    0.2 (AG): Added pulse search; changed function arguments.
"""

import pandas as pd

def filter_camera_ddbb(fieldname, expr):
    """
    Filters the database found in complete_UFO_ddbb.xlsx and returns the cases 
    for the given camera passed as argument.

    Parameters
    ----------
    camera_code : TYPE
        The camera code to look for. The search is based on Python's contains 
        of the str class. Example: '-O5WB'.

    Returns
    -------
    op_camera_rows : dataframe
        The filtered pandas dataframe

    """
    
    ufo_path = "complete_UFO_ddbb.xlsx"
    UFO_df = pd.read_excel(ufo_path)
    
    if fieldname == 'Camera':
        op_res = UFO_df[UFO_df[fieldname].str.contains(expr)]
    elif fieldname == 'Pulse':
        op_res = UFO_df[UFO_df[fieldname] == expr]
    else:
        print('Cannot find that field')
        
    return op_res
