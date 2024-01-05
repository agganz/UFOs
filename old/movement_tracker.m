filename = "KL8-E8WA_101432.mp4";
vidReader = VideoReader(filename);
vidPlayer = vision.DeployableVideoPlayer;

minBlobArea = 5; % Minimum blob size, in pixels, to be considered as a detection
detectorObjects = setupDetectorObjects(minBlobArea);

interestingFrameInds = [150,160,170,330,350,370,Inf];
interestingFrames = cell(1,numel(interestingFrameInds)-1);
ind = 0;
frameCount = 0;
numFrames = vidReader.NumFrames;
bboxes = cell(1,numFrames);
centroids = cell(1,numFrames);

while hasFrame(vidReader)
    % Read a video frame and detect objects in it.
    frame = readFrame(vidReader); % Read frame
    frameCount = frameCount + 1; % Increment frame count
    
    % Detect blocs in the video frame
    [centroids{frameCount}, bboxes{frameCount}] = detectBlobs(detectorObjects, frame);

	% Annotate frame with blobs
    frame = insertShape(frame,"rectangle",bboxes{frameCount}, ...
        Color="magenta",LineWidth=4);

    % Add frame count in the top right corner
    frame = insertText(frame,[0,0],"Frame: "+int2str(frameCount), ...
        BoxColor="black",TextColor="yellow",BoxOpacity=1);

    % Display Video
    step(vidPlayer,frame);

    % Grab interesting frames
    if frameCount == interestingFrameInds(ind+1)
        ind = ind + 1;
        interestingFrames{ind} = frame;
    end
end