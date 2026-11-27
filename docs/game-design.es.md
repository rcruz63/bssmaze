# Diseño del juego

El idioma del juego es **inglés** (jurado internacional). Esta documentación
está en español. Las reglas son pequeñas a propósito: deben caber en 4 días.

## 1. Bucle principal
1. El motor muestra el nodo actual (narrado por el LLM o por la plantilla offline).
2. El jugador escribe una orden en texto libre.
3. El narrador la convierte en una `ProposedAction` (o el parser clásico, si falla).
4. El motor valida la acción contra las reglas y la aplica o la rechaza.
5. El motor emite eventos; el narrador los cuenta; el renderizador los dibuja.
6. Se repite hasta victoria, derrota, fin de llamada o caída de portadora.

## 2. Personaje
| Atributo | Rango | Uso |
|---|---|---|
| `hit_points` | 0..20 | Vida. A 0 se pierde. |
| `wits` (ingenio) | 0..5 | Modificador en acertijos y trampas |
| `brawn` (fuerza) | 0..5 | Modificador en ataque |
| `luck` (suerte) | 0..5 | Modificador al huir y en la caída |
| inventario | máx. 8 ids | Objetos únicos |

Al crear personaje se reparten 6 puntos entre los tres modificadores (máx. 3 cada uno).

## 3. Dados y semilla
- Una tirada es `d20 + modificador >= dificultad`.
- 20 natural siempre acierta; 1 natural siempre falla.
- Un único `random.Random` con semilla vive en el estado. Se guarda la semilla y
  el número de tiradas, así una partida se puede reproducir exactamente.
- Motivo: tests deterministas y repeticiones para depurar.

## 4. Grafo de nodos
Una historia es un conjunto de **nodos** con salidas, requisitos, objetos y
encuentros. Se cargan desde YAML y se validan con Pydantic.

```yaml
- id: crypt_door
  title: The Sealed Crypt
  text: A rusty door hums with static.
  exits:
    - {label: north, target_id: crypt, requirement: {item: iron_key}}
  items: []
  encounter: null
  is_ending: false
```
El **validador de grafo** comprueba: nodo inicial existe, todas las referencias
existen (`target_id`), todos los nodos son alcanzables desde el inicio, no hay nodos sin salida
(salvo los marcados `is_ending: true`) y desde cualquier nodo se puede llegar a un final.

## 5. Combate por turnos
- Lo resuelve solo el motor. Ronda: jugador, luego enemigo.
- Acciones: `attack` (`d20 + brawn >= defensa del enemigo`, daño fijo del arma),
  `use` (objeto), `flee` (`d20 + luck >= 12`).
- El enemigo ataca con `d20 + ataque >= 10 + armadura`; su daño es fijo.
- El LLM solo añade texto de ambiente; no toca números.

## 6. Papel del LLM
| Tarea | Entrada | Salida | Quién valida |
|---|---|---|---|
| Narrar nodo | `NarrationContext` acotado | Texto | Longitud y formato |
| Interpretar orden | Texto del jugador (como dato) | `ProposedAction` | Esquema + lista blanca + reglas |
| Texto de enemigo | Nombre y evento ya decidido | Frase | Longitud |

Defensas:
- Lista blanca de acciones: move, look, take, use, attack, flee, inventory, help, quit.
- Esquema estricto (`extra="forbid"`), 200 caracteres máximo de entrada.
- El texto del jugador va entre delimitadores y se declara dato, no instrucción.
- Tiempo límite de 8 s. Si falla o devuelve algo inválido, entra el narrador offline.
- El contexto no incluye banderas ocultas, historia completa ni claves.

## 7. Narrador offline determinista
Plantillas por nodo y un parser de verbos (`go north`, `take key`, `hit ghoul`).
Se usa en tests, sin clave de API y como respaldo de la demo.

## 8. Caída de portadora (función estrella)
1. Al inicio de cada ronda de combate el motor tira contra `drop_chance` (8 % por defecto).
2. Si cae: se guarda el estado, se muestran mensajes en ficción
   (`+++ATH0`, `NO CARRIER`) y se cierra la conexión (en la web, la respuesta trae
   `carrier_dropped` y el cliente se desconecta).
3. Al reconectar con el mismo handle, se carga el guardado y se retoma la misma ronda.
4. La decisión usa la RNG del motor, por lo que los tests pueden forzarla.
Motivo: da identidad al juego y demuestra que el estado vive en el motor, no en la conexión.

## 9. Sabor BBS
Pantalla de login, handle, boletines del SysOp, menú de juegos "door" y límite de
tiempo por llamada (40 turnos, contados en turnos y no en segundos para ser
deterministas). Al agotarse: `NO CARRIER`.

## 10. Guardado y reanudación
Un JSON por handle con el estado validado. Si el archivo está corrupto se aparta
(`.bad`) y se empieza de nuevo. No contiene secretos.

## 11. Historia: "The Haunted Maze"
Aproximadamente 14 nodos. Meta: salir del laberinto con la Llave de Hierro.
| Zona | Nodos | Contenido |
|---|---|---|
| Entrada | `gate`, `hall` | Boletín del SysOp, primer objeto (linterna) |
| Laberinto | `maze_a`..`maze_e` | Callejones, un acertijo de ingenio |
| Sótano | `cellar`, `ossuary` | Llave de hierro, primer combate (esqueleto) |
| Cripta | `crypt_door`, `crypt` | Puerta con llave, jefe (el Fantasma del SysOp) |
| Finales | `escape`, `trapped` | Victoria y derrota |

## 12. Internacionalización
Catálogos `en` y `es-ES` solo para textos de interfaz (menús, errores, ayuda). Si
falta una clave en `es-ES` se usa `en`. Un test exige que ambos tengan las mismas claves.

## 13. Proveedor de LLM
Interfaz `NarratorProvider` en `narrator/`. Cadena: Amazon Bedrock (principal), Gemini
(respaldo) y narrador offline. Los ids de modelo van en `BEDROCK_MODEL_ID` y `GEMINI_MODEL`,
nunca en el código. Ver ADR 0006.

El script `scripts/validate_story_graph.py` hace una versión ligera de estas
comprobaciones sobre `stories/` (destinos, callejones sin salida, líneas de más de
80 columnas, nodos inalcanzables) y corre en `make check`.
