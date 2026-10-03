import { SUBJECTS } from '../data/topics';
import { DnaProfile, Modality, FORMAT_LABEL } from '../utils/dnaEngine';
import { weakTopicIds, QuizResult } from '../utils/planEngine';
import type { TutorProfile } from '../api/client';

const MOVE: Record<Modality, string> = {
  visual: 'Sketch it as a diagram: boxes for each step, arrows for the flow, a colour per stage.',
  auditory: 'Explain it out loud as if teaching a friend, then record yourself and listen back.',
  readWrite: 'Write a five-line structured summary with headings, then rewrite it from memory.',
  kinesthetic: 'Build the smallest working example yourself, then break it on purpose and fix it.',
};

const allTopics = SUBJECTS.flatMap((s) => s.topics.map((t) => ({ ...t, subject: s.name })));
const words = (s: string) => s.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').split(/\s+/).filter((w) => w.length > 2);

/** Answers questions about the learner themself (focus, revision, DNA, plan). Returns null for subject questions. */
export const intentReply = (question: string, dna: DnaProfile): string | null => {
  const q = question.toLowerCase();
  const long = dna.scores.focusEndurance >= 50;
  const move = MOVE[dna.topModality];

  if (/^(hi|hello|hey)\b/.test(q)) return `Hi! I tailor explanations to your DNA (${dna.archetype.name}). Ask about a topic, or try "how should I revise?"`;
  if (/focus|distract|procrastinat|tired/.test(q))
    return long
      ? 'You have solid focus stamina. Try 45-minute deep-work blocks, phone away, then a 10-minute break.'
      : 'Your focus works best in bursts. Try 25 minutes on, 5 off, and pick one small goal per burst.';
  if (/revise|revision|remember|forget|memor/.test(q))
    return `${dna.recommendations[2]}. Since you learn through ${FORMAT_LABEL[dna.topModality]}: ${move}`;
  if (/dna|my profile|why am i|archetype/.test(q))
    return `${dna.archetype.name} (${dna.dnaCode}): ${dna.archetype.description} Your biggest gap is ${dna.topBlindSpots[0]}.`;
  if (/plan|schedule|what should i study|next/.test(q))
    return `Open Study Plan for your week. A good session for you is ${long ? '45' : '20-25'} minutes using ${FORMAT_LABEL[dna.topModality]}.`;
  if (/quiz|test me|practice/.test(q)) return 'Head to Quiz Runner: finishing a quiz updates your retention and pace scores.';
  return null;
};

/** Offline subject answer from the built-in topic list, adapted to the learner's strongest style. */
export const topicReply = (question: string, dna: DnaProfile): string => {
  const move = MOVE[dna.topModality];
  const qw = new Set(words(question));
  const scored = allTopics
    .map((t) => ({ t, score: words(`${t.name} ${t.skills.join(' ')} ${t.subject}`).filter((w) => qw.has(w)).length }))
    .sort((a, b) => b.score - a.score);
  if (scored[0].score > 0) {
    const t = scored[0].t;
    return `${t.name} (${t.subject}): ${t.description}\n\nHow to learn it your way: ${move}\n\nKey skills: ${t.skills.slice(0, 3).join(', ')}. About ${t.estimatedMinutes} minutes to cover.`;
  }
  return 'I can explain topics from Python, SQL, Statistics, ML and DSA, and I adapt to how you learn. Try "explain recursion" or "how should I revise?"';
};

/** Fully offline tutor (used whenever the backend is unreachable). */
export const tutorReply = (question: string, dna: DnaProfile): string => intentReply(question, dna) ?? topicReply(question, dna);

/** Maps the learner's DNA to the context the backend tutor expects. */
export const toTutorProfile = (dna: DnaProfile, results: QuizResult[]): TutorProfile => {
  const topicName = (id: string) => allTopics.find((t) => t.id === id)?.name;
  return {
    pace: dna.scores.learningPace >= 70 ? 'Fast' : dna.scores.learningPace >= 40 ? 'Moderate' : 'Slow',
    preferred_format: FORMAT_LABEL[dna.topModality],
    attention: dna.scores.focusEndurance >= 70 ? 45 : dna.scores.focusEndurance >= 45 ? 30 : 20,
    weak_topics: weakTopicIds(results).map(topicName).filter((n): n is string => Boolean(n)).slice(0, 10),
  };
};
