# -*- coding: utf-8 -*-
"""
Created on Wed May 01 13:41:42 2019

Sirve para cargar los datos extraidos a csv de la Base de datos de la ANA
y extraer las series para guardarlas en el formato csv usado en la tesis

@author: Daniela
"""

#==============================================================================
# Importar módulos
#==============================================================================
import numpy as np
import pandas as pd
import copy as copy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as datetime


#==============================================================================
# Rutas
#==============================================================================

ruta_csvmdb='G:/Mi unidad/Maestria/Tesis/2019-1Final/01_DATOS/InfoCruda/ANA/Vazoes.csv'
ruta_csvtesis='G:/Mi unidad/Maestria/Tesis/2019-1Final/01_DATOS/InfoOrganizada/Q/ANA/'
ruta_csvmdb_metadatos='G:/Mi unidad/Maestria/Tesis/2019-1Final/01_DATOS/InfoCruda/ANA/Estacao.csv'

#==============================================================================
# Leer datos mdb
#==============================================================================

# Leer csvmdb con información de caudal
usecols=['EstacaoCodigo','Data','Maxima','Minima','Media','MediaStatus']
dtype={'EstacaoCodigo':'str','Data':'str','Maxima':'float','Minima':'float','Media':'float','MediaStatus':'int'}
csvmdb=pd.read_csv(ruta_csvmdb,usecols=usecols,dtype=dtype)
csvmdb.Data=pd.to_datetime(csvmdb['Data'][:])

# Leer csvmdb con información de las estaciones
usecols=['Codigo','Nome','Latitude','Longitude','Altitude','AreaDrenagem','PeriodoDescLiquidaInicio','PeriodoDescLiquidaFim']
dtype={'Codigo':'str','Nome':'str','Latitude':'float','Longitude':'float','Altitude':'float','AreaDrenagem':'float','PeriodoDescLiquidaInicio':'str','PeriodoDescLiquidaFim':'str'}
csvmdb_metadatos=pd.read_csv(ruta_csvmdb_metadatos,usecols=usecols,dtype=dtype)
csvmdb_metadatos.PeriodoDescLiquidaInicio=pd.to_datetime(csvmdb_metadatos['PeriodoDescLiquidaInicio'][:])
csvmdb_metadatos.PeriodoDescLiquidaFim=pd.to_datetime(csvmdb_metadatos['PeriodoDescLiquidaFim'][:])

#==============================================================================
# procesar datos
#==============================================================================

# codigos de las 204 estaciones que tienen datos de caudal
codigos_estaciones_csvmdb=np.unique(csvmdb['EstacaoCodigo'])

# ¿todas las estaciones con datos tienen metadatos? sí, y todas las estaciones aparecen sólo una vez en la tabla de metadatos
estaciones_datosymetadatos=[]
for estacion in codigos_estaciones_csvmdb:
#    print((csvmdb_metadatos['Codigo']==estacion).sum(), estacion)
    if (csvmdb_metadatos['Codigo']==estacion).sum().astype(bool):
        estaciones_datosymetadatos.append(estacion)

# Crear metadatos a guardar
#metadatos=pd.DataFrame(index=estaciones_datosymetadatos,columns=['codigo','nombre','latitud','longitud','altitud','area','fecha_inicio_metadatos','fecha_fin_metadatos','fecha_inicio_datos','fecha_fin_datos'])
metadatos=pd.DataFrame(index=estaciones_datosymetadatos,columns=['nombre','latitud','longitud','altitud','area_metadatos','fecha_inicio_metadatos','fecha_fin_metadatos','fecha_inicio_datos','fecha_fin_datos','meses_faltantes'])

# 
fecha_maximorum=pd.to_datetime('01/01/2000')
fecha_minimorum=pd.to_datetime('01/01/2000')

estaciones_remover=[]
estaciones_condatos=[]

estacion=metadatos.index[1]

