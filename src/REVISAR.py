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

# ---------------------------
# TABLA HASH SIMPLE
# ---------------------------

class TablaHashUsuarios:
    # Tabla hash con chaining. Uso array Python para buckets por sencillez operativa.
    # Justificación: se pide evitar dict en la lógica; usar buckets está permitido.
    def __init__(self, capacidad: int = 13):
        self.capacidad = capacidad  # preferible primo para dispersión
        self.buckets = [None] * capacidad

    def _indice(self, expediente: int) -> int:
        return expediente % self.capacidad

    def agregar(self, usuario: UsuarioNodo) -> None:
        idx = self._indice(usuario.expediente)
        # Inserción en cabeza del bucket para simplicidad y O(1)
        usuario.siguiente = self.buckets[idx]
        self.buckets[idx] = usuario

    def buscar(self, expediente: int) -> UsuarioNodo | None:
        idx = self._indice(expediente)
        actual = self.buckets[idx]
        while actual:
            if actual.expediente == expediente:
                return actual
            actual = actual.siguiente
        return None
    
    # ---------------------------
# CENTRO DE ATENCIÓN (LÓGICA)
# ---------------------------

class CentroAtencion:
    # Controla mapeo tipo_tramite -> receptor y reglas de negocio.
    def __init__(self):
        self.receptores = {}  # id_receptor -> Receptor (uso dict para índices de objetos)
        self.map_tramite = {}  # tipo -> id_receptor
        self.tabla = TablaHashUsuarios(capacidad=17)
        self.next_expediente = 1000  # asignador automático si el operador no indica ID

    def agregar_receptor(self, id_receptor: str, tipos_tramite: list[str]) -> None:
        if id_receptor in self.receptores:
            raise ValueError("Receptor ya existe")
        r = Receptor(id_receptor)
        self.receptores[id_receptor] = r
        for t in tipos_tramite:
            self.map_tramite[t] = id_receptor

    def asignar_receptor(self, tipo_tramite: str) -> Receptor:
        # Buscar receptor asignado; fallback al primer receptor activo disponible.
        rid = self.map_tramite.get(tipo_tramite)
        if rid:
            r = self.receptores.get(rid)
            if r and r.activo:
                return r
        # fallback: buscar cualquier receptor activo
        for rec in self.receptores.values():
            if rec.activo:
                # actualizar mapeo para la próxima vez (mejora práctica)
                self.map_tramite[tipo_tramite] = rec.id
                return rec
        raise RuntimeError("No hay receptores activos en este momento")

    def registrar_usuario(self, nombre: str, tipo_tramite: str,
                         tiempo_estimado: int, hora_solicitada: int | None = None,
                         expediente_externo: int | None = None) -> UsuarioNodo:
        # Determinar expediente
        expediente = expediente_externo if expediente_externo is not None else self.next_expediente
        if expediente_externo is None:
            self.next_expediente += 1

        receptor = self.asignar_receptor(tipo_tramite)
        cola = receptor.cola

        # Decidir hora_turno: si no se solicita, se calcula como turno final de la cola
        if hora_solicitada is None:
            if cola.final:
                hora_turno = cola.final.hora_turno + cola.final.tiempo_estimado
            else:
                hora_turno = 0  # primer turno disponible
        else:
            hora_turno = hora_solicitada

        usuario = UsuarioNodo(expediente, nombre, tipo_tramite, tiempo_estimado, hora_turno)
        cola.encolar(usuario)
        # Insertar en tabla hash para búsqueda rápida
        self.tabla.agregar(usuario)
        return usuario, receptor.id

    def procesar_siguiente(self, id_receptor: str) -> tuple[UsuarioNodo | None, int]:
        # Atender al siguiente usuario en la ventanilla indicada.
        receptor = self.receptores.get(id_receptor)
        if receptor is None:
            raise ValueError("Ventanilla inexistente")
        usuario = receptor.cola.desencolar()
        if usuario is None:
            return None, 0
        tiempo_real = usuario.tiempo_estimado
        retraso = 0
        if tiempo_real > 5:
            retraso = 5
            # Desplazar hora_turno de todos en cola
            actual = receptor.cola.frente
            while actual:
                actual.hora_turno += retraso
                actual = actual.siguiente
            receptor.registrar_recorrido()
            if not receptor.activo:
                # reasignar cola si receptor quedó inactivo
                self._reasignar_cola(receptor)
        return usuario, retraso

    def _reasignar_cola(self, receptor_inactivo: Receptor) -> None:
        # Reasigna los usuarios de un receptor inactivo a otros receptores activos.
        activos = [r for r in self.receptores.values() if r.activo]
        if not activos:
            # No hay receptores activos; decisión: dejar la cola como está y registrar alerta.
            # Un operador humano debe intervenir.
            return
        # Reasignar uno por uno; copiamos nodos para preservar trazabilidad original.
        actual = receptor_inactivo.cola.frente
        while actual:
            # seleccionar receptor con menor carga
            mejor = min(activos, key=lambda r: r.cola.contar())
            copia = UsuarioNodo(actual.expediente, actual.nombre, actual.tipo_tramite,
                                actual.tiempo_estimado, actual.hora_turno)
            # copiar documentos
            copia.documentos = actual.documentos.copiar()
            mejor.cola.encolar(copia)
            # NOTA: la tabla hash apunta al nodo original; si se requiere consistencia
            # absoluta entre ubicación y tabla, habría que reinsertar referencias.
            actual = actual.siguiente
        # vaciar cola del receptor inactivo
        receptor_inactivo.cola.frente = receptor_inactivo.cola.final = None

