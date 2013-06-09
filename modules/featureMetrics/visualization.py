import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt


def visualize(toConsider, metrics, outputPath):
    bars = []
    labels = []
    for contribution in metrics.keys():
        if contribution in toConsider:
            bars.append(metrics[contribution]['loc'])
            labels.append(contribution)

    fig = plt.figure()
    width = 0.35

    ind = np.arange(len(bars))
    plt.bar(ind, bars)
    plt.subplots_adjust(bottom=0.30)
    plt.xticks(ind+width/2.0, labels, rotation=90, fontsize='small')
    plt.ylabel('lines of code')
    plt.title('Contributions of the same featureset compared by lines of code')
    plt.savefig(outputPath)