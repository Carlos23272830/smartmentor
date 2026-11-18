# Brief v2 del proyecto: SmartMentor, plataforma de cursos adaptativos generados con IA

Proyecto de grado · Maestría en Ciencia de Datos · Cierre de la cohorte 1 · Noviembre de 2026 · Documento vivo: cada cohorte lo actualiza.

Este documento compara el [brief original](../brief.md) (octubre de 2026) con lo que la cohorte 1 construyó y midió. No reemplaza al original: lo contrasta. Las fuentes son las bitácoras de [`proyecto/cohorte_1/bitacora/`](bitacora/), los [ADR](../../docs/adr/README.md), los [resultados de los experimentos](../../docs/evaluation/results/) y el seguimiento de [`proyecto/cohorte_1/seguimiento/`](seguimiento/README.md).

## 1. Resumen ejecutivo

SmartMentor genera rutas de aprendizaje personalizadas a partir de un syllabus. El instructor carga el syllabus y, si quiere, apuntes o lecturas. La IA extrae los temas y sus prerrequisitos, y el instructor los revisa. Al publicar el curso, la IA genera explicaciones con RAG, busca videos y crea los bancos de preguntas. El aprendiz completa su perfil, presenta un diagnóstico, confirma un objetivo, sigue una ruta que omite lo que ya domina y obtiene un badge al aprobar la evaluación final.

**Estado al cierre de la cohorte 1:**

- **El flujo completo funciona de punta a punta** con el LLM real (Gemini), en un stack de cinco servicios con Docker Compose y una base compartida en Neon.
- **Se construyeron las 96 pantallas del prototipo de Figma v3** para el aprendiz, el instructor y el administrador.
- **Se ejecutaron seis experimentos de calidad** (E2, E3, E5, E6, E7 y E8). Su lectura en una línea:
  - funcionan la extracción de temas, el recomendador de videos y el juez de respuestas cortas;
  - no llegan a la meta la calidad de las preguntas ni los prerrequisitos extraídos.
- **Los resultados son indicativos.** Los jueces fueron agentes de IA, no expertos humanos, y los datos son de prueba.
- **El piloto con usuarios reales pasa a la siguiente fase**, junto con los experimentos que dependen de él (E4, E9 y E10).

## 2. Objetivos: planteado frente a logrado

| # | Objetivo específico del brief | Estado | Evidencia y comentario |
| --- | --- | --- | --- |
| 1 | Modelar el syllabus como un grafo de temas con prerrequisitos y resultados de aprendizaje medibles | ✔ Logrado, con una salvedad | La IA extrae el DAG y el instructor lo revisa en D2 y D2d. E2: F1 de temas 1,000 ✔; F1 de prerrequisitos 0,58 a 0,69 ✖. Por eso la revisión del instructor es obligatoria |
| 2 | Generar la prueba diagnóstica y estimar el nivel por tema | ✔ Construido · ⏭ validación pendiente | El diagnóstico y la estimación de nivel funcionan. Su validez (E4, AUC ≥ 0,7) necesita los datos del piloto. En la cohorte de desarrollo el AUC fue 0,635, con apenas 14 pares |
| 3 | Definir el objetivo combinando la meta de la ruta, el perfil y el diagnóstico | ✔ Logrado | La IA propone el objetivo en tres partes (verbo de Bloom, contenido y criterio), con 46 verbos válidos. El aprendiz lo confirma o lo edita en E4b, y la propuesta original se guarda aparte (B-033) |
| 4 | Generar y curar recursos (video y texto) y evaluaciones alineadas con Bloom | ✔ Construido · ✖ calidad de preguntas bajo la meta | RAG con citas, videos con curaduría del instructor y bancos de ítems revisados antes de publicar. E5 (fidelidad 0,889) ✔ y E6 (P@3 0,718) ✔; E3 (28,8 % y luego 60 % de ítems válidos) ✖ |
| 5 | Evaluar la calidad del contenido y la efectividad de la ruta con métricas y un piloto | ◐ Parcial | Hay métricas del sistema con jueces-agente y un cuaderno de métricas que corre sobre la base real. El piloto y las métricas de aprendizaje (Hake, d de Cohen y SUS con personas reales) pasan a la siguiente fase |

