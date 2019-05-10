import numpy as np
import os
import sys
import math
import pylab
import colorsys
import matplotlib
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap, cm
from matplotlib.lines import Line2D
import shapefile

path = './zh2region/'
colors = []


def get_cmap(n, name='hsv'):
    '''
    Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.
    '''
    return plt.cm.get_cmap(name, n)


def draw_pie(data, top, ax, X, Y, size=1500):
    xy = []
    start = 0.
    #cut ratios
    sum_top_5 = sum([x[1] for x in data[:5]])
    ratios = [x[1] / sum_top_5 for x in data[:5]]
    #print(ratios)
    for ratio in ratios:
        x = [0] + np.cos(np.linspace(2*math.pi*start,
                                     2*math.pi*(start+ratio), 30)).tolist()
        y = [0] + np.sin(np.linspace(2*math.pi*start,
                                     2*math.pi*(start+ratio), 30)).tolist()
        xy.append(list(zip(x, y)))
        start += ratio

    for i, xyi in enumerate(xy):
        zh = [x[0] for x in top]
        index_zh = zh.index(data[i][0])
        #print(index_zh)
        ax.scatter([X], [Y], marker=(xyi, 0), s=size,
                   facecolor=colors[index_zh], linewidth=0.3, edgecolor="k")


def main():
    #read coordinates of each county/city
    place = []
    xlon = []
    ylat = []
    with open('./Taiwan_coordinates.txt', 'r') as fi:
        for line in fi:
            coor = line.split()
            place.append(coor[0])
            xlon.append(float(coor[1]))
            ylat.append(float(coor[2]))

    #read nametable (english -> chinese)
    nametable = {}
    with open('./nametable', 'r') as fi:
        for line in fi:
            name = line.split()
            nametable[name[0]] = name[1]

    #read county
    part = sys.argv[1]
    with open('./part_region', 'r') as fi:
        for line in fi:
            line_split = line.split()
            if line_split[0] == part:
                county = line_split[1:]
                break

    #read every npy
    rank = {}
    for filename in os.listdir(path):
        english_name = filename.split('_')[0]
        chinese_name = nametable[english_name]
        if chinese_name not in county:
            continue
        data = dict(np.load(path + filename).item())
        if chinese_name in rank.keys():
            rank[chinese_name] = {**rank[chinese_name], **data}
        else:
            rank[chinese_name] = data
    #sort
    for key in rank.keys():
        rank[key] = sorted(rank[key].items(),
                           key=lambda d: d[1], reverse=True)

    #delete bad ZH
    bad_ZH = []
    with open('./bad_ZH', 'r') as fi:
        bad_ZH = [line.strip() for line in fi]
    for key in rank.keys():
        rank[key] = [x for x in rank[key] if x[0] not in bad_ZH]

    #extract top 5 list
    top = {}
    for key in rank.keys():
        for i in range(5):
            if rank[key][i][0] in top.keys():
                top[rank[key][i][0]] += rank[key][i][1]
            else:
                top[rank[key][i][0]] = rank[key][i][1]
    top = sorted(top.items(), key=lambda d: d[1], reverse=True)

    #choose color
    num_color = len(top)
    randHSVcolors = [(np.random.uniform(low=0.0, high=1),
                      np.random.uniform(low=0.2, high=1),
                      np.random.uniform(low=0.9, high=1))
                     for i in range(num_color)]

    global colors
    for HSVcolor in randHSVcolors:
        colors.append(colorsys.hsv_to_rgb(HSVcolor[0],
                                          HSVcolor[1],
                                          HSVcolor[2]))

    #map boundary
    fig = plt.figure()
    ax = fig.add_axes([.05, .01, .79, .95])

    #read lon & lat
    with open('./part_lon_lat', 'r') as fi:
        for line in fi:
            line_split = line.split()
            if line_split[0] == part:
                x1, x2, y1, y2 = line_split[1:]
                break

    #create legend

    labels = [top[i][0] for i in range(len(top))]
    ChineseFont1 = FontProperties(fname='./NotoSansCJK-Black.ttc',
                                  weight='bold')
    legend_elements = []
    for i in range(len(top)):
        legend_elements.append(Line2D([0], [0], color=colors[i],
                               lw=3, label=labels[i]))
    fig, ax = plt.subplots()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(handles=legend_elements, loc='center left', markerscale=20,
              prop=ChineseFont1, fontsize='x-small', bbox_to_anchor=(1, 0.5))

    #Create the map
    m = Basemap(resolution='f', projection='merc', llcrnrlat=y1, urcrnrlat=y2,
                llcrnrlon=x1, urcrnrlon=x2, lat_ts=0)
    m.drawcoastlines(linewidth=0.6)
    #m.drawparallels(np.arange(22.5, 26), labels=[1,0,0,0], fontsize=5)
    #m.drawmeridians(np.arange(118, 123), labels=[0,0,0,1], fontsize=5)
    plt.title('Freq_by_region_' + part, fontsize=10, weight='bold')
    #plt.xlabel('lon', fontsize=5, x=1, weight='bold')
    #plt.ylabel('lat', fontsize=5, y=1, weight='bold')

    #read shapefile
    m.readshapefile('./gadm36_TWN_shp/gadm36_TWN_0', '0',
                    linewidth=0.4, drawbounds=True)
    m.readshapefile('./gadm36_TWN_shp/gadm36_TWN_1', '1',
                    linewidth=0.4, drawbounds=True)
    m.readshapefile('./gadm36_TWN_shp/gadm36_TWN_2', '2',
                    linewidth=0.4, drawbounds=True)

    #plot pie charts:
    for key in rank.keys():
        index = place.index(key)
        X, Y = m(xlon[index], ylat[index])
        draw_pie(rank[key], top, ax, X, Y, size=650)

    #output charts
    plt.savefig('freq_by_region_pies_%s.png' % part, dpi=2000)

if __name__ == '__main__':
    main()
