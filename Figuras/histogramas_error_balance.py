# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:55:54 2020
Crea histogramas de las tendencias
@author: Daniela
"""
#==============================================================================
#- Importar módulos
#==============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Figuras as fig

#==============================================================================
#- Cargar variables del disco
#==============================================================================
#- Definir rutas
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/'
ruta_metadatos = raiz + 'InfoOrganizada/Q/ANA/usar/metadatos12.csv'
ruta_histograma = raiz + 'infoCalculada/EvolucionBalance/histograma_error_balance.png'
ruta_mapa = raiz + 'infoCalculada/EvolucionBalance/mapa_error_balance.png'

#- Cargar metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
usar = metadatos['usar'][:] == 1
metadatos = metadatos.loc[usar,:]

#==============================================================================
#- Histograma error balance
#==============================================================================
plt.figure()

yR = 100. * metadatos.loc[:,'err_bal(mm/mes)'].values / metadatos.loc[:,'recRmlp(mm/mes)'].values
#yRpos = yR[yR > 0.]
bars = np.histogram(yR, bins=10)
x = 0.5*(bars[1][:-1] + bars[1][1:])
wid = bars[1][1:]-bars[1][:-1]
y = 100.*bars[0].astype(float)/bars[0].sum().astype(float)
histR = plt.bar(x,y,width=wid)
plt.xlabel(u"[%]")
plt.ylabel(u"frecuencia [%]")
plt.title(r"Error en balance relativo a R")
plt.savefig(ruta_histograma, dpi=300, bbox_inches="tight")


#==============================================================================
#- Mapas error balance
#==============================================================================
latitudes = metadatos['latitud'][:].values
longitudes = metadatos['longitud'][:].values

#alpha = 1.
#markercolor = 'darkred'#R:'blue'# P:'cyan'# ETR:'gold'# dS:'darkred'
extent = [-21., 6., -80.2, -49.2]#[llcrnrlat,urcrnrlat,llcrnrlon,urcrnrlon]

ruta_bordecuenca = [raiz + 'InfoOrganizada/00_GIS/amazlm_1608', u'Cuenca Amazonica']
ruta_drenaje = [raiz + 'InfoOrganizada/00_GIS/red_estaciones_clip', u'Drenaje']

values = yR
minmax_array = np.array([np.min([0.,np.min(np.abs(values))]),np.max(np.abs(values)),np.min(values),np.max(values)])
minmax = pd.DataFrame(data = minmax_array,index=['min','max','min2','max2'],columns=[0])

error = ""
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
figura = fig.mapa_puntos_sizes(values, latitudes, longitudes, umbral, sizes, error, extent, ruta_bordecuenca, ruta_drenaje, alpha = 0.8, markercolor1 = markercolor2, markercolor2 = markercolor3, leg_minval = leg_minval, leg_maxval = leg_maxval, leg_maxabs = leg_maxabs, leg_minabs = leg_minabs)#, exp=exp, zeroval = zeroval)
plt.title(r"Error en balance relativo a R")
#- guardar
plt.savefig(ruta_mapa , dpi = 300, bbox_inches = 'tight')


