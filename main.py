from back.models.arista import Arista
from back.models.nodo import Nodo
from back.models.tank import Tank
from back.models.barrio import Barrio
import json
from back.models.BaseDatos import BaseDatos
tank_a = Tank(capacidad=100, capacidadTotal=100)
tank_b = Tank(capacidad=150, capacidadTotal=150)

# Crear nodos con y sin tanques
nodo_a = Nodo(id="A", tank=tank_a)
nodo_b = Nodo(id="B")
nodo_c = Nodo(id="C")
nodo_d = Nodo(id="D", tank=tank_b)
nodo_e = Nodo(id="E")
nodo_f = Nodo(id="F")
nodo_g = Nodo(id="G")
nodo_h = Nodo(id="H")
nodo_i = Nodo(id="I")
nodo_j = Nodo(id="J")

# Crear aristas entre los nodos con diferentes pesos (flujo y flujo óptimo)
aristas = [
    Arista(flujo=2, nodo=nodo_b, obstruido=0, flujoOptimo=2),  # A -> B
    Arista(flujo=3, nodo=nodo_c, obstruido=0, flujoOptimo=3),  # A -> C
    Arista(flujo=1, nodo=nodo_d, obstruido=0, flujoOptimo=1),  # B -> D
    Arista(flujo=4, nodo=nodo_e, obstruido=0, flujoOptimo=4),  # B -> E
    Arista(flujo=2, nodo=nodo_f, obstruido=0, flujoOptimo=2),  # C -> F
    Arista(flujo=1, nodo=nodo_g, obstruido=0, flujoOptimo=1),  # D -> G
    Arista(flujo=3, nodo=nodo_h, obstruido=0, flujoOptimo=3),  # E -> H
    Arista(flujo=2, nodo=nodo_i, obstruido=0, flujoOptimo=2),  # F -> I
    Arista(flujo=1, nodo=nodo_j, obstruido=0, flujoOptimo=1),  # G -> J
]

# Crear el barrio
barrio = Barrio("A")

# Agregar nodos al barrio
nodos = [nodo_a, nodo_b, nodo_c, nodo_d, nodo_e, nodo_f, nodo_g, nodo_h, nodo_i, nodo_j]
for nodo in nodos:
    barrio.agregarNodo(nodo)

# Conectar los nodos con aristas
arista_map = {
    nodo_a: [aristas[0], aristas[1]],
    nodo_b: [aristas[2], aristas[3]],
    nodo_c: [aristas[4]],
    nodo_d: [aristas[5]],
    nodo_e: [aristas[6]],
    nodo_f: [aristas[7]],
    nodo_g: [aristas[8]],
}

for nodo, aristas_nodo in arista_map.items():
    for arista in aristas_nodo:
        barrio.agregarArista(nodo, arista)

# Mostrar la estructura del barrio
print("Barrio completo con valores de aristas:")
print(json.dumps(barrio.toDict(), indent=4))

# Ejecutar el algoritmo para generar el subgrafo
subgrafo = barrio.shortestPathsFromTanks()

# Mostrar el subgrafo resultante
print("Subgrafo generado por shortestPathsFromTanks:")
print(json.dumps(subgrafo.toDict(), indent=4))

# Crear instancia de BaseDatos
base_datos = BaseDatos()

# Almacenar nodos en la base de datos
for nodo in nodos:
    base_datos.almacenarNodo(nodo)

# Almacenar aristas en la base de datos
for arista in aristas:
    base_datos.almacenarArista(arista)

# Almacenar barrio en la base de datos
base_datos.almacenarBarrio(barrio.id, barrio)

# Almacenar tanques en la base de datos
base_datos.almacenarTanque("tank_a", tank_a)
base_datos.almacenarTanque("tank_b", tank_b)

# Guardar datos en archivo
base_datos.guardarEnArchivo("datos.json")

# Mostrar datos almacenados
print("Datos almacenados en la base de datos:")
print(json.dumps(base_datos.obtenerDatos(), indent=4))