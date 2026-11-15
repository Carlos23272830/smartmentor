"""AD5 (cursos e inscripciones) y C4 (catálogo de prompts).

AD4 y AD4b (piloto) ya no existen: el piloto se define fuera de la app (F-013).
"""

from apptest import page_texts
from staff_support import (
    assert_no_exception,
    click,
    staff_app,
    staff_text_reader,  # noqa: F401
)

from core.navigation import PAGES, registered_pages
from services.staff_prompts import PROMPTS

COURSES = "pages/admin/courses_enrollments.py"
CATALOG = "pages/admin/prompt_catalog.py"


def test_the_pilot_screens_are_gone() -> None:
    """F-013: ni página, ni entrada de navegación, ni botón que lleve al piloto."""
    assert not any("pilot" in spec.path for spec in PAGES)
    assert not any(spec.url_path == "pilot" for spec in registered_pages())
    at = staff_app("admin", page="pages/admin/metrics.py")
    assert_no_exception(at)
    assert not any("piloto" in b.label.lower() for b in at.button)


def test_ad5_lists_courses_and_enrollments() -> None:
    at = staff_app("admin", page=COURSES)
    assert_no_exception(at)
    texts = page_texts(at)
    for expected in (
        "Cursos, rutas e inscripciones",
        "Sin asignar",
        "Sin ruta",
        "Asignar instructor",
        "Personalizada",
        "Ruta fija",
        "Aceptado",
        "Pendiente",
        "Fundamentos de ML · 2026-2",
        "Durante el piloto, cambiar a un aprendiz de ruta o de grupo lo saca del análisis.",
    ):
        assert any(expected in t for t in texts), expected


def test_ad5_assign_an_instructor() -> None:
    at = staff_app("admin", page=COURSES)
    at = click(at, "Asignar instructor")
    at.selectbox(key="ce-owner").set_value(12).run()
    at = click(at, "Guardar instructor")
    assert_no_exception(at)
    assert not at.error


def test_ad5_withdraw_and_move_enrollment() -> None:
    at = staff_app("admin", page=COURSES)
    at = next(b for b in at.button if b.label == "Retirar").click().run()
    at.text_area(key="ce-note").set_value("Pidió retirarse").run()
    at = click(at, "Retirar")
    assert_no_exception(at)
    at = next(b for b in at.button if b.label == "Cambiar de ruta").click().run()
    at = click(at, "Mover")
    assert_no_exception(at)
    assert not at.error


def test_ad5_enroll_a_learner() -> None:
    at = staff_app("admin", page=COURSES)
    at = click(at, "Inscribir aprendiz")
    at = click(at, "Inscribir")
    assert_no_exception(at)
    assert not at.error


def test_ad5_empty_and_forbidden() -> None:
    at = staff_app("admin", scenario="empty", page=COURSES)
    texts = page_texts(at)
    assert "Todavía no hay cursos." in texts and "Todavía no hay inscripciones." in texts
    at = staff_app("instructor", scenario="forbidden", page=COURSES)
    assert "403" in page_texts(at, skip_header=False)


def test_c4_prompt_catalog() -> None:
    at = staff_app("admin", page=CATALOG)
    assert_no_exception(at)
    texts = page_texts(at)
    assert "Catálogo de prompts y versiones" in texts
    for prompt in PROMPTS:
        assert f"{prompt.prompt_id} v{prompt.version}" in texts
    assert len({p.prompt_id for p in PROMPTS}) == len(PROMPTS)
    at = click(at, "Volver al Log LLM")
    assert "Log LLM y costos" in page_texts(at)
