import { useState } from 'react';
import { ExternalLink, Search } from 'lucide-react';
import { Card } from '../components/Card';
import { RESOURCES } from '../data/resources';
import { SUBJECTS } from '../data/topics';
import { useUserStore } from '../store/userStore';

export default function Resources() {
  const { dnaProfile } = useUserStore();
  const [q, setQ] = useState('');
  const [subject, setSubject] = useState('all');
  const list = RESOURCES
    .filter((r) => (subject === 'all' || r.subject === subject) && `${r.title} ${r.type}`.toLowerCase().includes(q.toLowerCase()))
    .sort((a, b) => Number(b.style === dnaProfile?.topModality) - Number(a.style === dnaProfile?.topModality));

  return (
    <div className="space-y-6">
      <h1 className="page-title">Resources</h1>
      <div className="relative"><Search className="absolute left-3.5 top-3.5 text-slate-400" size={18} />
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search resources…" className="w-full rounded-xl border border-slate-300 py-3 pl-10 pr-4" /></div>
      <div className="flex flex-wrap gap-2">
        {[{ id: 'all', name: 'All' }, ...SUBJECTS].map((s) => (
          <button key={s.id} onClick={() => setSubject(s.id)} className={`rounded-full border px-4 py-1.5 text-sm font-semibold ${subject === s.id ? 'border-indigo-600 bg-indigo-600 text-white' : 'border-slate-300 bg-white hover:bg-slate-50'}`}>{s.name}</button>
        ))}
      </div>
      {list.length === 0 ? <p className="text-slate-500">No resources match your search.</p> : (
        <div className="grid gap-4 md:grid-cols-2">
          {list.map((r) => (
            <Card key={r.id} className="flex items-center justify-between gap-3 !p-5">
              <div className="min-w-0">
                <h3 className="font-bold">{r.title}</h3>
                <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-slate-500">
                  <span>{SUBJECTS.find((s) => s.id === r.subject)?.name} · {r.type}</span>
                  {r.style === dnaProfile?.topModality && <span className="rounded bg-emerald-50 px-1.5 py-0.5 font-bold text-emerald-700">Matches your style</span>}
                  {r.style === dnaProfile?.lowModality && <span className="rounded bg-amber-50 px-1.5 py-0.5 font-bold text-amber-700">Builds your gap</span>}
                </div>
              </div>
              <a href={r.url} target="_blank" rel="noreferrer" aria-label={`Open ${r.title}`} className="shrink-0 rounded-lg bg-slate-100 p-2 hover:bg-slate-200"><ExternalLink size={16} /></a>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
