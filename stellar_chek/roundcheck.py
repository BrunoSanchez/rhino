#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import sep
from astropy.io import fits
from astropy.io import ascii
from astroML import crossmatch as cx

cat = ascii.open(cat_path, names = ['cstarid', 'x', 'y', 'imag'])
data = fits.get_data(image_path)
data = data.byteswap().newbyteorder()
bkg = sep.background(image_data)
data = image_data - bkg

def go_test(cat, image_data, threshold):
    #make the extraction
    sources = sep.extract(image_data, threshold)
    #crossmatch the cats
    S = np.array([cat['x'], cat['y']]).T
    O = np.array([sources['x'], sources['y']]).T
      #right
    distr, indr = cx.crossmatch(S, O, max_distance=1.8)
    matchsr = ~np.isinf(distr)
      #left 
    distl, indl = cx.crossmatch(O, S, max_distance=1.8)
    matchsl = ~np.isinf(distl)
    ##
    objID = np.zeros_like(O[:,0]) -1
    CSTARID = np.zeros_like(O[:,0]) -1
    for i in range(len(O)):
        if distl[i] != np.inf: 
            dist_o = distl[i]
            ind_o  = indl[i]
            # now ind is a star number
            # lets see if that star has matched the same obj
            if distr[ind_o] != np.inf:
                dist_s = distr[ind_o]
                ind_s = indr[ind_o]
                if ind_s == i:
                    objID[i] = ind_o  
                    CSTARID[i] = stars['cstarid'][ind_o]
    sources['objID'] = objID
    sources['cstarid'] = CSTARID
    # report the hits as detections
    n_hits = sum(objID > 0.)
    # report the false detections
    n_false= sum(objID < 0.)
    return 

