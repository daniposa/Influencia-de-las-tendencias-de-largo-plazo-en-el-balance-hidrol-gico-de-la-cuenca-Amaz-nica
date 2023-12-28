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
from scipy.stats import gaussian_kde
import scipy.stats as sc
#==============================================================================
#- Definir rutas
#==============================================================================
#- Ruta carpeta raiz
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/'

#- Ruta de los metadatos
ruta_metadatos = raiz + 'Q/ANA/usar/metadatos10.csv'

#- Ruta guardar figuras
ruta_figuras = raiz + 'reconstruccion/IndicadoresError/fig_scatter/'
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
    yall_R = experimentos_R[experimentos].values
    yorig_R = experimentos_R.loc[:,'0'].values
    xx_R = np.reshape(yall_R,(yall_R.size),order='C').astype(np.float)
    yy_R = np.repeat(yorig_R, 20).astype(np.float)
    xx1_R = xx_R[np.where(np.logical_and(np.isnan(xx_R)==False,np.isnan(yy_R)==False))]
    yy1_R = yy_R[np.where(np.logical_and(np.isnan(xx_R)==False,np.isnan(yy_R)==False))]
    xy_R = np.vstack([xx1_R,yy1_R])
    z_R = gaussian_kde(xy_R)(xy_R)
    sorted_index = np.argsort(z_R)
    z_R = z_R[sorted_index]
    xx1_R = xx1_R[sorted_index]
    yy1_R = yy1_R[sorted_index]
    line_1_1_R = np.array([0.98 * np.min(xy_R),1.01 * np.max(xy_R)])
    vble_R = 'R'
    units = '[mm/mes]'
    
    yall_P = experimentos_P[experimentos].values
    yorig_P = experimentos_P.loc[:,'0'].values
    xx_P = np.reshape(yall_P,(yall_P.size),order='C').astype(np.float)
    yy_P = np.repeat(yorig_P, 20).astype(np.float)
    xx1_P = xx_P[np.where(np.logical_and(np.isnan(xx_P)==False,np.isnan(yy_P)==False))]
    yy1_P = yy_P[np.where(np.logical_and(np.isnan(xx_P)==False,np.isnan(yy_P)==False))]
    xy_P = np.vstack([xx1_P,yy1_P])
    z_P = gaussian_kde(xy_P)(xy_P)
    sorted_index = np.argsort(z_P)
    z_P = z_P[sorted_index]
    xx1_P = xx1_P[sorted_index]
    yy1_P = yy1_P[sorted_index]
    line_1_1_P = np.array([0.98 * np.min(xy_P),1.01 * np.max(xy_P)])
    vble_P = 'P'
    
    yall_ETR = experimentos_ETR[experimentos].values
    yorig_ETR = experimentos_ETR.loc[:,'0'].values
    xx_ETR = np.reshape(yall_ETR,(yall_ETR.size),order='C').astype(np.float)
    yy_ETR = np.repeat(yorig_ETR, 20).astype(np.float)
    xx1_ETR = xx_ETR[np.where(np.logical_and(np.isnan(xx_ETR)==False,np.isnan(yy_ETR)==False))]
    yy1_ETR = yy_ETR[np.where(np.logical_and(np.isnan(xx_ETR)==False,np.isnan(yy_ETR)==False))]
    xy_ETR = np.vstack([xx1_ETR,yy1_ETR])
    z_ETR = gaussian_kde(xy_ETR)(xy_ETR)
    sorted_index = np.argsort(z_ETR)
    z_ETR = z_ETR[sorted_index]
    xx1_ETR = xx1_ETR[sorted_index]
    yy1_ETR = yy1_ETR[sorted_index]
    line_1_1_ETR = np.array([0.98 * np.min(xy_ETR),1.01 * np.max(xy_ETR)])
    vble_ETR = 'ETR'
    
    yall_dS = experimentos_dS[experimentos].values
    yorig_dS = experimentos_dS.loc[:,'0'].values
    xx_dS = np.reshape(yall_dS,(yall_dS.size),order='C').astype(np.float)
    yy_dS = np.repeat(yorig_dS, 20).astype(np.float)
    xx1_dS = xx_dS[np.where(np.logical_and(np.isnan(xx_dS)==False,np.isnan(yy_dS)==False))]
    yy1_dS = yy_dS[np.where(np.logical_and(np.isnan(xx_dS)==False,np.isnan(yy_dS)==False))]
    xy_dS = np.vstack([xx1_dS,yy1_dS])
    z_dS = gaussian_kde(xy_dS)(xy_dS)
    sorted_index = np.argsort(z_dS)
    z_dS = z_dS[sorted_index]
    xx1_dS = xx1_dS[sorted_index]
    yy1_dS = yy1_dS[sorted_index]
    line_1_1_dS = np.array([0.98 * np.min(xy_dS),1.01 * np.max(xy_dS)])
    vble_dS = 'dS'
    
    #==============================================================================
    #- dibujar serie y bandas de reconstrucción
    #==============================================================================
    #fig , (axR, axP, axETR, axdS) = plt.subplots(1, 4, figsize=(15,3.5))
    #fig , ((axR, axP), (axETR, axdS)) = plt.subplots(2, 2, figsize=(15,7))
    #titulo = str(estacion) + ' - ' + str(nombres[estacion]) + ' - ' + str(corrientes[estacion])
    fig , (axR1, axP1, axETR1, axdS1) = plt.subplots(1, 4, figsize=(15,3), gridspec_kw={'hspace':0})#,sharey=True)
    
    #fig.suptitle(str(estacion))
    lw_med = 1
    lw_orig = 1.5
    
    axR1.scatter( xx1_R , yy1_R , s=50, c=z_R, cmap='jet', marker='.')
    axR1.plot(line_1_1_R , line_1_1_R,'--k')
    #axR1.set_xlim(line_1_1_R[0], line_1_1_R[-1])
    axR1.set_ylim(line_1_1_R[0], line_1_1_R[-1])
    axR1.set_xlabel(vble_R + ' reconstruido ' + units)
    axR1.set_ylabel(u'valor medido '+r'$[mm/mes]$')
    #axR1.text(0, line_1_1_R[-1]*0.9, "R2 = {:.2f}".format(sc.spearmanr(xx1_R,yy1_R)[0]))
    axR1.set_title(u"\u03C1s = {:.2f}".format(sc.spearmanr(xx1_R,yy1_R)[0]))
    
    
    axP1.scatter( xx1_P , yy1_P , s=50, c=z_P, cmap='jet', marker='.')
    axP1.plot(line_1_1_P , line_1_1_P,'--k')
    #axP1.set_xlim(line_1_1_P[0], line_1_1_P[-1])
    axP1.set_ylim(line_1_1_P[0], line_1_1_P[-1])
    axP1.set_xlabel(vble_P + ' reconstruido ' + units)
    #axP1.set_ylabel(u'P medido '+r'$[mm/mes]$')
    #axP1.text(0, line_1_1_P[-1]*0.9, "R2 = {:.2f}".format(sc.spearmanr(xx1_P,yy1_P)[0]))
    axP1.set_title(u"\u03C1s = {:.2f}".format(sc.spearmanr(xx1_P,yy1_P)[0]))
    
    axETR1.scatter( xx1_ETR , yy1_ETR , s=50, c=z_ETR, cmap='jet', marker='.')
    axETR1.plot(line_1_1_ETR , line_1_1_ETR,'--k')
    #axETR1.set_xlim(line_1_1_ETR[0], line_1_1_ETR[-1])
    axETR1.set_ylim(line_1_1_ETR[0], line_1_1_ETR[-1])
    axETR1.set_xlabel(vble_ETR + ' reconstruido ' + units)
    #axETR1.set_ylabel(u'ETR medido '+r'$[mm/mes]$')
    #axETR1.text(0, line_1_1_ETR[-1]*0.9, "R2 = {:.2f}".format(sc.spearmanr(xx1_ETR,yy1_ETR)[0]))
    axETR1.set_title(u"\u03C1s = {:.2f}".format(sc.spearmanr(xx1_ETR,yy1_ETR)[0]))
        
    axdS1.scatter( xx1_dS , yy1_dS , s=50, c=z_dS, cmap='jet', marker='.')
    axdS1.plot(line_1_1_dS , line_1_1_dS,'--k')
    #axdS1.set_xlim(line_1_1_dS[0], line_1_1_dS[-1])
    axdS1.set_ylim(line_1_1_dS[0], line_1_1_dS[-1])
    axdS1.set_xlabel('dS reconstruido ' + units)
    #axdS1.set_ylabel(u'dS medido '+r'$[mm/mes]$')
    #axdS1.text(0, line_1_1_dS[-1]*0.9, "R2 = {:.2f}".format(sc.spearmanr(xx1_dS,yy1_dS)[0]))
    axdS1.set_title(u"\u03C1s = {:.2f}".format(sc.spearmanr(xx1_dS,yy1_dS)[0]))
    
    plt.savefig(ruta_figuras + str(estacion) + '.png', dpi=300, bbox_inches = 'tight')
    plt.close()
