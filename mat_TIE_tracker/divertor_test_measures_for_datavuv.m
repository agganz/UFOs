% GETS the divertor distance for all cameras in data_vuv.xlsx. 
% 0.1 (AG): first and hopefully last version.

datavuv = importdatavuv('../data/data_vuv.xlsx');

if ~exist('acfmodel', 'var')
    acfmodel = create_ACF_model_for_divertor(false, '', false);
end

div_size = zeros(size(datavuv, 1), 1);
differences_in_dist = div_size;

for i = 1 : size(datavuv, 1)
    disp(['Row: ', num2str(i)])
    camera = datavuv.ExpCam(i);
    JPN = datavuv.Pulse(i);
    video_folder = 'E:\JET_cameras\UFO_data';
    video_path = retrieve_local_video(camera, JPN, video_folder);
    div_size(i) = get_divertor_lenght_acf(video_path ,acfmodel, false);
    differences_in_dist(i) = (div_size(i) - datavuv.DistanceMeasured(i)) / datavuv.DistanceMeasured(i);
end


function datavuv = importdatavuv(workbookFile, sheetName, dataLines)
%IMPORTFILE Import data from a spreadsheet
%  DATAVUV = IMPORTFILE(FILE) reads data from the first worksheet in the
%  Microsoft Excel spreadsheet file named FILE.  Returns the data as a
%  table.
%
%  DATAVUV = IMPORTFILE(FILE, SHEET) reads from the specified worksheet.
%
%  DATAVUV = IMPORTFILE(FILE, SHEET, DATALINES) reads from the specified
%  worksheet for the specified row interval(s). Specify DATALINES as a
%  positive scalar integer or a N-by-2 array of positive scalar integers
%  for dis-contiguous row intervals.
%
%  Example:
%  datavuv = importfile("C:\Users\Doctorando1\Documents\UFOs\data\data_vuv.xlsx", "Sheet1", [2, Inf]);
%
%  See also READTABLE.
%
% Auto-generated by MATLAB on 27-Aug-2024 14:49:32

%% Input handling

% If no sheet is specified, read from Sheet1
if nargin == 1 || isempty(sheetName)
    sheetName = "Sheet1";
end

% If row start and end points are not specified, define defaults
if nargin <= 2
    dataLines = [2, Inf];
end

%% Set up the Import Options and import the data
opts = spreadsheetImportOptions("NumVariables", 20);

% Specify sheet and range
opts.Sheet = sheetName;
opts.DataRange = dataLines(1, :);

% Specify column names and types
opts.VariableNames = ["VarName1", "Pulse", "OpCam", "Time", "ExpCam", "Disruption", "Comments", "MeasuredSpeed", "Comments_personal", "Initial_pos", "VUVKT2", "VUVComment", "Zone", "Observed", "TotRes", "CameraFilter", "STDSpeed", "OldScaledFactor", "ScFactor", "DistanceMeasured"];
opts.VariableTypes = ["double", "double", "double", "double", "categorical", "double", "string", "double", "string", "string", "categorical", "categorical", "categorical", "categorical", "double", "categorical", "double", "double", "double", "double"];

% Specify variable properties
opts = setvaropts(opts, ["Comments", "Comments_personal", "Initial_pos"], "WhitespaceRule", "preserve");
opts = setvaropts(opts, ["ExpCam", "Comments", "Comments_personal", "Initial_pos", "VUVKT2", "VUVComment", "Zone", "Observed", "CameraFilter"], "EmptyFieldRule", "auto");

% Import the data
datavuv = readtable(workbookFile, opts, "UseExcel", false);

for idx = 2:size(dataLines, 1)
    opts.DataRange = dataLines(idx, :);
    tb = readtable(workbookFile, opts, "UseExcel", false);
    datavuv = [datavuv; tb]; %#ok<AGROW>
end

end