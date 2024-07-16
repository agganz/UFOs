% Alejandro Gonzalez
%
% Returns the pixel intensity inside a given box for the wanted image.
%
% Changelog
%   0.1 (AG): first version
%   0.1.1 (AG): fixed bug: boxes not limitted properly.

function mean_int = get_int_in_box(image, box)
    arguments
        image (:, :, 1) % black and white image
        box (1, 4)
    end

    xf = box(1) + box(3);
    yf = box(2) + box(4);
    try
        mean_int = mean(image(box(2) : yf, box(1) : xf), 'all');
    catch
        mean_int = mean(image, 'all');
    end
end
