"""E10, E11, E11b, E12, E13a y E13b: badge, progreso, autorizaciones, logros y encuesta."""

from apptest import button, page_texts, session_of
from learner_support import (
    ACHIEVEMENTS,
    BADGE,
    FINAL,
    FINAL_RESULT,
    PATH,
    PROGRESS,
    RETENTION,
    SURVEY,
    client_of,
    fail,
    learner_app,
    matches_figma,
    no_exception,
)
from streamlit.testing.v1 import AppTest

from clients.base import ApiError
from clients.models import AttemptResult, NextAction
from clients.models_learner import StudyGoals


def test_e10_follows_figma() -> None:
    at = learner_app("learner_completed", BADGE)
    # El ícono de la insignia y el botón de descarga no los lee `AppTest`.
    matches_figma(at, "E10", accepted=("★", "Descargar badge"))


def test_e10_without_pending_survey_hides_the_survey_card() -> None:
    at = learner_app("learner_badge", BADGE)
    no_exception(at)
    assert "Responder encuesta" not in page_texts(at)


def test_e10_public_verification_and_share() -> None:
    at = learner_app("learner_badge", BADGE)
    assert not at.code
    button(at, "Compartir").click().run()
    assert at.code
    assert "Verificación pública" in [e.label for e in at.expander]
    # La evidencia llega como lista (B-034) y su narrativa se muestra.
    assert any("con 88 % (umbral 80 %)" in text for text in page_texts(at))


def test_e10_survey_card_opens_the_survey() -> None:
    at = learner_app("learner_completed", BADGE)
    button(at, "Responder encuesta").click().run()
    no_exception(at)
    assert session_of(at).learner.survey_step == 1


def test_e10_offline() -> None:
    at = learner_app("learner_offline", BADGE)
    no_exception(at)
    assert at.error


# --- E12 -----------------------------------------------------------------------------------------


def test_e12_lists_obtained_and_locked_badges() -> None:
    at = learner_app("learner_badge", ACHIEVEMENTS)
    no_exception(at)
    texts = page_texts(at)
    assert "Logros" in texts
    assert "Tus badges digitales: imagen PNG + archivo JSON Open Badges." in texts
    assert "Fundamentos de Machine Learning" in texts
    assert "Obtenido 5 oct 2026" in texts
    assert "Bloqueado · inscríbete para obtenerlo" in texts
    assert "Ver badge" in texts


def test_e12_view_badge_opens_that_enrollment() -> None:
    at = learner_app("learner_badge", ACHIEVEMENTS)
    button(at, "Ver badge").click().run()
    no_exception(at)
    assert session_of(at).selected_enrollment_id == 7
    assert "¡Ruta completada!" in page_texts(at)


def test_e12_error_is_friendly() -> None:
    at = learner_app("learner_badge", ACHIEVEMENTS, run=False)
    fail(at, "list_badges", ApiError(500, "INTERNAL_ERROR"))
    at.run()
    no_exception(at)
    assert at.error


# --- E11 · E11b ----------------------------------------------------------------------------------


def test_e11_follows_figma() -> None:
    at = learner_app("learner_path", PROGRESS)
    matches_figma(
        at,
        "E11",
        accepted=(
            # La API no dice si hay prueba de retención (E14, P2), los intentos por tema se
            # calculan con los datos de la ruta y la persona de ejemplo no participa del piloto.
            "Tu rol: Aprendiz · Solo ves tu propio avance, nunca el de otros aprendices.",
            "1,5",
            "Prueba de retención disponible · opcional",
            "10 preguntas · unos 10 minutos. Nos ayuda a medir cuánto recuerdas semanas después "
            "de terminar la ruta.",
            "Empezar prueba",
            "Datos: autorizado el 1 oct 2026",
            "Piloto: participas · ruta personalizada",
        ),
    )


