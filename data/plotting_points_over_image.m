% Alejandro Gonzalez
%
% Plot TIE original coordinates
%
%

coords = data_table.Initial_pos;
disr_times = data_table.Disruption;
cam = data_table.ExpCam;
velocity = data_table.MeasuredSpeed;
x_array = nan(1, length(coords));
y_array = nan(1, length(coords));

for i = 1 : length(coords)
    elem = coords(i);
    if elem == ""
        continue
    end
    if data_table.ExpCam ~= 'KLDT-E5WD'
        continue
    end
    elem_digits = regexp(elem, '\d+', 'Match');
    x = str2double(elem_digits(1));
    y = str2double(elem_digits(2));
    x_array(i) = y;
    y_array(i) = x;
end

imshow('../EW5D_background_res.PNG');
axis on
hold on;
scatter(x_array, y_array, 'filled', 'red')
hold off

%% Speeds
disr_flag = false;
vel_flag = false;
hold on
for i = 1 : length(disr_times)
    disr_time = disr_times(i);
    speed = velocity(i);
    if isnan(speed)
        continue
    end
    if disr_time == 0
        is_disr = false;
    else
        is_disr = true;
    end

    if is_disr
        if disr_flag
            scatter(i, speed, 'red', 'filled', 'HandleVisibility', 'off');
        else
            scatter(i, speed, 'red', 'filled', 'DisplayName', 'Disruption times')
            disr_flag = true;
        end
    else
        if vel_flag
            scatter(i, speed, 'blue', 'filled', 'HandleVisibility', 'off');
        else
            scatter(i, speed, 'blue', 'filled', 'DisplayName', 'UFO detection time')
            vel_flag = true;
        end
    end
end
hold off