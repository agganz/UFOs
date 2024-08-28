% Plot speeds.
%
% Changelog
%   0.1 (AG): First version.
%   0.2 (AG): added crosses for missing data.
%   0.2.1 (AG): changed the column of the scfactor.
%   0.2.2 (AG): added more detail to the x legend.
%   0.3 (AG): redone using the ACF scale factor.

hold on
disr_flag = false;
no_disr_flag = false;
disr_no_mes_flag = false;
no_disr_no_mes_flag = false;

for i = 1 : size(datavuv, 1)
    disr_time = datavuv.Disruption(i);
    speed = datavuv.MeasuredSpeed(i);
    speed = speed / datavuv.ACFFactor(i);

    if disr_time == 0
        if speed < 0
            speed = -10;
            if no_disr_no_mes_flag
                scatter(i, speed, 120, 'MarkerEdgeColor', "#0072BD", 'LineWidth', 1, 'MarkerFaceColor', '#2ca02C', 'Marker', 'x', 'HandleVisibility', 'off')
            else
                scatter(i, speed, 120, 'MarkerEdgeColor', "#0072BD", 'LineWidth', 1, 'MarkerFaceColor', '#2ca02C', 'Marker', 'x', 'DisplayName', "Non-Disruptive, can't measure")
                no_disr_no_mes_flag = true;
            end
        else
            if no_disr_flag
                scatter(i, speed, 'MarkerFaceColor', "#0072BD", 'MarkerEdgeColor','#2ca02C', 'HandleVisibility', 'off')
            else
                scatter(i, speed, 'MarkerFaceColor', "#0072BD", 'MarkerEdgeColor','#2ca02C', 'DisplayName', 'Non-disruptive pulse')
                no_disr_flag = true;
            end
        end
    else
        if speed < 0
            speed = -10;
            if disr_no_mes_flag
                scatter(i, speed, 120, 'MarkerFaceColor', '#d62728', 'LineWidth', 1, 'MarkerEdgeColor', '#d62728', 'Marker', 'x', 'HandleVisibility', 'off')
            else
                scatter(i, speed, 120, 'MarkerFaceColor', '#d62728', 'LineWidth', 1, 'MarkerEdgeColor', '#d62728', 'Marker', 'x', 'DisplayName', "Disruptive, can't measure")

                disr_no_mes_flag = true;
            end
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
xlabel('TIE index in reduced dataset', 'Interpreter', 'latex')
ylabel('Normalised TIE speed (m/s)', 'Interpreter', 'latex')
ax = gca;
legend('Interpreter', 'latex')
ax.FontSize = 15;
box on
grid on

hold off