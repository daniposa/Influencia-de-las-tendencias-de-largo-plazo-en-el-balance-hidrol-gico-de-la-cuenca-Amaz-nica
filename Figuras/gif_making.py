# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 16:56:34 2020

@author: Daniela
"""
import imageio as imageio

im1 = imageio.imread('B:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/reconstruccion/IndicadoresError/fig_bandasP5P95_ENG/14300000.png')
im2 = imageio.imread('B:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/reconstruccion/IndicadoresError/fig_bandasP5P95_ENG/17050001.png')
im3 = imageio.imread('B:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/reconstruccion/IndicadoresError/fig_bandasP5P95_ENG/12650000.png')

imgif=[im1,im2,im3]
imageio.mimsave('B:/00_Backup_Tesis/2019-1Final/03_Publicaciones/AGU/Poster/Reconstruction/reconstruction2.gif', imgif,fps=1.51)
