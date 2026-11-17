import grpc
from concurrent import futures
import uuid
import pagos_pb2
import pagos_pb2_grpc


class ValidadorPagos(pagos_pb2_grpc.ValidadorPagosServicer):
    def VerificarTransaccion(self, request, context):
        print("\n====================================")
        print("NUEVA TRANSACCION RECIBIDA")
        print("====================================")
        print(f"ID: {request.id_transaccion}")
        print(f"Monto: {request.monto}")
        print(f"Moneda: {request.codigo_moneda}")
        print(f"Pais: {request.pais_origen}")

        tarjeta = request.numero_tarjeta
        monto = request.monto
        pais = request.pais_origen.upper()

        if monto <= 0 or not tarjeta.isascii() or not tarjeta.isdecimal() or len(tarjeta) != 16:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Monto o número de tarjeta inválido")
            print("ERROR: Argumentos invalidos")
            return pagos_pb2.ResultadoPago(aprobado=False, codigo_autorizacion="", motivo_rechazo="Datos invalidos")

        if tarjeta.startswith("4000"):
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Tarjeta bloquada por fraude")
            print("ERROR: Tarjeta bloqueada por fraude")
            return pagos_pb2.ResultadoPago(aprobado=False, codigo_autorizacion="", motivo_rechazo="Tarjeta bloqueada")

        if monto > 10000 and pais not in ["US", "MX"]:
            print("RECHAZADO: Politica de fraude")
            return pagos_pb2.ResultadoPago(
                aprobado=False, codigo_autorizacion="",
                motivo_rechazo="Monto superior a 10000 USD desde un pais no autorizado"
            )

        codigo = str(uuid.uuid4())[:8].upper()
        print("TRANSACCION APROBADA")
        print(f"Codigo de autorizacion: {codigo}")
        return pagos_pb2.ResultadoPago(aprobado=True, codigo_autorizacion=codigo, motivo_rechazo="")


def iniciar_servidor():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pagos_pb2_grpc.add_ValidadorPagosServicer_to_server(ValidadorPagos(), servidor)
    puerto = 50051
    servidor.add_insecure_port(f"[::]:{puerto}")
    servidor.start()
    print("====================================")
    print(" SERVIDOR DE VALIDACION DE PAGOS")
    print("====================================")
    print(f"Servidor activo en puerto {puerto}")
    print("Esperando transacciones...")
    print("====================================")
    try:
        servidor.wait_for_termination()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        servidor.stop(0)


if __name__ == "__main__":
    iniciar_servidor()
