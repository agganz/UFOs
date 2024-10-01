% Alejandro Gonzalez
% Plots a 2D histogram with the TIE occurrence for JET zones and
% composition
%
% Changelog
%   0.1 (AG): First version
%   0.1.1 (AG): fixed bug in title
%   0.1.2 (AG): fixed bug in axis names cos apparently I can't read

matrix_in = zeros(7, 11);

for n_row = 1 : size(datavuv, 1)
    material = datavuv.VUVKT2(n_row);
    zone = datavuv.Zone(n_row);
    zone = string(zone);
    material = string(material);


    if contains(zone, 'UDPT')
        j = 1;
    elseif contains(zone, 'IWGL')
        j = 2;
    elseif contains(zone, 'UIWP')
        j = 3;
    elseif contains(zone, 'NPL')
        j = 4;
    elseif contains(zone, 'LH')
        j = 5;
    elseif contains(zone, 'ILA')
        j = 6;
    elseif contains(zone, 'Divertor')
        j = 7;
    elseif contains(zone, 'BEION4')
        j = 8;
    elseif contains(zone, '4D')
        j = 9;
    elseif contains(zone, 'ICRH')
        j = 10;
    else
        j = 11;
    end

    if contains(material, 'Ti')
        i = 1;
    elseif contains(material, 'W')
        i = 2;
    elseif contains(material, 'Ni')
        i = 3;
    elseif contains(material, 'Mo')
        i = 4;
    elseif contains(material, '/') || contains(material, ',')
        i = 6;
    elseif contains(material, '?') || contains(material, 'Nothing')
        i = 7;
    else
        i = 5;
    end
    matrix_in(i,j) = matrix_in(i, j) + 1;
end

ctaxis = 0 : 2 : max(matrix_in, [], 'all');
imagesc(matrix_in)
xticks(1:11)
yticks(1:7)
xticklabels({'UDPT', 'IWGL', 'UIWP', 'NPL', 'LH', 'ILA', 'Div.', 'BEION4', '4D', 'ICRH', 'NS/NC'})
yticklabels({'Ti', 'W', 'Ni', 'Mo', 'Other', 'Comb.', 'NS/NC'})
ax = gca;
ax.FontSize = 15;
xlabel('Area in device', 'Interpreter', 'latex')
ylabel('TIE material', 'Interpreter', 'latex')
title('Distribution of TIEs in device', 'Interpreter', 'latex')
c = colorbar;
c.Label.String = 'Number of TIEs';
c.TickLabelInterpreter = 'latex';
c.Ticks = ctaxis;
box on;
grid on;
c.FontSize = 15;
