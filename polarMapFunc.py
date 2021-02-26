#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:33:51 2021

@author: kivimaki
Versio 0.1
Kaikki kommentointi puuttuu
"""

import numpy as np
import Ngl

#----------------------------------------------------------------------
# Based on add_lon_labels from PyNGL example spaghetti.py.
# -- The labels won't fit perfectly when mpCenterLonF is used.
#----------------------------------------------------------------------
# This procedure adds longitude labels to the outside of a circular 
# polar stereographic map. 
#----------------------------------------------------------------------
def add_lon_labels(wks,map,res):
#-- List the longitude values where you want labels.  It's assumed that longitude=0
#-- is at the bottom of the plot, and 180W at the top. You can adjust as necessary.
  lon_values = np.arange(-180,180,30)
  nlon       = lon_values.shape[0]
  lat_values = np.zeros(nlon,'f') + res.mpMinLatF

#-- Get the NDC coordinates of these lat,lon labels. We'll use this information 
#-- to place labels *outside* of the map plot.
  xndc, yndc = Ngl.datatondc(map,lon_values,lat_values)

#-- Set an array of justification strings to use with the "txJust" resource
#-- for each label, based on which quadrant it appears in.
  just_strs  = ["BottomCenter",                 #-- top of plot
                "BottomRight","BottomRight",    #-- upper left quadrant
                "CenterRight",                  #-- left of plot
                "TopRight","TopRight",          #-- lower left quadrant
                "TopCenter",                    #-- bottom of plot
                "TopLeft","TopLeft",            #-- lower right quadrant
                "CenterLeft",                   #-- right of plot
                "BottomLeft","BottomLeft"]      #-- upper right qudrant

#-- Create an array of longitude labels with "W" and "E" added.
  lon_labels = []
  for i in range(nlon):
      if lon_values[i] == -180:
         lon_labels.append("{:g}W ~C~ ".format(abs(lon_values[i]))) #-- move the label upward
      elif lon_values[i] < 0:
         lon_labels.append("{:g}W ".format(abs(lon_values[i])))     #-- add W and move to the left

      elif lon_values[i] > 0:
         lon_labels.append(" {:g}E".format(lon_values[i]))          #-- add E and move to the right
      else:
         lon_labels.append(" ~C~{:g}".format(lon_values[i]))        #-- move label downward

#-- Loop through each label and add it.
  txres = Ngl.Resources()
  txres.txFontHeightF = 0.01
  for i in range(nlon):
    txres.txJust = just_strs[i]
    Ngl.text_ndc(wks,lon_labels[i],xndc[i],yndc[i],txres)

  return


def plotMap(plotName,dat,lon,lat,minLat,colorMap,limits,spacing,title):
    """
    Parameters
    ----------
    plotName :  Tallennettavan kuvan nimi ilman kuvaformaattia, tällä hetkellä png ainut mahdollinen
    dat:        Piirrettävä data 2D numpy mask arrayna
    lon:        Datan lon arvot 1D numpy arrayna
    lat:        Datan lat arvot 1D numpy arrayna
    minLat:     Kuinka alas eteläsuunnassa kartta piirretään
    colorMap:   Käytettävän värikartan nimi
    limits:     Mitkä ovat datan ala- ja ylärajat
    spacing:    Kuinka suurella välillä data piirretään kuvaan
    title:      Kuvan otsikko
    
    -------
    
    Tällä työkalulla pystytään piirtämään ainoastaan ennalta luokiteltua 2D dataa, jonka lat ja lon rajat ovat tiedossa.
    """
    maxLat = 90
    dat,lon = Ngl.add_cyclic(dat,lon)

    wks = Ngl.open_wks('png',plotName)
    Ngl.define_colormap(wks,colorMap)        
    
    # Taustakartan määrittäminen
    mpres                       =  Ngl.Resources()  
    mpres.nglDraw               =  False            #-- don't draw until the end
    mpres.nglFrame              =  False            #-- don't automatically advance frame
    mpres.nglMaximize           =  False            #-- don't maximize the plot, we want to
                                                    #--     use viewport settings
    mpres.vpXF                  =  0.05             #-- viewport x-position
    mpres.vpYF                  =  0.88             #-- viewport y-position
    mpres.vpWidthF              =  0.8              #-- viewport width
    mpres.vpHeightF             =  0.8              #-- viewport height
    
    mpres.mpProjection          = 'Stereographic'   #-- set projection
    mpres.mpEllipticalBoundary  =  True             #-- map projection area is limited to an ellipse 
                                                    #--     inscribed within the normal rectangular 
                                                    #--     perimeter of the viewport
    mpres.mpDataSetName         = 'Earth..4'        #-- change map data set
    mpres.mpDataBaseVersion     = 'MediumRes'       #-- choose higher map resolution
    mpres.mpLimitMode           = 'LatLon'
    mpres.mpMaxLatF             =  maxLat              #-- maximum latitude; northern hemisphere
    mpres.mpMinLatF             =  minLat             #-- minimum latitude
    mpres.mpCenterLatF          =  90.              #-- center latitude
    mpres.pmTickMarkDisplayMode = 'Never'           #-- turn off default ticmkark object, don't draw the box
    
    # Väritetään maa ja vesi
    mpres.mpFillOn              = True   
    mpres.mpFillAreaSpecifiers  = ["water","land"]      # water, land
    mpres.mpSpecifiedFillColors = ['azure','whitesmoke']     
    
    map = Ngl.map(wks,mpres)                        #-- create base map
    add_lon_labels(wks,map,mpres)                   #-- add labels to map       

    # Datan piirtäminen
    res                       =  Ngl.Resources()    #-- plot mods desired
    res.nglDraw               =  False              #-- do not draw until the end
    res.nglFrame              =  False              #-- do not automatically advance frame
    
    res.cnFillOn              =  True               #-- turn contour fill on
    res.cnLinesOn             =  False              #-- turn off contour lines
    res.cnLineLabelsOn        =  False              #-- turn off contour line labels
    res.cnInfoLabelOn         =  False              #-- turn off contour line info label
    res.cnLevelSelectionMode  = "ManualLevels"      #-- define your own contour levels
    res.cnMinLevelValF        =  limits[0] + spacing               #-- minimum contour value
    res.cnMaxLevelValF        =  limits[-1] - spacing           #-- maximum contour value
    res.cnLevelSpacingF       =  spacing               #-- contour increment 
    res.sfXArray              =  lon                #-- use cyclic longitude
    res.sfYArray              =  lat                #-- latitude 
    
    res.lbLabelFontHeightF    =  0.012              #-- set labelbar font size
    res.lbLeftMarginF         =  0.3                #-- move labelbar to the right
    res.pmLabelBarWidthF      =  0.1                #-- width of labelbar
    res.pmLabelBarHeightF     =  mpres.vpHeightF - 0.2 #-- height of labelbar
    
    res.tiMainString          = title  #-- title string
    
    plot = Ngl.contour(wks,dat,res)                   #-- create contour plot
    
    # Piirretään kartta ja data
    Ngl.overlay(map,plot)                           #-- overlay this contour on map
    Ngl.draw(map)                                   #-- draw the map
    Ngl.frame(wks)                                  #-- advance the frame
