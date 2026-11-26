# ADR 0004: Terminal web para el jurado

- Estado: aceptada (detalles en la tarea 14; acceso y alojamiento en ADR 0007)
- Fecha: 2026-11-26

## Contexto
El jurado solo puede probar mediante una URL. Los navegadores no hablan Telnet.

## Decisión
Una página estática con **xterm.js** conectada por **WebSocket** al mismo bucle de
sesión que usa Telnet. Un servidor `asyncio` sirve la página y el WebSocket (biblioteca
`websockets`). La salida va en UTF-8; el tema verde o ámbar se aplica con ANSI de
16 colores, igual que en Telnet.

## Motivos
- Una sola implementación del juego, dos transportes: `server/session.py` no sabe
  cuál está usando.
- xterm.js interpreta ANSI y cajas Unicode, así que la experiencia es idéntica.
- Se puede desplegar en un contenedor con un solo puerto HTTP.

## Alternativas
- ttyd / wetty: delegan en un proceso externo; menos control del limitador de baudios.
- Cliente propio en HTML: reinventa el emulador de terminal.

## Consecuencias
Telnet y web comparten tubería de salida y fachada de sesión (ADR 0008).
Va protegida con login (ADR 0007). Hay que vendorizar xterm.js (licencia MIT) y anotarlo en el README.
