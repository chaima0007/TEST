"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { usePathname } from "next/navigation";

const TIPS: Record<string, { message: string; insight?: string }> = {
  "/dashboard": {
    message: "Bonjour ! Voici votre panorama concurrentiel du jour. Je vois 3 signaux importants à surveiller ce matin.",
    insight: "Salesforce a modifié sa page pricing hier soir — pensez à vérifier l'impact sur vos offres.",
  },
  "/dashboard/competitors": {
    message: "Vous surveillez 5 concurrents actifs. Je vous recommande d'examiner HubSpot en priorité : leur activité a augmenté de 34% cette semaine.",
    insight: "Astuce : filtrez par menace 'Élevée' pour prioriser votre analyse.",
  },
  "/dashboard/pricing": {
    message: "Les tendances de prix révèlent une opportunité. Un concurrent vient de baisser ses tarifs — c'est le moment idéal pour activer vos offres comparatives.",
    insight: "Une baisse de prix chez un concurrent est souvent le signe d'une pression marché ou d'un repositionnement stratégique.",
  },
  "/dashboard/alerts": {
    message: "Vous avez des alertes non lues. Je les ai triées par niveau d'urgence — commencez par les alertes rouges.",
    insight: "Les alertes de type 'Acquisition' ont statistiquement le plus fort impact sur votre positionnement dans les 30 jours.",
  },
  "/dashboard/reports": {
    message: "Vos rapports sont prêts. Le rapport exécutif mensuel est particulièrement riche ce mois-ci — 3 insights stratégiques à partager avec votre CODIR.",
    insight: "Générez un rapport ciblé avant votre prochaine réunion commerciale pour renforcer vos arguments de vente.",
  },
  "/dashboard/compare": {
    message: "La comparaison multi-concurrents est votre meilleur outil avant un pitch client. Sélectionnez jusqu'à 3 acteurs pour une analyse côte à côte.",
    insight: "Identifiez les zones où vous surpassez tous vos concurrents — ce sont vos arguments de vente prioritaires.",
  },
  "/dashboard/settings": {
    message: "Vos paramètres sont configurés de manière optimale. N'oubliez pas d'activer les alertes Slack pour ne manquer aucun signal critique.",
    insight: "Les intégrations Teams et Slack réduisent le temps de réaction moyen de 4h à 23 minutes.",
  },
};

const DEFAULT_TIP = {
  message: "Je suis là pour vous aider à transformer chaque signal concurrentiel en décision stratégique. Posez-moi vos questions.",
  insight: undefined,
};

type Phase = "idle" | "thinking" | "speaking" | "done";

// ─── Avatar SVG ───────────────────────────────────────────────────────────────

interface AvatarProps {
  phase?: Phase;
  blink?: boolean;
  nod?: boolean;
  hovered?: boolean;
  size?: "sm" | "md";
}

