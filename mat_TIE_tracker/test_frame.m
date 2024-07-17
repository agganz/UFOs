function change_scale_from_float_to_bw(image)
    arguments
        image (:, :, 1)
    end

        I_bw = convert_to_true_bw(vidFrame);
    I_bw = medfilt2(I_bw); % median blur for noise filtering

    avg_image = mean(I_bw, 'all');
    [bboxes, scores] = detect(acfDetector, clean_image);
    box_idx = zeros(1, size(bboxes, 1));

    for i = 1 : size(bboxes, 1)
        if scores(i) < 50
            continue
        end
        mean_int_box = get_int_in_box(I_bw, bboxes(i, :));
        if mean_int_box > avg_image + 0.25 * avg_image
            box_idx(i) = i;
        end
    end

    box_idx = box_idx(box_idx > 0);
    bboxes = bboxes(box_idx, :);
    scores = scores(box_idx);
    [~, scr_idx] = maxk(scores, 3);
    bboxes = bboxes(scr_idx, :);
    scores = scores(scr_idx);
    
    if isempty(scores)
        continue
    end

    annotation = acfDetector.ModelName;
    % I = insertObjectAnnotation(I,'rectangle',bboxes,annotation);
    I_clean = insertText(I_bw, [2, 2], num2str(n_frame));
    I_clean = insertObjectAnnotation(I_clean,'rectangle',bboxes, scores);
    
    writeVideo(vid_out, I_clean)
end