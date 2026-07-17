"use client";

// Agent animé « assistant juridique ».
// Objectif : humaniser et dédramatiser le juridique — sobre, chaleureux, JAMAIS enfantin.
// Style : figure géométrique épurée (buste), palette professionnelle, micro-animations discrètes
// (flottement lent, clignement, légère respiration). Pas de gros yeux cartoon, pas de couleurs criardes.
//
// TRANSPARENCE (obligatoire, sans exception) : ces personnages sont des ASSISTANTS VIRTUELS
// (IA + supervision humaine), PAS de vrais avocats. La mention est affichée automatiquement
// sous chaque avatar — impossible d'en oublier un. Voir la page « Qui sont nos assistants ? ».

type Accent = "indigo" | "rose" | "emerald" | "amber" | "sky" | "blue" | "violet" | "teal";

const ACCENTS: Record<Accent, { from: string; to: string; soft: string; ring: string; text: string }> = {
  indigo: { from: "#6366f1", to: "#4338ca", soft: "#eef2ff", ring: "#c7d2fe", text: "#3730a3" },
  rose: { from: "#f43f5e", to: "#be123c", soft: "#fff1f2", ring: "#fecdd3", text: "#9f1239" },
  emerald: { from: "#10b981", to: "#047857", soft: "#ecfdf5", ring: "#a7f3d0", text: "#065f46" },
  amber: { from: "#f59e0b", to: "#b45309", soft: "#fffbeb", ring: "#fde68a", text: "#92400e" },
  sky: { from: "#0ea5e9", to: "#0369a1", soft: "#f0f9ff", ring: "#bae6fd", text: "#075985" },
  blue: { from: "#2563eb", to: "#1e40af", soft: "#eff6ff", ring: "#bfdbfe", text: "#1e3a8a" },
  violet: { from: "#8b5cf6", to: "#6d28d9", soft: "#f5f3ff", ring: "#ddd6fe", text: "#5b21b6" },
  teal: { from: "#14b8a6", to: "#0f766e", soft: "#f0fdfa", ring: "#99f6e4", text: "#115e59" },
};

export default function AgentAvocat({
  name = "Votre référent",
  role,
  message,
  accent = "indigo",
  size = 96,
}: {
  name?: string;
  role?: string;
  message?: string;
  accent?: Accent;
  size?: number;
}) {
  const c = ACCENTS[accent] ?? ACCENTS.indigo;
  const uid = `${accent}-${size}`;

  return (
    <div className="flex items-center gap-4">
      <div
        className="relative flex-shrink-0"
        style={{ width: size, height: size, animation: "agentFloat 5s ease-in-out infinite" }}
      >
        <svg viewBox="0 0 100 100" width={size} height={size} role="img" aria-label={`Avatar ${name}${role ? ", " + role : ""}`}>
          <defs>
            <linearGradient id={`bg-${uid}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={c.from} />
              <stop offset="100%" stopColor={c.to} />
            </linearGradient>
          </defs>

          {/* Pastille de fond */}
          <circle cx="50" cy="50" r="48" fill={`url(#bg-${uid})`} />
          <circle cx="50" cy="50" r="48" fill="none" stroke="rgba(255,255,255,0.25)" strokeWidth="1.5" />

          {/* Buste : épaules (veste) */}
          <path d="M22 92c0-14 12.5-22 28-22s28 8 28 22z" fill="rgba(255,255,255,0.95)" />
          <path d="M50 70c-6 6-6 14-6 22h12c0-8 0-16-6-22z" fill={c.soft} />
          {/* Col + cravate sobre */}
          <path d="M50 70l-6 5 6 6 6-6z" fill={c.from} />
          <path d="M50 81l-3 9h6z" fill={c.to} />

          {/* Tête (légère respiration) */}
          <g style={{ transformOrigin: "50px 46px", animation: "agentBreathe 5s ease-in-out infinite" }}>
            <circle cx="50" cy="42" r="17" fill="#f1d9c4" />
            {/* Cheveux sobres */}
            <path d="M33 40c0-11 8-18 17-18s17 7 17 18c0-6-6-9-17-9s-17 3-17 9z" fill="#3f3a36" />
            {/* Yeux qui clignent */}
            <g fill="#3f3a36" style={{ transformOrigin: "50px 42px", animation: "agentBlink 6s ease-in-out infinite" }}>
              <circle cx="44" cy="42" r="1.8" />
              <circle cx="56" cy="42" r="1.8" />
            </g>
            {/* Sourire discret, rassurant */}
            <path d="M45 49c2 2.5 8 2.5 10 0" fill="none" stroke="#b07a5a" strokeWidth="1.8" strokeLinecap="round" />
          </g>
        </svg>
      </div>

      {(name || role || message) && (
        <div className="min-w-0">
          {(name || role) && (
            <p className="leading-tight" style={{ color: c.text }}>
              <span className="font-bold tracking-tight">{name}</span>
              {role && (
                <span className="text-xs font-medium opacity-70">
                  {name ? " · " : ""}
                  {role}
                </span>
              )}
            </p>
          )}
          {/* Mention de transparence — affichée automatiquement sur CHAQUE avatar (sans exception) */}
          <span
            className="mt-1 inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide"
            style={{ backgroundColor: c.soft, color: c.text, border: `1px solid ${c.ring}` }}
            title="Ces assistants sont des personnages virtuels (IA + supervision humaine). Ce ne sont pas de vrais avocats."
          >
            <span aria-hidden="true">✦</span> Assistant virtuel · pas un avocat réel
          </span>
          {message && (
            <div
              className="relative mt-2 inline-block rounded-2xl rounded-tl-sm px-3.5 py-2 text-sm leading-relaxed"
              style={{ backgroundColor: c.soft, color: c.text, border: `1px solid ${c.ring}` }}
            >
              {message}
            </div>
          )}
        </div>
      )}

      <style>{`
        @keyframes agentFloat { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
        @keyframes agentBreathe { 0%,100% { transform: scale(1); } 50% { transform: scale(1.025); } }
        @keyframes agentBlink {
          0%, 92%, 100% { transform: scaleY(1); }
          95% { transform: scaleY(0.1); }
        }
        @media (prefers-reduced-motion: reduce) {
          [aria-label^="Avatar"] { animation: none !important; }
        }
      `}</style>
    </div>
  );
}
