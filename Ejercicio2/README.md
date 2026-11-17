# Ejercicio 2 — gRPC Server Streaming

Servicio `MonitorCadenaFrio` con método `TransmitirTelemetria`.

Genera el código Python desde `telemetria.proto`:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. telemetria.proto
```

Inicia `python servidor_telemetria.py` y, en otra terminal, `python cliente_telemetria.py`.

El cliente recibe lecturas continuamente usando `for respuesta in stub.TransmitirTelemetria(peticion)`. El servidor utiliza `yield` y marca alerta si la temperatura es menor a 2 °C o mayor a 8 °C. `CAM-999` produce `NOT_FOUND`.
