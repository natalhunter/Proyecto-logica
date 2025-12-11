# Menú Principal #

# Documentos requeridos para cualquier trámite
DOCUMENTOS_REQUERIDOS = [
    "Acta de nacimiento",
    "RFC",
    "CURP",
    "INE"
]

# Colas por ventanilla
ventanilla1 = []   # Entrega de documentos
ventanilla2 = []   # Trámite simple
ventanilla3 = []   # Trámite complejo
ventanilla4 = []   # Pagos

TIEMPOS = {
    "documentos": 5,
    "simple": 10,
    "complejo": 20,
    "pagos": 8
}


def validar_documentos():
    print("\n📄 **Documentos obligatorios para realizar un trámite:**")
    for doc in DOCUMENTOS_REQUERIDOS:
        print(f"- {doc}")

    print("\nResponde 'si' o 'no' para cada uno:")

    for doc in DOCUMENTOS_REQUERIDOS:
        respuesta = input(f"¿Trae {doc}? ").strip().lower()
        if respuesta != "si":
            print(f"\n❌ No puede continuar. Falta: {doc}")
            print("➡ Por favor regrese al módulo de información.\n")
            return False

    print("\n✔ Todos los documentos están completos.")
    return True


def registrar_cliente():
    print("\n--- Registrar Cliente ---")
    nombre = input("Nombre del cliente: ")

    # Validación de documentos antes de continuar
    if not validar_documentos():
        return  # No puede seguir al trámite

    print("\nSeleccione el tipo de trámite:")
    print("1) Entrega de documentos")
    print("2) Trámite simple")
    print("3) Trámite complejo")
    print("4) Pagos")

    opcion = input("Opción: ")

    if opcion == "1":
        ventanilla1.append(nombre)
        print(f"✔ {nombre} enviado a VENTANILLA 1.")
        print(f"⏱ Tiempo estimado: {TIEMPOS['documentos']} min")

    elif opcion == "2":
        ventanilla2.append(nombre)
        print(f"✔ {nombre} enviado a VENTANILLA 2.")
        print(f"⏱ Tiempo estimado: {TIEMPOS['simple']} min")

    elif opcion == "3":
        ventanilla3.append(nombre)
        print(f"✔ {nombre} enviado a VENTANILLA 3.")
        print(f"⏱ Tiempo estimado: {TIEMPOS['complejo']} min")

    elif opcion == "4":
        ventanilla4.append(nombre)
        print(f"✔ {nombre} enviado a VENTANILLA 4.")
        print(f"⏱ Tiempo estimado: {TIEMPOS['pagos']} min")

    else:
        print("❌ Opción inválida.")


def ver_colas():
    print("\n--- Estado de las ventanillas ---")
    print(f"Ventanilla 1 (Documentos): {ventanilla1}")
    print(f"Ventanilla 2 (Simple): {ventanilla2}")
    print(f"Ventanilla 3 (Complejo): {ventanilla3}")
    print(f"Ventanilla 4 (Pagos): {ventanilla4}")


def atender_cliente():
    print("\n--- Atender Cliente ---")
    print("1) Ventanilla 1")
    print("2) Ventanilla 2")
    print("3) Ventanilla 3")
    print("4) Ventanilla 4")

    op = input("Selecciona ventanilla: ")

    if op == "1" and ventanilla1:
        print(f"✔ Atendiendo a {ventanilla1.pop(0)}")

    elif op == "2" and ventanilla2:
        print(f"✔ Atendiendo a {ventanilla2.pop(0)}")

    elif op == "3" and ventanilla3:
        print(f"✔ Atendiendo a {ventanilla3.pop(0)}")

    elif op == "4" and ventanilla4:
        print(f"✔ Atendiendo a {ventanilla4.pop(0)}")

    else:
        print("❌ No hay clientes en esta ventanilla.")


def tiempo_estimado():
    print("\n--- Tiempos de Espera ---")
    print(f"Ventanilla 1: {len(ventanilla1) * TIEMPOS['documentos']} min")
    print(f"Ventanilla 2: {len(ventanilla2) * TIEMPOS['simple']} min")
    print(f"Ventanilla 3: {len(ventanilla3) * TIEMPOS['complejo']} min")
    print(f"Ventanilla 4: {len(ventanilla4) * TIEMPOS['pagos']} min")


# ================================
# MENÚ PRINCIPAL
# ================================
while True:
    print("\n====== SISTEMA DE TRÁMITES ======")
    print("1) Registrar cliente")
    print("2) Ver colas")
    print("3) Atender cliente")
    print("4) Ver tiempo estimado")
    print("5) Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        registrar_cliente()
    elif opcion == "2":
        ver_colas()
    elif opcion == "3":
        atender_cliente()
    elif opcion == "4":
        tiempo_estimado()
    elif opcion == "5":
        print("Saliendo del sistema...")
        break
    else:
        print("❌ Opción inválida.")

