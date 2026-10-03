/** Small circular progress indicator (pure CSS conic-gradient, no chart library needed). */
export const Ring = ({ value, size = 56, color = '#4f46e5', label }: { value: number; size?: number; color?: string; label?: string }) => {
  const v = Math.max(0, Math.min(100, Math.round(value)));
  return (
    <div
      role="img" aria-label={label ?? `${v}%`} className="grid shrink-0 place-items-center rounded-full"
      style={{ width: size, height: size, background: `conic-gradient(${color} ${v * 3.6}deg, #e2e8f0 0deg)` }}
    >
      <div className="grid place-items-center rounded-full bg-white text-xs font-extrabold text-slate-800" style={{ width: size - 12, height: size - 12 }}>
        {v}%
      </div>
    </div>
  );
};
