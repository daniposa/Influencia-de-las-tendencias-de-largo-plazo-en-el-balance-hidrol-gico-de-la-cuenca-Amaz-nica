# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 13:38:13 2019
Toma los datos de GRACE y los transforma en una serie de 
tiempo para cada cuenca, que se guarda como un csv.
@author: Daniela Posada Gil
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
ruta_metadatos='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Q/ANA/usar/metadatos7.csv'
ruta_dS='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoCruda/S_GRACE/GLDAS_NOAH10_M.A200101_201501.totalH2O.nc.nc4'
ruta_cuencas_tif='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Cuencas/areapixel/tif'

#- rango de fechas dS MODIFICAR
meses=['01','02','03','04','05','06','07','08','09','10','11','12']

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
valores_dST=np.empty((0,110))# Evapotranspiración total mensual
valores_dSP=np.empty((0,110))# Evapotranspiración promedio mensual
dSmlp_mtrx=np.zeros_like(cuenca_base['mtrx'])# Evapotranspiración media de largo plazo

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
#- Leer netcdf de dS
#==============================================================================

#- leer archivo netcdf de dS
dS_netcdf=nc.Dataset(ruta_dS)

#- calcular variables necesarias para la función que lo convierte en diccionario raster
variable = 'Water_Thickness'# unidades [cm]
lat_dim = 1
lon_dim = 2
time_dim = 0

#- Fechas que contiene el netcdf
times=dS_netcdf['Time'][:]
dates=nc.num2date(times,dS_netcdf['Time'].units,calendar=dS_netcdf['Time'].calendar)

#- Fechas como índices de dataframe
dates_pd=pd.to_datetime(dates)#- Las fechas que hay

#- El rango de tiempo completo (no excluye meses faltantes)
dia_inicio = '01/' + meses[dates.min().month - 1] + '/' + str(dates.min().year)
date_start=pd.to_datetime(str(dates.min().year)+'/' + meses[dates.min().month - 1] + '/01',format='%Y/%m/%d')
date_end=pd.to_datetime(str(dates.max().year)+'/' + meses[dates.max().month - 1] + '/01',format='%Y/%m/%d')
date_range=pd.date_range(date_start , date_end , freq='MS')

num_meses=times.size#- Número de meses


#==============================================================================
#- Construir series de dS y raster de dS media
#==============================================================================

for time_to_extract in np.arange(num_meses):
    #time_to_extract=0
    time0=time.time()    
    print(str(date_range[time_to_extract]))
    #- convertir netcdf a raster
    # leer las propiedades de georeferenciación del ráster
    dims = [dim for dim in dS_netcdf.variables[variable].dimensions]
    xdim = np.array(dS_netcdf.variables[dims[lon_dim]])
    ydim = np.array(dS_netcdf.variables[dims[lat_dim]])
    time_ = dS_netcdf.variables[dims[time_dim]]
        
    #- calcular resolución
    dx = np.average(xdim[1:]-xdim[0:np.size(xdim)-1])
    dy = np.average(ydim[1:]-ydim[0:np.size(ydim)-1])
    
    #- leer matriz para el tiempo específico
    mtrx=np.array(dS_netcdf.variables[variable][time_to_extract])
    mtrx=mtrx * 10.#[cm] a [mm]
    
    #- cambiar latitudes de [0 - 360] a [-180 - 180]
    mtrx=np.concatenate((mtrx[:,180:],mtrx[:,:180]),axis=1)
    xdim[180:]=xdim[180:]-360.
    xdim = np.concatenate((xdim[180:],xdim[:180]))
        
    #- Como la matriz está invertida en Y hay que volverla al derecho
    ydim = ydim[::-1]
    mtrx = np.flipud(mtrx)
    dy = -dy
    
    #- cacular propiedades raster
    clsz = 0.5*(dx-dy)
    xll = np.min(xdim)-0.5*dx
    yll = np.min(ydim)+0.5*dy
    nodt = dS_netcdf[variable]._FillValue
    
    #- construir el diccionario raster
    dS_rst=rst.BuildRaster(xll,yll,clsz,nodt,mtrx)
    rst.ChangeNoData(dS_rst,-9999.0)
    #rst.WriteTifRaster('H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/dS/dS_rst.tif',dS_rst)
    
    #- remuestrear mes a resolución de cuencas
    dS_resampled=rst.SampleRastToRast(dS_rst,cuenca_base)
    inan,jnan=np.where(dS_resampled['mtrx']<=0.0)
    dS_resampled['mtrx'][inan,jnan]=0.0
    
    #- dS media de largo plazo [mm/mes]
    dSmlp_mtrx=dSmlp_mtrx+dS_resampled['mtrx']
    
    #- preparar para guardar info del mes
    valores_dST=np.append(valores_dST,np.zeros((1,110)),axis=0)# dS total mensual
    valores_dSP=np.append(valores_dSP,np.zeros((1,110)),axis=0)# dS promedio mensual
    col = 0
    for estacion in lista_estaciones:
        #estacion=lista_estaciones[0]
        #print(estacion)
        
        #- Calcular dS en area
        not_nan=(dS_resampled['mtrx'][mascaras[col]]>0.0).astype(float)
        dS_area_mtrx=dS_resampled['mtrx'][mascaras[col]]*areas_pixeles[col]*0.001*not_nan #[m3/mes]
        
        #- dS total mensual [Hm3/mes]
        dST=dS_area_mtrx.sum()/(10.**6.)
        
        valores_dST[-1,col]=dST
        
        AT=areas_pixeles[col].sum() #[m2]
        AT_sin_nan=(areas_pixeles[col]*not_nan).sum()
        
        #- dS promedio mensual [mm/mes]
        dSP=dST*(10.**6.)/AT_sin_nan*1000.
        valores_dSP[-1,col]=dSP
        col = col+ 1
    time1=time.time()
    print(time1-time0)

