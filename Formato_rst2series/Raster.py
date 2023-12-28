# -*- coding: utf-8 -*-
"""
Module Raster
-------------

Author
------
Rendón-Álvarez, J. P., Tue Apr 25 13:02:46 2017. 
E-mails: jprendona@unal.edu.co, pablo.rendon@udea.edu.co

Description
-----------
This module contains functions to read and write raster files

License
-------
This work is licensed under the Creative Commons Attribution-NonComercial-
ShareAlike 4.0 International License. To view a copy o this license, visit
http://creativecommons.org/licenses/by-nc-sa/4.0

Notices
-------
This program is distributed in the hope that it will be used, but without any
warranty. No author or distributor accepts responsability to anyone for
consequences of using them or for whether they serve any particular purpose
or work at all, unless he says so in writing. Everyone is granted permission
to copy, modify an distribute this program, but only under the condition that
this notice and above authority and license notices remain intact
"""

import numpy as np
from osgeo import gdal
from netCDF4 import Dataset
import netCDF4 as nc

def ReadRaster(path):
    
    u"""
    It loads a raster after identifiying the file extension
    
    Parameters
    ----------
    path : text
        Raster file direction in the hard disk
    
    Returns
    -------
    rst : dictionary
        Raster dictionary with the next attribute naming convention:
            - ncols : Number of columns
            - nrows : Number of rows
            - xll   : X-axis coordinate of the lower left corner
            - yll   : Y-axis coordinate of the lower left corner
            - xur   : X-axis coordinate of the upper right corner
            - yur   : Y-axis coordinate of the upper right corner
            - clsz  : Cell size
            - nodt  : Missing data value
            - mtrx  : Data matrix
    """
    
    # It identifies the file extension and reads the raster
    ext=path.lower().split('.')[-1]
    if ext=='asc':
        rst=ReadAsciiRaster(path)
    elif ext=='tif' or ext=='tiff':
        rst=ReadTifRaster(path)
    else:
        print('File format not recognized')
        rst=BuildRaster(0.0,0.0,0.0,0.0,np.array(0))
    return rst
    
def ReadAsciiRaster(path):
    
    u"""
    It loads an Arc/ASCII raster file from the hard disk
    
    Parameters
    ----------
    path : text
        Raster file direction in the hard disk
    
    Returns
    -------
    rst : dictionary
        Raster dictionary with the next attribute naming convention:
            - ncols : Number of columns
            - nrows : Number of rows
            - xll   : X-axis coordinate of the lower left corner
            - yll   : Y-axis coordinate of the lower left corner
            - xur   : X-axis coordinate of the upper right corner
            - yur   : Y-axis coordinate of the upper right corner
            - clsz  : Cell size
            - nodt  : Missing data value
            - mtrx  : Data matrix
    """
    
    #It reads the header information as text
    asc_file=open(path,'r')
    asc_line=asc_file.readline()
    temp,ncols=str.split(asc_line)
    asc_line=asc_file.readline()
    temp,nrows=str.split(asc_line)
    asc_line=asc_file.readline()
    temp,xll=str.split(asc_line)
    asc_line=asc_file.readline()
    temp,yll=str.split(asc_line)
    asc_line=asc_file.readline()
    temp,clsz=str.split(asc_line)
    asc_line=asc_file.readline()
    temp,nodt=str.split(asc_line)
    asc_file.close()
    
    #It converts header information from text to numbers   
    ncols=int(ncols)
    nrows=int(nrows)
    xll=float(xll)
    yll=float(yll)
    clsz=float(clsz)
    nodt=float(nodt)
    
    #It reads the matrix information, builds the raster and returns
    mtrx=np.loadtxt(path,skiprows=6)
        
    #It builds the Raste dictionary and returns
    rst=BuildRaster(xll,yll,clsz,nodt,mtrx)
    ChangeNoData(rst,-9999.0)
    return rst

