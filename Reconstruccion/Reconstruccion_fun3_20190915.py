# -*- coding: utf-8 -*-
#==============================================================================
#------------------------------------------------------------------------------
# -- FUNCIONES RECONSTRUCCION DE SERIES DE TIEMPO USANDO FUNCIONES ORTOGONALES EMPIRICAS
#------------------------------------------------------------------------------
#==============================================================================
"""
Created on Mon Mar 28 01:30:48 2016

@author: Daniela
"""

import pandas as pd
import numpy as np
#==============================================================================
# -- Funcion para estandarizar las series
#==============================================================================

def fn_stn(in_ds):
    """
    Estandariza las series
    
    INPUT:
    
    -in_ds = Series de tiempo como pandas dataframe con fechas en los índices y 
        estaciones en las columnas
    
    OUTPUT:
    
    -in_stn_ds: series de tiempo estandarizadas como un pandas dataframe.
    
    -in_mea: medias de las series en un dataframe.
    
    -in_std: Desviaciones estándar en un dataframe.
        
    """
    # Create matrix to fill with means:
    in_mea=pd.DataFrame(np.zeros((1,in_ds.columns.size)),index=['mean'],columns=in_ds.columns)
    
    # Create matrix to fill with standard deviations:
    in_std=pd.DataFrame(np.zeros((1,in_ds.columns.size)),index=['std'],columns=in_ds.columns)
    
    # Create matrix to fill with mins:
    in_min=pd.DataFrame(np.zeros((1,in_ds.columns.size)),index=['min'],columns=in_ds.columns)
    
    # Calculate means, standard deviations and mins to fill the matrices:
    for i in in_mea.columns:
        aux_mon_val=in_ds[i][:].values
        in_mea[i]['mean']=np.nanmean(aux_mon_val)
        in_std[i]['std']=np.nanstd(aux_mon_val)
        in_min[i]['min']=np.nanmin(aux_mon_val)
    # Series standarization:
    # create matrix to fill with standarized series
    in_stn_ds=pd.DataFrame(np.zeros(in_ds.shape), index=in_ds.index,columns=in_ds.columns)
    for i in in_stn_ds.columns:
        for j in in_stn_ds.index:
            in_stn_ds[i][j]=(in_ds[i][j] - in_mea[i]['mean'])/(in_std[i]['std'])
    return (in_stn_ds, in_mea, in_std, in_min)

#==============================================================================
# -- Funcion para desestandarizar las series
#==============================================================================
def fn_destn1(in_stn_ds,in_mea,in_std,in_min):
    """
    Desestandariza una sola serie con media=0 y std=1, recuperando el valor original de
    su media y desviación estándar
    
    Parameters:
    ----------
    
    in_stn_ds : Pandas DataFrame
            serie estandarizada
    
    in_mea : Pandas DataFrame
            media de la serie
    
    in_std : Pandas DataFrame
            desviación estándar de la serie

    in_min : Pandas DataFrame
            mínimo valor de la serie
    
    Returns:
    --------
    
    in_uns_ds : Pandas DataFrame
        Serie desestadarizada
    """
    # Create matrix to fill with unstn_ds:
    in_uns_ds=in_stn_ds.copy()
    # Unstandarize:
    for k in in_stn_ds.index:
        in_uns_ds[k]=in_stn_ds[k]*in_std+in_mea
        if in_uns_ds[k] <= 0.1 * in_min:
            in_uns_ds[k]=in_min
    return in_uns_ds

#==============================================================================
# -- Funcion para desestandarizar las series
#==============================================================================
def fn_destn2(in_stn_ds,in_mea,in_std,in_min):
    """
    Desestandariza series con media=0 y std=1, recuperando el valor original de
    su media y desviación estándar
    
    Parameters:
    ----------
    
    in_stn_ds : Pandas DataFrame
            series estandarizadas
    
    in_mea : Pandas DataFrame
            medias de las series
    
    in_std : Pandas DataFrame
            desviación estándar de las series
    
    Returns:
    --------
    
    in_uns_ds : Pandas DataFrame
        Series desestadarizadas
    """
    # Create matrix to fill with unstn_ds:
    in_uns_ds=pd.DataFrame(np.zeros(in_stn_ds.shape),index=in_stn_ds.index,columns=in_stn_ds.columns)
    # Unstandarize:
    for k in in_stn_ds.index:
        for j in in_stn_ds.columns:
            in_uns_ds[j][k]=in_stn_ds[j][k]*in_std[j]['std']+in_mea[j]['mean']
            if in_uns_ds[j][k] <= 0.:
                in_uns_ds[j][k]=in_min[j]['min']
    return in_uns_ds