## 3. Alcance del MVP: planteado frente a construido

| El brief incluía | Qué se construyó |
| --- | --- |
| Gestión básica de estudiantes, cursos y rutas (CRUD, roles admin y estudiante) | ✔ Tres roles neutros, `learner`, `instructor` y `admin` (ADR 0021), con un selector de perfil para quien tiene varios. Las etiquetas visibles se configuran por contexto |
| Carga del syllabus (PDF o texto) y extracción de temas con LLM, validada por el docente | ✔ D1b a D2d: carga, extracción asíncrona, revisión de temas y prerrequisitos, grafo y registro de correcciones para el F1 |
| Perfil en texto libre y prueba diagnóstica generada | ✔ Perfil y hoja de vida (E2 y E2b) y diagnóstico con estimación de nivel |
| Recursos: videos de YouTube y texto con RAG | ✔ Las fuentes del RAG son el syllabus y **los apuntes que sube el instructor** (R-004 y R-010, agregado en esta cohorte). Videos con curaduría del instructor (ADR 0016) y según el nivel de inglés del aprendiz |
| Evaluaciones de opción múltiple y respuesta corta con calificación automática | ✔ Banco de ítems generado y revisado antes de publicar (ADR 0015). Las respuestas cortas las califica el LLM con rúbrica, y hay una cola de calificación humana (D5c) |
| Badge digital (imagen y JSON tipo Open Badges) | ✔ E10 y E12, con verificación pública del JSON |
| Dashboard simple de avance para el docente | ✔ D3 y D4, y además métricas globales y log del LLM para el administrador (AD2 y AD3) |

**Lo que se agregó sin estar en el brief:**

- autenticación con Keycloak y OTP por rol;
- consentimiento informado y derechos sobre los datos (Ley 1581);
- anotación ciega de ítems (D5b);
- calificación humana (D5c);
- encuesta final y prueba de retención;
- presupuesto en dólares por tarea del LLM.

**Lo que se retiró:** el módulo de administración del piloto (AD4 y AD4b, F-013), que pasa a la siguiente fase con el piloto.

## 4. Arquitectura y stack: sugerido frente a elegido

El brief sugería cuatro capas en Python: Streamlit, FastAPI, una capa de IA con LlamaIndex y PostgreSQL con pgvector. La cohorte mantuvo la idea, pero separó la IA en un servicio propio y agregó identidad y trabajos asíncronos.

| Pieza | El brief sugería | Se eligió | Por qué (ADR) |
| --- | --- | --- | --- |
| Base de datos | Supabase o PostgreSQL gestionado con pgvector | PostgreSQL 17 con pgvector; en local con Docker y compartida en Neon para el equipo | Una sola base relacional y vectorial (0001) |
| Esquema | — | Liquibase, con auditoría y `rollback` por changeset | Esquema versionado y reproducible (0002 y 0007) |
| API de negocio | FastAPI | FastAPI, organizada por dominio | Reglas de negocio en la API, no en la interfaz (0003 y 0017) |
| Capa de IA | Dentro de la API, con LlamaIndex | **Microservicio aparte (`ai/`)** con API y trabajador, sin LlamaIndex | Aislar y medir la IA. El RAG es una consulta SQL sobre tablas de Liquibase, sin tablas propias de LlamaIndex (0008, 0009 y 0013) |
| Trabajos largos | — | Cola en PostgreSQL, con lease y reintentos, sin broker | Menos piezas que operar (0010) |
| LLM y embeddings | Claude, GPT u open source | Gemini (`flash` y `flash-lite`) con `gemini-embedding-001` (768 dimensiones) | Costo y salidas estructuradas (0011 y 0012) |
| Identidad | — | Keycloak, con realm versionado, OTP por rol y *client credentials* entre servicios | Seguridad y roles (0004, 0005 y 0014) |
| Interfaz | Streamlit o Next.js | Streamlit 1.67, rehecho desde Figma v3 con CSS propio y tokens | Rapidez, y fidelidad al prototipo (0006 y 0017) |
| Datos personales | Anonimización (Ley 1581) | Consentimiento, supresión y auditoría; usuarios de base de datos de mínimo privilegio | 0018 y 0019 |
| Despliegue | Render, Railway o Hugging Face Spaces | Docker Compose; el destino del piloto se decide en la siguiente fase | 0020 |

