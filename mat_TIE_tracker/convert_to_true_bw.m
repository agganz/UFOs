% Alejandro Gonzalez
%
% Moves a RGB image into a bw grayscale. This does NOT use rgb2gray, as
% this does not change the scalling. This relies on the original image
% being in HSV format to compact the H layer into a new image.
%
% Changelog:
%   0.1 (AG): first version.

function true_bw = convert_to_true_bw(rgb_image)
    arguments
        rgb_image (:, :, 3)
    end

    hsv_image = rgb2hsv(rgb_image);
    true_bw = hsv_image(:,:,1);
end