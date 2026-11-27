# ADR 0004: Terminal web para el jurado

- Estado: aceptada; el transporte WebSocket fue **reemplazado por HTTP** (ADR 0010)
- Fecha: 2026-11-26; actualizada el 2026-11-27

## Contexto
El jurado solo puede probar mediante una URL. Los navegadores no hablan Telnet.

## Decisión
Una página estática con **xterm.js** (en S3, servida por CloudFront) que llama a
`POST /api/command` en un API Gateway HTTP API. Cada orden es una petición y una respuesta;
no hay conexión viva. La respuesta trae el texto ya formateado (ANSI de 16 colores, 80 columnas)
y metadatos pequeños. El tema verde o ámbar se aplica con ANSI, igual que en Telnet.
El cliente pinta los bytes con el ritmo de baudios y muestra el saludo falso de Telnet.

## Motivos
- Una sola implementación del juego, dos transportes: la fachada de sesión no sabe cuál usa.
- El juego es por turnos: HTTP sin estado encaja con Lambda y evita `connectionId`.
- xterm.js interpreta ANSI y cajas Unicode, así que la experiencia es idéntica a `nc`.
- Mismo origen (CloudFront enruta `/api/*`): sin CORS.

## Alternativas
- WebSocket (API Gateway o servidor propio): innecesario para turnos; más piezas y estado.
- ttyd / wetty: delegan en un proceso externo; menos control del ritmo de baudios.
- Cliente propio en HTML: reinventa el emulador de terminal.

## Consecuencias
Telnet y web comparten tubería de salida y fachada de sesión (ADR 0008).
Va protegida con login y token firmado (ADR 0007, 0010). Hay que vendorizar xterm.js
(licencia MIT) y anotarlo en el README.
