# Changelog

# Note that this script was taken from S. Silburn. These changes have been done by Alejandro Gonzlaez (AG). Thus, the first modified version will be noted as 1.1.

# 1.1 (AG): now it returns vid.tvec[start_frame : end_frame]
# 1.2 (AG): Added one last frame to the returned time to ensure everything is captured.
# 1.3 (AG): added background extraction via function argument.
# 1.4 (AG): solved a bug in which an empty video would be created if the time range did not match


import os
import time
import datetime

import matplotlib.animation as manimation
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import numpy as np

# Uses Valentina Huber's JUVIL library
from juvil.VVideo import VVideo


def export_jet_video(camera,pulse,output_filename,fps=None,bitrate=5000,dynamic_clim=True,clim=None, meta = ['jpn','camera','time'],time_range=None, extract_bkg = False):
    '''
    Write out a JET pulse video as an MP4 file.

    Parameters:

        camera (str)           : JET Camera name


        pulse (int)            : JET pulse number

        output_filename (str) : The mp4 output file.

        fps (float)           : Frames-per-second for output video. If not given, \
                                it will be set such that the video plays back in real-time, \
                                or 60fps, whichever is lower.

        bitrate (int)         : Bit rate for output

        dynamic_clim (bool)   : Whether to dynamically adjust the brightness \
                                for each frame (default).

        clim (sequence)       : If not using dynamic_clim, the minimum and maximum \
                                digital level to use for colour scaling of the output. \
                                If not given and dynamic_clim = False, the full range \
                                of the camera will be used.

        meta (list)           : List of metadata fields to overlay in the bottom \
                                left of the output video. It seems the only ones I've implemented are \
                                'time', 'jpn' and 'camera'
    '''
    #if not os.path.exists(plt.rcParams['animation.ffmpeg_path']):
    #    raise Exception('Path to ffmpeg executable not set correctly. Please specify the path to ffmpeg using set_ffmpeg_path(path) before running ipx_to_mp4().')

    # Load the video
    vid = VVideo(camera,pulse)

    # Load various metadata
    vid.load_conf()

    # Background subtration if available / appropriate
    bg = False
    if vid.alpha_comments is None or extract_bkg:
        bg = True
    elif 'average' not in vid.alpha_comments.lower():
        bg = True

    if fps is None:
        fps = min(60,1./vid.tstep)

    if output_filename is None:
        output_filename = '{:s}_{:d}.mp4'.format(camera.upper(),pulse)

    # Start and end times
    n_frames = vid.nframes
    if time_range is None:
        start_frame = 0
        end_frame = n_frames - 1
    else:
        if vid.tvec[-1] <= time_range[0]:
            raise IndexError('The initial value for the time range is larger than the recording time.')
        else:
            start_frame = np.argmin(np.abs(time_range[0] - vid.tvec))
            end_frame = np.argmin(np.abs(time_range[1] - vid.tvec))

    # Bits per pixel (vid object stores it as bytes per pixel)
    bitdepth = vid.bitdepth * 8

    # First frame
    im0 = vid.get_frame_at(0).get_processed_data()

    if 'time' in meta:
        timestamp = True
        meta.remove('time')

    im_size = im0.shape[:2]

    if not dynamic_clim and clim is None:
        clim = [0,2**bitdepth - 1]
    elif dynamic_clim:
        clim = [im0.min(),im0.max()]

    fig = plt.figure(figsize=(im_size[1]/100.,im_size[0]/100.),dpi=100)
    im = plt.imshow(im0,cmap='gray',clim=clim)

    if timestamp or metastamp:
        timestamp = AnchoredText('Overlay stamp',loc=3,prop={'color':'w','fontsize':10})
        timestamp.patch.set_facecolor('k')
        timestamp.patch.set_alpha(0.2)
        plt.gca().add_artist(timestamp)


    plt.axis('off')
    plt.subplots_adjust(left=0,right=1,bottom=0,top=1)

    writer = manimation.FFMpegWriter(fps=fps, bitrate=bitrate)

    looplog = LoopProgPrinter()
    update_time = 0
    print('\n---------------------------\nJET Video mp4 Writer\n---------------------------')
    print('Output to: {:s}\n'.format(os.path.abspath(output_filename)))

    metastamp = ''
    if len(meta) > 0:
        for metaname in meta:
            if metaname.lower() == 'jpn':
                metastamp = metastamp + 'JET Pulse {:d}\n'.format(pulse)
            elif metaname.lower() == 'camera':
                metastamp = metastamp + 'Camera: {:s}\n'.format(camera.upper())
            else:
                print('Requested metadata "{:s}" not recognised and will be omitted.'.format(metaname))
    print(' ' )
    with writer.saving(fig, output_filename,dpi=100):

        for frame_num in range(start_frame,end_frame):

            fr = vid.get_frame_at(frame_num).get_processed_data(subbgr=bg)

            im.set_data(fr)

            if dynamic_clim:
                im.set_clim([fr.min(),fr.max()])

            if timestamp or metastamp:
                overlay_txt = metastamp
                if timestamp:
                    overlay_txt = overlay_txt + 'T = {:.3f} s'.format(vid.tvec[frame_num] - 40)

                timestamp.txt.set_text('')

            writer.grab_frame()

            if time.time() - update_time > 2:
                looplog.update( float(frame_num+1)/n_frames )

    looplog.update(1.)
    print(' ')
    
    return vid.tvec[start_frame : end_frame + 1]


