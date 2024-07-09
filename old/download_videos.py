import jet2video
import pandas as pd

# Load the data
data = pd.read_excel('data_vuv.xlsx')

jpn_column = data['Pulse']
cameras = data['ExpCam']
times = data['Time']

for i, elem in enumerate(jpn_column):
    time_in = [times[i] - 0.5, times[i] + 0.5]
    exp_cam = cameras[i]
    jpn = jpn_column[i]
    filename = '{}_{}.mp4'.format(exp_cam, jpn_column[i])
    jet2video.export_jet_video(exp_cam, jpn, filename, fps=None,bitrate=5000,dynamic_clim=True,clim=None, meta = ['jpn','camera','time'],time_range = time_in, extract_bkg = True, cmap = 'hsv') 

