# -*- coding: utf-8 -*-
"""
Created on Wed Sep 04 18:01:10 2019
Calcula las series de escorrentía total mensual RT[Hm3/mes], promedio mensual 
(en el espacio) RP[mm/mes], y el mapa de la escorrentía media de largo plazo 
Rmlp[mm/mes]
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

#- leer datos de caudal
ruta_Qm3s = root + 'Q/ANA/usar/matriz_Q.csv'
Qm3s_todos = pd.read_csv(ruta_Qm3s , index_col = 0 )
#NOTA: FALTA RECONSTRUIR DEFINITIVAMENTE

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
    Pmlp['mtrx'][Pmlp['mtrx'] == 0.] = Pmlp['nodt']
    rst.WriteTifRaster(ruta_Pmlp,Pmlp)
    
    #- datos ETR
    ETRT = pd.read_csv(ruta_ETRT , index_col = 0 )
    ETRP = pd.read_csv(ruta_ETRP , index_col = 0 )
    ETRmlp = rst.ReadRaster(ruta_ETRmlp)
    ETRmlp['mtrx'][ETRmlp['mtrx'] == 0.] = ETRmlp['nodt']
    rst.WriteTifRaster(ruta_ETRmlp,ETRmlp)
    
    #- datos dS
    dST = pd.read_csv(ruta_dST , index_col = 0 )
    dSP = pd.read_csv(ruta_dSP , index_col = 0 )
    dSmlp = rst.ReadRaster(ruta_dSmlp)
    dSmlp['mtrx'][dSmlp['mtrx'] == 0.] = dSmlp['nodt']
    rst.WriteTifRaster(ruta_dSmlp,dSmlp)
    
    if estacion == lista_estaciones[-1]:
        #- calcular Rmlp por balance de largo plazo
        Rmlp = cp.copy(Pmlp)
        Rmlp['mtrx'] = Pmlp['mtrx'] - ETRmlp['mtrx']
        Rmlp['mtrx'][Rmlp['mtrx'] == 0.] = Rmlp['nodt']
        rst.WriteTifRaster(ruta_Rmlp,Rmlp)
        
    else:
        #- Serie de caudal de la estacion
        Qm3s = Qm3s_todos[str(estacion)][:].copy()
        
        #- calcular RT y RP a partir de la serie de Q
        seconds = pd.date_range(start=pd.to_datetime(Qm3s.index)[0] , end=(pd.to_datetime(Qm3s.index)[-1]+pd.DateOffset(months = 1)), freq='M').day.values.astype(np.float) * 86400.
        RT = (Qm3s * seconds) /(10.**6.)
        RP = (Qm3s * seconds) * 1000. / (metadatos['Area_rst(km2)'][estacion] * 10. ** 6.)
        
        #- calcular Rmlp por balance de largo plazo
        Rmlp = cp.copy(Pmlp)
        Rmlp['mtrx'] = Pmlp['mtrx'] - ETRmlp['mtrx']
        Rmlp['mtrx'][Rmlp['mtrx'] == 0.] = Rmlp['nodt']
        
        #- Escribir Rmlp promedio espacial en metadatos
        metadatos['Rmlp(mm/mes)'][estacion] = RP.mean()
        
        #- Guardar RT, RP y Rmlp
        st.EscribirSerie(ruta_RT, RT)
        st.EscribirSerie(ruta_RP, RP)
        rst.WriteTifRaster(ruta_Rmlp,Rmlp)
    print(estacion)

#- guardar metadatos
metadatos.to_csv('H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Q/ANA/usar/metadatos10.csv')
