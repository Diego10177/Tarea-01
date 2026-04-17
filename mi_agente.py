import random
from entorno import Agente

class MiAgente(Agente):
    def _init_(self):
        super()._init_(nombre="Navegador_Pro_v2")
        # Diccionario para almacenar el rastro de coordenadas
        self.mapa_mental = {}
        self.direccion_anterior = None

    def al_iniciar(self):
        self.mapa_mental = {}
        self.direccion_anterior = None

    def decidir(self, percepcion):
        # 1. ACTUALIZAR ESTADO INTERNO
        coord_actual = percepcion['posicion']
        self.mapa_mental[coord_actual] = True

        # 2. DETECCIÓN DE OBJETIVO FINAL
        # Si la meta está en una celda vecina, retornamos esa dirección de inmediato
        for accion in self.ACCIONES:
            if percepcion[accion] == 'meta':
                return accion

        # 3. CLASIFICACIÓN DE RUTAS DISPONIBLES
        vias_libres = [a for a in self.ACCIONES if percepcion[a] == 'libre']
        
        exploracion = []
        retorno = []

        for v in vias_libres:
            dr, dc = self.DELTAS[v]
            proxima_pos = (coord_actual[0] + dr, coord_actual[1] + dc)
            
            if proxima_pos not in self.mapa_mental:
                exploracion.append(v)
            else:
                retorno.append(v)

        # 4. LÓGICA DE SELECCIÓN DE MOVIMIENTO
        eleccion = random.choice(exploracion)

        if exploracion:
           
            # Mantener el rumbo si el camino sigue siendo nuevo
            if self.direccion_anterior in exploracion:
                eleccion = self.direccion_anterior
            else:
                # Si no hay inercia ni 'abajo', elegir ruta nueva al azar
                eleccion = random.choice(exploracion)
        
        elif retorno:
            # En caso de callejón, retroceder por zonas conocidas
            eleccion = random.choice(retorno)
        else:
            # Backup de seguridad
            eleccion = random.choice(self.ACCIONES)

        self.direccion_anterior = eleccion
        return eleccion