def get_framerate(camera, pulse):
    """
    Returns the frame rate of a given video. Assumes constant
    framerate and it's obtained substracting the two initial times.

    Parameters:
    -----------
    camera : str
        Noramlsied camera name.
    pulse : int
        JPN
    """

    vid = VVideo(camera,pulse)

    # Load various metadata
    vid.load_conf()

    framerate = vid.tvec[1] - vid.tvec[0]
    return framerate


def set_ffmpeg_path(ffmpeg_path):
    '''
    Convenience function to configure matplotlib.
    Tells matplotlib where to find the ffmpeg executable.

    Parameters:

        ffmpeg_path (str): Path to the ffmpeg executable.
    '''
    if os.path.isfile(ffmpeg_path):
        plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path
    else:
        raise FileNotFoundError('Specified ffmpeg executable "{:s}" not found.'.format(ffmpeg_path))


class LoopProgPrinter:
    '''
    A little object for telling the user how a long,
    loopy calculation is progressing, using stdout.

    Includes simple time to completion prediction.
    '''
    def __init__(self):

        self.starttime = None
        self.startdatetime = None
        self.frac_done = 0.

        # Config parameters
        self.wait_time = 5
        self.min_remaining_length = 5
        self.start_printed = False
        self.end_printed = False


    def update(self,status):

        if status is None:
            return

        try:
            float(status)
            self.frac_done = status
            if self.starttime is None:
                self.starttime = time.time()
                self.startdatetime = datetime.datetime.now()
        except (TypeError, ValueError):
            print(status)
            return


        elapsed_time = time.time() - self.starttime

        if elapsed_time > self.wait_time and not self.start_printed and self.frac_done > 0:

                est_time = (elapsed_time / self.frac_done)

                if est_time - elapsed_time > self.min_remaining_length:
                    est_time_string = ''
                    if est_time > 3600:
                        est_time_string = est_time_string + '{:.0f} hr '.format(np.floor(est_time/3600))
                    if est_time > 600:
                        est_time_string = est_time_string + '{:.0f} min.'.format((est_time - 3600*np.floor(est_time/3600))/60)
                    elif est_time > 59:
                        est_time_string = est_time_string + '{:.0f} min {:.0f} sec.'.format(np.floor(est_time/60),est_time % 60)
                    else:
                        est_time_string ='{:.0f} sec.'.format(est_time)
                    print(self.startdatetime.strftime('Started on:         %Y-%m-%d at %H:%M:%S'))
                    print('Estimated duration: {:s}'.format(est_time_string))

                    self.start_printed = True

        elif self.frac_done == 1. and not self.end_printed:

            tot_time = time.time() - self.starttime
            time_string = ''
            if tot_time > 3600:
                time_string = time_string + '{:.0f} hr '.format(np.floor(tot_time / 3600))
            if tot_time >= 59:
                time_string = time_string + '{:.0f} min '.format(np.floor( (tot_time - 3600*np.floor(tot_time / 3600))  / 60))
            time_string = time_string + '{:.0f} sec. '.format( tot_time - 60*np.floor(tot_time / 60) )
            print('Completed in:       {:s}'.format(time_string))


            self.end_printed = True



if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description="JET video writer tool")
    parser.add_argument("-p","-P", dest="jpn", type=int, help="JET pulse number", metavar="PULSE", required=True)
    parser.add_argument("-c","-cam", dest="cam", help="JET camera name", required=True)
    parser.add_argument("-o", dest="outfname", default=None, help="Output video file name")
    parser.add_argument("-t", "-time", dest="timerange", default=None, help="Time range in seconds in the format <start>,<end>")
    args=parser.parse_args()


    if args.timerange is not None:
        trange = [float(args.timerange.split(',')[0]),float(args.timerange.split(',')[1])]
    else:
        trange=None
    export_jet_video(args.cam, args.jpn, args.outfname,time_range=trange)

