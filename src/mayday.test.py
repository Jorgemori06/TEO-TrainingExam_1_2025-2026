from mayday import *

# Evita el warning de \M en Windows:
ruta = r"data\Mayday.csv"

def funcionPrincipal():
    desastres = lee_desastres(ruta)
    #print("Se han leído:", len(desastres))
    #print("Los dos primeros son:")
    #print(desastres[0])
    #print(desastres[1])
    #print(desastres_con_fallecidos_en_tierra(desastres, 5))
    #print("La década con más colisiones fue ", decada_mas_colisiones(desastres))
    #f1, f2, dias = mayor_periodo_sin_desastres(desastres)
    #print(f"El mayor periodo sin desastres comienza el {f1}, termina el {f2} y dura {dias} días.")
    #f1, f2, dias = mayor_periodo_sin_desastres(desastres, "Taking-off")
    #print(f"El mayor periodo sin desastres durante la operación Taking-off comienza el {f1}, termina el {f2} y dura {dias} días.")
    #f1, f2, dias = mayor_periodo_sin_desastres(desastres, "Landing")
    #print(f"El mayor periodo sin desastres durante la operación Landing comienza el {f1}, termina el {f2} y dura {dias} días.")
    #print("Las estadísticas por operación son: ", estadisticas_por_operacion(desastres))
    #print(" Las estadísticas por operación con tasa de supervivencia menor a 0.15 son:", estadisticas_por_operacion(desastres, 0.15))


if __name__ == "__main__":
    funcionPrincipal()
