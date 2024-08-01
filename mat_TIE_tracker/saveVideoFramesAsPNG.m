% Alejandro Gonzalez
%
% Divides a given video (from the given path) into its frames, saved in the
% same folder. Absolute path is much recommended.
%
% Changelog
%   0.1 (AG): first version.

function saveVideoFramesAsPNG(videoPath)
    % Read the video
    video = VideoReader(videoPath);
    
    % Create the output folder
    [outputFolder, video_name] = fileparts(videoPath);
    video_name_no_format = video_name(1:end-4);

    % Iterate through each frame
    frameCount = 1;
    while hasFrame(video)
        % Read the current frame
        frame = readFrame(video);
        
        % Save the frame as a PNG
        outputFileName = sprintf('frame_%04d.png', frameCount);
        outputFileName = strcat(video_name_no_format, '_', outputFileName);
        outputFilePath = fullfile(outputFolder, outputFileName);
        imwrite(frame, outputFilePath);
        
        % Increment the frame count
        frameCount = frameCount + 1;
    end
    
    disp('All frames saved as PNG.');
end