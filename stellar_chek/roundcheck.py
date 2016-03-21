#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import sep
from astropy.io import fits
from astropy.io import ascii
from astroML import crossmatch as cx
import pandas as pd

data_path = os.path.abspath('/home/bos0109/sersic/work/rhino/data/extract_test/stellar/CSTAR/')
images_path = os.path.join(data_path, 'images')
master_Ryan = os.path.join(images_path, 'master10_wcs.fits')

cat_path = os.path.join(data_path, 'cats/stars.dat')

cat = ascii.read(cat_path, names = ['cstarid', 'x', 'y', 'imag'])
data = fits.getdata(master_Ryan)
data = data.byteswap().newbyteorder()
bkg = sep.Background(data)
data = data - bkg

def go_test(cat, image_data, thresh):
    threshold = thresh*bkg.globalrms
    #make the extraction
    sources = sep.extract(image_data, threshold)
    cat.to_pandas()
    sources = pd.DataFrame(sources)
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
                    CSTARID[i] = cat['cstarid'][ind_o]
    sources['objID'] = objID
    sources['cstarid'] = CSTARID
    # report the hits as detections
    n_hits = sum(objID > 0.)
    print 'Number of hits ==> {}'.format(n_hits)
    # report the false detections
    n_false= sum(objID < 0.)
    print 'N umber of falses ==> {}'.format(n_false)
    return [thresh, n_hits, n_false]

if __name__ == '__main__':
    import sys
    go_test(cat, data, float(sys.argv[1]))

#go_test(cat, data, 100*bkg.globalrms)