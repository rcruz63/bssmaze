# ADR 0009: Guardado detrás de un Protocol `SaveStore`

- Estado: aceptada
- Fecha: 2026-11-26

## Contexto
La caída de portadora guarda el estado y el mismo jugador lo retoma. En Cloud Run el disco
del contenedor es efímero y la instancia escala a cero tras unos 15 minutos sin tráfico.
Un juez que vuelva al día siguiente perdería la partida si el guardado vive solo en disco local.

## Decisión
1. La sesión guarda solo a través de `SaveStore`, un `typing.Protocol` con tres métodos:
   `load(player_id) -> SaveGame | None`, `save(player_id, save_game) -> None`,
   `delete(player_id) -> None`.
2. `LocalFileSaveStore` es la implementación por defecto (disco local) y la única en tests.
3. `GcsSaveStore` es opcional: se elige solo si existe la variable `GCS_SAVE_BUCKET`.
   Importa `google-cloud-storage` de forma perezosa; la dependencia se añade a `pyproject`
   solo en la tarea 14.11.
4. Sin bucket, la reanudación funciona solo mientras la instancia siga activa. README, notas
   de la demo y lista de envío deben decirlo.

## Motivos
- Un Protocol pequeño permite cambiar de almacén sin tocar el motor ni la sesión.
- El bucket es opcional para no añadir coste ni complejidad al desarrollo local.

## Consecuencias
Propiedad P17 (ida y vuelta, `delete` idempotente). Tareas 11.1, 14.11 y 14.12; requisitos R10.4 a R10.6.