function Avatar({ phase = "idle", blink = false, nod = false, hovered = false, size = "md" }: AvatarProps) {
  const irisY   = phase === "thinking" ? -0.8 : 0;
  const browY   = phase === "thinking" ? -1   : 0;
  const mouthSY = phase === "speaking" ? 1.06 : 1;

  return (
    <svg
      viewBox="0 0 80 80"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="w-full h-full select-none"
      style={{
        transform: nod ? "translateY(1.5px)" : "translateY(0)",
        transition: "transform 0.5s cubic-bezier(0.34,1.56,0.64,1)",
      }}
    >
      {/* ── shadow ── */}
      <ellipse cx="40" cy="51" rx="13" ry="2.5" fill="#00000015" />

      {/* ── background ── */}
      <circle cx="40" cy="40" r="40" fill="url(#bg)" />
      <circle cx="40" cy="40" r="40" fill="url(#dots)" opacity="0.16" />
      {hovered && <circle cx="40" cy="40" r="39" stroke="url(#glow)" strokeWidth="2.5" fill="none" />}

      {/* ── body ── */}
      <path d="M8 80 C8 55 20 47 40 47 C60 47 72 55 72 80" fill="url(#body)" />
      <path d="M26 51 L22 74 L40 65 L58 74 L54 51" fill="url(#jacket)" />
      <path d="M36 51 L31 62 L40 65" fill="url(#lapel)" opacity="0.55" />
      <path d="M44 51 L49 62 L40 65" fill="url(#lapel)" opacity="0.55" />
      <path d="M40 65 L38.5 77 M40 65 L41.5 77" stroke="white" strokeWidth="0.4" opacity="0.2" />
      <path d="M8 62 Q22 55 40 53 Q58 55 72 62" stroke="white" strokeWidth="0.7" opacity="0.1" fill="none" />

      {/* ── collar + tie ── */}
      <path d="M35 49 L37 56 L40 54 L43 56 L45 49" fill="white" opacity="0.93" />
      <path d="M38.8 56 L40 66 L41.2 56 L40 54Z" fill="url(#tie)" />
      <ellipse cx="40" cy="55.5" rx="1.4" ry="1" fill="url(#tie)" />

      {/* ── neck ── */}
      <path d="M35 43 Q40 47 45 43 L44 50 Q40 53 36 50Z" fill="url(#skin)" />
      <path d="M36 50 Q40 52.5 44 50 L44 52 Q40 54.5 36 52Z" fill="#D4956E" opacity="0.28" />

      {/* ── head ── */}
      <ellipse cx="40" cy="30" rx="14.5" ry="17" fill="url(#face)" />
      <ellipse cx="40" cy="43.5" rx="11" ry="3" fill="#D4956E" opacity="0.15" />

      {/* ── blush ── */}
      <circle cx="30" cy="36.5" r="4.5" fill="#FFB3A7" opacity="0.18" />
      <circle cx="50" cy="36.5" r="4.5" fill="#FFB3A7" opacity="0.18" />

      {/* ── hair ── */}
      <path d="M25.5 26 C25 15 30 10 40 10 C50 10 55 15 54.5 26 C53 19 50 14 40 14 C30 14 27 19 25.5 26Z" fill="url(#hair)" />
      <ellipse cx="40" cy="13.5" rx="12" ry="5.5" fill="url(#hair)" />
      <path d="M53.5 21 C55 25 55.5 30 54 35" stroke="#3d2b8e" strokeWidth="1.8" strokeLinecap="round" fill="none" opacity="0.65" />
      <path d="M54.5 23 C56.5 27 56.5 32 54.5 37" stroke="#4a3599" strokeWidth="1.1" strokeLinecap="round" fill="none" opacity="0.45" />
      <path d="M26.5 21 C25 25 24.5 30 26 35" stroke="#3d2b8e" strokeWidth="1.8" strokeLinecap="round" fill="none" opacity="0.65" />
      <path d="M25.5 23 C23.5 27 23.5 32 25.5 37" stroke="#4a3599" strokeWidth="1.1" strokeLinecap="round" fill="none" opacity="0.45" />

      {/* ── ears ── */}
      <ellipse cx="26" cy="31.5" rx="2.8" ry="3.3" fill="url(#face)" />
      <ellipse cx="54" cy="31.5" rx="2.8" ry="3.3" fill="url(#face)" />
      <path d="M26.5 29.5 Q27.5 31.5 26.5 33.5" stroke="#D4956E" strokeWidth="0.7" fill="none" opacity="0.4" />
      <path d="M53.5 29.5 Q52.5 31.5 53.5 33.5" stroke="#D4956E" strokeWidth="0.7" fill="none" opacity="0.4" />

      {/* ── eyes ── */}
      <ellipse cx="34.5" cy="29.5" rx="4.2" ry="3.3" fill="white" />
      <ellipse cx="45.5" cy="29.5" rx="4.2" ry="3.3" fill="white" />

      <circle cx="34.8" cy={29.5 + irisY} r="2.4" fill="url(#irisL)" />
      <circle cx="45.8" cy={29.5 + irisY} r="2.4" fill="url(#irisR)" />
      <circle cx="34.8" cy={29.5 + irisY} r="2.4" stroke="#3128a8" strokeWidth="0.35" fill="none" opacity="0.35" />
      <circle cx="45.8" cy={29.5 + irisY} r="2.4" stroke="#3128a8" strokeWidth="0.35" fill="none" opacity="0.35" />
      <circle cx="35.1" cy={29.6 + irisY} r="1.2" fill="#1a1740" />
      <circle cx="46.1" cy={29.6 + irisY} r="1.2" fill="#1a1740" />
      <circle cx="35.7" cy={28.8 + irisY} r="0.6" fill="white" opacity="0.92" />
      <circle cx="46.7" cy={28.8 + irisY} r="0.6" fill="white" opacity="0.92" />
      <circle cx="34.2" cy={30.3 + irisY} r="0.28" fill="white" opacity="0.45" />
      <circle cx="45.2" cy={30.3 + irisY} r="0.28" fill="white" opacity="0.45" />

      {/* blink */}
      {blink && (
        <>
          <ellipse cx="34.5" cy="29.5" rx="4.4" ry="3.5" fill="url(#face)" />
          <ellipse cx="45.5" cy="29.5" rx="4.4" ry="3.5" fill="url(#face)" />
        </>
      )}

      {/* lower lids */}
      <path d="M30.5 31.5 Q34.5 32.5 38.5 31.5" stroke="#D4956E" strokeWidth="0.45" fill="none" opacity="0.3" />
      <path d="M41.5 31.5 Q45.5 32.5 49.5 31.5" stroke="#D4956E" strokeWidth="0.45" fill="none" opacity="0.3" />

      {/* lashes */}
      <path d="M30.8 27.5 L30 26.5 M33 26.5 L32.8 25.4 M35 26.2 L35.2 25 M37.2 26.5 L37.8 25.5 M38.8 27.3 L39.5 26.5" stroke="#2d1b69" strokeWidth="0.65" strokeLinecap="round" opacity="0.55" />
      <path d="M41.8 27.3 L41.2 26.3 M43.2 26.5 L43 25.4 M45.2 26.2 L45.3 25 M47.2 26.5 L47.8 25.5 M49 27.5 L49.8 26.5" stroke="#2d1b69" strokeWidth="0.65" strokeLinecap="round" opacity="0.55" />

      {/* brows */}
      <path
        d={`M30.5 ${25 + browY} Q34.5 ${23 + browY} 38.5 ${25 + browY}`}
        stroke="#2d1b69" strokeWidth="1.5" strokeLinecap="round" fill="none"
        style={{ transition: "d 0.3s ease" }}
      />
      <path
        d={`M41.5 ${25 + browY} Q45.5 ${23 + browY} 49.5 ${25 + browY}`}
        stroke="#2d1b69" strokeWidth="1.5" strokeLinecap="round" fill="none"
        style={{ transition: "d 0.3s ease" }}
      />

      {/* ── nose ── */}
      <path d="M38.5 32.5 Q40 35.5 41.5 32.5" stroke="#C8896A" strokeWidth="1.1" strokeLinecap="round" fill="none" />
      <path d="M37.5 35.5 Q40 36.8 42.5 35.5" stroke="#C8896A" strokeWidth="0.9" strokeLinecap="round" fill="none" opacity="0.65" />
      <circle cx="37.8" cy="35.8" r="1.1" fill="#C8896A" opacity="0.3" />
      <circle cx="42.2" cy="35.8" r="1.1" fill="#C8896A" opacity="0.3" />

      {/* ── mouth ── */}
      <g
        style={{
          transformOrigin: "40px 40px",
          transform: `scaleY(${mouthSY})`,
          transition: "transform 0.12s ease-in-out",
        }}
      >
        <path d="M35.5 38.5 Q37.5 37.5 40 38 Q42.5 37.5 44.5 38.5" stroke="#C8756A" strokeWidth="0.9" strokeLinecap="round" fill="none" />
        <path d="M35.5 38.5 Q40 43.5 44.5 38.5" fill="#C8756A" stroke="#C8756A" strokeWidth="0.4" strokeLinecap="round" opacity="0.88" />
        <path d="M36.5 39 Q40 42 43.5 39 L43 40 Q40 42.5 37 40Z" fill="white" opacity="0.82" />
        <path d="M36.5 39.5 Q40 42.5 43.5 39.5 Q42 42 40 42.2 Q38 42 36.5 39.5Z" fill="#D4856A" opacity="0.22" />
      </g>
      <circle cx="35" cy="40" r="0.75" fill="#D4956E" opacity="0.22" />
      <circle cx="45" cy="40" r="0.75" fill="#D4956E" opacity="0.22" />

      <defs>
        <radialGradient id="bg" cx="42%" cy="35%" r="65%">
          <stop offset="0%" stopColor="#dde4ff" />
          <stop offset="65%" stopColor="#c4d0ff" />
          <stop offset="100%" stopColor="#a8b8f0" />
        </radialGradient>
        <pattern id="dots" x="0" y="0" width="6" height="6" patternUnits="userSpaceOnUse">
          <circle cx="1" cy="1" r="0.65" fill="#6366f1" />
        </pattern>
        <radialGradient id="glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#a5b4fc" />
          <stop offset="100%" stopColor="#6366f1" />
        </radialGradient>
        <radialGradient id="face" cx="45%" cy="40%" r="60%">
          <stop offset="0%" stopColor="#F9D6BC" />
          <stop offset="60%" stopColor="#F4C5A8" />
          <stop offset="100%" stopColor="#E8A882" />
        </radialGradient>
        <linearGradient id="skin" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#F4C5A8" />
          <stop offset="100%" stopColor="#E8A882" />
        </linearGradient>
        <linearGradient id="hair" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#4a3599" />
          <stop offset="55%" stopColor="#3d2b8e" />
          <stop offset="100%" stopColor="#2d1b69" />
        </linearGradient>
        <linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#4338CA" />
          <stop offset="100%" stopColor="#312e81" />
        </linearGradient>
        <linearGradient id="jacket" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#5048e5" />
          <stop offset="50%" stopColor="#4338CA" />
          <stop offset="100%" stopColor="#3730a3" />
        </linearGradient>
        <linearGradient id="lapel" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#6366f1" />
          <stop offset="100%" stopColor="#4338CA" />
        </linearGradient>
        <linearGradient id="tie" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#818cf8" />
          <stop offset="100%" stopColor="#4338ca" />
        </linearGradient>
        <radialGradient id="irisL" cx="38%" cy="33%" r="65%">
          <stop offset="0%" stopColor="#6d71f5" />
          <stop offset="55%" stopColor="#4338CA" />
          <stop offset="100%" stopColor="#312e81" />
        </radialGradient>
        <radialGradient id="irisR" cx="38%" cy="33%" r="65%">
          <stop offset="0%" stopColor="#6d71f5" />
          <stop offset="55%" stopColor="#4338CA" />
          <stop offset="100%" stopColor="#312e81" />
        </radialGradient>
      </defs>
    </svg>
  );
}

