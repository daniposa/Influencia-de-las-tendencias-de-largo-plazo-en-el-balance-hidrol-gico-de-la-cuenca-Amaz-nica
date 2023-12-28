# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:36:38 2020
Dibuja series, scatter plots y ciclos anuales del error
@author: Daniela
"""
#==============================================================================
#------------------------------------------------------------------------------
#- Series y Scatter plots
#------------------------------------------------------------------------------
#==============================================================================
#- Importar módulos requeridos
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#==============================================================================
#- Definir rutas
#==============================================================================
#- Ruta carpeta raiz
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/'

#- Ruta de los metadatos
ruta_metadatos = raiz + 'Q/ANA/usar/metadatos12.csv'

#- Ruta guardar figuras
ruta_figuras = raiz + 'reconstruccion/IndicadoresError/fig_bandasP5P95_ENG/'
#==============================================================================
#- Leer y procesar datos
#==============================================================================
#- cargar metadatos
metadatos=pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
estaciones = metadatos.index.values
nombres = metadatos['nombre']
corrientes = metadatos['Corriente']
variables = ['R','P','ETR','dS']
experimentos = [str(i) for i in range(1,21)]

for estacion in estaciones[:-1]:
    #estacion = estaciones[0]
    #- Ruta de lectura de experimentos
    ruta_exp_R = raiz + 'reconstruccion/R/reconstruccion_rez/R_' + str(estacion) + '.csv'
    ruta_exp_P = raiz + 'reconstruccion/P/reconstruccion_rez/P_' + str(estacion) + '.csv'
    ruta_exp_ETR = raiz + 'reconstruccion/ETR/reconstruccion_rez/ETR_' + str(estacion) + '.csv'
    ruta_exp_dS = raiz + 'reconstruccion/dS/reconstruccion_rez/dS_' + str(estacion) + '.csv'
    
    #- cargar experimentos
    experimentos_R = pd.read_csv(ruta_exp_R, index_col = 0)
    experimentos_P = pd.read_csv(ruta_exp_P, index_col = 0)
    experimentos_ETR = pd.read_csv(ruta_exp_ETR, index_col = 0)
    experimentos_dS = pd.read_csv(ruta_exp_dS, index_col = 0)
    
    #- calcular estadísticos de los experimentos:
    x = pd.to_datetime(experimentos_R.index)
    ymin_R = experimentos_R['p5']
    ymed_R = experimentos_R['p50']
    ymax_R = experimentos_R['p95']
    yorig_R = experimentos_R.loc[:,'0'].values
    vble = 'R'
    #units = '[mm/mes]'
    
    ymin_P = experimentos_P['p5']
    ymed_P = experimentos_P['p50']
    ymax_P = experimentos_P['p95']
    yorig_P = experimentos_P.loc[:,'0'].values
    vble = 'P'
    #units = '[mm/mes]'
    
    ymin_ETR = experimentos_ETR['p5']
    ymed_ETR = experimentos_ETR['p50']
    ymax_ETR = experimentos_ETR['p95']
    yorig_ETR = experimentos_ETR.loc[:,'0'].values
    vble = 'ETR'
    #units = '[mm/mes]'
    
    ymin_dS = experimentos_dS['p5']
    ymed_dS = experimentos_dS['p50']
    ymax_dS = experimentos_dS['p95']
    yorig_dS = experimentos_dS.loc[:,'0'].values
    vble = 'dS'
    #units = '[mm/mes]'
    units = '[mm/month]'
    
    #==============================================================================
    #- dibujar serie y bandas de reconstrucción
    #==============================================================================
    #fig , (axR, axP, axETR, axdS) = plt.subplots(1, 4, figsize=(15,3.5))
    #fig , ((axR, axP), (axETR, axdS)) = plt.subplots(2, 2, figsize=(15,7))
    titulo = str(estacion) + ' - ' + str(nombres[estacion]) + ' - ' + str(corrientes[estacion])
    fig , (axR1, axP1, axETR1, axdS1) = plt.subplots(4, 1, sharex=True, figsize=(13,7), gridspec_kw={'hspace':0})
    
    #fig.suptitle(str(estacion))
    lw_med = 1
    lw_orig = 1.5
    
    axR1.fill_between(x, ymin_R, ymax_R, facecolor='red')
    axR1.plot(x, ymed_R, 'b--',lw=lw_med)
    axR1.plot(x, yorig_R, c='k', lw=lw_orig)
    #axR.set_xlabel(u'Fecha')
    #axR.set_title('R' + ' ' + r'$[mm/mes]$')
    axR1.set_title(titulo)
    #axR1.set_ylabel('R' + ' ' + r'$[mm/mes]$')
    axR1.set_ylabel('R' + ' ' + r'$[mm/month]$')
    
    axP1.fill_between(x, ymin_P, ymax_P, facecolor='red')
    axP1.plot(x, ymed_P, 'b--',lw=lw_med)
    axP1.plot(x, yorig_P, c='k', lw=lw_orig)
    #axP.set_xlabel(u'Fecha')
    #axP.set_title('P' + ' ' + r'$[mm/mes]$')
    #axP1.set_ylabel('P' + ' ' + r'$[mm/mes]$')
    axP1.set_ylabel('P' + ' ' + r'$[mm/month]$')
    
    axETR1.fill_between(x, ymin_ETR, ymax_ETR, facecolor='red')
    axETR1.plot(x, ymed_ETR, 'b--',lw=lw_med)
    axETR1.plot(x, yorig_ETR, c='k', lw=lw_orig)
    #axETR.set_xlabel(u'Fecha')
    #axETR.set_title('ETR' + ' ' + r'$[mm/mes]$')
    #axETR1.set_ylabel('ETR' + ' ' + r'$[mm/mes]$')
    axETR1.set_ylabel('ETR' + ' ' + r'$[mm/month]$')
        
    axdS1.fill_between(x, ymin_dS, ymax_dS, facecolor='red')
    axdS1.plot(x, ymed_dS, 'b--',lw=lw_med)
    axdS1.plot(x, yorig_dS, c='k', lw=lw_orig)
    #axdS1.set_xlabel(u'Fecha [Año]')
    axdS1.set_xlabel(u'Date [year]')
    #axdS.set_title('dS' + ' ' + r'$[mm/mes]$')
    #axdS1.set_ylabel('dS' + ' ' + r'$[mm/mes]$')
    axdS1.set_ylabel('dS' + ' ' + r'$[mm/month]$')
    
    plt.savefig(ruta_figuras + str(estacion) + '.png', dpi=300, bbox_inches = 'tight')
    plt.savefig(ruta_figuras + str(estacion) + '.svg', bbox_inches = 'tight')
    plt.close()
