% Alejandro Gonzalez
% 801-11-1980
% Checks the overlapping of two 2D boxes given their coordinates and sizes.
%
% Changelog
%   0.1 (AG): first version. Still to be tested.


function overlap = checkOverlap(box1, box2)
    % Extract coordinates of box1
    x1 = box1(1);
    y1 = box1(2);
    width1 = box1(3);
    height1 = box1(4);
    
    % Extract coordinates of box2
    x2 = box2(1);
    y2 = box2(2);
    width2 = box2(3);
    height2 = box2(4);
    
    % Calculate the coordinates of the corners of box1
    x1_min = x1;
    x1_max = x1 + width1;
    y1_min = y1;
    y1_max = y1 + height1;
    
    % Calculate the coordinates of the corners of box2
    x2_min = x2;
    x2_max = x2 + width2;
    y2_min = y2;
    y2_max = y2 + height2;
    
    % Check if the boxes overlap
    if (x1_min <= x2_max && x1_max >= x2_min && y1_min <= y2_max && y1_max >= y2_min)
        overlap = true;
    else
        overlap = false;
    end
end