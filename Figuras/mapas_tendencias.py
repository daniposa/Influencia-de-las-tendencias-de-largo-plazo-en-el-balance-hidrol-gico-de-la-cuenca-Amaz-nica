# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 18:11:38 2020
Genera los mapas de las tendencias de largo plazo
@author: Daniela
"""
#==============================================================================
#- Importar módulos
#==============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
import Figuras as fig

#==============================================================================
#- Cargar variables del disco
#==============================================================================
#- Definir rutas
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/'
ruta_metadatos = raiz + 'InfoOrganizada/Q/ANA/usar/metadatos11.csv'
ruta_resultados = raiz + 'InfoCalculada/Tendencias/figuras_ENG/'
ruta_tendencias = raiz + 'InfoCalculada/Tendencias/tendencias_Sen.csv'

#- Cargar metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
usar = metadatos['usar'][:] == 1
metadatos = metadatos.loc[usar,:]
#- Cargar resultados
tendencias = pd.read_csv(ruta_tendencias, index_col=0, encoding = 'utf8')
tendencias = tendencias.loc[usar,:]

#==============================================================================
#- Cargar entradas de la función
#==============================================================================
latitudes = metadatos['latitud'][:].values
longitudes = metadatos['longitud'][:].values

#alpha = 1.
#markercolor = 'darkred'#R:'blue'# P:'cyan'# ETR:'gold'# dS:'darkred'
extent = [-21., 6., -80.2, -49.2]#[llcrnrlat,urcrnrlat,llcrnrlon,urcrnrlon]

ruta_bordecuenca = [raiz + 'InfoOrganizada/00_GIS/amazlm_1608', u'Cuenca Amazonica']
ruta_drenaje = [raiz + 'InfoOrganizada/00_GIS/red_estaciones_clip', u'Drenaje']
#minmax_array = np.array([np.min([0.,np.min(np.abs(tendencias.values))]),np.max(np.abs(tendencias.values)),np.min(tendencias.values),np.max(tendencias.values)])
#minmax = pd.DataFrame(data = minmax_array,index=['min','max','min2','max2'],columns=[0])

for columna in tendencias.columns:
    #columna = tendencias.columns[0]
    minmax_array = np.array([np.min([0.,np.min(np.abs(tendencias[columna].values))]),np.max(np.abs(tendencias[columna].values)),np.min(tendencias[columna].values),np.max(tendencias[columna].values)])
    minmax_array = minmax_array * 12.
    minmax = pd.DataFrame(data = minmax_array,index=['min','max','min2','max2'],columns=[0])
    values = tendencias[columna].values * 12.
    if columna == 'dS':
        #error = u'd\u00b2' + columna[1:] + u'/dt\u00b2' + '\n' + u'[mm/año]'
        error = u'd\u00b2' + columna[1:] + u'/dt\u00b2' + '\n' + u'[mm/year]'
    else:
        #error = 'd' + columna + u'/dt'+ '\n' + u'[mm/año]'
        error = 'd' + columna + u'/dt'+ '\n' + u'[mm/year]'
    #markercolor = 'red'
    markercolor2 = 'blue'
    markercolor3 = 'red'
    umbral = 0.0
    leg_minval = minmax[0]['min2']
    leg_maxval = minmax[0]['max2']
    leg_maxabs = minmax[0]['max']
    leg_minabs = minmax[0]['min']
    exp = 0.65
    zeroval = 2.0
    sizes = fig.sizes_fun(values = np.abs(values), maxabs = leg_maxabs, minabs = leg_minabs, exp = exp, zeroval = zeroval)
    figura = fig.mapa_puntos_sizes2(values, latitudes, longitudes, umbral, sizes, error, extent, ruta_bordecuenca, ruta_drenaje, alpha = 0.8, markercolor1 = markercolor2, markercolor2 = markercolor3, leg_minval = leg_minval, leg_maxval = leg_maxval, leg_maxabs = leg_maxabs, leg_minabs = leg_minabs, exp=exp, zeroval = zeroval)
    #- guardar
    plt.savefig(ruta_resultados + columna + '.png' , dpi = 300, bbox_inches = 'tight')
    plt.close(figura)
    print(columna)

for columna in tendencias.columns:
    #columna = tendencias.columns[0]
    minmax_array = np.array([np.min([0.,np.min(np.abs(tendencias[columna].values))]),np.max(np.abs(tendencias[columna].values)),np.min(tendencias[columna].values),np.max(tendencias[columna].values)])
    minmax_array = minmax_array * 12.
    minmax = pd.DataFrame(data = minmax_array,index=['min','max','min2','max2'],columns=[0])
    values = tendencias[columna].values * 12.
    if columna == 'dS':
        #error = u'd\u00b2' + columna[1:] + u'/dt\u00b2' + '\n' + u'[mm/año]'
        error = u'd\u00b2' + columna[1:] + u'/dt\u00b2' + '\n' + u'[mm/year]'
    else:
        #error = 'd' + columna + u'/dt'+ '\n' + u'[mm/año]'
        error = 'd' + columna + u'/dt'+ '\n' + u'[mm/year]'
    #markercolor = 'red'
    markercolor2 = 'blue'
    markercolor3 = 'red'
    umbral = 0.0
    leg_minval = minmax[0]['min2']
    leg_maxval = minmax[0]['max2']
    leg_maxabs = minmax[0]['max']
    leg_minabs = minmax[0]['min']
    exp = 0.65
    zeroval = 2.0
    sizes = fig.sizes_fun(values = np.abs(values), maxabs = leg_maxabs, minabs = leg_minabs, exp = exp, zeroval = zeroval)
    figura = fig.mapa_puntos_sizes2(values, latitudes, longitudes, umbral, sizes, error, extent, ruta_bordecuenca, ruta_drenaje, alpha = 0.8, markercolor1 = markercolor2, markercolor2 = markercolor3, leg_minval = leg_minval, leg_maxval = leg_maxval, leg_maxabs = leg_maxabs, leg_minabs = leg_minabs, exp=exp, zeroval = zeroval)
    #- guardar
    plt.savefig(ruta_resultados + columna + '.png' , dpi = 300, bbox_inches = 'tight')
    plt.close(figura)
    print(columna)
