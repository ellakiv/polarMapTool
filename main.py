#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:33:48 2021

@author: kivimaki
"""
from netCDF4 import Dataset
import numpy as np
import polarMapFunc

# Datan lukeminen
pf = Dataset('ESACCI-PER_0.25_Cells_2017_EPSG4326.nc')
# Data pitää antaa piirtofunktiolle numpy masked arrayna eli tässä niihin 
# kohtiin missä ei ole dataa laitetaan tieto siitä että ko. dataa ei piirrettä.
# Esimerkkidatalla kaikki arvot <0 maskattiin ei-dataa sisältäväksi.
dat = pf['Band1'][:,:].data                       
dat = np.ma.masked_less(dat, 0)
lat = pf['lat'][:].data                         
lon = pf['lon'][:].data  

# Millä tiedostonimellä kuva tallennetaan
plot_name = 'L4permafrost'            
# Mihin asti kuva piirretään eteläsuunnassa            
minLatitude = 50
# Mitä colormappia käytetään
colorMap = 'BlueYellowRed'
# Millä rajoilla data piirretään.
# Esimerkkidata on prosentteja 0-100% joten tässä asetaan ne ala- ja ylärajaksi 
# ja data jaotellaan 10% väleihin.
dataLimits = [0,100]
dataSpacing = 10
# Kuvan otsikko
title = 'CCI L4 Permafrost'

polarMapFunc.plotMap(plot_name,dat,lon,lat,minLatitude,colorMap,dataLimits,dataSpacing,title)