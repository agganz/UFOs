# Plots bars that counts the TIE incident for materials and zones.
# Plot data must be changed manually.
#
# Changelog:
#    0.1 (AG): first version.
#    0.2 (AG): fixed label in zones.
#    0.2.1 (AG): changed the quantity of items.
#    0.2.2 (AG): added mode

import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import math

font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 16}

matplotlib.rc('font', **font)

# other stands for Al + O

material = ["Ti", "W", "Ni", "Mo", 'Other', "Combined", "Unsure"] # before there was CU (0, 0)
disr_materials = [18, 20, 0, 2, 0, 4, 13]
no_disr_materials = [8, 3, 1, 3, 2, 0, 3]
total_data_materials = list(np.array(disr_materials) + np.array(no_disr_materials))

zone = ["UDPT", "IWGL", "UIWP", "NPL", "LH","ILA", "Divertor", "BEION4", "4D", 'ICRH', 'Unsure']
no_disr_zone = [6, 0, 1, 0, 1, 0, 1, 5, 2, 1, 3]
disr_zone = [15, 3, 3, 4, 0, 4, 13, 9, 4, 0, 2]
total_data_zone = list(np.array(disr_zone) + np.array(no_disr_zone))

print('Total data zone:', sum(total_data_zone))
print('Total data materials:', sum(total_data_materials))

def plot_bar(disr, no_disr, labels, x_label, title_plot):
    """
    Plot a bar chart with two sets of data.
    """

    x = np.arange(len(labels))
    width = 0.35

    total_elems = disr + no_disr
    new_y_axis = range(math.floor(min(total_elems)), math.ceil(max(total_elems))+1)

    fig, ax = plt.subplots()
    fig.set_size_inches(9, 8)
    rects1 = ax.bar(x - width/2, disr, width, label='Disruptive', color='tab:red')
    rects2 = ax.bar(x + width/2, no_disr, width, label='Non Disruptive', color="#0072BD")

    ax.set_ylabel('Number of TIEs')
    ax.set_xlabel(x_label)
    ax.set_title(title_plot)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_yticks(new_y_axis)
    ax.legend()

    fig.tight_layout()
    plt.show()

# Example usage
titlemat = 'TIE composition in disruptive and non-disruptive discharges'
xlabelmat = 'TIE composition'

titlezone ='Location of TIEs in disruptive and non-disruptive discharges'
xlabelzone = 'Area in device'

mode = 'zone'
if mode == 'material':
    plot_bar(disr_materials, no_disr_materials, material, xlabelmat, titlemat)
elif mode == 'zone':
    plot_bar(disr_zone, no_disr_zone, zone, xlabelzone, titlezone)
