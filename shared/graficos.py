import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
sys.path.append('../shared/')
from fuente import *

def agrupar_valores(fuente):
    infoSimb = informacion_simbolos(fuente)
    return set(infoSimb.get_values())

def graficar_histograma(titulo, etiquetaY, etiquetasBarras, tamanosBarras):
    #configuracion de colores
    colorBarras = '#3D7DAA' #34627C'
    colorBordeBarras = '#1E4150'#'#3C7DAA'
    colorFondo = '#E6E6E6'    
    colorFuente = '#222020'

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    #configuracion de la grilla y el fondo
    ax.grid(zorder=0)
    ax.grid(True)
    plt.grid(b=True, which='both', color='w',linestyle='-', linewidth=1)
    ax.set_axis_bgcolor(colorFondo) 
    ax.spines['bottom'].set_color('w')
    ax.spines['top'].set_color('w')
    ax.spines['left'].set_color('w')
    ax.spines['right'].set_color('w')

    #tamanosBarras = agrupar_valores(tamanosBarras)

    ind = np.arange(len(tamanosBarras)) # las posiciones x de las barras tamanosBarras.size
    anchoBarra = 0.35                         # ancho de las barras

    rects1 = ax.bar(ind, tamanosBarras, anchoBarra, color=colorBarras, edgecolor=colorBordeBarras, zorder=3)

    # ejes y etiquetas
    ax.set_xlim(-anchoBarra,len(ind)+anchoBarra)
    ax.set_ylim(0, max(tamanosBarras)+1)
    #ax.set_xlim(0, 100)

    ax.set_ylabel(etiquetaY)
    ax.set_title(titulo)
    xTickMarks = etiquetasBarras
    
    ax.set_xticks(ind+anchoBarra)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=0, fontsize=10, weight='bold', color=colorFuente)
    
    
    return ax.get_figure()

def graficar_comparacion_simbolos_fuente(titulo, etiquetaY, etiquetasBarras, entropia, entropiaMaxima, tamanosBarras):    
    fig = graficar_histograma(titulo, etiquetaY, etiquetasBarras, tamanosBarras)

    colorEntropia = '#BF111D'    
    plt.axhline(entropia, color=colorEntropia, linestyle='-', linewidth=2, zorder=4)

    colorEntropiaMaxima = 'g'    
    plt.axhline(entropiaMaxima, color=colorEntropiaMaxima, linestyle='-', linewidth=2, zorder=5)

    red_patch = mpatches.Patch(color=colorEntropia, label='Entropia')
    green_patch = mpatches.Patch(color=colorEntropiaMaxima, label='Entropia maxima')
    plt.legend(handles=[red_patch, green_patch])
    fig.savefig("gr.png", figsize=(1200,1200),  dpi=200)
    plt.show()

def graficar_comparacion_simbolos_entropia(fuente, titulo):   
    etiquetaY ="Informacion"
    etiquetasBarras = ["UNICAST", "BROADCAST"]    
    graficar_comparacion_simbolos_fuente(titulo, etiquetaY, etiquetasBarras, entropia_fuente(fuente), entropia_maxima_fuente(fuente), informacion_simbolos(fuente))

def graficar_comparacion_simbolos_entropia_agrupados(fuente, titulo):   
    etiquetaY ="Informacion"
    etiquetasBarras = []    
    
    tamanosBarrasAgrupados = set(informacion_simbolos(fuente).values)
    graficar_comparacion_simbolos_fuente(titulo, etiquetaY, etiquetasBarras, entropia_fuente(fuente), entropia_maxima_fuente(fuente), tamanosBarrasAgrupados)
