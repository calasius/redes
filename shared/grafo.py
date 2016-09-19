import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import sys
sys.path.append('../shared/')
from fuente import *

# en cantidadMinimaInteracciones pasamos la cantidad minima 
# de interacciones que tiene que tener el nodo para ser graficado
def crear_grafo_cmin(paquetes, cMinIntNodo=0, maxPerNode=15):
    
    grafo = nx.DiGraph()
   
    fuente, who_has_packages = calcularFuenteS2(paquetes)
    contadores = fuente.value_counts()
    etiquetas={}
    counterPerNodeIn = {}
    counterPerNodeOut = {}
    cantidadSimbolos = len(contadores)
    if cantidadSimbolos > 70 :
        cMinIntNodo = 5

    for paquete in who_has_packages:
        agregar_paquete(grafo, paquete, etiquetas, contadores, cMinIntNodo, counterPerNodeIn, counterPerNodeOut, maxPerNode)
    max_value = contadores.get_values().max()
    min_value = (contadores.get_values().min() / float(max_value))*700
    node_sizes = [(contadores[node] / float(max_value))*700 if node in contadores else min_value for node in grafo.nodes()]
    plt.figure(figsize=(12,12)) 

    pos=nx.spring_layout(grafo)
    nx.draw_networkx_labels(grafo,pos,etiquetas,node_size=60,font_size=8, font_color="g")
    nx.draw(grafo,pos,node_size=node_sizes,font_size=8)

    #mostramos los pesos de las aristas
    labels = nx.get_edge_attributes(grafo,'weight')
    nx.draw_networkx_edge_labels(grafo,pos,edge_labels=labels)
    
    pylab.show()
    return grafo

def crear_grafo(paquetes):
    return crear_grafo_cmin(paquetes, 0)

def agregar_paquete(grafo, paquete, etiquetas, contadores, cMinIntNodo, counterPerNodeIn, counterPerNodeOut, maxPerNode):
    origen = paquete.psrc
    destino = paquete.pdst
    cantNodos = 0
    
    if (contadores[destino]>=cMinIntNodo):
        
        if (origen not in counterPerNodeOut):
            counterPerNodeOut[origen] = 0
        if(destino not in counterPerNodeIn):
            counterPerNodeIn[destino] = 0
        if (counterPerNodeIn[destino] <= maxPerNode and counterPerNodeOut[origen] <= maxPerNode):        
            if (not grafo.has_node(origen)):
                grafo.add_node(origen)
                etiquetas[origen]=origen
                cantNodos = cantNodos + 1

            if (not grafo.has_node(destino)):
                grafo.add_node(destino)
                etiquetas[destino]=destino
                cantNodos = cantNodos + 1
            counterPerNodeIn[destino] += 1
            counterPerNodeOut[origen] += 1
            grafo.add_edge(origen, destino)
            
    return grafo