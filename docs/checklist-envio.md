# Lista de envío al hackathon

Versión de trabajo en español. La versión que usa el agente está en
`.kiro/steering/submission-checklist.md` (se invoca con `#submission-checklist`).

- [ ] Repositorio público con licencia MIT (`LICENSE`).
- [ ] `.kiro/` versionado; `git check-ignore -v .kiro` no imprime nada.
- [ ] Código escrito entre el 30 de octubre y el 4 de diciembre de 2026.
- [ ] Categoría Resurrection.
- [ ] URL de demo (terminal web) y datos de Telnet. Funciona sin clave de API.
- [ ] Usuario y contraseña de la demo solo en el campo *testing instructions* de Devpost, nunca en el repositorio.
- [ ] Guardados: `GCS_SAVE_BUCKET` configurado, o README y notas de la demo avisan de que la reanudación solo funciona mientras la instancia siga activa.
- [ ] `GEMINI_MODEL` configurado en Cloud Run y comprobado con `list_models` y la clave real.
- [ ] Cloud Run con `max-instances 1`, alerta de presupuesto de GCP y tope diario de llamadas LLM comprobado.
- [ ] Telnet real se muestra en local y en el vídeo (Cloud Run no sirve TCP crudo).
- [ ] Vídeo de menos de 3 minutos en YouTube.
- [ ] Descripción: qué es, cómo se usó Kiro (specs, steering, hooks, estrategia, experimentos).
- [ ] **Bonus:** entrada de blog sobre cómo se construyó con Kiro.
- [ ] **Bonus:** publicación en redes con la etiqueta #KiroweenHackathon26.
- [ ] `make check` en verde sobre un clon limpio.
- [ ] Enviar con margen: objetivo jueves 3 de diciembre.
