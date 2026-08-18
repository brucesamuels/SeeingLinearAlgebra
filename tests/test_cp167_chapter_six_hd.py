from pathlib import Path

ASSEMBLY = Path("scripts/assemble_cp167_chapter_six_hd.zsh")


def source() -> str:
    return ASSEMBLY.read_text(encoding="utf-8")


def test_hd_assembly_has_approved_chapter_six_order() -> None:
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


def test_hd_render_is_fresh_1080p60() -> None:
    text = source()
    assert "python -m manim --disable_caching -qh" in text
    assert "*/1080p60/*" in text
    assert "480p15" not in text
    assert "find_existing_clip" not in text


def test_hd_output_has_final_chapter_name() -> None:
    text = source()
    assert 'output="media/ChapterSixOrthogonalityAndProjection.mp4"' in text
    assert 'work_dir="media/chapter_six_assembly_hd"' in text
    assert "_preview.mp4" not in text


def test_hd_assembly_validates_compatibility_and_stream_copies() -> None:
    text = source()
    assert "probe_spec()" in text
    assert "codec_name,width,height,r_frame_rate,pix_fmt" in text
    assert "Video format mismatch" in text
    assert "ffmpeg -y -v warning" in text
    assert "-f concat -safe 0" in text
    assert "-c copy -movflags +faststart" in text


def test_orthonormalization_remains_direct_bridge_into_qr() -> None:
    text = source()
    assert text.index("159|Gram-Schmidt in R^3") < text.index("158|From Orthogonal to Orthonormal")
    assert text.index("158|From Orthogonal to Orthonormal") < text.index("160|QR Factorization")


def test_all_17_scene_sources_and_classes_are_explicit() -> None:
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
