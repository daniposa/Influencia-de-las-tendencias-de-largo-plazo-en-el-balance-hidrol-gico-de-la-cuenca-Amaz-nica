# -*- coding: utf-8 -*-
"""
Created on Fri Jul 05 11:46:02 2019
Transforma una máscara de cuenca en un objeto cuenca, que es básicamente un 
diccionario ráster cuyos valores son el área de cada pixel con un atributo
adicional que corresponde al área de la cuenca en km2. Guarda tanto el ráster
como la variable pickle.
@author: Daniela
"""

#==============================================================================
#- Importar módulos
#==============================================================================
import rst2series as rst2series
import pandas as pd
import Raster as rst

#==============================================================================
#- Convertir máscara
#==============================================================================
#- rutas de archivos Base
ruta_metadatos='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Q/ANA/usar/metadatos.csv'
ruta_mascaras_tif='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Cuencas/New Folder/'
ruta_areas='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Cuencas/areapixel/area_pixel.csv'
ruta_cuencas_pk='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Cuencas/areapixel/pickle'
ruta_cuencas_tif='H:/00_Backup_Tesis/2019-1Final/01_DATOS/InfoOrganizada/Cuencas/areapixel/tif'
#- cargar metadatos de estaciones usadas
metadatos=pd.read_csv(ruta_metadatos,index_col=0)
lista_estaciones=metadatos.index #lista de estaciones usadas

#- convertir máscara a objeto cuenca
for estacion in ['11450000','12550000','12870000','13550000','17345000']:
    print(estacion)
    
    #- cargar máscara
    ruta_mascara=ruta_mascaras_tif+str(estacion)+'.tif'
    mascara=rst.ReadRaster(ruta_mascara)
    
    #- recortar máscara
    limit=[-82.0,-45.0,-21.0,6.0]
    mascara_clip=rst.ClipRaster(mascara,limit)
    
    #- cargar csv de tabla
    areas=pd.read_csv(ruta_areas, header=0)
    
    #- crear cuenca
    cuenca=rst2series.area_pixel(mascara_clip,areas)
    
    #- guardar raster
    rst.WriteTifRaster(ruta_cuencas_tif+'/'+str(estacion)+'.tif',cuenca)
    
    print('tif guardado')



