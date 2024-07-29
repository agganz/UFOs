% Alejandro Gonzalez
% 
% Train model detector. The data path is hardcoded.
%
% Changelog
%   0.1 (AG): first version
%   0.1.1 (AG): added save_as_file
%   0.1.2 (AG): added model_name.

function acfDetector = train_retrieve_model(save_as_file, model_name)
    arguments
        save_as_file logical = true
        model_name char = 'acfModel.mat'
    end

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
    acfDetector = trainACFObjectDetector(training_dataset,'NegativeSamplesFactor', 5, 'ObjectTrainingSize', [50, 50]);
    
    if save_as_file
        save(model_name, 'acfDetector')
    end
end