from typing import NamedTuple
from datetime import datetime, date, time
import csv

Vuelo = NamedTuple("Vuelo",     
  [("operador", str), # Compañía aérea que operaba el vuelo (opcional)
   ("codigo", str),   # Código de vuelo (opcional)
   ("ruta", str),     # Ruta del vuelo (opcional)
   ("modelo", str)])  # Modelo de avión que operaba el vuelo (opcional)

Desastre   = NamedTuple("Desastre",     
  [("fecha", date),                 # Fecha del desastre aéreo
    ("hora", time | None),        # Hora del desastre (opcional)  
    ("localizacion", str),        # Localización del desastre
    ("supervivientes",int),       # Supervivientes
    ("fallecidos",int),           # Fallecidos    
    ("fallecidos_en_tierra",int), # Fallecidos en tierra (no eran pasajeros del vuelo)
    ("operacion",str),        # Momento operativo del vuelo cuando ocurrió el desastre   
    ("vuelos", list[Vuelo])]) # Vuelos implicados en el desastre

def lee_desastres(ruta:str)->list[Desastre]:
    res=[]
    with open(ruta, encoding='utf-8') as f:
        lector=csv.reader(f)
        next(lector)
        for fila in lector:
            fecha= parsea_fecha(fila[0])
            hora=parsea_hora(fila[1])
            localización=fila[2]
            supevivientes=int(fila[3])
            fallecidos=int(fila[4])
            fallecidos_en_tierra=int(fila[5])
            operación=fila[6]
            vuelos=parsea_vuelos(fila[7])
            desastre=Desastre(fecha, hora, localización, supevivientes, fallecidos, fallecidos_en_tierra, operación, vuelos)
            res.append(desastre)
    return res

def parsea_fecha(fecha:str) -> date:
    return datetime.strptime(fecha[0], "%d/%m/%Y").date

def parsea_hora(hora:str)->time|None:
    if hora=="":
        return None
    else:
        return datetime.strptime(hora, "%H:%M").time()

def parsea_vuelos(operadores:str, codigos:str, rutas:str,modelos:str) -> list[Vuelo]:
    lista_vuelos = []
    operadores_list = operadores.split('/')   
    codigos_list = codigos.split('/')
    rutas_list = rutas.split('/')
    modelos_list = modelos.split('/')
    for operador, codigo, ruta, modelo in zip(operadores_list, codigos_list, rutas_list, modelos_list):
        vuelo = Vuelo(operador, codigo, ruta, modelo)
        lista_vuelos.append(vuelo)
    return lista_vuelos   


def desastres_con_fallecidos_en_tierra(desastres:list[Desastre],n:int|None=None)->list[tuple[str,date,time,int]]:
    for desastre in desastres:
        


