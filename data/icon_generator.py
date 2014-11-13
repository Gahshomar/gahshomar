# -*- coding: utf-8 -*-
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
import matplotlib.pyplot as plt; plt.rcdefaults()
# import matplotlib
# matplotlib.rc('font', **{'sans-serif' : 'Arial',
#                            'family' : 'sans-serif'})
import matplotlib.font_manager as fm
elham = fm.FontProperties(fname='/usr/share/fonts/truetype/ttf-farsiweb/koodak.ttf')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

# BLACK = np.array((83, 81, 73)) / 255
# GRAY = np.array((223, 219, 210)) / 255
# DARK = 'dark'

BLACK = np.array((223, 218, 216)) / 255
GRAY = np.array((60, 60, 60)) / 255
DARK = 'light'

NUM_DICT = {'0':u'۰',
            '1':u'۱',
            '2':u'۲',
            '3':u'۳',
            '4':u'۴',
            '5':u'۵',
            '6':u'۶',
            '7':u'۷',
            '8':u'۸',
            '9':u'۹'}
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
  print(text)
  y = xy[1]  # shift y-value for label so that it's below the artist
  if text[0] == '۱':
    ts = 0
  else:
    ts = 0
  plt.text(xy[0]-0+ts, y+20, text, fontproperties=elham,
  size=240, ha="center", color=BLACK) #, family='cursive'

def main():
  for i in range(1,32):
    fig, ax = plt.subplots()
    fig.set_facecolor('None')
    # create 3x3 grid to plot the artists
  #   grid = np.mgrid[0.2:0.8:2j, 0.2:0.8:1j].reshape(2, -1).T
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
    # print(grid)
    
    patches = []
    
    # add a fancy box
    fancybox = mpatches.FancyBboxPatch(
            grid[0], w, h * 5 // 9 + 20,
            boxstyle=mpatches.BoxStyle("Round", pad=padding), color=GRAY)
    patches.append(fancybox)
    label(grid[0] + [w // 2, 0], latinN2PersianN(i))
  
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
  
  #   colors = np.linspace(0, 1, len(patches))
  #   collection = PatchCollection(patches, cmap=plt.cm.spectral, alpha=0.4)
    collection = PatchCollection(patches, match_original=True)
    ax.add_collection(collection)
    
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.axis('equal')
    plt.axis('off')
  
    fig.set_size_inches(5.12,5.12)
    fig.savefig('icons/Folder/persian-calendar-{dark}-theme-{i}.png'.format(i=i, dark=DARK), 
                transparent=True)
                # bbox_inches='tight', transparent=True)
    plt.close()
if __name__ == '__main__':
  main()
