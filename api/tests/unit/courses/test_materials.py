"""Apuntes y lecturas del curso (R-004): extracción del texto y reglas de `MaterialService`."""

import pytest

from app.common.constants import MaterialOrigin
from app.common.exceptions import (
    BusinessRuleError,
    NotFoundError,
    UnsupportedMediaTypeError,
)
from app.domains.courses import service as course_service
from app.domains.courses.materials_text import extract_material
from app.domains.courses.service import MaterialService
from tests.unit.conftest import World
from tests.unit.courses.test_course_service import new_course
from tests.unit.fakes import InMemoryMaterials

NOTES = "# Regresión lineal\n\nLa regresión lineal ajusta una recta por mínimos cuadrados."


@pytest.fixture
def materials() -> InMemoryMaterials:
    return InMemoryMaterials()


@pytest.fixture
def service(world: World, materials: InMemoryMaterials) -> MaterialService:
    return MaterialService(world.courses, materials, world.uow)


# --- extracción -------------------------------------------------------------------------------


async def test_a_markdown_file_is_read_as_text_and_keeps_its_name() -> None:
    extracted = await extract_material(NOTES.encode(), "apuntes_u2.md")
    assert extracted.source_type == "text"
    assert extracted.file_name == "apuntes_u2.md"
    assert "mínimos cuadrados" in extracted.text


async def test_a_txt_file_with_a_bom_is_read_without_it() -> None:
    extracted = await extract_material(b"\xef\xbb\xbf" + NOTES.encode(), "apuntes.TXT")
    assert extracted.text.startswith("# Regresión")


async def test_an_empty_text_file_is_rejected_with_a_material_code() -> None:
    with pytest.raises(BusinessRuleError) as error:
        await extract_material(b"   \n\n", "vacio.txt")
    assert error.value.code == "MATERIAL_NO_TEXT"


async def test_other_extensions_are_rejected() -> None:
    with pytest.raises(UnsupportedMediaTypeError) as error:
        await extract_material(b"PK\x03\x04", "diapositivas.pptx")
    assert error.value.code == "MATERIAL_UNSUPPORTED_TYPE"


async def test_a_text_file_that_is_not_utf8_is_rejected() -> None:
    with pytest.raises(UnsupportedMediaTypeError) as error:
        await extract_material("Regresión".encode("utf-16"), "apuntes.txt")
    assert error.value.code == "MATERIAL_UNSUPPORTED_TYPE"


async def test_a_file_named_pdf_that_is_not_a_pdf_is_rejected() -> None:
    with pytest.raises(UnsupportedMediaTypeError) as error:
        await extract_material(b"no soy un pdf", "libro.pdf")
    assert error.value.code == "MATERIAL_UNSUPPORTED_TYPE"


# --- servicio ---------------------------------------------------------------------------------


async def test_the_owner_uploads_a_material_and_lists_it(
    world: World, service: MaterialService
) -> None:
    course_id = await new_course(world)
    extracted = await extract_material(NOTES.encode(), "apuntes_u2.md")

    material, created = await service.upload(
        world.instructor, course_id, extracted, MaterialOrigin.OWN_NOTES
    )

    assert created
    assert material.origin == "own_notes"
    assert material.extracted_text == extracted.text
    listed = await service.list_materials(world.instructor, course_id)
    assert [m.id for m in listed] == [material.id]


async def test_the_same_file_twice_returns_the_existing_material(
    world: World, service: MaterialService, materials: InMemoryMaterials
) -> None:
    course_id = await new_course(world)
    extracted = await extract_material(NOTES.encode(), "apuntes_u2.md")
    first, _ = await service.upload(
        world.instructor, course_id, extracted, MaterialOrigin.OWN_NOTES
    )

    again, created = await service.upload(
        world.instructor, course_id, extracted, MaterialOrigin.OPEN_LICENSE
    )

    assert not created
    assert again.id == first.id
    assert len(materials.items) == 1


async def test_another_instructor_gets_404_for_a_course_that_is_not_theirs(
    world: World, service: MaterialService
) -> None:
    course_id = await new_course(world)
    extracted = await extract_material(NOTES.encode(), "apuntes.md")

    with pytest.raises(NotFoundError) as error:
        await service.upload(world.other_instructor, course_id, extracted, MaterialOrigin.OWN_NOTES)
    assert error.value.code == "COURSE_NOT_FOUND"
    with pytest.raises(NotFoundError):
        await service.list_materials(world.other_instructor, course_id)


async def test_an_admin_can_add_materials_to_any_course(
    world: World, service: MaterialService
) -> None:
    course_id = await new_course(world)
    extracted = await extract_material(NOTES.encode(), "apuntes.md")
    _, created = await service.upload(world.admin, course_id, extracted, MaterialOrigin.PERMITTED)
    assert created


async def test_the_limit_of_active_materials_is_enforced(
    world: World, service: MaterialService, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(course_service, "MAX_ACTIVE_MATERIALS", 2)
    course_id = await new_course(world)
    for n in range(2):
        extracted = await extract_material(f"{NOTES} parte {n}".encode(), f"u{n}.md")
        await service.upload(world.instructor, course_id, extracted, MaterialOrigin.OWN_NOTES)

    extra = await extract_material(f"{NOTES} parte 3".encode(), "u3.md")
    with pytest.raises(BusinessRuleError) as error:
        await service.upload(world.instructor, course_id, extra, MaterialOrigin.OWN_NOTES)
    assert error.value.code == "MATERIAL_LIMIT_REACHED"
