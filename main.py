import os
from models import Encomienda, Destino, CategoriaPeso, TipoServicio, Cliente
from clientes_repo import RepoClientes
from estrategias import (
    CalculoBaseStrategy,
    RecargosServiciosStrategy,
    CalculoIvaStrategy,
    CotizadorService
)


def main():
    print(">> [INICIO] Arrancando aplicación...")

    # Inicializamos dependencias
    repo_clientes = RepoClientes()
    cotizador = CotizadorService([
        CalculoBaseStrategy(),
        RecargosServiciosStrategy(),
        CalculoIvaStrategy()
    ])

    while True:
        print("\n========================================")
        print("    SISTEMA DE LOGÍSTICA - MENÚ PRINCIPAL")
        print("========================================")
        print("1. Registrar nuevo cliente")
        print("2. Cotizar nueva encomienda")
        print("3. Salir")

        opcion = input("\nSeleccione una opción (1-3): ").strip()

        if opcion == "1":
            print("\n--- REGISTRO DE CLIENTE ---")
            dni = input("DNI: ").strip()
            nombre = input("Nombre y Apellido: ").strip()
            contacto = input("Contacto (Email/Teléfono): ").strip()

            try:
                cliente = Cliente(dni=dni, nombre=nombre, contacto=contacto)
                repo_clientes.save(cliente)
                print(f">> ¡Éxito! Cliente {nombre} guardado correctamente.")
            except Exception as e:
                print(f">> Error al guardar el cliente: {e}")

        elif opcion == "2":
            print("\n--- COTIZACIÓN DE ENCOMIENDA ---")
            dni = input("DNI del cliente remitente: ").strip()

            try:
                cliente = repo_clientes.find_by_dni(dni)
                print(f">> Cliente verificado: {cliente.nombre}")

                print(
                    "\nDestinos disponibles: CABA, GBA_NORTE, GBA_SUR, INTERIOR")
                dest_input = input("Ingrese destino: ").strip().upper()
                destino = Destino[dest_input]

                print("\nCategorías de peso: LIVIANO, MEDIO, PESADO")
                peso_input = input("Ingrese peso: ").strip().upper()
                peso = CategoriaPeso[peso_input]

                print("\nServicios extra disponibles: URGENTE, FRAGIL, EXPRESS")
                serv_input = input(
                    "Ingrese servicios separados por coma (o presione Enter para ninguno): ").strip()

                servicios = []
                if serv_input:
                    nombres_servicios = [s.strip().upper() for s in
                                         serv_input.split(",")]
                    servicios = [TipoServicio[s] for s in nombres_servicios if
                                 s in TipoServicio.__members__]

                encomienda = Encomienda(
                    cliente_id=cliente.id,
                    destino=destino,
                    peso=peso,
                    servicios=servicios
                )

                cotizacion = cotizador.calcular_costo(encomienda)

                print("\n" + "=" * 40)
                print("           RESULTADO DE COTIZACIÓN")
                print("=" * 40)
                print(f"Tracking ID: {encomienda.tracking_id}")
                print(f"Subtotal (Zona + Peso): ${cotizacion.subtotal:.2f}")
                print(f"Recargos por servicios:  ${cotizacion.recargos:.2f}")
                print(f"IVA (21%):               ${cotizacion.iva:.2f}")
                print(f"TOTAL A PAGAR:           ${cotizacion.total:.2f}")
                print("=" * 40)

            except KeyError:
                print(
                    ">> Error: Ingresaste una opción de destino, peso o servicio que no es válida.")
            except Exception as e:
                print(f">> Error: {e}")

        elif opcion == "3":
            print("\n¡Gracias por usar el sistema de logística! Saliendo...")
            break
        else:
            print(
                ">> Opción no válida. Por favor, elegí un número entre 1 y 3.")


if __name__ == "__main__":
    main()
