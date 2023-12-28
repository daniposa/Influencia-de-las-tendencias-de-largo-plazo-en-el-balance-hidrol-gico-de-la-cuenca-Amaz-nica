# -*- coding: utf-8 -*-
#==============================================================================
#------------------------------------------------------------------------------
# -- RECONSTRUCCION DE SERIES DE TIEMPO USANDO FUNCIONES ORTOGONALES EMPIRICAS
#------------------------------------------------------------------------------
#==============================================================================
"""
Created on Mon Mar 09 18:57:30 2020

@author: Daniela
"""
#==============================================================================
# -- Importar los modulos requeridos
#==============================================================================

import numpy as np
import pandas as pd
import Reconstruccion_fun3_20190915 as f
import matplotlib.pyplot as plt
import random as random
import Figuras as Figuras
import time as time
#==============================================================================
# -- Cargar datos de la ANA
#==============================================================================
# Ruta de la carpeta raiz
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/'

# Cargar todos los datos sin reconstruir
ruta_csvtesis = raiz + 'datos_crudos_rpetrds.csv'
all_ds=pd.read_csv(ruta_csvtesis,parse_dates=True,header=0,index_col=0)

# Ruta guardar matrices de reconstrucción
ruta_reconstruccion_R = raiz + 'reconstruccion/R/reconstruccion_rez/' 
ruta_reconstruccion_P = raiz + 'reconstruccion/P/reconstruccion_rez/' 
ruta_reconstruccion_ETR = raiz + 'reconstruccion/ETR/reconstruccion_rez/'
ruta_reconstruccion_dS = raiz + 'reconstruccion/dS/reconstruccion_rez/'

# Ruta de los metadatos
ruta_metadatos = raiz + 'Q/ANA/usar/metadatos10.csv'

# Ruta guardar las figuras de los Scatter-plots
ruta_fig_experimentos_R = ruta_reconstruccion_R + 'scatter_bandasP5P95/'
ruta_fig_experimentos_P = ruta_reconstruccion_P + 'scatter_bandasP5P95/'
ruta_fig_experimentos_ETR = ruta_reconstruccion_ETR + 'scatter_bandasP5P95/'
ruta_fig_experimentos_dS = ruta_reconstruccion_dS + 'scatter_bandasP5P95/'

#==============================================================================
# -- Cargar datos
#==============================================================================
#- cargar metadatos
metadatos=pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')

#- Recortar datos al periodo escogido:
start = pd.to_datetime('02/01/1995')# formato mm/dd/yyy
end = pd.to_datetime('02/01/2015')# formato mm/dd/yyy
all_ds = all_ds.loc[pd.date_range(start,end,freq='MS'),:]

del all_ds['R_99999999']# La serie no existe, está vacía

#==============================================================================
# -- Estandarizar las series
#==============================================================================
# Estandarizacion de las series para media 0 y desvest 1.
#- Aplicar la funcion estandarizadora:
all_stn_ds , all_mea , all_std , all_min = f.fn_stn(all_ds)

#==============================================================================
# -- Construir matriz base de reconstrucción
#==============================================================================
# Seleccionar las series que tienen menos del 15% de valores faltantes para
# base de reconstrucción
notnan_st = all_ds.notna().sum(axis=0)
numeses = np.size(all_ds.index)
porc_notnan = notnan_st.copy()
porc_notnan[:][:] = 100 * notnan_st.values / numeses
not_nan_lst = porc_notnan.index[porc_notnan.ge(85).values].values #- 175 estaciones con más del 85% de datos. tiempos con menos de 18 estaciones sin dato

#- crear matriz base de reconstrucción
base_stn_ds = all_stn_ds.loc[:,not_nan_lst]

#- matriz de reconstrucción rezagada
base_stn_ds_2 = base_stn_ds.copy()
rez1 = base_stn_ds.shift().add_suffix('rez1')
rez2 = base_stn_ds.shift(2).add_suffix('rez2')
rez3 = base_stn_ds.shift(3).add_suffix('rez3')
rez4 = base_stn_ds.shift(4).add_suffix('rez4')
rez5 = base_stn_ds.shift(5).add_suffix('rez5')
rez6 = base_stn_ds.shift(6).add_suffix('rez6')
base_stn_ds_2 = pd.concat([base_stn_ds_2 , rez1 , rez2 , rez3 , rez4 , rez5 , rez6] , axis=1)

#==============================================================================
# -- Reconstruccion
#==============================================================================

#- crear matriz para guardar los resultados de la reconstruccion
all_ds_reconstruidas = all_ds.copy() * 0.0

series=all_ds.columns

for serie in series:
    #serie=series[4]
    print(serie)
    #- extraer serie del DataFrame
    serie_stn = all_stn_ds.loc[:,serie].copy()
    #- reconstruccion definitiva
    serie_stn_copy = serie_stn.copy()
    #- agrandar matriz base con la serie a reconstruir
    if (not_nan_lst == serie).sum()==0:
        #in_stn_ds=base_stn_ds.copy().join(serie_stn_copy) # - matriz única
        in_stn_ds=base_stn_ds_2.copy().join(serie_stn_copy) # - matriz rezagada
    else:
        #in_stn_ds = base_stn_ds.copy() #- matriz única
        in_stn_ds = base_stn_ds_2.copy() #- matriz rezagada
        in_stn_ds.loc[:,serie] = serie_stn_copy
    #- reconstruir
    in_mea = all_mea.copy()
    in_std = all_std.copy()
    in_min = all_min.copy()
    porc_var = 0.925
    serie_reconstruida = f.recons_serie_dani(serie, in_stn_ds, in_mea, in_std, in_min, porc_var)
    all_ds_reconstruidas.loc[:,serie]=serie_reconstruida.copy()

all_ds_reconstruidas.to_csv( raiz + 'reconstruccion/datos_recons_rpetrds_rez.csv')

