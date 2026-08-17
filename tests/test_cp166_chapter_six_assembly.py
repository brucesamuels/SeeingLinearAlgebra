from pathlib import Path

ASSEMBLY = Path("scripts/assemble_cp166_chapter_six_preview.zsh")


def source() -> str:
    return ASSEMBLY.read_text(encoding="utf-8")


def test_assembly_has_approved_chapter_six_order() -> None:
    text = source()
    ordered_tokens = [
        "149|Why Orthogonality?",
        "150|Dot Product and Perpendicularity",
        "151|Orthogonal Sets",
        "152|Orthonormal Sets",
        "153|Projection onto a Vector",
        "154|Orthogonal Decomposition",
        "155|Projection onto a Subspace",
        "156|Orthogonal Complements",
        "157|Gram-Schmidt with Two Vectors",
        "159|Gram-Schmidt in R^3",
        "158|From Orthogonal to Orthonormal",
        "160|QR Factorization: Gram-Schmidt in Matrix Form",
        "161|Least Squares: Projection and the Normal Equation",
        "162|Orthogonal Matrices Preserve Geometry",
        "163|Rotations and Reflections: Orthogonal Transformations",
        "164|Projection Matrices: Symmetric and Idempotent",
        "165|Orthogonality and Projection: The Big Picture",
    ]
    positions = [text.index(token) for token in ordered_tokens]
    assert positions == sorted(positions)


def test_orthonormalization_is_direct_bridge_into_qr() -> None:
    text = source()
    assert text.index("159|Gram-Schmidt in R^3") < text.index("158|From Orthogonal to Orthonormal")
    assert text.index("158|From Orthogonal to Orthonormal") < text.index("160|QR Factorization")


def test_assembly_targets_preview_quality_and_reuses_existing_renders() -> None:
    text = source()
    assert "-path '*/480p15/*'" in text
    assert "python -m manim --disable_caching -ql" in text
    assert "--fresh" in text
    assert "find_existing_clip" in text


def test_assembly_validates_video_compatibility_before_concat() -> None:
    text = source()
    assert "probe_spec()" in text
    assert "codec_name,width,height,r_frame_rate,pix_fmt" in text
    assert "Video format mismatch" in text
    assert "ffmpeg -y -v warning" in text
    assert "-f concat -safe 0" in text
    assert "-c copy -movflags +faststart" in text


def test_preview_output_has_stable_chapter_name() -> None:
    text = source()
    assert 'output="media/ChapterSixOrthogonalityAndProjection_preview.mp4"' in text
    assert 'work_dir="media/chapter_six_assembly_preview"' in text


def test_all_scene_sources_and_classes_are_explicit() -> None:
    text = source()
    required = {
        "scenes/why_orthogonality_presentation.py": "WhyOrthogonalityPresentation",
        "scenes/dot_product_perpendicularity_presentation.py": "DotProductPerpendicularityPresentation",
        "scenes/orthogonal_sets_presentation.py": "OrthogonalSetsPresentation",
        "scenes/orthonormal_sets_presentation.py": "OrthonormalSetsPresentation",
        "scenes/vector_projection_presentation.py": "VectorProjectionPresentation",
        "scenes/orthogonal_decomposition_presentation.py": "OrthogonalDecompositionPresentation",
        "scenes/subspace_projection_presentation.py": "SubspaceProjectionPresentation",
        "scenes/orthogonal_complements_presentation.py": "OrthogonalComplementsPresentation",
        "scenes/gram_schmidt_two_vectors_presentation.py": "GramSchmidtTwoVectorsPresentation",
        "scenes/gram_schmidt_three_vectors_presentation.py": "GramSchmidtThreeVectorsPresentation",
        "scenes/orthonormalization_presentation.py": "OrthonormalizationPresentation",
        "scenes/qr_factorization_presentation.py": "QRFactorizationPresentation",
        "scenes/least_squares_projection_presentation.py": "LeastSquaresProjectionPresentation",
        "scenes/orthogonal_matrices_presentation.py": "OrthogonalMatricesPresentation",
        "scenes/rotations_reflections_presentation.py": "RotationsReflectionsPresentation",
        "scenes/projection_matrices_presentation.py": "ProjectionMatricesPresentation",
        "scenes/chapter_six_finale_presentation.py": "ChapterSixFinalePresentation",
    }
    for scene_file, scene_class in required.items():
        assert scene_file in text
        assert scene_class in text
