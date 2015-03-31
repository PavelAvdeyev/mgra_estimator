from boomslang import *

import Configure as conf

def prepare_unique_datasets(tools, results):
    name_labels = []
    vals = [[[], [], []] for _ in range(len(tools))]
    min_y = 101.0

    for key, infos in results.items():
        _, genes, rear, _ = key
        name = "(" + str(5 * genes) + "," + str(rear) + ")"
        name_labels.append(name)

        for i in range(len(tools)):
            TP, FN, FP = infos[i]

            vals[i][0].append(TP)
            vals[i][1].append(FN)
            vals[i][2].append(FP)

            if min_y > TP:
                min_y = TP

    return name_labels, vals, min_y


def draw_clustered_stacked_histigram(filename, name_labels, vals, min_y, name_y, number_tools):
    """
    Draw clustered stacked graphic with any tools
    """
    hatches = ['/', '-', '\\', '.', ',', '//', '\\\\', '+', 'o']
    colors = ['lightgreen', 'steelblue', 'red']
    labels = ['True Positive', 'False Negative', 'False Positive']

    cluster = ClusteredBars()
    for i in range(number_tools):
        stack = StackedBars()
        for j in range(3):
            bar = Bar()
            bar.xValues = range(len(vals[i][j]))
            bar.yValues = vals[i][j]
            bar.hatch = hatches[i]
            bar.color = colors[j]
            bar.label = labels[j]
            stack.add(bar)

        cluster.add(stack)

    cluster.spacing = 1.5
    cluster.xTickLabels = name_labels
    cluster.xTickLabelProperties = {
        'fontsize': 8,
        'horizontalalignment': 'left',
        'rotation': 340
    }

    plot = Plot()
    plot.setYFormatter((lambda s, pos: str(int(s)) + "%"))
    plot.axesLabelSize = 12
    plot.xLabel = "Simulated datasets"
    plot.yLabel = name_y
    plot.yLimits = (min_y - 3, 100)
    plot.add(cluster)
    plot.save(filename)


def draw_clustered_histogram(filename, results):
    """
    Draw clustered graphic with three tools
    """

    labels = ['MGRA2', 'PMAG+', 'GapAdj', 'GASTS']
    colors = ['lightgreen', 'steelblue', 'red', 'yellow', 'grey']

    my_name_labels = []
    for key, _ in results.items():
        _, genes, rear, _ = key
        name = "(" + str(5 * genes) + "," + str(rear) + ")"
        my_name_labels.append(name)

    min_y = 10000
    max_y = 0
    yVals = [[] for _ in range(len(conf.tools))]
    for _, infos in results.items():
        for i in range(len(conf.tools)):
            yVals[i].append(infos[i])

        if min_y > min(infos):
            min_y = min(infos)

        if max_y < max(infos):
            max_y = max(infos)

    cluster = ClusteredBars()
    for i in range(len(conf.tools)):
        bar = Bar()
        bar.xValues = range(len(yVals[i]))
        bar.yValues = yVals[i]
        bar.color = colors[i]
        bar.label = labels[i]
        cluster.add(bar)

    cluster.spacing = 1.0
    cluster.xTickLabels = my_name_labels
    cluster.xTickLabelProperties = {
        'fontsize': 8,
        'horizontalalignment': 'left',
        'rotation': 340
    }

    plot = Plot()
    plot.axesLabelSize = 12
    plot.xLabel = "Simulated datasets"
    plot.yLabel = "Distance"
    plot.yLimits = (min_y - 3, max_y + 3)
    plot.add(cluster)
    plot.hasLegend()
    plot.save(filename)