def ReadNetCDFRaster(path,vrbl):
    
    u"""
    It loads a 2D netCDF raster file from the hard disk
    
    Parameters
    ----------
    path : text
        Raster file direction in the hard disk
    vrbl : text
        Variable to be loaded
    
    Returns
    -------
    rst : dictionary
        Raster dictionary with the next attribute naming convention:
            - ncols : Number of columns
            - nrows : Number of rows
            - xll   : X-axis coordinate of the lower left corner
            - yll   : Y-axis coordinate of the lower left corner
            - xur   : X-axis coordinate of the upper right corner
            - yur   : Y-axis coordinate of the upper right corner
            - clsz  : Cell size
            - nodt  : Missing data value
            - mtrx  : Data matrix
    """
    
    # It reads the georeferenciation properties
    dataset=Dataset(path)
    dims=[dim for dim in dataset.dimensions]
    xdim=np.array(dataset.variables[dims[0]])
    ydim=np.array(dataset.variables[dims[1]])
    dx=np.average(xdim[1:]-xdim[0:np.size(xdim)-1])
    dy=np.average(ydim[1:]-ydim[0:np.size(ydim)-1])
    clsz=0.5*(dx+dy)
    xll=np.min(xdim)-0.5*dx
    yll=np.min(ydim)-0.5*dy
    nodt=dataset.variables[vrbl]._FillValue
    
    # It loads the netCDF Dataset
    mtrx=np.fliplr(np.array(dataset.variables[vrbl])).T
    mtrx[mtrx==np.NaN]=nodt
    dataset.close()
    
    # It builds the Raster dictionary and returns
    rst=BuildRaster(xll,yll,clsz,nodt,mtrx)
    ChangeNoData(rst,-9999.0)
    return rst

def ReadTifRaster(path):
    
    u"""
    It loads a GeoTiff raster file from the hard disk
    
    Parameters
    ----------
    path : text
        Raster file direction in the hard disk
    vrbl : text
        Variable to be loaded
    
    Returns
    -------
    rst : dictionary
        Raster dictionary with the next attribute naming convention:
            - ncols : Number of columns
            - nrows : Number of rows
            - xll   : X-axis coordinate of the lower left corner
            - yll   : Y-axis coordinate of the lower left corner
            - xur   : X-axis coordinate of the upper right corner
            - yur   : Y-axis coordinate of the upper right corner
            - clsz  : Cell size
            - nodt  : Missing data value
            - mtrx  : Data matrix
    """
    
    # It reads the georeferenciation properties and the data matrix
    tif=gdal.Open(path)
    mtrx=tif.GetRasterBand(1).ReadAsArray()
    georef=tif.GetGeoTransform()
    if georef[1]<0:
        xll=georef[0]+georef[1]*mtrx.shape[1]#np.size(mtrx,1)
    else:
        xll=georef[0]
    if georef[5]<0:
        yll=georef[3]+georef[5]*mtrx.shape[0]#np.size(mtrx,0)
    else:
        yll=georef[3]
    clsz=0.5*(np.abs(georef[1])+np.abs(georef[5]))
    nodt=tif.GetRasterBand(1).GetNoDataValue()
    tif=None
    
    # It builds the Raster dictionary and returns
    rst=BuildRaster(xll,yll,clsz,nodt,mtrx)
    ChangeNoData(rst,-9999.0)
    return rst
    
def WriteAsciiRaster(path,rst):

    u"""
    It saves a Raster dictionary in the hard disk using the Arc/ASCII format

    Parameters
    ----------
    path: text
        Direction in the hard disk in which the Arc/ASCII file will be written
    rst: dictionary
        AsciiRaster dictionary to export
    """

    #It builds the header information string    
    hdr='ncols        '+str(rst['ncols'])\
    +'\nnrows        '+str(rst['nrows'])\
    +'\nxllcorner    '+str(rst['xll'])\
    +'\nyllcorner    '+str(rst['yll'])\
    +'\ncellsize     '+str(rst['clsz'])\
    +'\nnodata_value '+str(rst['nodt'])
    
    #It saves data in the hard disk and finishes
    file=open(path,'w')
    file.write(hdr)
    for row in rst['mtrx']:
        line='\n'+' '.join(row.astype('str'))
        file.write(line)
    file.close()
    
def WriteTifRaster(path,rst,prcsn=gdal.GDT_Float32):

    u"""
    It saves a Raster dictionary in the hard disk using the GeoTiff format

    Parameters
    ----------
    path: text
        Direction in the hard disk in which the GeoTiff file will be written
    rst: dictionary
        AsciiRaster dictionary to export
    prcsn: optional, integer
        Data precision. By default gdal.GDT_Float32, but any other data type
        can be specified
    """
    
    # It creates the driver and the file
    driver=gdal.GetDriverByName("GTiff")
    tif=driver.Create(path,rst['ncols'],rst['nrows'],1,prcsn)
    
    # It sets the metadata, band data and finishes
    tif.SetGeoTransform((rst['xll'],rst['clsz'],0.0,rst['yur'],0.0,-rst['clsz']))
    band=tif.GetRasterBand(1)
    band.SetNoDataValue(rst['nodt'])
    band.WriteArray(rst['mtrx'],0,0)
    band.FlushCache()
    tif=None;band=None
    
