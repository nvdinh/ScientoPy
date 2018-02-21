import numpy as np
from scipy.spatial import cKDTree
import globalVar

LABEL_COLOR = "#dddddd"
BUBBLE_COLOR = "#63d065"
EDGE_COLOR = "#444444"

xMax = 1
yMax = 1

def get_label_xy(xyData, i):
    tree = cKDTree(xyData)
    thresh = 0.15
    neighbors = tree.query_ball_point([xyData[i, 0], xyData[i, 1]], thresh)

    #print neighbors

    # if no conflicts
    if len(neighbors) == 1:
        xy = (-30, 30)
    else:
        mean = np.mean(xyData[:, :2][neighbors], axis=0)

        if mean[0] == xyData[i, 0] and mean[1] == xyData[i, 1]:
            if i < np.max(neighbors):
                xy = (-30, 30)
            else:
                xy = (30, -30)
        else:
            angle = np.arctan2(xyData[i, 1] - mean[1], xyData[i, 0] - mean[0])

            if angle > np.pi / 2:
                xy = (-30, 30)
            elif angle > 0:
                xy = (30, 30)
            elif angle > -np.pi / 2:
                xy = (30, -30)
            else:
                xy = (-30, -30)

    return xy


def labeled_scatter_plot(data, labels, plt_in):

    # Get the max of each axis
    xMax = data[:, :2][:, 0].max()
    yMax = data[:, :2][:, 1].max()
    zMax = data[:, 2].max()

    xMin = data[:, :2][:, 0].min()
    yMin = data[:, :2][:, 1].min()
    zMin = data[:, 2].min()

    #print("yMax = %s" % yMax)

    # Plot bubbles in scatter
    plt_in.scatter(
        data[:, 0], data[:, 1], marker='o', c = BUBBLE_COLOR, s=1000*(data[:, 2]/float(zMax)),
        cmap = plt_in.get_cmap('Spectral'))

    # Get xyData points ploted scaled to 1
    xData = data[:, :2][:, 0]/float(xMax)
    yData = data[:, :2][:, 1]/float(yMax)
    xyData = np.append([xData], [yData], axis=0)
    xyData = np.transpose(xyData)

    # Plot each label
    for i in range(data.shape[0]):
        print labels[i]
        xy = get_label_xy(xyData, i)
        plt_in.annotate(
            labels[i],
            xy = data[i, :2], xytext = xy,
            textcoords = 'offset points', ha = 'center', va = 'center',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = LABEL_COLOR, alpha = 0.75),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

        xy = np.array(xy) * [0.08*xMax/30.0, 0.12*yMax/30.0]
        xyLabel = data[i, :2] + xy
        xyLabelScaled1 = xyLabel * [1/xMax, 1/yMax]

        xyData = np.append(xyData, [xyLabelScaled1], axis=0)

    #for i in range(0,len(labels)):
    #    print("(%d): %s, label: %d" % (i, labels[i], (i + len(labels))))

    # Set the graphs limits
    if(xMin > 0):
        plt_in.xlim(xmin=0)
    else:
        plt_in.xlim(xmin = xMin * 1.2)
    plt_in.xlim(xmax=xMax * 1.2)

    if(yMin > 0):
        plt_in.ylim(ymin = 0)
    else:
        plt_in.ylim(ymin = yMin - (yMax*0.1))

    if(yMax > 0):
        plt_in.ylim(ymax = yMax*1.2)
    else:
        plt_in.ylim(ymax= yMax *(-1.2))


def labeled_scatter_plot_colors(data, labels, plt_in):

    cmap = plt_in.cm.Paired(np.linspace(0, 1, len(labels)))

    # Get the max of each axis
    xMax = data[:, :2][:, 0].max()
    yMax = data[:, :2][:, 1].max()
    zMax = data[:, 2].max()

    xMin = data[:, :2][:, 0].min()
    yMin = data[:, :2][:, 1].min()
    zMin = data[:, 2].min()

    # print("yMax = %s" % yMax)

    fig = plt_in.figure()
    ax = plt_in.subplot(111)

    i = 0
    for dataIn in data:
        #plt_in.plot(dataIn[0], dataIn[1], 'o', color=globalVar.COLORS[i], markersize=100*dataIn[2]/float(zMax), label=labels[i])
        ax.scatter(dataIn[0], dataIn[1], marker="o", s=2000 * (dataIn[2] + 1) / float(zMax), c="w", edgecolors=EDGE_COLOR)
        ax.scatter(dataIn[0], dataIn[1], marker=globalVar.MARKERS[i], label=labels[i],
                       s=800 * (dataIn[2] + 1) / float(zMax), c=cmap[i].tolist(), edgecolors=cmap[i].tolist())
        i += 1


    # for i in range(0,len(labels)):
    #    print("(%d): %s, label: %d" % (i, labels[i], (i + len(labels))))


    # Shrink current axis by 20%
    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])


    lgnd = ax.legend(loc=2, scatterpoints=1, fontsize=12, fancybox=True, ncol=3)

    lgnd.get_frame().set_alpha(0.5)


    #lgnd = plt_in.legend(loc='center left', bbox_to_anchor=(1, 0.815), numpoints=1)
    for handle in lgnd.legendHandles:
        handle.set_sizes([100.0])

    # Set the graphs limits
    if (xMin > 0):
        plt_in.xlim(xmin=0)
    else:
        plt_in.xlim(xmin=xMin * 1.2)
    plt_in.xlim(xmax=xMax * 1.2)

    if (yMin > 0):
        plt_in.ylim(ymin=0)
    else:
        plt_in.ylim(ymin=yMin - (yMax * 0.1))

    if (yMax > 0):
        plt_in.ylim(ymax=yMax * 1.4)
    else:
        plt_in.ylim(ymax=yMax * (-1.2))



