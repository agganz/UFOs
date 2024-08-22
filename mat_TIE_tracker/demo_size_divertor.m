video_path = 'E:\JET_cameras\UFO_data\KLDT-E5WD_99340.mp4';
J1 = imread('E:\JET_cameras\UFO_data\divertor_cut.png');
J2 = imread('E:\JET_cameras\UFO_data\divertor_cut2.png');
J3 = imread('E:\JET_cameras\UFO_data\divertor_cut3.png');
J4 = imread('E:\JET_cameras\UFO_data\divertor_cut4.png');

J1_bw = convert_to_true_bw(J);
J2_bw = convert_to_true_bw(J2);
J3_bw = convert_to_true_bw(J3);
J4_bw = convert_to_true_bw(J4);

video = VideoReader(video_path);

% Iterate through each frame

while hasFrame(video)
    % Read the current frame
    I = readFrame(video);
    I_bw = convert_to_true_bw(I);
    
    %     single_frame = single(frame);
    c3 = normxcorr2(J3_bw, I_bw);
    c1 = normxcorr2(J1_bw, I_bw);
    c2 = normxcorr2(J2_bw, I_bw);
    c4 = normxcorr2(J4_bw, I_bw);
    [refrows, refcols] = size(I_bw);
    c1 = imresize(c1, [refrows, refcols]);
    c2 = imresize(c2, [refrows, refcols]);
    c3 = imresize(c3, [refrows, refcols]);
    c4 = imresize(c4, [refrows, refcols]);

    c = c1 + c2 + c3 + c4 / 4;
    [ypeak,xpeak] = find(c==max(c(:)));
    disp(['Point: ', num2str(ypeak), ',', num2str(xpeak)])
    yoffSet = ypeak-size(J4,1);
    xoffSet = xpeak-size(J4,2);
    hold on
    imshow(c)
    drawrectangle(gca,'Position',[xoffSet,yoffSet,size(J1,2),size(J1, 1)], ...
    'FaceAlpha',0);
    hold off

end