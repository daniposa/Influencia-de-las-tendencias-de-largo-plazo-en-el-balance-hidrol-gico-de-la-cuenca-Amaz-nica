# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 14:24:26 2020
Construye las gráficas de EMD
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
#- Definir rutas
#==============================================================================
#- Definir rutas
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/'

#- Ruta metadatos
#ruta_metadatos = raiz + 'InfoOrganizada/Q/ANA/usar/metadatos10.csv'
#ruta_metadatos2 = raiz + 'InfoOrganizada/Q/ANA/usar/metadatos11.csv'
ruta_metadatos = raiz + 'InfoOrganizada/Q/ANA/usar/metadatos11.csv'

#- Ruta de las series de tiempo
ruta_series = raiz + 'InfoOrganizada/reconstruccion/datos_recons_rpetrds_rez_definitiva.csv'

#- Ruta resultados
ruta_resultados = raiz + 'infoCalculada/EMD/'

#==============================================================================
#- Cargar variables generales
#==============================================================================
#- Cargar metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
#metadatos.insert(19,'recRmlp(mm/mes)',0.)
#metadatos.insert(20,'recPmlp(mm/mes)',0.)
#metadatos.insert(21,'recETRmlp(mm/mes)',0.)
#metadatos.insert(22,'recdS/dtmlp(mm/mes)',0.)
#- Cargar series de tiempo
series_reconstruidas = pd.read_csv(ruta_series, index_col=0, encoding = 'utf8')

series = metadatos.index[:-1]
series_usar = metadatos.index[metadatos['3M3V'].values.astype(bool)]
#==============================================================================
#- cambiar dS por dS/dt
#==============================================================================
for serie in series:
    #serie = series[0]
    nombre = 'dS_' + str(serie)
    valores = series_reconstruidas[nombre].values
    gradiente = np.gradient(valores)    
    series_reconstruidas[nombre] = gradiente
#==============================================================================
#- Graficar EMDs
#==============================================================================

