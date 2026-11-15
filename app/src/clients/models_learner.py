"""Modelos de las pantallas del aprendiz que `models.py` no cubre (F07b).

- `BadgeAssertion`: el `badge.v1` (Open Badges 2.0) que sirve
  `GET /badges/{public_id}/assertion.json` sin sesión; la interfaz solo muestra su verificación.
- `StudyGoals`: propuesta para «Mis metas» y la racha de E11. El contrato (`api-v2.md`) no tiene
  esta ruta todavía; el cliente HTTP trata un 404 como «sin metas» y la sección no se dibuja.
- `InteractionEvent`: un evento de uso de `POST /me/events` (`EventBody` del OpenAPI), para el
  tiempo en tarea (m27).
"""

from collections.abc import Sequence
from datetime import datetime
from typing import Any, Protocol

from pydantic import Field

from clients.models import ApiModel


class ObIssuer(ApiModel):
    id: str
    name: str
    url: str | None = None


class ObBadgeClass(ApiModel):
    id: str
    name: str
    description: str
    issuer: ObIssuer


class ObRecipient(ApiModel):
    type: str = "email"
    hashed: bool = True
    identity: str = ""


class ObEvidence(ApiModel):
    narrative: str = ""


class BadgeAssertion(ApiModel):
    """Vista de `badge.v1`: la persona receptora va con hash y sal, nunca en claro."""

    id: str
    recipient: ObRecipient
    badge: ObBadgeClass
    issued_on: str = Field(alias="issuedOn")
    evidence: ObEvidence


class StudyGoals(ApiModel):
    """Propuesta: metas del día y del mes con su avance, y días de racha."""

    daily_minutes_goal: int
    daily_minutes_done: int
    monthly_topics_goal: int
    monthly_topics_done: int
    streak_days: int
    daily_options: list[int] = Field(default_factory=lambda: [15, 30, 45])
    monthly_options: list[int] = Field(default_factory=lambda: [2, 3, 4])


class AttemptSummary(ApiModel):
    """`AttemptHistoryItem` del OpenAPI: un intento ya calificado, para el historial (E7c, E9c)."""

    attempt_id: int | None = None
    number: int
    score: float
    correct: int
    total: int
    extra_grant: bool = False
    passed: bool | None = None


class StudyGoalsUpdate(ApiModel):
    daily_minutes_goal: int
    monthly_topics_goal: int


EVENT_TYPE_PATTERN = r"^[a-z][a-z0-9_.]*$"
MAX_EVENTS_PER_BATCH = 100


class InteractionEvent(ApiModel):
    """`EventBody` del OpenAPI. El tipo es libre (sin `CHECK` en la base) pero con este patrón."""

    enrollment_id: int = Field(ge=1)
    event_type: str = Field(min_length=1, max_length=60, pattern=EVENT_TYPE_PATTERN)
    occurred_at: datetime
    topic_id: int | None = Field(default=None, ge=1)
    payload: dict[str, Any] | None = None


class LearnerOps(Protocol):
    """Operaciones del aprendiz que `SmartMentorClient` suma a las de `base.py`."""

    def get_badge_assertion(self, public_id: str) -> BadgeAssertion: ...
    def get_badge_image(self, public_id: str) -> bytes: ...
    def get_study_goals(self) -> StudyGoals | None: ...
    def set_study_goals(self, update: StudyGoalsUpdate) -> StudyGoals: ...
    def list_attempt_history(
        self, enrollment_id: int, step_id: int | None
    ) -> list[AttemptSummary]: ...
    def record_events(self, events: Sequence[InteractionEvent]) -> int: ...
