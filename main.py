from back.controllers.controllerRed import ControllerRed
import json

# Crear instancia del controlador
controller = ControllerRed()

# Crear el barrio
response_barrio = controller.crearBarrio("A")

# Crear nodos con y sin tanques
response_nodo_a = controller.crearNodo(id="A", tank={"capacidad": 100, "capacitdadTotal": 100}, barrioId="A")
response_nodo_d = controller.crearNodo(id="D", tank={"capacidad": 150, "capacitdadTotal": 150}, barrioId="A")
response_nodo_b = controller.crearNodo(id="B", barrioId="A")
response_nodo_c = controller.crearNodo(id="C", barrioId="A")
response_nodo_e = controller.crearNodo(id="E", barrioId="A")
response_nodo_f = controller.crearNodo(id="F", barrioId="A")
response_nodo_g = controller.crearNodo(id="G", barrioId="A")
response_nodo_h = controller.crearNodo(id="H", barrioId="A")
response_nodo_i = controller.crearNodo(id="I", barrioId="A")
response_nodo_j = controller.crearNodo(id="J", barrioId="A")
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
# Guardar datos en archivo
response_guardar = controller.guardarEnArchivo("datos.json")
# Mostrar datos almacenados
response_datos = controller.obtenerDatos()
# Crear el barrio B
response_barrio_b = controller.crearBarrio("B")

# Crear nodos para el barrio B
response_nodo_k = controller.crearNodo(id="K", tank={"capacidad": 200, "capacitdadTotal": 200}, barrioId="B")
response_nodo_l = controller.crearNodo(id="L", barrioId="B")
response_nodo_m = controller.crearNodo(id="M", barrioId="B")

# Crear aristas para el barrio B
response_arista_kl = controller.crearArista(flujo=3, nodoIdTo=response_nodo_l["nodo"]["id"],
                       obstruido=0, flujoOptimo=3, barrioId="B",
                        nodoIdFrom="K")  # K -> L
response_arista_lm = controller.crearArista(flujo=2, nodoIdTo=response_nodo_m["nodo"]["id"],
                       obstruido=0, flujoOptimo=2, barrioId="B",
                        nodoIdFrom="L")  # L -> M

# Crear el barrio C
response_barrio_c = controller.crearBarrio("C")

# Crear nodos para el barrio C
response_nodo_n = controller.crearNodo(id="N", tank={"capacidad": 250, "capacitdadTotal": 250}, barrioId="C")
response_nodo_o = controller.crearNodo(id="O", barrioId="C")
response_nodo_p = controller.crearNodo(id="P", barrioId="C")

# Crear aristas para el barrio C
response_arista_no = controller.crearArista(flujo=4, nodoIdTo=response_nodo_o["nodo"]["id"],
                       obstruido=0, flujoOptimo=4, barrioId="C",
                        nodoIdFrom="N")  # N -> O
response_arista_op = controller.crearArista(flujo=3, nodoIdTo=response_nodo_p["nodo"]["id"],
                       obstruido=0, flujoOptimo=3, barrioId="C",
                        nodoIdFrom="O")  # O -> P

# Guardar datos en archivo nuevamente
response_guardar = controller.guardarEnArchivo("datos.json")

# Mostrar datos almacenados nuevamente
response_datos = controller.obtenerDatos()


# Crear aristas entre barrios
response_arista_barrio_a_b = controller.crearAristaBarrio(flujo=5, tankId=response_nodo_a["nodo"]["id"],
                              obstruido=0, barrioId="B", nodoId=response_nodo_k["nodo"]["id"],
                              flujoOptimo=5)  # A -> K (Barrio A -> Barrio B)
response_arista_barrio_b_c = controller.crearAristaBarrio(flujo=6, tankId=response_nodo_k["nodo"]["id"],
                              obstruido=0, barrioId="C", nodoId=response_nodo_n["nodo"]["id"],
                              flujoOptimo=6)  # K -> N (Barrio B -> Barrio C)


response_guardar = controller.guardarEnArchivo("datos.json")

responseObstrucion = controller.crearObstrucion("A", "C", 1)


optimoResponse = controller.optimizarBarrio("A")
optimoResponse = controller.optimizarBarrio("B")
optimoResponse = controller.optimizarBarrio("C")

response_guardar = controller.guardarEnArchivo("datos.json")





# Eliminar una arista entre nodos en el barrio A
response_eliminar_arista_ab = controller.eliminarArista(barrioId="A", nodoIdFrom="A", nodoIdTo="B")

# Eliminar un nodo en el barrio A
response_eliminar_nodo_j = controller.eliminarNodo(barrioId="A", nodoId="J")

responseRed = controller.optimizarRed()

responseObstrucion = controller.crearObstrucion("A", "C", 2)

response_guardar = controller.guardarEnArchivo("datos.json")
