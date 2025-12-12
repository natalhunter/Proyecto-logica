# Sistema de Ventanillas con Colas y Hash en Python

## Descripción
Este proyecto simula un sistema de ventanillas para atención de clientes, utilizando estructuras de datos clásicas: **colas simples**, **pilas**, **colas ordenadas** y **tabla hash**.  
Permite registrar clientes, asignar turnos, gestionar documentos, y consultar la información de forma organizada y eficiente.

El sistema incluye un **menú interactivo** para:

- Registrar clientes con tipo, documentos y receptor.
- Mostrar un **snapshot** ordenado por turno.
- Consultar clientes en la **tabla hash**.
- Salir del sistema.

---

## Estructura del Código

- `Nodo`: Clase genérica para listas enlazadas.
- `Cola`: Cola simple para gestionar ventanillas.
- `Pila`: Pila simple para operaciones LIFO.
- `ColaOrdenada`: Cola con inserción ordenada por turno.
- `Hash` y `HashNode`: Tabla hash simple para almacenar información de clientes.
- `registrar(cliente)`: Registra un cliente asignándole tiempo según tipo y lo añade a la cola correspondiente.
- `snapshot()`: Devuelve una lista de clientes ordenados por turno.
- `menu()`: Menú interactivo principal para operar el sistema.

---

## Instalación

1. Asegúrate de tener Python 3 instalado.
2. Clona o descarga el repositorio.
3. Ejecuta el programa:

```bash
python proyectofinal_entrega_documentación.py

