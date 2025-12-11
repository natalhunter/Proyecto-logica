class DocumentoNodo:
    # Nodo de lista enlazada para documentos. Elegí un nodo simple para poder
    # iterar y copiar documentos sin depender de listas nativas.
    def __init__(self, nombre_documento: str):
        self.nombre = nombre_documento
        self.siguiente = None

class ListaDocumentos:
    # Lista enlazada para documentos; operaciones mínimas: agregar, iterar, copiar.
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre_documento: str) -> None:
        # Inserción al final: decisión humana porque el usuario suele añadir uno por uno.
        nodo = DocumentoNodo(nombre_documento)
        if self.cabeza is None:
            self.cabeza = nodo
            return
        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nodo

    def iter_nombres(self):
        actual = self.cabeza
        while actual:
            yield actual.nombre
            actual = actual.siguiente

    def copiar(self):
        # Crear una copia independiente de la lista de documentos.
        copia = ListaDocumentos()
        for nombre in self.iter_nombres():
            copia.agregar(nombre)
        return copia
    

    class UsuarioNodo:
    # Nodo que representa a un usuario; se usa también para encadenar en la tabla hash.
    def __init__(self, expediente: int, nombre: str, tipo_tramite: str,
                 tiempo_estimado: int, hora_turno: int):
        self.expediente = expediente
        self.nombre = nombre
        self.tipo_tramite = tipo_tramite
        self.tiempo_estimado = tiempo_estimado
        self.hora_turno = hora_turno
        self.documentos = ListaDocumentos()
        self.siguiente = None  # campo reutilizable para colas y chaining en hash


        # ---------------------------
# COLA ENLAZADA (FIFO)
# ---------------------------

class ColaEnlazada:
    # Cola FIFO por enlace; decisión humana para cumplir requerimiento de estructuras.
    def __init__(self):
        self.frente = None
        self.final = None

    def encolar(self, usuario: UsuarioNodo) -> None:
        # Mantener O(1). Aseguro que 'siguiente' del usuario quede en None.
        usuario.siguiente = None
        if self.frente is None:
            self.frente = self.final = usuario
            return
        self.final.siguiente = usuario
        self.final = usuario

    def desencolar(self) -> UsuarioNodo | None:
        # Devolver el nodo o None si está vacía.
        if self.frente is None:
            return None
        u = self.frente
        self.frente = u.siguiente
        if self.frente is None:
            self.final = None
        u.siguiente = None
        return u

    def esta_vacia(self) -> bool:
        return self.frente is None

    def iterar(self):
        actual = self.frente
        while actual:
            yield actual
            actual = actual.siguiente

    def contar(self) -> int:
        # O(n), uso ocasional en reasignaciones; justificado por tamaño moderado de colas.
        c = 0
        actual = self.frente
        while actual:
            c += 1
            actual = actual.siguiente
        return c
# ---------------------------
# RECEPTOR (VENTANILLA)
# ---------------------------

class Receptor:
    # Modelo del receptor en ventanilla. Controla recorridas (penalizaciones).
    def __init__(self, id_receptor: str):
        self.id = id_receptor
        self.cola = ColaEnlazada()
        self.recorridas = 0  # contador de desplazamientos de turnos
        self.activo = True

    def registrar_recorrido(self) -> None:
        self.recorridas += 1
        if self.recorridas > 3:
            self.activo = False



            
    


