# -*- coding: utf-8 -*-
"""
Created on Thu Sep 05 20:46:23 2019
Crea una matriz con todas los datos crudos de R, P, ETR y dS
@author: Daniela
"""

#==============================================================================
#- Importar módulos
#==============================================================================
#import rst2series as rst2series
import pandas as pd
import Raster as rst
import numpy as np
import SeriesTiempo as st
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib as matp
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
import copy as cp
import time as time

#==============================================================================
#- Definir rutas de carpetas base
#==============================================================================
#- carpeta raiz
root = 'H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/'

#- rutas de archivos Base
ruta_metadatos = root + 'Q/ANA/usar/metadatos10.csv'

#- cargar metadatos de estaciones usadas
metadatos = pd.read_csv(ruta_metadatos,index_col=0)
lista_estaciones = metadatos.index #- lista de estaciones usadas

lista_R = ['R_'+str(codigo) for codigo in list(lista_estaciones)]
lista_P = ['P_'+str(codigo) for codigo in list(lista_estaciones)]
lista_ETR = ['ETR_'+str(codigo) for codigo in list(lista_estaciones)]
lista_dS = ['dS_'+str(codigo) for codigo in list(lista_estaciones)]

lista_rpetrds = np.array(zip(lista_R, lista_P, lista_ETR, lista_dS)).flatten()

fecha_ini = pd.to_datetime('01/01/1974', format='%d/%m/%Y')
fecha_fin = pd.to_datetime('01/12/2017', format='%d/%m/%Y')
datos_rpetrds=pd.DataFrame(index = pd.date_range(start = fecha_ini , end = fecha_fin , freq='MS') , columns=lista_rpetrds)

for estacion in lista_estaciones:
    #estacion=lista_estaciones[0]
    #==============================================================================
    #- Definir rutas de series
    #==============================================================================
    #- rutas P
    ruta_PP = root + 'P/P_media_mensual/' + str(estacion) + '.csv'
    
    #- rutas ETR
    ruta_ETRP = root + 'ETR/ETR_media_mensual/' + str(estacion) + '.csv'
    
    #- rutas dS
    ruta_dSP= root + 'dS/dS_media_mensual/' + str(estacion) + '.csv'
    
    #- rutas Q
    ruta_RP = root + 'R/R_media_mensual/' + str(estacion) + '.csv'
    
    #==============================================================================
    #- Leer datos
    #==============================================================================    
    #- datos P
    PP = pd.read_csv(ruta_PP , index_col = 0 , header = None)
    index = pd.to_datetime(PP.index, format='%d/%m/%Y')
    column= 'P_' + str(estacion)
    datos_rpetrds[column][index] = PP.values
    
    #- datos ETR
    ETRP = pd.read_csv(ruta_ETRP , index_col = 0 , header = None)
    index = pd.to_datetime(ETRP.index, format='%d/%m/%Y')
    column= 'ETR_' + str(estacion)
    datos_rpetrds[column][index] = ETRP.values
    
    #- datos dS
    dSP = pd.read_csv(ruta_dSP , index_col = 0 , header = None)
    index = pd.to_datetime(dSP.index, format='%d/%m/%Y')
    column= 'dS_' + str(estacion)
    datos_rpetrds[column][index] = dSP.values
    
    try:
        #- datos R
        RP = pd.read_csv(ruta_RP , index_col = 0 , header = None)
        index = pd.to_datetime(RP.index, format='%d/%m/%Y')
        column= 'R_' + str(estacion)
        datos_rpetrds[column][index] = RP.values
    except:
        None

#==============================================================================
#- Guardar datos
#==============================================================================
ruta_datos_crudos = root + 'datos_crudos_rpetrds.csv'
datos_rpetrds.to_csv( ruta_datos_crudos )

#==============================================================================
#- Graficar datos faltantes
#==============================================================================

completos = datos_rpetrds.notna().T.astype(int)
#completos = datos_rpetrds.loc[rango_fechas,:].notna().T.astype(int)
completos[completos==0.0] = np.nan
completos.loc[lista_P,:] = completos.loc[lista_P,:].values + 1 
completos.loc[lista_ETR,:] = completos.loc[lista_ETR,:].values + 2 
completos.loc[lista_dS,:] = completos.loc[lista_dS,:].values + 3 

ruta_figura_completos = root + 'datos_faltantes.png'
fig,ax = plt.subplots(figsize=(15,20))
cmap = plt.cm.get_cmap('jet',4)
bounds=[0.5,1.5,2.5,3.5,4.5]
norm = matp.colors.BoundaryNorm(bounds, cmap.N)
ax = plt.imshow(completos, aspect=40./18., cmap=cmap, norm=norm)
cbar = plt.colorbar(cmap=cmap, norm=norm , boundaries=bounds, ticks=[1,2,3,4])
cbar.ax.get_yaxis().set_ticks([])
cbar.ax.text(-0.2,0.875,'dS', ha='center', va='center')
cbar.ax.text(-0.2,0.625,'ETR', ha='center', va='center')
cbar.ax.text(-0.2,0.375,'P', ha='center', va='center')
cbar.ax.text(-0.2,0.125,'R', ha='center', va='center')
cbar.set_label('Variable')
plt.yticks(np.arange(0,440,4),lista_estaciones)
plt.xticks(np.arange(0,528,36),completos.columns[np.arange(0,528,36)].year)
plt.xlabel('Fecha')
plt.ylabel(u'Estación')
plt.subplots_adjust(left=0.03, bottom=0.03, right=1, top=0.97, wspace=0, hspace=0.05)
#plt.grid(True)
plt.savefig(ruta_figura_completos, dpi=300)

ruta_figura_completos2 = root + 'datos_faltantes_agregados.png'
completos = datos_rpetrds.notna().T.astype(int)
fig, ax = plt.subplots()
(completos.loc[lista_R,:].sum(axis=0) * 100. / 110.).plot(c='navy')
(completos.loc[lista_P,:].sum(axis=0) * 100. / 110.).plot(c='cyan')
(completos.loc[lista_ETR,:].sum(axis=0) * 100. / 110.).plot(c='gold')
(completos.loc[lista_dS,:].sum(axis=0) * 100. / 110.).plot(c='darkred')
plt.xlabel('Fecha')
plt.ylabel(u'Porcentaje de datos [%]')
plt.legend(['R','P','ETR','dS'])
plt.subplots_adjust(left=0.1, bottom=0.125, right=0.98, top=0.98, wspace=0.2, hspace=0.2)
plt.savefig(ruta_figura_completos2, dpi=300)

total_completos = completos.loc[lista_R,:].sum(axis=0) + completos.loc[lista_P,:].sum(axis=0) + completos.loc[lista_ETR,:].sum(axis=0) + completos.loc[lista_dS,:].sum(axis=0)
mob_sum = [np.sum(total_completos.values[i - 120: i + 120]) for i in range(120, 528 - 120)]
mob_sum_serie = total_completos.iloc[120:-120].copy()
mob_sum_serie[:] = mob_sum
max_index = mob_sum_serie.idxmax(axis=0)
fecha_ini = max_index - pd.DateOffset(months=120)
fecha_fin = max_index + pd.DateOffset(months=120)
rango_fechas = pd.date_range(fecha_ini , fecha_fin, freq='MS')
mob_sum_serie.plot()
