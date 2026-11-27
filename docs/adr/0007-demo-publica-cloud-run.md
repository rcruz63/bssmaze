# ADR 0007: Demo pública protegida (serverless en AWS; Cloud Run como alternativa)

- Estado: **reemplazada en su decisión de alojamiento por la ADR 0010** (serverless en AWS).
  Se conserva lo demás: demo solo web, acceso protegido y topes de gasto.
- Fecha: 2026-11-26; actualizada el 2026-11-27

## Contexto
El jurado solo prueba mediante una URL. Un LLM público sin protección permitiría que
desconocidos gasten el presupuesto.

## Decisión (vigente)
1. La demo pública es **solo la terminal web** (xterm.js, HTTP, ADR 0004 y 0010).
2. Va protegida con **usuario y contraseña** (variables de entorno o SSM). Las credenciales
   se entregan en el campo *testing instructions* de Devpost, visible solo para patrocinador y jurado.
3. Alojamiento: **S3 + CloudFront + API Gateway HTTP API + Lambda + DynamoDB** (ADR 0010).
4. El **Telnet real** se muestra en local y en el vídeo; no se despliega.
5. Límites: tope de llamadas LLM por sesión y por día (contador atómico en DynamoDB, ADR 0009),
   límite de intentos de login por IP (bloqueo progresivo con TTL), comparación de
   credenciales en tiempo constante y pantalla de login dentro de la ficción BBS.

## Decisión original reemplazada
Alojar en **Google Cloud Run** (una instancia, WebSocket, contador en memoria, alerta de GCP).
Se conserva como **alternativa documentada**, junto con Lightsail.

## Motivos del cambio
- Kiro es de AWS y hay créditos de AWS (no hay bonus del hackathon por ello).
- El contador diario en DynamoDB es exacto y no se reinicia; en Cloud Run el contador en
  memoria se ponía a cero con cada reinicio (el límite `shortcut` de antes desaparece).
- Sin WebSocket: el juego es por turnos y no necesita conexión viva.

## Consecuencias
Tareas 7.4, 13.5 y 14; requisitos R13.
