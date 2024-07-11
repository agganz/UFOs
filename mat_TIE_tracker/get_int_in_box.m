% Alejandro Gonzalez
%
% Returns the pixel intensity inside a given box for the wanted image.
%
% Changelog
%   0.1 (AG): first version

function mean_int = get_int_in_box(image, box)
    arguments
        image (:, :, 1) % black and white image
        box (1, 4)
    end

    xf = box(1) + box(4);
    yf = box(2) + box(3);
    mean_int = mean(image(box(2) : yf, box(1) : xf), 'all');
end