#============================================================================== 
# -- Calcular la matriz de Toeplitz
#==============================================================================
def fn_toep(in_stn_ds, use_cov = False):
    """
    Crea la matriz de Toeplitz de un conjunto de series de tiempo. Es una matriz cuadrada
    y simetrica donde cada elemento i,j contiene la covarianza/correlación de la serie i con la serie j
    
    Parameters:
    ----------
    
    in_ds : Pandas DataFrame
        Data series as a pandas dataframe with dates in the index and 
        stations in the columns
    
    use_cov : Bool, default False
        if False correlation used instead of covariance. If True covariance is 
        used.
    
    Returns:
    ------
    
    toep : Pandas DataFrame
        Toeplitz matrix
    """
    if use_cov==True:
        toep=pd.DataFrame(in_stn_ds.cov().values,index=in_stn_ds.columns,columns=range(in_stn_ds.columns.size))
    else:
        toep=pd.DataFrame(in_stn_ds.corr().values,index=in_stn_ds.columns,columns=range(in_stn_ds.columns.size))
    return toep

#==============================================================================
# -- Calculate Eigenvalues and Eigenvectors
#==============================================================================
#Sorted eigenvalues and eigenvectors function:
def fn_eig_val_vec(in_toep):
    """
    As the toeplitz matrix is a square symetric matrix: 
    - All eigenvalues of a real symmetric matrix are real.
    -Eigenvectors corresponding to distinct eigenvalues are
    orthogonal.
    
    Parameters:
    -----------
    
    in_toep : Toeplitz matrix as a pandas dataframe
    
    Returns:
    --------
    
    in_sort_eig_val : pandas DataFrame
    
    in_sort_eig_vec : pandas DataFrame
    
    in_FOE_sort : pandas DataFrame
    """
    aux_toep_array=in_toep.values
    aux_eig_val,aux_eig_vec=np.linalg.eig(aux_toep_array)
    sort_arg = np.argsort(aux_eig_val)
    sort_arg = sort_arg[::-1]
    aux_sort_eig_val=np.array(aux_eig_val)[sort_arg]
    aux_sort_eig_vec=np.array(aux_eig_vec)[:,sort_arg]
    in_FOE_sort= np.array(in_toep.columns)[sort_arg]
    in_sort_eig_vec=pd.DataFrame(aux_sort_eig_vec, index=in_toep.index, columns=in_FOE_sort)
    in_sort_eig_val=pd.DataFrame(aux_sort_eig_val, index=in_FOE_sort)
    in_sort_cumvar=(in_sort_eig_val/in_sort_eig_val.sum()).cumsum()
    return in_sort_eig_val,in_sort_eig_vec,in_sort_cumvar

#==============================================================================
# -- Calculate Principal Components
#==============================================================================

def fn_PCs(in_stn_ds, in_eig_vec):
    """
    Principal components are time series with the oscillation modes of the set of 
    time series.
    
    Rows of the eig vectors matrix must be ordered according to the standarized series columns
    """
    #sort stand_ds in the same order of eig_vals and convert stand_ds from pandas dataframe to a numpy array
    aux_stn_ds_array=np.array(in_stn_ds.values)
    #Replace nans with zeros
    aux_stn_ds_array=np.nan_to_num(aux_stn_ds_array)
    
    aux_eig_vec_array=np.array(in_eig_vec.values)
    #Matrix multiplication
    aux_PCs_array=np.dot(aux_stn_ds_array,aux_eig_vec_array)
    #make it a data_frame
    PCs=pd.DataFrame(data=np.array(aux_PCs_array), index=in_stn_ds.index, columns=in_eig_vec.columns)
    return PCs

