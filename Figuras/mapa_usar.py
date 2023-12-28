# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 23:38:29 2020
Crea el mapa de estaciones usadas
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
ruta_metadatos = raiz + 'Q/ANA/usar/metadatos11.csv'
ruta_resultados = raiz + 'reconstruccion/IndicadoresError/'
#- Cargar metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')

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

values = metadatos['3M3V'].values[:-1]
error = 'Used'
markercolor1 = 'white'
markercolor2 = 'k'
umbral =0.7
figura = fig.mapa_puntos_binarios(values, latitudes, longitudes, umbral, error, extent, ruta_bordecuenca, ruta_drenaje, alpha = 1., markercolor1=markercolor1,markercolor2=markercolor2)
plt.savefig(ruta_resultados + 'Usar_ENG.png' , dpi = 300, bbox_inches = 'tight')
plt.close(figura)