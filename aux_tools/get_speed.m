% Alejandro Gonzalez
%
% Calculates the mean speed of a set of points given the (x, y) coordinates
% and the time interval.
%
% Changelog
%   0.1 (AG): First version


function mean_vel = get_speed(x, y, frame_rate)

vel = zeros(1, length(x));
    for i = 1 : length(x) - 1
        current = [x(i), y(i)];
        next = [x(i + 1), y(i + 1)];
        distance = pdist([current; next]);
        speed = distance / frame_rate;
        vel(i) = speed;
    end
    mean_vel = mean(speed);
end
