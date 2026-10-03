import { Link } from 'react-router-dom';
import { Target, Flame, AlertTriangle, ArrowRight, Check } from 'lucide-react';
import { useUserStore } from '../store/userStore';
import { Card } from '../components/Card';
import { DNARadar, CodeTiles } from '../components/DNARadar';
import { Ring } from '../components/Ring';
import { TRAIT_KEYS, TRAIT_LABEL } from '../utils/dnaEngine';
import { effectiveStreak, lastSevenDays } from '../utils/streak';
import { SUBJECTS } from '../data/topics';

export default function Dashboard() {
  const { userProfile, dnaProfile, plan, streak, quizResults, toggleTask } = useUserStore();
  if (!dnaProfile) return null;
  const { archetype, scores, dnaCode, codeLegend, topStrengths, topBlindSpots, lowModality } = dnaProfile;
  const name = userProfile?.name?.trim();
  const next = plan.find((t) => !t.done);
  const doneCount = plan.filter((t) => t.done).length;
  const todays = plan.filter((t) => !t.done).slice(0, 3);
  const count = effectiveStreak(streak);
  const pct = plan.length ? Math.round((doneCount / plan.length) * 100) : 0;
  const avg = quizResults.length ? Math.round((100 * quizResults.reduce((sum, r) => sum + r.correct / r.total, 0)) / quizResults.length) : null;
  const topTrait = TRAIT_KEYS.reduce((best, k) => (scores[k] > scores[best] ? k : best), TRAIT_KEYS[0]);
  const subjectName = (id: string) => SUBJECTS.find((s) => s.id === id)?.name ?? id;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title">{name ? `Welcome back, ${name}` : 'Welcome back'}</h1>
        <p className="mt-1 text-slate-500">{doneCount} of {plan.length} study tasks done this week.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <Card className="flex items-center gap-4 !p-5">
          <Ring value={pct} label={`${pct}% of the weekly plan done`} />
          <div><div className="text-sm text-slate-500">Weekly plan</div><div className="font-bold">{doneCount}/{plan.length} tasks done</div></div>
        </Card>
        <Card className="flex items-center gap-4 !p-5">
          <Ring value={avg ?? 0} color="#10b981" label={avg === null ? 'No quizzes yet' : `Quiz average ${avg}%`} />
          <div><div className="text-sm text-slate-500">Quiz average</div><div className="font-bold">{avg === null ? 'No quizzes yet' : `${quizResults.length} quiz${quizResults.length === 1 ? '' : 'zes'} taken`}</div></div>
        </Card>
        <Card className="flex items-center gap-4 !p-5">
          <Ring value={scores[topTrait]} color="#8b5cf6" label={`${TRAIT_LABEL[topTrait]} score ${scores[topTrait]}`} />
          <div><div className="text-sm text-slate-500">Strongest trait</div><div className="font-bold">{TRAIT_LABEL[topTrait]}</div></div>
        </Card>
      </div>

      <div className="grid gap-5 lg:grid-cols-[5fr_6fr]">
        <Card className="flex flex-col justify-center">
          <CodeTiles code={dnaCode} legend={codeLegend} />
          <h2 className="mt-6 text-2xl font-extrabold tracking-tight">{archetype.name}</h2>
          <p className="mt-1.5 max-w-prose leading-relaxed text-slate-600">{archetype.description}</p>
          <div className="mt-4 flex flex-wrap gap-2 text-sm font-semibold">
            <span className="rounded-full bg-emerald-50 px-3 py-1 text-emerald-800">Strongest: {topStrengths[0]}</span>
            <span className="rounded-full bg-rose-50 px-3 py-1 text-rose-700">Needs work: {topBlindSpots[0]}</span>
          </div>
        </Card>
        <Card>
          <h3 className="font-bold">Your learning profile</h3>
          <DNARadar scores={scores} />
        </Card>
      </div>

      <div className="grid gap-5 md:grid-cols-3">
        <Card className="flex items-center gap-4">
          <div className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-indigo-50 text-indigo-600"><Target size={20} /></div>
          <div className="min-w-0 flex-1">
            <div className="text-sm text-slate-500">Next action</div>
            <div className="line-clamp-2 font-bold leading-snug">{next ? next.title : 'All tasks done'}</div>
          </div>
          <Link to={next ? '/plan' : '/quiz'} className="btn-primary !px-3.5">{next ? 'Start' : 'Quiz'} <ArrowRight size={15} /></Link>
        </Card>
        <Card className="flex items-center gap-4">
          <div className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-amber-50 text-amber-600"><Flame size={20} /></div>
          <div className="min-w-0">
            <div className="text-sm text-slate-500">Study streak</div>
            <div className="font-bold">{count} {count === 1 ? 'day' : 'days'}</div>
            <div className="mt-2 flex gap-1" aria-hidden>
              {lastSevenDays(streak).map((d, i) => (
                <span key={i} className={`grid h-6 w-6 place-items-center rounded-md text-[11px] font-bold ${d.hit ? 'bg-amber-500 text-white' : 'bg-slate-100 text-slate-400'}`}>{d.label}</span>
              ))}
            </div>
          </div>
        </Card>
        <Card className="flex items-center gap-4">
          <div className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-rose-50 text-rose-600"><AlertTriangle size={20} /></div>
          <div className="min-w-0 flex-1">
            <div className="text-sm text-slate-500">Biggest gap</div>
            <div className="truncate font-bold">{topBlindSpots[0]}</div>
            <div className="mt-2 h-2 rounded-full bg-slate-100"><div className="h-2 rounded-full bg-rose-500" style={{ width: `${scores[lowModality]}%` }} /></div>
            <div className="mt-1 text-xs text-slate-500">{TRAIT_LABEL[lowModality]} score {scores[lowModality]}/100</div>
          </div>
        </Card>
      </div>

      <div className="grid gap-5 lg:grid-cols-[6fr_5fr]">
        <Card>
          <div className="mb-3 flex items-center justify-between"><h3 className="font-bold">Up next</h3><Link to="/plan" className="text-sm font-semibold text-indigo-700">Full plan</Link></div>
          {todays.length === 0 ? <p className="text-slate-500">You finished this week's plan. Take a quiz to keep your DNA evolving.</p> : (
            <ul className="space-y-3">
              {todays.map((t) => (
                <li key={t.id} className="flex items-center gap-3">
                  <button aria-label={`Mark ${t.title} done`} onClick={() => toggleTask(t.id)} className="grid h-6 w-6 place-items-center rounded-lg border-2 border-slate-300 text-white hover:border-indigo-500"><Check size={14} /></button>
                  <div><div className="font-semibold">{t.title}</div><div className="text-sm text-slate-500">{t.minutes} min · {t.detail}</div></div>
                </li>
              ))}
            </ul>
          )}
        </Card>
        <Card>
          <div className="mb-3 flex items-center justify-between"><h3 className="font-bold">Recent quizzes</h3><Link to="/quiz" className="text-sm font-semibold text-indigo-700">Take a quiz</Link></div>
          {quizResults.length === 0 ? <p className="text-slate-500">No quizzes yet. Your first one will update your retention and pace scores.</p> : (
            <ul className="space-y-3">
              {quizResults.slice(0, 4).map((r, i) => (
                <li key={i} className="flex items-center justify-between">
                  <span className="font-semibold">{subjectName(r.subject)}</span>
                  <span className="text-sm text-slate-500">{new Date(r.date).toLocaleDateString()} · <b className="text-slate-800">{r.correct}/{r.total}</b></span>
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>
    </div>
  );
}