#==============================================================================
# -- Calculate Reconstructed standarized timeseries Dani
#==============================================================================
# Define reconstruction function:
def Recons_dani(in_eig_vec, in_pcs, in_num_of_pcs, in_stn_ds):
    # Create a numpy array to save the reconstruction matrix to fill gaps:
    aux_rec_fill_dani_sds=np.zeros((in_stn_ds.shape[0], in_stn_ds.shape[1]))
    
    # Create a numpy array to save the reconstructed standarized data series:
    aux_rec_dani_sds=np.array(in_stn_ds.values)
    
    # Multiply PCs with chosen e_vec coefficients:
    evec_x_pcs=np.zeros((in_stn_ds.shape[0],in_num_of_pcs))
    e_vec_s=np.array(in_eig_vec.values)[:,0:in_num_of_pcs] # all chosen e_vec to reconstruct all timeseries
    pcs_array=np.array(in_pcs.values)[:,0:in_num_of_pcs] # all Chosen PCs to reconstruct all timeseries
    
    for k in range(in_eig_vec.shape[1]):
        e_vector=e_vec_s[k,:] # Eigen vectors coefficients only for timeserie k
        for l in range(in_num_of_pcs):
            evec_x_pcs[:,l]=e_vector[l]*pcs_array[:,l] # each coefficients multiplyed by each PCs on each column
        aux_rec_fill_dani_sds[:,k]=evec_x_pcs.sum(1) # The sum of all multiplications is the reconstruction timeserie of timeserie at position k
    rec_fill_dani_sds=pd.DataFrame(aux_rec_fill_dani_sds,index=in_stn_ds.index,columns=in_stn_ds.columns)
    aux_correct_std=1/rec_fill_dani_sds.std() # Correct standard deviation
    rec_fill_dani_sds_correct = rec_fill_dani_sds * aux_correct_std
    aux_rec_fill_dani_sds_correct=rec_fill_dani_sds_correct.values
    for k in range(aux_rec_fill_dani_sds_correct.shape[0]):
        for l in range(aux_rec_fill_dani_sds_correct.shape[1]):
            if np.isnan(aux_rec_dani_sds[k,l]):
                aux_rec_dani_sds[k,l]=aux_rec_fill_dani_sds_correct[k,l] #fill gaps with the reconstructed timeseries    
    rec_dani_df=pd.DataFrame(aux_rec_dani_sds,index=in_stn_ds.index,columns=in_stn_ds.columns) #create a pandas dataframe with the reconstructed timeseries
    
    return rec_dani_df, rec_fill_dani_sds_correct

#==============================================================================
# -- Reconstruction Ghill
#==============================================================================

def ReconsGhill(in_ts, in_per_var, in_num_of_lags, correct_negat=True):
    #-1) Build matrix of timeseries lags
    mat_arr=np.zeros((len(in_ts),in_num_of_lags+1))*np.nan
    for i in range(in_num_of_lags+1):
        mat_arr[:,i]=np.append(in_ts.values[i::],np.zeros((i))*np.nan)
    mat=pd.DataFrame(data=mat_arr,index=in_ts.index,columns=range(in_num_of_lags+1))
    
    #-2) Standarize timeseries
    stns,means,stds=fn_stn(mat)
    
    #-3) Calculate Toeplitz matrix
    toep=fn_toep(stns,use_cov=True)
    
    #-4) Calculate eigenthings
    eival,eivec,var=fn_eig_val_vec(toep)
    in_num_of_pcs=np.where(var.values>in_per_var)[0][0]
    
    #-5) Calculate PCs
    PCs=fn_PCs(stns, eivec)
    
    #-6) Reconstruct
    # Create a numpy array to save the reconstruction matrix to fill gaps
    aux_fill_stns=np.zeros((stns.shape[0], stns.shape[1]))
    # Create a numpy array to save the reconstructed standarized data series:
    rec_stns=np.array(stns.values)
    # Create a numpy array to calculate lineal combination multiplication
    eivecxpcs=np.zeros((stns.shape[0],in_num_of_pcs))
    # array with all chosen eivec to reconstruct all timeseries
    eivec_ch=np.array(eivec.values)[:,0:in_num_of_pcs]
    # array with all Chosen PCs to reconstruct all timeseries
    pcs_ch=np.array(PCs.values)[:,0:in_num_of_pcs]
    # calculate reconstruction timeseries
    for k in range(eivec_ch.shape[1]):
        coef_eivec_k=eivec_ch[k,:] # Eigen vectors coefficients only for timeserie k
        for l in range(in_num_of_pcs):
            eivecxpcs[:,l]=coef_eivec_k[l]*pcs_ch[:,l] # each coefficients multiplyed by each PCs on each column
        aux_fill_stns[:,k]=eivecxpcs.sum(1) # The sum of all multiplications is the reconstruction timeserie of timeserie at position k
    fill_stns=pd.DataFrame(data=aux_fill_stns,index=stns.index,columns=stns.columns)
    aux_corr_stns=1./fill_stns.std()# Correct standard deviation
    rec_stns_corr = fill_stns * aux_corr_stns
    rec_stns_corr_arr=rec_stns_corr.values
    for k in range(rec_stns_corr_arr.shape[0]):
        for l in range(rec_stns_corr_arr.shape[1]):
            if np.isnan(rec_stns[k,l]):
                rec_stns[k,l]=rec_stns_corr_arr[k,l] #fill gaps with the reconstructed timeseries
    rec_stns_df=pd.DataFrame(data=rec_stns,index=stns.index,columns=stns.columns) #create a pandas dataframe with the reconstructed timeseries
    #-7) Unstandarize
    rec = fn_destn(in_stn_ds=rec_stns_df,in_mea=means,in_std=stds)
    #-8) Change negative values to minhist:
    if correct_negat==True:
        q_min=rec[:][mat.columns[0]].min()
        rec.values[rec.values<0]=q_min
    return rec, in_num_of_pcs

