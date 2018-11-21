import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import mpl_toolkits
from mpl_toolkits.basemap import Basemap
import seaborn as sns

import hazelbean as hb

match_raster = '../Data/inputs/Base/country_ids.tif'
## Compare models by R2 scores

def plot_R2_2params(param_x, param_color, xgb_tuning,scatter=False,savefig=None,
                    ylim=None,title=None,figsize=(20,5),color_palette='Dark2'):

    fig, ax = plt.subplots(figsize=figsize)


    palette = plt.get_cmap(color_palette)
    num=0
    for param_color_value in xgb_tuning[param_color].unique():
        num+=1
        x = (xgb_tuning[xgb_tuning[param_color]==param_color_value][param_x])
        y = (xgb_tuning[xgb_tuning[param_color]==param_color_value]['R2'])
        #labels= (xgb_tuning[xgb_tuning[param_color]==learning_rate][param_color])
        if scatter == False:
            P = plt.plot(x,y, marker='.',color=palette(num), linewidth=2, alpha=0.9,
                 label=(str(param_color)+' : ' +str(param_color_value)))
        if scatter == True:
            P = plt.scatter(x,y, marker='o',color=palette(num),
                 label=(str(param_color)+' : ' +str(param_color_value)))
        
    plt.legend(loc=2, ncol=1)
    
    if title == None:
        title = "Comparing models by "+ param_x +" and "+ param_color
    plt.title(title, loc='left', fontsize=18, fontweight=0, color='black')

    plt.xlabel(param_x)
    plt.ylabel("R2")
    
    # Y lim
    if ylim != None:
        if scatter == False:
            P[0].axes.set_ylim(ylim)
        if scatter == True:
            P.axes.set_ylim(ylim)

    if savefig != None:
        plt.savefig(savefig,dpi=300)

######## ######## ########

########   MAPS   ########

######### ######## ########

def export_raster(df,col_name,savefig=False):
    '''export_as_tif'''
    #Make a zeros_df of length 9331200
    match_af = hb.ArrayFrame(match_raster)
    zeros_array = np.zeros(match_af.size)
    zeros_df = pd.DataFrame(zeros_array)
    DF = df[col_name].reset_index()
    ### Merge with zeros_df to include non-ag pixels
    full_df = pd.merge(zeros_df, DF, left_index=True, right_on='pixel_id', how='outer')
    
    
    values = full_df[col_name].as_matrix().reshape((2160, 4320)).astype(np.float32)

    ### to do transform df to array to raster
    target_path = savefig
    x_pixels = 4320  # = match.RasterXSize
    y_pixels = 2160  # = match.RasterYSize
    driver = gdal.GetDriverByName('GTiff')
    output = driver.Create(target_path,x_pixels, y_pixels, 1 ,gdal.GDT_Float32)
    output.GetRasterBand(1).WriteArray(values)

    match = gdal.Open(match_raster)
    proj = match.GetProjection()
    geotrans = match.GetGeoTransform()
    output.SetGeoTransform(geotrans)
    output.SetProjection(proj)
    output.FlushCache()
    #output.GetRasterBand(1).SetNoDataValue(np.nan)
    output=None
    

    
    #if savefig != False:
    #    print('Saving tif at '+ savefig)
    #    plt.savefig(savefig,dpi=300)
    #    pass
    
    return full_df

#### Python Maps ####
    
