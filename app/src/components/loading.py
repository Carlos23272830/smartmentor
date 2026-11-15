"""Indicador «Cargando…» para las peticiones normales a la API.

Es un único `st.spinner`: Streamlit lo dibuja solo si la petición tarda más de 0,5 s
(`DELAY_SECS`), así que las respuestas rápidas no parpadean. No reemplaza las pantallas de espera
de la IA (U1a a U1d, `loading_steps.py`).
"""

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

LOADING_TEXT = "Cargando…"

# Peticiones en curso en esta ejecución del guion; el script de Streamlit corre en un solo hilo.
_depth: ContextVar[int] = ContextVar("loading_depth", default=0)


@contextmanager
def loading_indicator() -> Iterator[None]:
    """Muestra «Cargando…» mientras dura el bloque.

    No se anida: si ya hay un indicador activo, el bloque interno no dibuja otro. Sin contexto de
    Streamlit (pruebas del cliente con `respx`, scripts) no hace nada.
    """
    if _depth.get() > 0 or get_script_run_ctx(suppress_warning=True) is None:
        yield
        return
    token = _depth.set(1)
    try:
        with st.spinner(LOADING_TEXT):
            yield
    finally:
        _depth.reset(token)
