# Lista de envío al hackathon

Versión de trabajo en español. La versión que usa el agente está en
`.kiro/steering/submission-checklist.md` (se invoca con `#submission-checklist`).

- [ ] Repositorio público con licencia MIT (`LICENSE`).
- [ ] `.kiro/` versionado; `git check-ignore -v .kiro` no imprime nada.
- [ ] Código escrito entre el 30 de octubre y el 4 de diciembre de 2026.
- [ ] Categoría Resurrection.
- [ ] URL de demo (terminal web en CloudFront) y datos de Telnet. Funciona sin acceso a AWS ni clave de Gemini.
- [ ] Usuario y contraseña de la demo solo en el campo *testing instructions* de Devpost, nunca en el repositorio.
- [ ] Estado: `STATE_TABLE_NAME` configurado en la Lambda; una partida guardada por caída de portadora se retoma al día siguiente (DynamoDB con TTL).
- [ ] `BEDROCK_MODEL_ID` (y `GEMINI_MODEL` si se usa) configurados y comprobados con `list_models` en la cuenta y con la clave reales; acceso a modelos de Bedrock activado en la región.
- [ ] Despliegue serverless hecho con `sam deploy`, alerta de AWS Budgets y tope diario de llamadas LLM comprobado.
- [ ] Telnet real se muestra en local y en el vídeo (no se despliega).
- [ ] Vídeo de menos de 3 minutos en YouTube.
- [ ] Descripción: qué es, cómo se usó Kiro (specs, steering, hooks, estrategia, experimentos).
- [ ] **Bonus:** entrada de blog sobre cómo se construyó con Kiro.
- [ ] **Bonus:** publicación en redes con la etiqueta #KiroweenHackathon26.
- [ ] `make check` en verde sobre un clon limpio.
- [ ] Enviar con margen: objetivo jueves 3 de diciembre.
