# -------------------------------------------------------------
# PROYECTO FINAL: SISTEMA DE ENTREGA DE DOCUMENTACIÓN
# Contexto: Optimización de atención de turnos en ventanillas de instituciones
# Autor: Gabriel Gamez / Equipo
# Entorno: Python 3.11+, sin estructuras avanzadas para operaciones principales
# -------------------------------------------------------------

# ---------------------
# Constantes del sistema
DOCUMENTOS = ("Acta", "RFC", "CURP", "INE", "Comprobante de pago")  
T_DOC = 5          # Tiempo estimado para trámites de documentos básicos
T_SIMPLE = 10      # Tiempo estimado para trámites simples
T_COMPLEJO = 20    # Tiempo estimado para trámites complejos
T_PAGOS = 5        # Tiempo máximo para entrega de pagos rápidos
MAX_TURNO = 5      # Incremento máximo en minutos si hay retraso en atención
MAX_MAL_SERVICIO = 3  # Número de retrasos tolerados por receptor antes de rotación

# -------------------------------------------------------------
# Nodo genérico para listas enlazadas
class Nodo:
    """
    Propósito: Contener un valor y referencia al siguiente nodo.
    Explicación humana: Cada nodo representa un cliente dentro de una cola enlazada.
    Esto permite insertar, eliminar o recorrer clientes en orden de turno.
    Complejidad temporal: O(1) para creación.
    Complejidad espacial: O(1) por nodo.
    Edge cases: Puede almacenar cualquier tipo de valor. Si no apunta a otro nodo, sig = None.
    """
    def __init__(self, valor):
        self.v = valor
        self.sig = None

# -------------------------------------------------------------
# Cola ordenada por prioridad de turno
class ColaOrdenada:
    """
    Propósito: Mantener clientes ordenados por número de turno.
    Algoritmo:
      - Para insertar, recorre la lista hasta encontrar la posición adecuada.
      - pop_min elimina el nodo con turno más bajo (atención siguiente).
    Complejidad:
      - Inserción: O(1) mejor caso (inicio), O(n) peor caso (final)
      - pop_min: O(1)
      - Mostrar: O(n)
    Edge cases: Cola vacía, reinserción por retrasos.
    """
    def __init__(self):
        self.ini = None  # Nodo con turno más bajo

    def insertar(self, par):
        """
        Inserta un cliente manteniendo orden por turno.
        par = (nombre, tipo, tiempo, turno, hora, docs, receptor)
        """
        n = Nodo(par)
        if not self.ini or par[3] < self.ini.v[3]:
            n.sig = self.ini
            self.ini = n
            return
        a = self.ini
        while a.sig and a.sig.v[3] <= par[3]:
            a = a.sig
        n.sig = a.sig
        a.sig = n

    def pop_min(self):
        """
        Elimina y retorna el cliente con turno más bajo.
        Retorna None si la cola está vacía.
        """
        if not self.ini:
            return None
        v = self.ini.v
        self.ini = self.ini.sig
        return v

    def mostrar(self):
        """
        Retorna lista de clientes en orden de turno.
        Uso: Generar snapshot del sistema.
        """
        a = self.ini
        res = []
        while a:
            res.append(a.v)
            a = a.sig
        return res

# -------------------------------------------------------------
# Hash table simple para clientes
class HashNode:
    """
    Nodo para tabla hash usando encadenamiento.
    Almacena clave (nombre del cliente) y valor (datos asociados).
    """
    def __init__(self, k, v):
        self.k = k
        self.v = v
        self.sig = None

class Hash:
    """
    Propósito: Permitir búsqueda rápida de clientes por nombre.
    Algoritmo: Hash simple basado en suma ponderada de caracteres. Manejo de colisiones mediante encadenamiento.
    Complejidad:
      - Promedio: O(1)
      - Peor caso: O(n/bucket)
      - Espacio: O(n)
    Edge cases: get/delete en clave inexistente retorna None.
    """
    def __init__(self, cap=31):
        self.cap = cap
        self.b = [None]*cap

    def _h(self, k):
        h = 0
        for c in k:
            h = (h*31 + ord(c)) % self.cap
        return h

    def set(self, k, v):
        i = self._h(k)
        a = self.b[i]
        while a:
            if a.k == k:
                a.v = v
                return
            a = a.sig
        n = HashNode(k, v)
        n.sig = self.b[i]
        self.b[i] = n

    def get(self, k):
        i = self._h(k)
        a = self.b[i]
        while a:
            if a.k == k:
                return a.v
            a = a.sig
        return None

    def delete(self, k):
        i = self._h(k)
        a = self.b[i]
        p = None
        while a:
            if a.k == k:
                if p: p.sig = a.sig
                else: self.b[i] = a.sig
                return
            p = a
            a = a.sig

# -------------------------------------------------------------
# Clase para receptores de ventanilla
class Receptor:
    """
    Propósito: Mantener estado de cada ventanilla y número de retrasos.
    Edge cases: Si mal_servicio > MAX_MAL_SERVICIO, se reinicia y puede cambiar receptor.
    """
    def __init__(self, nombre):
        self.nombre = nombre
        self.mal_servicio = 0
        self.ocupado_hasta = 0