def test_e11_shows_progress_bars_and_badges_v050() -> None:
    """Barra del curso y de cada meta, y los estados de «Tus datos» como insignias."""
    at = learner_app("learner_path", PROGRESS)
    no_exception(at)
    assert len(at.get("progress")) == 3  # curso, meta de hoy y meta del mes
    badges = [e.value for e in at.markdown if "-badge[" in e.value]
    assert any("Racha de 3 días" in text for text in badges)
    assert any("Datos: autorizado el" in text for text in badges)
    assert any("Piloto: " in text for text in badges)


def test_e11_without_goals_they_can_be_chosen_b028() -> None:
    """La API responde 404 hasta que hay metas: la sección se muestra vacía y se pueden elegir."""
    at = learner_app("learner_path", PROGRESS, run=False)
    client = client_of(at)
    original_get, original_set = client.get_study_goals, client.set_study_goals
    saved: list[StudyGoals] = []

    def save(update: object) -> StudyGoals:
        goals = original_set(update)  # type: ignore[arg-type]
        saved.append(goals)
        client.get_study_goals = original_get  # type: ignore[method-assign]
        return goals

    client.get_study_goals = lambda: None if not saved else original_get()  # type: ignore[method-assign]
    client.set_study_goals = save  # type: ignore[method-assign]
    at.run()
    no_exception(at)
    texts = page_texts(at)
    assert "Mis metas · opcional" in texts
    assert "Todavía no tienes metas. Elige una para hoy y otra para este mes." in texts
    at.segmented_control(key="goal-daily").set_value(30).run()
    assert saved == []  # falta la meta del mes
    at.segmented_control(key="goal-monthly").set_value(3).run()
    no_exception(at)
    assert len(saved) == 1


def test_e11_changing_the_daily_goal_saves_it() -> None:
    at = learner_app("learner_path", PROGRESS)
    saved: list[StudyGoals] = []
    client = client_of(at)
    original = client.set_study_goals

    def spy(update: object) -> StudyGoals:
        goals = original(update)  # type: ignore[arg-type]
        saved.append(goals)
        return goals

    client.set_study_goals = spy  # type: ignore[method-assign]
    at.segmented_control(key="goal-daily").set_value(45).run()
    no_exception(at)
    assert saved[0].daily_minutes_goal == 45


def test_e11_continue_follows_next_action() -> None:
    at = learner_app("learner_path", PROGRESS)
    button(at, "Continuar mi ruta").click().run()
    no_exception(at)
    assert session_of(at).learner.step_id == 813


def test_e11b_leave_the_pilot_revokes_only_the_pilot_consent() -> None:
    at = learner_app("learner_path", PROGRESS, run=False)
    client = client_of(at)
    client.grant_consent("pilot_research", "1.0")
    at.run()
    me = client.get_me()
    session_of(at).me = me
    at.run()
    revoked = []
    original = client.revoke_consent

    def spy(kind: str) -> object:
        revoked.append(kind)
        return original(kind)  # type: ignore[arg-type]

    client.revoke_consent = spy  # type: ignore[method-assign]
    button(at, "Gestionar mis autorizaciones").click().run()
    # V-051: E11b es una ventana modal (`st.dialog`); sus textos no están en el cuerpo de la página.
    assert "Elige qué quieres cambiar. Puedes volver a autorizar más adelante." in [
        c.value for c in at.caption
    ]
    assert button(at, "Confirmar").disabled
    at.radio(key="consents-choice").set_value("Salir del piloto").run()
    button(at, "Confirmar").click().run()
    no_exception(at)
    assert revoked == ["pilot_research"]


def test_e11b_revoking_everything_requests_deletion_and_asks_for_consent_again() -> None:
    at = learner_app("learner_path", PROGRESS)
    requests = []
    client = client_of(at)
    client.create_data_subject_request = lambda kind, _comment: requests.append(kind)  # type: ignore[method-assign,assignment,return-value]
    button(at, "Gestionar mis autorizaciones").click().run()
    at.radio(key="consents-choice").set_value("Revocar la autorización y borrar mis datos").run()
    button(at, "Confirmar").click().run()
    no_exception(at)
    assert requests == ["deletion"]
    assert session_of(at).me is not None
    assert session_of(at).me.requires_consent  # type: ignore[union-attr]