def visualize_two_maps(serie1, serie2,
                     savefig=False,colorscheme='diverging',
                     resize=False,
                     shape=(2160,4320)):

    fig, axes = plt.subplots(2, 1, figsize=(20,15))
    
    # Define global vmin and vmax
    vmax = max(serie1.max(),serie2.max())
    vmin = min(serie1.min(),serie2.min())
    
    # -- Prepare data --
    #Make a zeros_df of length 9331200
    match_af = hb.ArrayFrame(match_raster)
    zeros_array = np.zeros(match_af.size)
    zeros_df = pd.DataFrame(zeros_array)
    
    ### Merge with zeros_df to include non-ag pixels
    full_df1 = pd.merge(zeros_df, serie1.reset_index(), left_index=True, right_on='pixel_id', how='outer')
    full_df2 = pd.merge(zeros_df, serie2.reset_index(), left_index=True, right_on='pixel_id', how='outer')
    
    ## -- Plot columns --
    
    #Colorscale
    if colorscheme == 'diverging':
        raw_cmap =  plt.get_cmap('PiYG')
        cmap = customColorMap_v(raw_cmap, vmin, vmax,#serie1, serie2, serie3, ### Cleaner option: woudl take vmin, vmax as args instead of series
                                    resize=resize)
    elif colorscheme == 'sequential':
        raw_cmap = plt.get_cmap('inferno_r') #alternatively 'magma'
        cmap = customColorMap_v(raw_cmap, vmin, vmax,#serie1, serie2, serie3,
                                    resize=resize)
    else:
        print('Wrong colorscheme')
    
    
    #Plot data
    data = np.array(full_df1[full_df1.columns[-1]])
    bm = Basemap(ax=axes[0])
    im = bm.imshow(np.flipud(data.reshape(shape)),cmap=cmap,vmin=vmin,vmax=vmax)
    bm.drawcoastlines(linewidth=0.15, color='0.1')
    axes[0].set_title(serie1.name)

    data = np.array(full_df2[full_df2.columns[-1]])
    bm = Basemap(ax=axes[1])
    im = bm.imshow(np.flipud(data.reshape(shape)),cmap=cmap,vmin=vmin,vmax=vmax)
    bm.drawcoastlines(linewidth=0.15, color='0.1')
    axes[1].set_title(serie2.name)
    
    #cbar = plt.colorbar(im, orientation='vertical',fraction=0.0234, pad=0.04)
    
    fig.colorbar(im, ax=axes.ravel().tolist())
    #Or:
    #cax,kw = mpl.colorbar.make_axes([ax for ax in axes.flat])
    #plt.colorbar(im, cax=cax, **kw)
  
    if savefig != False:
        fig.savefig(savefig,dpi=300)
        
   #if colorscheme != cmap:    
   #     return cmap


def visualize_3_maps(serie1, serie2, serie3,
                     savefig=False,colorscheme='diverging',
                     resize=False,
                     shape=(2160,4320)):

    fig, axes = plt.subplots(2, 2, figsize=(20,9))
    
    # Define global vmin and vmax
    vmax = max(serie1.max(),serie2.max(),serie3.max())
    vmin = min(serie1.min(),serie2.min(),serie3.min())

    # -- Prepare data --
    #Make a zeros_df of length 9331200
    match_af = hb.ArrayFrame(match_raster)
    zeros_array = np.zeros(match_af.size)
    zeros_df = pd.DataFrame(zeros_array)
    
    ### Merge with zeros_df to include non-ag pixels
    full_df1 = pd.merge(zeros_df, serie1.reset_index(), left_index=True, right_on='pixel_id', how='outer')
    full_df2 = pd.merge(zeros_df, serie2.reset_index(), left_index=True, right_on='pixel_id', how='outer')
    full_df3 = pd.merge(zeros_df, serie3.reset_index(), left_index=True, right_on='pixel_id', how='outer')
    
    ## -- Plot columns --
    
    #Colorscale
    if colorscheme == 'diverging':
        raw_cmap =  plt.get_cmap('PiYG')
        cmap = customColorMap_v(raw_cmap, vmin, vmax,#serie1, serie2, serie3, ### Cleaner option: woudl take vmin, vmax as args instead of series
                                    resize=resize)
    elif colorscheme == 'sequential':
        raw_cmap = plt.get_cmap('inferno_r') #alternatively 'magma'
        cmap = customColorMap_v(raw_cmap, vmin, vmax,#serie1, serie2, serie3,
                                    resize=resize)
    else:
        print('Wrong colorscheme')
    
    
    #Plot data
    data = np.array(full_df1[full_df1.columns[-1]])
    bm = Basemap(ax=axes[0,0])
    im = bm.imshow(np.flipud(data.reshape(shape)),cmap=cmap,vmin=vmin,vmax=vmax)
    bm.drawcoastlines(linewidth=0.15, color='0.1')
    axes[0,0].set_title(serie1.name)

    data = np.array(full_df2[full_df2.columns[-1]])
    bm = Basemap(ax=axes[1,1])
    im = bm.imshow(np.flipud(data.reshape(shape)),cmap=cmap,vmin=vmin,vmax=vmax)
    bm.drawcoastlines(linewidth=0.15, color='0.1')
    axes[1,1].set_title(serie2.name)

    data = np.array(full_df3[full_df3.columns[-1]])
    bm = Basemap(ax=axes[1,0])
    im = bm.imshow(np.flipud(data.reshape(shape)),cmap=cmap,vmin=vmin,vmax=vmax)
    bm.drawcoastlines(linewidth=0.15, color='0.1')
    axes[1,0].set_title(serie3.name)
    
    #cbar = plt.colorbar(im, orientation='vertical',fraction=0.0234, pad=0.04)
    
    fig.colorbar(im, ax=axes.ravel().tolist())
    #Or:
    #cax,kw = mpl.colorbar.make_axes([ax for ax in axes.flat])
    #plt.colorbar(im, cax=cax, **kw)
  
    if savefig != False:
        fig.savefig(savefig,dpi=300)
        
   #if colorscheme != cmap:    
   #     return cmap