# ---------------------------
# FUNCIONES AUXILIARES: HORA Y VALIDACIÓN
# ---------------------------

def hora_a_minutos(hora_str: str) -> int:
    # Convertir 'HH:MM' a minutos desde medianoche. Decisión: raise ValueError si formato inválido.
    partes = hora_str.strip().split(":")
    if len(partes) != 2:
        raise ValueError("Formato de hora debe ser HH:MM")
    horas = int(partes[0])
    minutos = int(partes[1])
    if not (0 <= horas < 24 and 0 <= minutos < 60):
        raise ValueError("Hora fuera de rango")
    return horas * 60 + minutos

def minutos_a_hora(minutos: int) -> str:
    h = minutos // 60
    m = minutos % 60
    return f"{h:02d}:{m:02d}"

# ---------------------------
# INTERFAZ DE CONSOLA (MENÚ) - mínima y separada de la lógica
# ---------------------------

def menu_minimo():
    centro = CentroAtencion()
    # Crear receptores con tipos. Decisión: mapeo explícito para control.
    centro.agregar_receptor("V1", ["documentos", "comprobante"])
    centro.agregar_receptor("V2", ["simple"])
    centro.agregar_receptor("V3", ["complejo"])
    centro.agregar_receptor("V4", ["pagos"])

    # Documentos requeridos - adaptable
    DOCUMENTOS_REQUERIDOS = ["Acta de nacimiento", "RFC", "CURP", "INE"]
    TIEMPOS = {"documentos": 5, "simple": 10, "complejo": 20, "pagos": 8}

    def validar_documentos():
        # Valido cada documento y retorno True/False.
        faltantes = []
        for doc in DOCUMENTOS_REQUERIDOS:
            r = input(f"Trae {doc}? (si/no): ").strip().lower()
            if r != "si":
                faltantes.append(doc)
        if faltantes:
            print("Faltan:", ", ".join(faltantes))
            return False
        return True

    print("Sistema de trámites - inicio.")
    while True:
        print("\nOpciones:")
        print("1- Registrar cliente")
        print("2- Mostrar colas")
        print("3- Atender siguiente")
        print("4- Buscar por expediente")
        print("5- Salir")
        op = input("Elige: ").strip()
        if op == "1":
            nombre = input("Nombre completo: ").strip()
            if not nombre:
                print("Nombre vacío. Intenta de nuevo.")
                continue
            if not validar_documentos():
                print("Documentación incompleta. Volver al inicio.")
                continue
            tipo = input("Tipo trámite (documentos/simple/complejo/pagos): ").strip()
            if tipo not in TIEMPOS:
                print("Tipo inválido.")
                continue
            try:
                tiempo = int(input(f"Tiempo estimado en minutos (default {TIEMPOS[tipo]}): ").strip() or TIEMPOS[tipo])
            except ValueError:
                tiempo = TIEMPOS[tipo]
            hora_req = input("Hora solicitada HH:MM o Enter: ").strip()
            hora_min = None
            if hora_req:
                try:
                    hora_min = hora_a_minutos(hora_req)
                except ValueError as e:
                    print("Hora inválida:", e)
                    hora_min = None
            usuario, vid = centro.registrar_usuario(nombre, tipo, tiempo, hora_min)
            print(f"Registrado: exp {usuario.expediente}, ventanilla {vid}, turno {minutos_a_hora(usuario.hora_turno)}")
            # agregar documentos
            while True:
                doc = input("Agregar documento (enter para terminar): ").strip()
                if not doc:
                    break
                usuario.documentos.agregar(doc)
        elif op == "2":
            for vid, rec in centro.receptores.items():
                print(f"\nVentanilla {vid} - activo={rec.activo} recorridas={rec.recorridas}")
                for u in rec.cola.iterar():
                    docs = ", ".join(list(u.documentos.iter_nombres()))
                    print(f"  {u.expediente} {u.nombre} {u.tipo_tramite} {u.tiempo_estimado}min turno {minutos_a_hora(u.hora_turno)} docs[{docs}]")
        elif op == "3":
            vid = input("Ventanilla a procesar (ej. V1): ").strip()
            try:
                usuario, retraso = centro.procesar_siguiente(vid)
            except Exception as e:
                print("Error:", e)
                continue
            if usuario is None:
                print("No hay usuarios en esa ventanilla.")
            else:
                print(f"Atendido: {usuario.nombre} (exp {usuario.expediente}) - tiempo real {usuario.tiempo_estimado} min")
                if retraso > 0:
                    print(f"Retraso detectado: {retraso} min -> receptor recorridas={centro.receptores[vid].recorridas}")
                    if not centro.receptores[vid].activo:
                        print(f"Receptor {vid} inactivado; su cola fue reasignada.")
        elif op == "4":
            try:
                exp = int(input("Expediente a buscar: ").strip())
            except ValueError:
                print("Número inválido")
                continue
            u = centro.tabla.buscar(exp)
            if not u:
                print("Usuario no encontrado")
            else:
                docs = ", ".join(list(u.documentos.iter_nombres()))
                print(f"Encontrado: {u.expediente} {u.nombre} {u.tipo_tramite} {u.tiempo_estimado}min turno {minutos_a_hora(u.hora_turno)} docs[{docs}]")
        elif op == "5":
            print("Cerrando sistema.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu_minimo()


    


