# Pendientes del proyecto

Une dos revisiones del 2026-11-14, con `dev` en `e9f349c` (PR 1 a PR 7 fusionados y la CI en verde):

- **Producto y piloto:** pantallas, decisiones del dueño y cierre.
- **Evaluación y código de IA:** la revisión del repositorio frente a la entrega final (piezas de IA, experimentos y resultados). Sus IDs empiezan por `R-`.

Pruebas sobre `dev`: interfaz, 746 en verde (Ruff y mypy limpios); servicio de IA, 463 en verde y 10 omitidas; API, 447 unitarias en verde. Las 214 de integración de la API necesitan PostgreSQL y pasan en la CI.

Este archivo resume, no reemplaza. El detalle con fecha y hora está en [`HOJA_DE_RUTA.md`](HOJA_DE_RUTA.md), [`BUGS.md`](BUGS.md), [`FIGMA.md`](FIGMA.md) y [`HANDOFF.md`](../../HANDOFF.md).

## Significado de los iconos

| Icono | Tareas y mejoras | Bugs y huecos de Figma |
| --- | --- | --- |
| ☐ | Pendiente | Abierto |
| ◐ | En curso | En corrección |
| ⏳ | Hecho en local, sin subir | Corregido en local, sin subir |
| ⬆ | Subido a una rama, sin PR | Corrección subida, sin PR |
| 🔼 | Subido a una rama, con PR abierto | Corrección subida, PR abierto |
| ✔ | En `dev` | Corregido y en `dev` |
| ⛔ | Bloqueado (se dice por qué) | Bloqueado |
| ✖ | Descartado (se dice por qué) | No es un bug, o no se corrige |
| 👤 | Depende del dueño: en «Funcionalidades» se separa qué decidir y qué pantallas de Figma revisar | Igual |

**Estado «Finalizado»:** se indica la fecha y dónde quedó: `dev` si ya está fusionado, o el nombre de la rama si se hizo aparte y falta fusionarla.

**Responsable:** quien lleva el punto hoy. «—» quiere decir que todavía no tiene responsable.

**Peso en la entrega final:** **Crítico** (sin esto no hay resultados que mostrar), **Alto** (bloquea un experimento o la prueba con usuarios), **Medio** (afecta la calidad o la demo), **Bajo** (detalle o pulido).

Los códigos de pantalla (E1, D5b, AD4…) son los de Figma v3 (archivo maestro `atp2fZdSolEoaww3n9jRLg`); cada enlace abre el nodo en Figma. La lista completa está en [`pantallas.md`](../../design/03-prototipo-alta-fidelidad/v3/pantallas.md).

## Ruta crítica hacia la entrega final

La entrega final pide «un recorrido integral por el proceso, observando los resultados en el tiempo, así como los experimentos y las técnicas aplicadas». Hoy solo está ejecutado E1. El orden sugerido:

1. **Código, 1 o 2 días:** R-001 (filtro de videos), R-003 (eventos de la interfaz) y T-010 / T-011 (recorrer la final y el badge en el navegador).
2. **Experimentos sin terceros:** E2, E3, E6, E7 y E8, con dos integrantes del equipo como anotadores (reportado como tal), y la línea base (R-006).
3. **En paralelo, para E9:** T-031 (syllabus real), T-040 y F-007 (textos legales y fechas), T-043 (despliegue) y la convocatoria.
4. **Cierre:** T-051, T-052 y el documento final.

## Evaluación y resultados

