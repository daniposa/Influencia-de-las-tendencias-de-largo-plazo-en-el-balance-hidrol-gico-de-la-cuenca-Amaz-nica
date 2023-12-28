# -*- coding: utf-8 -*-
#==============================================================================
#------------------------------------------------------------------------------
# -- FUNCIONES VALIDACIÓN - CÁLCULO DE INDICADORES DE ERROR
#------------------------------------------------------------------------------
#==============================================================================
"""
Created on Sun Sep 15 18:36:26 2019
Funciones par calcular la bondad del método de reconstrucción. Tiene los 
cálculos de todos los estimadores de error para la comparación de 2 series

@author: Daniela
"""

import numpy as np
import scipy as sc
import scipy.stats as st
import pymannkendall as mk
from random import sample
#==============================================================================
# -- Funciones para estimar el error
#==============================================================================

def calcular_error_medio_absoluto_relativo(serie_obs, serie_est):
    """
    Calcula el error medio absoluto de la serie estimada versus la serie observada
    
    Parameters
    ----------
    serie_obs : array
        serie de valores observados
    
    serie_est : array
        serie de valores estimados en la reconstrucción
        
    Returns
    -------
    error_medio_absoluto : float
        Valor del error medio absoluto
        
    """
    error = serie_obs - serie_est
    error_medio_absoluto = 100. * np.nanmean(np.abs(error)) / np.nanmean(serie_obs)  
    return error_medio_absoluto

def calcular_nash(serie_obs, serie_est):
    """
    Calcula la eficiencia de Nash - Sutcliffe
    
    Parameters
    ----------
    serie_obs : array
        serie de valores observados
    
    serie_est : array
        serie de valores estimados en la reconstrucción
        
    Returns
    -------
    nash : float
        Valor de la eficiencia de Nash - sutcliffe
    """
    error_cuadrado = (serie_obs - serie_est)**2.
    error_cuadrado_media = (serie_obs - np.mean(serie_obs))**2.
    nash = 1. - (np.sum(error_cuadrado) / np.sum(error_cuadrado_media))
    return nash

def calcular_relative_bias(serie_obs, serie_est):
    """
    Calcula el sesgo de la media (bias) de los valores estimados, escalados por
    la magnitud de los valores observados
    
    Parameters
    ----------
    serie_obs : array
        serie de valores observados
    
    serie_est : array
        serie de valores estimados en la reconstrucción
        
    Returns
    -------
    relative_bias : float
        Valor del sesgo de la media (relative bias) escalado
    """
    
    relative_bias = 100. * (np.nansum(serie_obs - serie_est) / np.nansum(serie_obs))
    return relative_bias

def calcular_resultado_KS_test(serie_obs, serie_est, porc_confiabilidad):
    """
    Calcula el resultado de la prueba Kolmogorov - Smirnov no paramétrica
    cuya hipótesis nula es Ho: Las fdp de las 2 variables es la misma, 
    con un porcentaje de confiabilidad especificado. Si se rechaza la hipótesis
    nula se puede concluir que las fdp de las dos variables son diferentes con
    una confiabilidad igual a la especificada, sin embargo, si la hipótesis nula
    no se rechaza no se puede concluir que son iguales las fdp, sino que no hay
    evidencia suficiente para considerar que las fdp son diferentes.
    
    Parameters
    ----------
    serie_obs : array
        serie de valores observados
    
    serie_est : array
        serie de valores estimados en la reconstrucción
        
    porc_confiabilidad : float between 0 and 1
        valor de la confiabilidad con que se busca rechazar la hipótesis nula
        
    Returns
    -------
    resultado_KS_test : binary
        Devuelve 1 si la hipótesis nula NO puede ser rechazada y 0 si se
        rechaza la hipótesis nula.
    """
    
    statistic , pvalue = sc.stats.ks_2samp(serie_obs, serie_est)
    resultado_KS_test = float(pvalue >= (1. - porc_confiabilidad))
    return resultado_KS_test

def calcular_coeficiente_correlacion(serie_obs, serie_est):
    """
    Calcula el coeficiente de correlación de los datos estimados con los observados
    
    Parameters
    ----------
    serie_obs : array
        serie de valores observados
    
    serie_est : array
        serie de valores estimados en la reconstrucción
        
    Returns
    -------
    corr_coef : Real
        Coeficiente de correlación de los valores observados y medidos
    """
    # calcular coeficiente de correlación de Pearson
    #corr_coef=np.corrcoef(serie_obs, serie_est)[0,1]
    # calcular coeficiente de correlacion de Spearman
    corr_coef=st.spearmanr(serie_obs, serie_est)[0]
    return corr_coef

