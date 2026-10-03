export const effectiveStreak = (s: { count: number; last: string }) => {
  const y = new Date(Date.now() - 864e5).toDateString();
  return s.last === new Date().toDateString() || s.last === y ? s.count : 0;
};
/** Last 7 calendar days (oldest first) with whether each one is part of the current streak. */
export const lastSevenDays = (s: { count: number; last: string }) => {
  const count = effectiveStreak(s);
  const offset = s.last === new Date().toDateString() ? 0 : 1;
  return Array.from({ length: 7 }, (_, i) => {
    const ago = 6 - i;
    const d = new Date(Date.now() - ago * 864e5);
    return { label: d.toLocaleDateString('en', { weekday: 'narrow' }), hit: count > 0 && ago >= offset && ago - offset < count };
  });
};
