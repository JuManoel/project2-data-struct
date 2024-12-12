from back.controllers.controllerRed import ControllerRed
import json

# Crear instancia del controlador
controller = ControllerRed()

# Crear el barrio
response_barrio = controller.crearBarrio("A",)
print(response_barrio)

# Crear nodos con y sin tanques
response_nodo_a = controller.crearNodo(id="A", tank={"capacidad": 100, "capacitdadTotal": 100})
response_nodo_d = controller.crearNodo(id="D", tank={"capacidad": 150, "capacitdadTotal": 150})
response_nodo_b = controller.crearNodo(id="B")
response_nodo_c = controller.crearNodo(id="C")
response_nodo_e = controller.crearNodo(id="E")
response_nodo_f = controller.crearNodo(id="F")
response_nodo_g = controller.crearNodo(id="G")
response_nodo_h = controller.crearNodo(id="H")
response_nodo_i = controller.crearNodo(id="I")
response_nodo_j = controller.crearNodo(id="J")

print(response_nodo_a)
print(response_nodo_d)
print(response_nodo_b)
print(response_nodo_c)
print(response_nodo_e)
print(response_nodo_f)
print(response_nodo_g)
print(response_nodo_h)
print(response_nodo_i)
print(response_nodo_j)

# Crear aristas entre los nodos con diferentes pesos (flujo y flujo óptimo)
response_arista_ab = controller.crearArista(flujo=2, nodoIdTo=response_nodo_b["nodo"]["id"],
                                             obstruido=0, flujoOptimo=2, barrioId="A",
                                               nodoIdFrom="A")  # A -> B
response_arista_ac = controller.crearArista(flujo=3, nodoIdTo=response_nodo_c["nodo"]["id"], 
                                            obstruido=0, flujoOptimo=3, barrioId="A",
                                              nodoIdFrom="A")  # A -> C
response_arista_bd = controller.crearArista(flujo=1, nodoIdTo=response_nodo_d["nodo"]["id"],
                                             obstruido=0, flujoOptimo=1, barrioId="A",
                                              nodoIdFrom="B")  # B -> D
response_arista_be = controller.crearArista(flujo=4, nodoIdTo=response_nodo_e["nodo"]["id"],
                                             obstruido=0, flujoOptimo=4, barrioId="A",
                                              nodoIdFrom="B")  # B -> E
response_arista_cf = controller.crearArista(flujo=2, nodoIdTo=response_nodo_f["nodo"]["id"],
                                             obstruido=0, flujoOptimo=2, barrioId="A",
                                              nodoIdFrom="C")  # C -> F
response_arista_dg = controller.crearArista(flujo=1, nodoIdTo=response_nodo_g["nodo"]["id"],
                                             obstruido=0, flujoOptimo=1, barrioId="A",
                                              nodoIdFrom="D")  # D -> G
response_arista_eh = controller.crearArista(flujo=3, nodoIdTo=response_nodo_h["nodo"]["id"],
                                             obstruido=0, flujoOptimo=3, barrioId="A",
                                              nodoIdFrom="E")  # E -> H
response_arista_fi = controller.crearArista(flujo=2, nodoIdTo=response_nodo_i["nodo"]["id"],
                                             obstruido=0, flujoOptimo=2, barrioId="A",
                                              nodoIdFrom="F")  # F -> I
response_arista_gj = controller.crearArista(flujo=1, nodoIdTo=response_nodo_j["nodo"]["id"],
                                             obstruido=0, flujoOptimo=1, barrioId="A",
                                              nodoIdFrom="G")  # G -> J

print(response_arista_ab)
print(response_arista_ac)
print(response_arista_bd)
print(response_arista_be)
print(response_arista_cf)
print(response_arista_dg)
print(response_arista_eh)
print(response_arista_fi)
print(response_arista_gj)



# Guardar datos en archivo
response_guardar = controller.guardarEnArchivo("datos.json")
print(response_guardar)

# Mostrar datos almacenados
response_datos = controller.obtenerDatos()
print("Datos almacenados en la base de datos:")
print(json.dumps(response_datos["data"], indent=4))