**Decisiones del brief que se mantuvieron:** salidas estructuradas validadas con esquemas, prompts versionados como código (13 en `prompts/catalog.yaml`, con hash), caché del contenido generado por tema y registro de cada llamada (prompt, modelo, tokens, costo y latencia).

## 5. Modelo de datos

El brief proponía 11 entidades. La versión `v2.0.x` tiene **40 tablas de negocio y de IA** y 35 tablas `_audit`. Detalle en [`database/README.md`](../../database/README.md).

Las diferencias principales:

- **Resultados de aprendizaje y prerrequisitos en tablas propias.** El brief los guardaba como listas dentro del tema.
- **Banco de ítems separado de los intentos**, con anotaciones (`item_annotations`) y calificaciones humanas (`human_gradings`) para medir la calidad.
- **Capa de IA con tablas propias:** `ai_jobs`, `ai_generation_cache`, `ai_embeddings`, `source_documents`, `document_chunks` y `llm_call_logs`. Más `course_materials`, los apuntes del instructor (R-004).
- **Tablas de ética y piloto:** `consents`, `data_subject_requests`, `pilots`, `survey_responses` e `interaction_events`.

## 6. Proceso y cronograma: plan de 8 semanas frente a lo ocurrido

El brief planeaba 8 semanas: prototipo, fundamentos, flujo completo, piloto y cierre. La cohorte avanzó por fases técnicas, y el piloto no llegó a ejecutarse.

| Fase | Contenido | Estado |
| --- | --- | --- |
| F0 | Prototipo, wireframes, Mago de Oz y estándares del repositorio | ✔ |
| F1 | ADR, contratos de API y de IA, prompts y casos de uso | ✔ |
| F2 | Base `v2.0.0` | ✔ |
| F3 | API: identidad, cursos, rutas, evaluaciones, contenido y piloto | ✔ |
| F4 y F5 | Servicio de IA: base y contenido (RAG, videos y bancos de ítems) | ✔ |
| F6 | Integración de punta a punta con el LLM real | ✔ El 2026-11-12, un curso creado desde la interfaz y recorrido por 4 aprendices simulados: 354 llamadas por US$ 1,83 |
| F7 | Interfaz v3 (96 pantallas) | ✔ |
| F8 | Keycloak, infraestructura y CI | ✔ |
| F9 | Herramientas de evaluación y experimentos | ✔ Herramientas · ◐ experimentos con jueces-agente · ⏭ piloto |
| F10 y F11 | Revisión final, brief v2 y traspaso | ◐ Este documento |

**Forma de trabajo:**

- Cada tarea se anota en `proyecto/cohorte_1/seguimiento/TRAZABILIDAD.md` con un responsable.
- Los cambios llegan a `dev` por pull request (82 fusionados al 2026-11-16), con una CI que corre Ruff, mypy y pytest en los tres servicios, más Liquibase, los prompts, el realm, gitleaks y Trivy.
- El seguimiento cierra con 98 puntos: 84 realizados, 9 migrados a la siguiente fase y 5 abiertos.

**Desvío principal frente al plan:** el hito de la semana 4 («flujo completo») se cumplió más tarde de lo planeado, y el piloto no alcanzó a ejecutarse. Siguiendo la regla del brief («recortar alcance antes que mover el piloto sin datos»), la cohorte cerró la fase con experimentos sobre datos de prueba y dejó el piloto preparado para la siguiente.

## 7. Resultados de los experimentos

Todos los resultados se obtuvieron con **jueces-agente** (Claude Opus y Sonnet), a ciegas y sobre datos de prueba. Resumen completo: [`resumen-r005-2026-11-16.md`](../../docs/evaluation/results/resumen-r005-2026-11-16.md).

### 7.1 Métricas del sistema