def test_e11b_cancel_closes_the_panel() -> None:
    at = learner_app("learner_path", PROGRESS)
    button(at, "Gestionar mis autorizaciones").click().run()
    button(at, "Cancelar").click().run()
    assert "Elige qué quieres cambiar. Puedes volver a autorizar más adelante." not in [
        c.value for c in at.caption
    ]


def test_e11_offline() -> None:
    at = learner_app("learner_offline", PROGRESS)
    no_exception(at)
    assert at.error


# --- E13a · E13b ---------------------------------------------------------------------------------


def _fill(at: AppTest, count: int, start: int = 0) -> None:
    for index in range(start, start + count):
        at.radio[index].set_value(5).run()


def test_e13a_follows_figma() -> None:
    at = learner_app("learner_completed", SURVEY)
    matches_figma(at, "E13a", accepted=("Fundamentos de ML · Encuesta final",))


def test_e13_shows_the_step_progress_bar() -> None:
    at = learner_app("learner_completed", SURVEY)
    assert [p.value for p in at.progress] == [50]
    _fill(at, 8)
    button(at, "Siguiente").click().run()
    assert [p.value for p in at.progress] == [100]


def test_e13a_next_needs_every_answer() -> None:
    at = learner_app("learner_completed", SURVEY)
    assert button(at, "Siguiente").disabled
    _fill(at, 8)
    assert not button(at, "Siguiente").disabled


def test_e13b_follows_figma_and_sends_the_survey() -> None:
    at = learner_app("learner_completed", SURVEY)
    _fill(at, 8)
    button(at, "Siguiente").click().run()
    matches_figma(at, "E13b", accepted=("Fundamentos de ML · Encuesta final",))
    sent = []
    client_of(at).submit_final_survey = lambda *_a, **kw: sent.append(kw) or 85.0  # type: ignore[method-assign]
    _fill(at, 5)
    at.text_area(key="survey-comment").set_value("Más ejemplos.").run()
    button(at, "Enviar encuesta").click().run()
    no_exception(at)
    assert len(sent[0]["sus_items"]) == 10
    assert sent[0]["likert"] == {"q1": 5, "q2": 5, "q3": 5}
    assert sent[0]["comment"] == "Más ejemplos."


def test_e13b_back_keeps_step_one_answers() -> None:
    at = learner_app("learner_completed", SURVEY)
    _fill(at, 8)
    button(at, "Siguiente").click().run()
    button(at, "Anterior").click().run()
    assert not button(at, "Siguiente").disabled


def test_e13_already_answered_is_a_friendly_error() -> None:
    at = learner_app("learner_completed", SURVEY)
    _fill(at, 8)
    button(at, "Siguiente").click().run()
    _fill(at, 5)
    fail(at, "submit_final_survey", ApiError(409, "SURVEY_ALREADY_SUBMITTED"))
    button(at, "Enviar encuesta").click().run()
    assert at.error[0].value == "Ya respondiste la encuesta."


def test_e13_skip_returns_to_the_badge() -> None:
    at = learner_app("learner_completed", SURVEY)
    button(at, "Ahora no").click().run()
    no_exception(at)
    assert "¡Ruta completada!" in page_texts(at)


# --- E14 (P2) ------------------------------------------------------------------------------------


def test_e14_is_only_offered_when_the_route_is_completed() -> None:
    at = learner_app("learner_path", RETENTION)
    no_exception(at)
    assert at.info
    assert "Prueba de retención" not in page_texts(at)


