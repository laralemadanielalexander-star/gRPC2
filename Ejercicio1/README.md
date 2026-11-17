# Ejercicio 1 — gRPC Unario

Servicio `ValidadorPagos` con método `VerificarTransaccion`.

Genera el código Python desde `pagos.proto`:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pagos.proto
```

Inicia `python servidor_pagos.py` y, en otra terminal, `python cliente_pagos.py`.

Casos: TX-001 aprobado; TX-002 `INVALID_ARGUMENT`; TX-003 `PERMISSION_DENIED`; TX-004 rechazado por política; TX-005 aprobado.
