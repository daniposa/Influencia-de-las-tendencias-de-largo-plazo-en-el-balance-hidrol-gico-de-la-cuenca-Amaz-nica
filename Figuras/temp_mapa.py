# -*- coding: utf-8 -*-
"""
Created on Sun Oct 06 10:36:56 2019
Función que crea Mapas de puntos con el tamaño relativo a una magnitud
@author: Daniela
"""
#==============================================================================
#- Importar módulos
#==============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os as os
from mpl_toolkits.basemap import Basemap
import Raster as raster
import Figuras as fig

#==============================================================================
#- Cargar variables del disco
#==============================================================================
#- Definir rutas
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/'
ruta_metadatos = raiz + 'Q/ANA/usar/metadatos10.csv'
ruta_resultados = raiz + 'reconstruccion/IndicadoresError/resumen_errores.csv'
rutas_figuras = {}
for i in ['EMAR','ENS','SESGO','CC','RECMR','RKS','TENDSEN','TENDMK']:
    rutas_figuras[i] = raiz + 'reconstruccion/IndicadoresError/mapas_errores/' + i + '/'
#- Cargar metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
#- Cargar resultados
resultados = pd.read_csv(ruta_resultados, index_col=0, encoding = 'utf8')
#==============================================================================
#- Cargar entradas de la función
#==============================================================================
latitudes = metadatos['latitud'][:].values[:-1]
longitudes = metadatos['longitud'][:].values[:-1]

#alpha = 1.
#markercolor = 'darkred'#R:'blue'# P:'cyan'# ETR:'gold'# dS:'darkred'
extent = [-21., 6., -80.2, -49.2]#[llcrnrlat,urcrnrlat,llcrnrlon,urcrnrlon]

ruta_bordecuenca = [raiz + '00_GIS/amazlm_1608', u'Cuenca Amazonica']
ruta_drenaje = [raiz + '00_GIS/red_estaciones_clip', u'Drenaje']
minmax_array = np.array([[3.,75.,3.,75.],[0.,.99,-.80,.99],[0.,15.,-15.,12.],[0.05,1.,0.05,1.],[3.,98.,3.,98.],[0.,24.,-13.,24.]])
minmax = pd.DataFrame(data = minmax_array,index=['EMAR','ENS','SESGO','CC','RECMR', 'TENDSEN'],columns=['min','max','min2','max2'])

for columna in resultados.columns:
    #columna = resultados.columns[0]
    values = resultados[columna].values[:-1]
    err_name = columna.split('_')[0][1:]
    print(columna)
    #variable = columna.split('_')[1]
    if columna[0] == 'm':# and 
        error = columna[1:]# + ' medio'
        #markercolor = 'red'
        if err_name == 'RKS' or err_name == 'TENDMK':
            markercolor1 = 'orangered'
            markercolor2 = 'green'
            umbral =0.7
            figura = fig.mapa_puntos_binarios(values, latitudes, longitudes, umbral, error, extent, ruta_bordecuenca, ruta_drenaje, alpha = 1., markercolor1=markercolor1,markercolor2=markercolor2)
        else:
            markercolor2 = 'blue'
            markercolor3 = 'red'
            umbral = 0.0
            leg_minval = minmax['min2'][err_name]
            leg_maxval = minmax['max2'][err_name]
            leg_maxabs = minmax['max'][err_name]
            leg_minabs = minmax['min'][err_name]
            sizes = 2.0 + ((np.abs(values)-leg_minabs)*(100./(leg_maxabs - leg_minabs))+1.)**0.55
            if err_name == 'CC':
                titulo_cc = u"\u03C1s" + columna[3:]
                figura = fig.mapa_puntos_sizes(values, latitudes, longitudes, umbral, sizes, titulo_cc, extent, ruta_bordecuenca, ruta_drenaje, alpha = 0.8, markercolor1 = markercolor2, markercolor2 = markercolor3, leg_minval = leg_minval, leg_maxval = leg_maxval, leg_maxabs = leg_maxabs, leg_minabs = leg_minabs)
            else:
                figura = fig.mapa_puntos_sizes(values, latitudes, longitudes, umbral, sizes, error, extent, ruta_bordecuenca, ruta_drenaje, alpha = 0.8, markercolor1 = markercolor2, markercolor2 = markercolor3, leg_minval = leg_minval, leg_maxval = leg_maxval, leg_maxabs = leg_maxabs, leg_minabs = leg_minabs)
        #- guardar
        plt.savefig(rutas_figuras[err_name] + columna + '.png' , dpi = 300, bbox_inches = 'tight')
        plt.close(figura)
    else:
        error = 'P(' + columna[1:] + ') favorable'
        markercolor1 = 'orangered'
        markercolor2 = 'green'
        umbral =0.7
        figura = fig.mapa_puntos_binarios(values, latitudes, longitudes, umbral, error, extent, ruta_bordecuenca, ruta_drenaje, alpha = 1., markercolor1=markercolor1,markercolor2=markercolor2)
        #- guardar
        plt.savefig(rutas_figuras[err_name] + columna + '.png' , dpi = 300, bbox_inches = 'tight')
        plt.close(figura)
## Definir el tamaño de la figura
#plt.figure(figsize=(5.,5.))
#
## En qué bordes aparecen las cordenadas
#drawlat=[True,False,False,False]
#drawlon=[False,False,False,True]
#
## Trazar mapa
#mapa = Basemap(projection='mill',llcrnrlat = extent[0],urcrnrlat = extent[1],llcrnrlon = extent[2], urcrnrlon = extent[3],resolution='h')
#mapa.drawmapboundary(fill_color='lightgrey')
#mapa.fillcontinents(color='white',lake_color='lightgrey')
#
## Dibujar shapes en el mapa
#shape_info= mapa.readshapefile(ruta_bordecuenca[0], ruta_bordecuenca[1], color='k', linewidth=2.)
#shape_info2= mapa.readshapefile(ruta_drenaje[0], ruta_drenaje[1], color='k')
#
## Dibujar datos
#for i in np.arange(1,latitudes.size + 1):
#    x,y = mapa(longitudes[i - 1], latitudes[i - 1])
#    mapa.plot(x, y, marker = 'o', color = markercolor, ls = '', markeredgecolor='k', markersize = sizes[i - 1], alpha = alpha)
#
## Dibujar coordenadas en los bordes
#mapa.drawparallels(np.arange(-20.0,6.0,5.),linewidth=0.,labels=drawlat)#,family='Helvetica')
#mapa.drawmeridians(np.arange(-80.,-45.,5.),linewidth=0.,labels=drawlon)#,family='Helvetica')
#
##- Construir leyenda
#marcador_minimo = mpl.lines.Line2D([], [], marker = 'o', color = markercolor, ls = '', markeredgecolor='k',markersize = min(sizes), alpha = alpha, label= str(min(values)))
#marcador_maximo = mpl.lines.Line2D([], [], marker = 'o', color = markercolor, ls = '', markeredgecolor='k',markersize = max(sizes), alpha = alpha, label= str(max(values)))
#leg = plt.legend(handles = [marcador_minimo, marcador_maximo], loc='lower left', title = error)
#
#plt.show()