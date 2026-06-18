"use client";

import { useState, useEffect, useRef } from "react";
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

type EmotionalState = "idle" | "thinking" | "speaking";

interface AvatarSVGProps {
  emotionalState?: EmotionalState;
  isHovered?: boolean;
  blinkPhase?: boolean;
  nodPhase?: boolean;
}

function AvatarSVG({ emotionalState = "idle", isHovered = false, blinkPhase = false, nodPhase = false }: AvatarSVGProps) {
  const eyeLidHeight = blinkPhase ? 3.5 : 0;
  const irisOffsetY = emotionalState === "thinking" ? -0.8 : 0;
  const mouthScaleY = emotionalState === "speaking" ? 1.05 : 1;
  const browOffsetY = emotionalState === "thinking" ? -1 : 0;
  const headTiltY = nodPhase ? 1 : 0;
  const bodyScale = emotionalState === "idle" ? 1 : 1;

  return (
    <svg
      viewBox="0 0 80 80"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="w-full h-full"
      style={{ transform: `translateY(${headTiltY}px)`, transition: "transform 0.4s ease" }}
    >
      {/* Soft drop shadow under chin */}
      <ellipse cx="40" cy="50" rx="12" ry="2.5" fill="#00000018" />

      {/* Background — radial gradient, softer and more professional */}
      <circle cx="40" cy="40" r="40" fill="url(#bgGrad)" />

      {/* Subtle dot-pattern texture overlay */}
      <circle cx="40" cy="40" r="40" fill="url(#dotPattern)" opacity="0.18" />

      {/* Body / shoulders */}
      <path
        d="M10 78 C10 56 21 48 40 48 C59 48 70 56 70 78"
        fill="url(#bodyGrad)"
      />

      {/* Blazer — left lapel with subtle fold highlight */}
      <path d="M28 52 L24 72 L40 64 L56 72 L52 52" fill="url(#jacketGrad)" opacity="0.97" />
      {/* Left lapel fold */}
      <path d="M36 52 L32 62 L40 64" fill="url(#lapelGrad)" opacity="0.6" />
      {/* Right lapel fold */}
      <path d="M44 52 L48 62 L40 64" fill="url(#lapelGrad)" opacity="0.6" />
      {/* Blazer crease lines */}
      <path d="M40 64 L38 76" stroke="white" strokeWidth="0.4" opacity="0.25" />
      <path d="M40 64 L42 76" stroke="white" strokeWidth="0.4" opacity="0.25" />
      {/* Shoulder highlight */}
      <path d="M10 60 Q22 54 40 52 Q58 54 70 60" stroke="white" strokeWidth="0.6" opacity="0.12" fill="none" />

      {/* Shirt collar visible */}
      <path d="M35 50 L37 57 L40 55 L43 57 L45 50" fill="white" opacity="0.92" />

      {/* Tie */}
      <path d="M38.5 57 L40 66 L41.5 57 L40 55Z" fill="url(#tieGrad)" opacity="0.85" />
      {/* Tie knot */}
      <ellipse cx="40" cy="56.5" rx="1.5" ry="1" fill="url(#tieGrad)" opacity="0.9" />

      {/* Neck — skin tone gradient */}
      <path d="M35 44 Q40 48 45 44 L44 51 Q40 53.5 36 51Z" fill="url(#skinGrad)" />
      {/* Neck shadow */}
      <path d="M36 51 Q40 53 44 51 L44 53 Q40 55 36 53Z" fill="#D4956E" opacity="0.3" />

      {/* Head — improved proportions, wider forehead */}
      <ellipse cx="40" cy="31" rx="14.5" ry="17" fill="url(#faceSkinGrad)" />

      {/* Jaw shadow for depth */}
      <ellipse cx="40" cy="44" rx="10" ry="3" fill="#D4956E" opacity="0.18" />

      {/* Cheek blush */}
      <circle cx="30.5" cy="37" r="4" fill="#FFB3A7" opacity="0.2" />
      <circle cx="49.5" cy="37" r="4" fill="#FFB3A7" opacity="0.2" />

      {/* ===== HAIR ===== */}
      {/* Main hair cap */}
      <path
        d="M25.5 27 C25 16 30 11 40 11 C50 11 55 16 54.5 27 C53 20 50 15 40 15 C30 15 27 20 25.5 27Z"
        fill="url(#hairGrad)"
      />
      <ellipse cx="40" cy="14.5" rx="12" ry="5.5" fill="url(#hairGrad)" />

      {/* Hair strands — right side */}
      <path d="M53 22 C54.5 25 55 30 53.5 35" stroke="#3d2b8e" strokeWidth="1.8" strokeLinecap="round" fill="none" opacity="0.7" />
      <path d="M54 24 C56 27 56 32 54 37" stroke="#4a3599" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.5" />
      {/* Hair strands — left side */}
      <path d="M27 22 C25.5 25 25 30 26.5 35" stroke="#3d2b8e" strokeWidth="1.8" strokeLinecap="round" fill="none" opacity="0.7" />
      <path d="M26 24 C24 27 24 32 26 37" stroke="#4a3599" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.5" />
      {/* Top hair detail strands */}
      <path d="M33 13 C34 11 38 10.5 40 11" stroke="#5040a0" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.5" />
      <path d="M47 13 C46 11 42 10.5 40 11" stroke="#5040a0" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.5" />

      {/* Ears */}
      <ellipse cx="26" cy="32.5" rx="2.8" ry="3.3" fill="url(#faceSkinGrad)" />
      <ellipse cx="54" cy="32.5" rx="2.8" ry="3.3" fill="url(#faceSkinGrad)" />
      {/* Ear inner */}
      <path d="M26.5 30.5 Q27.5 32.5 26.5 34.5" stroke="#D4956E" strokeWidth="0.7" fill="none" opacity="0.5" />
      <path d="M53.5 30.5 Q52.5 32.5 53.5 34.5" stroke="#D4956E" strokeWidth="0.7" fill="none" opacity="0.5" />

      {/* ===== EYES ===== */}
      {/* Eye whites — almond shaped */}
      <ellipse cx="34.5" cy="30.5" rx="4.2" ry="3.3" fill="white" />
      <ellipse cx="45.5" cy="30.5" rx="4.2" ry="3.3" fill="white" />

      {/* Iris — detailed with gradient */}
      <circle cx="34.8" cy={30.5 + irisOffsetY} r="2.4" fill="url(#irisGradL)" style={{ transition: "cy 0.3s ease" }} />
      <circle cx="45.8" cy={30.5 + irisOffsetY} r="2.4" fill="url(#irisGradR)" style={{ transition: "cy 0.3s ease" }} />
      {/* Iris ring detail */}
      <circle cx="34.8" cy={30.5 + irisOffsetY} r="2.4" stroke="#3128a8" strokeWidth="0.4" fill="none" opacity="0.4" />
      <circle cx="45.8" cy={30.5 + irisOffsetY} r="2.4" stroke="#3128a8" strokeWidth="0.4" fill="none" opacity="0.4" />
      {/* Pupils */}
      <circle cx="35.1" cy={30.6 + irisOffsetY} r="1.2" fill="#1a1740" />
      <circle cx="46.1" cy={30.6 + irisOffsetY} r="1.2" fill="#1a1740" />
      {/* Main eye shine */}
      <circle cx="35.7" cy={29.7 + irisOffsetY} r="0.6" fill="white" opacity="0.9" />
      <circle cx="46.7" cy={29.7 + irisOffsetY} r="0.6" fill="white" opacity="0.9" />
      {/* Secondary small shine */}
      <circle cx="34.3" cy={31.2 + irisOffsetY} r="0.3" fill="white" opacity="0.5" />
      <circle cx="45.3" cy={31.2 + irisOffsetY} r="0.3" fill="white" opacity="0.5" />

      {/* Eyelids (for blink animation) */}
      {blinkPhase && (
        <>
          <ellipse cx="34.5" cy="30.5" rx="4.2" ry={eyeLidHeight} fill="#F4C5A8" />
          <ellipse cx="45.5" cy="30.5" rx="4.2" ry={eyeLidHeight} fill="#F4C5A8" />
        </>
      )}

      {/* Lower eyelid line */}
      <path d="M30.5 32.5 Q34.5 33.5 38.5 32.5" stroke="#D4956E" strokeWidth="0.5" fill="none" opacity="0.35" />
      <path d="M41.5 32.5 Q45.5 33.5 49.5 32.5" stroke="#D4956E" strokeWidth="0.5" fill="none" opacity="0.35" />

      {/* Eyelashes — top (subtle) */}
      <path d="M30.8 28.5 L30 27.5 M33 27.5 L32.8 26.4 M35 27.2 L35.2 26 M37.2 27.5 L37.8 26.5 M38.8 28.3 L39.5 27.5" stroke="#2d1b69" strokeWidth="0.7" strokeLinecap="round" opacity="0.6" />
      <path d="M41.8 28.3 L41.2 27.3 M43.2 27.5 L43 26.4 M45.2 27.2 L45.3 26 M47.2 27.5 L47.8 26.5 M49 28.5 L49.8 27.5" stroke="#2d1b69" strokeWidth="0.7" strokeLinecap="round" opacity="0.6" />

      {/* Eyebrows — natural arch, shift up when thinking */}
      <path d={`M30.5 ${26 + browOffsetY} Q34.5 ${24 + browOffsetY} 38.5 ${26 + browOffsetY}`} stroke="#2d1b69" strokeWidth="1.5" strokeLinecap="round" fill="none" style={{ transition: "d 0.3s ease" }} />
      <path d={`M41.5 ${26 + browOffsetY} Q45.5 ${24 + browOffsetY} 49.5 ${26 + browOffsetY}`} stroke="#2d1b69" strokeWidth="1.5" strokeLinecap="round" fill="none" style={{ transition: "d 0.3s ease" }} />

      {/* ===== NOSE ===== */}
      <path d="M38.5 33.5 Q40 36.5 41.5 33.5" stroke="#C8896A" strokeWidth="1.1" strokeLinecap="round" fill="none" />
      <path d="M37.5 36.5 Q38.8 37.5 40 37.2 Q41.2 37.5 42.5 36.5" stroke="#C8896A" strokeWidth="0.9" strokeLinecap="round" fill="none" opacity="0.7" />
      <circle cx="37.8" cy="36.8" r="1.1" fill="#C8896A" opacity="0.35" />
      <circle cx="42.2" cy="36.8" r="1.1" fill="#C8896A" opacity="0.35" />

      {/* ===== MOUTH ===== */}
      {/* Mouth group — animated when speaking */}
      <g style={{ transformOrigin: "40px 41px", transform: `scaleY(${mouthScaleY})`, transition: "transform 0.15s ease-in-out" }}>
        {/* Upper lip */}
        <path d="M35.5 39.5 Q37.5 38.5 40 39 Q42.5 38.5 44.5 39.5" stroke="#C8756A" strokeWidth="1" strokeLinecap="round" fill="none" />
        {/* Main smile */}
        <path d="M35.5 39.5 Q40 44.5 44.5 39.5" fill="#C8756A" stroke="#C8756A" strokeWidth="0.5" strokeLinecap="round" opacity="0.9" />
        {/* Teeth glimpse */}
        <path d="M36.5 40 Q40 43 43.5 40 L43 41 Q40 43.5 37 41Z" fill="white" opacity="0.85" />
        {/* Lower lip */}
        <path d="M36.5 40.5 Q40 43.5 43.5 40.5 Q42 43 40 43.2 Q38 43 36.5 40.5Z" fill="#D4856A" opacity="0.25" />
      </g>

      {/* Smile dimples */}
      <circle cx="35" cy="41" r="0.8" fill="#D4956E" opacity="0.25" />
      <circle cx="45" cy="41" r="0.8" fill="#D4956E" opacity="0.25" />

      {/* Hover glow effect */}
      {isHovered && (
        <circle cx="40" cy="40" r="39" stroke="url(#hoverGlow)" strokeWidth="2" fill="none" opacity="0.6" />
      )}

      <defs>
        {/* Background gradient — softer, more professional */}
        <radialGradient id="bgGrad" cx="42%" cy="35%" r="65%">
          <stop offset="0%" stopColor="#dde4ff" />
          <stop offset="60%" stopColor="#c4d0ff" />
          <stop offset="100%" stopColor="#a8b8f0" />
        </radialGradient>

        {/* Dot micro-texture */}
        <pattern id="dotPattern" x="0" y="0" width="6" height="6" patternUnits="userSpaceOnUse">
          <circle cx="1" cy="1" r="0.7" fill="#6366f1" />
        </pattern>

        {/* Skin gradients */}
        <radialGradient id="faceSkinGrad" cx="45%" cy="40%" r="60%">
          <stop offset="0%" stopColor="#F8D5B8" />
          <stop offset="60%" stopColor="#F4C5A8" />
          <stop offset="100%" stopColor="#E8A882" />
        </radialGradient>
        <linearGradient id="skinGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#F4C5A8" />
          <stop offset="100%" stopColor="#E8A882" />
        </linearGradient>

        {/* Hair gradient */}
        <linearGradient id="hairGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#4a3599" />
          <stop offset="50%" stopColor="#3d2b8e" />
          <stop offset="100%" stopColor="#2d1b69" />
        </linearGradient>

        {/* Body / jacket gradients */}
        <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#4338CA" />
          <stop offset="100%" stopColor="#312e81" />
        </linearGradient>
        <linearGradient id="jacketGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#4f46e5" />
          <stop offset="50%" stopColor="#4338CA" />
          <stop offset="100%" stopColor="#3730a3" />
        </linearGradient>
        <linearGradient id="lapelGrad" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#6366f1" />
          <stop offset="100%" stopColor="#4338CA" />
        </linearGradient>

        {/* Tie */}
        <linearGradient id="tieGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#818cf8" />
          <stop offset="100%" stopColor="#4338ca" />
        </linearGradient>

        {/* Iris gradients — each eye slightly different for realism */}
        <radialGradient id="irisGradL" cx="40%" cy="35%" r="65%">
          <stop offset="0%" stopColor="#6366f1" />
          <stop offset="50%" stopColor="#4338CA" />
          <stop offset="100%" stopColor="#312e81" />
        </radialGradient>
        <radialGradient id="irisGradR" cx="40%" cy="35%" r="65%">
          <stop offset="0%" stopColor="#6366f1" />
          <stop offset="50%" stopColor="#4338CA" />
          <stop offset="100%" stopColor="#312e81" />
        </radialGradient>

        {/* Hover glow */}
        <radialGradient id="hoverGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#a5b4fc" />
          <stop offset="100%" stopColor="#6366f1" />
        </radialGradient>
      </defs>
    </svg>
  );
}

