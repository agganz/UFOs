# Alejandro Gonzalez
# Downloads videos from jet2video in mp4 according to UFO appearance time.
#
# Changelog
#    0.1 (AG): first version.
#    0.2 (AG): fixed bug in unreachable times.

import sys
sys.path.append('..')
import jet2video
import pandas as pd

# Load the data
data = pd.read_excel('../data/data_vuv.xlsx')

jpn_column = data['Pulse']
cameras = data['ExpCam']
times = data['Time']

for i in range(len(jpn_column)):
    time_in = [times[i] - 0.5, times[i] + 0.5]
    exp_cam = cameras[i]
    jpn = jpn_column[i]
    filename = '{}_{}.mp4'.format(exp_cam, jpn_column[i])
    try:
        jet2video.export_jet_video(exp_cam, jpn, filename, fps=None,bitrate=5000,dynamic_clim=True,clim=None, meta = ['jpn','camera','time'],time_range = time_in, extract_bkg = True, cmap = 'hsv') 
    except IndexError:
        continue 
