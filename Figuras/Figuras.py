# -*- coding: utf-8 -*-
#==============================================================================
#------------------------------------------------------------------------------
# -- FUNCIONES PARA REALIZAR GRÁFICOS EN PYTHON
#------------------------------------------------------------------------------
#==============================================================================
"""
Created on Mon Mar 28 01:30:48 2016

Es una compilación de los códigos escritos para generar figuras con formato

@author: Daniela
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.stats as sc
from scipy.stats import gaussian_kde
import numpy as np
from mpl_toolkits.basemap import Basemap

#==============================================================================
# -- Figura series y scatterplot
#==============================================================================
def fig_seriesyscatter(serie,reconstruccion_ser,medicion_ser,metadatos):
    """
    Dibuja la comparación de la serie original y la de reconstrucción y un
    scatter plot de ambas series
    
    Parameters:
    ----------
    
    serie:
        string.
        Código de la serie
    
    reconstruccion_ser:
        Pandas_Series.
        Serie de reconstrucción
    
    medicion_ser:
        Pandas_Series.
        Serie medida
    
    metadatos:
        Pandas_DataFrame.
        Dataframe con los metadatos de la serie para extraer el nombre de la estación y de la corriente
    Returns:
    -------
    
    fig:
        Figura.
        Objeto tipo figura que se puede guardar usando matplotlib.pyplot.savefig
    
    """
    fig=plt.figure(figsize=(12,3.5))
    titulo=serie+' - '+metadatos['nombre'][int(serie)]+' - '+str(metadatos['Corriente'][int(serie)])
    fig.suptitle(titulo)
    gs = gridspec.GridSpec(1, 3)
    ax1 = plt.subplot(gs[0,:-1])
    ax2 = plt.subplot(gs[0,2],sharey=ax1)
    plt.sca(ax1)
    plt.ylabel(u'Q '+r'$[m^3/s]$')
    plt.xlabel(u'Fecha [año]')
    reconstruccion_ser.plot(ls='-',c='r',lw=2)
    medicion_ser.plot(c='k')
    ax1.legend([u'Reconstrucción',u'Medición'],loc="upper left")
    plt.sca(ax2)
    notna_index=medicion_ser.loc[medicion_ser.notna().values].index
    x=reconstruccion_ser[notna_index].values
    y=medicion_ser[notna_index].values
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    sorted_index=np.argsort(z)
    z=z[sorted_index]
    x=x[sorted_index]
    y=y[sorted_index]
    plt.scatter(x,y,s=50,c=z,cmap='jet',marker='.')
    plt.xlabel(u'Q reconstruido '+r'$[m^3/s]$')
    #plt.ylabel(u'Q medido '+r'$[m^3/s]$')
    plt.title("R2 = {:.2f}".format(np.corrcoef(x,y)[0,1]))
    return fig

#==============================================================================
# -- Figura series
#==============================================================================
def fig_series(serie,reconstruccion_ser,medicion_ser,metadatos):
    """
    Dibuja la serie original y en los faltantes la de reconstrucción
    
    Parameters:
    ----------
    
    serie:
        string.
        Código de la serie
    
    reconstruccion_ser:
        Pandas_Series.
        Serie de reconstrucción
    
    medicion_ser:
        Pandas_Series.
        Serie medida
    
    metadatos:
        Pandas_DataFrame.
        Dataframe con los metadatos de la serie para extraer el nombre de la estación y de la corriente
    Returns:
    -------
    
    fig:
        Figura.
        Objeto tipo figura que se puede guardar usando matplotlib.pyplot.savefig
    """
    fig=plt.figure(figsize=(9,3.5))
    titulo=serie+' - '+metadatos['nombre'][int(serie)]+' - '+str(metadatos['Corriente'][int(serie)])
    fig.suptitle(titulo)
    plt.ylabel(u'Q '+r'$[m^3/s]$')
    plt.xlabel(u'Fecha [año]')
    reconstruccion_ser.plot(ls='-',c='r')
    medicion_ser.plot(c='k',lw=2)
    plt.legend([u'Reconstrucción',u'Medición'],loc="upper left")
    return fig


#==============================================================================
# -- Figura series y scatterplot 2
#==============================================================================
def fig_seriesyscatter2(serie, x, ymin, ymedia, ymax, yall, yorig, vble = u'Q', units = r'$[m^3/s]$'):
    """
    Dibuja la comparación de la serie original y la validación de 
    reconstrucción con sus valores maximo, minimo, y medio. También dibuja un
    scatter plot de la serie y su validación
    
    Parameters:
    -----------
    
    x:
        array or list.
        fechas de las series de tiempo.
    
    ymin:
        array or list.
        valores mínimos de la validación para cada fecha.
    
    ymedia:
        array or list.
        valores medios de la validación para cada fecha.
    
    ymax:
        array or list.
        valores máximos de la validación para cada fecha.
    
    yall:
        array.
        valores de los 20 experimentos para cada fecha.
    
    yorig:
        array or list.
        valores originales de la serie para cada fecha.
    
    Returns:
    --------
    
    fig:
        Figura.
        Objeto tipo figura para guardar usando matplotlib.pyplot.savefig
    """
    #- configure plot
    fig=plt.figure(figsize=(15,3.5))
    gs = gridspec.GridSpec(1, 3)
    ax1 = plt.subplot(gs[0,:-1])
    ax2 = plt.subplot(gs[0,2],sharey=ax1)
    
    #- configure sublot ax1
    plt.sca(ax1)
    fig.suptitle(str(serie))
    ax1.fill_between(x, ymin, ymax, facecolor='red')
    ax1.plot(x, ymedia, 'b--',lw=1)
    ax1.plot(x, yorig, c='k', lw=1)
    plt.xlabel(u'Fecha')
    plt.ylabel(vble + ' ' + units)
    
    #- configure subplot ax2
    plt.sca(ax2)
    xx = np.reshape(yall,(yall.size),order='C').astype(np.float)
    yy = np.repeat(yorig, 20).astype(np.float)
    #yy = np.reshape(yy,(yy.size),order='F').astype(np.float)
    xx1 = xx[np.where(np.logical_and(np.isnan(xx)==False,np.isnan(yy)==False))]
    yy1 = yy[np.where(np.logical_and(np.isnan(xx)==False,np.isnan(yy)==False))]
    xy = np.vstack([xx1,yy1])
    z = gaussian_kde(xy)(xy)
    sorted_index = np.argsort(z)
    z = z[sorted_index]
    xx1 = xx1[sorted_index]
    yy1 = yy1[sorted_index]
    line_1_1 = np.array([0.98 * np.min(xy),1.01 * np.max(xy)])
    plt.scatter( xx1 , yy1 , s=50, c=z, cmap='jet', marker='.')
    plt.plot(line_1_1 , line_1_1,'--k')
    plt.xlim(line_1_1[0], line_1_1[-1])
    plt.ylim(line_1_1[0], line_1_1[-1])
    plt.xlabel(vble + ' reconstruido ' + units)
    #plt.ylabel(u'Q medido '+r'$[m^3/s]$')
    plt.title("R2 = {:.2f}".format(sc.spearmanr(xx1,yy1)[0,1]))
    return fig

#==============================================================================
# -- Figura Mapa puntos tamaño variable
#==============================================================================
    
def mapa_puntos_sizes(values, latitudes, longitudes, umbral, sizes, error, extent, ruta_bordecuenca, ruta_drenaje, alpha = 0.5, markercolor1 = 'k',markercolor2 = 'green', leg_minval = 0.0, leg_maxval = 1.0, leg_maxabs = 1.0, leg_minabs = 0.0):
    exp = 0.5
    zeroval = 2.
    # Definir el tamaño de la figura
    figura = plt.figure(figsize=(5.,5.))
    
    # En qué bordes aparecen las cordenadas
    drawlat=[True,False,False,False]
    drawlon=[False,False,False,True]
    
    # Trazar mapa
    mapa = Basemap(projection='mill',llcrnrlat = extent[0],urcrnrlat = extent[1],llcrnrlon = extent[2], urcrnrlon = extent[3],resolution='h')
    mapa.drawmapboundary(fill_color='lightgrey')
    mapa.fillcontinents(color='white',lake_color='lightgrey')
    mapa.drawrivers(color='navy')
    # Dibujar shapes en el mapa
    shape_info= mapa.readshapefile(ruta_bordecuenca[0], ruta_bordecuenca[1], color='k', linewidth=2.)
    #shape_info2= mapa.readshapefile(ruta_drenaje[0], ruta_drenaje[1], color='navy')
    
    # Dibujar datos
    for i in np.arange(1,latitudes.size + 1):
        x,y = mapa(longitudes[i - 1], latitudes[i - 1])
        if values[i - 1] <= umbral:
            mapa.plot(x, y, marker = "v", color = markercolor1, ls = '', markeredgecolor='k', markersize = sizes[i - 1], alpha = alpha)
        else:
            mapa.plot(x, y, marker = "^", color = markercolor2, ls = '', markeredgecolor='k', markersize = sizes[i - 1], alpha = alpha)
    
    # Dibujar coordenadas en los bordes
    mapa.drawparallels(np.arange(-15.0,6.0,5.),linewidth=0.,labels=drawlat, rotation = 90, fontsize=14, xoffset = 0.)#,family='Helvetica')
    mapa.drawmeridians(np.arange(-80.,-40.,10.),linewidth=0.,labels=drawlon, fontsize=14, yoffset = 0.)#,family='Helvetica')
    
    #- Construir leyenda
    if leg_minval <= umbral:
        leg_medval = umbral + leg_maxval * 0.01
        size_min = zeroval + (np.abs(leg_minval)*(100./(leg_maxabs - leg_minabs) + 1.))**exp
        size_med = zeroval + (np.abs(leg_medval)*(100./(leg_maxabs - leg_minabs) + 1.))**exp
        size_max = zeroval + (np.abs(leg_maxval)*(100./(leg_maxabs - leg_minabs) + 1.))**exp
        marcador_minimo = mpl.lines.Line2D([], [], marker = "v", color = markercolor1, ls = '', markeredgecolor='k',markersize = size_min, alpha = alpha, label= "{:8.2f}".format(leg_minval))
        marcador_medio = mpl.lines.Line2D([], [], marker = "^", color = markercolor2, ls = '', markeredgecolor='k',markersize =  size_med, alpha = alpha, label= "{:8.2f}".format(leg_medval))
        marcador_maximo = mpl.lines.Line2D([], [], marker = "^", color = markercolor2, ls = '', markeredgecolor='k',markersize = size_max, alpha = alpha, label= "{:8.2f}".format(leg_maxval))
        leg = plt.legend(handles = [marcador_minimo, marcador_medio, marcador_maximo], loc='lower left', title = error, fontsize=12)
        leg_title = leg.get_title()
        leg_title.set_fontsize(18)
    else:
        leg_medval = 0.5 * (leg_maxval + leg_minval)
        size_min = zeroval + (np.abs(leg_minval)*(100./(leg_maxabs - leg_minabs) + 1.))**exp
        size_med = zeroval + (np.abs(leg_medval)*(100./(leg_maxabs - leg_minabs) + 1.))**exp
        size_max = zeroval + (np.abs(leg_maxval)*(100./(leg_maxabs - leg_minabs) + 1.))**exp
        marcador_minimo = mpl.lines.Line2D([], [], marker = "^", color = markercolor2, ls = '', markeredgecolor='k',markersize = size_min, alpha = alpha, label= "{:8.2f}".format(leg_minval))
        marcador_medio = mpl.lines.Line2D([], [], marker = "^", color = markercolor2, ls = '', markeredgecolor='k',markersize = size_med, alpha = alpha, label= "{:8.2f}".format(leg_medval))
        marcador_maximo = mpl.lines.Line2D([], [], marker = "^", color = markercolor2, ls = '', markeredgecolor='k',markersize = size_max, alpha = alpha, label= "{:8.2f}".format(leg_maxval))
        leg = plt.legend(handles = [marcador_minimo, marcador_medio, marcador_maximo], loc='lower left', title = error, fontsize=12)
        leg_title = leg.get_title()
        leg_title.set_fontsize(18)
    #plt.show()
    return figura

#==============================================================================
# -- Figura Mapa puntos tamaño variable 2
#==============================================================================
    
def mapa_puntos_sizes2(values, latitudes, longitudes, umbral, sizes, error, extent, ruta_bordecuenca, ruta_drenaje, alpha = 0.5, markercolor1 = 'k',markercolor2 = 'green', leg_minval = 0.0, leg_maxval = 1.0, leg_maxabs = 1.0, leg_minabs = 0.0, exp = 0.55, zeroval = 2.0):
    # Definir el tamaño de la figura
    figura = plt.figure(figsize=(5.,5.))
    
    # En qué bordes aparecen las cordenadas
    drawlat=[True,False,False,False]
    drawlon=[False,False,False,True]
    
    # Trazar mapa
    mapa = Basemap(projection='mill',llcrnrlat = extent[0],urcrnrlat = extent[1],llcrnrlon = extent[2], urcrnrlon = extent[3],resolution='h')
    mapa.drawmapboundary(fill_color='grey')#'lightgrey')
    mapa.fillcontinents(color='white',lake_color='grey')
    mapa.drawrivers(color='grey')

    # Dibujar shapes en el mapa
    shape_info= mapa.readshapefile(ruta_bordecuenca[0], ruta_bordecuenca[1], color='k', linewidth=2.)
    #shape_info2= mapa.readshapefile(ruta_drenaje[0], ruta_drenaje[1], color='navy')
    
    # Dibujar datos
    for i in np.arange(1,latitudes.size + 1):
        x,y = mapa(longitudes[i - 1], latitudes[i - 1])
        if values[i - 1] < umbral:
            mapa.plot(x, y, marker = "v", color = markercolor1, ls = '', markeredgecolor='k', markersize = sizes[i - 1], alpha = alpha)
        elif values[i - 1] > umbral:
            mapa.plot(x, y, marker = "^", color = markercolor2, ls = '', markeredgecolor='k', markersize = sizes[i - 1], alpha = alpha)
        else:
            mapa.plot(x, y, marker = 'o', color = 'white', ls = '', markeredgecolor='k', alpha = alpha)
    
    # Dibujar coordenadas en los bordes
    mapa.drawparallels(np.arange(-15.0,6.0,5.),linewidth=0.,labels=drawlat, rotation = 90, fontsize=14)#,family='Helvetica')
    mapa.drawmeridians(np.arange(-80.,-40.,10.),linewidth=0.,labels=drawlon, fontsize=14)#,family='Helvetica')
    
    #- Construir leyenda
    if leg_minval <= umbral:
        leg_medval = umbral# + leg_maxval * 0.01
        size_min = sizes_fun(values = leg_minval,maxabs = leg_maxabs, minabs = leg_minabs, exp = exp, zeroval = zeroval)
        size_med = sizes_fun(values = umbral + leg_maxval * 0.01,maxabs = leg_maxabs, minabs = leg_minabs, exp = exp, zeroval = zeroval)
        size_max = sizes_fun(values = leg_maxval,maxabs = leg_maxabs, minabs = leg_minabs, exp = exp, zeroval = zeroval)
        marcador_minimo = mpl.lines.Line2D([], [], marker = "v", color = markercolor1, ls = '', markeredgecolor='k',markersize = size_min, alpha = alpha, label= "{:8.2f}".format(leg_minval))
        marcador_medio = mpl.lines.Line2D([], [], marker = "o", color = 'white', ls = '', markeredgecolor='k', alpha = alpha, label= "{:8.2f}".format(leg_medval))
        marcador_maximo = mpl.lines.Line2D([], [], marker = "^", color = markercolor2, ls = '', markeredgecolor='k',markersize = size_max, alpha = alpha, label= "{:8.2f}".format(leg_maxval))
        leg = plt.legend(handles = [marcador_minimo, marcador_medio, marcador_maximo], loc='lower left', title = error, fontsize=12)
        leg = plt.legend(handles = [marcador_minimo, marcador_medio, marcador_maximo], loc='lower left', title = error, fontsize=12)
        leg_title = leg.get_title()
        leg_title.set_fontsize(18)
    else:
        leg_medval = 0.5 * (leg_maxval + leg_minval)
        size_min = sizes_fun(values = leg_minval,maxabs = leg_maxabs, minabs = leg_minabs, exp = exp, zeroval = zeroval)
        size_med = sizes_fun(values = leg_medval,maxabs = leg_maxabs, minabs = leg_minabs, exp = exp, zeroval = zeroval)
        size_max = sizes_fun(values = leg_maxval,maxabs = leg_maxabs, minabs = leg_minabs, exp = exp, zeroval = zeroval)
        marcador_minimo = mpl.lines.Line2D([], [], marker = "^", color = markercolor2, ls = '', markeredgecolor='k',markersize = size_min, alpha = alpha, label= "{:8.2f}".format(leg_minval))
        marcador_medio = mpl.lines.Line2D([], [], marker = "^", color = markercolor2, ls = '', markeredgecolor='k', alpha = alpha, label= "{:8.2f}".format(leg_medval))
        marcador_maximo = mpl.lines.Line2D([], [], marker = "^", color = markercolor2, ls = '', markeredgecolor='k',markersize = size_max, alpha = alpha, label= "{:8.2f}".format(leg_maxval))
        leg = plt.legend(handles = [marcador_minimo, marcador_medio, marcador_maximo], loc='lower left', title = error, fontsize=12)
        leg_title = leg.get_title()
        leg_title.set_fontsize(18)
    #plt.show()
    return figura
#==============================================================================
# -- Tamaños
#==============================================================================
def sizes_fun(values,maxabs,minabs,exp = 0.55, zeroval = 2.0):
    sizes = zeroval + (np.abs(values)*(100./(maxabs - minabs) + 1.))**exp
    return sizes

#==============================================================================
# -- Figura Mapa puntos binarios
#==============================================================================
    
def mapa_puntos_binarios(values, latitudes, longitudes, umbral, error, extent, ruta_bordecuenca, ruta_drenaje, alpha = 0.5, markercolor1 = 'k',markercolor2 = 'green'):
    # Definir el tamaño de la figura
    figura = plt.figure(figsize=(5.,5.))
    
    # En qué bordes aparecen las cordenadas
    drawlat=[True,False,False,False]
    drawlon=[False,False,False,True]
    
    # Trazar mapa
    mapa = Basemap(projection='mill',llcrnrlat = extent[0],urcrnrlat = extent[1],llcrnrlon = extent[2], urcrnrlon = extent[3],resolution='h')
    mapa.drawmapboundary(fill_color='lightgrey')
    mapa.fillcontinents(color='white',lake_color='lightgrey')
    mapa.drawrivers(color='navy')
    # Dibujar shapes en el mapa
    shape_info= mapa.readshapefile(ruta_bordecuenca[0], ruta_bordecuenca[1], color='k', linewidth=2.)
    #shape_info2= mapa.readshapefile(ruta_drenaje[0], ruta_drenaje[1], color='navy')
    
    # Dibujar datos
    for i in np.arange(1,latitudes.size + 1):
        x,y = mapa(longitudes[i - 1], latitudes[i - 1])
        if values[i - 1] <= umbral:
            mapa.plot(x, y, marker = 'o', color = markercolor1, ls = '', markeredgecolor='k', alpha = alpha)#, markersize = sizes[i - 1]
        else:
            mapa.plot(x, y, marker = 'o', color = markercolor2, ls = '', markeredgecolor='k', alpha = alpha)#, markersize = sizes[i - 1]    
    # Dibujar coordenadas en los bordes
    mapa.drawparallels(np.arange(-15.0,6.0,5.),linewidth=0.,labels=drawlat, rotation = 90, fontsize=14)#,family='Helvetica')
    mapa.drawmeridians(np.arange(-80.,-40.,10.),linewidth=0.,labels=drawlon, fontsize=14)#,family='Helvetica')
    
    #- Construir leyenda
    minvalue='0'
    maxvalue='1'
    marcador_minimo = mpl.lines.Line2D([], [], marker = 'o', color = markercolor1, ls = '', markeredgecolor='k', alpha = alpha, label= minvalue)#markersize = min(sizes)
    marcador_maximo = mpl.lines.Line2D([], [], marker = 'o', color = markercolor2, ls = '', markeredgecolor='k', alpha = alpha, label= maxvalue)#,markersize = max(sizes)
    leg = plt.legend(handles = [marcador_minimo, marcador_maximo], loc='lower left', title = error, fontsize=12)
    leg_title = leg.get_title()
    leg_title.set_fontsize(18)
    #plt.show()
    return figura

#==============================================================================
# -- Figura series y scatterplot 2
#==============================================================================
def fig_scatter(serie, x, ymin, ymedia, ymax, yall, yorig, vble = u'Q', units = r'$[m^3/s]$'):
    """
    Dibuja la comparación de la serie original y la validación de 
    reconstrucción con sus valores maximo, minimo, y medio. También dibuja un
    scatter plot de la serie y su validación
    
    Parameters:
    -----------
    
    x:
        array or list.
        fechas de las series de tiempo.
    
    ymin:
        array or list.
        valores mínimos de la validación para cada fecha.
    
    ymedia:
        array or list.
        valores medios de la validación para cada fecha.
    
    ymax:
        array or list.
        valores máximos de la validación para cada fecha.
    
    yall:
        array.
        valores de los 20 experimentos para cada fecha.
    
    yorig:
        array or list.
        valores originales de la serie para cada fecha.
    
    Returns:
    --------
    
    fig:
        Figura.
        Objeto tipo figura para guardar usando matplotlib.pyplot.savefig
    """
    #- configure plot
    fig=plt.figure(figsize=(15,3.5))
    gs = gridspec.GridSpec(1, 3)
    ax1 = plt.subplot(gs[0,:-1])
    ax2 = plt.subplot(gs[0,2],sharey=ax1)
    
    #- configure subplot ax2
    plt.sca(ax2)
    xx = np.reshape(yall,(yall.size),order='C').astype(np.float)
    yy = np.repeat(yorig, 20).astype(np.float)
    #yy = np.reshape(yy,(yy.size),order='F').astype(np.float)
    xx1 = xx[np.where(np.logical_and(np.isnan(xx)==False,np.isnan(yy)==False))]
    yy1 = yy[np.where(np.logical_and(np.isnan(xx)==False,np.isnan(yy)==False))]
    xy = np.vstack([xx1,yy1])
    z = gaussian_kde(xy)(xy)
    sorted_index = np.argsort(z)
    z = z[sorted_index]
    xx1 = xx1[sorted_index]
    yy1 = yy1[sorted_index]
    line_1_1 = np.array([0.98 * np.min(xy),1.01 * np.max(xy)])
    plt.scatter( xx1 , yy1 , s=50, c=z, cmap='jet', marker='.')
    plt.plot(line_1_1 , line_1_1,'--k')
    plt.xlim(line_1_1[0], line_1_1[-1])
    plt.ylim(line_1_1[0], line_1_1[-1])
    plt.xlabel(vble + ' reconstruido ' + units)
    #plt.ylabel(u'Q medido '+r'$[m^3/s]$')
    plt.title("R2 = {:.2f}".format(sc.spearmanr(xx1,yy1)[0,1]))
    return fig













