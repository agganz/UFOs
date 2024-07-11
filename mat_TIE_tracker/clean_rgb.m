% Alejandro Gonzlez
%
% Takes a RGB image and denoises it using a denoise neural network that
% takes one colour layer at a time.
%
% Changelog
%   0.1 (AG): first version

function clean_image = clean_rgb(image)
    arguments
        image (:, :, 3)
    end

    [noisyR,noisyG,noisyB] = imsplit(image);
    net = denoisingNetwork("dncnn");
    denoisedR = denoiseImage(noisyR,net);
    denoisedG = denoiseImage(noisyG,net);
    denoisedB = denoiseImage(noisyB,net);
    clean_image = cat(3,denoisedR,denoisedG,denoisedB);
end