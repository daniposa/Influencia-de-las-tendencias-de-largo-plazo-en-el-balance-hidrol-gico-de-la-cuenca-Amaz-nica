# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:55:54 2020
Crea diagramas  de dispersión de la tendencia vs. el área y el valor promedio de la variable
@author: Daniela
"""
#==============================================================================
#- Importar módulos
#==============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
#import Figuras as fig
from sklearn.linear_model import LinearRegression
import scipy.stats as sc

#==============================================================================
#- Cargar variables del disco
#==============================================================================
#- Definir rutas
raiz = 'B:/00_Backup_Tesis/2019-1Final/01_DATOS/'
ruta_metadatos = raiz + 'InfoOrganizada/Q/ANA/usar/metadatos11.csv'
ruta_resultados = raiz + 'InfoCalculada/Tendencias/figuras/'
ruta_tendencias = raiz + 'InfoCalculada/Tendencias/tendencias_Sen.csv'
ruta_figuras = raiz + 'infoCalculada/Tendencias/scaters/coefcorrPearson/'

#- Cargar metadatos
metadatos = pd.read_csv(ruta_metadatos, index_col=0, encoding = 'utf8')
usar = metadatos['usar'][:] == 1
metadatos = metadatos.loc[usar,:]
#- Cargar resultados
tendencias = pd.read_csv(ruta_tendencias, index_col=0, encoding = 'utf8')
tendencias = tendencias.loc[usar,:] * 12.

#==============================================================================
#- Tendencias Positivas vs valor medio
#==============================================================================
figure,axs = plt.subplots(1,4, figsize = (14,2), gridspec_kw={'wspace' : 0.3})#'hspace' : 0.6,

yR = tendencias.loc[:,'R'].values
xR = metadatos.loc[:,u'recRmlp(mm/mes)'].values
yRpos = yR[yR > 0.]
xRpos = xR[yR > 0.]
logyRpos = np.log10(yRpos)
logxRpos = np.log10(xRpos)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxRpos,logyRpos)
linx = [xRpos.min() , xRpos.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxRpos,logyRpos)[0]
scaR = axs[0].scatter(xRpos,yRpos,color='r', marker = '^')
linR = axs[0].plot(linx,liny,'r')
axs[0].set_xscale("log")
axs[0].set_yscale("log")
axs[0].set_xlabel("[mm]")
axs[0].set_ylabel(u"[mm/año]")
axs[0].set_title(r"a) dR/dt_pos vs. R" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

yP = tendencias.loc[:,'P'].values
xP = metadatos.loc[:,u'recPmlp(mm/mes)'].values
yPpos = yP[yP > 0.]
xPpos = xP[yP > 0.]
logyPpos = np.log10(yPpos)
logxPpos = np.log10(xPpos)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxPpos,logyPpos)
linx = [xPpos.min() , xPpos.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxPpos,logyPpos)[0]
scaP = axs[1].scatter(xPpos,yPpos,color='r', marker = '^')
linP = axs[1].plot(linx,liny,'r')
axs[1].set_xscale("log")
axs[1].set_yscale("log")
axs[1].set_xlabel("[mm]")
#axs[2].set_ylabel(u"[mm/año]")
axs[1].set_title(r"b) dP/dt_pos vs. P" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

yETR = tendencias.loc[:,'ETR'].values
xETR = metadatos.loc[:,u'recETRmlp(mm/mes)'].values
yETRpos = yETR[yETR > 0.]
xETRpos = xETR[yETR > 0.]
logyETRpos = np.log10(yETRpos)
logxETRpos = np.log10(xETRpos)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxETRpos,logyETRpos)
linx = [xETRpos.min() , xETRpos.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxETRpos,logyETRpos)[0]
scaETR = axs[2].scatter(xETRpos,yETRpos,color='r', marker = '^')
linETR = axs[2].plot(linx,liny,'r')
axs[2].set_xscale("log")
axs[2].set_yscale("log")
#axs[2].set_ylabel(u"[mm/año]")
axs[2].set_xlabel("[mm]")
axs[2].set_title(r"c) dETR/dt_pos vs. ETR" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

ydSdt = tendencias.loc[:,'dS'].values
xdSdt = metadatos.loc[:,u'recdS/dtmlp(mm/mes)'].values + 10.
ydSdtpos = ydSdt[ydSdt > 0.]
xdSdtpos = xdSdt[ydSdt > 0.]
logydSdtpos = np.log10(ydSdtpos)
logxdSdtpos = np.log10(xdSdtpos)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxdSdtpos,logydSdtpos)
linx = [xdSdtpos.min() , xdSdtpos.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxdSdtpos,logydSdtpos)[0]
scadSdt = axs[3].scatter(xdSdtpos,ydSdtpos,color='r', marker = '^')
lindSdt = axs[3].plot(linx,liny,'r')
axs[3].set_xscale("log")
axs[3].set_yscale("log")
axs[3].set_xlabel("[mm]")
#axs[2].set_ylabel(u"[mm/año]")
axs[3].set_title(r"d) $d^2$S/$dt^2$_pos vs. dSdt" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))
plt.savefig(ruta_figuras + 'tend_media_pos.png', dpi=300, bbox_inches = 'tight')
#==============================================================================
#- Tendencias Negativas vs valor medio
#==============================================================================
figure,axs = plt.subplots(1,4, figsize = (14,2), gridspec_kw={'wspace' : 0.3})#'hspace' : 0.6,

#yR = tendencias.loc[:,'R'].values
#xR = metadatos.loc[:,u'recRmlp(mm/mes)'].values
yRneg = np.abs(yR[yR < 0.])
xRneg = xR[yR < 0.]
logyRneg = np.log10(yRneg)
logxRneg = np.log10(xRneg)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxRneg,logyRneg)
linx = [xRneg.min() , xRneg.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxRneg,logyRneg)[0]
scaR = axs[0].scatter(xRneg,yRneg,color='b', marker = 'v')
linR = axs[0].plot(linx,liny,'b')
axs[0].set_xscale("log")
axs[0].set_yscale("log")
axs[0].set_ylabel(u"[mm/año]")
axs[0].set_xlabel("[mm]")
axs[0].set_title(r"e) dR/dt_neg vs. R" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

#yP = tendencias.loc[:,'P'].values
#xP = metadatos.loc[:,u'recPmlp(mm/mes)'].values
yPneg = np.abs(yP[yP < 0.])
xPneg = xP[yP < 0.]
logyPneg = np.log10(yPneg)
logxPneg = np.log10(xPneg)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxPneg,logyPneg)
linx = [xPneg.min() , xPneg.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxPneg,logyPneg)[0]
scaP = axs[1].scatter(xPneg,yPneg,color='b', marker = 'v')
linP = axs[1].plot(linx,liny,'b')
axs[1].set_xscale("log")
axs[1].set_yscale("log")
axs[1].set_xlabel("[mm]")
#axs[1].set_ylabel(u"mm/año")
axs[1].set_title(r"f) dP/dt_neg vs. P" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

#yETR = tendencias.loc[:,'ETR'].values
#xETR = metadatos.loc[:,u'recETRmlp(mm/mes)'].values
yETRneg = np.abs(yETR[yETR < 0.])
xETRneg = xETR[yETR < 0.]
logyETRneg = np.log10(yETRneg)
logxETRneg = np.log10(xETRneg)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxETRneg,logyETRneg)
linx = [xETRneg.min() , xETRneg.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxETRneg,logyETRneg)[0]
scaETR = axs[2].scatter(xETRneg,yETRneg,color='b', marker = 'v')
linETR = axs[2].plot(linx,liny,'b')
axs[2].set_xscale("log")
axs[2].set_yscale("log")
axs[2].set_ylim(yETRneg.min()*0.9, yETRneg.max()*1.1)
axs[2].set_xlim(xETRneg.min()*0.99, xETRneg.max()*1.01)
#axs[2].set_ylabel(u"[mm/año]")
axs[2].set_xlabel(" \n\n[mm]")
axs[2].set_title(r"g) dETR/dt_neg vs. ETR" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

#ydSdt = tendencias.loc[:,'dS'].values
#xdSdt = metadatos.loc[:,u'recdS/dtmlp(mm/mes)'].values + 100.
ydSdtneg = np.abs(ydSdt[ydSdt < 0.])
xdSdtneg = xdSdt[ydSdt < 0.]
logydSdtneg = np.log10(ydSdtneg)
logxdSdtneg = np.log10(xdSdtneg)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxdSdtneg,logydSdtneg)
linx = [xdSdtneg.min() , xdSdtneg.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxdSdtneg,logydSdtneg)[0]
scadSdt = axs[3].scatter(xdSdtneg,ydSdtneg,color='b', marker = 'v')
lindSdt = axs[3].plot(linx,liny,'B')
axs[3].set_xscale("log")
axs[3].set_yscale("log")
axs[3].set_ylim(ydSdtneg.min()*0.9, ydSdtneg.max()*1.1)
axs[3].set_xlim(xdSdtneg.min()*0.999, xdSdtneg.max()*1.001)
axs[3].set_xlabel("[mm]")
axs[3].set_title(r"h) $d^2$S/$dt^2$_neg vs. dSdt" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))
plt.savefig(ruta_figuras + 'tend_media_neg.png', dpi=300, bbox_inches = 'tight')
#==============================================================================
#- Tendencias Positivas vs area
#==============================================================================
xR = xP = xETR = xdSdt = metadatos.loc[:,u'Area_rst(km2)'].values
##xR = xP = xETR = xdSdt = metadatos.loc[:,u'area_metadatos'].values
#
figure,axs = plt.subplots(1,4, figsize = (14,2), gridspec_kw={'wspace' : 0.3})#, sharex = True)#'hspace' : 0.6,

#yR = tendencias.loc[:,'R'].values
#xR = metadatos.loc[:,u'recRmlp(mm/mes)'].values
#yRpos = yR[yR > 0.]
xRpos = xR[yR > 0.]
#logyRpos = np.log10(yRpos)
logxRpos = np.log10(xRpos)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxRpos,logyRpos)
linx = [xRpos.min() , xRpos.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxRpos,logyRpos)[0]
scaR = axs[0].scatter(xRpos,yRpos,color='r', marker = '^')
linR = axs[0].plot(linx,liny,'r')
axs[0].set_xscale("log")
axs[0].set_yscale("log")
axs[0].set_ylabel(u"[mm/año]")
axs[0].set_xlabel(r"[$km^2$]")
axs[0].set_title(r"i) dR/dt_pos vs. A" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

#yP = tendencias.loc[:,'P'].values
#xP = metadatos.loc[:,u'recPmlp(mm/mes)'].values
#yPpos = yP[yP > 0.]
xPpos = xP[yP > 0.]
#logyPpos = np.log10(yPpos)
logxPpos = np.log10(xPpos)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxPpos,logyPpos)
linx = [xPpos.min() , xPpos.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxPpos,logyPpos)[0]
scaP = axs[1].scatter(xPpos,yPpos,color='r', marker = '^')
linP = axs[1].plot(linx,liny,'r')
axs[1].set_xscale("log")
axs[1].set_yscale("log")
#axs[1].set_ylabel(u"[mm/año]")
axs[1].set_xlabel(r"[$km^2$]")
axs[1].set_title(r"j) dP/dt_pos vs. A" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

#yETR = tendencias.loc[:,'ETR'].values
#xETR = metadatos.loc[:,u'recETRmlp(mm/mes)'].values
#yETRpos = yETR[yETR > 0.]
xETRpos = xETR[yETR > 0.]
#logyETRpos = np.log10(yETRpos)
logxETRpos = np.log10(xETRpos)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxETRpos,logyETRpos)
linx = [xETRpos.min() , xETRpos.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxETRpos,logyETRpos)[0]
scaETR = axs[2].scatter(xETRpos,yETRpos,color='r', marker = '^')
linETR = axs[2].plot(linx,liny,'r')
axs[2].set_xscale("log")
axs[2].set_yscale("log")
#axs[2].set_ylabel(u"[mm/año]")
axs[2].set_xlabel(r"[$km^2$]")
axs[2].set_title(r"k) dETR/dt_pos vs. A" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

#ydSdt = tendencias.loc[:,'dS'].values
#xdSdt = metadatos.loc[:,u'recdS/dtmlp(mm/mes)'].values + 100.
#ydSdtpos = ydSdt[ydSdt > 0.]
xdSdtpos = xdSdt[ydSdt > 0.]
#logydSdtpos = np.log10(ydSdtpos)
logxdSdtpos = np.log10(xdSdtpos)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxdSdtpos,logydSdtpos)
linx = [xdSdtpos.min() , xdSdtpos.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxdSdtpos,logydSdtpos)[0]
scadSdt = axs[3].scatter(xdSdtpos,ydSdtpos,color='r', marker = '^')
lindSdt = axs[3].plot(linx,liny,'r')
axs[3].set_xscale("log")
axs[3].set_yscale("log")
#axs[1,1].set_ylabel(u"[mm/año]")
axs[3].set_xlabel(r"[$km^2$]")
axs[3].set_title(r"l) $d^2$S/$dt^2$_pos vs. A" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

plt.savefig(ruta_figuras + 'tend_area_pos.png', dpi=300, bbox_inches = 'tight')

#==============================================================================
#- Tendencias Negativas vs area
#==============================================================================
#xR = xP = xETR = xdSdt = metadatos.loc[:,u'Area_rst(km2)'].values
##xR = xP = xETR = xdSdt = metadatos.loc[:,u'area_metadatos'].values
#
figure,axs = plt.subplots(1,4, figsize = (14,2), gridspec_kw={'wspace' : 0.3})#, sharex = True)#'hspace' : 0.6,

#yR = tendencias.loc[:,'R'].values
#xR = metadatos.loc[:,u'recRmlp(mm/mes)'].values
#yRneg = np.abs(yR[yR < 0.])
xRneg = xR[yR < 0.]
#logyRneg = np.log10(yRneg)
logxRneg = np.log10(xRneg)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxRneg,logyRneg)
linx = [xRneg.min() , xRneg.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxRneg,logyRneg)[0]
scaR = axs[0].scatter(xRneg,yRneg,color='b', marker = 'v')
linR = axs[0].plot(linx,liny,'b')
axs[0].set_xscale("log")
axs[0].set_yscale("log")
axs[0].set_ylabel(u"[mm/año]")
axs[0].set_xlabel(r"[$km^2$]")
axs[0].set_title(r"m) dR/dt_neg vs. A" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

#yP = tendencias.loc[:,'P'].values
#xP = metadatos.loc[:,u'recPmlp(mm/mes)'].values
#yPneg = np.abs(yP[yP < 0.])
xPneg = xP[yP < 0.]
#logyPneg = np.log10(yPneg)
logxPneg = np.log10(xPneg)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxPneg,logyPneg)
linx = [xPneg.min() , xPneg.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxPneg,logyPneg)[0]
scaP = axs[1].scatter(xPneg,yPneg,color='b', marker = 'v')
linP = axs[1].plot(linx,liny,'b')
axs[1].set_xscale("log")
axs[1].set_yscale("log")
#axs[1].set_ylabel(u"[mm/año]")
axs[1].set_xlabel(r"[$km^2$]")
axs[1].set_title(r"n) dP/dt_neg vs. A" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

#yETR = tendencias.loc[:,'ETR'].values
#xETR = metadatos.loc[:,u'recETRmlp(mm/mes)'].values
#yETRneg = np.abs(yETR[yETR < 0.])
xETRneg = xETR[yETR < 0.]
#logyETRneg = np.log10(yETRneg)
logxETRneg = np.log10(xETRneg)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxETRneg,logyETRneg)
linx = [xETRneg.min() , xETRneg.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxETRneg,logyETRneg)[0]
scaETR = axs[2].scatter(xETRneg,yETRneg,color='b', marker = 'v')
linETR = axs[2].plot(linx,liny,'b')
axs[2].set_xscale("log")
axs[2].set_yscale("log")
axs[2].set_ylim(yETRneg.min()*0.9, yETRneg.max()*1.1)
axs[2].set_xlim(xETRneg.min()*0.9, xETRneg.max()*1.1)
#axs[2].set_ylabel(u"[mm/año]")
axs[2].set_xlabel(r"[$km^2$]")
axs[2].set_title(r"o) dETR/dt_neg vs. A" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

#ydSdt = tendencias.loc[:,'dS'].values
#xdSdt = metadatos.loc[:,u'recdS/dtmlp(mm/mes)'].values + 100.
#ydSdtneg = np.abs(ydSdt[ydSdt < 0.])
xdSdtneg = xdSdt[ydSdt < 0.]
#logydSdtneg = np.log10(ydSdtneg)
logxdSdtneg = np.log10(xdSdtneg)
pendiente, intercepto, r_value, p_value, std_err = sc.linregress(logxdSdtneg,logydSdtneg)
linx = [xdSdtneg.min() , xdSdtneg.max()]
liny = [ (10**intercepto)*(linx[0]**pendiente), (10**intercepto)*(linx[1]**pendiente)]
r_value = sc.spearmanr(logxdSdtneg,logydSdtneg)[0]
scadSdt = axs[3].scatter(xdSdtneg,ydSdtneg,color='b', marker = 'v')
lindSdt = axs[3].plot(linx,liny,'b')
axs[3].set_xscale("log")
axs[3].set_yscale("log")
axs[3].set_ylim(ydSdtneg.min()*0.9, ydSdtneg.max()*1.1)
axs[3].set_xlim(xdSdtneg.min()*0.9, xdSdtneg.max()*1.1)
#axs[3].set_ylabel(u"[mm/año]")
axs[3].set_xlabel(r"[$km^2$]")
axs[3].set_title(r"p) $d^2$S/$dt^2$_neg vs. A" "\n" r"[y={:2.2}x^{:2.2}] $\rho$={:2.2}".format(10**intercepto,pendiente,r_value))

plt.savefig(ruta_figuras + 'tend_area_neg.png', dpi=300, bbox_inches = 'tight')





