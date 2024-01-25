import pandas as pd
from juvil.VVideo import VVideo
import filter_ddbb

def create_ddbb_from_op_cameras(ddbb):
    """
    """
    column_names = ('Pulse', 'Op.Cam', 'Time', 'Exp.Cam', 'Comment')
    final_ddbb = pd.Dataframe(columns = column_names)

    # Select data from operational cameras
    pulses_with_op5 = filter_ddbb.filter_camera_ddbb('Camera', '-O5W')
    pulses_with_op8 = filter_ddbb.filter_camera_ddbb('Camera', '-O8W')

    list_of_exp_5_cameras = ('KLDT-E5WC', 'KLDT-E5WD', 'KLDT-E5WE')
    list_of_exp_8_cameras = ('KL7-E8WB', 'KL8-E8WA')


    # Data for the 5th octant:
    for row in pulses_with_op5:
        JPN = row['Pulse']
        UFO_time = row['Time']
        op_ref = row['Camera']
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
                tmp_df = {'Pulse': JPN, 'Op.Cam': op_ref, 'Time': UFO_time, 'Exp.Cam' : camera, 'Comment' : row['Comment']}
                final_ddbb = final_ddbb.append(tmp_df, ignore_index = True) 

    # Load various metadata

    return final_ddbb