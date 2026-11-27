# ADR 0009: Estado en un Protocol `StateStore` (DynamoDB, memoria y archivo)

- Estado: aceptada; la idea de guardar en GCS queda **reemplazada** por DynamoDB (ADR 0010)
- Fecha: 2026-11-26; actualizada el 2026-11-27

## Contexto
La caída de portadora guarda el estado y el mismo jugador lo retoma. Una Lambda no tiene
disco persistente ni memoria compartida entre invocaciones. Además hacen falta un tope
diario exacto de llamadas LLM y control de intentos de login. Todo eso es estado pequeño.

## Decisión
1. Tres Protocols pequeños, cada uno en su archivo:
   - `SaveStore`: `load(player_id) -> SaveGame | None`, `save(player_id, save_game)`, `delete(player_id)`.
   - `DailyBudget`: `try_consume(day, cap) -> bool` (atómico; nunca pasa del tope).
   - `LoginAttempts`: `register_failure(ip, now)`, `blocked_until(ip, now)` y `reset(ip)`.
2. `StateStore` es la composición de los tres. Hay tres implementaciones:
   - `DynamoStateStore`: **una sola tabla** `PAY_PER_REQUEST` con TTL `ttl`. Claves
     `SAVE#<handle>`, `BUDGET#<YYYY-MM-DD>` y `AUTH#<ip>`. El tope usa `ConditionExpression`.
   - `MemoryStore`: tests y desarrollo.
   - `FileStore`: juego local; un JSON por handle, `.bad` si está corrupto.
3. `boto3` se importa de forma perezosa solo en `DynamoStateStore`. Viene en el runtime
   de Lambda y no se empaqueta. Los tests usan un cliente falso, sin red.
4. Se elige con `STATE_TABLE_NAME`: con valor, DynamoDB; vacío, `FileStore`.
5. Las partidas llevan TTL (por ejemplo 30 días); un guardado caducado equivale a no existir.

## Motivos
- Protocols pequeños: el motor y la sesión no saben dónde viven los datos.
- El contador atómico elimina el límite antiguo de Cloud Run (contador en memoria que se reiniciaba).
- Con Lambda sin estado, el guardado es lo único que une dos peticiones del mismo jugador.

## Consecuencias
Propiedades P11, P17 (ida y vuelta, `delete` idempotente), P15 (el tope no se supera ni con
incrementos concurrentes en la implementación en memoria) y P16 (bloqueo monótono).
Tareas 11 y 14.1; requisitos R10 y R13.
