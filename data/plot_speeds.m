% Plot speeds.
%
% Changelog
%   0.1 (AG): First version.

hold on

for i = 1 : size(datavuv, 1)
    disr_time = datavuv.Disruption(i);
    speed = datavuv.MeasuredSpeed(i);
    if datavuv.ExpCam == "KLDT-E5WD"
        speed = speed / (322 * 416);
    else
        speed = speed / datavuv.Sc_Factor;
    end

    if disr_time == 0
        bar(i, speed, 'FaceColor', "#2ca02C ")
    else
        bar(i, speed, 'FaceColor',"#d62728")
    end
end

box on
grid on

hold off