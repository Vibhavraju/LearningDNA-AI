import { RefreshCw, Check } from 'lucide-react';
import { useUserStore } from '../store/userStore';
import { Card } from '../components/Card';
import { DAY_NAMES } from '../utils/planEngine';

export default function StudyPlan() {
  const { plan, toggleTask, regeneratePlan } = useUserStore();
  const done = plan.filter((t) => t.done).length;
  const pct = plan.length ? Math.round((done / plan.length) * 100) : 0;
  const today = (new Date().getDay() + 6) % 7; // Monday = 0
  const KIND: Record<string, string> = { learn: 'bg-indigo-50 text-indigo-700', revise: 'bg-amber-50 text-amber-700', gap: 'bg-rose-50 text-rose-700' };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div><h1 className="page-title">Study Plan</h1><p className="mt-1 text-slate-500">Built from your DNA and quiz results. Regenerate after a quiz to refresh it.</p></div>
        <button onClick={regeneratePlan} className="btn-primary"><RefreshCw size={16} /> Regenerate</button>
      </div>
      <Card>
        <div className="flex items-center justify-between text-sm font-semibold"><span>Weekly progress</span><span>{done}/{plan.length} done</span></div>
        <div className="mt-2 h-2.5 rounded-full bg-slate-100"><div className="h-2.5 rounded-full bg-emerald-500 transition-all" style={{ width: `${pct}%` }} /></div>
      </Card>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {DAY_NAMES.map((d, di) => {
          const tasks = plan.filter((t) => t.day === di);
          if (!tasks.length) return null;
          return (
            <Card key={d} className={`!p-4 ${di === today ? 'ring-2 ring-indigo-500' : ''}`}>
              <div className="mb-3 flex items-center justify-between font-extrabold text-indigo-700">{d}{di === today && <span className="rounded-full bg-indigo-600 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide text-white">Today</span>}</div>
              <ul className="space-y-3">
                {tasks.map((t) => (
                  <li key={t.id} className="flex gap-2.5">
                    <button aria-label={`Mark ${t.title} ${t.done ? 'not done' : 'done'}`} onClick={() => toggleTask(t.id)}
                      className={`mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded-md border-2 text-white ${t.done ? 'border-emerald-500 bg-emerald-500' : 'border-slate-300'}`}>{t.done && <Check size={12} />}</button>
                    <div className={t.done ? 'opacity-50' : ''}>
                      <div className={`text-sm font-semibold ${t.done ? 'line-through' : ''}`}>{t.title}</div>
                      <div className="text-xs text-slate-500">{t.minutes} min · {t.detail}</div>
                      <span className={`mt-1 inline-block rounded px-1.5 py-0.5 text-[10px] font-bold ${KIND[t.kind]}`}>{t.kind}</span>
                    </div>
                  </li>
                ))}
              </ul>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
