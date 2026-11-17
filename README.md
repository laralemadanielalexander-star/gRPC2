# gRPC2 — Programación Distribuida

Repositorio de dos ejercicios gRPC en Python.

- **Ejercicio 1 (Unario):** validación de pagos y detección de fraude.
- **Ejercicio 2 (Server Streaming):** telemetría IoT de camiones de cadena de frío.

## Instalación

Desde la carpeta raíz del repositorio:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ejercicio 1

```bash
cd Ejercicio1
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pagos.proto
python servidor_pagos.py
```

En otra terminal, activa el mismo entorno y ejecuta:

```bash
cd Ejercicio1
python cliente_pagos.py
```

Pruebas: TX-001 aprobada, TX-002 error `INVALID_ARGUMENT`, TX-003 error `PERMISSION_DENIED`, TX-004 rechazada por política, TX-005 aprobada.

## Ejercicio 2

Detén el servidor del Ejercicio 1 porque ambos usan el puerto 50051.

```bash
cd Ejercicio2
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. telemetria.proto
python servidor_telemetria.py
```

En otra terminal, activa el mismo entorno y ejecuta:

```bash
cd Ejercicio2
python cliente_telemetria.py
```

Prueba `CAM-001` o `CAM-002` con intervalo de 2 segundos. Para verificar el manejo de errores, ingresa `CAM-999` (`NOT_FOUND`).

## Notas

Los archivos `*_pb2.py` y `*_pb2_grpc.py` se generan con Protobuf. No se versionan los entornos virtuales ni las cachés de Python. El código es educativo y no procesa pagos reales; no incluye TLS ni medición de latencia.