def visualize_4_maps(serie1, serie2, serie3,serie4,
                     savefig=False,colorscheme='diverging',
                     resize=False,
                     shape=(2160,4320)):

    fig, axes = plt.subplots(2, 2, figsize=(20,9))
    
    # Define global vmin and vmax
    vmax = max(serie1.max(),serie2.max(),serie3.max(),serie4.max())
    vmin = min(serie1.min(),serie2.min(),serie3.min(),serie4.min())

    # -- Prepare data --
    #Make a zeros_df of length 9331200
    match_af = hb.ArrayFrame(match_raster)
    zeros_array = np.zeros(match_af.size)
    zeros_df = pd.DataFrame(zeros_array)
    
    ### Merge with zeros_df to include non-ag pixels
    full_df1 = pd.merge(zeros_df, serie1.reset_index(), left_index=True, right_on='pixel_id', how='outer')
    full_df2 = pd.merge(zeros_df, serie2.reset_index(), left_index=True, right_on='pixel_id', how='outer')
    full_df3 = pd.merge(zeros_df, serie3.reset_index(), left_index=True, right_on='pixel_id', how='outer')
    full_df4 = pd.merge(zeros_df, serie4.reset_index(), left_index=True, right_on='pixel_id', how='outer')
    
    ## -- Plot columns --
    
    #Colorscale
    if colorscheme == 'diverging':
        raw_cmap =  plt.get_cmap('PiYG')
        cmap = customColorMap_v(raw_cmap, vmin, vmax,#serie1, serie2, serie3, ### Cleaner option: woudl take vmin, vmax as args instead of series
                                    resize=resize)
    elif colorscheme == 'sequential':
        raw_cmap = plt.get_cmap('inferno_r') #alternatively 'magma'
        cmap = customColorMap_v(raw_cmap, vmin, vmax,#serie1, serie2, serie3,
                                    resize=resize)
    else:
        print('Wrong colorscheme')
    
    
    #Plot data
    data = np.array(full_df1[full_df1.columns[-1]])
    bm = Basemap(ax=axes[0,0])
    im = bm.imshow(np.flipud(data.reshape(shape)),cmap=cmap,vmin=vmin,vmax=vmax)
    bm.drawcoastlines(linewidth=0.15, color='0.1')
    axes[0,0].set_title(serie1.name)

    data = np.array(full_df2[full_df2.columns[-1]])
    bm = Basemap(ax=axes[0,1])
    im = bm.imshow(np.flipud(data.reshape(shape)),cmap=cmap,vmin=vmin,vmax=vmax)
    bm.drawcoastlines(linewidth=0.15, color='0.1')
    axes[0,1].set_title(serie2.name)

    data = np.array(full_df3[full_df3.columns[-1]])
    bm = Basemap(ax=axes[1,0])
    im = bm.imshow(np.flipud(data.reshape(shape)),cmap=cmap,vmin=vmin,vmax=vmax)
    bm.drawcoastlines(linewidth=0.15, color='0.1')
    axes[1,0].set_title(serie3.name)
    
    data = np.array(full_df4[full_df4.columns[-1]])
    bm = Basemap(ax=axes[1,1])
    im = bm.imshow(np.flipud(data.reshape(shape)),cmap=cmap,vmin=vmin,vmax=vmax)
    bm.drawcoastlines(linewidth=0.15, color='0.1')
    axes[1,1].set_title(serie4.name)
    
    #cbar = plt.colorbar(im, orientation='vertical',fraction=0.0234, pad=0.04)
    
    fig.colorbar(im, ax=axes.ravel().tolist())
    #Or:
    #cax,kw = mpl.colorbar.make_axes([ax for ax in axes.flat])
    #plt.colorbar(im, cax=cax, **kw)
  
    if savefig != False:
        fig.savefig(savefig,dpi=300)
        
   #if colorscheme != cmap:    
   #     return cmap


