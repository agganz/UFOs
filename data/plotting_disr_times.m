% Alejandro Gonzalez
% Basic plot util to check the timing of the disruption 
% and the UFO.
%
% If the dataset changes, so does the input function.
%
% TODO: use velocities as well when I get them.
%
% Changelog:
%	0.1 (AG): first version.
%   0.2 (AG): new plots with better labeling
%   0.2.1 (AG): updated labels

data_table = importfile('clean_edited_5th_8th.csv');
unique_pulses = unique(data_table.Pulse);
total_pulses = length(unique_pulses);
list_disr_time = zeros(1, length(unique_pulses));

% tiledlayout(2,1)
% Top plot
% nexttile
hold on
count_no_disr = 0;
disr_flag = false;
ufo_flag = false;

for i = 1 : length(unique_pulses)
    jpn = unique_pulses(i);
    row_ind = find(data_table.Pulse == jpn);
    row_ind = row_ind(1);
    disr_time = data_table.Disruption(row_ind);
    if disr_time == 0
        count_no_disr = count_no_disr + 1;
        list_disr_time(i) = NaN;
        continue
    end
    ufo_time = data_table.Time(row_ind);
    if ufo_time > 70
        continue
    end
    list_disr_time(i) = ufo_time - disr_time; % negative number = UFO prior to disruption
    if disr_flag
        scatter(i, disr_time, 'red', 'filled', 'HandleVisibility', 'off');
    else
        scatter(i, disr_time, 'red', 'filled', 'DisplayName', 'Disruption times')
        disr_flag = true;
    end
    if ufo_flag
        scatter(i, ufo_time, 'blue', 'filled', 'HandleVisibility', 'off');
    else
        scatter(i, ufo_time, 'blue', 'filled', 'DisplayName', 'UFO detection time')
        ufo_flag = true;
    end
end

xlim([1, length(unique_pulses)])

legend()
hold off
ylabel('Time (s)')
xlabel('Pulse counter')
title('Time of TIE and disruption occurrences', 'Interpreter', 'latex')
% nexttile
% Comparing times
close all;

datavuv = importvuv('data_vuv.xlsx');
unique_vuv_pulses = unique(datavuv.Pulses);

scatter(1 : length(list_disr_time), list_disr_time, 'filled', 'HandleVisibility', 'off')
msg1 = strcat("Pulsos con disrupciones: ", num2str(total_pulses - count_no_disr));
disp(msg1)
disp(strcat("Total pulses: ", num2str(total_pulses)))
xlim([1, length(unique_pulses)])
ylabel('$t_{TIE} - t_{disruption}$ (s)', 'Interpreter', 'latex')
yregion(-0.5, 0.5,'FaceColor','g','EdgeColor','k', 'DisplayName', "$\pm$0.5 seconds discrepancy")
xlabel('Pulse counter', 'Interpreter', 'latex')
title('Time difference between TIE and disruption', 'Interpreter', 'latex')
legend('Interpreter', 'latex')
set(gca,'FontSize',13);



function cleanedited5th8th = importfile(filename, dataLines)
%IMPORTFILE Import data from a text file
%  CLEANEDITED5TH8TH = IMPORTFILE(FILENAME) reads data from text file
%  FILENAME for the default selection.  Returns the data as a table.
%
%  CLEANEDITED5TH8TH = IMPORTFILE(FILE, DATALINES) reads data for the
%  specified row interval(s) of text file FILENAME. Specify DATALINES as
%  a positive scalar integer or a N-by-2 array of positive scalar
%  integers for dis-contiguous row intervals.
%
%  Example:
%  cleanedited5th8th = importfile("C:\Users\Doctorando1\Documents\UFOs\data\clean_edited_5th_8th.csv", [2, Inf]);
%
%  See also READTABLE.
%
% Auto-generated by MATLAB on 03-Apr-2024 17:16:40

%% Input handling

% If dataLines is not specified, define defaults
if nargin < 2
    dataLines = [2, Inf];
end

%% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 11);

% Specify range and delimiter
opts.DataLines = dataLines;
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["VarName1", "Pulse", "OpCam", "Time", "ExpCam", "Disruption", "Comments", "MeasuredSpeed", "Comments_personal", "Initial_pos", "VarName11"];
opts.VariableTypes = ["double", "double", "double", "double", "categorical", "double", "categorical", "double", "string", "string", "string"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Specify variable properties
opts = setvaropts(opts, ["Comments_personal", "Initial_pos", "VarName11"], "WhitespaceRule", "preserve");
opts = setvaropts(opts, ["ExpCam", "Comments", "Comments_personal", "Initial_pos", "VarName11"], "EmptyFieldRule", "auto");
opts = setvaropts(opts, "OpCam", "TrimNonNumeric", true);
opts = setvaropts(opts, "OpCam", "ThousandsSeparator", ",");

% Import the data
cleanedited5th8th = readtable(filename, opts);

end

function datavuv = importvuv(workbookFile, sheetName, dataLines)
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
% Auto-generated by MATLAB on 05-Apr-2024 14:28:58

%% Input handling

% If no sheet is specified, read first sheet
if nargin == 1 || isempty(sheetName)
    sheetName = 1;
end

% If row start and end points are not specified, define defaults
if nargin <= 2
    dataLines = [2, Inf];
end

%% Set up the Import Options and import the data
opts = spreadsheetImportOptions("NumVariables", 12);

% Specify sheet and range
opts.Sheet = sheetName;
opts.DataRange = dataLines(1, :);

% Specify column names and types
opts.VariableNames = ["VarName1", "Pulse", "OpCam", "Time", "ExpCam", "Disruption", "Comments", "MeasuredSpeed", "Comments_personal", "Initial_pos", "VUVKT2", "VUVComment"];
opts.VariableTypes = ["double", "double", "double", "double", "categorical", "double", "string", "double", "string", "string", "categorical", "string"];

% Specify variable properties
opts = setvaropts(opts, ["Comments", "Comments_personal", "Initial_pos", "VUVComment"], "WhitespaceRule", "preserve");
opts = setvaropts(opts, ["ExpCam", "Comments", "Comments_personal", "Initial_pos", "VUVKT2", "VUVComment"], "EmptyFieldRule", "auto");

% Import the data
datavuv = readtable(workbookFile, opts, "UseExcel", false);

for idx = 2:size(dataLines, 1)
    opts.DataRange = dataLines(idx, :);
    tb = readtable(workbookFile, opts, "UseExcel", false);
    datavuv = [datavuv; tb]; %#ok<AGROW>
end

end