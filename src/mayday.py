from typing import NamedTuple
from datetime import datetime, date, time
from collections import defaultdict
import csv

Vuelo = NamedTuple(
    "Vuelo",
    [
        ("operador", str),  # Compañía aérea que operaba el vuelo (opcional)
        ("codigo", str),    # Código de vuelo (opcional)
        ("ruta", str),      # Ruta del vuelo (opcional)
        ("modelo", str),    # Modelo de avión que operaba el vuelo (opcional)
    ],
)

Desastre = NamedTuple(
    "Desastre",
    [
        ("fecha", date),                 # Fecha del desastre aéreo
        ("hora", time | None),           # Hora del desastre (opcional)
        ("localizacion", str),           # Localización del desastre
        ("supervivientes", int),         # Supervivientes
        ("fallecidos", int),             # Fallecidos
        ("fallecidos_en_tierra", int),   # Fallecidos en tierra
        ("operacion", str),              # Momento operativo del vuelo
        ("vuelos", list[Vuelo]),         # Vuelos implicados
    ],
)


def lee_desastres(ruta: str) -> list[Desastre]:
    res: list[Desastre] = []
    with open(ruta, encoding="utf-8", newline="") as f:
        lector = csv.reader(f, delimiter=";")
        next(lector, None)  # saltar cabecera

        for fila in lector:
            # Columnas según enunciado:
            # 0 Date, 1 Time, 2 Location, 3 Operator, 4 Flight, 5 Route, 6 Type,
            # 7 Survivors, 8 Fatalities, 9 Ground, 10 Operation
            fecha = parsea_fecha(fila[0])
            hora = parsea_hora(fila[1])
            localizacion = fila[2].strip()

            operadores = fila[3]
            codigos = fila[4]
            rutas = fila[5]
            modelos = fila[6]
            vuelos = parsea_vuelos(operadores, codigos, rutas, modelos)

            supervivientes = int(fila[7]) if fila[7].strip() != "" else 0
            fallecidos = int(fila[8]) if fila[8].strip() != "" else 0
            fallecidos_en_tierra = int(fila[9]) if fila[9].strip() != "" else 0
            operacion = fila[10].strip()

            res.append(
                Desastre(
                    fecha,
                    hora,
                    localizacion,
                    supervivientes,
                    fallecidos,
                    fallecidos_en_tierra,
                    operacion,
                    vuelos,
                )
            )

    return res


def parsea_fecha(fecha: str) -> date:
    # Ej: "27/03/1977"
    return datetime.strptime(fecha.strip(), "%d/%m/%Y").date()


def parsea_hora(hora: str) -> time | None:
    # Ej: "17:07" o vacío
    h = hora.strip()
    if h == "":
        return None
    return datetime.strptime(h, "%H:%M").time()


def parsea_vuelos(operadores: str, codigos: str, rutas: str, modelos: str) -> list[Vuelo]:
    """
    Cada uno de estos campos puede contener varios valores separados por "/".
    Creamos un Vuelo por cada bloque, haciendo strip() para quitar espacios.
    """
    ops = [x.strip() for x in operadores.split("/")]
    codos = [x.strip() for x in codigos.split("/")]
    rts = [x.strip() for x in rutas.split("/")]
    mods = [x.strip() for x in modelos.split("/")]

    # Por si hubiese longitudes distintas (raro, pero así no revienta):
    n = min(len(ops), len(codos), len(rts), len(mods))

    return [Vuelo(ops[i], codos[i], rts[i], mods[i]) for i in range(n)]

def desastres_con_fallecidos_en_tierra(desastres: list[Desastre], n: int | None = None) -> list[tuple[str, date, time, int]]:
    lista = []
    for d in desastres:
        if d.fallecidos_en_tierra > 0:
            t = (d.localizacion, d.fecha, d.hora, d.fallecidos_en_tierra)
            lista.append(t)

    lista.sort(key=lambda t: t[3], reverse=True)

    if n is None:
        return lista
    else:
        return lista[:n]

def decada_mas_colisiones(desastres:list[Desastre]) -> tuple[int,int]: 
    conteo = defaultdict(int)
    for d in desastres:
        if len(d.vuelos)>=2:
            decada = (d.fecha.year//10)*10
            conteo[decada]+=1
    return max (conteo.items(), key= lambda par: par[1])

def mayor_periodo_sin_desastres(desastres:list[Desastre], operacion:str|None=None)-> tuple[date, date, int]:
    if operacion is not None:
        desastres = [d for d in desastres if d.operacion==operacion]
    desastres = sorted(desastres, key=lambda d: d.fecha)
    fecha1: date | None = None
    fecha2: date | None = None
    mejor_fecha1: date | None = None
    mejor_fecha2: date | None = None
    dias_sin_desastres=0
    for d in desastres:
        if fecha1 == None and fecha2 == None:
            fecha1 = d.fecha
            fecha2 = d.fecha
        else:
            fecha1 = fecha2
            fecha2 = d.fecha
            dias_entre_desastres = (fecha2-fecha1).days
            if dias_entre_desastres>dias_sin_desastres:
                dias_sin_desastres=dias_entre_desastres
                mejor_fecha1=fecha1
                mejor_fecha2=fecha2
    return (mejor_fecha1, mejor_fecha2, dias_sin_desastres)

def estadisticas_por_operacion(desastres: list[Desastre], limite_tasa_supervivencia:float|None=None)->dict[str,tuple[int,float,float]]:
    diccionario = defaultdict(lambda: [0, 0, 0])
    for d in desastres:
        pasajeros = d.supervivientes + d.fallecidos  # NO cuenta fallecidos_en_tierra
        tasa = d.fallecidos / pasajeros  # tasa de supervivencia según el enunciado
        if limite_tasa_supervivencia is None or tasa <= limite_tasa_supervivencia:
            diccionario[d.operacion][0] += 1
            diccionario[d.operacion][1] += d.supervivientes
            diccionario[d.operacion][2] += d.fallecidos

    # convertir acumulados a (count, media_sup, media_fall)
    res: dict[str, tuple[int, float, float]] = {}
    for operacion, (count, sum_sup, sum_fall) in diccionario.items():
        res[operacion] = (count, sum_sup / count, sum_fall / count)
    return res
