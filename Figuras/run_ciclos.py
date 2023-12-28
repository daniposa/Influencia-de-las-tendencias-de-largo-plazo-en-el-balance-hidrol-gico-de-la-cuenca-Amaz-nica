# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:39:29 2019
Graficar los ciclos de las variables original, reconstruida y de los
indicadores de error 
@author: Daniela
"""
#==============================================================================
#- Importar módulos requeridos
#==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Figuras as fig

#==============================================================================
#- Cargar variables del disco
#==============================================================================
#- Definir rutas
raiz = 'H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/reconstruccion/IndicadoresError/'
ruta_metadatos = 'H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Q/ANA/usar/metadatos10.csv'

#- Cargar metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
estaciones = metadatos.index.values

variables=['R','P','ETR','dS']

for estacion in estaciones:
    #estacion = '18460000'
    ruta_cicloR = raiz + 'R/ciclos_error_' + str(estacion) + '.csv'
    ruta_cicloP = raiz + 'P/ciclos_error_' + str(estacion) + '.csv'
    ruta_cicloETR = raiz + 'ETR/ciclos_error_' + str(estacion) + '.csv'
    ruta_ciclodS = raiz + 'dS/ciclos_error_' + str(estacion) + '.csv'
    
    ruta_figura = raiz + '/fig_ciclos_error/ciclos_error_' + str(estacion) + '.png'
    indicadores = ['EMAR','ENS','SESGO','CC','RECMR','RKS']
    
    #- Cargar ciclos
    ciclosR = pd.read_csv(ruta_cicloR, index_col=0, encoding = 'utf8')
    ciclosP = pd.read_csv(ruta_cicloP, index_col=0, encoding = 'utf8')
    ciclosETR = pd.read_csv(ruta_cicloETR, index_col=0, encoding = 'utf8')
    ciclosdS = pd.read_csv(ruta_ciclodS, index_col=0, encoding = 'utf8')
    
    ciclos={0:ciclosR, 1:ciclosP, 2:ciclosETR, 3:ciclosdS}
    
    figura, axs = plt.subplots(4, 4, sharex=True, figsize=(20,8))#, sharey=True)
    figura.subplots_adjust(hspace=0, wspace=0.2)
    for columna in range(4):
        axs[0,columna].set_title(variables[columna])
        axs[0,columna].errorbar(range(12), ciclos[columna]['media_obs'].values,ciclos[columna]['desvest_obs'].values,capsize=3)
        axs[0,columna].errorbar(range(12), ciclos[columna]['media_est'].values,ciclos[columna]['desvest_est'].values,capsize=3)
        axs[1,columna].errorbar(range(12), ciclos[columna]['mediaEMAR'].values,ciclos[columna]['desvestEMAR'].values,capsize=3)
        axs[2,columna].errorbar(range(12), ciclos[columna]['mediaSESGO'].values,ciclos[columna]['desvestSESGO'].values,capsize=3)
        axs[3,columna].errorbar(range(12), ciclos[columna]['mediaRECMR'].values,ciclos[columna]['desvestRECMR'].values,capsize=3)
        axs[3,columna].set_xticks(range(12))
        axs[3,columna].set_xticklabels(list(ciclos[columna].index))
    axs[0,0].set_ylabel('Obs y Est [mm]')
    axs[1,0].set_ylabel('EMAR [mm]')
    axs[2,0].set_ylabel('SESGO [mm]')
    axs[3,0].set_ylabel('RECMR [mm]')
    plt.suptitle(str(estacion))
    plt.savefig(ruta_figura, dpi=300)
    plt.close()






