'''
Created on Apr 13, 2014

@author: amir
'''
'''
for a in *light*.png; do convert -trim -transparent "rgb(223, 218, 216)" "$a" "$a"; done
for a in *light*.png; do convert -transparent "rgb(221, 216, 214)" "$a" "$a"; done
for a in *dark*.png; do convert -trim -transparent "rgb(83, 81, 73)" "$a" "$a"; done
for a in *dark*.png; do convert -transparent "rgb(84, 82, 74)" "$a" "$a"; done
'''
import matplotlib.pyplot as plt
plt.rcdefaults()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

BLACK = np.array((83, 81, 73)) / 255
GRAY = np.array((223, 219, 210)) / 255

# BLACK = np.array((223, 218, 216)) / 255
# GRAY = np.array((60, 60, 60)) / 255

NUM_DICT = {'0': '۰',
            '1': '۱',
            '2': '۲',
            '3': '۳',
            '4': '۴',
            '5': '۵',
            '6': '۶',
            '7': '۷',
            '8': '۸',
            '9': '۹'}


def latinN2PersianN(num):
    num = repr(num)
    numP = ''
    for v in num:
        if v in NUM_DICT:
            numP += NUM_DICT[v]
        else:
            numP += v
    return numP


def label(xy, text):
    y = xy[1]    # shift y-value for label so that it's below the artist
    plt.text(xy[0], y, text, ha="center", family='sans', size=250, color=BLACK)

def main():
    for i in range(1,2):
        fig, ax = plt.subplots()
        fig.set_facecolor('None')
        # create 3x3 grid to plot the artists
    #     grid = np.mgrid[0.2:0.8:2j, 0.2:0.8:1j].reshape(2, -1).T
        padding = 20
        w = 512
        h = 512
        sec_hight = h * 2 // 9 + 20
        sec_y = (h * 7) // 9 - 20
        small_width = w // 6
        small_hight = sec_hight * 2 // 3
        x_pad_small = w // 7
        y_small = sec_y + sec_hight - small_hight + padding
        small2_width = small_width
        small2_hight = small_hight // 2
        small2_y = sec_y + sec_hight + padding
        grid = np.array([[ 0, 0], [ 0, sec_y], [x_pad_small, y_small], [w - x_pad_small - small_width, y_small],
                                         [x_pad_small, small2_y], [w - x_pad_small - small_width, small2_y]])
        print(grid)
        
        patches = []
        
        # add a fancy box
        fancybox = mpatches.FancyBboxPatch(
                        grid[0], w, h * 5 // 9 + 20,
                        boxstyle=mpatches.BoxStyle("Round", pad=padding), color=GRAY)
        patches.append(fancybox)
        # label(grid[0] + [w // 2, 0], 'گاه‌شمار')
    
        fancybox = mpatches.FancyBboxPatch(
                        grid[4], small2_width, small2_hight,
                        color=GRAY)
        patches.append(fancybox)
        
        fancybox = mpatches.FancyBboxPatch(
                        grid[5], small2_width, small2_hight,
                        color=GRAY)
        patches.append(fancybox)
        
        fancybox = mpatches.FancyBboxPatch(
                        grid[1], w, sec_hight,
                        boxstyle=mpatches.BoxStyle("Round", pad=padding), color=GRAY)
        patches.append(fancybox)
        
        fancybox = mpatches.FancyBboxPatch(
                        grid[2], small_width, small_hight,
                        color=BLACK)
        patches.append(fancybox)
        
        fancybox = mpatches.FancyBboxPatch(
                        grid[3], small_width, small_hight,
                        color=BLACK)
        patches.append(fancybox)
    
    #     colors = np.linspace(0, 1, len(patches))
    #     collection = PatchCollection(patches, cmap=plt.cm.spectral, alpha=0.4)
        collection = PatchCollection(patches, match_original=True)
        ax.add_collection(collection)
        
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.axis('equal')
        plt.axis('off')
    
        fig.savefig('icons/persian-calendar-dark-theme-{}.svg'.format(i), 
                                bbox_inches='tight', transparent=True)
if __name__ == '__main__':
    main()
