# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:55:54 2020
Crea histogramas de las tendencias
@author: Daniela
"""
#==============================================================================
#- Importar módulos
#==============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import scipy.stats as sc

#==============================================================================
#- Cargar variables del disco
#==============================================================================
#- Definir rutas
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/'
ruta_metadatos = raiz + 'InfoOrganizada/Q/ANA/usar/metadatos11.csv'
ruta_resultados = raiz + 'InfoCalculada/Tendencias/figuras/'
ruta_tendencias = raiz + 'InfoCalculada/Tendencias/tendencias_Sen.csv'
ruta_figuras = raiz + 'infoCalculada/Tendencias/'

#- Cargar metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
usar = metadatos['usar'][:] == 1
metadatos = metadatos.loc[usar,:]
#- Cargar resultados
tendencias = pd.read_csv(ruta_tendencias, index_col=0, encoding = 'utf8')
tendencias = tendencias.loc[usar,:] * 12.

#==============================================================================
#- Tendencias
#==============================================================================
figure,axs = plt.subplots(1,4, figsize = (14,2))#, gridspec_kw={'wspace' : 0.3})#'hspace' : 0.6,

yR = tendencias.loc[:,'R'].values
yRpos = yR[yR > 0.]
bars = np.histogram(yR, bins=10)
x = 0.5*(bars[1][:-1] + bars[1][1:])
wid = bars[1][1:]-bars[1][:-1]
y = 100.*bars[0].astype(float)/bars[0].sum().astype(float)
histR = axs[0].bar(x,y,width=wid)
#axs[0].set_xlabel(u"[mm/año]")
#axs[0].set_ylabel(u"frecuencia [%]")
axs[0].set_xlabel(u"[mm/year]")
axs[0].set_ylabel(u"frequency [%]")
axs[0].set_title(r"a) dR/dt")

yP = tendencias.loc[:,'P'].values
yPpos = yP[yP > 0.]
bars = np.histogram(yP, bins=10)
x = 0.5*(bars[1][:-1] + bars[1][1:])
wid = bars[1][1:]-bars[1][:-1]
y = 100.*bars[0].astype(float)/bars[0].sum().astype(float)
histP = axs[1].bar(x,y,width=wid)
#axs[1].set_xlabel(u"[mm/año]")
axs[1].set_xlabel(u"[mm/year]")
axs[1].set_title(r"b) dP/dt")

yETR = tendencias.loc[:,'ETR'].values
yETRpos = yETR[yETR > 0.]
bars = np.histogram(yETR, bins=10)
x = 0.5*(bars[1][:-1] + bars[1][1:])
wid = bars[1][1:]-bars[1][:-1]
y = 100.*bars[0].astype(float)/bars[0].sum().astype(float)
histETR = axs[2].bar(x,y,width=wid)
#axs[2].set_xlabel(u"[mm/año]")
axs[2].set_xlabel(u"[mm/year]")
axs[2].set_title(r"c) dETR/dt")

ydSdt = tendencias.loc[:,'dS'].values
ydSdtpos = ydSdt[ydSdt > 0.]
bars = np.histogram(ydSdt, bins=10)
x = 0.5*(bars[1][:-1] + bars[1][1:])
wid = bars[1][1:]-bars[1][:-1]
y = 100.*bars[0].astype(float)/bars[0].sum().astype(float)
histdSdt = axs[3].bar(x,y,width=wid)
#axs[3].set_xlabel(u"[mm/año]")
axs[3].set_xlabel(u"[mm/year]")
axs[3].set_title(r"d) $d^2$S/$dt^2$")
plt.savefig(ruta_figuras + 'hist_tend_ENG.png', dpi=300, bbox_inches = 'tight')

#==============================================================================
#- Tendencias
#==============================================================================
