% Alejandro Gonzalez
% 
% Creates an ACF model for finding the divertor in a video. Data paths are
% hardcoded so I don't kill myself adding them everytime this is called.
%
% Changelog
%   0.1 (AG): first version
%   0.1.1 (AG): added save_as_file
%   0.1.2 (AG): added model_name.

function acfDetector = create_ACF_model_for_divertor(save_as_file, model_name, dist_camera)
    arguments
        save_as_file logical = true
        model_name char = 'acfModel.mat'
        dist_camera logical = true
    end

    if dist_camera
        main_folder = 'E:\JET_cameras\UFO_data\Divertors\ConCamara';
    else
        main_folder = 'E:\JET_cameras\UFO_data\Divertors\Independiente';
    end
    
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
    acfDetector = trainACFObjectDetector(training_dataset,'NegativeSamplesFactor', 6);
    
    if save_as_file
        save(model_name, 'acfDetector')
    end
end