# Ventanillas iniciales
ventanillas = {
    "v1": Receptor("Receptor 1"),
    "v2": Receptor("Receptor 2"),
    "v3": Receptor("Receptor 3"),
    "v4": Receptor("Receptor 4"),
}

cola_prio = ColaOrdenada()
tabla = Hash()

# -------------------------------------------------------------
# Registro de cliente
def registrar(cliente):
    """
    Asigna tiempo y ventanilla según tipo de trámite. Inserta en cola y hash.
    Edge cases: Tipo no reconocido se asigna a ventanilla de pagos.
    """
    nombre, tipo, docs, turno, hora, receptor_nombre = cliente
    if tipo == "doc": t = T_DOC; vent = ventanillas["v1"]
    elif tipo == "simple": t = T_SIMPLE; vent = ventanillas["v2"]
    elif tipo == "complejo": t = T_COMPLEJO; vent = ventanillas["v3"]
    else: t = T_PAGOS; vent = ventanillas["v4"]

    cola_prio.insertar((nombre, tipo, t, turno, hora, docs, vent.nombre))
    tabla.set(nombre, (tipo, t, turno, hora, docs, vent.nombre))
    return t

# -------------------------------------------------------------
# Snapshot de clientes
def snapshot():
    res = []
    for x in cola_prio.mostrar():
        id_demo = "ID{:04d}".format(x[3])
        res.append(f"{id_demo} {x[0]} {x[1]} {x[2]}min turno{x[3]} hora {x[4]} docs{x[5]} receptor {x[6]}")
    return res

# -------------------------------------------------------------
# Atención de clientes
def atender_clientes():
    """
    Atención secuencial de clientes, manejo de retrasos y rotación de receptores.
    Algoritmo humano: pop_min de cola, revisar ocupación del receptor, recalcular turno si necesario.
    """
    print("\n--- Atención de clientes ---")
    while True:
        cliente = cola_prio.pop_min()
        if not cliente:
            print("No hay más clientes en espera")
            break
        nombre, tipo, t, turno, hora, docs, receptor_nombre = cliente
        receptor = ventanillas["v" + receptor_nombre[-1]]

        if receptor.ocupado_hasta > turno:
            turno += MAX_TURNO
            print(f"Cliente {nombre} retrasado, nuevo turno {turno}")
            receptor.mal_servicio += 1
            if receptor.mal_servicio > MAX_MAL_SERVICIO:
                print(f"{receptor.nombre} removido por mal servicio, se asigna nuevo receptor")
                receptor.mal_servicio = 0
            cola_prio.insertar((nombre, tipo, t, turno, hora, docs, receptor_nombre))
        else:
            receptor.ocupado_hasta = turno + t
            print(f"Cliente {nombre} atendido en {receptor.nombre} durante {t} minutos")

# -------------------------------------------------------------
# Buscar cliente por turno
def buscar_por_turno(turno_buscar):
    a = cola_prio.ini
    while a:
        if a.v[3] == turno_buscar:
            return a.v
        a = a.sig
    return None

def mostrar_cliente_por_turno():
    try:
        turno_input = int(input("Ingresa el número de turno a buscar: "))
    except ValueError:
        print("Turno inválido. Debe ser un número entero.")
        return
    cliente = buscar_por_turno(turno_input)
    if cliente:
        print(f"Cliente encontrado: Turno {cliente[3]} - Nombre: {cliente[0]}, Tipo: {cliente[1]}, Tiempo: {cliente[2]} min, Hora: {cliente[4]}, Documentos: {cliente[5]}, Receptor: {cliente[6]}")
    else:
        print(f"No se encontró ningún cliente con turno {turno_input}")


# -------------------------------------------------------------
# Menú interactivo
def menu():

    turno_cont = 5

    while True:
        print("\n--- Menú Proyecto Final ---")
        print("1. Registrar cliente")
        print("2. Mostrar snapshot de turnos")
        print("3. Atender clientes")
        print("4. Consultar cliente en tabla por nombre")
        print("5. Buscar cliente por turno")
        print("6. Salir")
        opcion = input("Elige opción: ")

        if opcion == "1":
            nombre = input("Nombre del cliente: ")
            tipo = input("Tipo (doc/simple/complejo/pago): ").lower()
            docs = input("Documentos (separados por coma): ").split(",")
            receptor_nombre = input("Receptor asignado: ")
            hora = input("Hora (ej. 10:55): ")
            registrar((nombre, tipo, docs, turno_cont, hora, receptor_nombre))
            print(f"Cliente registrado con turno {turno_cont}")
            turno_cont += 1
        elif opcion == "2":
            s = snapshot()
            print("\n--- Snapshot ---")
            for x in s:
                print(x)
        elif opcion == "3":
            atender_clientes()
        elif opcion == "4":
            clave = input("Nombre del cliente a consultar: ")
            res = tabla.get(clave)
            if res:
                print(f"Cliente: {clave}, Datos: {res}")
            else:
                print("Cliente no encontrado")
        elif opcion == "5":
            mostrar_cliente_por_turno()
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

# -------------------------------------------------------------
# Ejecución principal
if __name__ == "__main__":
    menu()