| ID | Pendiente | Funcionalidades | Estado | Responsable | Depende de | Peso |
| --- | --- | --- | --- | --- | --- | --- |
| R-005 | Ejecutar los experimentos E2 a E10 | • Ver la tabla [Experimentos](#experimentos)<br>• En `data/eval/gold` solo hay plantillas: no hay ninguna anotación real | ☐ Solo E1 ejecutado (2026-11-12) | — | Ver cada experimento | **Crítico** |
| R-006 | Cuaderno de métricas con la base real y línea base | • Correr `notebooks/metrics_cohort1.ipynb` con el usuario `smartmentor_metrics` (hoy solo corrió con datos sintéticos)<br>• Medir la línea base de la sección 4.4 del segundo corte (nunca se ejecutó)<br>• Guardar las cifras por fecha para mostrar «resultados en el tiempo» | ☐ | — | — | **Alto** |
| R-001 | Filtro de videos que descarta los videos en inglés | • `ai/app/application/content/course_generation.py`: el idioma queda fijo en `"es"` al publicar<br>• `ai/app/domain/video_ranking.py`: `english_allowed` siempre es `False`, así que todo video marcado `en` se descarta<br>• El nivel de inglés de la hoja de vida nunca llega al recomendador<br>• Es la causa de los temas sin candidatos (Claude Code, MLOps)<br>• Pantallas: D5e Videos del tema, E6 Tema | ☐ Verificado en `dev` el 2026-11-14 | — | — | **Alto**: bloquea E6 |
| R-002 | Normalización mínimo-máximo de la señal del perfil | • `ai/app/domain/leveling.py`, `normalized_priors`: sigue el hallazgo 1 del primer corte (una diferencia de 0,011 se vuelve 0 y 100)<br>• Construir la variante (c) de E4, con escala absoluta, para poder compararla | ☐ | — | — | **Alto**: afecta E4 |
| R-003 | La interfaz no envía eventos de uso | • La API ya recibe eventos (`POST …/events`, tabla `interaction_events`), pero la app nunca los envía (verificado en `app/src/clients` el 2026-11-14)<br>• Sin eso no se miden el tiempo en tarea (m27) ni los minutos ahorrados de H2<br>• Pantallas: E5, E6, E6b, E8 | ☐ | — | — | **Alto**: E9 y H2 |
| R-004 | Carga de apuntes para el RAG desde la interfaz | • Hoy la única fuente es el syllabus<br>• Sin apuntes no corre el diseño 2 × 2 de E5 (syllabus contra syllabus más apuntes)<br>• Pantallas: D1b / D2 (carga) y D5d (explicación) | ☐ | — | — | Medio: E5 |
| R-007 | Piezas del primer corte sin construir | • Recomendación de video por conceptos débiles de cada aprendiz (sin ella no se prueba H3)<br>• Índice bayesiano de calidad del video<br>• Capítulos de los cursos completos como candidatos<br>• Trabajo del aprendiz simulado con LLM (tiene prompt, no código)<br>• Ya están declarados como desvíos en el segundo corte: van como limitaciones y trabajo futuro | ✖ Fuera de esta cohorte | — | — | Medio |

### Experimentos

| Exp. | Qué mide | Estado | Responsable | Qué falta | Depende de |
| --- | --- | --- | --- | --- | --- |
| E1 | Flujo de punta a punta con Gemini real | ✔ Finalizado 2026-11-12 · `dev` (por la API) | Eduar Troyano | Repetirlo por la interfaz y con el syllabus real (T-032) | T-031, T-010 / T-011 |
| E2 | Estructuración del syllabus (F1 ≥ 0,85) | ☐ | — | Correr los 2 modelos × 3 repeticiones; el instructor corrige en D2 | Puede empezar con los 3 syllabus publicados; T-031 para el real |
| E3 | Preguntas válidas (≥ 80 %, κ ≥ 0,6) | ☐ | — | 80 ítems anotados a ciegas por dos personas en D5b | Dos anotadores (T-041) |
| E4 | Validez del diagnóstico (AUC ≥ 0,7) | ☐ | — | Datos de E9 y la variante (c) | R-002, E9 |
| E5 | Fidelidad y cobertura del RAG (≥ 0,8) | ☐ | — | Correr las condiciones; juicio de cobertura del experto | R-004 para el 2 × 2; la condición actual se puede medir ya |
| E6 | Videos por tema (P@3 ≥ 0,7) | ☐ | — | Juicio de dos jueces con la plantilla del conjunto de oro | R-001 |
| E7 | Juez LLM contra humano (QWK ≥ 0,6) | ☐ | — | ≥ 50 respuestas cortas calificadas a ciegas en D5c | T-041; respuestas de E9 o del equipo |
| E8 | Latencia, JSON inválido y costo | ◐ Hay datos: 354 llamadas, US$ 1,83 (2026-11-12) | Eduar Troyano | Cortarlo por tarea del aprendiz y por curso; actualizar después de B-013 | — |
| E9 | Prueba con 5 o 6 empleados (g ≥ 0,3, SUS ≥ 68) | ⛔ | — | Syllabus real, textos legales, fechas, despliegue y convocatoria | T-031, T-040, F-007, T-043, R-003 |
| E10 | Revisión del reporte con la organización | ⛔ | — | Confirmar el interlocutor | 👤 Dueño, E9 |
| E11 | Piloto comparativo (unos 175 por brazo) | ✖ Fase posterior | — | Diseñado y en parte construido | — |

## Producto: interfaz y flujo

| ID | Pendiente | Funcionalidades | Estado | Responsable | Depende de | Peso |
| --- | --- | --- | --- | --- | --- | --- |
| T-010 / T-011 | Flujo del aprendiz verificado en el navegador con la API real | • E1 Catálogo, E2 / E2b Perfil y hoja de vida<br>• E3 Diagnóstico, E4 Resultado, E4b Editar el objetivo<br>• E5 Ruta, E6 Tema, E6b / E6c Quiz, E7 / E7b / E7c Resultado, refuerzo e intentos agotados<br>• E8 Final, E9 Repaso, E9c Final con intentos agotados<br>• E10 Badge, E11 Mi progreso (con metas), E11b Autorizaciones, E12 Logros<br>• E13a / E13b Encuesta, E14 Retención<br>• U1a a U1d Pantallas de espera de la IA | ◐ Código en `dev` (PR 5 y PR 7). Recorrido en curso el 2026-11-14: E1 → inscripción → E3 → U1a → E4 hecho | Eduar Troyano | — | **Alto** |
| Riesgo B-009 | Streamlit 1.67: los widgets con `key` traían un valor viejo después de `st.stop()` | • Arreglado E4b (lo cancelado reaparecía) y D2b (al quitar un resultado de aprendizaje se guardaba el texto equivocado)<br>• Sin riesgo, con la razón anotada: nuevo curso (D1b a D2d), encuesta (E13a / E13b), quiz (E6b / E6c), final (E8), D5d y el resto<br>• Ya corregido antes: A3 / A3b (`38fcf00`, en `dev`) | ⏳ Finalizado 2026-11-14 · rama `fix/widgets-key-streamlit-167` (`3bc10f3`, `5b9479f`; 748 pruebas) | Eduar Troyano | — | Medio |
| B-009 menores | Cuatro casos menores de estado de widgets que no vienen de la subida | • A3c abierto por URL directa: la casilla de datos de A3 vuelve sin marcar<br>• E13b: el comentario se pierde con «Anterior»<br>• E2 / E15: un borrador sin guardar puede sobrevivir al pasar por E4<br>• D1c: «Volver a mis cursos» no borra `nc-draft` | ☐ | — | — | Bajo |
| B-021 | Bloqueo al editar el objetivo | • E4 → E4b: la página se queda en «Conectando», con la CPU alta y sin llamar a la API | ◐ Reproducción en curso el 2026-11-14 | Eduar Troyano | — | Medio |
| R-008 | Lentitud de la API con Neon (parte de B-018) | • Cada petición del aprendiz hace unas 16 consultas seguidas a Neon (unos 110 ms cada una), cerca de 1,8 s por `GET /me/enrollments/{id}`<br>• La app ya evita recargas; falta bajar las consultas en la API | ☐ | — | — | Medio: experiencia en E9 |
| B-025 👤 | Repasar temas aprobados | **Qué decidir:** si la API entrega el contenido de los temas aprobados u omitidos para repasarlos (hoy responde `409 STEP_NOT_AVAILABLE`), o si el repaso queda solo en el aviso actual<br>**Pantallas de Figma a revisar:**<br>• [E9 Repaso dirigido](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=5-280) (`5:280`): el botón «Repasar tema» de los temas débiles<br>• [E5 Vista de ruta](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=5-148) (`5:148`): abrir un tema aprobado u omitido<br>• [E6 Tema (video + texto + quiz)](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=5-209) (`5:209`): qué se muestra al repasar (¿sin quiz?) | ◐ Arreglo parcial en la app | Eduar Troyano | Dueño | Bajo |
| T-016 👤 | Vista de la ruta fija | **Qué decidir:** si se puede crear, en el piloto local, un aprendiz del grupo de comparación (escribe en la base del piloto)<br>**Pantallas de Figma a revisar:**<br>• [E5b Vista de ruta · Ruta fija](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=96-657) (`96:657`): lo que ve el aprendiz del grupo de comparación<br>• [AD4b Vista previa de la ruta fija](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=110-885) (`110:885`): ya hecha, sirve de referencia<br>• [E5 Vista de ruta](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=5-148) (`5:148`): para comparar con la ruta adaptativa | ◐ AD4b hecho; E5b revisada con datos de ejemplo (V-043) | Eduar Troyano | Dueño | Bajo: es para E11 |
| T-015 | Pantallas del administrador | • AD1 Usuarios, AD2 LLM, AD3 Métricas, AD4 / AD4b Piloto, AD5 Cursos, C4 Prompts<br>• Comprobadas contra la API local real (solo lecturas): 50 logs del LLM, 29 métricas, 15 inscripciones y roles se leen bien<br>• Prueba nueva: AD4 sin piloto muestra el aviso y no ofrece controles<br>• El formulario para crear el piloto sigue en F-013 | ✔ Finalizado 2026-11-14 · `dev` (AD1 a AD5 y C4); la prueba nueva en rama `feature/admin-y-fixtures` (`0c6e964`) | Eduar Troyano | — | Bajo |
| F-002 (T-021) | Catálogo vacío | • [E1 Catálogo de rutas](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=5-2) (`5:2`): mensaje «Todavía no hay rutas publicadas.» (decisión del dueño del 2026-11-14; ya existía en `catalog.py`) | ✔ Finalizado 2026-11-14 · `dev` | Eduar Troyano | — | Bajo |
| F-003 (T-022) 👤 | Instructor sin cursos | **Qué decidir:** el diseño del estado vacío, o aprobar que se resuelva con el estilo actual<br>**Pantallas de Figma a revisar:**<br>• [D1 Instructor · Mis cursos](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=3-2) (`3:2`): el primer ingreso<br>• [D1b Nuevo curso](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=95-538) (`95:538`): el enlace para crear el primer curso | ⛔ Falta el diseño o la aprobación | — | Dueño | Bajo |
| F-004 (T-023) | Menú de perfil con cambio de rol (CU-35) | • El menú de la cuenta muestra nombre, correo, **Rol activo ✓** y, si el usuario tiene más roles (`GET /me`), **Cambiar de perfil** con cada uno, y «Cerrar sesión»<br>• Referencia: [A1 Selector de rol](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=2-169) (`2:169`) y [E15 Mi perfil](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=123-1031) (`123:1031`)<br>• Para verlo en 8501 hace falta un usuario con dos roles (se asignan en AD1) | ⏳ Finalizado 2026-11-14 · rama `feature/menu-perfil-roles` (`e6c6782`; 747 pruebas) | Eduar Troyano | — | Bajo |
| F-013 👤 | AD4 sin piloto | **Qué decidir:** si se agrega un formulario para crear el piloto (ruta y fechas); hoy la página muestra un aviso<br>**Pantallas de Figma a revisar:**<br>• [AD4 Admin · Piloto](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=96-1083) (`96:1083`) | ⛔ Falta el diseño o la aprobación | — | Dueño | Bajo |
| T-024 | Datos de ejemplo copiados de Figma | • F-008 (calidad del video antes de calificar) y F-010 («Embedding» por «Revisión»): ya resueltos en la app<br>• 👤 F-006 (datos de Laura y de Julián Pérez entre E5, D3, D4 y D4b): la contradicción viene de Figma y las pruebas que comparan con Figma la exigen. **Qué decidir:** corregir Figma o aceptar la diferencia. Pantallas: D3, D4 y D4b | ◐ F-008 y F-010 ✔ en `dev`; F-006 depende del dueño | Eduar Troyano | Dueño (F-006) | Bajo |
| T-033 | Nota del LLM en el navegador | • Comprobar que la nota aparece después de guardar (cambio 6 del PR 3) | ◐ En curso el 2026-11-14 (depende del OTP del instructor local) | Eduar Troyano | — | Bajo |
| T-034 | Revisión visual frente a Figma | • Hecho antes: E1, E6, A6, A7, D1 a D5f y AD1 a AD5<br>• Hecho el 2026-11-14: E2 a E15, U1a y A3b / A3c, con datos de ejemplo (25 diferencias, V-033 a V-057)<br>• No comparables: A3 (el registro es de Keycloak), U1b a U1d (mismo componente que U1a, textos iguales a Figma) | ✔ Revisión finalizada 2026-11-14 (sin rama: no cambia código) | Eduar Troyano | — | Bajo |
| V-033 a V-057 | Arreglos visuales del aprendiz | • **Alta:** V-033 preguntas de E3, E6b, E8 y E14 (la pregunta como título y las opciones en tarjeta); V-050 E11 Mi progreso (tarjetas de metas y datos, y barras de avance)<br>• **Media:** barra de progreso (V-034), avisos y tarjeta del quiz (V-035, V-036), botones alineados a la derecha (V-037), E2b / E15 en dos columnas (V-038), E4b y E11b como ventana modal (V-041, V-051), filas de la ruta E5 (V-042), E7, E7b, E7c y E9c (V-045 a V-047), E12 en rejilla (V-052), escala Likert de E13 (V-053), E14 (V-054)<br>• **Baja:** V-039, V-040, V-043, V-044, V-048, V-049, V-055<br>• 👤 **Qué decidir:** V-049 («Descargar JSON» y «Verificación pública» en E10), V-053 (botón verde de E13b frente al color por rol), V-056 (A3b sin participar por omisión) y V-057 (A3c dice «la organización» y no «la universidad») | ☐ | — | Dueño (V-049, V-053, V-056, V-057) | Medio |

## Hito, piloto y cierre

| ID | Pendiente | Funcionalidades | Estado | Responsable | Depende de | Peso |
| --- | --- | --- | --- | --- | --- | --- |
| T-031 👤 | Syllabus real del curso piloto | **Qué entregar:** el syllabus real (Carlos Villada)<br>**Pantallas de Figma a revisar con el syllabus cargado:**<br>• [D1b Nuevo curso](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=95-538) (`95:538`): carga del syllabus<br>• [D1c Carga · Extrayendo temas](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=95-592) (`95:592`): espera de la IA<br>• [D2 Curso y syllabus](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=6-2) (`6:2`): temas, prerrequisitos y resultados extraídos | ⛔ | — | Dueño (Carlos Villada) | **Alto**: E2 y E9 |
| T-032 | Corrida completa con el syllabus real | • Syllabus → temas → contenido (RAG y videos) → diagnóstico → ruta → quiz → final → badge, con costo y latencia<br>• Ya se hizo por la API (E1); falta por la interfaz | ◐ | Eduar Troyano | T-031, T-010 / T-011 | Alto |
| F-007 👤 | **Fechas del piloto vencidas** | **Qué decidir:** las fechas nuevas del piloto<br>**Pantallas de Figma a revisar:**<br>• [A3b Consentimiento informado](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=103-725) (`103:725`): dice del 2 al 15 de noviembre de 2026<br>• Hay que corregirlas antes de convocar a nadie | ☐ | — | Dueño | **Alto**: bloquea E9 |
| T-040 👤 | Textos legales | **Qué decidir:** los textos revisados por jurídica (P-09), la organización responsable y la fecha del piloto (F-007: Figma dice del 2 al 15 de noviembre de 2026, que ya pasó)<br>**Pantallas de Figma a revisar:**<br>• [A3 Registro aprendiz](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=2-225) (`2:225`): autorización de datos (Ley 1581) y casilla del piloto<br>• [A3b Consentimiento informado](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=103-725) (`103:725`): texto del piloto, fechas y decisión de participar<br>• [A3c Tus datos y tus derechos](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=121-903) (`121:903`): derechos y quién ve cada dato<br>• [E11b Gestionar autorizaciones](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=122-962) (`122:962`): retirar el consentimiento | ⛔ | — | Dueño y jurídica | **Alto** |
| T-041 | Anotación de expertos y calificación humana | • D5b Cola de anotación con personas reales<br>• D5c Calificación humana frente al LLM como juez | ☐ | — | T-032 | **Alto**: E3 y E7 |
| T-042 | Prueba de usabilidad | • Guion de tareas y cuestionario SUS<br>• Registro de resultados | ☐ | — | T-034 | Alto |
| T-043 👤 | Prueba con usuarios y piloto (15 a 30 aprendices) | **Qué decidir:** dónde se despliega y quién lo opera (DEF-16 / D-06: red de la universidad o servicio gestionado), las fechas y cómo se reclutan los aprendices<br>**Pantallas de Figma a revisar:**<br>• [AD4 Admin · Piloto](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=96-1083) (`96:1083`): configuración, grupos y estado del piloto<br>• [AD4b Vista previa de la ruta fija](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=110-885) (`110:885`) y [E5b Ruta fija](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=96-657) (`96:657`): grupo de comparación<br>• [A3b Consentimiento informado](https://www.figma.com/design/atp2fZdSolEoaww3n9jRLg/?node-id=103-725) (`103:725`): fechas del piloto (depende de T-040) | ⛔ | — | Dueño, T-032 y T-040 | **Alto** |
| T-050 | Endurecimiento antes de usar datos reales | • Rotar los secretos del historial de git y limpiarlo<br>• Quitar el cliente `smartmentor-dev-tools`<br>• Keycloak en `start` con HTTPS y host fijo | ☐ | — | — | Medio: obligatorio antes de E9 |
| T-051 | Brief v2 | • Redactarlo a partir de las bitácoras F00 a F09 | ☐ | — | — | Medio |
| T-052 | Release | • Etiqueta `v1.0-cohorte1` y notas de la versión | ☐ | — | T-051 | Medio |
| R-009 | Documentos de estado desactualizados | • `HANDOFF.md`, `checklist.md`, `BUGS.md`, `SUBIDAS.md`, `app/README.md` y `CHANGELOG.md` al día con los PR 5 y 7<br>• `HOJA_DE_RUTA.md` con la fecha de actualización del 2026-11-14<br>• El commit `75d4f17` («ajuste checjlist», cambia `topic.py`) ya está en `dev`: no se renombra para no reescribir la historia | ⬆ Finalizado 2026-11-14 · rama `feature/seguimiento-pr5-en-dev` | Eduar Troyano | — | Bajo |

## Deuda técnica sin tarea

| Tema | Funcionalidad afectada |
| --- | --- |
| Renovación del token por redirección | Al renovar la sesión, la app vuelve a la página de inicio |
| `GET /jobs/{id}` siempre devuelve `next_action` en `null` (B-012) | La app vuelve a leer la inscripción después de cada trabajo de IA |
| El lease de los trabajos de IA (1800 s) no se renueva mientras corren | Generación de bancos de preguntas largos |
| Las pruebas no miden la cobertura | Toda la base de código |

Las mejoras M-003 a M-008 esperan la decisión del dueño ([`MEJORAS.md`](MEJORAS.md)).

## Quién vio cada punto

| Visto por | IDs |
| --- | --- |
| Las dos revisiones | T-010 / T-011, B-021, B-025, riesgo B-009, T-021 a T-023, T-031, T-040, T-041, T-042, T-043, T-050, T-051, T-052, B-012, cobertura |
| Solo la revisión de producto | F-007, T-016, T-015, T-024, T-033, T-034, renovación del token, lease de los trabajos |
| Solo la revisión de evaluación | R-001 a R-009 |
| Nuevos del 2026-11-14 (agentes de verificación) | B-009 menores, V-033 a V-057 |
