import { useState } from 'react';
import { Check, X } from 'lucide-react';
import { useUserStore } from '../store/userStore';
import { Card } from '../components/Card';
import { QUIZ_BANK, QuizQuestion } from '../data/quizBank';
import { SUBJECTS } from '../data/topics';

/** Fisher-Yates shuffle (Array.sort with a random comparator is biased). */
const pickQuestions = (subject: string) => {
  const pool = QUIZ_BANK.filter((q) => q.subject === subject);
  for (let i = pool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  return pool.slice(0, 5);
};
const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];

export default function QuizRunner() {
  const { userProfile, recordQuiz } = useUserStore();
  const [subject, setSubject] = useState(userProfile?.subject ?? SUBJECTS[0].id);
  const [qs, setQs] = useState<QuizQuestion[] | null>(null);
  const [i, setI] = useState(0);
  const [sel, setSel] = useState<number | null>(null);
  const [wrong, setWrong] = useState<QuizQuestion[]>([]);
  const [finished, setFinished] = useState(false);

  const start = () => { setQs(pickQuestions(subject)); setI(0); setSel(null); setWrong([]); setFinished(false); };
  const total = qs?.length ?? 0;
  const correct = total - wrong.length;

  const choose = (idx: number) => {
    if (sel !== null || !qs) return;
    setSel(idx);
    if (idx !== qs[i].correct) setWrong((w) => [...w, qs[i]]);
  };
  const next = () => {
    if (!qs) return;
    if (i < qs.length - 1) { setI(i + 1); setSel(null); return; }
    const missed = new Set(wrong.map((q) => q.id));
    recordQuiz({ date: new Date().toISOString(), subject, topicIds: [...new Set(qs.filter((q) => missed.has(q.id)).map((q) => q.topicId))], correct: total - wrong.length, total });
    setFinished(true);
  };

  if (!qs) {
    return (
      <div className="mx-auto max-w-2xl space-y-6">
        <h1 className="page-title">Quiz Runner</h1>
        <Card>
          <p className="text-slate-600">Pick a subject for a 5-question quiz. Your result updates your retention and pace scores, and your study plan.</p>
          <div className="mt-4 flex flex-wrap gap-2">
            {SUBJECTS.map((s) => (
              <button key={s.id} onClick={() => setSubject(s.id)} className={`rounded-full border px-4 py-2 text-sm font-semibold ${subject === s.id ? 'border-indigo-600 bg-indigo-600 text-white' : 'border-slate-300 hover:bg-slate-50'}`}>{s.name}</button>
            ))}
          </div>
          <button className="btn-primary mt-6" onClick={start}>Start quiz</button>
        </Card>
      </div>
    );
  }

  if (finished) {
    const topics = [...new Set(wrong.map((q) => SUBJECTS.flatMap((s) => s.topics).find((t) => t.id === q.topicId)?.name).filter(Boolean))];
    return (
      <div className="mx-auto max-w-2xl space-y-6">
        <h1 className="page-title">Quiz complete</h1>
        <Card className="text-center">
          <div className="text-5xl font-extrabold text-indigo-700">{correct}/{total}</div>
          <p className="mt-2 text-slate-600">{correct === total ? 'Perfect score. Your retention score went up.' : 'Your DNA and study plan have been updated.'}</p>
          {topics.length > 0 && <p className="mt-3 text-sm text-slate-600">Review: <b>{topics.join(', ')}</b></p>}
          <div className="mt-6 flex justify-center gap-3"><button className="btn-primary" onClick={start}>Try another</button><button className="btn-ghost" onClick={() => setQs(null)}>Change subject</button></div>
        </Card>
      </div>
    );
  }

  const q = qs[i];
  const answered = i + (sel !== null ? 1 : 0);
  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <h1 className="page-title">Quiz Runner</h1>
      <Card>
        <div className="mb-1 flex items-center justify-between text-sm font-semibold text-indigo-700"><span>Question {i + 1} of {total}</span><span className="text-slate-400">{answered - wrong.length} correct so far</span></div>
        <div className="mb-5 h-1.5 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-indigo-600 transition-all" style={{ width: `${(answered / total) * 100}%` }} /></div>
        <h2 className="mb-5 text-xl font-bold">{q.text}</h2>
        <div className="space-y-3">
          {q.options.map((o, idx) => {
            const state = sel === null ? '' : idx === q.correct ? 'border-emerald-500 bg-emerald-50' : idx === sel ? 'border-rose-500 bg-rose-50' : 'opacity-60';
            return (
              <button key={idx} onClick={() => choose(idx)} disabled={sel !== null}
                className={`flex w-full items-center gap-3 rounded-xl border-2 p-4 text-left transition ${sel === null ? 'border-slate-200 hover:border-indigo-400 hover:bg-indigo-50/40' : 'border-slate-200'} ${state}`}>
                <span className="grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-slate-100 text-xs font-bold text-slate-600">{LETTERS[idx]}</span>
                <span className="flex-1">{o}</span>{sel !== null && idx === q.correct && <Check size={18} className="text-emerald-600" />}{sel === idx && idx !== q.correct && <X size={18} className="text-rose-600" />}
              </button>
            );
          })}
        </div>
        {sel !== null && (
          <div className="mt-5 rounded-xl bg-slate-50 p-4 text-sm text-slate-700"><b>{sel === q.correct ? 'Correct. ' : 'Not quite. '}</b>{q.explanation}</div>
        )}
        {sel !== null && <button className="btn-primary mt-5 w-full" onClick={next}>{i === total - 1 ? 'Finish' : 'Next question'}</button>}
      </Card>
    </div>
  );
}
