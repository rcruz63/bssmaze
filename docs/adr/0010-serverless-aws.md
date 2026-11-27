# ADR 0010: Despliegue serverless en AWS (decisión paraguas)

- Estado: aceptada (reemplaza a la ADR 0007 como camino principal; ver también 0006 y 0009)
- Fecha: 2026-11-27

## Contexto
El jurado solo prueba con una URL y un LLM público gasta crédito. El usuario y el bot
Crew compararon tres caminos: Cloud Run (la ADR 0007 original), una instancia Lightsail
y una arquitectura serverless en AWS. El usuario eligió **serverless en AWS**.

Motivo, dicho con honestidad: Kiro es un producto de AWS y el usuario tiene créditos de
AWS. **El hackathon no da ningún bonus por usar AWS**; es una razón de relato (coherencia
con Kiro), no de puntuación.

## Decisión
Arquitectura: S3 + CloudFront (terminal web estática, xterm.js) + API Gateway **HTTP API**
+ Lambda (Python 3.12, arm64) + DynamoDB + Amazon Bedrock. Telnet real queda en local.
Cuatro decisiones técnicas fijas:

1. **HTTP API, no WebSockets.** `POST /api/command`. El juego es por turnos
   (petición y respuesta), la Lambda no guarda estado y no hay `connectionId`.
   - El efecto de baudios lo pinta el **navegador**: xterm.js reparte los bytes con
     el ritmo `baud / 10` en el cliente. El servidor nunca duerme para simular baudios.
   - La respuesta lleva el texto ya formateado (80 columnas, ANSI) y metadatos pequeños
     (`baud`, `carrier_dropped`, `ending`). El saludo falso de Telnet
     (`Trying... Connected to ... Escape character is '^]'`) es sabor del cliente.
   - Mismo origen: CloudFront sirve lo estático desde S3 y enruta `/api/*` al HTTP API.
     No hay CORS.
   - Caída de portadora: el motor la decide y la respuesta trae `carrier_dropped`. El cliente
     muestra `NO CARRIER` y se desconecta; el siguiente login retoma el guardado.
2. **DynamoDB, una sola tabla**, bajo demanda (`PAY_PER_REQUEST`), con atributo TTL `ttl`.
   Guarda: partidas `SAVE#<handle>`, contador diario atómico `BUDGET#<YYYY-MM-DD>` (con
   `ConditionExpression`: tope global exacto) e intentos de login `AUTH#<ip>` (bloqueo
   progresivo con TTL). En local y en tests: `MemoryStore` y `FileStore` con las mismas
   interfaces. Detalle en la ADR 0009. La identidad entre peticiones es un **token HMAC
   firmado y de vida corta** que devuelve el login; el secreto viene de env o SSM.
3. **Paquete .zip hecho con uv**, sin imagen ECR, mientras las dependencias sean ligeras
   (`pydantic`, `pyyaml`; `boto3` ya viene en el runtime de Lambda y no se empaqueta).
   Plataforma `aarch64-manylinux2014`. Infraestructura como código: una plantilla **AWS SAM**
   (`infra/template.yaml`) con Lambda, HTTP API, tabla, bucket S3, CloudFront y alerta de AWS Budgets.
   Despliegue con `sam deploy` (guía en `docs/despliegue-aws.md`). El objetivo `make package`
   lo crea la tarea 14.3.
4. **Telnet real sigue en local**: el adaptador TCP (tarea 7) usa el mismo motor y el mismo
   `render/pipeline.py` para el vídeo y el juego local. **No se despliega.** La propiedad
   P14 (paridad de bytes entre el adaptador Telnet y el manejador Lambda, misma semilla y
   mismo guion) y un test dorado se mantienen.

## Qué debe hacer cada parte
- **Usuario:** aportar credenciales o perfil de AWS (`aws configure sso` en su terminal, nunca
  en el repositorio), elegir región y **activar el acceso a modelos de Bedrock** en esa región.
- **Crew:** escribir plantilla, código y docs; comprobar ids de modelo con el comando de listado.

## Alternativas conservadas
- **Cloud Run:** contenedor único con WebSocket. Válido y simple, pero ata la sesión al
  proceso, necesita contador en memoria (se reinicia) y no usa los créditos de AWS.
- **Lightsail:** una instancia con el mismo código y Telnet real abierto. Plan B (abajo).

## Compromisos y riesgos
| Tema | Efecto | Mitigación |
|---|---|---|
| Arranque en frío | 1 a 3 s en la primera petición tras inactividad | Dependencias ligeras, zip, arm64; el cliente muestra el módem "marcando" |
| Turnos con LLM | Bedrock puede tardar | Límite de 8 s, luego narrador offline |
| Más piezas de AWS | Más puntos de fallo | Despliegue de humo temprano |
| Coste | Pago por uso; sin tráfico cuesta casi cero | Topes diarios y por sesión, AWS Budgets |
| Sin Telnet en la nube | El jurado no prueba Telnet | Se muestra en vídeo y en local |

## Plan de respaldo
- **Sáb 28 nov:** despliegue de humo (tarea S1): Lambda hola-mundo + HTTP API + CloudFront +
  DynamoDB con SAM.
- **Si el despliegue serverless no funciona el dom 29 nov:** se pasa a una instancia
  **Lightsail** con el mismo código (adaptador HTTP local más Telnet), sin cambiar motor ni render.

## Consecuencias
Reemplaza el requisito R13.8 (Cloud Run). Cambia R6 y R7 (transportes), R13 y las tareas
S1, 7, 11, 13 y 14. ADR 0004 y 0008 se actualizan: el web ya no usa WebSocket.
