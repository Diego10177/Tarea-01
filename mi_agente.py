"""
mi_agente.py — Aquí defines tu agente.
╔══════════════════════════════════════════════╗
║  ✏️  EDITA ESTE ARCHIVO                      ║
╚══════════════════════════════════════════════╝

Tu agente debe:
    1. Heredar de la clase Agente
    2. Implementar el método decidir(percepcion)
    3. Retornar: 'arriba', 'abajo', 'izquierda' o 'derecha'

Lo que recibes en 'percepcion':
───────────────────────────────
percepcion = {
    'posicion':       (3, 5),          # Tu fila y columna actual
    'arriba':         'libre',         # Qué hay arriba
    'abajo':          'pared',         # Qué hay abajo
    'izquierda':      'libre',         # Qué hay a la izquierda
    'derecha':        None,            # None = fuera del mapa

    # OPCIONAL — brújula hacia la meta.
    # No es percepción real del entorno, es información global.
    # Usarla hace el ejercicio más fácil. No usarla es más realista.
    'direccion_meta': ('abajo', 'derecha'),
}

Valores posibles de cada dirección:
    'libre'  → puedes moverte ahí
    'pared'  → bloqueado
    'meta'   → ¡la meta! ve hacia allá
    None     → borde del mapa, no puedes ir

Si tu agente retorna un movimiento inválido (hacia pared o
fuera del mapa), simplemente se queda en su lugar.
"""

from entorno import Agente


class MiAgente(Agente):
    """
    Tu agente de navegación.

    Implementa el método decidir() para que el agente
    llegue del punto A al punto B en el grid.
    """

    def __init__(self):
        super().__init__(nombre="Mi Agente")
        # Puedes agregar atributos aquí si los necesitas.
        # Ejemplo:
        #   self.pasos = 0
        #   self.memoria = {}
        self.memoria = {} 

    def al_iniciar(self):
        """Se llama una vez al iniciar la simulación. Opcional."""
        self.memoria = {}
        pass

    def decidir(self, percepcion):
        pos_actual = percepcion['posicion']
        
        # 1. Registrar visita actual en la memoria
        self.memoria[pos_actual] = self.memoria.get(pos_actual, 0) + 1
        
        # 2. Obtener brújula (hacia dónde queda la meta)
        vert, horiz = percepcion['direccion_meta']

        # 3. Crear lista de prioridades basada en la brújula
        prioridades = []
        if vert != 'ninguna': prioridades.append(vert)
        if horiz != 'ninguna': prioridades.append(horiz)
        
        # Añadimos el resto de direcciones posibles
        for acc in self.ACCIONES:
            if acc not in prioridades:
                prioridades.append(acc)

        # 4. Elegir el mejor movimiento basado en la menor cantidad de visitas
        mejor_accion = None
        min_visitas = float('inf')

        for accion in prioridades:
            estado = percepcion.get(accion)
            
            # Si vemos la meta, vamos directo
            if estado == 'meta':
                return accion
            
            # Si la celda está libre, evaluamos cuántas veces hemos pasado por ahí
            if estado == 'libre':
                # Calculamos la posición futura para consultar la memoria
                dr, dc = self.DELTAS[accion]
                futura_pos = (pos_actual[0] + dr, pos_actual[1] + dc)
                
                visitas = self.memoria.get(futura_pos, 0)
                
                # Buscamos la dirección que nos lleve a la celda MENOS visitada
                if visitas < min_visitas:
                    min_visitas = visitas
                    mejor_accion = accion

        return mejor_accion if mejor_accion else 'arriba'