| Experimento | Métrica del brief | Meta | Resultado | Cumple |
| --- | --- | --- | --- | --- |
| [E2](../../docs/evaluation/results/e2-2026-11-16.md) · Estructuración del syllabus | F1 de temas y prerrequisitos | F1 ≥ 0,85 | Temas 1,000; prerrequisitos 0,694 (`flash-lite`) y 0,578 (`flash`) | ✔ temas · ✖ prerrequisitos |
| [E3](../../docs/evaluation/results/e3-2026-11-16.md) · Preguntas válidas | % válidas y κ de Cohen | ≥ 80 % y κ ≥ 0,6 | 28,8 % válidas con ambos jueces; κ 0,704 | ✖ calidad · ✔ acuerdo |
| [E3b](../../docs/evaluation/results/e3b-2026-11-16.md) · Preguntas tras B-062 | Igual que E3 | Igual que E3 | De 32,5 % a 60,0 % válidas (prompt `topic_quiz` v2, más formato y mezcla de opciones en el código); κ 0,264 | ✖ calidad (mejora) · ✖ acuerdo |
| [E5](../../docs/evaluation/results/e5-2026-11-16.md) y [E5b](../../docs/evaluation/results/e5b-2026-11-16.md) · Fidelidad del RAG | Fidelidad a las fuentes | ≥ 0,8 | Media 0,889 (un tema en 0,667). Con TOP_K = 10 entraron fragmentos de las lecturas, pero la comparación con y sin lecturas no fue concluyente | ✔ media · sin concluir |
| [E6](../../docs/evaluation/results/e6-2026-11-16.md) · Videos por tema | Precision@3 | ≥ 0,7 | P@3 0,718; κ 0,766 entre jueces | ✔ |
| [E7](../../docs/evaluation/results/e7-2026-11-16.md) · Calificación automática | QWK juez del sistema frente a referencia | ≥ 0,6 | QWK 0,998, con una muestra polarizada (casi sin respuestas parciales) | ✔ con salvedad |
| [E8](../../docs/evaluation/results/e8-2026-11-15.md) · Desempeño técnico | Latencia p95 y JSON inválido | p95 < 20 s; JSON inválido < 2 % | p95 global 120,1 s ✖ (bancos de preguntas y explicaciones; 28 timeouts a los 120 s). La calificación de respuestas cortas (2,1 s) y el cierre del diagnóstico (9,2 s) sí cumplen. JSON inválido 0,8 % ✔ | ✖ latencia de generación · ✔ camino del aprendiz · ✔ JSON |

**Costo:**

- todo el log del LLM: US$ 1,85 en 372 llamadas;
- costo medio por inscripción: US$ 0,040;
- los experimentos: unos US$ 0,16 de un tope de US$ 3.

El 68 % del costo lo generan los bancos de preguntas, que se pagan una vez al publicar el curso, no por cada aprendiz.

### 7.2 Métricas de los estudiantes (cohorte de desarrollo)

El [cuaderno de métricas](../../docs/evaluation/results/metrics-cohort1-2026-11-15.md) corre contra la base real con un usuario de solo lectura. Pero la cohorte es de desarrollo: 9 inscripciones analizadas de **3 personas**, más aprendices simulados. Sirve para comprobar que el cálculo funciona, **no para afirmar efectos**.

| Métrica | Valor | Meta |
| --- | --- | --- |
| Ganancia de Hake media | −0,109 (7 inscripciones) | g ≥ 0,3 |
| Aprobación al primer intento | 57,1 % (14 pasos) | 60 % a 85 % |
| Intentos hasta aprobar | 1,33 | ≤ 1,8 |
| Finalización y badge | 77,8 % | ≥ 60 % |
| Percepción (Likert 1 a 5) | Satisfacción 4,43, utilidad 4,57 y autoeficacia 4,43 (7 encuestas) | Media ≥ 4 |
| SUS | 80,7 (7 encuestas) | ≥ 68 |
| Temas omitidos por persona | 2,33 (21 de 42 pasos) | Reportar |
| d de Cohen, tiempo en tarea y retención | Sin datos: no hubo sorteo de grupos, eventos en inscripciones analizadas ni segunda medición | Reportar |

### 7.3 Lectura de conjunto

- **Funciona:** la estructuración de temas (E2), el recomendador de videos (E6), el juez de respuestas cortas en casos claros (E7) y el camino que el aprendiz espera (E8).
- **No llega a la meta:** la calidad de las preguntas, sobre todo por distractores triviales (E3; mejora con B-062), los prerrequisitos que extrae la IA (E2), un tema concreto de E5 (ETL/ELT) y la latencia de generar bancos y explicaciones (E8).
- **No se pudo concluir:** si las lecturas mejoran las explicaciones (E5 y E5b) y cómo se comporta el juez en respuestas parciales (E7).

