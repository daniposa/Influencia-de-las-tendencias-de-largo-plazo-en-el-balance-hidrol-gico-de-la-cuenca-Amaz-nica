# -*- coding: utf-8 -*-
#==============================================================================
#------------------------------------------------------------------------------
# -- VALIDACION DE LA RECONSTRUCCIÓN
#------------------------------------------------------------------------------
#==============================================================================
"""
Created on Sun Sep 15 11:46:15 2019

Este programa toma las matrices de validación, que contienen las 20 realizaciones
de reconstrucción para cada serie y evalúa las métricas de error que sirven para
evaluar la bondad del método de reconstrucción.

@author: Daniela Posada Gil
"""
#==============================================================================
# -- Importar los modulos requeridos
#==============================================================================

import numpy as np
import pandas as pd
#import Reconstruccion_fun3_20190915 as f
#import matplotlib.pyplot as plt
#import random as random
#import Figuras as Figuras
#import time as time
import Validacion_fun as val

#==============================================================================
# -- Rutas de matrices de validación y lectura de metadatos
#==============================================================================
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/'
ruta_metadatos = raiz + 'Q/ANA/usar/metadatos10.csv'
ruta_resultados_error = raiz + 'reconstruccion/IndicadoresError/resumen_errores.csv'

#- rutas matrices de validación
ruta_reconstruccion_R = raiz + 'reconstruccion/R/reconstruccion_rez/R_' 
ruta_reconstruccion_P = raiz + 'reconstruccion/P/reconstruccion_rez/P_' 
ruta_reconstruccion_ETR = raiz + 'reconstruccion/ETR/reconstruccion_rez/ETR_'
ruta_reconstruccion_dS = raiz + 'reconstruccion/dS/reconstruccion_rez/dS_'

#- cargar metadatos
metadatos=pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')

#==============================================================================
# -- Crear matriz para guardar indicadores de error
#==============================================================================
estaciones = metadatos.index.values

estadisticos = ['m','p']
indicadores_error = ['EMAR','ENS','SESGO','RKS','CC','RECMR','TENDSEN','TENDMK']
variables = ['R','P','ETR','dS']

columnas=[]
for variable in variables:
    for indicador in indicadores_error:
        for estadistico in estadisticos:
            columnas.append(estadistico + indicador + '_' + variable)

