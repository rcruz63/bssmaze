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
Una Lambda "hola mundo" detrás de `POST /api/command`, con tabla y CloudFront. Sirve para
descubrir pronto los problemas de permisos, región y arranque en frío.

## Respaldo
Si el despliegue serverless no funciona el dom 29 nov, se usa una instancia Lightsail con el
mismo código (ADR 0010). Para borrar todo: `sam delete`.
