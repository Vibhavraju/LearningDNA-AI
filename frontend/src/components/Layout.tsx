import { useState, ReactNode } from 'react';
import { NavLink, useLocation, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { LayoutDashboard, Dna, CalendarDays, ListChecks, Bot, Library, Settings, Bell, Menu, X, Flame } from 'lucide-react';
import { useUserStore } from '../store/userStore';
import { effectiveStreak } from '../utils/streak';

const NAV = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/dna', label: 'My Learning DNA', icon: Dna },
  { to: '/plan', label: 'Study Plan', icon: CalendarDays },
  { to: '/quiz', label: 'Quiz Runner', icon: ListChecks },
  { to: '/tutor', label: 'AI Tutor', icon: Bot },
  { to: '/resources', label: 'Resources', icon: Library },
  { to: '/settings', label: 'Settings', icon: Settings },
];

export const Layout = ({ children }: { children: ReactNode }) => {
  const [open, setOpen] = useState(false);
  const { pathname } = useLocation();
  const { userProfile, dnaProfile, plan, streak } = useUserStore();
  const pending = plan.filter((t) => !t.done).length;
  const name = userProfile?.name ?? 'Learner';
  const days = effectiveStreak(streak);
  const today = new Date().toLocaleDateString('en', { weekday: 'long', month: 'long', day: 'numeric' });

  return (
    <div className="flex h-screen">
      {open && <div className="fixed inset-0 z-20 bg-slate-900/40 backdrop-blur-sm md:hidden" onClick={() => setOpen(false)} />}
      <aside className={`fixed inset-y-0 left-0 z-30 flex w-64 flex-col bg-gradient-to-b from-[#1B2670] to-[#121A4E] p-4 text-indigo-100 transition-transform md:static md:translate-x-0 ${open ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="mb-7 flex items-center gap-3 px-2 pt-2">
          <div className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-indigo-400 to-sky-400 text-white shadow-lg shadow-indigo-900/40"><Dna size={22} /></div>
          <div className="leading-tight">
            <div className="text-lg font-extrabold text-white">Learning DNA</div>
            <div className="text-xs font-medium text-indigo-300">Learn the way you learn</div>
          </div>
        </div>
        <nav className="flex flex-1 flex-col gap-1" aria-label="Main">
          {NAV.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to} to={to} end={to === '/'} onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-semibold transition ${isActive ? 'bg-white text-[#18235F] shadow-md shadow-black/10' : 'text-indigo-100 hover:bg-white/10'}`}
            >
              <Icon size={18} /> {label}
            </NavLink>
          ))}
        </nav>
        <div className="rounded-2xl bg-white/10 p-3">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-gradient-to-br from-indigo-300 to-sky-300 font-bold text-[#18235F]">{name[0]?.toUpperCase()}</div>
            <div className="min-w-0 text-sm">
              <div className="truncate font-semibold text-white">{name}</div>
              <div className="font-mono text-xs text-indigo-300">{dnaProfile?.dnaCode}</div>
            </div>
          </div>
          <div className="mt-3 flex items-center gap-2 rounded-lg bg-black/15 px-3 py-2 text-xs font-semibold text-indigo-100">
            <Flame size={14} className={days > 0 ? 'text-amber-400' : 'text-indigo-300'} />
            {days > 0 ? `${days}-day study streak` : 'Start a streak today'}
          </div>
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="no-print flex items-center justify-between px-4 py-3 md:px-8">
          <button className="rounded-lg p-2 md:hidden" aria-label="Toggle menu" onClick={() => setOpen(!open)}>
            {open ? <X /> : <Menu />}
          </button>
          <div className="hidden text-sm font-semibold text-slate-500 md:block">{today}</div>
          <Link to="/plan" aria-label={`${pending} tasks pending`} className="relative rounded-xl border border-slate-200 bg-white p-2.5 text-slate-600 shadow-sm hover:text-indigo-700">
            <Bell size={20} />
            {pending > 0 && <span className="absolute -right-1 -top-1 grid h-4 min-w-4 place-items-center rounded-full bg-rose-500 px-1 text-[10px] font-bold text-white">{pending}</span>}
          </Link>
        </header>
        <main className="flex-1 overflow-y-auto px-4 pb-10 md:px-8">
          <motion.div key={pathname} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.22 }} className="mx-auto max-w-6xl">
            {children}
          </motion.div>
        </main>
      </div>
    </div>
  );
};
