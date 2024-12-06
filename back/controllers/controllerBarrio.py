from back.models.barrio import Barrio
class ControllerBarrio:
    def crearBarrio(self, id):
        barrio=Barrio(id)
        return barrio
