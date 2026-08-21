from engine.eigenvalues_chapter_review import EigenvaluesChapterReview


def test_review_has_expected_topics() -> None:
    review=EigenvaluesChapterReview()
    titles=[t.title for t in review.topics()]
    assert titles == [
        "Eigenpairs","Eigenspaces","Diagonalization","Repeated eigenvalues","Symmetric matrices","Applications"
    ]
