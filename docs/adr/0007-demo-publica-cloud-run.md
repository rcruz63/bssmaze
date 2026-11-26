# ADR 0007: Demo pública en Google Cloud Run con acceso protegido

- Estado: aceptada
- Fecha: 2026-11-26

## Contexto
El jurado solo prueba mediante una URL. Un LLM público sin protección permitiría que
desconocidos gasten el presupuesto.

## Decisión
1. La demo pública es **solo la terminal web** (xterm.js sobre WebSocket, ADR 0004).
2. Va protegida con **usuario y contraseña** (variables de entorno). Las credenciales se
   entregan en el campo *testing instructions* de Devpost, visible solo para patrocinador y jurado.
3. Alojamiento en **Google Cloud Run**: escala a cero, `max-instances 1`, soporta
   WebSocket, alerta de presupuesto. Los créditos de GCP cubren también Gemini.
4. Cloud Run no sirve TCP crudo: el **Telnet real** se muestra en local y en el vídeo.
   Extra opcional más adelante: una VM pequeña con puerto Telnet.
5. Límites: tope de llamadas LLM por sesión y por día, con respaldo al narrador offline;
   límite de intentos de login por dirección (esperas crecientes y bloqueo temporal),
   comparación de credenciales en tiempo constante y pantalla de login dentro de la ficción BBS.
6. **AWS** (hay créditos) queda documentado como alternativa equivalente.

## Motivos
- Con una sola instancia, el contador diario en memoria es suficiente y simple.
- Escalar a cero evita coste fuera de la evaluación.

## Consecuencias
Con una instancia, un reinicio pone el contador diario a cero; es un límite aceptado
(`shortcut`) y la alerta de presupuesto de GCP es la segunda barrera.
Tareas 7.4, 13.5 y 14.3 a 14.8; requisitos R13.
