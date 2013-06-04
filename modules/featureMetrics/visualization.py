import numpy as np
import matplotlib.pyplot as plt

def visualize(toConsider, metrics, outputPath):
    bars = []
    labels = []
    for contribution in metrics.keys():
        if contribution in toConsider:
            bars.append(metrics[contribution]['loc'])
            labels.append(contribution)


    fig = plt.figure(num=None)
    width = 0.35

    ind = np.arange(len(bars))
    plt.bar(ind, bars)

    plt.xticks(ind+width/2.0, labels, rotation=30, fontsize='small')
    plt.ylabel('lines of code')
    plt.savefig(outputPath)