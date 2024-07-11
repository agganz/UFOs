% Alejandro Gonzalez
% 
% Train model detector.
%
% Changelog
%   0.1 (AG): first version

function acfDetector = train_retrieve_model
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
end