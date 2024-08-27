% Alejandro Gonzalez
%
% Retrieves a video stored locally. Structure: camera_JPN.mp4.
%
% Changelog:
%   0.1 (AG): first version

function filePath = retrieve_local_video(name, number, folder)
    % Construct the file name
    fileName = sprintf('%s_%d.mp4', name, number);
    
    % Get the list of files in the folder
    files = dir(fullfile(folder, '*.mp4'));
    
    % Search for the file with the matching name
    for i = 1:numel(files)
        if strcmp(files(i).name, fileName)
            filePath = fullfile(folder, files(i).name);
            return;
        end
    end
    
    % File not found
    filePath = '';
end