## 8. Lo que pasa a la siguiente fase

El piloto con usuarios reales no se alcanzó en esta fase. Pasan 10 puntos del seguimiento ([`TRAZABILIDAD.md`](seguimiento/TRAZABILIDAD.md), sección «Migrados a la siguiente fase»):

| ID | Qué | Por qué pasa |
| --- | --- | --- |
| T-043 | Piloto con 15 a 30 aprendices: dónde se despliega, quién lo opera y cómo se recluta | No se alcanza en esta fase |
| E9 | Prueba con 5 o 6 empleados (g ≥ 0,3 y SUS ≥ 68) | Es parte del piloto |
| E4 | Validez del diagnóstico (AUC ≥ 0,7) | Necesita los datos de E9 |
| E10 | Revisión del reporte con la organización | Depende de E9 y del interlocutor |
| T-040 | Textos legales revisados por jurídica | Requisito del piloto con datos reales. Mientras tanto, la app cita a «la organización responsable» (configurable) |
| F-007 | Fechas del piloto | Las del prototipo vencieron; se fijan al retomarlo (`PILOT_WINDOW_TEXT`) |
| T-031 | Syllabus real del curso piloto | Los experimentos usaron los cursos ya cargados |
| T-050 | Endurecimiento antes de usar datos reales: rotar secretos, quitar el cliente de desarrollo y Keycloak con HTTPS y OTP | Obligatorio antes de E9 |
| T-042 | Prueba de usabilidad (guion y SUS) | Se hace con usuarios reales |
| B-049 | Explicación alterna al reprobar un quiz («Otra forma de verlo», E7b) | El prompt y la tarea de IA ya existen; falta que la API la pida y la guarde. Sirve sobre todo con aprendices reales |

## 9. Retos y dificultades

| Reto | Qué pasó | Cómo se resolvió o qué se aprendió |
| --- | --- | --- |
| Tope de gasto y timeouts del LLM | El tope de Google AI Studio detuvo F6 un tiempo, y los bancos de preguntas superaban el límite de 120 s (B-013) | Timeout de 240 s, lease de 1800 s, presupuesto en dólares por tarea y registro de cada llamada |
| Latencia con la base en la nube | Cada petición hacía unas 16 consultas a Neon, de unos 110 ms cada una (R-008, B-056 y B-063) | Se redujeron las consultas y se leyó en lote en los listados |
| Trabajo en paralelo y mezclas | Fusiones automáticas que duplicaron código (por ejemplo, el doble envío multipart que corrigió T-055, PR 44) | Pull requests revisados, CI obligatoria y asignación previa en TRAZABILIDAD.md |
| Diferencias entre Windows y Linux | Los prompts descargados con CRLF cambiaban su hash y el trabajador de IA no arrancaba | Saltos de línea LF para `prompts/` (arreglo local documentado como deuda técnica) |
| Configuración de identidad | Un realm de Keycloak antiguo dejaba entrar sin OTP (B-035) | En local se acepta; en QA y producción el OTP es obligatorio (nota de activación) |
| Dependencias | Vulnerabilidades en `pillow` y `certifi` (B-009) | Subida a Streamlit 1.67, revisando el cambio de comportamiento de los widgets |
| Fidelidad al prototipo | 96 pantallas con decenas de diferencias visuales (G-001) | Revisión pantalla por pantalla con registro de diferencias (V-001 en adelante) |
| Calidad de las preguntas | Distractores triviales, formato roto y la respuesta casi siempre en la primera opción (B-062) | Prompt v2, limpieza de formato y mezcla de opciones en el código (E3b: de 32,5 % a 60 %) |

## 10. Limitaciones

