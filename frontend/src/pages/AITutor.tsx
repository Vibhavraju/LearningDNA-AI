import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';
import { useUserStore } from '../store/userStore';
import { intentReply, topicReply, toTutorProfile } from '../services/tutor';
import { tutorChat, checkBackend } from '../api/client';

interface Msg { role: 'user' | 'assistant'; content: string; sources?: string[] }
const SUGGESTIONS = ['Explain recursion', 'How should I revise?', 'Why is my DNA this way?', 'Help me focus'];

export default function AITutor() {
  const { dnaProfile, userProfile, quizResults } = useUserStore();
  const [messages, setMessages] = useState<Msg[]>([
    { role: 'assistant', content: `Hi ${userProfile?.name ?? ''}! I explain things the way you learn best (${dnaProfile?.archetype.name}). What are you working on?` },
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const [online, setOnline] = useState<boolean | null>(null);
  const end = useRef<HTMLDivElement>(null);

  useEffect(() => { end.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, typing]);
  useEffect(() => {
    let alive = true;
    checkBackend().then((ok) => { if (alive) setOnline(ok); });
    return () => { alive = false; };
  }, []);

  if (!dnaProfile) return null;

  const send = async (text: string) => {
    const msg = text.trim();
    if (!msg || typing) return;
    setMessages((m) => [...m, { role: 'user', content: msg }]);
    setInput('');
    setTyping(true);

    // Questions about the learner are answered locally; subject questions go to the backend (RAG + LLM) when it is up.
    let reply: Msg = { role: 'assistant', content: intentReply(msg, dnaProfile) ?? '' };
    if (!reply.content) {
      try {
        const r = await tutorChat(msg, toTutorProfile(dnaProfile, quizResults));
        setOnline(true);
        // No retrieved sources means the backend could not ground the answer; the local topic guide is more useful then.
        reply = r.sources.length > 0 ? { role: 'assistant', content: r.response, sources: r.sources } : { role: 'assistant', content: topicReply(msg, dnaProfile) };
      } catch {
        setOnline(false);
        reply = { role: 'assistant', content: topicReply(msg, dnaProfile) };
      }
    }
    setMessages((m) => [...m, reply]);
    setTyping(false);
  };

  return (
    <div className="flex h-[calc(100vh-110px)] flex-col">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
        <h1 className="page-title">AI Tutor</h1>
        <span className={`chip text-xs ${online ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}`}>
          <span className={`h-2 w-2 rounded-full ${online ? 'bg-emerald-500' : 'bg-amber-500'}`} />
          {online === null ? 'Checking tutor…' : online ? 'Connected to backend' : 'Offline mode'}
        </span>
      </div>
      <div className="flex-1 space-y-4 overflow-y-auto rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        {messages.map((m, i) => (
          <div key={i} className={`flex items-end gap-2.5 ${m.role === 'user' ? 'flex-row-reverse' : ''}`}>
            <div className={`grid h-8 w-8 shrink-0 place-items-center rounded-full ${m.role === 'user' ? 'bg-indigo-100 text-indigo-700' : 'bg-gradient-to-br from-indigo-500 to-sky-500 text-white'}`}>
              {m.role === 'user' ? <User size={16} /> : <Bot size={16} />}
            </div>
            <div className={`max-w-[80%] whitespace-pre-line rounded-2xl px-4 py-3 leading-relaxed ${m.role === 'user' ? 'rounded-br-md bg-indigo-600 text-white' : 'rounded-bl-md bg-slate-100'}`}>
              {m.content}
              {m.sources && m.sources.length > 0 && <div className="mt-2 text-xs font-semibold text-slate-500">Sources: {m.sources.join(', ')}</div>}
            </div>
          </div>
        ))}
        {typing && (
          <div className="flex items-end gap-2.5" aria-live="polite">
            <div className="grid h-8 w-8 place-items-center rounded-full bg-gradient-to-br from-indigo-500 to-sky-500 text-white"><Bot size={16} /></div>
            <div className="rounded-2xl rounded-bl-md bg-slate-100 px-4 py-3 text-slate-400">Thinking…</div>
          </div>
        )}
        <div ref={end} />
      </div>
      <div className="mt-3 flex flex-wrap gap-2">
        {SUGGESTIONS.map((s) => <button key={s} onClick={() => send(s)} className="rounded-full border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium hover:border-indigo-400 hover:bg-indigo-50">{s}</button>)}
      </div>
      <form className="mt-3 flex gap-2" onSubmit={(e) => { e.preventDefault(); send(input); }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask anything…" maxLength={500} aria-label="Message" className="flex-1 rounded-xl border border-slate-300 px-4 py-3" />
        <button className="btn-primary" aria-label="Send" disabled={!input.trim() || typing}><Send size={18} /></button>
      </form>
    </div>
  );
}