def BuildRaster(xll,yll,clsz,nodt,mtrx):
    
    u"""
    It builds a Raster dictionary when all of its attributes are specified
    
    Parameters
    ----------
    xll : float
        X-axis coordinate of the lower left corner
    yll : float
        Y-axis coordinate of the lower left corner
    clsz : float
        Cell size
    nodt : number 
        Missing data value
    mtrx : float
        Data array
        
    Returns
    -------
    rst : dictionary
        A dictionary with the raster information
    """
    
    #It calculates aditional necessary information
    nrows=np.size(mtrx,0)
    ncols=np.size(mtrx,1)
    nclls=nrows*ncols
    xur=xll+ncols*clsz
    yur=yll+nrows*clsz
    
    #It assambles the Raster dictinary and returns
    rst={'ncols':ncols,'nrows':nrows,'nclls':nclls,'xll':xll,'yll':yll,\
    'xur':xur,'yur':yur,'clsz':clsz,'nodt':nodt,'mtrx':mtrx}
    return rst

def ChangeNoData(rst,new_nodt):
    
    u"""
    It replaces the no data value in the data array for an specified new no data
    value
    
    Parameters
    ----------
    rst : dictionary
        Raster dictionary
    new_nodt : number
        New no data value
    """
    rst['mtrx'][rst['mtrx']==rst['nodt']]=new_nodt
    rst['nodt']=new_nodt

def ClipRaster(rst,limit):
    
    u"""
    It clips a raster within a square window limit
    
    Parameters
    ----------
    rst : dictionary
        Raster dictionary
    limit : flat
        Vector of square window limit coordinates with the next order
        [xmin,xmax,ymin,ymax]
    """
    
    # It defines the row-col index limits
    col_min=max(0,np.int((limit[0]-rst['xll'])/rst['clsz'])+1)
    col_max=min(np.int((limit[1]-rst['xll'])/rst['clsz']),rst['ncols'])
    row_min=max(0,np.int((rst['yur']-limit[3])/rst['clsz'])+1)
    row_max=min(np.int((rst['yur']-limit[2])/rst['clsz']),rst['nrows'])
    
    # It clips the data matrix and defines the new georeferenciation
    mtrx=rst['mtrx'][row_min:row_max,col_min:col_max]
    xll=rst['xll']+col_min*rst['clsz']
    yll=rst['yur']-row_max*rst['clsz']
    
    # It builds the clipped raster and returns
    clip_rst=BuildRaster(xll,yll,rst['clsz'],rst['nodt'],mtrx)
    return clip_rst

def vector2raster(x,y,val,clsz,nodt = -9999.):
    """
    Takes a value vector, its latitudes and longitudes, and builds a raster 
    with the minimum extent that contains all the values pixels
    
    Parameters
    ----------
    x : array
        array with the same size as values that contains longitudes
    
    y : array
        array with the same size as values that contains latitudes
    
    val : array
        array with the values to put into the raster
    
    clsz : float
        cell size of the raster to build
    
    nodt : float
        value that indicates that there is no data 
    
    Returns
    -------
    
    raster : raster
        raster object that contains the values in it's only band    
    """
    xmin = np.min(x) - 3.*clsz
    xmax = np.max(x) + 3.*clsz
    ymin = np.min(y) - 3.*clsz
    ymax = np.max(y) + 3.*clsz
    xll = xmin - 0.5*clsz
    yll = ymin - 0.5*clsz
    columns = np.int((xmax + clsz - xmin)/clsz)
    rows = np.int((ymax-ymin+clsz)/clsz)
    mtrx = np.zeros((rows,columns)) + nodt
    raster = BuildRaster(xll, yll, clsz, nodt, mtrx)
    i,j = XYtoij(x, y, raster)
    #cont = 0
    #for k,l in zip(i,j):
    #    raster['mtrx'][k,l]=val[cont]
    #    cont = cont + 1
    raster['mtrx'][i,j]=val
    return raster

def NullsInBounds(rst):
    
    u"""
    It sets no data values in the bounds of raster
    
    Parameters
    ----------
    rst : dictionary
        Raster dictionary
    """
    
    # It sets no data values in the bounds
    rst['mtrx'][0,:]=rst['nodt']
    rst['mtrx'][rst['nrows']-1,:]=rst['nodt']
    rst['mtrx'][:,0]=rst['nodt']
    rst['mtrx'][:,rst['ncols']-1]=rst['nodt']

def XYtoij(X,Y,raster):
    """
    Transform X Y coordinates to i j indices of the matrix of a raster

    Parameters
    ----------
    X:float or list of floats
        X coordinate

    Y: float or list of floats
        Y coordinate

    raster: raster object
            Base raster to obtain matrix indices

    Returns
    -------
    i: int
        Row index

    j: int
        Colum index

    """
    i=np.floor(raster['nrows']-((Y-raster['yll'])/raster['clsz'])).astype(int)
    j=(np.floor((X-raster['xll'])/raster['clsz'])).astype(int)
    return i,j       
        
