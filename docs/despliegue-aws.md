# Despliegue serverless en AWS

Decisión: ADR 0010. Diseño: `.kiro/specs/telnet-tales/design-aws.md`. Esta guía se
completa en las tareas S1 y 14.9; los comandos son los previstos.

## Qué debe hacer el usuario (acción humana)
1. Instalar AWS CLI y SAM CLI, y entrar en su terminal: `aws configure sso` (o un perfil).
   Las credenciales **nunca** van en el repositorio ni en `.env.example`.
2. Elegir la región y **activar el acceso a modelos de Amazon Bedrock** en esa región.
3. Guardar `AUTH_SECRET` y la contraseña de la demo en SSM Parameter Store (o en las
   variables de la Lambda) y copiar usuario y contraseña al campo *testing instructions* de Devpost.

## Pasos
```bash
make package                     # zip arm64 con uv (tarea 14.3)
sam build
sam deploy --guided --profile <perfil>
aws cloudformation describe-stacks --stack-name <pila> --query 'Stacks[0].Outputs'
uv run python -m telnet_tales.narrator.list_models   # comprueba BEDROCK_MODEL_ID
```
El resultado incluye la URL de CloudFront. La plantilla es `infra/template.yaml`
(Lambda, HTTP API, DynamoDB, S3, CloudFront y alerta de AWS Budgets).

## Despliegue de humo (sáb 28 nov)
Hecho el 27 nov (tarea S1). Pila `telnet-tales-smoke`, región `us-east-1`, perfil `casa`.
Recursos: Lambda python3.12 arm64 (`infra/smoke/handler.py`), HTTP API `POST /api/command`,
tabla DynamoDB (TTL `ttl`), bucket S3 privado y CloudFront con OAC y ruta `/api/*` sin
caché. IAM mínimo: solo `PutItem` y `GetItem` sobre la tabla; el permiso de Bedrock está
comentado en la plantilla.

- CloudFront: https://d2q60lhdk0h8ue.cloudfront.net
- API: https://62elw6oupa.execute-api.us-east-1.amazonaws.com
- Tabla: `telnet-tales-smoke-Table-R2P3D386VRYJ`
- Bucket: `telnet-tales-smoke-sitebucket-98dtgflapfi5`

Redespliegue, desde la raíz del repo:
```bash
export SAM_CLI_TELEMETRY=0   # sin esto sam se quedó colgado en esta máquina
make smoke-deploy            # sam build + sam deploy con infra/samconfig.toml
```
Subir la página es un paso manual del usuario (el agente tiene bloqueada la copia a S3):
```bash
aws s3 cp infra/web/index.html s3://telnet-tales-smoke-sitebucket-98dtgflapfi5/index.html --content-type text/html --profile casa --region us-east-1
```
Prueba de la API:
```bash
curl -s -X POST https://d2q60lhdk0h8ue.cloudfront.net/api/command -H 'content-type: application/json' -d '{}'
```
Medido con curl (tiempo total): 1.36 s en frío, 0.81 s y 0.53 s en caliente. En la Lambda:
`Init Duration` 369 ms, 155 ms la primera llamada y 20 ms las siguientes.

Borrar todo (solo lo ejecuta el usuario; primero hay que vaciar el bucket):
```bash
aws s3 rm s3://telnet-tales-smoke-sitebucket-98dtgflapfi5 --recursive --profile casa --region us-east-1
sam delete --stack-name telnet-tales-smoke --profile casa --region us-east-1
```
Pendiente del usuario: la alerta de AWS Budgets necesita su correo.

## Respaldo
Si el despliegue serverless no funciona el dom 29 nov, se usa una instancia Lightsail con el
mismo código (ADR 0010). Para borrar todo: `sam delete`.