resultados_error = pd.DataFrame(index = estaciones , columns = columnas)
#==============================================================================
# -- Calcular indicadores de error
#==============================================================================
for estacion in estaciones:
    #estacion = estaciones[0]
    print(estacion)
    for variable in variables:
        #variable = 'R'
        #variable = 'dS'
        print(variable)
        #- cargar matrices:
        try:
            if variable == 'R':
                ruta_matriz = ruta_reconstruccion_R + str(estacion) + '.csv'
            elif variable == 'P':
                ruta_matriz = ruta_reconstruccion_P + str(estacion) + '.csv'
            elif variable == 'ETR':
                ruta_matriz = ruta_reconstruccion_ETR + str(estacion) + '.csv'
            elif variable == 'dS':
                ruta_matriz = ruta_reconstruccion_dS + str(estacion) + '.csv'
            
            matriz_validacion = pd.read_csv(ruta_matriz, index_col=0, encoding = 'utf8')
        except:
            print('No se pudo cargar la matriz de la variable : ' + variable + str(estacion))
        
        experimentos = [str(i) for i in range(1,21)]
        
        #- crear vector para almacenar los errores de cada serie de validación
        indicadores = pd.DataFrame(index = experimentos, columns = indicadores_error)
        
        #======================================================================
        #- Calcular fdps del error
        #======================================================================
        for i in experimentos:
            #i = experimentos[0]
            
            #- remover nans de series estimada y observada
            estimado = matriz_validacion[i][:].values
            observado = matriz_validacion['0'][:].values
            no_nan = np.logical_or(np.isnan(estimado),np.isnan(observado)) == 0.
            estimado = estimado[no_nan]
            observado = observado[no_nan]
            
            #- calcular errores
            indicadores['EMAR'][i] = val.calcular_error_medio_absoluto_relativo(observado, estimado)
            indicadores['ENS'][i] = val.calcular_nash(observado, estimado)
            indicadores['SESGO'][i] = val.calcular_relative_bias(observado, estimado)
            indicadores['RKS'][i] = val.calcular_resultado_KS_test(observado, estimado, 0.95)
            indicadores['CC'][i] = val.calcular_coeficiente_correlacion(observado, estimado)
            indicadores['RECMR'][i] = val.calcular_recmr(observado, estimado)
            indicadores['TENDSEN'][i], indicadores['TENDMK'][i] = val.calcular_sesgo_tend(observado, estimado, porc_reemp = 0.4)
            
        #- Calcular valores medios de los indicadores de error
        resultados_error['mEMAR_'+variable][estacion] = np.nanmean(indicadores['EMAR'].values)
        print('mEMAR', resultados_error['mEMAR_'+variable][estacion])
        resultados_error['mENS_'+variable][estacion] = np.nanmean(indicadores['ENS'].values)
        print('mENS', resultados_error['mENS_'+variable][estacion])
        resultados_error['mSESGO_'+variable][estacion] = np.nanmean(indicadores['SESGO'].values)
        print('mSESGO', resultados_error['mSESGO_'+variable][estacion])
        resultados_error['mRKS_'+variable][estacion] = np.round(np.nanmean(indicadores['RKS'].values.astype(np.float)))
        print('mRKS', resultados_error['mRKS_'+variable][estacion])
        resultados_error['mCC_'+variable][estacion] = np.nanmean(indicadores['CC'].values)
        print('mCC', resultados_error['mCC_'+variable][estacion])
        resultados_error['mRECMR_'+variable][estacion] = np.nanmean(indicadores['RECMR'].values)
        print('mRECMR', resultados_error['mRECMR_'+variable][estacion])
        resultados_error['mTENDSEN_'+variable][estacion] = np.nanmean(indicadores['TENDSEN'].values)
        print('mTENDSEN', resultados_error['mTENDSEN_'+variable][estacion])
        resultados_error['mTENDMK_'+variable][estacion] = np.round(np.nanmean(indicadores['TENDMK'].values.astype(np.float)))
        print('mTENDMK', resultados_error['mTENDMK_'+variable][estacion])
        
        #- Calcular la probabilidad de que los indicadores caigan en rango aceptable
        resultados_error['pEMAR_'+variable][estacion] = val.calcular_prob_rango(indicadores['EMAR'].values, minimo = 0.0, maximo = 35.0)
        print('pEMAR',resultados_error['pEMAR_'+variable][estacion])
        resultados_error['pENS_'+variable][estacion] = val.calcular_prob_rango(indicadores['ENS'].values, minimo = 0.6, maximo = 1.0)
        print('pENS',resultados_error['pENS_'+variable][estacion])
        resultados_error['pSESGO_'+variable][estacion] = val.calcular_prob_rango(indicadores['SESGO'].values, minimo = -20.0, maximo = 20.0)
        print('pSESGO',resultados_error['pEMAR_'+variable][estacion])
        resultados_error['pRKS_'+variable][estacion] = val.calcular_prob_rango(indicadores['RKS'].values, minimo = 1)
        print('pRKS',resultados_error['pRKS_'+variable][estacion])
        resultados_error['pCC_'+variable][estacion] = val.calcular_prob_rango(indicadores['CC'].values, minimo = 0.6, maximo = 1.0)
        print('pCC',resultados_error['pCC_'+variable][estacion])
        resultados_error['pRECMR_'+variable][estacion] = val.calcular_prob_rango(indicadores['RECMR'].values, minimo = 0.0, maximo = 40.0)
        print('pRECMR',resultados_error['pRECMR_'+variable][estacion])
        resultados_error['pTENDSEN_'+variable][estacion] = val.calcular_prob_rango(indicadores['TENDSEN'].values, minimo = -0.5, maximo = 0.5)
        print('pTENDSEN',resultados_error['pTENDSEN_'+variable][estacion])
        resultados_error['pTENDMK_'+variable][estacion] = val.calcular_prob_rango(indicadores['TENDMK'].values, minimo = 1)
        print('pTENDMK',resultados_error['pTENDMK_'+variable][estacion])
        
#- Guardar resultados
resultados_error.to_csv(ruta_resultados_error)
#==============================================================================
#- Calcular ciclos anuales del error
#==============================================================================

