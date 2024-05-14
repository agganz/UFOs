import matplotlib
#matplotlib.use('TkAgg',force=True)
from matplotlib import pyplot as plt
#print("Switched to:",matplotlib.get_backend())

font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 14}

matplotlib.rc('font', **font)

material = ["Ti", "W", "Cu", "Ni", "Mo", "O", "Al", "Combined", "Undefined"]
disr_materials = [18, 19, 0, 0, 2, 0, 0, 4, 14]
no_disr_materials = [4, 2, 0, 1, 1, 1, 1, 0, 2]

zone = ["UDPT", "IWGL", "UIWP", "NPL", "LH","ILA", "Divertor", "BEION", "4D", 'ICRH', 'NA']
no_disr_zone = [4, 0, 1, 0, 1, 0, 1, 1, 1, 1, 3]
disr_zone = [14, 3, 3, 4, 1, 4, 13, 8, 4, 0, 3]

def plot_pie_with_legend(labels, values):
    """
    Plot a pie chart with legend
    """

    rm_list = []
    for i in range(len(values)):
        if values[i] == 0:
            rm_list.append(i)

    for index in sorted(rm_list, reverse = True):
        del labels[index]
        del values[index]

    fig, ax = plt.subplots(figsize=(9.5, 8))
    fig.subplots_adjust(left = 0, right = 1)
    ax.pie(values, labels = labels, shadow = False, autopct = '%1.1f%%', pctdistance = 0.85)
    fig.suptitle('Material distribution in disruptive discharges', y = 0.9)
    fig.legend(labels, loc='right', fontsize = 13, bbox_to_anchor = (0.8, 0.5))

    plt.show()

plot_pie_with_legend(material, disr_materials)