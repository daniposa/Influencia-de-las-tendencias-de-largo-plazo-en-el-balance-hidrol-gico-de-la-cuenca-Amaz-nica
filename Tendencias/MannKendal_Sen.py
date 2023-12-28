# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:14:59 2020

@author: Daniela
"""
#==============================================================================
#------------------------------------------------------------------------------
#- Descomposición en modos empíricos
#------------------------------------------------------------------------------
#==============================================================================
import numpy as np
import pandas as pd
import pymannkendall as mk
import matplotlib.pyplot as plt

#==============================================================================
#- rutas
#==============================================================================
# Ruta carpeta raiz
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/'

# Ruta de los metadatos
ruta_metadatos = raiz + 'InfoOrganizada/Q/ANA/usar/metadatos10.csv'

# Ruta de las imfs
ruta_emd = raiz + 'infoCalculada/EMD/'

# Ruta resultados
ruta_resultados = raiz + 'infoCalculada/'
#==============================================================================
#- Leer la información
#==============================================================================
#- Leer metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
series =  metadatos.index.values

#==============================================================================
#- calcular Tendencias
#==============================================================================
# lista de variables hidrologicas
variables = ['R', 'P', 'ETR', 'dS']

# Dataframe para almacenar los resultados
tendencias = pd.DataFrame(index = metadatos.index, columns = variables)
mannkendall = pd.DataFrame(index = metadatos.index, columns = variables)

for serie in series[:-1]:
    #serie = series[0]
    for variable in variables:
        #variable = variables[0]
        nombre = variable + '_' + str(serie)
        # Leer imfs de la serie
        imfs = pd.read_csv(ruta_emd + variable + '/' + nombre + '.csv', index_col=0, encoding = 'utf8')
        residuo = imfs.iloc[:,-1].values
        mktest_results = mk.hamed_rao_modification_test(residuo)
        mannkendall[variable][serie] = mktest_results[0]
        hay_tendencia = np.float(mktest_results[1])
        tendencias[variable][serie] = hay_tendencia * mktest_results[7]
        print(mannkendall[variable][serie],tendencias[variable][serie])


tendencias.to_csv(ruta_resultados + 'tendencias_Sen.csv')
mannkendall.to_csv(ruta_resultados + 'tendencias_MK.csv')












