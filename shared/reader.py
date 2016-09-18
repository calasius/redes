import scapy.all as sc
import numpy as np
import pandas as pd
from scipy.stats import entropy

def readPackagesOnline(timeout_en_segundos, fileName):
    packages = sc.sniff(timeout=timeout_en_segundos)
    #filtered = filter(lambda p : p.dst != '00:00:00:00:00:00' and p.src != '00:00:00:00:00:00', packages)
    sc.wrpcap(fileName,filtered)
    return packages


def readPackagesOffline(file):
    #Leo solo los paquetes ethernet
    packages = sc.sniff(offline=file,filter="ether")
    #Filtro los paquetes que ARP gratuitos
    #filtered = filter(lambda p : p.dst != '00:00:00:00:00:00' and p.src != '00:00:00:00:00:00', packages)
    return packages
