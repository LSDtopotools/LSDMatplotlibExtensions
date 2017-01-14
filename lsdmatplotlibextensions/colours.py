## LSDMatplotlibExtensions.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
## These functions are wrappers and extensions around the matplotlib 
## library to provide additionaly plotting functionality without having
## to copy and paste code all the time.
## They are not necessarily specific to LSDTopoTools usage.
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
## DAV
## 11/01/2017
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"""
Created on Thu Jan 12 14:33:21 2017

@author: DAV
"""

import numpy as _np
import matplotlib as _mpl
import matplotlib.pyplot as _plt
import matplotlib.gridspec as _gridspec
import matplotlib.colors as _mcolors
import matplotlib.cm as _cm

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=-1):
    """
    Truncates a standard matplotlib colourmap so
    that you can use part of the colourange in your plots.
    Handy when the colourmap you like has very light values at
    one end of the map.
    
    Usage exa_mple:
       minColor = 0.00
       maxColor = 0.85
       inferno_t = truncate_colormap(_plt.get_cmap("inferno"), minColor, maxColor) 
    """
    cmap = _plt.get_cmap(cmap)
    
    if n == -1:
        n = cmap.N
    new_cmap = _mcolors.LinearSegmentedColormap.from_list(
         'trunc({name},{a:.2f},{b:.2f})'.format(name=cmap.name, a=minval, b=maxval),
         cmap(_np.linspace(minval, maxval, n)))
    return new_cmap
    
def discrete_colourmap(N, base_cmap=None):
    """
    Create an N-bin discrete colourmap from the specified input colormap.
    github.com/jakevdp
    
    DAV: modified so you can pass in the string name of a colourmap
    or a Colormap object.
    """

    # Note that if base_cmap is a string or None, you can si_mply do
    #    return _plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:
    print type(base_cmap)
    if isinstance(base_cmap, _mcolors.Colormap):
        base = base_cmap
    elif isinstance(base_cmap, str):
        base = _plt.cm.get_cmap(base_cmap)
    else:
        print "DrapeName supplied is of type: ", type(base_cmap)
        raise ValueError('DrapeName must either be a string name of a colormap, \
                         or a Colormap. Please try again.')
        
    color_list = base(_np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)
    
def cmap_discretize(N, cmap):
    """Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet. 
        N: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)
    """

    if type(cmap) == str:
        cmap = _plt.get_cmap(cmap)
    colors_i = _np.concatenate((_np.linspace(0, 1., N), (0.,0.,0.,0.)))
    colors_rgba = cmap(colors_i)
    indices = _np.linspace(0, 1., N+1)
    cdict = {}
    for ki,key in enumerate(('red','green','blue')):
        cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki])
                       for i in xrange(N+1) ]
    # Return colormap object.
    return _mcolors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)
    

def colorbar_index(fig, cax, ncolors, cmap, drape_min_threshold, drape_max):
    discrete_cmap = discrete_colourmap(ncolors, cmap)
    
    mappable = _cm.ScalarMappable(cmap=discrete_cmap)
    mappable.set_array([])
    #mappable.set_clim(-0.5, ncolors + 0.5)
    mappable.set_clim(drape_min_threshold, drape_max)
    
    print type(fig)
    print type(mappable)
    print type(cax)
    print 
    cbar = fig.colorbar(mappable, cax=cax)
    print type(cbar)
    #cbar.set_ticks(_np.linspace(0, ncolors, ncolors))
    cbar.set_ticks(_np.linspace(drape_min_threshold, drape_max, ncolors+1))
    #cbar.set_ticklabels(range(ncolors))
    
    return cbar

