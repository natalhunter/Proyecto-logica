# Menu aqui no se almacena ningun dato #
# importamos funciones desde el archivo logica.py
import logica 

# Lista para documentos para realizar cualquer tramite

DOCUMENTOS_REQUERIDOS = [
    "Acta de nacimiento",
    "RFC",
    "CURP",
    "INE"
]


def validar_documentos():
    print("\n📄 **Documentacion necesaria para realizar cualquier tramite :**")
    for doc in DOCUMENTOS_REQUERIDOS:
        print(f"- {doc}")

    print("\nSolo responde si o no:")

    for doc in DOCUMENTOS_REQUERIDOS:
        respuesta = input(f"¿Trae {doc}? ").strip().lower()
        if respuesta != "si":
            print(f"\nNo puede continuar falta: {doc}")
            print("Por favor regreselo Por sus Documentos.\n")
            return False

    print("\n Admitido. Todos los documentos estan completos.")
    return True



def registrar_cliente(turno):
    print("\n--- Registrar Cliente ---")
    nombre = input("Nombre del cliente: ")

    # En esta seccion se  validan los documentos 
    if not validar_documentos():
        return turno  # No puede seguir al trámite

    print("\nSeleccione el tipo de tramite:")
    print("1) Entrega de documentos")
    print("2) Tramite simple")
    print("3) Tramite complejo")
    print("4) Pagos")

    opcion = input("Opcion: ")

   
    tipo = {
        "1": "doc",
        "2": "simple",
        "3": "complejo",
        "4": "pago"
    }.get(opcion, "pago")

    hora = ""  # esta linea se deshabilita, se implementa que la hora se inserte de manera automatica 

    #en esta linea se mandan la informacion a logica.py
    
    logica.registrar((nombre, tipo, DOCUMENTOS_REQUERIDOS, turno, hora, ""))

    print(f"Cliente registrado con turno {turno}")
    return turno + 1


def ver_colas():
    print("\n------- Turnos en espera -----")
    for linea in logica.snapshot(): #lee directamente la cola enlazada
        print(linea)


def atender_cliente():
    logica.atender_clientes()


# ''''''''''Menu''''''''''

turno = 13 

while True:
    print("\n------Sistema De Tramites--------")
    print("1) Registrar cliente")
    print("2) Ver colas")
    print("3) Atender cliente")
    print("4) Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        turno = registrar_cliente(turno)
    elif opcion == "2":
        ver_colas()
    elif opcion == "3":
        atender_cliente()
    elif opcion == "4":
        print("Bye Bye...")
        break
    else:
        print("Opcion Invalida.")


