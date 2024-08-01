% Alejandro Gonzalez
%
% Classifies a video given the video path.
%
% Changelog
%   0.1 (AG): First verison.

function video_label = get_label_from_video(video_path, net, disp_hist)

arguments
    video_path char
    net dlnetwork
    disp_hist logical = false
end

folderName = 'E:\JET_cameras\UFO_data\Scenes\saved_scenes\';

imds = imageDatastore(folderName, ...
    IncludeSubfolders=true, ...
    LabelSource="foldernames");

classNames = categories(imds.Labels);

label_count = zeros(1, numel(classNames));
video = VideoReader(video_path);

% Iterate through each frame

while hasFrame(video)
    % Read the current frame
    frame = readFrame(video);
    single_frame = single(frame);
    predicted_results = predict(net, single_frame);
    label = scores2label(predicted_results, classNames);
    idx_label = findStringPosition(classNames, label);
    label_count(idx_label) = label_count(idx_label) + 1;
end

[~, video_label_idx] = max(label_count);
video_label = classNames{video_label_idx};

if disp_hist
    histogram(label_count);
end
end


function position = findStringPosition(cellArray, searchString)
for i = 1:numel(cellArray)
    if strcmp(cellArray{i}, string(searchString))
        position = i;
        break
    end
end
end