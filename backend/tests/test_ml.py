import numpy as np

from app.ml.attention import detect_attention_change_point
from app.ml.bkt import BKT
from app.ml.consistency import compute_consistency, consistency_label
from app.ml.forgetting import fit_stability, forgetting_curve
from app.ml.learner_type import LEARNER_TYPES, classify_learner_type
from app.ml.speed import compute_learning_speed, pace_label


def test_bkt_mastery_rises_with_correct_answers():
    m, ll = BKT().forward(np.ones(10))
    assert np.all(np.diff(m) >= -1e-9) and m[-1] > 0.9
    assert np.all(np.isfinite(ll))


def test_bkt_mastery_drops_after_errors():
    m, _ = BKT().forward(np.array([1, 1, 1, 0, 0, 0]))
    assert m[-1] < m[2]


def test_bkt_fit_keeps_params_in_bounds():
    rng = np.random.default_rng(0)
    data = (rng.random(60) < np.linspace(0.2, 0.95, 60)).astype(float)
    b = BKT().fit(data)
    assert 0 < b.p_guess <= 0.3 and 0 < b.p_slip <= 0.3 and 0 < b.p_learn <= 0.6


def test_forgetting_curve_monotonic():
    assert forgetting_curve(0, 3) == 1.0
    assert forgetting_curve(1, 3) > forgetting_curve(5, 3) > forgetting_curve(20, 3)
    assert forgetting_curve(1, 0) == 0.0


def test_fit_stability_bounds():
    assert 2 <= fit_stability([3, 4], [1, 1]) <= 60
    assert fit_stability([], []) == 3.0


def test_consistency_regular_beats_irregular():
    assert compute_consistency([30] * 14) > compute_consistency([0, 0, 120, 0, 0, 0, 10, 0, 0, 90, 0, 0, 0, 0])
    assert compute_consistency([]) == 0.0 and compute_consistency([0, 0]) == 0.0
    assert consistency_label(90) == "Excellent"


def test_speed_and_pace():
    fast = compute_learning_speed(0.5, 3, 0.9)
    slow = compute_learning_speed(0.02, 18, 0.1)
    assert fast > slow and 0 <= slow <= fast <= 100
    assert pace_label(fast) == "Fast" and pace_label(slow) == "Slow"


def test_attention_detects_drop():
    eng = [0.9] * 6 + [0.4] * 6
    assert 25 <= detect_attention_change_point(eng) <= 35
    assert detect_attention_change_point([]) == 0.0


def test_learner_type_valid():
    assert classify_learner_type(np.array([0.75, 0.7, 0.8, 0.8, 0.7])) in LEARNER_TYPES
