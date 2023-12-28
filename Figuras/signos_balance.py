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
ruta_histograma = raiz + 'infoCalculada/Tendencias/histograma_balance_signos.png'
ruta_mapa = raiz + 'infoCalculada/Tendencias/mapa_balance_signos.png'
ruta_histograma2 = raiz + 'infoCalculada/Tendencias/histograma_balance_tend.png'
ruta_mapa2 = raiz + 'infoCalculada/Tendencias/mapa_balance_tend.png'
ruta_tendencias = raiz + 'InfoCalculada/Tendencias/tendencias_Sen.csv'

#- Cargar metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
usar = metadatos['usar'][:] == 1
metadatos = metadatos.loc[usar,:]
series = metadatos.index
#- Cargar resultados
tendencias = pd.read_csv(ruta_tendencias, index_col=0, encoding = 'utf8')
tendencias = tendencias.loc[usar,:]

#==============================================================================
#- Consistencia signos
#==============================================================================
signos = np.sign(tendencias)
signosP = signos['P'].values
signosETR = signos['ETR'].values
signosR = signos['R'].values

consistencia = []
for i in np.arange(signosP.size):
    P,ETR,R = (signosP[i], signosETR[i], signosR[i])
    consistencia.append(np.logical_and(P>0.,np.logical_or(ETR>0.,R>0.)) or np.logical_and(P==0.,ETR+R==0.) or np.logical_and(P<0.,np.logical_or(ETR<0.,R<0.)))
consistencia = np.array(consistencia)
#==============================================================================
#- Histograma consistencia signos
#==============================================================================
plt.figure()

X = [0., 1.]
Y = [(consistencia == False).sum()/float(consistencia.size), (consistencia == True).sum()/float(consistencia.size)]
plt.bar(X,Y, linewidth = 0.2, edgecolor = 'k')
#plt.xlabel(u"[%]")
plt.ylabel(u"frecuencia [%]")
plt.title(r"Consistencia signos de las tendencias")
plt.savefig(ruta_histograma, dpi=300, bbox_inches="tight")


#==============================================================================
#- Mapas consistencia signos
#==============================================================================
latitudes = metadatos['latitud'][:].values
longitudes = metadatos['longitud'][:].values

#alpha = 1.
#markercolor = 'darkred'#R:'blue'# P:'cyan'# ETR:'gold'# dS:'darkred'
extent = [-21., 6., -80.2, -49.2]#[llcrnrlat,urcrnrlat,llcrnrlon,urcrnrlon]

ruta_bordecuenca = [raiz + 'InfoOrganizada/00_GIS/amazlm_1608', u'Cuenca Amazonica']
ruta_drenaje = [raiz + 'InfoOrganizada/00_GIS/red_estaciones_clip', u'Drenaje']

values = consistencia

error = ""
markercolor1 = 'orangered'
markercolor2 = 'green'
umbral =0.7
figura = fig.mapa_puntos_binarios(values, latitudes, longitudes, umbral, error, extent, ruta_bordecuenca, ruta_drenaje, alpha = 1., markercolor1=markercolor1,markercolor2=markercolor2)
#plt.title(r"Consistencia signos de las tendencias")
plt.title("Trend sign consistency")
#- guardar
plt.savefig(ruta_mapa , dpi = 300, bbox_inches = 'tight')


#==============================================================================
#- Consistencia magnitudes
#==============================================================================
metadatos = metadatos.iloc[consistencia,:]
tendencias = tendencias.iloc[consistencia,:] * 12.

error_bal_tend = 100.*(tendencias['P'] - tendencias['ETR'] - tendencias['R'])/((np.abs(tendencias['P']) + np.abs(tendencias['ETR']) + np.abs(tendencias['R']))/3.)
error_bal_tend = error_bal_tend.fillna(0.)

#==============================================================================
#- Histograma consistencia signos
#==============================================================================
plt.figure()

yR = error_bal_tend
#yRpos = yR[yR > 0.]
bars = np.histogram(yR, bins=10)
x = 0.5*(bars[1][:-1] + bars[1][1:])
wid = bars[1][1:]-bars[1][:-1]
y = 100.*bars[0].astype(float)/bars[0].sum().astype(float)
histR = plt.bar(x,y,width=wid)
plt.xlabel(u"[%]")
plt.ylabel(u"frecuencia [%]")
plt.title("Error en balance de tendencias\n relativo al promedio de las tendencias")
plt.savefig(ruta_histograma2, dpi=300, bbox_inches="tight")


#==============================================================================
#- Mapas consistencia signos
#==============================================================================
latitudes = metadatos['latitud'][:].values
longitudes = metadatos['longitud'][:].values

#alpha = 1.
#markercolor = 'darkred'#R:'blue'# P:'cyan'# ETR:'gold'# dS:'darkred'
extent = [-21., 6., -80.2, -49.2]#[llcrnrlat,urcrnrlat,llcrnrlon,urcrnrlon]

ruta_bordecuenca = [raiz + 'InfoOrganizada/00_GIS/amazlm_1608', u'Cuenca Amazonica']
ruta_drenaje = [raiz + 'InfoOrganizada/00_GIS/red_estaciones_clip', u'Drenaje']

values = yR.values
minmax_array = np.array([np.min([0.,np.min(np.abs(values))]),np.max(np.abs(values)),np.min(values),np.max(values)])
minmax = pd.DataFrame(data = minmax_array,index=['min','max','min2','max2'],columns=[0])

error = "[%]"
#markercolor = 'red'
markercolor2 = 'blue'
markercolor3 = 'red'
umbral = 0.0
leg_minval = minmax[0]['min2']
leg_maxval = minmax[0]['max2']
leg_maxabs = minmax[0]['max']
leg_minabs = minmax[0]['min']
exp = 0.5
zeroval = 2.0
sizes = fig.sizes_fun(values = np.abs(values), maxabs = leg_maxabs, minabs = leg_minabs, exp = exp, zeroval = zeroval)
figura = fig.mapa_puntos_sizes(values, latitudes, longitudes, umbral, sizes, error, extent, ruta_bordecuenca, ruta_drenaje, alpha = 0.8, markercolor1 = markercolor2, markercolor2 = markercolor3, leg_minval = leg_minval, leg_maxval = leg_maxval, leg_maxabs = leg_maxabs, leg_minabs = leg_minabs)#, exp=exp, zeroval = zeroval)
plt.title("Error en balance de tendencias\n relativo al promedio de las tendencias")

#- guardar
plt.savefig(ruta_mapa2 , dpi = 300, bbox_inches = 'tight')
