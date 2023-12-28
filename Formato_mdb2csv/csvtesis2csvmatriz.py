# -*- coding: utf-8 -*-
"""
Created on Wed May 01 13:41:42 2019

Sirve para cargar los datos en el formato csv usado en la tesis y construir la matriz de datos a reconstruir para utilizar

@author: Daniela
"""

#==============================================================================
# Importar módulos
#==============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import datetime as datetime

#==============================================================================
# Rutas
#==============================================================================

ruta_csvtesis='G:/Mi unidad/Maestria/Tesis/2019-1Final/01_DATOS/InfoOrganizada/Q/ANA/'

#==============================================================================
# Rango temporal
#==============================================================================
# Leer los datos
matriz_datos=pd.read_csv(ruta_csvtesis+'matriz_Q.csv',parse_dates=True,header=0,index_col=0)
matriz_metadatos=pd.read_csv(ruta_csvtesis+'metadatos.csv',header=0,index_col=0)

# Conocer los nan
matriz_condatos_array=np.isnan(matriz_datos.values.astype(np.float64))==False
matriz_condatos=pd.DataFrame(matriz_condatos_array,index=matriz_datos.index,columns=matriz_datos.columns)

# Conocer las fechas
datetimes=pd.to_datetime(matriz_condatos.index)
num_fechas_ini=len(matriz_datos.index)#1034
num_estaciones_ini=len(matriz_datos.columns)#203

# Definir umbral de datos para el rango temporal de estudio
umbral_fechas=0.5
cumple_umbral=matriz_condatos.sum(axis=1)>matriz_condatos.sum(axis=1).quantile(umbral_fechas)
matriz_cumpleumbral=matriz_condatos[:][cumple_umbral].copy()
matriz_cumpleumbral.sum(axis=1).plot()
matriz_cumpleumbral_array=matriz_cumpleumbral.values

#x_lims=[0,matriz_condatos_array.shape[1]]
#y_lims=[datetimes[-1],datetimes[0]]
#y_lims=mdates.date2num(y_lims)
#fig,ax=plt.subplots(figsize=(5,800))
#ax.yaxis_date()
#ax.imshow(matriz_condatos,cmap='binary',extent = [x_lims[0], x_lims[1],  y_lims[0], y_lims[1]], aspect=0.00625)
#plt.xticks(np.arange(0,matriz_condatos_array.shape[1]),matriz_condatos.columns,rotation='vertical')
#ano=unicode('Año',encoding='utf-8')
#estacion_texto=unicode('Estación',encoding='utf-8')
#plt.ylabel(ano)
#plt.xlabel(estacion_texto)
#plt.yticks(np.arange(0,matriz_condatos_array.shape[0]),matriz_condatos.index)

datetimes=pd.to_datetime(matriz_cumpleumbral.index)
rango_fechas=pd.date_range(datetimes[0],datetimes[-1],freq='MS')

x_lims=[0,matriz_cumpleumbral_array.shape[1]]
y_lims=[datetimes[-1],datetimes[0]]
y_lims=mdates.date2num(y_lims)
fig,ax=plt.subplots(figsize=(5,800))
ax.yaxis_date()
ax.imshow(matriz_cumpleumbral,cmap='binary',extent = [x_lims[0], x_lims[1],  y_lims[0], y_lims[1]], aspect=0.00625)
plt.xticks(np.arange(0,matriz_cumpleumbral_array.shape[1]),matriz_cumpleumbral.columns,rotation='vertical')
ano=str('Año')
estacion_texto=str('Estación')
plt.ylabel(ano)
plt.xlabel(estacion_texto)

#==============================================================================
# Estaciones a usar
#==============================================================================
# Umbral de datos necesarios de una estación en el rango de tiempo
umbral_estacion=0.6
num_fechas_fin=len(rango_fechas)#516

# Estaciones que cumplen umbral
cumpleumbral2=((matriz_cumpleumbral.sum(axis=0)/float(num_fechas_fin))>umbral_estacion)
estaciones_cumpleumbral2=cumpleumbral2.index[cumpleumbral2.values]

# Construir matriz sólo con las estaciones que cumplen el umbral

matriz_cumpleumbral2=matriz_datos.loc[rango_fechas,estaciones_cumpleumbral2].copy()
matriz_cumpleumbral2.to_csv(ruta_csvtesis+'usar/matriz_Q.csv')

metadatos_cumpleumbral2=matriz_metadatos.loc[estaciones_cumpleumbral2.astype(int),:].copy()
metadatos_cumpleumbral2.to_csv(ruta_csvtesis+'usar/metadatos.csv')

















