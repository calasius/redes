import networkx as nx

def crear_grafo(fuente, contadores):
    etiquetas = {}
    W = nx.Graph()
    #W.size(True)
    for paquete in fuente:
        agregar_paquete(W, paquete, etiquetas, contadores)
    return W, etiquetas

def agregar_paquete(grafo, paquete, etiquetas, contadores):
    origen = paquete.psrc
    destino = paquete.pdst
    cantNodos = 0
    if (contadores[destino]>5):
        if (not grafo.has_node(origen)):
            grafo.add_node(origen)
            etiquetas[origen]=origen
            cantNodos = cantNodos + 1
        if (not grafo.has_node(destino)):
            grafo.add_node(destino)
            etiquetas[destino]=destino
            cantNodos = cantNodos + 1
        grafo.add_edge(origen, destino)
    
    return grafo