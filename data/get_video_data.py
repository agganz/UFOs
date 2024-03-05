# Alejandro Gonzalez
# Downloads video from the excel file or csv file.
#
# Changelog:
#       0.1 (AG): First version
#       0.2 (AG): added get_video_from_row


import sys
import os
father_dir = os.path.abspath('..')
sys.path.append(father_dir)
import jet2video

def get_videos(camera_name, pulse_id, time_detect):
    """
    Downloads a video dataframe given the data needed.
    """

    trange = (time_detect - 0.2, time_detect + 0.2)

    output_filename = camera_name + '_' + str(pulse_id) + '.mp4'
    _ = jet2video.export_jet_video(camera_name, pulse_id, output_filename, fps = None, bitrate = 5000, dynamic_clim = True, clim = None, meta = ['jpn','camera','time'], time_range = trange, extract_bkg = True)

    return 1


def get_video_from_row(df, row_number):
    """
    """

    pulse_id = df['Pulse'][row_number]
    camera_name = df['Exp.Cam'][row_number]
    time_detect = df['Time'][row_number]

    get_videos(camera_name, pulse_id, time_detect)
