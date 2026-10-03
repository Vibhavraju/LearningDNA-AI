# Evaluation

All numbers below were produced by `cd backend && python -m ml.evaluate` (30 simulated students, 28 days each,
deterministic seeds). They are **not** from real learners.

## BKT: predicting the next answer

Protocol: per (student, topic) with >= 10 answers, fit BKT on the first 70% of answers, predict the remaining 30% one
step ahead (1,512 held-out answers).

| Metric | BKT |
|--------|-----|
| AUC | 0.57 |
| RMSE | 0.48 |
| Accuracy | 64.6% |
| Majority-class baseline accuracy | 66.4% |

Reading: BKT is only slightly better than chance at ranking correct vs incorrect answers (AUC 0.57), and its accuracy is
**below** the always-predict-"correct" baseline. That is plausible for this data: the simulator mixes forgetting between
sessions into the answer probability, and BKT (which has no forgetting term) cannot model that. It is a limitation of the
current setup, not something to hide. Ways to improve: add a forgetting/time-gap feature to the BKT input, or use DKT.

## DKT

`python -m ml.train_dkt` trains the LSTM (needs `pip install -r requirements-ml.txt`) and `ml.evaluate` is written so it
can be extended to compare the two. **DKT results have not been measured in this repository**, so no DKT numbers are
claimed here.

## Behavioural checks (automated tests)

- Persona differences are recovered: the high-consistency/long-attention persona scores a higher overall DNA and a longer
  attention span than the low-consistency persona (`tests/test_services.py`).
- All DNA dimensions stay within 0-100; an empty learner returns zeros instead of crashing.
- Attention change-point detection locates a synthetic engagement drop at the right minute.

## Not measured

Retention-prediction error against real recall data, learner-type accuracy, and any effect on real learning outcomes.
