# ADR 0001: El LLM nunca modifica el estado del juego

- Estado: aceptada
- Fecha: 2026-11-26

## Contexto
Un LLM puede inventar objetos, curarse la vida o ser engañado por el texto del
jugador (inyección de prompt). Un juego con reglas necesita estado fiable y repetible.

## Decisión
El motor Python (Pydantic v2) es la única fuente de verdad de vida, inventario,
dados y nodo actual. El LLM solo recibe contexto acotado y devuelve narración o
una `ProposedAction`. El motor valida esquema, lista blanca y reglas, y entonces
aplica o rechaza.

## Alternativas
- LLM con herramientas que modifican el estado: flexible, pero no determinista ni seguro.
- LLM que devuelve el estado completo: se rompe con una sola alucinación.

## Consecuencias
- Tests deterministas con semilla y narrador offline.
- Una inyección de prompt no puede causar daño: el modelo no tiene ningún campo que cambie el estado.
- Menos libertad creativa: el LLM no puede crear objetos ni salidas nuevas.
