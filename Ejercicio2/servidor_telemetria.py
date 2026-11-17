import grpc
from concurrent import futures
import time
import random
from datetime import datetime
import telemetria_pb2
import telemetria_pb2_grpc

CAMIONES = {
    "CAM-001": {"latitud": -0.1807, "longitud": -78.4678},
    "CAM-002": {"latitud": -2.1709, "longitud": -79.9224},
}


class MonitorCadenaFrio(telemetria_pb2_grpc.MonitorCadenaFrioServicer):
    def TransmitirTelemetria(self, request, context):
        id_camion = request.id_camion
        intervalo = request.intervalo_segundos
        if id_camion not in CAMIONES:
            context.abort(grpc.StatusCode.NOT_FOUND, f"El camion {id_camion} no existe")
        if intervalo <= 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "El intervalo debe ser mayor a cero")

        print(f"\nCliente suscrito al camion: {id_camion}")
        print(f"Intervalo: {intervalo} segundos")
        while context.is_active():
            temperatura = round(random.uniform(0, 10), 2)
            latitud = CAMIONES[id_camion]["latitud"]
            longitud = CAMIONES[id_camion]["longitud"]
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            alerta = temperatura < 2.0 or temperatura > 8.0
            lectura = telemetria_pb2.LecturaSensor(
                id_camion=id_camion,
                temperatura_celsius=temperatura,
                latitud=latitud,
                longitud=longitud,
                timestamp=fecha,
                alerta_critica=alerta
            )
            print(f"Camion: {id_camion} | Temperatura: {temperatura} C | Alerta: {alerta}")
            yield lectura
            time.sleep(intervalo)


def iniciar_servidor():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    telemetria_pb2_grpc.add_MonitorCadenaFrioServicer_to_server(MonitorCadenaFrio(), servidor)
    puerto = 50051
    servidor.add_insecure_port(f"[::]:{puerto}")
    servidor.start()
    print("====================================")
    print(" SERVIDOR DE CADENA DE FRIO IoT")
    print("====================================")
    print(f"Servidor activo en puerto {puerto}")
    print("Camiones disponibles:")
    print("CAM-001")
    print("CAM-002")
    print("Esperando conexiones...")
    print("====================================")
    try:
        servidor.wait_for_termination()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        servidor.stop(0)


if __name__ == "__main__":
    iniciar_servidor()
