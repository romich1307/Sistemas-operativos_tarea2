import time
import threading
import multiprocessing
import statistics
import os
import platform
from datetime import datetime
# ============================================================
# PARTE A
# ============================================================

def suma_cuadrados(inicio, fin):
    suma = 0

    for i in range(inicio, fin):
        suma += i * i

    return suma

def tarea_io(segundos):
    time.sleep(segundos)
    
# ============================================================
# PRUEBAS DE CPU
# ============================================================

def cpu_secuencial(n):
    mitad = n // 2

    suma_cuadrados(0, mitad)
    suma_cuadrados(mitad, n)
    
def cpu_threads(n):
    mitad = n // 2

    t1 = threading.Thread(
        target=suma_cuadrados,
        args=(0, mitad)
    )

    t2 = threading.Thread(
        target=suma_cuadrados,
        args=(mitad, n)
    )

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
def cpu_procesos(n):
    mitad = n // 2

    p1 = multiprocessing.Process(
        target=suma_cuadrados,
        args=(0, mitad)
    )

    p2 = multiprocessing.Process(
        target=suma_cuadrados,
        args=(mitad, n)
    )

    p1.start()
    p2.start()

    p1.join()
    p2.join()
    
# ============================================================
# PRUEBAS DE E/S
# ============================================================

def io_secuencial(segundos):
    tarea_io(segundos)
    tarea_io(segundos)
    
def io_threads(segundos):
    t1 = threading.Thread(
        target=tarea_io,
        args=(segundos,)
    )

    t2 = threading.Thread(
        target=tarea_io,
        args=(segundos,)
    )

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
def io_procesos(segundos):
    p1 = multiprocessing.Process(
        target=tarea_io,
        args=(segundos,)
    )

    p2 = multiprocessing.Process(
        target=tarea_io,
        args=(segundos,)
    )

    p1.start()
    p2.start()

    p1.join()
    p2.join()
    
# ============================================================
# MEDICIÓN
# ============================================================

def medir(nombre, funcion, argumento):
    tiempos = []

    print(f"\n--- {nombre} ---")

    for repeticion in range(5):

        inicio = time.perf_counter()

        funcion(argumento)

        fin = time.perf_counter()

        tiempo = fin - inicio
        tiempos.append(tiempo)

        print(
            f"Repetición {repeticion + 1}: "
            f"{tiempo:.6f} segundos"
        )

    mediana = statistics.median(tiempos)

    print(f"Mediana: {mediana:.6f} segundos")

    return tiempos, mediana