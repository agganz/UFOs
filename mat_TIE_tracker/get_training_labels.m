% Alejandro Gonzalez
% Creates table for training


%% Test to see if it works
acfDetector = train_retrieve_model();

%% Preprocessing
I = imread('KL8-E8WA_1014324_402.png');
clean_image = clean_rgb(I);
I_bw = convert_to_true_bw(I);
I_bw = medfilt2(I_bw);

avg_image = mean(I_bw, 'all');
[bboxes, scores] = detect(acfDetector, clean_image);
% bboxes_clean = detect(acfDetector, clean_image);
box_idx = zeros(1, size(bboxes, 1));

for i = 1 : size(bboxes, 1)
    mean_int_box = get_int_in_box(I_bw, bboxes(i, :));
    if mean_int_box > avg_image
        box_idx(i) = i;
    end
end

box_idx = box_idx(box_idx > 0);
bboxes = bboxes(box_idx, :);

%% Show boxes
annotation = acfDetector.ModelName;
% I = insertObjectAnnotation(I,'rectangle',bboxes,annotation);
I_clean = insertObjectAnnotation(clean_image,'rectangle',bboxes, annotation);

% figure(1)
% imshow(I)
figure(2)
imshow(I_clean)