for estacion in estaciones:
    #estacion = estaciones[0]
    print(estacion)
    for variable in variables:
        #variable = 'R'
        #variable = 'dS'
        print(variable)
        #- cargar matrices:
        try:
            if variable == 'R':
                ruta_matriz = ruta_reconstruccion_R + str(estacion) + '.csv'
            elif variable == 'P':
                ruta_matriz = ruta_reconstruccion_P + str(estacion) + '.csv'
            elif variable == 'ETR':
                ruta_matriz = ruta_reconstruccion_ETR + str(estacion) + '.csv'
            elif variable == 'dS':
                ruta_matriz = ruta_reconstruccion_dS + str(estacion) + '.csv'
            
            matriz_validacion = pd.read_csv(ruta_matriz, index_col=0, encoding = 'utf8')
        except:
            print('No se pudo cargar la matriz de la variable : ' + variable + str(estacion))
        
        experimentos = [str(i) for i in range(1,21)]
        
        #======================================================================
        #- Calcular variación temporal del error
        #======================================================================
        # Índices de serie_error y ciclo
        meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
        columnas_ciclo = ['media_obs','desvest_obs','media_est','desvest_est','mediaEMAR', 'desvestEMAR','mediaSESGO', 'desvestSESGO','mediaRECMR', 'desvestRECMR']
        
        indices_series = matriz_validacion.index[np.isnan(matriz_validacion['0'].values)==False]
        columnas_serie = ['media_obs','media_est','desvest_est','mediaEMAR', 'mediaSESGO', 'mediaRECMR']
        
        # Matrices de serie y ciclos del error
        series_error = pd.DataFrame(index = indices_series, columns = columnas_serie)
        ciclos_error = pd.DataFrame(index = meses, columns = columnas_ciclo)
        
        # Llenar series error
        for fecha in indices_series:
            #fecha = indices_series[0]
            #- serie observada
            series_error['media_obs'][fecha] = matriz_validacion['0'][fecha]
            #- media de serie estimada
            series_error['media_est'][fecha] = matriz_validacion['med'][fecha]
            #- desviación estándar de la estimación
            series_error['desvest_est'][fecha] = np.nanstd( matriz_validacion.loc[fecha,'1':'20'])
            #- Cálculo de indicadores de error
            obs = np.zeros((20)) + series_error['media_obs'][fecha]
            est = matriz_validacion.loc[fecha,'1':'20'].values
            no_nan = np.logical_or(np.isnan(est),np.isnan(obs)) == 0.
            est = est[no_nan]
            obs = obs[no_nan]
            series_error['mediaEMAR'][fecha] = val.calcular_error_medio_absoluto_relativo(obs,est)
            series_error['mediaSESGO'][fecha] = val.calcular_relative_bias(obs, est)
            series_error['mediaRECMR'][fecha] = val.calcular_recmr(obs, est)
        #- Guardar resultados
        series_error.to_csv(raiz + 'reconstruccion/IndicadoresError/' + variable + '/series_error_' + str(estacion) + '.csv')
        
        #- Llenar ciclos
        # calcular fechas
        fechas = pd.to_datetime(indices_series)
        for mes in range(12):
            # indices de fechas del mes específico
            esmes = fechas.month == ( mes + 1)
            # ciclo anual de la variable observada
            ciclos_error['media_obs'][meses[mes]] = series_error['media_obs'][indices_series[esmes]].mean()
            ciclos_error['desvest_obs'][meses[mes]] = series_error['media_obs'][indices_series[esmes]].std()
            # ciclo anual de la estimaciones
            ciclos_error['media_est'][meses[mes]] = series_error['media_est'][indices_series[esmes]].mean()
            ciclos_error['desvest_est'][meses[mes]] = series_error['media_est'][indices_series[esmes]].std()
            # ciclo anual del Error medio absoluto relativo
            ciclos_error['mediaEMAR'][meses[mes]] = series_error['mediaEMAR'][indices_series[esmes]].mean()
            ciclos_error['desvestEMAR'][meses[mes]] = series_error['mediaEMAR'][indices_series[esmes]].std()
            # ciclo anual del sesgo
            ciclos_error['mediaSESGO'][meses[mes]] = series_error['mediaSESGO'][indices_series[esmes]].mean()
            ciclos_error['desvestSESGO'][meses[mes]] = series_error['mediaSESGO'][indices_series[esmes]].std()
            # ciclo anual de la raiz del error cuadrático medio
            ciclos_error['mediaRECMR'][meses[mes]] = series_error['mediaRECMR'][indices_series[esmes]].mean()
            ciclos_error['desvestRECMR'][meses[mes]] = series_error['mediaRECMR'][indices_series[esmes]].std()
        ciclos_error.to_csv(raiz + 'reconstruccion/IndicadoresError/' + variable + '/ciclos_error_' + str(estacion) + '.csv')

