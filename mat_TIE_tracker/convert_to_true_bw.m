% Alejandro Gonzalez
%
% Moves a RGB image into a bw grayscale. This does NOT use rgb2gray, as
% this does not change the scalling. This relies on the original image
% being in HSV format to compact the H layer into a new image.
%
% Changelog:
%   0.1 (AG): first version.
%   0.2 (AG): now it uses uint8 format.

function true_bw = convert_to_true_bw(rgb_image)
    arguments
        rgb_image (:, :, 3)
    end

    hsv_image = rgb2hsv(rgb_image);
    true_bw = round(hsv_image(:,:,1) .* 256);
    true_bw = uint8(true_bw);

    % Some processing:
    true_bw = (true_bw - mean(true_bw, 'all')) * 2;
end