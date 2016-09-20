import sys
sys.path.append('../shared/')
from reader import *
from graficos import *
from grafo import *
from fuente import *
import getopt

argv = sys.argv[1:]

try:
	opts, args = getopt.getopt(argv,"",["offline=","online="])
except getopt.GetoptError:
        print ('tp1.py --offline <input pcap file>')
        print ('sudo tp1.py --online <output pcap file>')
        sys.exit(2)

if (len(opts) == 0):
        print ('tp1.py --offline <input pcap file>')
        print ('sudo tp1.py --online <output pcap file>')
        sys.exit(2)

sniff_timeout = 10
packages = None

for opt, arg in opts:
        if opt == '-h':
            print ('tp1.py --offline <input pcap file>')
            print ('sudo tp1.py --online <output pcap file>')
            sys.exit()
        elif opt in ("--offline"):
            inputfile = arg
            packages = readPackagesOffline(inputfile)
        elif opt in ("--online"):
            outputfile = arg
            packages = readPackagesOnline(sniff_timeout,outputfile)

#Analisis fuente S
fuente_s = calcularFuenteS(packages)

contadores_s = fuente_s.value_counts()
print ("Cantidad de simbolos S")
print (contadores_s.iloc[:10], "\n")

entropia_s = entropia_fuente(fuente_s)
print ("Entropia Fuente S = ", entropia_s, "\n")

entropia_max_s = entropia_maxima_fuente(fuente_s)
print ("Entropia maxima S = ", entropia_max_s, "\n")

informacion_s = informacion_simbolos(fuente_s)
print ("Informacion simbolos S")
print (informacion_s, "\n")

titulo = "Comparacion entropias y informacion de simbolos de S"
graficar_comparacion_simbolos_entropia(fuente_s, titulo)

#Analisis fuente S1
fuente_s1, who_has_packages = calcularFuenteS1(packages)

contadores_s1 = fuente_s1.value_counts()

print ("Cantidad de simbolos S1")
print (contadores_s1, "\n")

entropia_s1 = entropia_fuente(fuente_s1)
print ("Entropia Fuente S1 = ", entropia_s1, "\n")

entropia_max_s1 = entropia_maxima_fuente(fuente_s1)
print ("Entropia maxima S1 = ", entropia_max_s1, "\n")

informacion_s1 = informacion_simbolos(fuente_s1)
print ("Informacion simbolos S1")
print (informacion_s1, "\n")

titulo = "Comparacion entropias y informacion de simbolos de S1"
graficar_comparacion_simbolos_entropia_agrupados(fuente_s1, titulo)
print ("Nodos distinguidos")
print (nodos_distinguidos(fuente_s1), "\n")

A = crear_grafo_cmin(packages)
print ("Cantidad de Nodos: ", A.number_of_nodes())
print ("Cantidad de Enlaces: ", A.number_of_edges())