// Small avatar for chat bubbles
function MiniAvatar() {
  return (
    <div className="w-7 h-7 rounded-full overflow-hidden flex-shrink-0 mt-0.5 ring-2 ring-indigo-100 shadow-sm">
      <AvatarSVG emotionalState="idle" />
    </div>
  );
}

export default function ExpertAssistant() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [visible, setVisible] = useState(false);
  const [typing, setTyping] = useState(false);
  const [displayedText, setDisplayedText] = useState("");
  const [pulse, setPulse] = useState(false);
  const [emotionalState, setEmotionalState] = useState<EmotionalState>("idle");
  const [isHovered, setIsHovered] = useState(false);
  const [blinkPhase, setBlinkPhase] = useState(false);
  const [nodPhase, setNodPhase] = useState(false);
  const [showGreeting, setShowGreeting] = useState(false);
  const [greetingVisible, setGreetingVisible] = useState(false);
  const [messageReactions, setMessageReactions] = useState<Record<string, string>>({});
  const blinkTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const nodTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const tip = TIPS[pathname] ?? DEFAULT_TIP;

  // Initial visibility
  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 1200);
    return () => clearTimeout(t);
  }, []);

  // Greeting bubble — only once per session
  useEffect(() => {
    if (!visible) return;
    const alreadyGreeted = typeof window !== "undefined" && localStorage.getItem("sophia_greeted");
    if (alreadyGreeted) return;
    const t = setTimeout(() => {
      setShowGreeting(true);
      setGreetingVisible(true);
      localStorage.setItem("sophia_greeted", "1");
      // Fade out after 4 seconds
      const t2 = setTimeout(() => setGreetingVisible(false), 4000);
      // Remove from DOM after fade
      const t3 = setTimeout(() => setShowGreeting(false), 5200);
      return () => { clearTimeout(t2); clearTimeout(t3); };
    }, 2000);
    return () => clearTimeout(t);
  }, [visible]);

  // Pulse ring on pathname change
  useEffect(() => {
    const t = setTimeout(() => setPulse(true), 3000);
    const t2 = setTimeout(() => setPulse(false), 5000);
    return () => { clearTimeout(t); clearTimeout(t2); };
  }, [pathname]);

  // Blink animation — every 4-7 seconds when idle
  useEffect(() => {
    if (open) return;
    const scheduleBlink = () => {
      const delay = 4000 + Math.random() * 3000;
      blinkTimerRef.current = setTimeout(() => {
        setBlinkPhase(true);
        setTimeout(() => setBlinkPhase(false), 150);
        scheduleBlink();
      }, delay);
    };
    scheduleBlink();
    return () => { if (blinkTimerRef.current) clearTimeout(blinkTimerRef.current); };
  }, [open]);

  // Nod animation — subtle head movement every 8-14 seconds when idle
  useEffect(() => {
    if (open) return;
    const scheduleNod = () => {
      const delay = 8000 + Math.random() * 6000;
      nodTimerRef.current = setTimeout(() => {
        setNodPhase(true);
        setTimeout(() => setNodPhase(false), 600);
        scheduleNod();
      }, delay);
    };
    scheduleNod();
    return () => { if (nodTimerRef.current) clearTimeout(nodTimerRef.current); };
  }, [open]);

  // Typewriter effect + emotional states
  useEffect(() => {
    if (!open) {
      setDisplayedText("");
      setEmotionalState("idle");
      return;
    }
    setEmotionalState("thinking");
    setTyping(true);
    setDisplayedText("");
    let i = 0;
    const msg = tip.message;
    // Short "thinking" pause before speaking
    const thinkDelay = setTimeout(() => {
      setEmotionalState("speaking");
      const interval = setInterval(() => {
        if (i < msg.length) {
          setDisplayedText(msg.slice(0, i + 1));
          i++;
        } else {
          setTyping(false);
          setEmotionalState("idle");
          clearInterval(interval);
        }
      }, 18);
      return () => clearInterval(interval);
    }, 600);
    return () => clearTimeout(thinkDelay);
  }, [open, tip.message]);

  const handleReaction = (emoji: string) => {
    setMessageReactions(prev => ({ ...prev, main: emoji }));
  };

  if (!visible) return null;

  return (
    <>
      {/* Global keyframe styles */}
      <style>{`
        @keyframes sophia-slide-in {
          from { opacity: 0; transform: translateX(20px) scale(0.95); }
          to   { opacity: 1; transform: translateX(0)   scale(1); }
        }
        @keyframes sophia-fade-out {
          from { opacity: 1; transform: translateX(0)   scale(1); }
          to   { opacity: 0; transform: translateX(10px) scale(0.95); }
        }
        @keyframes sophia-breathe {
          0%, 100% { transform: scale(1); }
          50%       { transform: scale(1.018); }
        }
        @keyframes sophia-float {
          0%, 100% { transform: translateY(0px); }
          50%       { transform: translateY(-3px); }
        }
        @keyframes sophia-mouth-talk {
          0%, 100% { transform: scaleY(1); }
          50%       { transform: scaleY(1.07); }
        }
        .sophia-breathing {
          animation: sophia-breathe 4s ease-in-out infinite;
        }
        .sophia-floating {
          animation: sophia-float 6s ease-in-out infinite;
        }
      `}</style>

      <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">

        {/* Chat panel */}
        {open && (
          <div
            className="w-80 rounded-2xl shadow-2xl border border-slate-100/80 overflow-hidden"
            style={{
              animation: "sophia-slide-in 0.3s cubic-bezier(0.16,1,0.3,1) forwards",
              background: "linear-gradient(160deg, #ffffff 0%, #f8f7ff 100%)",
            }}
          >
            {/* Micro-texture overlay on panel */}
            <div
              className="absolute inset-0 pointer-events-none opacity-[0.04] z-0"
              style={{
                backgroundImage: `url("data:image/svg+xml,%3Csvg width='12' height='12' viewBox='0 0 12 12' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='2' cy='2' r='1' fill='%234338ca'/%3E%3C/svg%3E")`,
              }}
            />

            <div className="relative z-10">
              {/* Header */}
              <div className="bg-gradient-to-r from-indigo-600 via-indigo-600 to-violet-600 px-4 py-3 flex items-center justify-between shadow-md">
                <div className="flex items-center gap-2.5">
                  <div
                    className="w-9 h-9 rounded-full overflow-hidden bg-indigo-200 flex-shrink-0 ring-2 ring-white/40 shadow-lg"
                    style={{ animation: emotionalState === "speaking" ? "sophia-breathe 0.8s ease-in-out infinite" : undefined }}
                  >
                    <AvatarSVG emotionalState={emotionalState} blinkPhase={blinkPhase} />
                  </div>
                  <div>
                    <p className="text-white font-semibold text-sm leading-tight tracking-wide">Sophia</p>
                    <div className="flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse shadow-[0_0_4px_rgba(52,211,153,0.8)]" />
                      <p className="text-indigo-200 text-[10px] font-medium">Expert · Intelligence Stratégique</p>
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => setOpen(false)}
                  className="text-white/60 hover:text-white transition-colors p-1.5 rounded-lg hover:bg-white/10 active:scale-90"
                >
                  <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
                    <path d="M12 4L4 12M4 4l8 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                  </svg>
                </button>
              </div>

              {/* Status bar */}
              <div className="bg-indigo-50/80 border-b border-indigo-100/60 px-4 py-1.5 flex items-center gap-2">
                <div className="flex gap-0.5">
                  {[0, 1, 2].map(i => (
                    <span
                      key={i}
                      className="w-1 h-2.5 rounded-full bg-indigo-400"
                      style={{ animation: `sophia-breathe ${0.8 + i * 0.2}s ease-in-out infinite`, animationDelay: `${i * 0.15}s` }}
                    />
                  ))}
                </div>
                <p className="text-indigo-600 text-[9px] font-semibold tracking-wider uppercase">
                  Sophia analyse votre tableau de bord en temps réel…
                </p>
              </div>

              {/* Body */}
              <div className="p-4 space-y-3">
                {/* Message bubble */}
                <div className="flex items-start gap-2.5">
                  <MiniAvatar />
                  <div className="flex-1">
                    <div
                      className="bg-white rounded-2xl rounded-tl-none px-3.5 py-2.5 border border-slate-100 shadow-sm"
                      style={{
                        animation: emotionalState === "thinking" ? "sophia-breathe 1.2s ease-in-out infinite" : undefined,
                      }}
                    >
                      {emotionalState === "thinking" && !displayedText ? (
                        <div className="flex items-center gap-1.5 py-1">
                          {[0, 1, 2].map(i => (
                            <span
                              key={i}
                              className="w-2 h-2 rounded-full bg-indigo-300"
                              style={{ animation: `sophia-breathe 1s ease-in-out infinite`, animationDelay: `${i * 0.2}s` }}
                            />
                          ))}
                        </div>
                      ) : (
                        <p className="text-slate-700 text-sm leading-relaxed">
                          {displayedText}
                          {typing && (
                            <span className="inline-block w-0.5 h-3.5 bg-indigo-400 ml-0.5 rounded-sm" style={{ animation: "sophia-breathe 0.8s ease-in-out infinite" }} />
                          )}
                        </p>
                      )}
                    </div>

                    {/* Emoji reactions */}
                    {!typing && displayedText && (
                      <div className="flex items-center gap-1.5 mt-1.5 ml-1">
                        {(["👍", "💡", "📊"] as const).map((emoji) => (
                          <button
                            key={emoji}
                            onClick={() => handleReaction(emoji)}
                            className={`text-sm px-2 py-0.5 rounded-full border transition-all hover:scale-110 active:scale-95 ${
                              messageReactions.main === emoji
                                ? "bg-indigo-100 border-indigo-300 shadow-sm"
                                : "bg-white/60 border-slate-200 hover:bg-slate-50"
                            }`}
                          >
                            {emoji}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                {/* Insight card */}
                {!typing && tip.insight && (
                  <div
                    className="ml-9 bg-gradient-to-br from-indigo-50 to-violet-50 border border-indigo-100 rounded-xl p-3"
                    style={{ animation: "sophia-slide-in 0.5s 0.3s cubic-bezier(0.16,1,0.3,1) both" }}
                  >
                    <div className="flex items-start gap-2">
                      <div className="w-5 h-5 rounded-full bg-indigo-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                        <svg className="w-3 h-3 text-indigo-500" viewBox="0 0 14 14" fill="currentColor">
                          <path d="M7 1a6 6 0 100 12A6 6 0 007 1zm0 9a.75.75 0 110-1.5A.75.75 0 017 10zm.75-3.25a.75.75 0 01-1.5 0V5a.75.75 0 011.5 0v1.75z" />
                        </svg>
                      </div>
                      <div className="flex-1">
                        <p className="text-indigo-700 text-xs leading-relaxed">{tip.insight}</p>
                        {/* Confidence indicator */}
                        <div className="flex items-center gap-1.5 mt-1.5">
                          <div className="flex gap-0.5">
                            {[...Array(5)].map((_, i) => (
                              <span key={i} className={`w-1.5 h-1.5 rounded-full ${i < 4 ? "bg-indigo-400" : "bg-indigo-200"}`} />
                            ))}
                          </div>
                          <span className="text-indigo-400 text-[9px] font-medium">Analyse basée sur 847 signaux</span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Quick actions */}
                {!typing && (
                  <div
                    className="ml-9 flex flex-wrap gap-2"
                    style={{ animation: "sophia-slide-in 0.4s 0.5s cubic-bezier(0.16,1,0.3,1) both" }}
                  >
                    {["Analyser maintenant", "Générer un rapport"].map((action) => (
                      <button
                        key={action}
                        className="text-xs font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 border border-indigo-100 px-3 py-1.5 rounded-full transition-all hover:scale-105 active:scale-95 hover:shadow-sm"
                      >
                        {action}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Input */}
              <div className="px-4 pb-4">
                <div className="flex items-center gap-2 bg-white border border-slate-200 rounded-xl px-3 py-2.5 focus-within:border-indigo-300 focus-within:shadow-[0_0_0_3px_rgba(99,102,241,0.1)] transition-all shadow-sm">
                  <input
                    type="text"
                    placeholder="Posez une question à Sophia…"
                    className="flex-1 bg-transparent text-sm text-slate-700 placeholder-slate-400 outline-none"
                  />
                  <button className="w-6 h-6 flex items-center justify-center rounded-lg bg-indigo-600 hover:bg-indigo-700 transition-colors flex-shrink-0 hover:scale-110 active:scale-90 shadow-sm">
                    <svg className="w-3.5 h-3.5 text-white" viewBox="0 0 14 14" fill="none">
                      <path d="M2 7h10M7.5 3L12 7l-4.5 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Greeting bubble */}
        {showGreeting && !open && (
          <div
            className="absolute bottom-16 right-16 mb-1 pointer-events-none"
            style={{
              animation: greetingVisible
                ? "sophia-slide-in 0.4s cubic-bezier(0.16,1,0.3,1) forwards"
                : "sophia-fade-out 0.8s ease forwards",
            }}
          >
            <div className="bg-slate-900 text-white text-sm font-medium px-4 py-2.5 rounded-2xl shadow-xl whitespace-nowrap max-w-[200px]">
              <span>Bonjour, je suis Sophia&nbsp;</span>
              <span role="img" aria-label="wave">👋</span>
              {/* Arrow pointing right toward the avatar */}
              <div
                className="absolute right-[-6px] top-1/2 -translate-y-1/2 w-0 h-0"
                style={{
                  borderTop: "5px solid transparent",
                  borderBottom: "5px solid transparent",
                  borderLeft: "6px solid #0f172a",
                }}
              />
            </div>
          </div>
        )}

        {/* Floating avatar button */}
        <div className="relative">
          {/* Notification pulse ring */}
          {pulse && !open && (
            <span className="absolute inset-0 rounded-full animate-ping bg-indigo-400 opacity-25" />
          )}

          {/* New message badge */}
          {!open && (
            <span className="absolute -top-1 -right-1 w-4 h-4 bg-indigo-500 rounded-full border-2 border-white flex items-center justify-center z-10 shadow-sm">
              <span className="text-white text-[8px] font-black">1</span>
            </span>
          )}

          <button
            onClick={() => setOpen((v) => !v)}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            className="w-14 h-14 rounded-full shadow-xl hover:shadow-2xl transition-all active:scale-95 overflow-hidden ring-2 ring-white ring-offset-2 ring-offset-slate-50"
            style={{
              animation: !open ? "sophia-floating 6s ease-in-out infinite" : undefined,
              transform: isHovered ? "scale(1.08)" : undefined,
              transition: "transform 0.25s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.25s ease",
            }}
            title="Sophia — Expert en Intelligence Stratégique"
          >
            <AvatarSVG
              emotionalState={emotionalState}
              isHovered={isHovered}
              blinkPhase={blinkPhase}
              nodPhase={nodPhase}
            />
          </button>
        </div>
      </div>
    </>
  );
}
