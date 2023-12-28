# -*- coding: utf-8 -*-
#==============================================================================
#------------------------------------------------------------------------------
# -- MATRICES VALIDACION RECONSTRUCCION DE SERIES DE TIEMPO USANDO FUNCIONES ORTOGONALES EMPIRICAS
#------------------------------------------------------------------------------
#==============================================================================
"""
Created on Tue Jun 09 08:23:42 2015

Este programa usa las series de R , P , ETR y dS para realizar una validación 
del método de reconstrucción usando funciones ortogonales empíricas

@author: Daniela Posada Gil
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
# -- Experimentos
#==============================================================================
#- crear matriz para guardar los resultados de los experimentos
columns1=range(21) #- 0:Original, 1-20:Experimentos
columns2=['min','med','max','p5','p50','p95']#minimo, medio, maximo, percentil 5%, percentil 50%, percentil 95% entre los experimentos
columns=columns1+columns2

#- crear matriz para guardar los resultados de la reconstruccion
all_ds_reconstruidas = all_ds.copy() * 0.0

#- comenzar ejecución de los experimentos
time2=time.time()
series=all_ds.columns

for serie in series[372:]:
    #serie=series[4]
    print(serie)
    experimento_st = pd.DataFrame(index=all_ds.index,columns=columns)
    experimento_st.loc[:,0] = all_ds.loc[:,serie].copy()
    #- extraer serie del DataFrame
    serie_stn = all_stn_ds.loc[:,serie].copy()
    
    #- encontrar índices donde NO hay faltantes
    notna_index = serie_stn.index[serie_stn.notna().values].values
    nan_index = serie_stn.index[serie_stn.isna().values].values
    num_remover = notna_index.size/10 #- numero de datos a remover (10%)
    
    #- para cada experimento:
    for experimento in range(1,21):
        #experimento=1
        time0 = time.time()
        #- ordenar aleatoriamente los indices
        random_positions = range(notna_index.size)
        random.shuffle(random_positions)
        random_positions = np.array(random_positions[:num_remover*10]).reshape((10,num_remover))
        
        #- ejecutar experimento para cada fecha
        for positions in random_positions:
            #positions=random_positions[0,:]
            serie_stn_copy = serie_stn.copy() #- crear copia para remover datos
            indices_removidos = notna_index[positions]
            serie_stn_copy.loc[indices_removidos] = np.nan #- remover datos de la copia
            
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
            porc_var = 0.925 #- matriz unica
            #porc_var =0.8550848 #- matriz rezagada
            serie_reconstruida = f.recons_serie_dani(serie, in_stn_ds, in_mea, in_std, in_min, porc_var)
            
            #- guardar resultados
            experimento_st.loc[indices_removidos,experimento] = serie_reconstruida.loc[indices_removidos].values
            #plt.figure(figsize=(15,3.5))
            #all_ds.loc[:,serie].plot()
            #serie_reconstruida.plot(ls='--',c='k')
        experimento_st.loc[nan_index,experimento] = serie_reconstruida.loc[nan_index].values
        time1=time.time()
        print('    duración experimento '+str(experimento)+' : '+str(time1-time0))
    
    #- calcular estadísticas de los experimentos:
    experimento_st.loc[:,'min'] = experimento_st.loc[:,range(1,21)].min(axis=1).values
    experimento_st.loc[:,'med'] = experimento_st.loc[:,range(1,21)].mean(axis=1).values
    experimento_st.loc[:,'max'] = experimento_st.loc[:,range(1,21)].max(axis=1).values
    experimento_st.loc[:,'p5'] = np.nanpercentile(experimento_st.loc[:,range(1,21)].values.astype(np.float),5,axis=1)
    experimento_st.loc[:,'p50'] = np.nanpercentile(experimento_st.loc[:,range(1,21)].values.astype(np.float),50,axis=1)
    experimento_st.loc[:,'p95'] = np.nanpercentile(experimento_st.loc[:,range(1,21)].values.astype(np.float),95,axis=1)
    
    #- dibujar figuras
    x = experimento_st.index
    ymin = experimento_st.loc[:,'min'].values
    ymax = experimento_st.loc[:,'max'].values
    ymedia = experimento_st.loc[:,'med'].values
    yall = experimento_st.loc[:,range(1,21)].values.astype(np.float)
    yorig = experimento_st.loc[:,0].values
    vble = serie[:-9]
    units = '[mm/mes]'
    fig=Figuras.fig_seriesyscatter2(serie, x, ymin, ymedia, ymax, yall, yorig, vble, units)
    if serie[:-8] == 'R_':
        plt.savefig(ruta_fig_experimentos_R + serie + '_med.png' , dpi=300)
        experimento_st.to_csv( ruta_reconstruccion_R + serie + '.csv')
    elif serie[:-8] == 'P_':
        plt.savefig(ruta_fig_experimentos_P + serie + '_med.png' , dpi=300)
        experimento_st.to_csv( ruta_reconstruccion_P + serie + '.csv')
    elif serie[:-8] == 'ETR_':
        plt.savefig(ruta_fig_experimentos_ETR + serie + '_med.png' , dpi=300)
        experimento_st.to_csv( ruta_reconstruccion_ETR + serie + '.csv')
    if serie[:-8] == 'dS_':
        plt.savefig(ruta_fig_experimentos_dS + serie + '_med.png' , dpi=300)
        experimento_st.to_csv( ruta_reconstruccion_dS + serie + '.csv')
    
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

    
#    plt.savefig(ruta_fig_experimentos + serie + '_med.png' , dpi=300)
    
#    x=experimento_st.index
#    ymin=experimento_st.loc[:,'p5'].values
#    ymax=experimento_st.loc[:,'p95'].values
#    ymedia=experimento_st.loc[:,'p50'].values
#    yall=experimento_st.loc[:,range(1,21)].values
#    yorig=all_ds.loc[:,serie].values
#    fig2=Figuras.fig_seriesyscatter2(serie, x, ymin, ymedia, ymax, yall, yorig)
#    plt.savefig(ruta_fig_experimentos + serie + '_perc.png' , dpi=300)
    
    #- guardar resultados
#    if serie[:-8] == 'R_':
#        experimento_st.to_csv( ruta_reconstruccion_R + serie + '.csv')
#    elif serie[:-8] == 'P_':
#        experimento_st.to_csv( ruta_reconstruccion_P + serie + '.csv')
#    elif serie[:-8] == 'ETR_':
#        experimento_st.to_csv( ruta_reconstruccion_ETR + serie + '.csv')
all_ds_reconstruidas.to_csv( raiz + 'reconstruccion/datos_recons_rpetrds_rez.csv')

time3=time.time()
print(str(time3-time2))