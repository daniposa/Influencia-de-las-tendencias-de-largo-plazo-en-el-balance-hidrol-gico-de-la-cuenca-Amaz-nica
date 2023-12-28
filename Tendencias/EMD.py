# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 19:37:25 2020
Descompone las series de tiempo en sus funciones ortogonales empíricas
@author: Daniela
"""
#==============================================================================
#------------------------------------------------------------------------------
#- Descomposición en modos empíricos
#------------------------------------------------------------------------------
#==============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PyEMD import EMD
emd=EMD

#==============================================================================
#- rutas
#==============================================================================
# Ruta carpeta raiz
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/'

# Ruta de los metadatos
ruta_metadatos = raiz + 'InfoOrganizada/Q/ANA/usar/metadatos10.csv'

# Ruta de las series de tiempo
ruta_series = raiz + 'InfoOrganizada/reconstruccion/datos_recons_rpetrds_rez_definitiva.csv'

# Ruta resultados
ruta_resultados = raiz + 'infoCalculada/'
ruta_emd = ruta_resultados + 'EMD/'

#==============================================================================
#- Leer la información
#==============================================================================
#- Leer metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
series =  metadatos.index.values

#- Leer la matriz de datos reconstruidos
matriz_series_original = pd.read_csv(ruta_series, index_col=0, parse_dates=True)
matriz_series = matriz_series_original.copy()
#==============================================================================
#- cambiar dS por dS/dt
#==============================================================================
for serie in series:
    #serie = series[0]
    nombre = 'dS_' + str(serie)
    valores = matriz_series[nombre].values
    gradiente = np.gradient(valores)    
    matriz_series[nombre] = gradiente

#==============================================================================
#- calcular EMD
#==============================================================================
# lista de variables hidrologicas
variables = ['R', 'P', 'ETR', 'dS']

# Calcular y guardar EMD para cada serievariable
for serie in series:
    #serie = series[0]
    for variable in variables:
        #variable = variables[0]
        # Separar serie
        nombre = variable + '_' + str(serie)
        valores = matriz_series[nombre].values
        range_serie = np.arange(np.size(valores))
        # Calcular IMFs
        IMF = EMD().emd(valores, range_serie)
        # Organizar
        N = IMF.shape[0]
        imfs = pd.DataFrame(data = IMF.T ,index = matriz_series.index, columns = range(N))
        # Guardar IMFs
        imfs.to_csv(ruta_emd + variable + '/' + nombre + '.csv')
        # Graficar IMFs
        plt.figure()
        plt.subplot(N + 1,1,1)
        plt.title(nombre)
        plt.xlabel("Tiempo [meses]")
        plt.plot(range_serie, valores, 'r')
        for n, imf in enumerate(IMF):
            plt.subplot(N + 1,1,n+2)
            plt.plot(range_serie, imf, 'g')
            plt.title("IMF "+str(n+1))
            plt.xlabel("Time [s]")
        # guardar IMFs
        plt.savefig(ruta_emd + variable + '/' + 'figuras/' + nombre + '.png', pdi=300)



