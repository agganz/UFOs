% Alejandro Gonzalez
% Creates table for training

%% Training data part
main_folder = 'E:\JET_cameras\UFO_data';

filelist = dir(strcat(main_folder, '\*.mat'));

for i = 1 : length(filelist)
    filename = filelist(i).name;
    full_path = fullfile(main_folder, filename);
    gt = load(full_path, 'gTruth');
    gt = gt.gTruth;
    truths(i) = gt;
end

%% Training the model
training_dataset = objectDetectorTrainingData(truths);
acfDetector = trainACFObjectDetector(training_dataset,'NegativeSamplesFactor', 5);

%% Test to see if it works

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