#==============================================================================
# -- Validation Reconstruccion Dani
#==============================================================================
# Define reconstruction function:
def recons_serie_dani(serie, in_stn_ds, in_mea, in_std, in_min, porc_var, max_iter = 50, umbral = 0.005 ):
    """
    Toma una serie y la devuelve reconstruida. Para la reconstrucción usa un 
    conjunto de series base.
    
    Parameters:
    ----------
    
    serie:
        string.
        código de la serie que se va a reconstruir.
    
    in_stn_ds:
        Pandas_Dataframe.
        Dataframe con las series base mas la serie a reconstruir estandarizadas.
    
    in_mea:
        Pandas Dataframe.
        DataFrame con las medias de las series base mas la serie a reconstruir.
    
    in_std:
        Pandas_Dataframe.
        Dataframe con las desviaciones estándar de las series base mas la serie
        a reconstruir.
    
    in_min:
        Pandas_dataframe.
        DataFrame con los valores mínimos históricos de las series base mas la 
        serie a reconstruir.
        
    max_iter:
        integer.
        Número máximo de iteraciones.
        
    umbral:
        float.
        Porcentaje de la desviación estándar que puede variar una reconstrucción respecto a la siguiente 
    
    Returns:
    --------
    
    serie_reconstruida:
        Pandas_Serie.
        Serie reconstruida.
    """
    #============================================================================== 
    # -- Localizar los valores faltantes
    #==============================================================================
    #FALTA LIDIAR CON QUE NO SE SABE DÓNDE HAY FALTANTES ¿O SÍ?
    
    is_na = np.isnan(in_stn_ds.values)
    i_na,j_na = np.where(is_na)
    
    iteracion = 0
    mean_dif = 100.
    
    iter_stn_ds = in_stn_ds.where(is_na == False, 0.0)
    while (iteracion < max_iter and mean_dif > umbral):
        # -- Calcular la matriz de Toeplitz
        in_toep=fn_toep(iter_stn_ds)
        
        # -- Calculate Eigenvalues and Eigenvectors
        in_eig_val,in_eig_vec,eig_porc_var=fn_eig_val_vec(in_toep)
        
        # -- Calcular Componentes Principales
        in_pcs=fn_PCs(iter_stn_ds, in_eig_vec)
        
        # -- Calcular Series de Reconstrucción estandarizadas con el método de Dani
        #- reconstruir con componentes principales que expliquen el porcentaje porc_var de la varianza
        num_porc_var = (eig_porc_var <= porc_var).astype(int)
        in_num_of_pcs = num_porc_var.sum()[0]
        
        recons_stn_ds, fill_stn_ds = Recons_dani(in_eig_vec, in_pcs, in_num_of_pcs, iter_stn_ds)
        
        # -- Comparar la nueva reconstrucción con la iteración anterior
        iter_stn_ds = iter_stn_ds.where(is_na)
        fill_stn_ds = fill_stn_ds.where(is_na)
        
        iter_difs = fill_stn_ds.values - iter_stn_ds.values
        mean_dif = np.abs(np.nanmean(iter_difs))
        
        # -- serie de iteración
        iter_stn_ds = in_stn_ds.where(is_na == False, fill_stn_ds)
        
        iteracion = iteracion + 1
        print(mean_dif, iteracion)
    
    usd_reconstructed_stn_ds = iter_stn_ds.copy()
        
    #==============================================================================
    # -- Desestandarizar Series de Reconstrucción
    #==============================================================================
    in_serie = usd_reconstructed_stn_ds.loc[:,serie]
    in_mea_serie = in_mea[serie]['mean']
    in_std_serie = in_std[serie]['std']
    in_min_serie = in_min[serie]['min']
    serie_reconstruida=fn_destn1(in_serie,in_mea_serie,in_std_serie,in_min_serie)

    return serie_reconstruida