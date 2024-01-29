# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:44:13 2023

@author: Alejandro Gonzalez Ganzabal


ChangeLog
    0.1 (AG): First version.
    0.1.1 (AG): Bug fixing shenanigans
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
    pulses_with_op5 = filter_ddbb.filter_camera_ddbb('Camera', '-O5W')
    pulses_with_op8 = filter_ddbb.filter_camera_ddbb('Camera', '-O8W')

    list_of_exp_5_cameras = ('KLDT-E5WC', 'KLDT-E5WD', 'KLDT-E5WE')
    list_of_exp_8_cameras = ('KL7-E8WB', 'KL8-E8WA')


    # Data for the 5th octant:
    for row in pulses_with_op5.index:
        JPN = pulses_with_op5['Pulse'][row]
        UFO_time = float(pulses_with_op5['Time'][row])
        op_ref = pulses_with_op5['Camera'][row]
        time_range = (UFO_time - 0.5, UFO_time + 0.5)
        for camera in list_of_exp_5_cameras:
            try:
                vid = VVideo(camera, JPN)
            except:
                continue
            vid.load_conf()

            if vid.tvec[-1] <= time_range[0]:
                continue
            else:
                # adds configuration to the dataframe
                tmp_df = {'Pulse': JPN, 'Op.Cam': op_ref, 'Time': UFO_time, 'Exp.Cam' : camera, 'Comments' : pulses_with_op5['Comments'][row]}
                print(tmp_df)
                final_ddbb = final_ddbb.append(tmp_df, ignore_index = True) 

    # Data for the 8th octant:
    for row in pulses_with_op8.index:
        JPN = pulses_with_op8['Pulse'][row]
        UFO_time = float(pulses_with_op8['Time'][row])
        op_ref = pulses_with_op8['Camera'][row]
        time_range = (UFO_time - 0.5, UFO_time + 0.5)
        for camera in list_of_exp_5_cameras:
            try:
                vid = VVideo(camera, JPN)
            except:
                continue
            vid.load_conf()

            if vid.tvec[-1] <= time_range[0]:
                continue
            else:
                # adds configuration to the dataframe
                tmp_df = {'Pulse': JPN, 'Op.Cam': op_ref, 'Time': UFO_time, 'Exp.Cam' : camera, 'Comments' : pulses_with_op8['Comments'][row]}
                print(tmp_df)
                final_ddbb = final_ddbb.append(tmp_df, ignore_index = True)

    return final_ddbb