def test_e14_shows_the_retention_questions() -> None:
    at = learner_app("learner_badge", RETENTION)
    no_exception(at)
    texts = page_texts(at)
    assert "Prueba de retención" in texts
    assert "Sin ayuda de IA ni apuntes" in texts
    assert any(t.startswith("Pregunta 1 de 5") for t in texts)
    assert at.get_by_key("retention-chips")
    assert at.get_by_key("card-quiz-retention")
    assert at.get_by_key("notice-info")  # render_notice(tone="info"): caja azul suave
    assert any(t.startswith("Preguntas equivalentes") for t in texts)
    assert not at.progress
    skip = button(at, "Ahora no")
    assert skip.key == "retention-skip"


def test_e11_offers_the_retention_test_after_completing_the_route() -> None:
    at = learner_app("learner_badge", PROGRESS)
    assert "Prueba de retención disponible · opcional" in page_texts(at)
    button(at, "Empezar prueba").click().run()
    no_exception(at)
    assert "Prueba de retención" in page_texts(at)


# --- B-037: varias rutas -------------------------------------------------------------------------


def test_b037_e11_defaults_to_the_most_recent_route_in_progress() -> None:
    at = learner_app("learner_multi_path", PROGRESS)
    no_exception(at)
    texts = page_texts(at)
    assert session_of(at).selected_enrollment_id == 9
    assert "1 de 4" in texts
    assert "Python para análisis de datos" in texts
    assert at.selectbox[0].value == 9
    assert "Prueba de retención disponible · opcional" not in texts


def test_b037_e11_selector_changes_the_cards() -> None:
    at = learner_app("learner_multi_path", PROGRESS)
    at.selectbox[0].set_value(8).run()
    no_exception(at)
    texts = page_texts(at)
    assert session_of(at).selected_enrollment_id == 8
    assert "3 de 5" in texts
    assert "1 de 4" not in texts
    assert at.selectbox[0].value == 8
    at.selectbox[0].set_value(7).run()
    assert "Prueba de retención disponible · opcional" in page_texts(at)


def test_b037_e11_single_route_has_no_selector() -> None:
    at = learner_app("learner_path", PROGRESS)
    assert len(at.selectbox) == 0


def test_b037_e12_enrolled_routes_are_not_shown_as_not_enrolled() -> None:
    at = learner_app("learner_multi_path", ACHIEVEMENTS)
    no_exception(at)
    texts = page_texts(at)
    assert "Obtenido 5 oct 2026" in texts
    assert "En curso · 3 de 5 temas aprobados" in texts
    assert "En curso · 1 de 4 temas aprobados" in texts
    # Solo las rutas sin inscripción siguen diciendo que hay que inscribirse (Claude x3, Google).
    assert texts.count("Bloqueado · inscríbete para obtenerlo") == 3


def test_b037_e14_is_enabled_by_any_completed_route() -> None:
    at = learner_app("learner_multi_path", RETENTION)
    no_exception(at)
    assert not at.info
    assert "Prueba de retención" in page_texts(at)
    assert session_of(at).selected_enrollment_id == 7


def test_b037_e14_stays_closed_when_no_route_is_completed() -> None:
    at = learner_app("learner_path", RETENTION)
    assert at.info


# --- B-045: al aprobar la final se ve el badge antes que la encuesta ------------------------------

SURVEY_PENDING = NextAction(type="answer_survey", screen="E13a")


def _on_badge(at: AppTest, *, survey_card: bool) -> None:
    """E10: el badge y, si la encuesta sigue pendiente, su tarjeta opcional."""
    no_exception(at)
    texts = page_texts(at)
    assert "¡Ruta completada!" in texts
    assert "Cuéntanos cómo te fue" not in texts
    assert ("Encuesta final · opcional" in texts) is survey_card
    assert any(b.key == "badge-survey" for b in at.button) is survey_card


def _answer_survey(at: AppTest) -> None:
    _fill(at, 8)
    button(at, "Siguiente").click().run()
    _fill(at, 5)
    button(at, "Enviar encuesta").click().run()


