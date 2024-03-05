# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:44:13 2023

@author: Alejandro Gonzalez Ganzabal


ChangeLog
    0.1 (AG): First version.
    0.1.1 (AG): Bug fixing shenanigans
    0.1.2 (AG): added two extra experimental cameras
    0.1.3 (AG): bug fixing checking the 8th octant
    0.2 (AG): fixed a bug related to the time vector max value.
"""

import pandas as pd
from juvil.VVideo import VVideo
import filter_ddbb

def create_ddbb_from_op_cameras():
    """
    Creates a complete dataframe with the video information for experimental cameras
    by evaluating UFOs in operational cameras, making sure that the data is present
    in both the file system in the server and in the same time range.

    Returns:

    final_ddbb : pd.Dataframe
        The final dataframe.
    """

    column_names = ('Pulse', 'Op.Cam', 'Time', 'Exp.Cam', 'Comments')
    final_ddbb = pd.DataFrame(columns = column_names)

    # Select data from operational cameras
    pulses_with_op5 = filter_ddbb.filter_expresion('Camera', '-O5W')
    pulses_with_op8 = filter_ddbb.filter_expresion('Camera', '-O8W')

    list_of_exp_5_cameras = ('KLDT-E5WC', 'KLDT-E5WD', 'KLDT-E5WE')
    list_of_exp_8_cameras = ('KL7-E8WB', 'KL8-E8WA', 'KL8-E8WC', 'KL8-E8WB')


    # Data for the 5th octant:
    for row in pulses_with_op5.index:
        JPN = pulses_with_op5['Pulse'][row]
        UFO_time = float(pulses_with_op5['Time'][row])
        op_ref = pulses_with_op5['Camera'][row]
        time_range = (UFO_time - 0.2, UFO_time + 0.2)
        for camera in list_of_exp_5_cameras:
            try:
                vid = VVideo(camera, JPN)
            except:
                continue
            vid.load_conf()
            try:
                if vid.tvec[0] <= time_range[0] and time_range[1] <= vid.tvec[1]:
                    continue
                else:
                # adds configuration to the dataframe
                    tmp_df = {'Pulse': JPN, 'Op.Cam': op_ref, 'Time': UFO_time, 'Exp.Cam' : camera, 'Comments' : pulses_with_op5['Comments'][row]}
                    final_ddbb = final_ddbb.append(tmp_df, ignore_index = True) 
            except IndexError:
                print('Problem with the time vector from JUVIL.')
                continue
    # Data for the 8th octant:
    for row in pulses_with_op8.index:
        JPN = pulses_with_op8['Pulse'][row]
        UFO_time = float(pulses_with_op8['Time'][row])
        op_ref = pulses_with_op8['Camera'][row]
        time_range = (UFO_time - 0.5, UFO_time + 0.5)
        for camera in list_of_exp_8_cameras:
            try:
                vid = VVideo(camera, JPN)
            except:
                continue
            vid.load_conf()
            try:
                if vid.tvec[0] <= time_range[0] and vid.tvec[1] <= time_range[1]:
                    continue
                else:
                    # adds configuration to the dataframe
                    tmp_df = {'Pulse': JPN, 'Op.Cam': op_ref, 'Time': UFO_time, 'Exp.Cam' : camera, 'Comments' : pulses_with_op8['Comments'][row]}
                    print(tmp_df)
                    final_ddbb = final_ddbb.append(tmp_df, ignore_index = True)
            except IndexError:
                print('Problem with original time vecotr.')
                continue
    # reverse search
    
    exp_df8 = filter_ddbb.filter_expresion('Camera', '-E8W')
    exp_df5 = filter_ddbb.filter_expresion('Camera', '-E5W')
    for ind in exp_df8.index:
        tmp_df = {'Pulse': exp_df8['Pulse'][ind], 'Op.Cam': 'KL1-O8WA', 'Time': exp_df8['Time'][ind], 'Exp.Cam' : exp_df8['Camera'][ind], 'Comments' : exp_df8['Comments'][ind]}
        final_ddbb = final_ddbb.append(tmp_df, ignore_index = True)
    for ind in exp_df5.index:
        tmp_df = {'Pulse': exp_df5['Pulse'][ind], 'Op.Cam': 'KLDT-O5WB', 'Time': exp_df5['Time'][ind], 'Exp.Cam' : exp_df5['Camera'][ind], 'Comments' : exp_df5['Comments'][ind]}
        final_ddbb = final_ddbb.append(tmp_df, ignore_index = True)


    return final_ddbb
