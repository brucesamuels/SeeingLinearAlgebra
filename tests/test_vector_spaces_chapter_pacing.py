from pathlib import Path

CARDS = Path("scenes/vector_spaces_chapter_cards.py")
ASSEMBLER = Path("scripts/assemble_vector_spaces_chapter.py")
RENDER = Path("scripts/render_vector_spaces_chapter.zsh")
REASSEMBLE = Path("scripts/reassemble_vector_spaces_chapter.zsh")
RERENDER_OPENING = Path("scripts/rerender_vector_spaces_opening.zsh")
SCRIPT = Path("CHAPTER_2_NARRATION_SCRIPT.md")


def test_opening_question_is_small_and_only_downscaled_when_needed() -> None:
    source = CARDS.read_text(encoding="utf-8")
    assert '"Vector Spaces: Structure, Dimension,\\nand the Spaces Inside a Matrix"' in source
    assert '"What makes a collection of vectors\\n"' in source
    assert '"into a space,\\n"' in source
    assert '"and how can a matrix reveal\\n"' in source
    assert '"its hidden structure?"' in source
    assert 'font_size=22' in source
    assert 'if question.width > CARD_TEXT_MAX_WIDTH:' in source
    assert 'question.scale_to_fit_width(CARD_TEXT_MAX_WIDTH)' in source
    assert 'question.shift(DOWN * 1.68)' in source
    assert ').scale_to_fit_width(CARD_TEXT_MAX_WIDTH)' not in source


def test_assembler_supports_duration_factor() -> None:
    source = ASSEMBLER.read_text(encoding="utf-8")
    assert "--duration-factor" in source
    assert "duration_factor: float = 1.0" in source
    assert "target_total = int(round((source_frame_index + 1) * duration_factor))" in source


def test_render_defaults_to_twenty_five_percent_longer() -> None:
    source = RENDER.read_text(encoding="utf-8")
    assert 'DURATION_FACTOR="${2:-1.25}"' in source
    assert '--duration-factor "$DURATION_FACTOR"' in source


def test_existing_segments_can_be_reassembled_without_manim_render() -> None:
    source = REASSEMBLE.read_text(encoding="utf-8")
    assert "python scripts/assemble_vector_spaces_chapter.py" in source
    assert "python -m manim" not in source
    assert 'DURATION_FACTOR="${1:-1.25}"' in source


def test_opening_only_script_renders_one_card_then_reassembles() -> None:
    source = RERENDER_OPENING.read_text(encoding="utf-8")
    assert "VectorSpacesChapterOpening" in source
    assert "VectorSpacesSectionOne" not in source
    assert "./scripts/reassemble_vector_spaces_chapter.zsh" in source


def test_narration_script_covers_chapter_sections() -> None:
    source = SCRIPT.read_text(encoding="utf-8")
    for heading in (
        "## Opening",
        "## From Dependence to Subspaces",
        "## Basis and Dimension",
        "## The Spaces Inside a Matrix",
        "## Rank and Nullity",
        "## The Four Fundamental Subspaces",
        "## Closing Reflection",
    ):
        assert heading in source
