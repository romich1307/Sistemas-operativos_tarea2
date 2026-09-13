# Sistemas Operativos - Tarea 2

## Comparación de Threads y Procesos

Este proyecto corresponde al curso de **Sistemas Operativos** de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Nacional de San Agustín.

El objetivo es comparar el comportamiento de una ejecución secuencial, dos threads y dos procesos frente a cargas de CPU y de entrada/salida (E/S). Además, se implementa un supervisor básico de procesos utilizando `multiprocessing`.

## Autora

**Romina Giuliana Camargo Hilachoque**

Curso: Sistemas Operativos  
Docente: Norman Patrick Harvey Arce  
Universidad Nacional de San Agustín  
Arequipa - Perú  
2026

---

## Descripción

La práctica está dividida en dos partes.

### Parte A - Comparación de rendimiento

Se implementaron dos tipos de carga:

#### Carga de CPU

Se calcula la suma de cuadrados para un rango de:

```text
N = 20 000 000
```

La carga se ejecuta de tres formas:

- Secuencial
- Con 2 threads
- Con 2 procesos

#### Carga de E/S

Se simulan dos operaciones de entrada/salida mediante:

```python
time.sleep(2)
```

Esta carga también se ejecuta de tres formas:

- Secuencial
- Con 2 threads
- Con 2 procesos

Cada configuración se ejecuta **cinco veces** utilizando:

```python
time.perf_counter()
```

Al finalizar las cinco ejecuciones se calcula la mediana mediante:

```python
statistics.median()
```

El uso de la mediana permite obtener un valor representativo y reducir el efecto de mediciones atípicas.

---

### Parte B - Supervisor de procesos

Se implementó un supervisor utilizando:

```python
multiprocessing.Process
```

El supervisor realiza las siguientes operaciones:

- Crea dos procesos hijos.
- Registra el PID de cada proceso.
- Registra la hora de inicio.
- Espera la finalización mediante `join()`.
- Obtiene el código de salida mediante `exitcode`.

En la ejecución realizada se obtuvo:

```text
Hijo 1
PID: 17812
Hora de inicio: 19:36:22
Código de salida: 0

Hijo 2
PID: 17772
Hora de inicio: 19:36:22
Código de salida: 0
```

El código de salida `0` indica que ambos procesos finalizaron correctamente.

---

## Plataforma utilizada

Las pruebas fueron realizadas en la siguiente plataforma:

```text
Sistema operativo: Windows 10
Procesador: AMD64 Family 23 Model 24 Stepping 1, AuthenticAMD
Núcleos lógicos: 8
Versión de Python: 3.12.0rc3
Carga CPU: N = 20 000 000
Carga E/S: 2 operaciones de 2 segundos
Repeticiones: 5
Medida representativa: mediana
```

---

## Resultados experimentales

### Carga de CPU

| Ejecución | R1 | R2 | R3 | R4 | R5 | Mediana |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 1.691359 | 1.544113 | 1.611912 | 1.726216 | 2.281890 | 1.691359 s |
| 2 threads | 1.946203 | 2.008345 | 2.026139 | 1.914134 | 1.903202 | 1.946203 s |
| 2 procesos | 1.017342 | 1.065452 | 1.045021 | 1.019102 | 1.004955 | 1.019102 s |

Para una carga de CPU de `N = 20 000 000`, los dos procesos obtuvieron la menor mediana.

La ejecución secuencial obtuvo una mediana de `1.691359 s`.

Los dos threads obtuvieron `1.946203 s`.

Los dos procesos obtuvieron `1.019102 s`.

En esta plataforma y con este tamaño de carga, los procesos redujeron el tiempo mediano aproximadamente un **39.75 %** frente a la ejecución secuencial.

Los threads, en cambio, presentaron una mediana mayor que la ejecución secuencial en esta prueba de CPU.

---

### Carga de E/S

| Ejecución | R1 | R2 | R3 | R4 | R5 | Mediana |
|---|---:|---:|---:|---:|---:|---:|
| Secuencial | 4.000569 | 4.001333 | 4.001239 | 4.001761 | 4.000708 | 4.001239 s |
| 2 threads | 2.001695 | 2.000926 | 2.001156 | 2.001319 | 2.001228 | 2.001228 s |
| 2 procesos | 2.161688 | 2.158349 | 2.163313 | 2.162100 | 2.157939 | 2.161688 s |

La ejecución secuencial obtuvo una mediana de `4.001239 s`.

Los dos threads obtuvieron `2.001228 s`.

Los dos procesos obtuvieron `2.161688 s`.

En esta carga, los threads permitieron superponer las dos esperas de E/S y redujeron aproximadamente a la mitad el tiempo total respecto de la ejecución secuencial.

Los procesos también permitieron ejecutar las esperas de forma concurrente, aunque presentaron un costo adicional de creación.

---

## Interpretación de resultados

### Costo de creación

La ejecución secuencial no necesita crear threads ni procesos adicionales, por lo que presenta un menor costo inicial.

Los threads se crean dentro del mismo proceso y comparten recursos.

Los procesos requieren la creación de estructuras independientes, por lo que presentan un mayor costo de creación y administración.

### Datos compartidos o serializados

