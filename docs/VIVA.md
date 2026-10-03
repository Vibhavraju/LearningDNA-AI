# Viva notes

- **One-liner:** an app that works out how a student learns (not just what they know) and adapts the plan and tutor to it.
- **Problem:** most e-learning platforms are static - everyone gets the same sequence and the same explanations.
- **Two layers:**
  1. *Self-report DNA (frontend):* 20 scenario questions -> 8 traits (4 input styles in the VARK spirit, focus, retention,
     pace, consistency) -> DNA code, archetype, plan. Quizzes then nudge retention, pace and consistency.
  2. *Behavioural DNA (backend):* computed from study events - BKT mastery, forgetting curve, attention change-point,
     consistency and speed (with a simulated-cohort percentile) -> learner type, recommendations.
- **Models:** BKT (mastery), exponential forgetting curve R(t)=exp(-t/S), change-point attention span, nearest-centroid
  learner type, TF-IDF retrieval for the tutor. DKT (LSTM) is implemented but not yet evaluated.
- **Evaluation:** see `EVALUATION.md` - BKT AUC 0.57 on simulated data, below the majority baseline on accuracy.
- **Limitations:** simulated data only, in-memory state, no auth, the two DNA models are not merged, VARK-style scoring
  is a study aid and not a clinical test.
- **Next steps:** real learner data, add a time-gap/forgetting input to BKT, train and compare DKT, persist to Postgres.
