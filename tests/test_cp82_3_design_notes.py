from pathlib import Path
def test_design_note_present():
    assert 'T(0)' in Path('CHECKPOINT_82_3.md').read_text()
