import { describe, it, expect } from 'vitest';
import { calculateDna, evolveDna } from '../utils/dnaEngine';
import { ASSESSMENT_QUESTIONS as QS } from '../data/assessmentQuestions';
import { generatePlan } from '../utils/planEngine';

const answersAlways = (trait: string) =>
  Object.fromEntries(QS.map((q) => {
    const ws = q.options.map((o) => (o.weights as Record<string, number>)[trait] ?? 0);
    return [q.id, ws.indexOf(Math.max(...ws))];
  }));

describe('DNA engine', () => {
  it('scores differ by answers (not hardcoded)', () => {
    const v = calculateDna(answersAlways('visual'));
    const a = calculateDna(answersAlways('auditory'));
    expect(v.topModality).toBe('visual');
    expect(a.topModality).toBe('auditory');
    expect(v.dnaCode).not.toBe(a.dnaCode);
  });
  it('keeps scores within 0-100', () => {
    const p = calculateDna(answersAlways('retention'));
    Object.values(p.scores).forEach((s) => { expect(s).toBeGreaterThanOrEqual(0); expect(s).toBeLessThanOrEqual(100); });
  });
  it('quiz results evolve retention', () => {
    const p = calculateDna(answersAlways('visual'));
    expect(evolveDna(p, 1).scores.retention).toBeGreaterThanOrEqual(p.scores.retention);
    expect(evolveDna(p, 0).scores.retention).toBeLessThanOrEqual(p.scores.retention);
  });
  it('builds a plan with revise tasks for weak topics', () => {
    const p = calculateDna(answersAlways('visual'));
    const plan = generatePlan(p, 'python', [{ date: '', subject: 'python', topicIds: ['py-recursion'], correct: 1, total: 5 }]);
    expect(plan.some((t) => t.kind === 'revise' && t.topicId === 'py-recursion')).toBe(true);
  });
  it('keeps stable, unique task ids so progress survives regeneration', () => {
    const p = calculateDna(answersAlways('visual'));
    const before = generatePlan(p, 'python', []);
    const after = generatePlan(p, 'python', [{ date: '', subject: 'python', topicIds: ['py-recursion'], correct: 1, total: 5 }]);
    expect(new Set(after.map((t) => t.id)).size).toBe(after.length);
    expect(before.every((t) => after.some((a) => a.id === t.id))).toBe(true);
  });
});