1. **Los jueces fueron agentes de IA, no expertos humanos.** E3, E6 y E7 usaron Claude Opus y Sonnet como evaluadores ciegos. El κ mide el acuerdo entre agentes, que comparten sesgos de familia; no mide la validez frente a un experto. E7 es «juez del sistema (Gemini) frente a juez de referencia (Claude)», no «LLM frente a humano».
2. **Datos de prueba, no un piloto.** Las métricas de estudiantes salen de 3 personas y aprendices simulados. Ningún resultado de aprendizaje se puede generalizar.
3. **Muestras pequeñas o sesgadas:**
   - E5b tiene una sola generación por condición;
   - la muestra de E7 está polarizada;
   - el JSON inválido por tarea se apoya en muy pocas llamadas (por ejemplo, 5 en `syllabus.structure`).
4. **La fidelidad del RAG la mide el mismo modelo que genera el texto.** No se usó RAGAS ni una verificación independiente.
5. **Métricas sin datos:** d de Cohen (no hubo sorteo de grupos), tiempo en tarea, retención y discriminación de ítems (ningún ítem llegó a 10 respuestas).
6. **El F1 de E2 se mide contra lo que dejó el instructor.** En cursos de prueba, el instructor pudo no editar nada, así que el F1 de 1,000 de la cohorte no prueba cuánto trabajo evita la IA.
7. **Piezas del diseño que no se construyeron** (R-007, declaradas como trabajo futuro): la recomendación de videos por conceptos débiles de cada aprendiz, el índice bayesiano de calidad del video, los capítulos de cursos completos como candidatos y el aprendiz simulado con LLM como código del sistema.

## 11. Riesgos, ética y protección de datos

Los riesgos del brief siguen vigentes. Esta cohorte agregó:

- **Ley 1581:** consentimiento activo (por omisión, «no participar» en el piloto), derechos sobre los datos (A3c y E11b), supresión con limpieza de auditoría y seudonimización antes de enviar datos al LLM (ADR 0018).
- **Mínimo privilegio:** un usuario de base de datos por servicio y otro de solo lectura para métricas (ADR 0019).
- **Antes de usar datos reales (T-050):** rotar los secretos que estuvieron en el historial de git, quitar el cliente de desarrollo `smartmentor-dev-tools`, Keycloak en modo `start` con HTTPS y OTP obligatorio para instructor y administrador.
- **Transparencia:** el aprendiz sabe que el contenido lo genera la IA, y cada explicación cita sus fuentes.
- **Supervisión humana:** el instructor revisa el syllabus, los ítems, los videos y los textos antes de publicar.

## 12. Recomendaciones para la cohorte 2

1. **Calibración humana:** que una o dos personas expertas repitan 15 a 20 elementos de E3, E6 y E7 y se compare su juicio con el de los jueces-agente.
2. **Ejecutar el piloto:** cerrar T-040, F-007, T-043 y T-050 y correr E9, E4 y E10, con grupo de control (ruta fija) para la d de Cohen.
3. **Calidad de las preguntas:** llevar las reglas del prompt v2 al diagnóstico y a la evaluación final, y medir un prompt v3 (nivel de Bloom y precisión técnica).
4. **Prerrequisitos:** mejorar su extracción o hacer más visible su revisión en D2.
5. **RAG:** probar lecturas más cercanas a cada tema o más fragmentos recuperados, repetir E5 con varias generaciones por condición y medir con un verificador independiente.
6. **Métricas pendientes:** pedir `estimated_minutes` en la extracción del syllabus, marcar `analysis_included` según el consentimiento y dar a métricas acceso de lectura a `assessment_items` (T-057).
7. **Trabajo futuro del brief:** pruebas adaptativas (IRT/CAT), knowledge tracing (BKT o DKT) y la explicación alterna al reprobar un quiz (B-049).

## 13. Referencias

- Las referencias científicas del [brief original](../brief.md#referencias-científicas) siguen vigentes.
- Decisiones de arquitectura: [`docs/adr/`](../../docs/adr/README.md) (ADR 0001 a 0021).
- Resultados: [`docs/evaluation/results/`](../../docs/evaluation/results/) y [definición de métricas](../../docs/evaluation/metrics.md).
- Bitácoras de fase: [`proyecto/cohorte_1/bitacora/`](bitacora/) (F00 a F09; la evidencia de F6 está en la [hoja de ruta](seguimiento/HOJA_DE_RUTA.md#evidencia-de-f6-2026-11-12)).
- Seguimiento: [`proyecto/cohorte_1/seguimiento/TRAZABILIDAD.md`](seguimiento/TRAZABILIDAD.md).