Los threads comparten el mismo espacio de memoria del proceso.

Esto facilita el acceso a datos comunes, aunque puede ser necesario utilizar mecanismos de sincronización cuando varios threads modifican información compartida.

Los procesos poseen espacios de memoria independientes.

Cuando necesitan intercambiar información pueden requerir mecanismos de comunicación entre procesos y serialización de datos.

### Uso de núcleos

El equipo utilizado posee **8 núcleos lógicos**.

La prueba utiliza dos procesos, por lo que ambos pueden ejecutarse en distintos núcleos lógicos.

En la carga de CPU, los procesos presentaron la menor mediana: `1.019102 s`.

Esto es consistente con un mejor aprovechamiento de más de un núcleo para una tarea intensiva de CPU.

### Threads y GIL

En CPython existe el **Global Interpreter Lock (GIL)**.

Este mecanismo limita la ejecución simultánea de bytecode Python por varios threads dentro del mismo proceso.

Por este motivo, los threads no necesariamente mejoran el rendimiento en tareas intensivas de CPU.

En esta ejecución, los threads obtuvieron una mediana mayor que la ejecución secuencial.

### Espera de E/S

En la ejecución secuencial, dos esperas de 2 segundos se ejecutan una después de la otra, produciendo aproximadamente `4 segundos`.

Con threads, ambas esperas pueden superponerse y el tiempo total se aproxima a `2 segundos`.

Los procesos también permiten esta superposición, aunque presentan un costo adicional de creación.

### Variabilidad del sistema

Las mediciones pueden variar debido a:

- procesos ejecutándose en segundo plano;
- planificación del sistema operativo;
- cambios en la frecuencia del procesador;
- uso de memoria;
- carga general del equipo;
- otras actividades del sistema.

Por esta razón, cada prueba fue ejecutada cinco veces y se utilizó la mediana.

En la prueba de CPU secuencial se obtuvo una medición de `2.281890 s`, considerablemente mayor que las otras repeticiones.

Esto demuestra por qué es conveniente utilizar la mediana en lugar de tomar una única medición.

---

## Estructura del proyecto

```text
Sistemas-operativos_tarea2/
│
├── laboratorio.py
├── resultados.txt
├── README.md
```

### `laboratorio.py`

Contiene la implementación completa de la Parte A y la Parte B.

Incluye:

- suma de cuadrados;
- simulación de E/S;
- ejecución secuencial;
- ejecución con threads;
- ejecución con procesos;
- temporizador;
- cálculo de mediana;
- generación de resultados;
- supervisor de procesos.

### `resultados.txt`

Contiene:

- información de la plataforma;
- cinco mediciones por configuración;
- medianas de cada prueba.

### `README.md`

Contiene la descripción general del proyecto, resultados y forma de ejecución.

### `informe/`

Contiene el informe desarrollado para la práctica.

### `capturas/`

Contiene evidencias de la ejecución del programa, código y supervisor.

---

## Ejecución del programa

Es necesario tener Python instalado.

Para comprobar la versión:

```powershell
python --version
```

En este proyecto se utilizó:

```text
Python 3.12.0rc3
```

Para ejecutar el programa:

```powershell
python laboratorio.py
```

El programa mostrará en la terminal:

- información de la plataforma;
- resultados de CPU;
- resultados de E/S;
- medianas;
- información del supervisor.

También generará automáticamente el archivo:

```text
resultados.txt
```

---

## Ejemplo de salida del supervisor

```text
==================================================
PARTE B - SUPERVISOR
==================================================

Supervisor registró hijo 1: PID=17812 | Inicio=19:36:22
Supervisor registró hijo 2: PID=17772 | Inicio=19:36:22

Supervisor esperando la terminación de los hijos...

Hijo 2 iniciado | PID=17772 | Hora=19:36:22
Hijo 1 iniciado | PID=17812 | Hora=19:36:22

Hijo 2 terminando | PID=17772
Hijo 1 terminando | PID=17812

PID 17812 terminó | Código de salida=0
PID 17772 terminó | Código de salida=0
```

---

## Tecnologías utilizadas

- Python
- `threading`
- `multiprocessing`
- `statistics`
- `time`
- `datetime`
- `os`
- `platform`
- Git
- GitHub

---

## Conclusiones

1. Para la carga de CPU de `N = 20 000 000`, los dos procesos obtuvieron la menor mediana con `1.019102 s`.

2. Los threads obtuvieron `1.946203 s` en la prueba de CPU, por lo que en esta ejecución no mejoraron el tiempo de la ejecución secuencial.

3. Para la carga de E/S, los threads obtuvieron una mediana de `2.001228 s`, aproximadamente la mitad del tiempo de la ejecución secuencial.

4. Los procesos también permitieron superponer las esperas de E/S, pero presentaron un tiempo ligeramente mayor que los threads debido al costo de creación y administración.

5. Los resultados dependen de la plataforma, del tipo de carga, del tamaño del problema y de las condiciones del sistema. Por ello, no se puede afirmar que threads o procesos sean siempre más rápidos.

---

## Repositorio

Este repositorio contiene el código fuente y la documentación correspondiente a la práctica de comparación entre threads y procesos del curso de Sistemas Operativos.