for serie in series:
    #serie = series[0]
    #- Rutas IMFs
    ruta_emd_R = ruta_resultados + 'R/R_' + str(serie) + '.csv'
    ruta_emd_P = ruta_resultados + 'P/P_' + str(serie) + '.csv'
    ruta_emd_ETR = ruta_resultados + 'ETR/ETR_' + str(serie) + '.csv'
    ruta_emd_dSdt = ruta_resultados + 'dS/dS_' + str(serie) + '.csv'
    #- Leer IMFs
    emd_R = pd.read_csv(ruta_emd_R, index_col=0, encoding = 'utf8')
    emd_P = pd.read_csv(ruta_emd_P, index_col=0, encoding = 'utf8')
    emd_ETR = pd.read_csv(ruta_emd_ETR, index_col=0, encoding = 'utf8')
    emd_dSdt = pd.read_csv(ruta_emd_dSdt, index_col=0, encoding = 'utf8')
    
    #- Leer series graficas
    
    serie_R = 'R_' + str(serie)
    yorig_R = series_reconstruidas[serie_R]
    ymodos_R = emd_R.iloc[:,:-1]
    yresiduo_R = emd_R.iloc[:,-1]
    
    serie_P = 'P_' + str(serie)
    yorig_P = series_reconstruidas[serie_P]
    ymodos_P = emd_P.iloc[:,:-1]
    yresiduo_P = emd_P.iloc[:,-1]
    
    serie_ETR = 'ETR_' + str(serie)
    yorig_ETR = series_reconstruidas[serie_ETR]
    ymodos_ETR = emd_ETR.iloc[:,:-1]
    yresiduo_ETR = emd_ETR.iloc[:,-1]
    
    serie_dSdt = 'dS_' + str(serie)
    yorig_dSdt = series_reconstruidas[serie_dSdt]
    ymodos_dSdt = emd_dSdt.iloc[:,:-1]
    yresiduo_dSdt = emd_dSdt.iloc[:,-1]
    
    #- Configurar grafica
    figura , axs = plt.subplots(2, 4, sharex=True, figsize=(12,4), gridspec_kw={'hspace':0})
    
    try:
        titulo = str(serie) + ' - ' + metadatos['nombre'][serie] + ' - ' + metadatos['Corriente'][serie]
    except:
        titulo = str(serie) + ' - ' + metadatos['nombre'][serie]
    plt.suptitle(titulo)
    x = pd.to_datetime(series_reconstruidas.index)
    #units = '[mm/mes]'
    units = '[mm/month]'
    #- Crear grafica
    axs[0,0].set_title('R')
    #axs[0,0].set_ylabel('Serie y residuo \n [mm/mes]')
    axs[0,0].set_ylabel('Series and residue \n [mm/month]')
    axs[0,0].plot(x,yorig_R.values, 'k', lw=1)
    axs[0,0].plot(x,yresiduo_R.values, 'r')
    colors = plt.cm.rainbow(np.linspace(0,1,ymodos_R.columns.size))
    for i,modo in enumerate(ymodos_R.columns):
        axs[1,0].plot(x,ymodos_R[modo].values, color = colors[i], lw=1)
    #axs[1,0].set_xlabel(u'Fecha [Año]')
    axs[1,0].set_xlabel(u'Date [year]')
    #axs[1,0].set_ylabel(u'FMIs \n [mm/mes]')
    axs[1,0].set_ylabel(u'IMFs \n [mm/month]')
    
    axs[0,1].set_title('P')
    axs[0,1].plot(x,yorig_P.values, 'k', lw=1)
    axs[0,1].plot(x,yresiduo_P.values, 'r')
    colors = plt.cm.rainbow(np.linspace(0,1,ymodos_P.columns.size))
    for i,modo in enumerate(ymodos_P.columns):
        axs[1,1].plot(x,ymodos_P[modo].values, color = colors[i], lw=1)
    #axs[1,1].set_xlabel(u'Fecha [Año]')
    axs[1,1].set_xlabel(u'Date [year]')
    
    axs[0,2].set_title('ETR')
    axs[0,2].plot(x,yorig_ETR, 'k', lw=1)
    axs[0,2].plot(x,yresiduo_ETR.values, 'r')
    colors = plt.cm.rainbow(np.linspace(0,1,ymodos_ETR.columns.size))
    for i,modo in enumerate(ymodos_ETR.columns):
        axs[1,2].plot(x,ymodos_ETR[modo].values, color = colors[i], lw=1)
    #axs[1,2].set_xlabel(u'Fecha [Año]')
    axs[1,2].set_xlabel(u'Date [year]')
    
    axs[0,3].set_title('dS/dt')
    axs[0,3].plot(x,yorig_dSdt.values, 'k', lw=1)
    axs[0,3].plot(x,yresiduo_dSdt.values, 'r')
    colors = plt.cm.rainbow(np.linspace(0,1,ymodos_dSdt.columns.size))
    for i,modo in enumerate(ymodos_dSdt.columns):
        axs[1,3].plot(x,ymodos_dSdt[modo].values, color = colors[i], lw=1)
    #axs[1,2].set_xlabel(u'Fecha [Año]')
    axs[1,2].set_xlabel(u'Date [year]')
    #Save PNG
    ruta_figura = ruta_resultados + 'figuras_emd_ENG/' + str(serie) + '.png'
    plt.savefig(ruta_figura, dpi=300, bbox_inches = 'tight')
    if serie in series_usar:
        ruta_figura = ruta_resultados + 'figuras_emd_ENG/usadas/' + str(serie) + '.png'
        plt.savefig(ruta_figura, dpi=300, bbox_inches = 'tight')
    #Save SVG
    ruta_figura = ruta_resultados + 'figuras_emd_ENG/' + str(serie) + '.svg'
    plt.savefig(ruta_figura, bbox_inches = 'tight')
    if serie in series_usar:
        ruta_figura = ruta_resultados + 'figuras_emd_ENG/usadas/' + str(serie) + '.svg'
        plt.savefig(ruta_figura, bbox_inches = 'tight')
    plt.close()
    
#    metadatos.loc[serie,'recRmlp(mm/mes)']=yorig_R.mean()
#    metadatos.loc[serie,'recPmlp(mm/mes)']=yorig_P.mean()
#    metadatos.loc[serie,'recETRmlp(mm/mes)']=yorig_ETR.mean()
#    metadatos.loc[serie,'recdS/dtmlp(mm/mes)']=yorig_dSdt.mean()
    print(serie)
#metadatos.to_csv(ruta_metadatos2)