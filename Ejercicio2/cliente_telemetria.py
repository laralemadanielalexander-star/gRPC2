import grpc
import telemetria_pb2
import telemetria_pb2_grpc

ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
RESET = "\033[0m"


def iniciar_cliente():
    print("====================================")
    print(" MONITOR DE CADENA DE FRIO")
    print("====================================")
    print("Camiones disponibles:")
    print("CAM-001")
    print("CAM-002")
    id_camion = input("\nIngrese el ID del camion: ").strip().upper()
    try:
        intervalo = int(input("Intervalo en segundos: "))
    except ValueError:
        print("ERROR: Ingrese un numero entero")
        return

    canal = grpc.insecure_channel("localhost:50051")
    stub = telemetria_pb2_grpc.MonitorCadenaFrioStub(canal)
    peticion = telemetria_pb2.SuscripcionCamion(
        id_camion=id_camion, intervalo_segundos=intervalo
    )
    print("\nConectando con el servidor...")
    print("Presione CTRL + C para detener el monitoreo")
    print("------------------------------------")
    try:
        for respuesta in stub.TransmitirTelemetria(peticion):
            print("\n====================================")
            print(f"Camion: {respuesta.id_camion}")
            print(f"Temperatura: {respuesta.temperatura_celsius:.2f} °C")
            print(f"Latitud: {respuesta.latitud}")
            print(f"Longitud: {respuesta.longitud}")
            print(f"Fecha: {respuesta.timestamp}")
            if respuesta.alerta_critica:
                print(ROJO + "!!! ALERTA CRITICA !!!" + RESET)
                print(ROJO + "Temperatura fuera del rango permitido (2°C - 8°C)" + RESET)
            else:
                print(VERDE + "Temperatura dentro del rango permitido" + RESET)
            print("====================================")
    except grpc.RpcError as error:
        if error.code() in (grpc.StatusCode.NOT_FOUND, grpc.StatusCode.INVALID_ARGUMENT):
            print(ROJO + f"\nERROR: {error.details()}" + RESET)
        else:
            print(ROJO + f"\nError de comunicacion: {error.details()}" + RESET)
    except KeyboardInterrupt:
        print(AMARILLO + "\nMonitoreo detenido por el usuario" + RESET)
    finally:
        canal.close()


if __name__ == "__main__":
    iniciar_cliente()
