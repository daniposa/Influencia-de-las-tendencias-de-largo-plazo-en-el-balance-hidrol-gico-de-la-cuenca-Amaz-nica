# -*- coding: utf-8 -*-
"""
Created on Thu Sep 05 20:46:23 2019

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
import copy as cp
import time as time

#==============================================================================
#- Definir rutas de carpetas base
#==============================================================================
#- carpeta raiz
root = 'H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/'

#- rutas de archivos Base
ruta_metadatos = root + 'Q/ANA/usar/metadatos9.csv'

#- cargar metadatos de estaciones usadas
metadatos = pd.read_csv(ruta_metadatos,index_col=0)
lista_estaciones = metadatos.index #- lista de estaciones usadas

for estacion in lista_estaciones:
    #estacion=lista_estaciones[0]
    #==============================================================================
    #- Definir rutas de series
    #==============================================================================
    #- rutas P
    ruta_PT = root + 'P/P_total_mensual/' + str(estacion)+'.csv'
    ruta_PP = root + 'P/P_media_mensual/' + str(estacion)+'.csv'
    ruta_Pmlp = root + 'P/P_media_largo_plazo/' + 'Pmlp_' + str(estacion)+'.tif'
    
    #- rutas ETR
    ruta_ETRT = root + 'ETR/ETR_total_mensual/' + str(estacion)+'.csv'
    ruta_ETRP = root + 'ETR/ETR_media_mensual/' + str(estacion)+'.csv'
    ruta_ETRmlp = root + 'ETR/ETR_media_largo_plazo/' + 'ETRmlp_' + str(estacion)+'.tif'
    
    #- rutas dS
    ruta_dST= root + 'dS/dS_total_mensual/' + str(estacion)+'.csv'
    ruta_dSP= root + 'dS/dS_media_mensual/' + str(estacion)+'.csv'
    ruta_dSmlp= root + 'dS/dS_media_largo_plazo/'+'dSmlp_' + str(estacion)+'.tif'
    
    #- rutas R
    ruta_RT = root + 'R/R_total_mensual/' + str(estacion)+'.csv'
    ruta_RP = root + 'R/R_media_mensual/' + str(estacion)+'.csv'
    ruta_Rmlp = root + 'R/R_media_largo_plazo/'+'Rmlp_' + str(estacion)+'.tif'
    
    #==============================================================================
    #- Leer datos
    #==============================================================================
    
    #- datos P
    PT = pd.read_csv(ruta_PT , index_col = 0 )
    PP = pd.read_csv(ruta_PP , index_col = 0 )
    Pmlp = rst.ReadRaster(ruta_Pmlp)
    
    #- datos ETR
    ETRT = pd.read_csv(ruta_ETRT , index_col = 0 )
    ETRP = pd.read_csv(ruta_ETRP , index_col = 0 )
    ETRmlp = rst.ReadRaster(ruta_ETRmlp)
    
    #- datos dS
    dST = pd.read_csv(ruta_dST , index_col = 0 )
    dSP = pd.read_csv(ruta_dSP , index_col = 0 )
    dSmlp = rst.ReadRaster(ruta_dSmlp)
    
    #- datos R
    RT = pd.read_csv(ruta_RT , index_col = 0 )
    RP = pd.read_csv(ruta_RP , index_col = 0 )
    Rmlp = rst.ReadRaster(ruta_Rmlp)
    
    #==============================================================================
    #- Leer datos
    #==============================================================================
    
    