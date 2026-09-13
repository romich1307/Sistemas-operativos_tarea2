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