def calcular_recmr(serie_obs, serie_est):
    """
    Calcula la raiz del error cuadrático medio
    
    Parameters
    ----------
    serie_obs : array
        serie de valores observados
    
    serie_est : array
        serie de valores estimados en la reconstrucción
        
    Returns
    -------
    rmse : float
        valor de la raiz del error cuadrático medio como un porcentaje del valor medio
    """
    # calcular raiz del error cuadrático medio
    squared_error=(serie_obs-serie_est)**2
    rmse=(100. * (np.sum(squared_error)/np.size(squared_error))**0.5) / np.mean(serie_obs)
    return rmse

def calcular_prob_rango(valores, minimo = -np.inf, maximo = np.inf):
    """
    Calcula la probabilidad de que una realización de la variable caiga dentro
    del rango [minimo , maximo] a partir de una muestra aleatoria de la variable
    
    Parameters
    ----------
    valores: array
        Vector con una muestra aleatoria de errores calculados
    
    minimo: float or integer
        valor mínimo del rango de valores
        
    maximo: float or integer
        valor máximo del rango de valores
        
    Returns
    -------
    prob_rango: float
        probabilidad de que una realización aleatoria de la variable obtenga
        valores que caigan dentro del rango [minimo , maximo]
    """
    en_rango = np.logical_and(valores >= minimo, valores <= maximo).astype(np.float)
    prob_error_acept = np.sum(en_rango) / np.float(valores.size)
    return prob_error_acept

def calcular_sesgo_tend(serie_obs, serie_est, porc_reemp = 1.,alpha = 0.05):
    """
    Calcula las tendencias de largo plazo y el sesgo de las tendencias
    estimadas respecto a las observadas.
    
    Parameters
    ----------
    serie_obs : array
        serie de valores observados. La serie no puede contener faltantes y 
        debe tener el mismo tamaño que serie_est.
    
    serie_est : array
        serie de valores estimados en la reconstrucción. La serie no puede 
        contener faltantes y debe tener el mismo tamaño que serie_obs.
        
    porc_reemp : float
        opcional, por defecto igual a 1. Porcentaje de datos de la serie 
        observada a reemplazar con los valores estimados en un bloque en 
        posición aleatoria.
    
    alpha : float
        opcional, por defecto igual a 0.05, es igual a 1 - significancia con 
        que se quiere rechazar la hipótesis nula de que no existe tendencia.
    
    Returns
    -------
    sesgo_tendencia : float
        valor del sesgo relativo a la tendencia de la serie observada.
        
    igual_tendencia : bool
        Si el resultado de la prueba Mann Kendall ("creciente", "decreciente", 
        "sin tendencia") para lo observado y lo estimado son iguales devuelve 
        True, y si son diferentes devuelve False.
    """
    #- reemplazar observado con estimado en un bloque del tamaño del porcentaje
    # de datos a reemplazar
    # tamaño de la muestra
    sample_size = int(serie_obs.size * porc_reemp)
    # selección del rango a reemplazar
    posibles_inicios = range(serie_obs.size - sample_size + 1)
    inicio = sample(posibles_inicios , 1)[0]
    rango_reemp = np.arange(start = inicio, stop = inicio + sample_size)
    # reemplazar
    serie_est2 = np.copy(serie_obs)
    serie_est2[rango_reemp] = serie_est[rango_reemp]
    
    #- Calcular prueba Mann Kendall - Hamed Rao y prueba Sen 
    mktest_results_obs = mk.hamed_rao_modification_test(serie_obs, alpha)
    mktest_results_est = mk.hamed_rao_modification_test(serie_est2, alpha)
    tend_obs = mktest_results_obs[7]
    mkt_obs = mktest_results_obs[0]
    tend_est = mktest_results_est[7]
    mkt_est = mktest_results_est[0]
    #print('tend_obs,mkt_obs,tend_est,mkt_est : ',tend_obs,mkt_obs,tend_est,mkt_est)
    #- Calcular sesgo y si las tendencias son iguales
    sesgo_tendencia = (tend_est - tend_obs) / tend_obs
    igual_tend = (mkt_obs == mkt_est)
    return sesgo_tendencia, igual_tend