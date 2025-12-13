
DOCUMENTOS = ("Acta", "RFC", "CURP", "INE", "Comprobante de pago")  
T_DOC = 5       # Tiempo para tramite documentos basicos 
T_SIMPLE = 10     # tiempo para tramites simples
T_COMPLEJO = 20     # tiempo tramites complejos
T_PAGOS = 5        # tiempo maximo para entrega de pagos 
MAX_TURNO = 5        # Incremento maximo en minutos
MAX_MAL_SERVICIO = 3  # Retrasos tolerados 



# nodo para listas enlazadas # guardar elemento y saber cual es el siguente en la fila 
class Nodo:
   
   
    def __init__(self, valor):
        self.v = valor
        self.sig = None



# cola ordenada por pioridad osea el mejor caso va a el inicio y el peor a el final 
class ColaOrdenada:
   
   
   
    def __init__(self):
        self.ini = None  # Nodo con turno más bajo

    def insertar(self, par): # inserta un cliente manteniendo oreden por turno 
      
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

    def pop_min(self): #Elimina y retorna el cliente con turno mas bajo o none para lista vacia 
        
        if not self.ini:
            return None
        v = self.ini.v
        self.ini = self.ini.sig
        return v

    def mostrar(self): # Regresa la lista de clientes en orden de turno.

        a = self.ini
        res = []
        while a:
            res.append(a.v)
            a = a.sig
        return res


# Hash table simple para clientes
class HashNode:
    def __init__(self, k, v):
        self.k = k
        self.v = v
        self.sig = None

class Hash: # esta classe permite la busqueda rapida de clientes 

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

# Clase para receptores de ventanilla mantener estado de cada ventanilla y numero de retrasos 
class Receptor:

    def __init__(self, nombre):
        self.nombre = nombre
        self.mal_servicio = 0
        self.ocupado_hasta = 0
 
 
 
# Ventanillas iniciales
ventanillas = {
    "v1": Receptor("v1 Entrega / revision de documentos"),
    "v2": Receptor("v2 Tramites simples"),
    "v3": Receptor("v3 Trámites complejos"),
    "v4": Receptor("v4 Pagos"),
}

cola_prio = ColaOrdenada()
tabla = Hash()


def buscar_ventanilla_libre(turno):
    for v in ventanillas.values():
        if v.ocupado_hasta <= turno: #----------------------------------------------modificacion para  reubicar a ventanilla
            return v
    return None





# Registro de cliente asigna tiempo y ventanilla segun el tipo de cada tramite inserta en cola y hash
def registrar(cliente):

    nombre, tipo, docs, turno, hora, receptor_nombre = cliente
    if tipo == "doc": t = T_DOC; vent = ventanillas["v1"]
    elif tipo == "simple": t = T_SIMPLE; vent = ventanillas["v2"]
    elif tipo == "complejo": t = T_COMPLEJO; vent = ventanillas["v3"]
    else: t = T_PAGOS; vent = ventanillas["v4"]

    cola_prio.insertar((nombre, tipo, t, turno, hora, docs, vent))
    tabla.set(nombre, (tipo, t, turno, hora, docs, vent))
    return t


# Snapshot de clientes se modifica para hacerlo mas entendible 
def snapshot():
    res = []
    for nombre, tipo, tiempo, turno, hora, docs, ventanilla in cola_prio.mostrar():
        res.append(
            f"Turno {turno} | {nombre} | {tipo.upper()} | Ventanilla: {ventanilla.nombre}"
        )
    return res



# Atención de clientes se modifica para oprimisar colas y que los clientes sean distribuidos a ventanillas desocupadas
def atender_clientes():



    print("\n--- Atención de clientes -----" )
    while True:
        cliente = cola_prio.pop_min()
        if not cliente:
            print("no hay clientes en espera")
            break
        nombre, tipo, t, turno, hora, docs, receptor = cliente
        

        if receptor.ocupado_hasta > turno:
        
            alternativa = buscar_ventanilla_libre(turno)

            if alternativa:
                print(f"Cliente {nombre} reasignado a {alternativa.nombre}")
                alternativa.ocupado_hasta = turno + t

            else:
                turno += MAX_TURNO
                print(f"Cliente {nombre} retrasado, nuevo turno {turno}")

                receptor.mal_servicio += 1
                if receptor.mal_servicio > MAX_MAL_SERVICIO:
                    print(f"{receptor.nombre} removido por mal servicio se asigna nuevo ")
                    receptor.mal_servicio = 0

            cola_prio.insertar((nombre, tipo, t, turno, hora, docs, receptor))

        else:
            receptor.ocupado_hasta = turno + t
            print(f"Cliente {nombre} atendido en {receptor.nombre} durante {t} minutos")


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
        turno_input = int(input("Ingresar el numero de turno a buscar : "))
    except ValueError:
        print("Turno invalido por favor ingrese un numero correcto.")
        return
    cliente = buscar_por_turno(turno_input)
    if cliente:
        print(f"Cliente encontrado: Turno {cliente[3]} - Nombre: {cliente[0]}, Tipo: {cliente[1]}, Tiempo: {cliente[2]} min, Hora: {cliente[4]}, Documentos: {cliente[5]}, Receptor: {cliente[6]}")
    else:
        print(f"No se encontro ningun cliente con turno  {turno_input}")







