% Alejandro Gonzalez
%
% Checks whether or not two detected boxes might be tracking the same TIE,
% by evaluating their proximity.
%
% Changelog
%   0.1 (AG): first version.

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

function mid_point = get_middle_point(box_item)
% Gets the coordinates of the center of a box item, assuming the format is
% [xi, yi, width, height].

    arguments
        box_item (1, 4)
    end

    xi = box_item(1);
    yi = box_item(2);
    xf = xi + box_item(4);
    yf = yi + box_item(3);

    mid_point = [round((xi + xf) / 2), round((yi + yf) / 2)];

end