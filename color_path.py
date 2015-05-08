# -*- coding: utf-8 -*-

import numpy as np 
import networkx as nx #library dealing with graphs
import struct
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from pandas import read_excel, read_csv #library to deal with files

from core.models import Pathway 

path = Pathway.objects.get(name="Wnt_Pathway") # Here I take pathway from OF database but it can be taken from file

filename = "nodes/Wnt_nodes_act.csv" #your nodes file
        
df_my_nodes = read_excel("nodes/Wnt_Pathway.xlsx", sheetname="nodes" ) # create dataframe from pathway file
nodes = list(df_my_nodes.columns.values) # take all the nodes in right sequence 
       
        
df_nicolay_nodes = read_csv(filename, delimiter='\t', index_col=0 ) #create dataframe from file
df_nicolay_nodes['nodes'] = nodes #convert nodes numbers to nodes names
df_nicolay_nodes = df_nicolay_nodes.set_index('nodes') # make it index column
        
def colormap(col): # main function for coloring the pathway
            
    G=nx.DiGraph() #create directed grapth
    positive = col[col>=0] # divide values into positive and negative
    negative = col[col<0]
            
    # NEGATIVE
    cmap =  plt.get_cmap('Blues') # setting color
            
    cNormp  = colors.Normalize(vmin=np.min(negative)-1, vmax=0) #normalise values to get color for each value
    scalarMap = cmx.ScalarMappable(norm=cNormp, cmap=cmap) #get the value-color mapping
             
            
    for node, value in negative.iteritems(): #color each node
        ffil = "#"+struct.pack('BBB',*scalarMap.to_rgba(value, bytes=True)[:3]).encode('hex').upper() #convert RGBA to HEX color format
        G.add_node(node, color='black',style='filled',
                           fillcolor=ffil) #adding node to the graph
                
    # POSITIVE
    cmap = plt.get_cmap('Reds')
            
    cNormp  = colors.Normalize(vmin=0, vmax=np.max(positive))
    scalarMap = cmx.ScalarMappable(norm=cNormp, cmap=cmap)       
  
            
    for node, value in positive.iteritems():
        ffil = "#"+struct.pack('BBB',*scalarMap.to_rgba(value, bytes=True)[:3]).encode('hex').upper()
        G.add_node(node, color='black',style='filled',
                           fillcolor=ffil)
            
    for node in path.node_set.all(): #creating edges. You can take this from pathway file
        for inrel in node.inrelations.all():
            if inrel.reltype == '1':
                relColor = 'green'
            if inrel.reltype == '0':
                relColor = 'red'
            G.add_edge(inrel.fromnode.name.encode('ascii','ignore'), inrel.tonode.name.encode('ascii','ignore'), color=relColor)
             
    

    A=nx.to_agraph(G) # convert networkx grapth into graphviz. You have to install graphviz library!
    A.layout(prog='dot') # method to place nodes on the canvas
    A.draw('nicolay/'+path.name+'/'+path.name+'_'+col.name+'.png') #saving picture to the file
            
            
df_nicolay_nodes.apply(colormap, axis=0) # apply drawing function to each row of dataframe