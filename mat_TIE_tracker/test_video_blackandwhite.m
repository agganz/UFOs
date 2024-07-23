% 0.1 (AG): first version. Now for BW videos.


video_folder = 'E:\JET_cameras\UFO_data';
video_file = 'KLDT-E5WD_104454.mp4';

full_path = fullfile(video_folder, video_file);
vid_obj = VideoReader(full_path);
vid_obj.CurrentTime = 0.0;

n_frame = 0;
vid_out = VideoWriter('demo.avi');
open(vid_out)

while hasFrame(vid_obj)
    n_frame = n_frame + 1;
    disp(strcat('Working on frame: ', num2str(n_frame)))
    vidFrame = readFrame(vid_obj);
    I_bw_simp = vidFrame(:, :, 1);
    I_bw_simp = medfilt2(I_bw_simp); % median blur for noise filtering
    I_bw = cat(3, I_bw_simp, I_bw_simp, I_bw_simp);

    avg_image = mean(I_bw, 'all');
    [bboxes, scores] = detect(acfDetector, clean_image);
    box_idx = zeros(1, size(bboxes, 1));
    boxes_int = zeros(1, size(bboxes, 1));

    if n_frame == 37
        beep
    end

    for i = 1 : size(bboxes, 1)
        mean_int_box = get_int_in_box(I_bw, bboxes(i, :));
        boxes_int(i) = mean_int_box;
    end

    prod_int_scores = boxes_int .* scores';
    box_idx = prod_int_scores > 700;
%     box_idx = box_idx(box_idx > 0);

    bboxes = bboxes(box_idx, :);
    scores = scores(box_idx);
%     [~, scr_idx] = maxk(scores, 3);
%     bboxes = bboxes(scr_idx, :);
%     scores = scores(scr_idx);

    prods_to_use = prod_int_scores(box_idx);
    
    if isempty(scores)
        continue
    end

    annotation = acfDetector.ModelName;
    % I = insertObjectAnnotation(I,'rectangle',bboxes,annotation);
    I_clean = insertText(I_bw, [2, 2], num2str(n_frame));
    I_clean = insertObjectAnnotation(I_clean,'rectangle',bboxes, prods_to_use);
    
    writeVideo(vid_out, I_clean)
end

vid_out.close;
beep