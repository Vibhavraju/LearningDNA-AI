import { useState } from 'react';
import { Card } from '../components/Card';
import { useUserStore } from '../store/userStore';
import { SUBJECTS } from '../data/topics';

export default function Settings() {
  const { userProfile, updateProfile, regeneratePlan, retakeAssessment, reset } = useUserStore();
  const [name, setName] = useState(userProfile?.name ?? '');
  const [subject, setSubject] = useState(userProfile?.subject ?? SUBJECTS[0].id);
  const [saved, setSaved] = useState(false);

  const save = () => {
    const changed = subject !== userProfile?.subject;
    updateProfile({ name: name.trim(), subject });
    if (changed) regeneratePlan();
    setSaved(true); setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="mx-auto max-w-xl space-y-6">
      <h1 className="page-title">Settings</h1>
      <Card className="space-y-4">
        <h2 className="font-bold">Profile</h2>
        <label className="block text-sm font-semibold">Name<input value={name} onChange={(e) => setName(e.target.value)} className="mt-1.5 w-full rounded-xl border border-slate-300 px-4 py-2.5 font-normal" /></label>
        <label className="block text-sm font-semibold">Main subject
          <select value={subject} onChange={(e) => setSubject(e.target.value)} className="mt-1.5 w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 font-normal">{SUBJECTS.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}</select>
        </label>
        <button className="btn-primary" disabled={!name.trim()} onClick={save}>{saved ? 'Saved' : 'Save changes'}</button>
      </Card>
      <Card className="space-y-3">
        <h2 className="font-bold">Data</h2>
        <button className="btn-ghost w-full" onClick={() => { if (confirm('Retake the assessment? Your DNA will be replaced.')) retakeAssessment(); }}>Retake assessment</button>
        <button className="w-full rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-rose-700" onClick={() => { if (confirm('Reset all data? This cannot be undone.')) { reset(); window.location.href = '/'; } }}>Reset all data</button>
      </Card>
    </div>
  );
}
