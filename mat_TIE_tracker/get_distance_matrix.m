% Alejandro Gonzalez
%
% Calculates a m*n Euclidean distance matrix between the list of boxes from
% two different frames. The lists are sized m and n.
%
% Changelog:
%   0.1 (AG): first version.

function distance_matrix = get_distance_matrix(first_frame, second_frame)
    arguments
        first_frame (:, 4)
        second_frame(:, 4)
    end

    distance_matrix = zeros(size(first_frame, 1), size(second_frame, 1));

    for i = 1 : size(first_frame, 1)
        first_frame_box = first_frame(i, :);
        first_box_mid = get_middle_point(first_frame_box);
        for j = 1 : size(second_frame, 1)
            second_frame_box = second_frame(j, :);
            second_box_mid = get_middle_point(second_frame_box);
            distance_ij = round(pdist([first_box_mid ; second_box_mid]));
            distance_matrix(i,j) = distance_ij;
        end
    end
end
            
            