import { SUBJECTS } from '../data/topics';
import { DnaProfile, FORMAT_LABEL } from './dnaEngine';

export interface PlanTask {
  id: string;
  title: string;
  topicId: string;
  minutes: number;
  detail: string;
  kind: 'learn' | 'revise' | 'gap';
  day: number; // 0..6
  done: boolean;
}
export interface QuizResult { date: string; subject: string; topicIds: string[]; correct: number; total: number }

/** Topic ids where the learner scored below 70% in a past quiz. */
export const weakTopicIds = (results: QuizResult[]): string[] => {
  const weak = new Set<string>();
  for (const r of results) if (r.total && r.correct / r.total < 0.7) r.topicIds.forEach((t) => weak.add(t));
  return [...weak];
};

export const DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

/** Builds a 7-day plan from the DNA profile, the chosen subject and past quiz results. */
export const generatePlan = (dna: DnaProfile, subjectId: string, results: QuizResult[]): PlanTask[] => {
  const subject = SUBJECTS.find((s) => s.id === subjectId) ?? SUBJECTS[0];
  const session = dna.scores.focusEndurance >= 70 ? 45 : dna.scores.focusEndurance >= 45 ? 30 : 20;
  const fmt = FORMAT_LABEL[dna.topModality];

  const weak = new Set(weakTopicIds(results));

  // `key` makes ids stable, so a task keeps its "done" state when the plan is regenerated.
  const tasks: (Omit<PlanTask, 'day' | 'id'> & { key: string })[] = [];
  subject.topics.forEach((t) => {
    tasks.push({ key: `learn:${t.id}`, title: `Learn: ${t.name}`, topicId: t.id, minutes: Math.min(session, t.estimatedMinutes), kind: 'learn', detail: `Use ${fmt}`, done: false });
    if (weak.has(t.id)) tasks.push({ key: `revise:${t.id}`, title: `Revise: ${t.name}`, topicId: t.id, minutes: 15, kind: 'revise', detail: 'Low quiz score: retry with active recall', done: false });
  });
  tasks.splice(2, 0, {
    key: 'gap', title: `Gap drill: ${FORMAT_LABEL[dna.lowModality]}`, topicId: subject.topics[0].id, minutes: 15, kind: 'gap',
    detail: 'Strengthens your weakest style', done: false,
  });
  tasks.push({ key: 'weekly', title: 'Weekly review quiz', topicId: subject.topics[0].id, minutes: 15, kind: 'revise', detail: 'Take a quiz in Quiz Runner', done: false });

  // Spread evenly across Mon-Sun so the week is balanced.
  const list = tasks.slice(0, 12);
  return list.map(({ key, ...t }, i) => ({ ...t, id: `${subject.id}:${key}`, day: list.length > 1 ? Math.round((i * 6) / (list.length - 1)) : 0 }));
};
