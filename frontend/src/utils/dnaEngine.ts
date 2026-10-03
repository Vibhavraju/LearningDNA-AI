import { ASSESSMENT_QUESTIONS } from '../data/assessmentQuestions';

export type TraitKey =
  | 'visual' | 'auditory' | 'readWrite' | 'kinesthetic'
  | 'focusEndurance' | 'retention' | 'learningPace' | 'consistency';
export type GeneScores = Record<TraitKey, number>;
export type Modality = 'visual' | 'auditory' | 'readWrite' | 'kinesthetic';

export interface DnaProfile {
  scores: GeneScores;
  dnaCode: string;
  codeLegend: string[];
  topModality: Modality;
  lowModality: Modality;
  archetype: { name: string; description: string };
  topStrengths: string[];
  topBlindSpots: string[];
  recommendations: string[];
  createdAt: string;
}

export const TRAIT_KEYS: TraitKey[] = ['visual', 'auditory', 'readWrite', 'kinesthetic', 'focusEndurance', 'retention', 'learningPace', 'consistency'];
export const MODALITIES: Modality[] = ['visual', 'auditory', 'readWrite', 'kinesthetic'];

export const TRAIT_LABEL: Record<TraitKey, string> = {
  visual: 'Visual', auditory: 'Auditory', readWrite: 'Read/Write', kinesthetic: 'Hands-on',
  focusEndurance: 'Focus', retention: 'Retention', learningPace: 'Pace', consistency: 'Consistency',
};
export const TRAIT_HELP: Record<TraitKey, string> = {
  visual: 'Learning from diagrams, charts and flows',
  auditory: 'Learning from talks, discussion and explaining aloud',
  readWrite: 'Learning from reading and writing notes',
  kinesthetic: 'Learning by building and experimenting',
  focusEndurance: 'How long you can stay focused in one sitting',
  retention: 'How well knowledge sticks over time',
  learningPace: 'How quickly you pick up new ideas',
  consistency: 'How steadily you keep up a study routine',
};
export const FORMAT_LABEL: Record<Modality, string> = {
  visual: 'diagrams & mind maps', auditory: 'explain-aloud & discussion',
  readWrite: 'structured notes', kinesthetic: 'hands-on practice',
};
const STRENGTH_NAME: Record<TraitKey, string> = {
  visual: 'Visual Thinking', auditory: 'Listening & Discussion', readWrite: 'Reading & Note-taking', kinesthetic: 'Hands-on Practice',
  focusEndurance: 'Sustained Focus', retention: 'Long-term Retention', learningPace: 'Quick Assimilation', consistency: 'Study Consistency',
};
const BLIND_NAME: Record<TraitKey, string> = {
  visual: 'Visual Processing', auditory: 'Auditory Processing', readWrite: 'Deep Reading', kinesthetic: 'Hands-on Practice',
  focusEndurance: 'Long Focus Sessions', retention: 'Remembering Over Time', learningPace: 'Slow Pacing', consistency: 'Study Consistency',
};

const clamp = (n: number) => Math.max(0, Math.min(100, Math.round(n)));

/** Scores each trait from option weights, normalised between the worst and best possible answer sets. */
export const scoreAnswers = (answers: Record<string, number>): GeneScores => {
  const out = {} as GeneScores;
  for (const t of TRAIT_KEYS) {
    let raw = 0, min = 0, max = 0;
    for (const q of ASSESSMENT_QUESTIONS) {
      const ws = q.options.map((o) => o.weights[t] ?? 0);
      min += Math.min(...ws);
      max += Math.max(...ws);
      const picked = answers[q.id];
      if (picked !== undefined) raw += ws[picked] ?? 0;
    }
    out[t] = max === min ? 50 : clamp(((raw - min) / (max - min)) * 100);
  }
  return out;
};

export const buildProfile = (scores: GeneScores): DnaProfile => {
  const byMod = [...MODALITIES].sort((a, b) => scores[b] - scores[a]);
  const topModality = byMod[0];
  const lowModality = byMod[byMod.length - 1];
  const fast = scores.learningPace >= 50;
  const long = scores.focusEndurance >= 50;
  const active = scores.retention >= 50;

  const letter: Record<Modality, string> = { visual: 'V', auditory: 'A', readWrite: 'R', kinesthetic: 'K' };
  const noun: Record<Modality, string> = { visual: 'Visual', auditory: 'Auditory', readWrite: 'Reading', kinesthetic: 'Hands-on' };
  const role = fast ? (long ? 'Powerhouse' : 'Sprinter') : long ? 'Marathoner' : 'Pacer';

  const ranked = (Object.keys(scores) as TraitKey[]).sort((a, b) => scores[b] - scores[a]);
  const strengths = ranked.filter((k) => scores[k] >= 50).slice(0, 3).map((k) => STRENGTH_NAME[k]);
  const recs = [
    `Lean on ${FORMAT_LABEL[topModality]} when starting a new topic`,
    long ? 'Use 45-minute deep-work blocks with a 10-minute break' : 'Use 25-minute Pomodoro bursts with 5-minute breaks',
    active ? 'Test yourself with active recall instead of re-reading' : 'Review new material again after 1, 3 and 7 days (spaced repetition)',
    `Practise ${FORMAT_LABEL[lowModality]} weekly to close your weakest gap`,
  ];

  return {
    scores,
    dnaCode: [letter[topModality], fast ? 'F' : 'S', long ? 'M' : 'S', active ? 'A' : 'R'].join('-'),
    codeLegend: [noun[topModality], fast ? 'Fast pace' : 'Steady pace', long ? 'Marathon focus' : 'Sprint focus', active ? 'Active recall' : 'Reflective review'],
    topModality, lowModality,
    archetype: {
      name: `The ${noun[topModality]} ${role}`,
      description: `You learn best through ${FORMAT_LABEL[topModality]}, ${fast ? 'pick ideas up quickly' : 'work at a steady, thorough pace'}, and ${long ? 'can stay focused for long sessions' : 'do your best work in short, focused bursts'}.`,
    },
    topStrengths: strengths.length ? strengths : [STRENGTH_NAME[topModality]],
    topBlindSpots: [...ranked].reverse().slice(0, 3).map((k) => BLIND_NAME[k]),
    recommendations: recs,
    createdAt: new Date().toISOString(),
  };
};

export const calculateDna = (answers: Record<string, number>): DnaProfile => buildProfile(scoreAnswers(answers));

/** Feedback loop: a finished quiz nudges retention and pace, so the DNA keeps evolving. */
export const evolveDna = (p: DnaProfile, accuracy: number): DnaProfile => {
  const delta = Math.round((accuracy - 0.6) * 10);
  const scores: GeneScores = {
    ...p.scores,
    retention: clamp(p.scores.retention + delta),
    learningPace: clamp(p.scores.learningPace + Math.round(delta / 2)),
    consistency: clamp(p.scores.consistency + 1),
  };
  return buildProfile(scores);
};
