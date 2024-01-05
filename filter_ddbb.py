# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:44:13 2023

@author: Alejandro Gonzalez Ganzabal


ChangeLog

    V.- 0.1 (AG): First version (GIT)
"""

import pandas as pd

def filter_camera_ddbb(camera_code):
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
    
    ufo_path = r"C:\Users\Doctorando1\Documents\UFOs\data\complete_UFO_ddbb.xlsx"
    UFO_df = pd.read_excel(ufo_path)
    
    op_camera_rows = UFO_df[UFO_df['Camera'].str.contains(camera_code)]
    
    return op_camera_rows