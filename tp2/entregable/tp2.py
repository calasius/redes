from __future__ import print_function, unicode_literals, with_statement
import math
from scapy.all import *
import numpy as np
import time
import pandas as pd
from scipy.stats import t
from math import sqrt
from math import pow
import requests
import os
import matplotlib.patches as mpatches
import argparse
import contextlib
import requests
import sys
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pygeoip

IP_SERVICE_URL = 'https://freegeoip.net/json/{}'

DEFAULT_RTT_VALUE = 0

ATTEMPS = 30


def get_ip(ip_file):
    """
    Returns a list of IP addresses from a file containing one IP per line.
    """
    with contextlib.closing(ip_file):
        return [line.strip() for line in ip_file]


def get_lat_lon(ip_list=[], lats=[], lons=[]):
    """
    This function connects to the FreeGeoIP web service to get info from
    a list of IP addresses.
    Returns two lists (latitude and longitude).
    """
    for ip in ip_list:
        r = requests.get("https://freegeoip.net/json/" + ip)
        json_response = r.json()
        if json_response['latitude'] and json_response['longitude']:
            print ("ip = {} lat = {} long = {}".format(ip, json_response['latitude'],json_response['longitude']))
            lats.append(json_response['latitude'])
            lons.append(json_response['longitude'])
    return lats, lons


def geoip_lat_lon(gi, ip_list):
    """
    This function uses the MaxMind library and databases to geolocate IP addresses
    Returns two lists (latitude and longitude).
    """
    lats=[]
    lons=[]
    for ip in ip_list:
        try:
            r = gi.record_by_addr(ip)
        except Exception:
            print("Unable to locate IP: %s" % ip)
            continue
        if r is not None:
            lats.append(r['latitude'])
            lons.append(r['longitude'])
    return lats, lons


def get_lat_lon_from_csv(csv_file, lats=[], lons=[]):
    """
    Retrieves the last two rows of a CSV formatted file to use as latitude
    and longitude.
    Returns two lists (latitudes and longitudes).
    Example CSV file:
    119.80.39.54, Beijing, China, 39.9289, 116.3883
    101.44.1.135, Shanghai, China, 31.0456, 121.3997
    219.144.17.74, Xian, China, 34.2583, 108.9286
    64.27.26.7, Los Angeles, United States, 34.053, -118.2642
    """
    with contextlib.closing(csv_file):
        reader = csv.reader(csv_file)
        for row in reader:
            lats.append(row[-2])
            lons.append(row[-1])

    return lats, lons


def generate_map(output, lats=[], lons=[], wesn=None):
    """
    Using Basemap and the matplotlib toolkit, this function generates a map and
    puts a red dot at the location of every IP addresses found in the list.
    The map is then saved in the file specified in `output`.
    """
    
    plt.close('all')
    print("Generating map and saving it to {}".format(output))
    if wesn:
        wesn = [float(i) for i in wesn.split('/')]
        m = Basemap(projection='cyl', resolution='l',
                llcrnrlon=wesn[0], llcrnrlat=wesn[2],
                urcrnrlon=wesn[1], urcrnrlat=wesn[3])
    else:
        m = Basemap(projection='cyl', resolution='l')
    m.bluemarble()

    x, y = m(lons, lats)
    
    m.plot(x, y, 40, 40, color='y')
    m.scatter(x, y, s=3, color='#ff0000', marker='o', alpha=0.3) #, alpha=0.3
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close('all')

def graficar_ruta(ruta, nombre_imagen):
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    lats, lons = geoip_lat_lon(gi,ruta)
    generate_map(nombre_imagen, lats, lons) #, wesn='-12/45/30/65'
    
    
def toLatex(df):
    from IPython.display import Latex
    return Latex(df.to_latex(sparsify=False))

def ipCountryCode(ip):    
    resp = requests.get(IP_SERVICE_URL.format(ip))
    if resp.status_code != 200:
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    return resp.json()['country_code']

def modified_thompson(n):
    alpha = 0.025
    t_critical = t.ppf(1-alpha, n-2)
    return (t_critical*(n-1)) / (sqrt(n) * sqrt(n-2 + pow(t_critical,2)))  

def enviar_paquete(host, time_to_live):
    packet = IP(dst=host, ttl=time_to_live) / ICMP()
    res = sr(packet, timeout=1, verbose=0)
    return res[0][ICMP]

def route(df):
    return df[df['ip'] != 'empty']['ip'].unique()

def calculateOutliers(rtt_df):
    descriptions = rtt_df.describe().T
    mean = descriptions['mean']
    std = descriptions['std']
    zrtt = (rtt_df-mean)/std
    n = len(zrtt)
    thomson_value = modified_thompson(n)
    abszrtt = abs(zrtt)
    return abszrtt[abszrtt['rtt'] > thomson_value], zrtt, thomson_value

def graficarThompsonHistogram(zrtt_df,thompson_value, host):
    v = zrtt_df.plot(kind='hist', bins=30, title=host)
    l = v.axvline(x=thompson_value, linewidth=4, color='r')
    lines, labels = v.get_legend_handles_labels()
    labels.append('Thomson')
    v.legend(['Thompson', 'zrtt'])
    plt.savefig("zrtt-"+host+'.png', dpi=300, bbox_inches='tight')
    
def graficarRttHistogram(rtt_df, host):
    v = rtt_df.plot(kind='hist', bins=30, title=host)
    plt.savefig("rtt-"+host+'.png', dpi=300, bbox_inches='tight')

def getIpAddress(host):
    import socket
    addr = socket.gethostbyname(host)
    return addr

def trace_route(host):
    ips_countrycode = {}
    hops = []
    ttl_without_response = []
    ip = getIpAddress(host)
    for i in range(0,ATTEMPS):
        tipo = 11
        ttl = 1
        last_rtt = 0
        while (tipo!=0 and ttl < 30):
            if (not ttl in ttl_without_response):
                ti = time.time()
                res1 = enviar_paquete(ip, ttl)
                tf = time.time()
                rtt = tf-ti
                if (len(res1) > 0):
                    tipo = res1[0][1].type
                    src = res1[0][1].src
                    countryCode = None
                    if(src in ips_countrycode):
                        countryCode = ips_countrycode[src]
                    else:
                        countryCode = ipCountryCode(src)
                        ips_countrycode[src] = countryCode
                    if (tipo > 0):
                        hops.append([host,ttl,i,src,countryCode, max(0,rtt-last_rtt)])
                    else:
                        hops.append([host,ttl,i,src,countryCode, max(0,rtt-last_rtt)])
                    last_rtt = rtt
                else:
                    hops.append([host,ttl,i,"empty","empty",DEFAULT_RTT_VALUE])
                    ttl_without_response.append(ttl)
            ttl = ttl + 1

    df = pd.DataFrame(hops,columns=['host','ttl','i','ip','cc','rtt'])
    indexed = df.set_index(['host','ttl','i','ip','cc'])
    rtt_df = indexed.groupby(level=['host','ttl','ip','cc']).mean()
    
    outliers_df, zrtt_df, thompson_value = calculateOutliers(rtt_df)
    
    print ("Grafico mapa")
    graficar_ruta(route(df),'route[{}].png'.format(host))
    
    print ("Grafico RTT Histogram")
    graficarRttHistogram(rtt_df, host)
    
    print ("Grafico ZRTT Histogram")
    graficarThompsonHistogram(zrtt_df,thompson_value, host)
    
    print ("rtt df")
    print (rtt_df)
    
    print ("Outliers df")
    print (outliers_df)

host = sys.argv[1]
print ("Traceroute for " +  host)
trace_route(host)






