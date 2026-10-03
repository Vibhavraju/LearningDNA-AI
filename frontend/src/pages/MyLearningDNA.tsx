import { useState } from 'react';
import { Info, Printer, RotateCcw } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { useUserStore } from '../store/userStore';
import { Card } from '../components/Card';
import { DNARadar, TraitBar, CodeTiles } from '../components/DNARadar';
import { TRAIT_KEYS, TRAIT_LABEL, TRAIT_HELP } from '../utils/dnaEngine';

export default function MyLearningDNA() {
  const { dnaProfile, history, retakeAssessment } = useUserStore();
  const [science, setScience] = useState(false);
  if (!dnaProfile) return null;
  const { archetype, scores, dnaCode, codeLegend, topStrengths, topBlindSpots, recommendations } = dnaProfile;
  const first = history[0]?.scores;
  const trend = history.map((h, i) => ({ update: i === 0 ? 'Start' : `#${i}`, Retention: h.scores.retention, Pace: h.scores.learningPace, Consistency: h.scores.consistency }));

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="page-title">My Learning DNA</h1>
        <div className="no-print flex gap-2">
          <button className="btn-ghost" onClick={() => window.print()}><Printer size={16} /> Export to PDF</button>
          <button className="btn-ghost" onClick={() => { if (confirm('Retake the assessment? Your current DNA will be replaced.')) retakeAssessment(); }}><RotateCcw size={16} /> Retake</button>
        </div>
      </div>

      <div className="grid gap-5 lg:grid-cols-2">
        <Card>
          <div className="flex items-start justify-between">
            <CodeTiles code={dnaCode} legend={codeLegend} />
            <button onClick={() => setScience(!science)} aria-label="About the science" className="no-print ml-3 text-slate-400 hover:text-indigo-700"><Info /></button>
          </div>
          <h2 className="mt-5 text-2xl font-extrabold tracking-tight">{archetype.name}</h2>
          <p className="mt-1.5 leading-relaxed text-slate-600">{archetype.description}</p>
          {science && <p className="mt-4 rounded-xl bg-indigo-50 p-4 text-sm text-indigo-900">Style scores are inspired by the VARK model and the Felder-Silverman learning styles. Pace, focus, retention and consistency come from your scenario answers, and retention and pace update after each quiz. This is a study aid, not a clinical test.</p>}
        </Card>
        <Card><DNARadar scores={scores} height={300} /></Card>
      </div>

      <Card>
        <h3 className="mb-4 font-bold">Trait scores</h3>
        <div className="grid gap-x-10 gap-y-5 md:grid-cols-2">
          {TRAIT_KEYS.map((k) => <TraitBar key={k} label={TRAIT_LABEL[k]} value={scores[k]} hint={TRAIT_HELP[k]} delta={first ? scores[k] - first[k] : 0} />)}
        </div>
        {history.length > 1 && <p className="mt-4 text-xs text-slate-500">Green and red numbers show change since your first assessment ({history.length - 1} update{history.length > 2 ? 's' : ''} from quizzes).</p>}
      </Card>

      {history.length > 1 && (
        <Card>
          <h3 className="mb-1 font-bold">How your DNA is evolving</h3>
          <p className="mb-3 text-sm text-slate-500">Every finished quiz nudges retention, pace and consistency.</p>
          <div style={{ height: 240 }} role="img" aria-label="Line chart of retention, pace and consistency after each quiz">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trend} margin={{ top: 8, right: 16, bottom: 0, left: -16 }}>
                <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" />
                <XAxis dataKey="update" tick={{ fill: '#64748b', fontSize: 12 }} />
                <YAxis domain={[0, 100]} tick={{ fill: '#64748b', fontSize: 12 }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="Retention" stroke="#4f46e5" strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="Pace" stroke="#10b981" strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="Consistency" stroke="#f59e0b" strokeWidth={2.5} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      )}

      <div className="grid gap-5 md:grid-cols-3">
        <Card><h3 className="mb-3 font-bold">Strengths</h3><ul className="list-inside list-disc space-y-1.5 text-slate-700">{topStrengths.map((s) => <li key={s}>{s}</li>)}</ul></Card>
        <Card><h3 className="mb-3 font-bold">Blind spots</h3><ul className="list-inside list-disc space-y-1.5 text-slate-700">{topBlindSpots.map((s) => <li key={s}>{s}</li>)}</ul></Card>
        <Card><h3 className="mb-3 font-bold">What to do</h3><ul className="list-inside list-disc space-y-1.5 text-slate-700">{recommendations.map((s) => <li key={s}>{s}</li>)}</ul></Card>
      </div>
    </div>
  );
}
