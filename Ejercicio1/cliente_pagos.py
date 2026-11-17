import grpc
import pagos_pb2
import pagos_pb2_grpc

ROJO = "\033[91m"
VERDE = "\033[92m"
RESET = "\033[0m"


def verificar_pago(stub, id_tx, tarjeta, monto, moneda, pais):
    print("\n====================================")
    print(f"TRANSACCION: {id_tx}")
    print("====================================")
    print(f"Monto: {monto} {moneda}")
    print(f"Pais: {pais}")
    print(f"Tarjeta: **** **** **** {tarjeta[-4:]}")
    peticion = pagos_pb2.SolicitudPago(
        id_transaccion=id_tx,
        numero_tarjeta=tarjeta,
        monto=monto,
        codigo_moneda=moneda,
        pais_origen=pais
    )
    try:
        respuesta = stub.VerificarTransaccion(peticion, timeout=5)
        if respuesta.aprobado:
            print(VERDE + "\nPAGO APROBADO" + RESET)
            print("Codigo de autorizacion:", respuesta.codigo_autorizacion)
        else:
            print(ROJO + "\nPAGO RECHAZADO" + RESET)
            print("Motivo:", respuesta.motivo_rechazo)
    except grpc.RpcError as e:
        print(ROJO + "\nERROR gRPC" + RESET)
        print("Codigo:", e.code())
        print("Detalle:", e.details())


def iniciar_cliente():
    print("====================================")
    print(" CLIENTE DE VALIDACION DE PAGOS")
    print("====================================")
    with grpc.insecure_channel("localhost:50051") as canal:
        stub = pagos_pb2_grpc.ValidadorPagosStub(canal)
        verificar_pago(stub, "TX-001", "5111111111111111", 150.00, "USD", "EC")
        verificar_pago(stub, "TX-002", "5111111111111111", -50.00, "USD", "EC")
        verificar_pago(stub, "TX-003", "4000123412341234", 200.00, "USD", "EC")
        verificar_pago(stub, "TX-004", "5111111111111111", 15000.00, "USD", "EC")
        verificar_pago(stub, "TX-005", "5111111111111111", 15000.00, "USD", "US")


if __name__ == "__main__":
    iniciar_cliente()
