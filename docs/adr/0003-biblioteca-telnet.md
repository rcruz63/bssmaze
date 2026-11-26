# ADR 0003: Biblioteca para el servidor Telnet

- Estado: aceptada (revisable en la tarea 8)
- Fecha: 2026-11-26

## Contexto
`telnetlib` salió de la biblioteca estándar en Python 3.13, y de todos modos era
solo un cliente. Hay que servir clientes reales (`telnet`, `nc`) y negociar opciones.

## Opciones
| Opción | A favor | En contra |
|---|---|---|
| `telnetlib3` 5.x (licencia ISC, asyncio, activa: versión 5.0.3 publicada en nov. 2026) | Negocia ECHO, SGA, NAWS, TTYPE y CHARSET; encaja con `asyncio` | Dependencia nueva; API propia |
| `asyncio` puro | Sin dependencias, control total | Hay que implementar IAC, subnegociación y eco; riesgo de errores en 4 días |

## Decisión
Usar **telnetlib3** detrás de un adaptador fino en `server/telnet.py`. El resto del
código solo ve un lector y un escritor de texto, así se puede cambiar de biblioteca
sin tocar el motor. Respaldo: modo "raw" `asyncio` si telnetlib3 diera problemas.

## Consecuencias
- Detectamos ancho de ventana (NAWS) pero se fuerza el límite de 80 columnas.
- El juego debe funcionar también con `nc` (sin negociación): el adaptador no la exige.
