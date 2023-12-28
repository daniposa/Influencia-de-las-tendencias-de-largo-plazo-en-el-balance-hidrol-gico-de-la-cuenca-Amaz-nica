# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:15:14 2019
Toma los datos de precipitación de CHIRPS y los transforma en una serie de 
tiempo para cada cuenca, que se guarda como un csv.
@author: Daniela
"""
#==============================================================================
#- Importar módulos
#==============================================================================

import pandas as pd
import Raster as rst
import numpy as np
import SeriesTiempo as st
#from datetime import datetime
import time as time

#==============================================================================
#- Definir rutas de carpetas
#==============================================================================
#- rutas de archivos Base
ruta_metadatos='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Q/ANA/usar/metadatos6.csv'
ruta_chirps='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoCruda/P_CHIRPS/'
ruta_cuencas_tif='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Cuencas/areapixel/tif'

#- rango de fechas chirps
meses=['01','02','03','04','05','06','07','08','09','10','11','12']
anos=range(1981,2018)
dia_inicio='01/01/1981'#- [dd/mm/yyyy]
dia_fin='01/12/2018'#- [dd/mm/yyyy]
##==============================================================================
##- Definir funcion de construir serie mensual
##==============================================================================
#
def ConstruirSerieMensual(dia_inicio,valores):
    
    u"""Construye una serie de tiempo diaria.
    
    Retorna una serie de tiempo diaria usando la estructura de almacenamiento
    de Pandas.
    
    Entradas
    --------
    dia_inicio: texto,
        Fecha del primer día de la serie de tiempo en formato dd/mm/yyyy
    valores: real,
        Vector (numpy array) de valores de la serie
    
    Retorna
    -------
    serie: pandas series,
        Serie de tiempo
        
    Autor y contacto
    ----------------
    Rendón-Álvarez, J. P., jprendona@gmail.com
    
    """
    
    fechas=pd.date_range(pd.to_datetime(dia_inicio,format='%d/%m/%Y'),periods=np.size(valores),freq='MS')
    serie=pd.Series(valores,index=fechas)
    return serie
#==============================================================================
#- Cargar cuencas
#==============================================================================
    
#- cargar metadatos de estaciones usadas
metadatos=pd.read_csv(ruta_metadatos,index_col=0)
lista_estaciones=metadatos.index #lista de estaciones usadas
#lista_estaciones=[11450000,12550000,12870000,13550000,17345000]
cuenca_base=rst.ReadRaster('H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Cuencas/areapixel/tif/99999999.tif')

#- variables almacenar resultados
valores_PT=np.empty((0,110))# Precipitación total mensual
valores_PP=np.empty((0,110))# Precipitación promedio mensual
Pmlp_mtrx=np.zeros_like(cuenca_base['mtrx'])# precipitación media de largo plazo

mascaras=[]#- indices de la matriz del raster para cada cuenca
areas_pixeles=[]#- area de cada pixel en los indices
for estacion in lista_estaciones:
    #- cargar cuenca
    ruta_cuenca=ruta_cuencas_tif+'/'+str(estacion)+'.tif'
    cuenca=rst.ReadRaster(ruta_cuenca)
    cuenca_masc=cuenca['mtrx']>0.0
    mascaras.append(np.where(cuenca_masc))
    areas_pixeles.append(cuenca['mtrx'][mascaras[-1]])
    metadatos['Area_rst(km2)'][estacion]=areas_pixeles[-1].sum()/1000000.
    print(len(mascaras))


#==============================================================================
#- Construir series de P y raster de P media
#==============================================================================

for ano in anos:
    #ano=anos[0]
    for mes in meses:
        #mes=meses[0]
        time0=time.time()
        print(str(ano)+'-'+str(mes))
        
        #- leer mes de chirps
        nombre='chirps-v2.0.'+str(ano)+'.'+mes+'.tif'
        chirps=rst.ReadRaster(ruta_chirps+nombre)
        
        #- remuestrear a resolución de cuencas
        chirps_resampled=rst.SampleRastToRast(chirps,cuenca_base)
        
        #- precipitación media de largo plazo [mm/mes]
        Pmlp_mtrx=Pmlp_mtrx+chirps_resampled['mtrx']
        
        #- preparar para guardar info del mes
        valores_PT=np.append(valores_PT,np.zeros((1,110)),axis=0)# Precipitación total mensual
        valores_PP=np.append(valores_PP,np.zeros((1,110)),axis=0)# Precipitación promedio mensual
        col = 0
        for estacion in lista_estaciones:
            #estacion=lista_estaciones[0]
            #print(estacion)
            
            #- Calcular chirps en area
            chirps_area_mtrx=chirps_resampled['mtrx'][mascaras[col]]*areas_pixeles[col]*0.001 #[m3/mes]
            
            #- Precipitación total mensual [Hm3/mes]
            PT=chirps_area_mtrx.sum()/(10.**6.)
            
            valores_PT[-1,col]=PT
            
            AT=areas_pixeles[col].sum() #[m2]
            
            #- Precipitación promedio mensual [mm/mes]
            PP=PT*(10.**6.)/AT*1000.
            valores_PP[-1,col]=PP
            col = col+ 1
        time1=time.time()
        print(time1-time0)

#- Guardar raster de Pmlp en todo el dominio espacial[mm/mes]
Pmlp_mtrx=Pmlp_mtrx/456.
Pmlp_mtrx[Pmlp_mtrx == 0.0]=cuenca_base['nodt']
Pmlp=rst.BuildRaster(cuenca_base['xll'],cuenca_base['yll'],cuenca_base['clsz'],cuenca_base['nodt'],Pmlp_mtrx)
Pmlp_fname='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/P/P_media_largo_plazo/'+'Pmlp.tif'
rst.WriteTifRaster(Pmlp_fname,Pmlp)

#- Guardar series de P y PmlP para cada cuenca
col=0
for estacion in lista_estaciones:
    
    Pmlp_cuenca_mtrx=np.zeros_like(cuenca_base['mtrx'])
    Pmlp_cuenca_mtrx[Pmlp_cuenca_mtrx == 0.0]=cuenca_base['nodt']
    Pmlp_cuenca=rst.BuildRaster(cuenca_base['xll'],cuenca_base['yll'],cuenca_base['clsz'],cuenca_base['nodt'],Pmlp_cuenca_mtrx)
    
    #- Serie precipitación total (PT)[Hm3/mes]
    #serie_PT=st.ConstruirSerieMensual(dia_inicio,valores_PT)
    serie_PT=ConstruirSerieMensual(dia_inicio,valores_PT[:,col])
    PT_fname='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/P/P_total_mensual/'+str(estacion)+'.csv'
    st.EscribirSerie(PT_fname,serie_PT)
    
    #- Serie Precipitación promedio mensual (PP)[mm/mes]
    #serie_PP=st.ConstruirSerieMensual(dia_inicio,valores_PP)
    serie_PP=ConstruirSerieMensual(dia_inicio,valores_PP[:,col])
    PP_fname='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/P/P_media_mensual/'+str(estacion)+'.csv'
    st.EscribirSerie(PP_fname,serie_PP)
    
    #- Ráster precipitación media de largo plazo [mm/mes]
    Pmlp_cuenca['mtrx'][mascaras[col]]=Pmlp_mtrx[mascaras[col]]
    
    Pmlp_cuenca_fname='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/P/P_media_largo_plazo/'+'Pmlp_'+str(estacion)+'.tif'
    rst.WriteTifRaster(Pmlp_cuenca_fname,Pmlp_cuenca)
    print('variables guardadas para la estación '+str(estacion))
    col= col + 1

metadatos['Pmlp(mm/mes)'][:]=valores_PP.mean(axis=0)
metadatos.to_csv('H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Q/ANA/usar/metadatos7.csv')