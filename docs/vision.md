# Visión: The Telnet Tales

## Idea en una frase
Resucitar los juegos "door" de las BBS de los años 80 y darles un narrador de IA,
sin perder lo que los hacía especiales: 80 columnas, módem lento y un SysOp
caprichoso que puede cortarte la llamada en mitad de un combate.

## Categoría del hackathon
Kiroween 2026, categoría **Resurrection**. Se construye entre el 30 de octubre
y el 4 de diciembre de 2026. No hay código previo.

## Para quién
- Jurado del hackathon: prueba el juego desde una URL (terminal web).
- Nostálgicos de las BBS: se conectan con `telnet` o `nc`.
- Desarrolladores: ejemplo de LLM acotado por un motor determinista.

## Qué lo hace distinto (innovación)
1. **El LLM nunca cambia el estado.** Solo narra y propone; el motor decide.
2. **Caída de portadora:** el SysOp corta la conexión en combate, el estado se
   guarda y al reconectar la partida continúa.
3. **Funciona sin LLM.** Un narrador offline determinista permite tests y demo
   resistente a fallos de red o de API.
4. **Latencia simulada** (2400 baudios) solo en la capa de salida.

## Criterios de éxito
| Criterio del jurado | Qué lo demuestra |
|---|---|
| Impacto potencial | Patrón reutilizable: LLM acotado por reglas deterministas |
| Implementación técnica | Specs, steering, hooks y tests de propiedades en `.kiro/` |
| Diseño | Estética retro coherente, 80 columnas, temas verde y ámbar |
| Innovación | Caída de portadora y resurrección del formato BBS |
| Presentación | Demo web, vídeo de menos de 3 minutos, README claro |

## Fuera de alcance
Multijugador, cuentas con contraseña, pagos, clientes gráficos.
