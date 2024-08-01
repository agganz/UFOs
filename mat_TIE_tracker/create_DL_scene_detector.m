% Alejandro Gonzalez
% Creates a Depp Learning model for scene detector with JET videos. Paths
% are hardcoded.
%
% Highly recommended to run train_retrieve_scenes to create the label
% folders. For moving from video to png frames, run saveVideoFramesAsPNG.m
%
% Changelog:
%   0.1 (AG): first version.

folderName = 'E:\JET_cameras\UFO_data\Scenes\saved_scenes\';

imds = imageDatastore(folderName, ...
    IncludeSubfolders=true, ...
    LabelSource="foldernames");

classNames = categories(imds.Labels);

numClasses = numel(categories(imds.Labels));
[imdsTrain,imdsValidation,imdsTest] = splitEachLabel(imds,0.7,0.15,"randomized");

net = imagePretrainedNetwork("squeezenet", NumClasses = numClasses);
inputSize = net.Layers(1).InputSize;

net = setLearnRateFactor(net,"conv10/Weights",10);
net = setLearnRateFactor(net,"conv10/Bias",10);

pixelRange = [-30 30];

imageAugmenter = imageDataAugmenter( ...
    RandXReflection=true, ...
    RandXTranslation=pixelRange, ...
    RandYTranslation=pixelRange);

augimdsTrain = augmentedImageDatastore(inputSize(1:2),imdsTrain, ...
    DataAugmentation=imageAugmenter);

augimdsValidation = augmentedImageDatastore(inputSize(1:2),imdsValidation);
augimdsTest = augmentedImageDatastore(inputSize(1:2),imdsTest);

options = trainingOptions("adam", ...
    ValidationData = augimdsValidation, ...
    ValidationFrequency = 5, ...
    Plots = "training-progress", ...
    Metrics = "accuracy", ...
    MaxEpochs = 16, ...
    Verbose = false);

net = trainnet(augimdsTrain, net, "crossentropy", options);
YTest = minibatchpredict(net,augimdsTest);
YTest = scores2label(YTest,classNames);
TTest = imdsTest.Labels;
acc = mean(TTest==YTest);

% analyzeNetwork(net);