#- Guardar raster de dSmlp en todo el dominio espacial[mm/mes]
dSmlp_mtrx=dSmlp_mtrx/num_meses
dSmlp_mtrx[dSmlp_mtrx == 0.0]=cuenca_base['nodt']
dSmlp=rst.BuildRaster(cuenca_base['xll'],cuenca_base['yll'],cuenca_base['clsz'],cuenca_base['nodt'],dSmlp_mtrx)
dSmlp_fname='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/dS/dS_media_largo_plazo/'+'dSmlp.tif'
rst.WriteTifRaster(dSmlp_fname,dSmlp)

#- Guardar series de dS y dSmlp para cada cuenca
col=0
for estacion in lista_estaciones:
    
    dSmlp_cuenca_mtrx=np.zeros_like(cuenca_base['mtrx'])
    dSmlp_cuenca_mtrx[dSmlp_cuenca_mtrx == 0.0]=cuenca_base['nodt']
    dSmlp_cuenca=rst.BuildRaster(cuenca_base['xll'],cuenca_base['yll'],cuenca_base['clsz'],cuenca_base['nodt'],dSmlp_cuenca_mtrx)
    
    #- Serie dS total (dST)[Hm3/mes]
    serie_dST=ConstruirSerieMensual(dia_inicio,valores_dST[:,col])
    dST_fname='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/dS/dS_total_mensual/'+str(estacion)+'.csv'
    st.EscribirSerie(dST_fname,serie_dST)
    
    #- Serie dS promedio mensual (dSP)[mm/mes]
    serie_dSP=ConstruirSerieMensual(dia_inicio,valores_dSP[:,col])
    dSP_fname='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/dS/dS_media_mensual/'+str(estacion)+'.csv'
    st.EscribirSerie(dSP_fname,serie_dSP)
    
    #- Ráster dS media de largo plazo [mm/mes]
    dSmlp_cuenca['mtrx'][mascaras[col]]=dSmlp_mtrx[mascaras[col]]
    
    dSmlp_cuenca_fname='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/dS/dS_media_largo_plazo/'+'dSmlp_'+str(estacion)+'.tif'
    rst.WriteTifRaster(dSmlp_cuenca_fname,dSmlp_cuenca)
    print('variables guardadas para la estación '+str(estacion))
    col= col + 1

metadatos['dSmlp(mm/mes)'][:]=np.nanmean(valores_dSP,axis=0)
metadatos.to_csv('H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Q/ANA/usar/metadatos8.csv')
