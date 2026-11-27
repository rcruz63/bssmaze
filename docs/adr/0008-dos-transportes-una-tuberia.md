# ADR 0008: Dos transportes, una sola tubería de salida

- Estado: aceptada; el segundo transporte pasa de WebSocket a **manejador Lambda HTTP** (ADR 0010)
- Fecha: 2026-11-26; actualizada el 2026-11-27

## Contexto
El jurado juega en el navegador (xterm.js) y los puristas con `telnet`. Si cada
transporte formateara su salida, las dos experiencias se separarían con el tiempo.

## Decisión
1. `render/pipeline.py` es la única función que convierte una vista en bytes
   (80 columnas, ANSI de 16 colores, cajas, i18n, CRLF).
2. La fachada de sesión (`server/session.py`) no conoce el transporte. El adaptador Telnet
   local (con el protocolo `Transport`) y el manejador Lambda
   (`server/lambda_handler.py`, delgado) solo mueven bytes y añaden su propio marco.
3. El aspecto CRT, el saludo falso de Telnet y el **ritmo de baudios del navegador** viven
   solo en el frontend (CSS y JS). En Telnet local, `render/throttle.py` retrasa la escritura.
   Ninguno cambia los bytes.
4. La propiedad P14 y un archivo dorado comprueban que, con la misma semilla y el mismo
   guion de órdenes, el adaptador Telnet y el manejador Lambda emiten bytes idénticos.

## Motivos
Un solo código que probar, y lo que ve el jurado es lo que se ve en Telnet.

## Consecuencias
Tareas 6.5, 7, 9.2, 14.2, 14.4, 14.7 y 14.8; requisitos R6.5, R6.6, R7.5 a R7.7.
