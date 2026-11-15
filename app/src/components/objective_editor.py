"""Editor del objetivo (E4b): verbo de Bloom + contenido + criterio medible, con vista previa.

El componente solo exige que las tres partes no estén vacías para habilitar «Guardar». El verbo se
elige de la lista que acepta la API (`BLOOM_ACTION_VERBS`); las reglas las aplica la API
(`422 OBJECTIVE_NOT_MEASURABLE`, `422 INVALID_BLOOM_VERB`) y la página muestra su mensaje.
"""

from dataclasses import dataclass

import streamlit as st

from components.layout import render_action_row, render_notice
from components.theme import BLOOM_ACTION_VERBS

VERB_PLACEHOLDER = "Elige un verbo"


@dataclass(frozen=True)
class ObjectiveDraft:
    bloom_verb: str
    content: str
    criterion: str

    @property
    def is_complete(self) -> bool:
        return bool(self.bloom_verb.strip() and self.content.strip() and self.criterion.strip())

    @property
    def statement(self) -> str:
        parts = (self.bloom_verb.strip(), self.content.strip(), self.criterion.strip())
        return " ".join(part for part in parts if part).rstrip(".") + "."


@dataclass(frozen=True)
class ObjectiveEditorResult:
    draft: ObjectiveDraft
    save: bool
    cancel: bool
    reset_to_proposal: bool


def render_objective_editor(
    draft: ObjectiveDraft,
    *,
    key: str,
    topics_count: int | None = None,
    pass_threshold: int | None = None,
    can_reset: bool = True,
) -> ObjectiveEditorResult:
    """Formulario de las tres partes.

    El título «Editar tu objetivo» lo pone la ventana modal (`st.dialog`) de la página (V-041).
    `topics_count` alimenta «Con este objetivo tu ruta tiene N temas».
    """
    st.caption("Redáctalo como un resultado medible: verbo de Bloom + contenido + criterio.")
    verbs = list(BLOOM_ACTION_VERBS)
    if draft.bloom_verb and draft.bloom_verb not in verbs:
        # La propuesta de la IA puede traer un verbo fuera de la lista: se conserva, y la API lo
        # acepta solo si es el de la propuesta guardada (B-020, B-033).
        verbs.insert(0, draft.bloom_verb)
    verb = st.selectbox(
        "Verbo de Bloom",
        verbs,
        index=verbs.index(draft.bloom_verb) if draft.bloom_verb in verbs else None,
        # Solo los verbos de la lista: la API rechaza los demás con 422 (B-033). Sin `placeholder`,
        # Streamlit muestra el texto de ayuda en inglés (B-039).
        placeholder=VERB_PLACEHOLDER,
        key=f"{key}-verb",
    )
    st.caption("Niveles: Recordar · Comprender · Aplicar · Analizar · Evaluar · Crear")
    content = st.text_input("Contenido", value=draft.content, key=f"{key}-content")
    criterion = st.text_input("Criterio medible", value=draft.criterion, key=f"{key}-criterion")
    current = ObjectiveDraft(verb or "", content, criterion)
    with st.container(key=f"panel-{key}-preview"):
        st.caption("**VISTA PREVIA**")
        st.markdown(f"**{current.statement}**" if current.is_complete else "—")
    if topics_count is not None or pass_threshold is not None:
        lines = []
        if topics_count is not None:
            lines.append(f"**Con este objetivo tu ruta tiene {topics_count} temas.**")
        if pass_threshold is not None:
            lines.append(
                f"El {pass_threshold} % para obtener el badge lo define tu instructor y no "
                "cambia con tu objetivo."
            )
        render_notice("\n\n".join(lines), tone="success")
    # «Volver a la propuesta» a la izquierda; «Cancelar» y «Guardar» a la derecha, como en Figma.
    link, actions = render_action_row(f"{key}-editor")
    with link:
        reset = (
            st.button("Volver a la propuesta de la IA", type="tertiary", key=f"{key}-reset")
            if can_reset
            else False
        )
    with actions:
        cancel = st.button("Cancelar", key=f"{key}-cancel")
        save = st.button(
            "Guardar objetivo",
            type="primary",
            key=f"{key}-save",
            disabled=not current.is_complete,
        )
    return ObjectiveEditorResult(current, save=save, cancel=cancel, reset_to_proposal=reset)
