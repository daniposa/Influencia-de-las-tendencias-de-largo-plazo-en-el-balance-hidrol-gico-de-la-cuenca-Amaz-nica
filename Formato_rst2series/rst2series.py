# -*- coding: utf-8 -*-
"""
Created on Thu Jul 04 18:01:45 2019

Se definen funciones que sirven para lidiar con los cambios en el área de pixel
debidos a las variaciones de la latitud, y al uso del SRC WGS84

@author: Daniela
"""
#==============================================================================
#- Importar módulos
#==============================================================================
import Raster as rst
import pandas as pd
from copy import copy
import numpy as np
from bisect import bisect_left
import pickle as pk


#==============================================================================
#- Calcular máscara de área de pixeles para un raster a resolución de 30s
#==============================================================================

def area_pixel(mascara,areas,ruta_cuenca=''):
    """
    Calcula a partir de una máscara de unos y ceros, la máscara de área de
    pixeles para una cuenca raster a la misma resolución
    que se usó para calcular la tabla guardada en ruta_areas
    
    Parameters
    ----------
    ruta_mascara : String
        ruta del archivo ráster que contiene la máscara de unos y ceros
    
    ruta_areas : String
        ruta de la tabla en formato csv que contiene el área calcuada en un SIG
        para cada pixel a la misma resolución que la máscara de unos y ceros
    
    ruta_cuenca : List
        (Opcional) Lista de 2 elementos en los que se especifica: [0] la ruta 
        en la que se quiere almacenar la variable de cuenca. [1] extensión con
        la que se quiere guardar la variable, que puede ser '.pk' para
        guardarse como variable de pickle o '.tif' si se desea que se guarde
        como ráster. NOTA: ESTO TODAVÍA NO ES FUNCIONAL
    
    Returns
    -------
    cuenca : Dictionary
        Objeto que contiene los atributos normales de un ráster mas: area_total
        
    """   
    
    #- calcular coordenadas de pixeles
    ii,jj=np.where(mascara['mtrx']>0.0)
    xx,yy=rst.IJtoxy(ii,jj,mascara)
    
    #- rastrear coordenadas en tabla de areas
    m2a_indices=[bisect_left(areas['bottom'], y) for y in yy]
    
    #- crear raster con valores de area de pixel
    cuenca_mtrx=np.empty(mascara['mtrx'].shape,dtype=np.float64)    
    cuenca_mtrx[ii,jj]=areas['area[m2]'][m2a_indices]
    cuenca=rst.BuildRaster(xll=mascara['xll'],yll=mascara['yll'],clsz=mascara['clsz'],nodt=mascara['nodt'],mtrx=cuenca_mtrx)    
    
    #- calcular área cuenca
    area_m2=cuenca_mtrx.sum()
    cuenca['area_km2']=area_m2/(10.0**6.0)
    
    #- guardar archivo de cuenca
    if ruta_cuenca!='':
        formato=ruta_cuenca[1]
        nombre_archivo_pk=ruta_cuenca[0]
        nombre_archivo_tif=ruta_cuenca[0]
        
        if formato=='.pk':
            pk.dump(cuenca,open(nombre_archivo_pk, 'wb'))
        elif formato=='.tif':
            rst.WriteTifRaster(nombre_archivo_tif,cuenca)
    
        else:
            print('formato no válido')
    return cuenca


#==============================================================================
#- Agregar campo de cualquier variable
#==============================================================================

"""
Toma un ráster y trasforma sus valores a la resolución de 30s,
para pnderar sus valores por el área de cada pixel y calcular el valor promedio
sobre la máscara de la cuenca

"""