% Alejandro Gonzalez
% Uses an Aggregate Chanel Feautre detected to find the divertor in each
% video frame to calculate its width in pixels.

% 0.1 (AG): first version.
% 0.1.1 (AG): removed the beeping sound as it was killing me.


function divertor_length = get_divertor_lenght_acf(video_path, acfmodel, NN_denoise)
    arguments
        video_path char
        acfmodel acfObjectDetector
        NN_denoise logical = false
    end
    
    vid_obj = VideoReader(video_path);
    vid_obj.CurrentTime = 0.0;
    
    n_frame = 0;
    vid_out = VideoWriter('demo.avi');
    open(vid_out)
    
    % The +1 is used to overestimate, in case NumFrame return the 'floor'
    % amount of frame rates. It won't matter in the calculation of the
    % divertor size. I just do not feel as adding another while loop.
    
    divertor_sizes = zeros(1, vid_obj.NumFrames + 1);
    
    while hasFrame(vid_obj)
        n_frame = n_frame + 1;
        disp(strcat('Working on frame: ', num2str(n_frame)))
        vidFrame = readFrame(vid_obj);
    
        if NN_denoise
            vidFrame = clean_rgb(vidFrame);
        end
    
        [bboxes, scores] = detect(acfmodel, vidFrame);
        % box_idx = zeros(1, size(bboxes, 1));
        % boxes_int = zeros(1, size(bboxes, 1));
    
    
        % for i = 1 : size(bboxes, 1)
        %     mean_int_box = get_int_in_box(I_bw, bboxes(i, :));
        %     boxes_int(i) = mean_int_box;
        % end
        %
        % prod_int_scores = boxes_int .* scores';
        % box_idx = prod_int_scores > 700;
        %     box_idx = box_idx(box_idx > 0);
    
        % bboxes = bboxes(box_idx, :);
        [~, scr_idx] = maxk(scores, 1);
        bboxes = bboxes(scr_idx, :);
        scores = scores(scr_idx);
    
        % prods_to_use = prod_int_scores(box_idx);
    
        if isempty(scores) || scores(1) < 75
            I_clean = insertText(vidFrame, [2, 2], num2str(n_frame));
            writeVideo(vid_out, I_clean)
            continue
        end
    
        divertor_sizes(n_frame) = bboxes(3);
    
        % I = insertObjectAnnotation(I,'rectangle',bboxes,annotation);
        I_clean = insertText(vidFrame, [2, 2], num2str(n_frame));
        I_clean = insertObjectAnnotation(I_clean,'rectangle',bboxes, scores);
        writeVideo(vid_out, I_clean)
    end
    
    vid_out.close;
    
    divertor_sizes = divertor_sizes(divertor_sizes > 0);
    divertor_length = mean(divertor_sizes);

end