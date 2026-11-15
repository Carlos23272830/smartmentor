# Subidas a GitHub

Registro de cada `push` y cada pull request. **Solo se agregan entradas al final.** Se sube únicamente con la aprobación del dueño, a ramas `feature/*` o `fix/*`, y nunca a `dev`, `stage` ni `main` ([README](README.md#flujo-de-trabajo)).

Repositorio: <https://github.com/armandoordonez/smartmentor>

## Plantilla

```markdown
### S-NNN · AAAA-MM-DD HH:MM · <rama>

- **Commits:** `abc1234` título, `def5678` título
- **IDs:** T-NNN, B-NNN
- **PR:** <enlace> hacia `dev` (abierto / fusionado el AAAA-MM-DD HH:MM en `hash`)
- **CI:** en verde / falló (qué paso) / sin correr
- **Pruebas locales:** comando y resultado, o «sin correr» y por qué
- **Quién aprobó la subida:** <persona>
```

## Antecedentes (antes de este registro)

| PR | Rama → base | Estado | Nota |
| --- | --- | --- | --- |
| 1 | `fix/syllabus-como-fuente-rag` → `dev` | Fusionado 2026-11-11 | |
| 2 | `feature/archivar-curso` → `fix/syllabus-como-fuente-rag` | Fusionado 2026-11-11 | Llegó a `dev` con el PR 1 |
| 3 | `fix/conteos-y-tablero` → `dev` | Fusionado 2026-11-11 (`d8de841`) | |
| 4 | `fix/bloqueo-trabajos-ia` → `fix/conteos-y-tablero` | Fusionado 2026-11-12 | **No llegó a `dev`** ([B-001](BUGS.md)) |
| 5 | `fix/flujo-aprendiz` → `dev` | Borrador | 3 commits por delante de `dev` |

## Registro

### S-001 · 2026-11-12 15:01 · `feature/seguimiento-trazabilidad`

- **Commits** (base `dev` = `d8de841`):
  - `ee2ee75` docs(proyecto): agrega la carpeta de seguimiento y trazabilidad [T-001]
  - `02c4f5a` docs(proyecto): registra la corrección de B-001 y corrige una hora de la bitácora [T-002]
  - `d47df63` feat: pantallas del instructor y del administrador con la API real [T-012 T-013 T-014 T-015]
  - `54b8b1e` docs(proyecto): seguimiento de T-012 a T-015, bugs B-003 a B-008 y estado por fase
  - `4ea823f` fix(api): bloquear con FOR NO KEY UPDATE para que ai/ pueda guardar sus trabajos (cherry-pick de `448e154`, autora Alexander Amador) [B-001]
- **IDs:** T-001, T-002, T-012, T-013, T-014, T-015a a T-015e, B-001, B-003 a B-008, F-012 a F-014
- **PR:** ninguno todavía. Se puede abrir en <https://github.com/armandoordonez/smartmentor/pull/new/feature/seguimiento-trazabilidad>
- **CI:** la corrida `43296141612` quedó en cola a las 15:01; su resultado se anota cuando termine
- **Pruebas locales:** sin correr (el dueño no autorizó ejecutar el proyecto)
- **Fuera de la subida:** `pr-3-descripcion-actualizada.md` (borrador del dueño, sin versionar)
- **Quién aprobó la subida:** el dueño, en el chat (2026-11-12 15:02)

### S-002 · 2026-11-12 15:05 a 15:25 · `feature/seguimiento-trazabilidad`

Correcciones que pidió la CI. Las pruebas no se pueden correr en este equipo (no hay Docker ni `uv`), así que el dueño pidió las pruebas y se corrieron en la CI:
- `73c9224` style: Ruff lint (I001, SIM108, E501, PT018) y un enlace roto → CI `43304494731`: falló el formato (app) y E501 (API)
- `7181ee3` style: línea larga y formato → CI `43304868193`: app con 620 pruebas en verde y 1 fallida (AD3 frente a Figma: faltaba la cohorte en el encabezado); API con el formato de 2 archivos
- `0c07692` fix(app): la cohorte vuelve al encabezado de AD3, y el formato del piloto → CI `43305251283`: app en verde; API con 659 en verde y 1 fallida (el OpenAPI publicado no coincidía: faltaba la descripción nueva de `GET /metrics/evaluation`)
- `58badeb` docs(contracts): sincroniza esa descripción → **CI `43305654426` en verde**

### Resultado de las pruebas · 2026-11-12 15:31

| Servicio | Ruff | Formato | mypy estricto | pytest |
| --- | --- | --- | --- | --- |
| api | ✔ | ✔ (216 archivos) | ✔ (141) | ✔ **660 en verde** |
| app | ✔ | ✔ (141) | ✔ (104) | ✔ **621 en verde** |
| ai | ✔ | ✔ (150) | ✔ (145) | ✔ 463 en verde, 10 omitidas |

También en verde: liquibase, keycloak-realm, prompts, infra, docs (markdownlint y enlaces), secrets (gitleaks) e images (Trivy). Fallan solo `audit (api)` y `audit (app)`, que son informativos y ya fallaban en `dev` ([B-009](BUGS.md)).

### S-003 · 2026-11-12 20:11 · `feature/seguimiento-trazabilidad`

- **Commits:**
  - `ec2dd00` fix(app): el nivel por tema de D4 sale de 0 a 100 % y no en 670 % [B-010]
  - `ddb3784` feat(auth): renovación silenciosa del token y sesión de 3 horas
  - `040bf54` fix: el reintento de la evaluación final genera preguntas nuevas [B-011]
  - `c585fa1` feat(scripts): simula aprendices que recorren cada ruta publicada
  - el commit del seguimiento (esta entrada)
- **IDs:** B-010, B-011, F-015, M-006
- **PR:** ninguno todavía
- **CI:** corrida `43342980911`: api (con las pruebas de integración, incluida la nueva de B-011), app, ai, liquibase, keycloak-realm, infra, prompts, secrets e images en verde. `docs` falló por 2 avisos de markdownlint en `BITACORA.md` (un encabezado repetido y una línea en blanco de más), corregidos en el commit siguiente. `audit (api)` y `audit (app)` fallan como en `dev` ([B-009](BUGS.md))
- **Pruebas locales:** app con Ruff, formato y mypy en verde, y 628 pruebas en verde. API con Ruff, formato y mypy en verde; unitarias con 445 en verde y 2 que fallan solo en este equipo por el `.env` real. La integración de la API no se corrió aquí porque apunta a Neon; la corre la CI. Prueba en vivo con 4 aprendices simulados (ver la bitácora).
- **Fuera de la subida:** `.claude/` (configuración local) y `pr-3-descripcion-actualizada.md`
- **Quién aprobó la subida:** el dueño, en el chat (2026-11-12 20:11)

### S-004 · 2026-11-12 20:17 · `feature/seguimiento-trazabilidad` → `dev`

- **Commits:** `5b9a6aa` docs(proyecto): corrige dos avisos de markdownlint y anota la CI de S-003; y el commit de esta entrada
- **PR:** <https://github.com/armandoordonez/smartmentor/pull/6> hacia `dev` (fusionado el 2026-11-12 21:11 en `42b14df`). Reúne S-001 a S-004: T-012 a T-015, B-001 a B-011 y la sesión de 3 h
- **CI:** corrida `43343437580` (`5b9a6aa`) en verde, también `docs`. Solo fallan `audit (api)` y `audit (app)`, informativos ([B-009](BUGS.md))
- **Quién aprobó la subida:** el dueño, en el chat (2026-11-12 20:17)

### S-005 · 2026-11-13 13:46 · `feature/hoja-de-ruta-f6-f7`

- **Rama:** nueva, desde `dev` en `42b14df` (después de fusionar el PR 6)
- **Commits:**
  - `047bc29` fix(ai): corta las llamadas al LLM a los 240 s y alarga el lease a 1800 s (B-013)
  - `16bbce0` docs(contratos): aclara que next_action de GET /jobs/{id} siempre es null (B-012)
  - `1f6d39a` test(app): error al preparar preguntas nuevas (T-020) y sincronía de C4 con el catálogo de prompts (M-008)
  - `4e59245` fix(app): revisión visual frente a Figma (V-001 a V-024) y CSS que DOMPurify descartaba (B-014)
  - `69a6651` docs(proyecto): seguimiento de F6 y F7, checklist al 60 %, HANDOFF y CHANGELOG (T-003, T-034)
  - `3e2e003` fix(app): revisión visual de D5b a D5f y A7 frente a Figma (V-026 a V-031)
  - el commit del seguimiento (esta entrada)
- **IDs:** B-012, B-013, B-014, M-008, T-003, T-020, T-034, V-001 a V-032
- **PR:** <https://github.com/armandoordonez/smartmentor/pull/7> hacia `dev`, abierto el 2026-11-13
- **CI:** corrida `43485918657` (`e9130ae`): 12 trabajos en verde y 1 en curso al abrir el PR. Fallan solo `audit (api)` y `audit (app)`, informativos ([B-009](BUGS.md))
- **Pruebas locales:** app con Ruff, formato y mypy en verde, y **632 pruebas en verde**. Revisión en el navegador del 8502 (datos de ejemplo) y del 8501 (pantalla previa al login)
- **Fuera de la subida:** `.claude/` (configuración local) y `pr-3-descripcion-actualizada.md`
- **Quién aprobó la subida:** el dueño, en el chat (2026-11-13 13:46)

### S-006 · 2026-11-13 13:57 · `feature/hoja-de-ruta-f6-f7` (PR 7)

- **Commits:** `build(deps)`: actualiza `certifi`, `dnspython` y `opentelemetry-api` en `api/uv.lock` y `certifi` en `app/uv.lock` (B-009); y el registro de S-005 y S-006
- **Por qué:** en el PR 7 fallaban `audit (api)` y `audit (app)` por vulnerabilidades conocidas en las dependencias fijadas, no por el código del PR
- **Pruebas locales:** `pip-audit` de `api/` sin vulnerabilidades. API con Ruff y mypy en verde y 445 pruebas unitarias en verde (fallan las 2 de siempre, solo aquí, por el `.env` real). App con 632 pruebas en verde
- **Queda:** `audit (app)` sigue fallando por `pillow` 12.3.0, que no se puede subir sin cambiar Streamlit 1.65 ([B-009](BUGS.md))
- **Quién aprobó la subida:** el dueño, en el chat («corrígelo y sube los cambios»)

### S-007 · 2026-11-13 14:40 · `feature/hoja-de-ruta-f6-f7` (PR 7)

- **Commits:**
  - `65c47ec` fix(app): la hoja de vida se guarda aunque Streamlit recargue los modelos [B-015]
  - `dedc6b1` fix(app): la hoja de vida sigue al diagnóstico y no vuelve al perfil [B-016]
  - el commit del seguimiento (esta entrada)
- **IDs:** B-015, B-016
- **Pruebas locales:** app con Ruff, formato y mypy en verde y **635 pruebas en verde** (3 nuevas). Recorrido en el navegador del 8502: consentimiento → catálogo → E2 → E2b con inglés B1 → E3
- **Ojo con el PR 5:** toca `pages/learner/onboarding_profile.py` y `clients/fixtures.py`, que el PR 5 también puede cambiar
- **Quién aprobó la subida:** el dueño, en el chat (2026-11-13 14:40)

### S-008 · 2026-11-13 16:53 · `feature/hoja-de-ruta-f6-f7` (PR 7)

- **Commits:**
  - `18cdffa` fix(app): diagnóstico, quiz y objetivo sin recargas ni 422 con la API real [B-018, B-019, B-020, B-022]
  - `11b2a48` fix(app): el catálogo abre la ruta y no salta al quiz abierto [B-023]
  - el commit del seguimiento (esta entrada), con B-017 y B-021
- **IDs:** B-017 a B-023
- **Pruebas locales:** app con Ruff, formato y mypy en verde y **637 pruebas en verde**. En la copia de prueba (PR 5 sobre PR 7, local), 739. El dueño probó cada arreglo en el 8501 con la API real
- **Ojo:** B-017 (el catálogo del aprendiz con la API real) se arregla con el PR 5, no con este PR
- **Quién aprobó la subida:** el dueño, en el chat (2026-11-13 16:53)

### S-009 · 2026-11-13 17:28 · `feature/hoja-de-ruta-f6-f7` (PR 7)

- **Commits:**
  - `0926d4a` fix(app): tema, quiz, final y metas coherentes con la API real [B-024, B-025, B-026, B-027, B-028]
  - `784bac6` fix(app): regenerar un recurso en D5 genera de nuevo y muestra la versión nueva [B-029]
  - el commit del seguimiento (esta entrada)
- **IDs:** B-024 a B-029
- **Pruebas locales:** app con Ruff, formato y mypy en verde y **643 pruebas en verde**. En la copia de prueba (PR 5 sobre PR 7, local), 746; 8501 reconstruido con ella
- **Ojo:** B-025 deja una decisión del dueño (que la API entregue el contenido de los temas aprobados para repasarlos desde E9). En el PR 5, `topic.py` y `quiz.py` también cambian: al fusionarlo hay que conservar los dos arreglos
- **Quién aprobó la subida:** el dueño, en el chat (2026-11-13 17:28)

### S-010 · 2026-11-13 17:33 · `dev_13112026_530` (respaldo de `dev`) y PR 7

- **Respaldo:** rama nueva `dev_13112026_530` en GitHub, creada en el mismo commit de `dev` (`42b14df`, la fusión del PR 6). No cambia `dev`
- **PR 7 hacia `dev`:** ya existía con todos los commits (B-012 a B-029). Se actualizaron el título y la descripción con el flujo del aprendiz (B-015 a B-029), las pruebas (643 y 746 con el PR 5) y lo que falta (B-017 con el PR 5 y la decisión de B-025)
- **Commits:** el de esta entrada
- **Quién aprobó la subida:** el dueño, en el chat (2026-11-13 17:33)

### S-011 · 2026-11-14 21:45 · PR 7 y PR 5 fusionados en `dev` (validación)

Revisión con `gh` y `git` del estado real de `dev`, sin subir nada.

- **PR 7** (`feature/hoja-de-ruta-f6-f7` → `dev`): fusionado el 2026-11-14 13:09 en `12ca602`. Trae B-012 a B-029, la revisión visual (V-001 a V-032) y el seguimiento de F6 y F7
- **PR 5** (`fix/flujo-aprendiz` → `dev`): fusionado el 2026-11-14 13:49 en `e9f349c`. Trae el flujo del aprendiz con la API real (`25f4c7c`, `397246f`, `c73d448`), la fusión con `dev` (`2d9145e`), `75d4f17` y `38fcf00` (Streamlit 1.67 y `pillow` 13.0.0, B-009)
- **IDs:** T-010, B-009, B-017 y B-012 a B-029
- **CI de `dev` (`e9f349c`):** en verde, los 15 trabajos, incluidos los tres `audit` (`ai`, `api` y `app`). Antes de `38fcf00` el de `app` fallaba por 42 vulnerabilidades de `pillow` 12.3.0
- **Pruebas locales:** app con 746 pruebas, Ruff, formato y mypy en verde
- **Verificado en el código de `dev`:** `FOR NO KEY UPDATE` (B-001), rutas `deactivate` (B-003), `topic_count` (B-017), `set_objective` sin `origin` (B-020), `open_attempt_id` en `topic.py` con un solo `topic-continue-quiz` (B-024), `ai_llm_timeout_seconds` en 240 (B-013) y Streamlit 1.67 con `pillow` 13.0.0 (B-009). El commit `448e154` del PR 4 no es ancestro de `dev` (se fusionó por otra rama), pero su contenido sí está
- **Quién aprobó la subida:** no hubo subida; se registra la validación

### S-012 · 2026-11-14 23:57 · 8 ramas nuevas y 9 PR hacia `dev`

- **Ramas subidas:** `fix/widgets-key-streamlit-167`, `feature/admin-y-fixtures`, `feature/menu-perfil-roles`, `fix/videos-ingles-r001`, `feature/nivel-escala-absoluta-r002`, `feature/eventos-interfaz-r003`, `fix/widgets-casos-menores` y `fix/visual-preguntas-y-progreso` (todas desde `dev`, `e9f349c`)
- **PR hacia `dev`:** [8](https://github.com/armandoordonez/smartmentor/pull/8) B-009 widgets · [9](https://github.com/armandoordonez/smartmentor/pull/9) T-015 · [10](https://github.com/armandoordonez/smartmentor/pull/10) F-004 · [11](https://github.com/armandoordonez/smartmentor/pull/11) R-001 · [12](https://github.com/armandoordonez/smartmentor/pull/12) R-002 · [13](https://github.com/armandoordonez/smartmentor/pull/13) R-003 · [14](https://github.com/armandoordonez/smartmentor/pull/14) B-009 menores · [15](https://github.com/armandoordonez/smartmentor/pull/15) V-033 y V-050 · [16](https://github.com/armandoordonez/smartmentor/pull/16) seguimiento
- **IDs:** B-009, T-015, T-024, F-004, R-001, R-002, R-003, V-033, V-050, R-009
- **Pruebas locales:** las 9 ramas fusionadas juntas en una copia: app 792 en verde, ai 474 en verde y 10 omitidas, Ruff, formato y mypy en verde, y `check-env-coherence.py` coherente. Se fusionan sin conflictos en cualquier orden. Al probarlas juntas apareció que R-001 no documentaba sus variables: se corrigió en `1354d20`
- **CI:** se anota al fusionar
- **Quién aprobó la subida:** el dueño, en el chat («Abro un PR por rama y tú fusionas»)

### S-013 · 2026-11-15 00:08 · PR 8 a PR 16 fusionados en `dev`

- **Fusiones (el dueño, en GitHub):** PR 15 (`ca0b133`) y PR 16 (`7fe1538`) el 2026-11-14 23:59; PR 8 (`dce0ecc`) y PR 14 (`209f913`) el 2026-11-15 00:00; PR 9 (`f6ad347`), PR 11 (`284d679`) y PR 12 (`d419a2b`) a las 00:01; PR 10 (`dc58757`) y PR 13 (`cedf2d7`) a las 00:02
- **IDs:** B-009, T-015, F-004, R-001, R-002, R-003, V-033, V-050, R-009
- **CI:** en verde en los 9 PR antes de fusionar, y en `dev` sobre `dc58757`, que los incluye a todos. Las corridas de los commits intermedios quedaron canceladas porque GitHub las reemplazó con la siguiente
- **Esta entrada:** rama `feature/seguimiento-fusion-pr8-16`, con PR hacia `dev`
- **Quién aprobó la subida:** el dueño, en el chat («Abro un PR por rama y tú fusionas»)

### S-014 · 2026-11-15 08:51 · PR 17 a PR 26 fusionados en `dev` y PR 27 abierto

- **Fusiones (el dueño, en GitHub, 2026-11-15):** PR 26 (`e1c44df`, 08:41), que incluía los PR 19, 21, 23, 24 y 25; PR 17 (`721f1a2`), 18 (`1a3677b`) y 20 (`eb8b638`) a las 08:44; PR 22 (`76da200`) a las 08:46
- **IDs:** E8, B-037, R-003 (m27), V-011 a V-013, V-040, V-042, V-043, B-030, B-031, B-034, V-045 a V-048, V-038, V-039, V-041, V-044, V-051, V-052, V-055, V-034 a V-036, V-054, R-008, R-009, G-001
- **Antes de fusionar:** las ramas de la app se probaron juntas en una copia (847 pruebas en verde) y cada PR tuvo la CI en verde
- **Abiertos:** [PR 27](https://github.com/armandoordonez/smartmentor/pull/27) (`fix/detalles-recorrido`, B-039) y [PR 28](https://github.com/armandoordonez/smartmentor/pull/28) (`fix/visual-nuevo-curso`, V-061 a V-069). Juntos encima de `dev`: 857 pruebas de la app en verde
- **Esta entrada:** rama `feature/seguimiento-fusion-pr17-26`, con PR hacia `dev`
- **Quién aprobó:** el dueño, en el chat («los pr todos ya fueron aprobados y mezclados»)
