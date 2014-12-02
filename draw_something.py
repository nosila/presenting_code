import os
import numpy as np

from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import pysal
import pylab as pl
import shapely
import shapely.geometry
from shapely.geometry import shape
from shapely.geometry import Point, LineString, Polygon, MultiPolygon 
from shapely.wkt import dumps, loads


import random
#grab a random color for coloring a figure
def get_random_color():
    r = lambda: random.randint(0,255)
    return('#%02X%02X%02X' % (r(),r(),r()))

#initialize the figure and draw the shape
def plot(shapelyGeometries, color_dict={"fill":"#AADDCC", "line":"#666666","hole_fill":"#ffffff", "hole_line":"#999999" }):
    'Plot shapelyGeometries'
    figure = pl.figure(num=None, figsize=(10, 10), dpi=180)
    axes = pl.axes()
    axes.set_aspect('equal', 'datalim')
    axes.xaxis.set_visible(False)
    axes.yaxis.set_visible(False)
    
    draw(shapelyGeometries, color_dict)
            
#Check the type and break up multipolygons        
def draw(gs, color_dict):
    'Draw shapelyGeometries'
    # Handle single and lists of geometries
    try:
        gs = iter(gs)
    except TypeError:
        gs = [gs]
    #Route polygons and multipolygons to the right place
    for g in gs:
        gType = g.geom_type
        if gType.startswith('Multi') or gType == 'GeometryCollection':
            draw(g.geoms, color_dict)
        else:
            draw_(g, color_dict)

#Break the shape into its interior and exterior rings            
def draw_(g, color_dict):

    'Draw a shapelyGeometry; thanks to Sean Gilles'
    gType = g.geom_type
    if gType == 'Point':
        pl.plot(g.x, g.y, 'k,')
    elif gType == 'LineString':
        x, y = g.xy
        pl.plot(x, y, 'b-', color=color_dict["line"])
    elif gType == 'Polygon':
        #can draw parts as multiple colors
        if not color_dict:
            color_dict={"fill":get_random_color(), 
                        "line":"#666666",
                        "hole_fill":"#FFFFFF", 
                        "hole_line":"#999999" }
    
    
        x, y = g.exterior.xy
        pl.fill(x, y, color=color_dict["fill"], aa=True) 
        pl.plot(x, y, color=color_dict["line"], aa=True, lw=1.0)
        for hole in g.interiors:
            x, y = hole.xy
            pl.fill(x, y, color=color_dict["hole_fill"], aa=True) 
            pl.plot(x, y, color=color_dict["hole_line"], aa=True, lw=1.0)
            