def customColorMap_v(cmap, vmin, vmax, resize=False, name='blabla'):
    '''Charlie's function to re-center and re-size colormap'''

    midpoint= 1 - vmax / (vmax + abs(vmin))
    
    if resize!=False: 
        start=resize[0]
        stop =resize[1]
        ### Could do directly with quantiles e.g  start = 1 / (serie.quantile(0.1) / serie.min() )
        ### And stop =  1 / (serie.quantile(0.9) / serie.max() )
    else:
        start = 0
        stop  = 1
    
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap


def visualize_data(df,col_name,savefig=False,colorscheme='diverging',
                   vminmax=False,savecmap=False,
                   shape=(2160,4320),title=None,resize=False):

    
    fig,axes = plt.subplots(1, 1, figsize=(20,15))

    # -- Prepare data --
    #Make a zeros_df of length 9331200
    match_af = hb.ArrayFrame(match_raster)
    zeros_array = np.zeros(match_af.size)
    zeros_df = pd.DataFrame(zeros_array)
    DF = df[col_name].reset_index()
    ### Merge with zeros_df to include non-ag pixels
    full_df = pd.merge(zeros_df, DF, left_index=True, right_on='pixel_id', how='outer')
    
    ## -- Plot column --
    
    #Colorscale
    if vminmax==False:
        serie = df[col_name]
        vmax = serie.max()
        vmin = serie.min()
    else:
        vmin = vminmax[0]
        vmax = vminmax[1]
    
    if colorscheme == 'diverging':
        raw_cmap =  plt.get_cmap('PiYG')
        cmap = customColorMap(raw_cmap, vmin, vmax, resize)
    elif colorscheme == 'sequential':
        raw_cmap = plt.get_cmap('inferno_r') #alternatively 'magma'
        cmap = customColorMap(raw_cmap, vmin, vmax, resize)
    #else:
        #cmap = replicateColorMap(colorscheme,vmin=14.022869333967861,vmax=19.24083736317894)
        
    
    
    
    #Plot data
    data = np.array(full_df[col_name])
    bm = Basemap()
    im = bm.imshow(np.flipud(data.reshape(shape)),cmap=cmap)
    bm.drawcoastlines(linewidth=0.15, color='0.1')
    
    cbar = plt.colorbar(im, orientation='vertical',fraction=0.0234, pad=0.04)
    
    if title == None:
        plt.title(col_name)
    else:
        plt.title(title)
    plt.show()
  
    if savefig != False:
        fig.savefig(savefig)
        
        
    if savecmap == True:
        return (vmin, vmax), resize
        
   #if colorscheme != cmap:    
   #     return cmap
    

def customColorMap(cmap, vmin, vmax, resize=False, name='blabla'):
    '''Charlie's function to re-center and re-size colormap'''
    
    midpoint= 1 - vmax / (vmax + abs(vmin)) 
    
    if resize!=False: 
        start=resize[0]
        stop =resize[1]
        ### Could do directly with quantiles e.g  start = 1 / (serie.quantile(0.1) / serie.min() )
        ### And stop =  1 / (serie.quantile(0.9) / serie.max() )
    else:
        start = 0
        stop  = 1
    
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)
    
    return newcmap#, vmin, vmax, midpoint