// ─── Main component ────────────────────────────────────────────────────────────

export default function ExpertAssistant() {
  const pathname = usePathname();
  const tip = TIPS[pathname] ?? DEFAULT_TIP;

  const [visible,    setVisible]    = useState(false);
  const [open,       setOpen]       = useState(false);
  const [closing,    setClosing]    = useState(false);
  const [phase,      setPhase]      = useState<Phase>("idle");
  const [text,       setText]       = useState("");
  const [done,       setDone]       = useState(false);
  const [blink,      setBlink]      = useState(false);
  const [nod,        setNod]        = useState(false);
  const [hovered,    setHovered]    = useState(false);
  const [pulse,      setPulse]      = useState(false);
  const [greeting,   setGreeting]   = useState(false);
  const [greetFade,  setGreetFade]  = useState(false);
  const [reaction,   setReaction]   = useState<string | null>(null);
  const [userInput,  setUserInput]  = useState("");
  const [userMsgs,   setUserMsgs]   = useState<string[]>([]);

  const blinkRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const nodRef   = useRef<ReturnType<typeof setTimeout> | null>(null);

  // ── appear after short delay ──
  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 900);
    return () => clearTimeout(t);
  }, []);

  // ── one-time greeting bubble ──
  useEffect(() => {
    if (!visible || open) return;
    if (typeof window !== "undefined" && localStorage.getItem("sophia_greeted")) return;
    const t = setTimeout(() => {
      setGreeting(true);
      setGreetFade(false);
      localStorage.setItem("sophia_greeted", "1");
      const t2 = setTimeout(() => setGreetFade(true), 3500);
      const t3 = setTimeout(() => setGreeting(false), 4700);
      return () => { clearTimeout(t2); clearTimeout(t3); };
    }, 2200);
    return () => clearTimeout(t);
  }, [visible, open]);

  // ── pulse on page change ──
  useEffect(() => {
    if (open) return;
    const t = setTimeout(() => setPulse(true),  2800);
    const t2 = setTimeout(() => setPulse(false), 4800);
    return () => { clearTimeout(t); clearTimeout(t2); };
  }, [pathname, open]);

  // ── blink loop (only when panel closed) ──
  const scheduleBlink = useCallback(() => {
    const delay = 4200 + Math.random() * 3200;
    blinkRef.current = setTimeout(() => {
      setBlink(true);
      setTimeout(() => setBlink(false), 140);
      scheduleBlink();
    }, delay);
  }, []);

  useEffect(() => {
    if (open) return;
    scheduleBlink();
    return () => { if (blinkRef.current) clearTimeout(blinkRef.current); };
  }, [open, scheduleBlink]);

  // ── nod loop (only when panel closed) ──
  const scheduleNod = useCallback(() => {
    const delay = 9000 + Math.random() * 6000;
    nodRef.current = setTimeout(() => {
      setNod(true);
      setTimeout(() => setNod(false), 550);
      scheduleNod();
    }, delay);
  }, []);

  useEffect(() => {
    if (open) return;
    scheduleNod();
    return () => { if (nodRef.current) clearTimeout(nodRef.current); };
  }, [open, scheduleNod]);

  // ── typewriter when panel opens or page changes while open ──
  useEffect(() => {
    if (!open) {
      setText("");
      setDone(false);
      setPhase("idle");
      setReaction(null);
      return;
    }
    setPhase("thinking");
    setDone(false);
    setText("");
    setReaction(null);

    let i = 0;
    const msg = tip.message;
    const think = setTimeout(() => {
      setPhase("speaking");
      const iv = setInterval(() => {
        if (i < msg.length) {
          setText(msg.slice(0, i + 1));
          i++;
        } else {
          setPhase("done");
          setDone(true);
          clearInterval(iv);
        }
      }, 17);
      return () => clearInterval(iv);
    }, 550);

    return () => clearTimeout(think);
  }, [open, tip.message]);

  // ── smooth close ──
  const handleClose = () => {
    setClosing(true);
    setTimeout(() => { setOpen(false); setClosing(false); }, 280);
  };

  const handleOpen = () => {
    if (open) { handleClose(); return; }
    setOpen(true);
  };

  const handleSend = () => {
    const msg = userInput.trim();
    if (!msg) return;
    setUserMsgs(prev => [...prev, msg]);
    setUserInput("");
  };

  if (!visible) return null;

  const isTyping = phase === "thinking" || phase === "speaking";

  return (
    <>
      <style>{`
        @keyframes s-in  { from { opacity:0; transform:translateX(16px) scale(.94); } to { opacity:1; transform:translateX(0) scale(1); } }
        @keyframes s-out { from { opacity:1; transform:translateX(0) scale(1); } to { opacity:0; transform:translateX(12px) scale(.94); } }
        @keyframes s-up  { from { opacity:0; transform:translateY(12px) scale(.96); } to { opacity:1; transform:translateY(0) scale(1); } }
        @keyframes s-dn  { from { opacity:1; transform:translateY(0) scale(1); } to { opacity:0; transform:translateY(10px) scale(.96); } }
        @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-4px)} }
        @keyframes breath{ 0%,100%{transform:scale(1)} 50%{transform:scale(1.02)} }
        @keyframes blink { 0%,90%,100%{opacity:1} 95%{opacity:0} }
        .s-float { animation: float 5.5s ease-in-out infinite; }
        .s-breath { animation: breath 3.8s ease-in-out infinite; }
        .cursor-blink { animation: blink 1s step-end infinite; }
      `}</style>

      <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">

        {/* ── chat panel ── */}
        {open && (
          <div
            className="w-80 rounded-2xl shadow-2xl border border-white/60 overflow-hidden"
            style={{
              animation: closing
                ? "s-dn 0.28s cubic-bezier(0.4,0,1,1) forwards"
                : "s-up 0.32s cubic-bezier(0.16,1,0.3,1) forwards",
              background: "linear-gradient(155deg, #ffffff 0%, #f5f3ff 100%)",
            }}
          >
            {/* dot texture */}
            <div
              className="absolute inset-0 pointer-events-none opacity-[0.035] z-0"
              style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg width='10' height='10' viewBox='0 0 10 10' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='1.5' cy='1.5' r='1' fill='%234338ca'/%3E%3C/svg%3E")` }}
            />

            <div className="relative z-10 flex flex-col">

              {/* header */}
              <div className="bg-gradient-to-r from-indigo-600 to-violet-600 px-4 py-3 flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div
                    className="w-9 h-9 rounded-full overflow-hidden ring-2 ring-white/35 shadow-md flex-shrink-0"
                    style={{ animation: phase === "speaking" ? "breath 0.9s ease-in-out infinite" : undefined }}
                  >
                    <Avatar phase={phase} />
                  </div>
                  <div>
                    <p className="text-white font-semibold text-sm leading-none mb-1">Sophia</p>
                    <div className="flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_5px_rgba(52,211,153,0.9)]" style={{ animation: "blink 2.5s ease-in-out infinite" }} />
                      <p className="text-indigo-200 text-[10px] font-medium">Expert · Intelligence Stratégique</p>
                    </div>
                  </div>
                </div>
                <button
                  onClick={handleClose}
                  className="text-white/50 hover:text-white p-1.5 rounded-lg hover:bg-white/10 transition-all active:scale-90"
                >
                  <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
                    <path d="M12 4L4 12M4 4l8 8" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
                  </svg>
                </button>
              </div>

              {/* status bar */}
              <div className="bg-indigo-50/70 border-b border-indigo-100/50 px-4 py-1.5 flex items-center gap-2">
                <div className="flex gap-[3px] items-end h-3">
                  {[0.7, 1, 0.55, 0.85, 0.65].map((h, i) => (
                    <span
                      key={i}
                      className="w-[3px] rounded-full bg-indigo-400"
                      style={{
                        height: `${h * 12}px`,
                        animation: `breath ${0.7 + i * 0.15}s ease-in-out infinite`,
                        animationDelay: `${i * 0.1}s`,
                      }}
                    />
                  ))}
                </div>
                <p className="text-indigo-500 text-[9px] font-semibold tracking-widest uppercase">
                  Sophia analyse votre tableau de bord…
                </p>
              </div>

              {/* messages */}
              <div className="p-4 space-y-3 max-h-72 overflow-y-auto">

                {/* sophia bubble */}
                <div className="flex items-start gap-2.5">
                  <div className="w-7 h-7 rounded-full overflow-hidden ring-2 ring-indigo-100 flex-shrink-0 mt-0.5">
                    <Avatar phase={phase} size="sm" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="bg-white rounded-2xl rounded-tl-none px-3.5 py-2.5 border border-slate-100 shadow-sm">
                      {phase === "thinking" && !text ? (
                        <div className="flex items-center gap-1.5 py-0.5">
                          {[0, 1, 2].map(i => (
                            <span
                              key={i}
                              className="w-2 h-2 rounded-full bg-indigo-300"
                              style={{ animation: `breath 1s ease-in-out infinite`, animationDelay: `${i * 0.22}s` }}
                            />
                          ))}
                        </div>
                      ) : (
                        <p className="text-slate-700 text-sm leading-relaxed break-words">
                          {text}
                          {isTyping && (
                            <span className="inline-block w-[2px] h-3.5 bg-indigo-500 ml-0.5 rounded-sm cursor-blink" />
                          )}
                        </p>
                      )}
                    </div>

                    {/* reactions */}
                    {done && (
                      <div
                        className="flex items-center gap-1.5 mt-1.5 ml-1"
                        style={{ animation: "s-in 0.3s 0.1s cubic-bezier(0.16,1,0.3,1) both" }}
                      >
                        {["👍", "💡", "📊"].map(e => (
                          <button
                            key={e}
                            onClick={() => setReaction(r => r === e ? null : e)}
                            className={`text-sm px-2 py-0.5 rounded-full border transition-all hover:scale-110 active:scale-95 ${
                              reaction === e
                                ? "bg-indigo-100 border-indigo-300 shadow-sm scale-110"
                                : "bg-white/70 border-slate-200 hover:bg-slate-50"
                            }`}
                          >
                            {e}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                {/* insight */}
                {done && tip.insight && (
                  <div
                    className="ml-9 bg-gradient-to-br from-indigo-50 to-violet-50/60 border border-indigo-100 rounded-xl p-3"
                    style={{ animation: "s-in 0.35s 0.2s cubic-bezier(0.16,1,0.3,1) both" }}
                  >
                    <div className="flex items-start gap-2">
                      <div className="w-5 h-5 rounded-full bg-indigo-100 flex items-center justify-center flex-shrink-0 mt-px">
                        <svg className="w-3 h-3 text-indigo-500" viewBox="0 0 14 14" fill="currentColor">
                          <path d="M7 1a6 6 0 100 12A6 6 0 007 1zm0 9a.75.75 0 110-1.5A.75.75 0 017 10zm.75-3.25a.75.75 0 01-1.5 0V5a.75.75 0 011.5 0v1.75z" />
                        </svg>
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-indigo-700 text-xs leading-relaxed">{tip.insight}</p>
                        <div className="flex items-center gap-1.5 mt-1.5">
                          <div className="flex gap-0.5">
                            {[0,1,2,3,4].map(i => (
                              <span key={i} className={`w-1.5 h-1.5 rounded-full ${i < 4 ? "bg-indigo-400" : "bg-indigo-200"}`} />
                            ))}
                          </div>
                          <span className="text-indigo-400 text-[9px] font-medium">847 signaux analysés</span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* quick actions */}
                {done && (
                  <div
                    className="ml-9 flex flex-wrap gap-2"
                    style={{ animation: "s-in 0.35s 0.35s cubic-bezier(0.16,1,0.3,1) both" }}
                  >
                    {["Analyser maintenant", "Générer un rapport"].map(a => (
                      <button
                        key={a}
                        className="text-xs font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 border border-indigo-100/80 px-3 py-1.5 rounded-full transition-all hover:scale-105 active:scale-95 hover:shadow-sm"
                      >
                        {a}
                      </button>
                    ))}
                  </div>
                )}

                {/* user messages */}
                {userMsgs.map((m, i) => (
                  <div key={i} className="flex justify-end" style={{ animation: "s-in 0.25s cubic-bezier(0.16,1,0.3,1) both" }}>
                    <div className="bg-indigo-600 text-white text-sm px-3.5 py-2 rounded-2xl rounded-br-none shadow-sm max-w-[85%]">
                      {m}
                    </div>
                  </div>
                ))}
              </div>

              {/* input */}
              <div className="px-4 pb-4 pt-1">
                <div className="flex items-center gap-2 bg-white border border-slate-200 rounded-xl px-3 py-2.5 focus-within:border-indigo-300 focus-within:shadow-[0_0_0_3px_rgba(99,102,241,0.12)] transition-all shadow-sm">
                  <input
                    type="text"
                    value={userInput}
                    onChange={e => setUserInput(e.target.value)}
                    onKeyDown={e => e.key === "Enter" && handleSend()}
                    placeholder="Posez une question à Sophia…"
                    className="flex-1 bg-transparent text-sm text-slate-700 placeholder-slate-400 outline-none"
                  />
                  <button
                    onClick={handleSend}
                    className="w-6 h-6 flex items-center justify-center rounded-lg bg-indigo-600 hover:bg-indigo-700 transition-all flex-shrink-0 hover:scale-110 active:scale-90 shadow-sm disabled:opacity-40"
                    disabled={!userInput.trim()}
                  >
                    <svg className="w-3.5 h-3.5 text-white" viewBox="0 0 14 14" fill="none">
                      <path d="M2 7h10M7.5 3L12 7l-4.5 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </button>
                </div>
              </div>

            </div>
          </div>
        )}

        {/* ── greeting bubble ── */}
        {greeting && !open && (
          <div
            className="absolute bottom-[4.5rem] right-16 pointer-events-none"
            style={{ animation: greetFade ? "s-out 0.8s ease forwards" : "s-in 0.4s cubic-bezier(0.16,1,0.3,1) forwards" }}
          >
            <div className="relative bg-slate-900 text-white text-sm font-medium px-4 py-2.5 rounded-2xl shadow-xl whitespace-nowrap">
              Bonjour, je suis Sophia&nbsp;👋
              <span
                className="absolute right-[-6px] top-1/2 -translate-y-1/2 w-0 h-0"
                style={{ borderTop: "5px solid transparent", borderBottom: "5px solid transparent", borderLeft: "6px solid #0f172a" }}
              />
            </div>
          </div>
        )}

        {/* ── floating button ── */}
        <div className="relative">
          {pulse && !open && (
            <span className="absolute inset-0 rounded-full animate-ping bg-indigo-400/30" />
          )}
          {!open && (
            <span className="absolute -top-1 -right-1 w-4 h-4 bg-indigo-500 rounded-full border-2 border-white flex items-center justify-center z-10 shadow-sm">
              <span className="text-white text-[8px] font-black">1</span>
            </span>
          )}
          <button
            onClick={handleOpen}
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}
            className="w-14 h-14 rounded-full shadow-xl overflow-hidden ring-2 ring-white ring-offset-2 ring-offset-slate-100"
            style={{
              animation: !open ? "float 5.5s ease-in-out infinite" : undefined,
              transform: hovered ? "scale(1.1)" : open ? "scale(1.02)" : "scale(1)",
              transition: "transform 0.3s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.3s ease",
              boxShadow: hovered ? "0 12px 32px rgba(99,102,241,0.45)" : undefined,
            }}
            title="Sophia — Expert en Intelligence Stratégique"
          >
            <Avatar phase={phase} blink={blink} nod={nod} hovered={hovered} />
          </button>
        </div>

      </div>
    </>
  );
}
