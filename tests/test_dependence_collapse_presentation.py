from pathlib import Path
P=Path('scenes/dependence_collapse_presentation.py')
def test_scene_uses_renderer_independent_model_and_thin_adapter():
    s=P.read_text(); assert 'DependenceCollapsePresentation(Scene)' in s; assert 'from engine.dependence_collapse import DependenceCollapse' in s; assert 'ManimDependenceCollapse' in s
def test_question_prediction_and_delayed_term_are_present():
    s=P.read_text(); assert 'Does every second vector create a plane?' in s; assert 'What happens when the two directions become the same?' in s; assert s.index('progress.animate.set_value(1.0)') < s.index('self.play(FadeIn(dependence))')
def test_field_and_parallelogram_collapse_continuously():
    s=P.read_text(); assert 'model.endpoints_for(progress.get_value(),pairs)' in s; assert 'area_ratio' in s; assert 'rate_func=linear' in s
def test_no_chapter_one_files_are_touched():
    s=P.read_text().lower(); assert 'chapter_one' not in s
