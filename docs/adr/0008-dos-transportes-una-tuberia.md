# ADR 0008: Dos transportes, una sola tubería de salida

- Estado: aceptada
- Fecha: 2026-11-26

## Contexto
El jurado juega en el navegador (xterm.js) y los puristas con `telnet`. Si cada
transporte formateara su salida, las dos experiencias se separarían con el tiempo.

## Decisión
1. `render/pipeline.py` es la única función que convierte una vista en bytes
   (80 columnas, ANSI de 16 colores, cajas, i18n, CRLF).
2. `server/session.py` es la única fachada de sesión y solo conoce el protocolo `Transport`.
3. Los adaptadores Telnet y WebSocket solo mueven bytes y añaden su propio marco de protocolo.
4. El aspecto CRT (líneas de barrido, brillo de fósforo, tipografía) vive solo en CSS y JS del frontend.
5. La limitación de baudios solo retrasa; no cambia los bytes.
6. La propiedad P14 y un archivo dorado comprueban que, con la misma semilla y el mismo
   guion de órdenes, ambos adaptadores emiten bytes idénticos.

## Motivos
Un solo código que probar, y lo que ve el jurado es lo que se ve en Telnet.

## Consecuencias
Tareas 6.5, 7.3, 9.2, 14.9 y 14.10; requisitos R6.5, R6.6, R7.5 a R7.7.
