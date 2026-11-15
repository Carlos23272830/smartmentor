"""El indicador «Cargando…» no se anida y no falla sin contexto de Streamlit."""

from contextlib import contextmanager
from typing import Any

import httpx
import pytest
import respx
from streamlit.testing.v1 import AppTest

from clients.api import ApiClient
from components import loading


def test_does_nothing_without_streamlit_context(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("no debe dibujar sin contexto")

    monkeypatch.setattr(loading.st, "spinner", fail)
    with loading.loading_indicator(), loading.loading_indicator():
        pass


def test_nested_calls_draw_a_single_spinner(monkeypatch: pytest.MonkeyPatch) -> None:
    texts: list[str] = []

    @contextmanager
    def fake_spinner(text: str) -> Any:
        texts.append(text)
        yield

    monkeypatch.setattr(loading, "get_script_run_ctx", lambda **_kwargs: object())
    monkeypatch.setattr(loading.st, "spinner", fake_spinner)
    with loading.loading_indicator(), loading.loading_indicator():
        pass
    assert texts == ["Cargando…"]
    with loading.loading_indicator():  # al terminar el primero, el siguiente sí dibuja
        pass
    assert texts == ["Cargando…", "Cargando…"]


def test_depth_is_released_after_an_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(loading, "get_script_run_ctx", lambda **_kwargs: object())
    monkeypatch.setattr(loading.st, "spinner", lambda _text: _noop())
    with pytest.raises(ValueError, match="boom"), loading.loading_indicator():
        raise ValueError("boom")
    assert loading._depth.get() == 0


@contextmanager
def _noop() -> Any:
    yield


@respx.mock
def test_api_client_works_without_streamlit_context() -> None:
    respx.get("http://api.test/api/v1/me/badges").mock(return_value=httpx.Response(200, json=[]))
    client = ApiClient(
        "http://api.test", lambda: "token", http=httpx.Client(base_url="http://api.test")
    )
    assert client.list_badges() == []


def _slow_script() -> None:
    import streamlit as st

    from components.loading import loading_indicator

    with loading_indicator(), loading_indicator():
        st.write("hecho")


def test_apptest_runs_inside_a_script() -> None:
    app = AppTest.from_function(_slow_script).run()
    assert not app.exception
    assert app.markdown[0].value == "hecho"
