import numpy as np
import pandas as pd
from scipy.stats import entropy
import scapy.all as sc

ARP_OP_WHO_HAS = 1
ARP_OP_IS_AT = 2

def simbolo_s(package):
    if package.dst == 'ff:ff:ff:ff:ff:ff':
        return "BROADCAST"
    else:
        return "UNICAST"
       
       
def entropia_fuente(fuente):
    counts = fuente.value_counts()
    return entropy(base=2,pk=counts.as_matrix())

def entropia_maxima_fuente(fuente):
    counts = fuente.value_counts()
    p = 1 / float(counts.size)
    return - np.log2(p)

def nodos_distinguidos(fuente):
    entropia = entropia_fuente(fuente)
    info = informacion_simbolos(fuente)
    info2 = info[info < entropia]
    return info2

def informacion_simbolos(fuente):
    counts = fuente.value_counts()
    total = counts.sum()
    probs = counts / float(total)
    return pd.Series(- np.log2(probs), index=counts.index)

def simbolo_s2(package):
    return package.pdst

def calcularFuenteS1(packages):
    fuente_s1 = pd.Series([simbolo_s(p) for p in packages])
    return fuente_s1

def calcularFuenteS2(packages):
    who_has_packages = filter(lambda p : p.haslayer(sc.ARP) and p["ARP"].op == ARP_OP_WHO_HAS,packages)
    fuente_s2 = pd.Series([simbolo_s2(p) for p in who_has_packages])
    return fuente_s2, who_has_packages

