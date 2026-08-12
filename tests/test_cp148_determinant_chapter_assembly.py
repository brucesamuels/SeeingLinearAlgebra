from pathlib import Path
import importlib.util


BUILD_SCRIPT = Path("scripts/build_cp148_determinant_chapter.py")


def load_builder():
    spec = importlib.util.spec_from_file_location("cp148_builder", BUILD_SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_chapter_contains_title_plus_twenty_lessons() -> None:
    builder = load_builder()
    assert len(builder.SCENE_ORDER) == 21


def test_chapter_begins_with_title_and_why_determinants() -> None:
    builder = load_builder()
    assert builder.SCENE_ORDER[0][0] == "DeterminantChapterTitleCard"
    assert builder.SCENE_ORDER[1][0] == "WhyDeterminantsPresentation"




def test_jacobian_preview_immediately_precedes_synthesis() -> None:
    builder = load_builder()
    classes = [scene for scene, _ in builder.SCENE_ORDER]
    assert classes[-2:] == [
        "DeterminantJacobianPreviewPresentation",
        "DeterminantChapterSynthesisPresentation",
    ]



def test_geometry_section_is_grouped_near_the_beginning() -> None:
    builder = load_builder()
    classes = [scene for scene, _ in builder.SCENE_ORDER]
    assert classes[2:6] == [
        "DeterminantAreaScalePresentation",
        "DeterminantOrientationPresentation",
        "DeterminantFormulaGeometryPresentation",
        "DeterminantGeometryPresentation",
    ]


def test_product_and_transpose_immediately_follow_properties_block() -> None:
    builder = load_builder()
    classes = [scene for scene, _ in builder.SCENE_ORDER]
    assert classes[6:10] == [
        "DeterminantPropertiesPresentation",
        "DeterminantConsequencesPresentation",
        "DeterminantProductRulePresentation",
        "DeterminantTransposeRulePresentation",
    ]


def test_computation_follows_properties_and_algebraic_rules() -> None:
    builder = load_builder()
    classes = [scene for scene, _ in builder.SCENE_ORDER]
    assert classes[10:16] == [
        "DeterminantEliminationPresentation",
        "DeterminantBigFormulaPresentation",
        "DeterminantBigFormulaDerivationPresentation",
        "DeterminantCofactorExpansionPresentation",
        "DeterminantCofactorEfficiencyPresentation",
        "DeterminantTriangularPresentation",
    ]


def test_final_hd_builder_can_require_1080p60() -> None:
    source = BUILD_SCRIPT.read_text(encoding="utf-8")
    assert "--quality-dir" in source
    assert "quality_dir in path.parts" in source

def test_title_card_text() -> None:
    source = Path("scenes/determinant_chapter_title_card.py").read_text(encoding="utf-8")
    assert 'Text("Chapter 5"' in source
    assert 'Text("Determinants"' in source
    assert "Scale • orientation • invertibility • structure" in source
    assert "self.wait(3.0)" in source


def test_builder_excludes_partial_movie_files() -> None:
    source = BUILD_SCRIPT.read_text(encoding="utf-8")
    assert '"partial_movie_files" not in path.parts' in source


def test_builder_reencodes_with_h264() -> None:
    source = BUILD_SCRIPT.read_text(encoding="utf-8")
    assert '"libx264"' in source
    assert '"yuv420p"' in source
    assert '"-crf"' in source
