% Plot speeds.
%
% Changelog
%   0.1 (AG): First version.
%   0.2 (AG): added crosses for missing data.
%   0.2.1 (AG): changed the column of the scfactor.

hold on
disr_flag = false;
no_disr_flag = false;

for i = 1 : size(datavuv, 1)
    disr_time = datavuv.Disruption(i);
    speed = datavuv.MeasuredSpeed(i);
    speed = speed / datavuv.ScFactor(i);

    if disr_time == 0
        if speed < 0
            scatter(i, speed, 120, 'MarkerEdgeColor', '#2ca02C', 'LineWidth', 1, 'MarkerFaceColor', '#2ca02C', 'Marker', 'x', 'HandleVisibility', 'off')
        else
            if no_disr_flag
                scatter(i, speed, 'MarkerFaceColor', "#2ca02C", 'MarkerEdgeColor','#2ca02C', 'HandleVisibility', 'off')
            else
                scatter(i, speed, 'MarkerFaceColor', "#2ca02C", 'MarkerEdgeColor','#2ca02C', 'DisplayName', 'Non-disruptive pulse')
                no_disr_flag = true;
            end
        end
    else
        if speed < 0
            scatter(i, speed, 120, 'MarkerFaceColor', '#d62728', 'LineWidth', 1, 'MarkerEdgeColor', '#d62728', 'Marker', 'x', 'HandleVisibility', 'off')
        else
            if disr_flag
                scatter(i, speed, 'MarkerFaceColor', "#d62728", 'MarkerEdgeColor', '#d62728', 'HandleVisibility', 'off')
            else
                scatter(i, speed, 'MarkerFaceColor', "#d62728", 'MarkerEdgeColor', '#d62728', 'DisplayName', 'Disruptive pulse')
                disr_flag = true;
            end
        end
    end
end

yline(0, 'k', 'HandleVisibility', 'off')

title('Normalised TIE speeds', 'Interpreter', 'latex')
xlabel('TIE in reduced dataset', 'Interpreter', 'latex')
ylabel('Normalised TIE speed ($s^{-1} pix^{-1})$', 'Interpreter', 'latex')
ax = gca;
legend('Interpreter', 'latex')
ax.FontSize = 15;
box on
grid on

hold off