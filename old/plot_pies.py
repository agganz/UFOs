# Alejandro Gonzalez
#
# Plotting routine for the pie charts. The data is hardcoded in the script.

import matplotlib
from matplotlib import pyplot as plt
import numpy as np

font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 14 * 1.5}

matplotlib.rc('font', **font)

# other stands for Al + O

material = ["Ti", "W", "Ni", "Mo", 'Other', "Comb.", "NS/NC"] # before there was CU (0, 0)
disr_materials = [18, 20, 0, 2, 0, 4, 13]
no_disr_materials = [8, 3, 1, 3, 2, 0, 3]
total_data_materials = list(np.array(disr_materials) + np.array(no_disr_materials))

zone = ["UDPT", "IWGL", "UIWP", "NPL", "LH","ILA", "Divertor", "BEION4", "4D", 'ICRH', 'NS/NC']
no_disr_zone = [6, 0, 1, 0, 1, 0, 1, 5, 2, 1, 3]
disr_zone = [15, 3, 3, 4, 0, 4, 13, 9, 4, 0, 2]
total_data_zone = list(np.array(disr_zone) + np.array(no_disr_zone))

print('Total data zone:', sum(total_data_zone))
print('Total data materials:', sum(total_data_materials))


def plot_pie_with_legend(labels, values, add_legend = True, cus_title = None, fig_name = 'demo', cut_off_legend = False):
    """
    Plot a pie chart with legend.

    Parameters:
        labels (list): List of labels for the pie chart.
        values (list): List of values for the pie chart.
        add_legend (bool): Flag to add a legend to the figure.
        cus_title (str): Custom title for the figure.
        fig_name (str): Name of the figure.
        cut_off_legend (bool): Flag to remove zero value entries.
    """

    if add_legend and cut_off_legend:
        rm_list = []
        for i in range(len(values)):
            if values[i] == 0:
                rm_list.append(i)

        for index in sorted(rm_list, reverse = True):
            del labels[index]
            del values[index]

    fig, ax = plt.subplots(figsize = (9.5 * 1.5, 8 * 1.5))
    fig.subplots_adjust(left = -0.1, right = 1.1)
    ax.pie(values, shadow = False, autopct = lambda p: "{0}%".format(round(p, 1)) if p > 0 else '', pctdistance = 0.85, colors = plt.cm.tab20.colors)
    fig.suptitle(cus_title, y = 0.9, fontsize = 28)

    if add_legend:
        fig.legend(labels, loc = 'right', fontsize = 22, bbox_to_anchor = (0.8, 0.5))
    
    plt.savefig("{0}.pdf".format(fig_name), format = "pdf", bbox_inches = "tight")


titles = ["TIE materials (total)", "TIE materials for disruptive discharges", "TIE materials for non-disruptive discharges", "TIE sighting areas (total)", "TIE sighting areas for disruptive discharges", "TIE sighting areas for non-disruptive discharges"]
data_pkg = [total_data_materials, disr_materials, no_disr_materials, total_data_zone, disr_zone, no_disr_zone]
label_pck = [material, material, material, zone, zone, zone]
legend_flags = (True, False, False, True, False, False)
fig_names = ["TIE_materials_total", "TIE_materials_disr", "TIE_materials_no_disr", "TIE_zones_total", "TIE_zones_disr", "TIE_zones_no_disr"]

for i in range(len(data_pkg)):
    plot_pie_with_legend(label_pck[i], data_pkg[i], legend_flags[i], cus_title = titles[i], fig_name = fig_names[i])