def IJtoxy(i,j,raster):
    """
    Transform X Y coordinates to i j indices

    Parameters
    ----------
    i: int or list of int
        Row index

    j: int or list of int
        Colum index

    raster: raster object
            Base raster to obtain matrix indices

    Returns
    -------
    X:float
        X coordinate

    Y: float
        Y coordinate
    """
    Y=((raster['nrows']-i)*(raster['clsz']))+raster['yll']-raster['clsz']/2
    X=raster['xll']+j*raster['clsz']+raster['clsz']/2
    return X,Y

def SampleRastToRast(rasterA,rasterB):
    """
    Turns values from rasterA into shape and resolution of rasterB

    Parameters
    ----------

    rasterA:
        raster object with data to sample.

    rasterB:
        raster object with desired spatial resolution and domain.

    Returns
    -------

    raster:
        raster object with sampled data on the desired resolution and domain.
    """
    xll=rasterB['xll']
    yll=rasterB['yll']
    clsz=rasterB['clsz']
    nodt=rasterB['nodt']
    mtrx=rasterB['mtrx'] * 0. + nodt
    rasterA['mtrx'][np.where(rasterA['mtrx']==rasterA['nodt'])]=nodt
    iB=np.argwhere(np.isreal(mtrx))[:,0]
    jB=np.argwhere(np.isreal(mtrx))[:,1]
    xB,yB=IJtoxy(iB,jB,rasterB)
    iBA,jBA=XYtoij(xB,yB,rasterA)
    iA=np.argwhere(np.isreal(rasterA['mtrx']))[:,0]
    jA=np.argwhere(np.isreal(rasterA['mtrx']))[:,1]

    corrBA=np.where((iBA>=iA.min())*(iBA<=iA.max())*(jBA>=jA.min())*(jBA<=jA.max()))[0]
    mtrx[iB[corrBA],jB[corrBA]]=rasterA['mtrx'][iBA[corrBA],jBA[corrBA]]

    raster=BuildRaster(xll,yll,clsz,nodt,mtrx)
    return raster

def netcdf2raster(netcdf_dataset,variable,lat_dim,lon_dim,time_dim,time_to_extract=0):
    """
    Gives to a netcdf dataset the format of a raster dictionary for one of its variables
    
    Parameters
    ----------
    
    netcdf_dataset:
        netCDF4 dataset
    
    variable:
        variable to extract from the netcdf_dataset
        
    lat_dim:
        Integer index of the lattitude dimension
        
    lon_dim:
        Integer index of the longitude dimension
        
    time_dim:
        Integer index of the time dimension
        
    time:
        Optional. Position on time axes of the 2D lat-lon matrix to extract
        
    Returns
    -------
    
    raster_dataset
        Dictionary with raster properties (xll, yll, clsz, nodt, mtrx)
        plus times of the third dimension of the matrix in datetime format

    """
    # It reads the georeferenciation properties
    dims = [dim for dim in netcdf_dataset.variables[variable].dimensions]
    xdim = np.array(netcdf_dataset.variables[dims[lon_dim]])
    ydim = np.array(netcdf_dataset.variables[dims[lat_dim]])
    time = netcdf_dataset.variables[dims[time_dim]]
    
    dx = np.average(xdim[1:]-xdim[0:np.size(xdim)-1])
    dy = np.average(ydim[1:]-ydim[0:np.size(ydim)-1])
    
    mtrx=np.array(netcdf_dataset.variables[variable])
    indices=np.where(mtrx>-9999.0)
    eje=[0,0,0]
    eje[time_dim]=0
    eje[lon_dim]=indices[lon_dim]
    eje[lat_dim]=indices[lat_dim]
    mtrx=mtrx[eje[0],eje[1],eje[2]].reshape((ydim.size,xdim.size))
#    mtrx2=np.array(netcdf_dataset.variables[variable])[0,:,:]
    if dx<0.0:
        xdim = xdim[::-1] 
        mtrx = np.fliplr(mtrx)
        dx = -dx
    
    if dy>0.0:
        ydim = ydim[::-1]
        mtrx = np.flipud(mtrx)
        dy = -dy
    
    try:
        times = nc.num2date(time[:], time.units, time.calendar)
    except:
        times = 'no se pudo cargar la variable de tiempos'
    clsz = 0.5*(dx-dy)
    xll = np.min(xdim)-0.5*dx
    yll = np.min(ydim)+0.5*dy
    
    try:
        nodt = netcdf_dataset._FillValue
    except:
        nodt=np.NaN
    
    #- build the Raster dictionary
    raster_dataset=BuildRaster(xll,yll,clsz,nodt,mtrx)
    raster_dataset['times']=times
    ChangeNoData(raster_dataset,-9999.0)

    return raster_dataset