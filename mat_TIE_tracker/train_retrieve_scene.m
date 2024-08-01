% Alejandro Gonzalez
% 
% Train scene detector.
%
% Changelog
%   0.1 (AG): first version
%   0.2 (AG): changed purpose. Now creates ordered files with gTruths.


function train_retrieve_scene()

    main_folder = 'E:\JET_cameras\UFO_data\Scenes';
    
    filelist = dir(strcat(main_folder, '\*.mat'));
    
    for i = 1 : length(filelist)
        filename = filelist(i).name;
        full_path = fullfile(main_folder, filename);
        gt = load(full_path, 'gTruth');
        gt = gt.gTruth;
        truths(i) = gt;
    end
    
    
    scenes_folder = 'E:\JET_cameras\UFO_data\Scenes\saved_scenes';
    [~, sceneLabels] = sceneTimeRanges(truths);

    groundTruthFolder = main_folder;
    trainingFolder = scenes_folder;

    extractVideoScenes(groundTruthFolder,trainingFolder, sceneLabels);
    
end

function extractVideoScenes(groundTruthFolder,trainingFolder,classes)
% If the video scenes are already extracted, no need to download
% the data set and extract video scenes.
if isfolder(trainingFolder)
    classFolders = fullfile(trainingFolder,string(classes));
    allClassFoldersFound = true;
    for ii = 1:numel(classFolders)
        if ~isfolder(classFolders(ii))
            allClassFoldersFound = false;
            break;
        end
    end
    if allClassFoldersFound
        return;
    end
end
if ~isfolder(groundTruthFolder)
    mkdir(groundTruthFolder);
end
downloadURL = "https://ssd.mathworks.com/supportfiles/vision/data/videoClipsAndSceneLabels.zip";

filename = fullfile(groundTruthFolder,"videoClipsAndSceneLabels.zip");
if ~exist(filename,'file')
    disp("Downloading the video clips and the corresponding scene labels to " + groundTruthFolder);
    websave(filename,downloadURL);    
end
% Unzip the contents to the download folder.
unzip(filename,groundTruthFolder);
labelDataFiles = dir(fullfile(groundTruthFolder,"*_labelData.mat"));
labelDataFiles = fullfile(groundTruthFolder,{labelDataFiles.name}');
numGtruth = numel(labelDataFiles);
% Load the label data information and create ground truth objects.
gTruth = groundTruth.empty(numGtruth,0);
for ii = 1:numGtruth
    ld = load(labelDataFiles{ii});
    videoFilename = fullfile(groundTruthFolder,ld.videoFilename);
    gds = groundTruthDataSource(videoFilename);
    gTruth(ii) = groundTruth(gds,ld.labelDefs,ld.labelData);
end
% Gather all the scene time ranges and the corresponding scene labels 
% using the sceneTimeRanges function.
[timeRanges, sceneLabels] = sceneTimeRanges(gTruth);
% Specify the subfolder names for each duration as the scene label names. 
foldernames = sceneLabels;
% Delete the folder if it already exists.
if isfolder(trainingFolder)
    rmdir(trainingFolder,'s');
end
% Video files are written to the folders specified by the folderNames input.
writeVideoScenes(gTruth,timeRanges,trainingFolder,foldernames);
end
