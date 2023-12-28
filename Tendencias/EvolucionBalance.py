# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 19:37:25 2020
Calcula el  del balance hídrico general en el largo plazo
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
#from PyEMD import EMD
#emd=EMD

#==============================================================================
#- rutas
#==============================================================================
# Ruta carpeta raiz
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/'

# Ruta de los metadatos
ruta_metadatos = raiz + 'InfoOrganizada/Q/ANA/usar/metadatos11.csv'

# Ruta de las series de tiempo
ruta_series = raiz + 'InfoOrganizada/reconstruccion/datos_recons_rpetrds_rez_definitiva.csv'

# Ruta resultados
ruta_resultados = raiz + 'infoCalculada/'
ruta_balance = ruta_resultados + 'EvolucionBalance/'

#==============================================================================
#- Leer la información
#==============================================================================
#- Leer metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
series =  metadatos.index.values
usar = metadatos['usar'][:] == 1
series_usar = metadatos.loc[usar,:].index

#- Leer la matriz de datos reconstruidos
matriz_series_original = pd.read_csv(ruta_series, index_col=0, parse_dates=True)
matriz_series = matriz_series_original.copy()
#==============================================================================
#- cambiar dS por dS/dt
#==============================================================================
#for serie in series:
#    #serie = series[0]
#    nombre = 'dS_' + str(serie)
#    valores = matriz_series[nombre].values
#    gradiente = np.gradient(valores)    
#    matriz_series[nombre] = gradiente

#==============================================================================
#- calcular evolucion balance
#==============================================================================
# lista de variables hidrologicas
variables = ['R', 'P', 'ETR', 'dS']

# Calcular y guardar EMD para cada serievariable
for serie in series[:-1]:
    #serie = series[0]
    # Separar series estacion
    nombres = [variable + '_' + str(serie) for variable in variables]
    series_variables = matriz_series.loc[:,nombres]
    series_variables.insert(4, 'P-E-R_'+str(serie), 0.)
    series_variables.insert(5, '(SF-SI)/Tlp_'+str(serie), 0.)
    series_variables.insert(6, '(SF-SI)/Tcp_'+str(serie), 0.)
    series_variables.insert(7, 'errbal_cp_'+str(serie), 0.)
    series_variables.loc[:,'P-E-R_' + str(serie)] = series_variables.loc[:,'P' + '_' + str(serie)] - series_variables.loc[:,'ETR' + '_' + str(serie)] - series_variables.loc[:,'R' + '_' + str(serie)]
    series_variables.loc[:,'(SF-SI)/Tlp_' + str(serie)] = series_variables.loc[:,'dS' + '_' + str(serie)] - series_variables.iloc[0,3]
    series_variables.loc[1:,'(SF-SI)/Tcp_' + str(serie)] = series_variables.iloc[1:,3].values - series_variables.iloc[:-1,3].values
    series_variables.loc[:,'errbal_cp_' + str(serie)] = series_variables.loc[:,'P' + '_' + str(serie)] - series_variables.loc[:,'ETR' + '_' + str(serie)] - series_variables.loc[:,'R' + '_' + str(serie)]-series_variables.loc[:,'(SF-SI)/Tcp_' + str(serie)] 
    range_serie = np.arange(1,np.shape(series_variables)[0]+1)
    range_serie = np.reshape(range_serie, (range_serie.size,1))
    series_cummean = series_variables.cumsum() / np.concatenate((range_serie,range_serie,range_serie,range_serie,range_serie,range_serie,range_serie,range_serie),axis=1)
    series_variables.loc[:,'P-E-R_' + str(serie)] = series_cummean.iloc[:,4]
    series_variables.loc[:,'(SF-SI)/Tlp_' + str(serie)] = (series_variables.loc[:,'(SF-SI)/Tlp_' + str(serie)].values / range_serie.T)[0]
    evolucion_balance = series_variables.iloc[:,[4,5]]
    # Calcular IMFs
    #valores_dS = evolucion_balance.iloc[:,0].values
    #IMF_dS = EMD().emd(valores_dS, np.arange(1,np.size(valores)+1))
    #valores_PER = evolucion_balance.iloc[:,1].values
    #IMF_PER = EMD().emd(valores_PER, np.arange(1,np.size(valores)+1))
    
    #evolucion_balance.insert(2, 'rdS_'+str(serie), 0.)
    #evolucion_balance.insert(3, 'rP-E-R_'+str(serie), 0.)
    
    #evolucion_balance.loc[:,'rdS_'+str(serie)] = evolucion_balance.loc[:,'dS_'+str(serie)].values - IMF_dS[0,:] - IMF_dS[1,:] - IMF_dS[2,:]
    #evolucion_balance.loc[:,'rP-E-R_'+str(serie)] = evolucion_balance.loc[:,'P-E-R_'+str(serie)].values - IMF_PER[0,:] - IMF_PER[1,:] - IMF_PER[2,:]
    
    figure = plt.figure(figsize = (10,3))
    #evolucion_balance.plot(style = ['k-','k--','r-','r--'])
    evolucion_balance.plot(style = ['k-','k--'])
    #plt.subplot(N + 1,1,1)
    plt.title(str(serie) + ' - ' + str(metadatos.loc[serie,'nombre']) + ' - ' + str(metadatos.loc[serie,'Corriente']))
    #plt.xlabel("Tiempo [meses]")
    plt.xlabel("Time [months]")
    plt.ylabel(u"(SF-SI) / (P-ETR-R)" + " [mm]")
    plt.savefig(ruta_balance + '/' + 'figuras_ENG/' + str(serie) + '.png', dpi=300, bbox_inches = "tight")
    if serie in series_usar:
        plt.savefig(ruta_balance + '/' + 'figuras_ENG/usar/' + str(serie) + '.png', dpi=300, bbox_inches = "tight")
    plt.close()
    fin = series_variables.index[-1]
    metadatos.loc[serie,'Sf-Si/T (mm/mes)'] = series_variables.loc[fin,u'(SF-SI)/Tlp_' + str(serie)]
    metadatos.loc[serie,'prom_err_bal_cp(mm/mes)'] = series_variables.loc[:,u'errbal_cp_' + str(serie)].mean()
    

metadatos.to_csv(ruta_metadatos[:-6]+'12.csv')

