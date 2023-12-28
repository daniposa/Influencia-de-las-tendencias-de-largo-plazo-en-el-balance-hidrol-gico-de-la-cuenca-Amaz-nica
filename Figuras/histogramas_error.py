# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 19:09:30 2020
Crea los histogramas
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
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/'
ruta_metadatos = raiz + 'Q/ANA/usar/metadatos10.csv'
ruta_resultados = raiz + 'reconstruccion/IndicadoresError/resumen_errores.csv'
errores = ['EMAR','ENS','SESGO','CC','RECMR','RKS','TENDSEN','TENDMK']
rutas_figuras= raiz + 'reconstruccion/IndicadoresError/fig_histogramas/'
#- Cargar metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
#- Cargar resultados
resultados = pd.read_csv(ruta_resultados, index_col=0, encoding = 'utf8')
resultados = resultados.replace([np.inf, -np.inf], np.nan)

#==============================================================================
#- Hacer figuras
#==============================================================================

lim_ok = pd.DataFrame(data = np.array([[0.,0.6,-20.,0.6,0.,0.5,-0.5,0.5],[35.,1.,20.,1.,40.,1.5,0.5,1.5]]), index = ['min_ok','max_ok'], columns = errores)
columnas = resultados.columns[np.arange(64,step=2)]

for i in np.arange(len(errores)):
    #i=0
    if columnas[i][1:-2] == 'RKS' or columnas[i][1:-2] == 'TENDMK':
        figura, ax = plt.subplots(1,4, sharey=True, figsize=(10,2))#gridspec_kw={'hspace': 0.2, 'wspace': 0.2})
        columna1 = columnas[i]
        columna2 = columnas[i + 8]
        columna3 = columnas[i + 16]
        columna4 = columnas[i + 24]
        min_ok = lim_ok[columnas[i][1:-2]]['min_ok']
        max_ok = lim_ok[columnas[i][1:-2]]['max_ok']
        ax[0].axvspan(min_ok, max_ok, alpha=0.5, color='green')
        X = [0., 1.]
        Y = [(resultados[columna1] == 0.).sum(), (resultados[columna1] == 1.).sum()]
        ax[0].bar(X,Y, linewidth = 0.2, edgecolor = 'k')
        ax[0].set_title(columna1[1:])
        ax[0].set_xlabel('valor')
        ax[0].set_ylabel('frec. relativa (%)')
        ax[1].axvspan(min_ok, max_ok, alpha=0.5, color='green')
        X = [0., 1.]
        Y = [(resultados[columna2] == 0.).sum(), (resultados[columna2] == 1.).sum()]
        ax[1].bar(X,Y, linewidth = 0.2, edgecolor = 'k')
        ax[1].set_title(columna2[1:])
        ax[1].set_xlabel('valor')
        ax[2].axvspan(min_ok, max_ok, alpha=0.5, color='green')
        X = [0., 1.]
        Y = [(resultados[columna3] == 0.).sum(), (resultados[columna3] == 1.).sum()]
        ax[2].bar(X,Y, linewidth = 0.2, edgecolor = 'k')
        ax[2].set_title(columna3[1:])
        ax[2].set_xlabel('valor')
        ax[3].axvspan(min_ok, max_ok, alpha=0.5, color='green')
        X = [0., 1.]
        Y = [(resultados[columna4] == 0.).sum(), (resultados[columna4] == 1.).sum()]
        ax[3].bar(X,Y, linewidth = 0.2, edgecolor = 'k')
        ax[3].set_title(columna4[1:])
        ax[3].set_xlabel('valor')
        plt.savefig(rutas_figuras + columna1[1:-2] + '.png', bbox_inches = 'tight')
    elif columnas[i][1:-2] == 'CC':
        figura, ax = plt.subplots(1,4, sharey=True, figsize=(10,2))#, gridspec_kw={'hspace': 0.6, 'wspace': 0.1})
        columna1 = columnas[i]
        columna2 = columnas[i + 8]
        columna3 = columnas[i + 16]
        columna4 = columnas[i + 24]
        min_ok = lim_ok[columnas[i][1:-2]]['min_ok']
        max_ok = lim_ok[columnas[i][1:-2]]['max_ok']
        ax[0].axvspan(min_ok, max_ok, alpha=0.5, color='green')
        resultados[columna1].hist(ax = ax[0], linewidth = 0.2, edgecolor = 'k')
        ax[0].set_title(u"\u03C1s" + columna1[3:])
        ax[0].set_xlabel('valor')
        ax[0].set_ylabel('frec. relativa (%)')
        ax[1].axvspan(min_ok, max_ok, alpha=0.5, color='green')
        resultados[columna2].hist(ax = ax[1], linewidth = 0.2, edgecolor = 'k')
        ax[1].set_title(u"\u03C1s" + columna2[3:])
        ax[1].set_xlabel('valor')
        ax[2].axvspan(min_ok, max_ok, alpha=0.5, color='green')
        resultados[columna3].hist(ax = ax[2], linewidth = 0.2, edgecolor = 'k')
        ax[2].set_title(u"\u03C1s" + columna3[3:])
        ax[2].set_xlabel('valor')
        ax[3].axvspan(min_ok, max_ok, alpha=0.5, color='green')
        resultados[columna4].hist(ax = ax[3], linewidth = 0.2, edgecolor = 'k')
        ax[3].set_title(u"\u03C1s" + columna4[3:])
        ax[3].set_xlabel('valor')
        plt.savefig(rutas_figuras + columna1[1:-2] + '.png', bbox_inches = 'tight')
    else:
        figura, ax = plt.subplots(1,4, sharey=True, figsize=(10,2))#, gridspec_kw={'hspace': 0.6, 'wspace': 0.1})
        columna1 = columnas[i]
        columna2 = columnas[i + 8]
        columna3 = columnas[i + 16]
        columna4 = columnas[i + 24]
        min_ok = lim_ok[columnas[i][1:-2]]['min_ok']
        max_ok = lim_ok[columnas[i][1:-2]]['max_ok']
        ax[0].axvspan(min_ok, max_ok, alpha=0.5, color='green')
        resultados[columna1].hist(ax = ax[0], linewidth = 0.2, edgecolor = 'k')
        ax[0].set_title(columna1[1:])
        ax[0].set_xlabel('valor')
        ax[0].set_ylabel('frec. relativa (%)')
        ax[1].axvspan(min_ok, max_ok, alpha=0.5, color='green')
        resultados[columna2].hist(ax = ax[1], linewidth = 0.2, edgecolor = 'k')
        ax[1].set_title(columna2[1:])
        ax[1].set_xlabel('valor')
        ax[2].axvspan(min_ok, max_ok, alpha=0.5, color='green')
        resultados[columna3].hist(ax = ax[2], linewidth = 0.2, edgecolor = 'k')
        ax[2].set_title(columna3[1:])
        ax[2].set_xlabel('valor')
        ax[3].axvspan(min_ok, max_ok, alpha=0.5, color='green')
        resultados[columna4].hist(ax = ax[3], linewidth = 0.2, edgecolor = 'k')
        ax[3].set_title(columna4[1:])
        ax[3].set_xlabel('valor')
        plt.savefig(rutas_figuras + columna1[1:-2] + '.png', bbox_inches = 'tight')