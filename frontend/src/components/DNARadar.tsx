import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, Radar, Tooltip } from 'recharts';
import { GeneScores, TRAIT_KEYS, TRAIT_LABEL } from '../utils/dnaEngine';

export const DNARadar = ({ scores, height = 340 }: { scores: GeneScores; height?: number }) => {
  const data = TRAIT_KEYS.map((k) => ({ trait: TRAIT_LABEL[k], value: scores[k] }));
  return (
    <div style={{ height }} aria-label="Learning DNA radar chart" role="img">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} outerRadius="68%" margin={{ top: 10, right: 36, bottom: 10, left: 36 }}>
          <PolarGrid stroke="#dfe2ee" />
          <PolarAngleAxis dataKey="trait" tick={{ fill: '#475569', fontSize: 12.5 }} />
          <Tooltip formatter={(v: number) => [`${v} / 100`, 'Score']} />
          <Radar dataKey="value" stroke="#4350D8" strokeWidth={2} fill="#4350D8" fillOpacity={0.28} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export const TraitBar = ({ label, value, hint, delta }: { label: string; value: number; hint?: string; delta?: number }) => (
  <div>
    <div className="flex items-baseline justify-between text-sm">
      <span className="font-semibold text-slate-800">{label}</span>
      <span className="font-bold tabular-nums">
        {value}
        {delta ? <span className={`ml-1.5 text-xs font-semibold ${delta > 0 ? 'text-emerald-600' : 'text-rose-600'}`}>{delta > 0 ? '+' : ''}{delta}</span> : null}
      </span>
    </div>
    <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-slate-100">
      <div className="h-full rounded-full bg-indigo-600" style={{ width: `${value}%` }} />
    </div>
    {hint && <p className="mt-1 text-xs text-slate-500">{hint}</p>}
  </div>
);

export const CodeTiles = ({ code, legend }: { code: string; legend: string[] }) => (
  <div className="flex gap-2.5" aria-label={`DNA code ${code}`}>
    {code.split('-').map((c, i) => (
      <div key={i} className="flex-1 rounded-xl bg-indigo-50 px-2 py-3 text-center">
        <div className="text-2xl font-extrabold leading-none text-indigo-700">{c}</div>
        <div className="mt-1.5 text-[11px] leading-tight text-slate-500">{legend[i]}</div>
      </div>
    ))}
  </div>
);
