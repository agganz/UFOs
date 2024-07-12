% Alejandro Gonzalez
%
% Gets the middle point of a box.
% Changelog:
%   0.1 (AG): first version. Taken from overlapBoxMiddlePoint.

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