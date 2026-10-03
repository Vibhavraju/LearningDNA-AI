import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { calculateDna, evolveDna, DnaProfile } from '../utils/dnaEngine';
import { generatePlan, PlanTask, QuizResult } from '../utils/planEngine';

export interface UserProfile { name: string; subject: string; goal: string }
interface Streak { count: number; last: string }
export interface DnaSnapshot { date: string; scores: DnaProfile['scores'] }

interface UserState {
  userProfile: UserProfile | null;
  assessmentAnswers: Record<string, number>;
  dnaProfile: DnaProfile | null;
  isOnboardingComplete: boolean;
  history: DnaSnapshot[];
  plan: PlanTask[];
  quizResults: QuizResult[];
  streak: Streak;

  setUserProfile: (p: UserProfile) => void;
  setAssessmentAnswer: (questionId: string, optionIndex: number) => void;
  completeAssessment: () => void;
  retakeAssessment: () => void;
  updateProfile: (p: Partial<UserProfile>) => void;
  toggleTask: (id: string) => void;
  regeneratePlan: () => void;
  recordQuiz: (r: QuizResult) => void;
  reset: () => void;
}

const today = () => new Date().toDateString();
const bumpStreak = (s: Streak): Streak => {
  if (s.last === today()) return s;
  const yesterday = new Date(Date.now() - 864e5).toDateString();
  return { count: s.last === yesterday ? s.count + 1 : 1, last: today() };
};
/** Carries "done" flags from the old plan onto a freshly generated one (matched by stable task id). */
const withProgress = (fresh: PlanTask[], old: PlanTask[]): PlanTask[] =>
  fresh.map((t) => ({ ...t, done: old.find((o) => o.id === t.id)?.done ?? false }));

const initial = {
  userProfile: null, assessmentAnswers: {}, dnaProfile: null, isOnboardingComplete: false,
  history: [] as DnaSnapshot[], plan: [] as PlanTask[], quizResults: [] as QuizResult[], streak: { count: 0, last: '' },
};

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({
      ...initial,
      setUserProfile: (userProfile) => set({ userProfile }),
      setAssessmentAnswer: (id, idx) => set((s) => ({ assessmentAnswers: { ...s.assessmentAnswers, [id]: idx } })),
      completeAssessment: () => {
        const { assessmentAnswers, userProfile, quizResults } = get();
        const dna = calculateDna(assessmentAnswers);
        set({
          dnaProfile: dna, isOnboardingComplete: true,
          history: [{ date: new Date().toISOString(), scores: dna.scores }],
          plan: generatePlan(dna, userProfile?.subject ?? 'python', quizResults),
        });
      },
      retakeAssessment: () => set({ assessmentAnswers: {}, dnaProfile: null, isOnboardingComplete: false }),
      updateProfile: (p) => set((s) => (s.userProfile ? { userProfile: { ...s.userProfile, ...p } } : s)),
      toggleTask: (id) => {
        const wasDone = get().plan.find((t) => t.id === id)?.done;
        set((s) => ({
          plan: s.plan.map((t) => (t.id === id ? { ...t, done: !t.done } : t)),
          streak: wasDone ? s.streak : bumpStreak(s.streak),
        }));
      },
      regeneratePlan: () => {
        const { dnaProfile, userProfile, quizResults, plan } = get();
        if (dnaProfile) set({ plan: withProgress(generatePlan(dnaProfile, userProfile?.subject ?? 'python', quizResults), plan) });
      },
      recordQuiz: (r) => {
        const { dnaProfile, quizResults, history, userProfile } = get();
        const results = [r, ...quizResults].slice(0, 50);
        const next = dnaProfile ? evolveDna(dnaProfile, r.correct / r.total) : null;
        set((s) => ({
          quizResults: results,
          dnaProfile: next,
          history: next ? [...history, { date: new Date().toISOString(), scores: next.scores }].slice(-30) : history,
          streak: bumpStreak(s.streak),
          plan: next ? withProgress(generatePlan(next, userProfile?.subject ?? 'python', results), s.plan) : s.plan,
        }));
      },
      reset: () => set({ ...initial }),
    }),
    { name: 'dna-storage', version: 2, migrate: () => ({ ...initial }) as never },
  ),
);