for estacion in estaciones_datosymetadatos:
    # Extracción de metadatos
    fila_metadatos=np.where(csvmdb_metadatos['Codigo']==estacion)[0]
    #metadatos['codigo'][estacion]=estacion
    metadatos['nombre'][estacion]=csvmdb_metadatos['Nome'][fila_metadatos].values[0]
    metadatos['latitud'][estacion]=csvmdb_metadatos['Latitude'][fila_metadatos].values[0]
    metadatos['longitud'][estacion]=csvmdb_metadatos['Longitude'][fila_metadatos].values[0]
    metadatos['altitud'][estacion]=csvmdb_metadatos['Altitude'][fila_metadatos].values[0]
    metadatos['area_metadatos'][estacion]=csvmdb_metadatos['AreaDrenagem'][fila_metadatos].values[0]
    metadatos['fecha_inicio_metadatos'][estacion]=csvmdb_metadatos['PeriodoDescLiquidaInicio'][fila_metadatos].values[0]
    metadatos['fecha_fin_metadatos'][estacion]=csvmdb_metadatos['PeriodoDescLiquidaFim'][fila_metadatos].values[0]
    
    # Cálculo de metadatos
    filas_estacion=csvmdb.EstacaoCodigo==estacion
    csvmdb_estacion=csvmdb[:][filas_estacion].copy()
    meses_con_datos=np.isnan(csvmdb_estacion.Media)==False
    csvmdb_estacion=csvmdb_estacion[:][meses_con_datos].copy()
    if csvmdb_estacion.size==0:  
        estaciones_remover.append(estacion)
    else:
        estaciones_condatos.append(estacion)
        csvmdb_estacion=csvmdb_estacion.sort_values(by='Data')
        fechas=np.unique(csvmdb_estacion.Data)
        fecha_min=fechas.min()
        fecha_minimorum=pd.Series([fecha_min,fecha_minimorum]).min()
        fecha_max=fechas.max()
        fecha_maximorum=pd.Series([fecha_max,fecha_maximorum]).max()
        metadatos['fecha_inicio_datos'][estacion]=fecha_min
        metadatos['fecha_fin_datos'][estacion]=fecha_max
        
        # Formato de tesis a estaciones
        timerange=pd.date_range(start=fecha_min,end=fecha_max,freq='MS')
        datos_estacion=pd.Series(index=timerange,name=estacion)
        
        # Encontrar fechas repetidas con valores incongruentes para remover
        remover_fechas=[]
        if fechas.size<csvmdb_estacion['Data'].size:
#            print('en la estación '+estacion+' hay fechas repetidas')
            valores,indices,inverse,cantidad=np.unique(csvmdb_estacion.Data,return_index=True,return_counts=True,return_inverse=True)
            fechas_repetidas=valores[cantidad>1]
            for fecha_r in fechas_repetidas:
                repetidas=csvmdb_estacion.Data==fecha_r
                fecha_print=str(csvmdb_estacion['Data'][repetidas].values[0])
                diferencia=int(100.*(np.max(np.abs(csvmdb_estacion['Media'][repetidas].values-csvmdb_estacion['Media'][repetidas].values[0])))/csvmdb_estacion['Media'][repetidas].values[0])
#                print (fecha_print+' tiene una diferencia máxima de '+str(diferencia)+'%')
                if diferencia>10:
                    remover_fechas.append(fecha_r)        
        
        dias_difdeuno=[]
        for index in csvmdb_estacion.index:
            fecha_i=pd.to_datetime(csvmdb_estacion['Data'][index])
            fecha_uno=fecha_i
            if fecha_i.day!=1:
                dias_difdeuno.append(fecha_i)
#                print('en la estación '+estacion+' la fecha '+str(fecha_i)+' tiene un día diferente de 1')
                fecha_uno=pd.datetime(year=fecha_i.year,month=fecha_i.month,day=1)
            if fecha_i in remover_fechas:
                datos_estacion[fecha_uno]=np.nan
            else:
                datos_estacion[fecha_uno]=csvmdb_estacion['Media'][index]
#        plt.figure()
#        datos_estacion.plot()
        datos_estacion.to_csv(ruta_csvtesis+estacion+'.csv',header=True)

metadatos=metadatos.loc[estaciones_condatos].copy()
metadatos.to_csv(ruta_csvtesis+'metadatos.csv')


# construir matriz de datos con todas las estaciones
fechasmorum=pd.date_range(start=fecha_minimorum,end=fecha_maximorum,freq='MS')
matriz_datos=pd.DataFrame(index=fechasmorum,columns=estaciones_condatos)

for estacion in estaciones_condatos:
    csv_estacion=pd.read_csv(ruta_csvtesis+estacion+'.csv', index_col=0)
    indices_estacion=pd.to_datetime(csv_estacion.index)
    matriz_datos.loc[indices_estacion,estacion]=csv_estacion.values.ravel()


matriz_datos.to_csv(ruta_csvtesis+'matriz_Q.csv')
