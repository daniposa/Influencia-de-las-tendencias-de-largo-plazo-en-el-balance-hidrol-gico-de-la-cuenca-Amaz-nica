# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 13:38:13 2019
Toma los datos de evapotranspiración real y los transforma en una serie de 
tiempo para cada cuenca, que se guarda como un csv.
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
#from datetime import datetime
import time as time

#==============================================================================
#- Definir rutas de carpetas
#==============================================================================
#- rutas de archivos Base
ruta_metadatos='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Q/ANA/usar/metadatos8.csv'
ruta_ETR='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoCruda/E_Paca/ETR_Paca/ET-Amazon_Paca_2019.nc'
ruta_cuencas_tif='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Cuencas/areapixel/tif'

#- rango de fechas ETR
meses=['01','02','03','04','05','06','07','08','09','10','11','12']
anos=range(2003,2014) #- hay datos de ETR desde 2003 hasta 2013
dia_inicio='01/01/2003'#- [dd/mm/yyyy]
dia_fin='01/12/2013'#- [dd/mm/yyyy]

##==============================================================================
##- Definir funcion de construir serie mensual
##==============================================================================
#
def ConstruirSerieMensual(dia_inicio,valores):
    
    """
    Construye una serie de tiempo mensual.
    
    Retorna una serie de tiempo mensual usando la estructura de almacenamiento
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
cuenca_base=rst.ReadRaster('H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Cuencas/areapixel/tif/99999999.tif')

#- variables almacenar resultados
valores_ETRT=np.empty((0,110))# Evapotranspiración total mensual
valores_ETRP=np.empty((0,110))# Evapotranspiración promedio mensual
ETRmlp_mtrx=np.zeros_like(cuenca_base['mtrx'])# Evapotranspiración media de largo plazo

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
#- Leer netcdf de etr
#==============================================================================

#- leer archivo netcdf de etr
etr_netcdf=nc.Dataset(ruta_ETR)

#- calcular variables necesarias para la función que lo convierte en diccionario raster
variable = 'ET'
lat_dim = 1
lon_dim = 2
time_dim = 0

times=etr_netcdf['time'][:]
num_meses=times.size
#==============================================================================
#- Construir series de ETR y raster de ETR media
#==============================================================================

for time_to_extract in np.arange(num_meses):
    #time_to_extract = np.arange(num_meses)[0]
    time0=time.time()    
    print(str(times[time_to_extract]))
    #- convertir netcdf a raster
    # leer las propiedades de georeferenciación del ráster
    dims = [dim for dim in etr_netcdf.variables[variable].dimensions]
    xdim = np.array(etr_netcdf.variables[dims[lon_dim]])
    ydim = np.array(etr_netcdf.variables[dims[lat_dim]])
    time_ = etr_netcdf.variables[dims[time_dim]]
    
    dx = np.average(xdim[1:]-xdim[0:np.size(xdim)-1])
    dy = np.average(ydim[1:]-ydim[0:np.size(ydim)-1])
    
    mtrx=np.array(etr_netcdf.variables[variable][time_to_extract])
    
    clsz = 0.5*(dx-dy)
    xll = np.min(xdim)-0.5*dx
    yll = np.min(ydim)+0.5*dy
    nodt = etr_netcdf['ET']._FillValue
    
    #- build the Raster dictionary
    etr_rst=rst.BuildRaster(xll,yll,clsz,nodt,mtrx)
    rst.ChangeNoData(etr_rst,-9999.0)
    
    #- remuestrear mes a resolución de cuencas
    etr_resampled=rst.SampleRastToRast(etr_rst,cuenca_base)
    inan,jnan=np.where(etr_resampled['mtrx']<=0.0)
    etr_resampled['mtrx'][inan,jnan]=0.0
    
    #- evapotranspiración media de largo plazo [mm/mes]
    ETRmlp_mtrx=ETRmlp_mtrx+etr_resampled['mtrx']
    
    #- preparar para guardar info del mes
    valores_ETRT=np.append(valores_ETRT,np.zeros((1,110)),axis=0)# evapotranspiración total mensual
    valores_ETRP=np.append(valores_ETRP,np.zeros((1,110)),axis=0)# evapotranspiración promedio mensual
    col = 0
    for estacion in lista_estaciones:
        #estacion=lista_estaciones[0]
        #print(estacion)
        
        #- Calcular etr en area
        not_nan=(etr_resampled['mtrx'][mascaras[col]]>0.0).astype(float)
        etr_area_mtrx=etr_resampled['mtrx'][mascaras[col]]*areas_pixeles[col]*0.001*not_nan #[m3/mes]
        
        #- evapotranspiración total mensual [Hm3/mes]
        ETRT=etr_area_mtrx.sum()/(10.**6.)
        
        valores_ETRT[-1,col]=ETRT
        
        AT=areas_pixeles[col].sum() #[m2]
        AT_sin_nan=(areas_pixeles[col]*not_nan).sum()
        
        #- evapotranspiración promedio mensual [mm/mes]
        ETRP=(ETRT*(10.**6.)/AT_sin_nan)*1000.
        valores_ETRP[-1,col]=ETRP
        col = col+ 1
    time1=time.time()
    print(time1-time0)

#- Guardar raster de ETRmlp en todo el dominio espacial[mm/mes]
ETRmlp_mtrx=ETRmlp_mtrx/num_meses
ETRmlp_mtrx[ETRmlp_mtrx == 0.0]=cuenca_base['nodt']
ETRmlp=rst.BuildRaster(cuenca_base['xll'],cuenca_base['yll'],cuenca_base['clsz'],cuenca_base['nodt'],ETRmlp_mtrx)
ETRmlp_fname='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/ETR/ETR_media_largo_plazo/'+'ETRmlp.tif'
rst.WriteTifRaster(ETRmlp_fname,ETRmlp)

#- Guardar series de ETR y ETRmlp para cada cuenca
col=0
for estacion in lista_estaciones:
    
    ETRmlp_cuenca_mtrx=np.zeros_like(cuenca_base['mtrx'])
    ETRmlp_cuenca_mtrx[ETRmlp_cuenca_mtrx == 0.0]=cuenca_base['nodt']
    ETRmlp_cuenca=rst.BuildRaster(cuenca_base['xll'],cuenca_base['yll'],cuenca_base['clsz'],cuenca_base['nodt'],ETRmlp_cuenca_mtrx)
    
    #- Serie evapotranspiración total (ETRT)[Hm3/mes]
    serie_ETRT=ConstruirSerieMensual(dia_inicio,valores_ETRT[:,col])
    ETRT_fname='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/ETR/ETR_total_mensual/'+str(estacion)+'.csv'
    st.EscribirSerie(ETRT_fname,serie_ETRT)
    
    #- Serie evapotranspiración promedio mensual (ETRP)[mm/mes]
    serie_ETRP=ConstruirSerieMensual(dia_inicio,valores_ETRP[:,col])
    ETRP_fname='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/ETR/ETR_media_mensual/'+str(estacion)+'.csv'
    st.EscribirSerie(ETRP_fname,serie_ETRP)
    
    #- Ráster evapotranspiración media de largo plazo [mm/mes]
    ETRmlp_cuenca['mtrx'][mascaras[col]]=ETRmlp_mtrx[mascaras[col]]
    
    ETRmlp_cuenca_fname='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/ETR/ETR_media_largo_plazo/'+'ETRmlp_'+str(estacion)+'.tif'
    rst.WriteTifRaster(ETRmlp_cuenca_fname,ETRmlp_cuenca)
    print('variables guardadas para la estación '+str(estacion))
    col= col + 1

metadatos['ETRmlp(mm/mes)'][:]=valores_ETRP.mean(axis=0)
metadatos.to_csv('H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Q/ANA/usar/metadatos9.csv')