def _pass_the_final(at: AppTest) -> None:
    """La entrega aprueba la final y la API manda `answer_survey` (E13a), como en el recorrido."""
    client = client_of(at)
    passed = client.doc("attempt_result", AttemptResult).model_copy(
        update={
            "assessment_type": "final",
            "passed": True,
            "score": 88.0,
            "next_action": SURVEY_PENDING,
        }
    )

    def graded(*_: object, **__: object) -> AttemptResult:
        client.echo_next_action(SURVEY_PENDING)
        return passed

    client.submit_attempt = graded  # type: ignore[method-assign,assignment]
    client.get_attempt_result = graded  # type: ignore[method-assign,assignment]


def test_b045_passing_the_final_shows_the_badge_with_the_survey_card() -> None:
    at = learner_app("learner_final_ready", FINAL, run=False)
    _pass_the_final(at)
    at.run()
    for index in range(8):
        at.radio[0].set_value(at.radio[0].options[0]).run()
        button(at, "Siguiente" if index < 7 else "Enviar evaluación").click().run()
    _on_badge(at, survey_card=True)


def test_b045_e9_with_a_passed_final_goes_to_the_badge() -> None:
    at = learner_app("learner_completed", FINAL_RESULT, run=False)
    _pass_the_final(at)
    session_of(at).learner.final_attempt_id = 9002
    at.run()
    _on_badge(at, survey_card=True)


def test_b045_badge_survey_card_opens_e13a_and_disappears_once_sent() -> None:
    at = learner_app("learner_completed", BADGE)
    _on_badge(at, survey_card=True)
    button(at, "Responder encuesta").click().run()
    no_exception(at)
    assert "Cuéntanos cómo te fue" in page_texts(at)
    # AppTest no conserva el `switch_page`: se abre E13a como lo haría el navegador.
    at.switch_page(SURVEY).run()
    _answer_survey(at)
    _on_badge(at, survey_card=False)
    # Al volver más tarde (otra ejecución) la encuesta tampoco se ofrece.
    at.switch_page(BADGE).run()
    _on_badge(at, survey_card=False)


def test_b045_skipping_the_survey_keeps_offering_it() -> None:
    at = learner_app("learner_completed", SURVEY)
    button(at, "Ahora no").click().run()
    _on_badge(at, survey_card=True)


def test_b045_e5_continue_with_pending_survey_opens_the_badge() -> None:
    at = learner_app("learner_completed", PATH)
    button(at, "Ver badge").click().run()
    _on_badge(at, survey_card=True)


def test_b045_e11_continue_with_pending_survey_opens_the_badge() -> None:
    at = learner_app("learner_completed", PROGRESS)
    button(at, "Continuar mi ruta").click().run()
    _on_badge(at, survey_card=True)


def test_b045_e11_continue_after_the_survey_opens_the_badge_without_the_card() -> None:
    at = learner_app("learner_completed", SURVEY)
    _answer_survey(at)
    at.switch_page(PROGRESS).run()
    button(at, "Continuar mi ruta").click().run()
    _on_badge(at, survey_card=False)


def test_b045_e8_with_the_route_completed_redirects_to_the_badge() -> None:
    at = learner_app("learner_completed", FINAL)
    _on_badge(at, survey_card=True)


def test_b045_e12_view_badge_keeps_the_pending_survey_card() -> None:
    at = learner_app("learner_completed", ACHIEVEMENTS)
    button(at, "Ver badge").click().run()
    _on_badge(at, survey_card=True)


def test_e13b_back_keeps_the_comment() -> None:
    at = learner_app("learner_completed", SURVEY)
    _fill(at, 8)
    button(at, "Siguiente").click().run()
    _fill(at, 5)
    at.text_area(key="survey-comment").set_value("Más ejemplos.").run()
    button(at, "Anterior").click().run()
    button(at, "Siguiente").click().run()
    assert at.text_area(key="survey-comment").value == "Más ejemplos."
