import { useState, type ReactNode } from 'react';
import { motion } from 'framer-motion';
import { Dna, ArrowLeft, Clock, Target, Sparkles } from 'lucide-react';
import { useUserStore } from '../store/userStore';
import { ASSESSMENT_QUESTIONS as QS } from '../data/assessmentQuestions';
import { SUBJECTS } from '../data/topics';

const GOALS = ['Ace my exams', 'Get job-ready', 'Learn a new skill', 'Build projects'];

export default function AssessmentPage() {
  const { assessmentAnswers, setAssessmentAnswer, setUserProfile, completeAssessment } = useUserStore();
  const saved = useUserStore.getState().userProfile;
  const [step, setStep] = useState(-1); // -1 = welcome
  const [name, setName] = useState(saved?.name ?? '');
  const [subject, setSubject] = useState(saved?.subject ?? SUBJECTS[0].id);
  const [goal, setGoal] = useState(saved?.goal ?? GOALS[0]);

  const start = () => { setUserProfile({ name: name.trim(), subject, goal }); setStep(0); };
  const pick = (i: number) => {
    setAssessmentAnswer(QS[step].id, i);
    if (step < QS.length - 1) setStep(step + 1);
    else completeAssessment();
  };

  const shell = (children: ReactNode) => (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-indigo-50 to-sky-50 p-4">
      <motion.div key={step} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }} className="w-full max-w-2xl rounded-3xl bg-white p-6 shadow-xl shadow-indigo-200/50 sm:p-10">{children}</motion.div>
    </div>
  );

  if (step === -1) {
    return shell(
      <>
        <div className="mb-6 flex items-center gap-2.5 text-indigo-700"><span className="grid h-9 w-9 place-items-center rounded-xl bg-gradient-to-br from-indigo-500 to-sky-500 text-white"><Dna size={20} /></span> <span className="text-lg font-extrabold">Learning DNA AI</span></div>
        <h1 className="page-title">Discover how you learn</h1>
        <p className="mt-2 text-slate-600">Answer {QS.length} short scenarios. There are no right answers, and your Learning DNA keeps updating as you study.</p>
        <ul className="mt-5 flex flex-wrap gap-2 text-sm font-semibold text-slate-600">
          <li className="chip bg-indigo-50 text-indigo-700"><Clock size={14} /> About 5 minutes</li>
          <li className="chip bg-sky-50 text-sky-700"><Target size={14} /> 8-trait profile</li>
          <li className="chip bg-emerald-50 text-emerald-700"><Sparkles size={14} /> Personal study plan</li>
        </ul>
        <label className="mt-6 block text-sm font-semibold">Your first name
          <input value={name} onChange={(e) => setName(e.target.value)} maxLength={30} placeholder="e.g. Asha"
            className="mt-1.5 w-full rounded-xl border border-slate-300 px-4 py-3 font-normal" />
        </label>
        <label className="mt-4 block text-sm font-semibold">What are you studying?
          <select value={subject} onChange={(e) => setSubject(e.target.value)} className="mt-1.5 w-full rounded-xl border border-slate-300 bg-white px-4 py-3 font-normal">
            {SUBJECTS.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
        </label>
        <div className="mt-4 text-sm font-semibold">Your goal
          <div className="mt-1.5 flex flex-wrap gap-2">
            {GOALS.map((g) => (
              <button key={g} onClick={() => setGoal(g)} className={`rounded-full border px-4 py-2 font-medium ${goal === g ? 'border-indigo-600 bg-indigo-600 text-white' : 'border-slate-300 hover:bg-slate-50'}`}>{g}</button>
            ))}
          </div>
        </div>
        <button className="btn-primary mt-8 w-full" disabled={!name.trim()} onClick={start}>Start assessment</button>
      </>,
    );
  }

  const q = QS[step];
  const chosen = assessmentAnswers[q.id];
  return shell(
    <>
      <div className="mb-6">
        <div className="flex justify-between text-sm font-semibold text-indigo-700"><span>Question {step + 1} of {QS.length}</span><span>{q.category}</span></div>
        <div className="mt-2 h-2 rounded-full bg-slate-100"><div className="h-2 rounded-full bg-indigo-600 transition-all" style={{ width: `${((step + 1) / QS.length) * 100}%` }} /></div>
      </div>
      <p className="text-slate-600">{q.scenario}</p>
      {q.question && <h2 className="mt-2 text-xl font-bold">{q.question}</h2>}
      <div className="mt-5 space-y-3">
        {q.options.map((o, i) => (
          <button key={i} onClick={() => pick(i)}
            className={`w-full rounded-xl border-2 p-4 text-left transition ${chosen === i ? 'border-indigo-600 bg-indigo-50' : 'border-slate-200 hover:border-indigo-400 hover:bg-indigo-50/50'}`}>
            {o.text}
          </button>
        ))}
      </div>
      <button onClick={() => setStep(step - 1)} className="mt-6 inline-flex items-center gap-1.5 font-semibold text-slate-500 hover:text-indigo-700"><ArrowLeft size={16} /> Back</button>
    </>,
  );
}
