# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 20:38:08 2019
Graficar scatter plots de Indicadores de error vs. Area
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
#- Disco
#disco = 'H'
disco = 'B'

#- Definir rutas
raiz = disco + ':/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/reconstruccion/IndicadoresError/'
ruta_metadatos = disco + ':/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Q/ANA/usar/metadatos10.csv'
ruta_indicadores = raiz + 'resumen_errores.csv'

#- Cargar metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
estaciones = metadatos.index.values
areas = metadatos['Area_rst(km2)'][:]

#- Cargar resumen resultados indicadores
resu_indicadores = pd.read_csv(ruta_indicadores, index_col=0, encoding = 'utf8')

variables=['R','P','ETR','dS']
indicadores = ['EMAR','ENS','SESGO','CC','RECMR','RKS']


for indicador in indicadores:
    #for variable in variables:
    plt.figure()
    
    x = metadatos['Area_rst(km2)'].values[:-1]
    
    columnaR = 'm' + indicador + '_R'
    yR = resu_indicadores[columnaR].values[:-1]
    scaR = plt.scatter(x,yR)
    
    columnaP = 'm' + indicador + '_P'
    yP = resu_indicadores[columnaP].values[:-1]
    scaP = plt.scatter(x,yP)
    
    columnaETR = 'm' + indicador + '_ETR'
    yETR = resu_indicadores[columnaETR].values[:-1]
    scaETR = plt.scatter(x,yETR)
    
    columnadS = 'm' + indicador + '_dS'
    ydS = resu_indicadores[columnadS].values[:-1]
    scadS = plt.scatter(x,ydS)
    
    if indicador == 'EMAR' or indicador == 'ENS' or indicador == 'CC' or indicador == 'RECMR':
        plt.xscale("log")
        plt.yscale("log")
    else:
        plt.xscale("log")
    plt.legend([scaR,scaP,scaETR,scadS], variables)
    plt.title(indicador)