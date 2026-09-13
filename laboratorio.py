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

def guardar_resultados(resultados, n, io_wait):

    with open("resultados.txt", "w", encoding="utf-8") as archivo:

        archivo.write("RESULTADOS DEL LABORATORIO\n")
        archivo.write("=" * 50 + "\n\n")

        archivo.write("PLATAFORMA\n")

        archivo.write(
            f"Sistema operativo: "
            f"{platform.system()} {platform.release()}\n"
        )

        archivo.write(
            f"Procesador: "
            f"{platform.processor() or 'No identificado'}\n"
        )

        archivo.write(
            f"Núcleos lógicos: {os.cpu_count()}\n"
        )

        archivo.write(
            f"Versión de Python: "
            f"{platform.python_version()}\n"
        )

        archivo.write(
            f"Carga CPU (N): {n}\n"
        )

        archivo.write(
            f"Espera E/S por tarea: {io_wait} s\n"
        )

        archivo.write(
            "Repeticiones por prueba: 5\n\n"
        )

        archivo.write("MEDIANAS\n")
        archivo.write("-" * 50 + "\n")

        for nombre, (_, mediana) in resultados.items():
            archivo.write(
                f"{nombre}: {mediana:.6f} s\n"
            )

        archivo.write("\nMEDICIONES COMPLETAS\n")
        archivo.write("-" * 50 + "\n")

        for nombre, (tiempos, mediana) in resultados.items():

            archivo.write(f"\n{nombre}\n")

            for i, tiempo in enumerate(tiempos, start=1):

                archivo.write(
                    f"  Repetición {i}: "
                    f"{tiempo:.6f} s\n"
                )

            archivo.write(
                f"  Mediana: {mediana:.6f} s\n"
            )

    print("\nResultados guardados en resultados.txt")
    
# ============================================================
# PARTE B - SUPERVISOR
# ============================================================

def tarea_hija(numero):

    print(
        f"Hijo {numero} iniciado | "
        f"PID={os.getpid()} | "
        f"Hora={datetime.now().strftime('%H:%M:%S')}"
    )

    time.sleep(2)

    print(
        f"Hijo {numero} terminando | "
        f"PID={os.getpid()}"
    )
    
def supervisor():

    print("\n" + "=" * 50)
    print("PARTE B - SUPERVISOR")
    print("=" * 50)

    procesos = []

    for numero in range(1, 3):

        proceso = multiprocessing.Process(
            target=tarea_hija,
            args=(numero,)
        )

        proceso.start()

        print(
            f"Supervisor registró hijo {numero}: "
            f"PID={proceso.pid} | "
            f"Inicio={datetime.now().strftime('%H:%M:%S')}"
        )

        procesos.append(proceso)

    print(
        "\nSupervisor esperando "
        "la terminación de los hijos...\n"
    )

    for proceso in procesos:

        proceso.join()

        print(
            f"PID {proceso.pid} terminó | "
            f"Código de salida={proceso.exitcode}"
        )
        
# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    N = 20_000_000
    IO_WAIT = 2

    print("=" * 50)
    print("INFORMACIÓN DE LA PLATAFORMA")
    print("=" * 50)

    print(
        f"Sistema operativo: "
        f"{platform.system()} {platform.release()}"
    )

    print(
        f"Procesador: "
        f"{platform.processor() or 'No identificado'}"
    )

    print(
        f"Núcleos lógicos: {os.cpu_count()}"
    )

    print(
        f"Python: {platform.python_version()}"
    )

    resultados = {}

    print("\n" + "=" * 50)
    print("PARTE A - CARGA DE CPU")
    print("=" * 50)

    resultados["CPU Secuencial"] = medir(
        "CPU Secuencial",
        cpu_secuencial,
        N
    )

    resultados["CPU Threads"] = medir(
        "CPU Threads",
        cpu_threads,
        N
    )

    resultados["CPU Procesos"] = medir(
        "CPU Procesos",
        cpu_procesos,
        N
    )

    print("\n" + "=" * 50)
    print("PARTE A - CARGA DE E/S")
    print("=" * 50)

    resultados["E/S Secuencial"] = medir(
        "E/S Secuencial",
        io_secuencial,
        IO_WAIT
    )

    resultados["E/S Threads"] = medir(
        "E/S Threads",
        io_threads,
        IO_WAIT
    )

    resultados["E/S Procesos"] = medir(
        "E/S Procesos",
        io_procesos,
        IO_WAIT
    )

    print("\n" + "=" * 50)
    print("RESUMEN DE MEDIANAS")
    print("=" * 50)

    for nombre, (_, mediana) in resultados.items():

        print(
            f"{nombre:<20}: "
            f"{mediana:.6f} s"
        )

    guardar_resultados(
        resultados,
        N,
        IO_WAIT
    )

    supervisor()