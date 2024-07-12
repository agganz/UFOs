% Alejandro Gonzalez
%
% Checks whether or not two detected boxes might be tracking the same TIE,
% by evaluating their proximity.
%
% Changelog
%   0.1 (AG): first version.
%   0.2 (AG): extracted get_middle_point as a standalone function.

function overlap = overlapBoxMiddlePoint(box1, box2, distance_threshold)
    arguments
        box1 (1, 4) % as [xi, yi, width, height]
        box2 (1, 4)
        distance_threshold double = 6 % minimum distance to consider overlap
    end

    mid_point1 = get_middle_point(box1);
    mid_point2 = get_middle_point(box2);
    distance = pdist([mid_point1 ; mid_point2]);

    if distance < round(distance_threshold)
        overlap = true;
    else
        overlap = false;
    end

end