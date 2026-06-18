"use client";

import { useState, useEffect } from "react";
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

function AvatarSVG() {
  return (
    <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full">
      {/* Background circle */}
      <circle cx="40" cy="40" r="40" fill="url(#bgGrad)" />

      {/* Body / shoulders */}
      <path
        d="M12 75 C12 58 22 50 40 50 C58 50 68 58 68 75"
        fill="url(#bodyGrad)"
      />

      {/* Jacket lapels */}
      <path d="M34 50 L30 68 L40 62 L50 68 L46 50" fill="url(#jacketGrad)" opacity="0.9" />
      <path d="M40 62 L38 75 M40 62 L42 75" stroke="white" strokeWidth="0.5" opacity="0.3" />

      {/* Neck */}
      <path d="M35 46 Q40 50 45 46 L44 52 Q40 54 36 52Z" fill="#FDBCB4" />

      {/* Head */}
      <ellipse cx="40" cy="32" rx="14" ry="16" fill="#FDBCB4" />

      {/* Hair */}
      <path
        d="M26 28 C26 18 30 14 40 14 C50 14 54 18 54 28 C54 24 51 18 40 18 C29 18 26 24 26 28Z"
        fill="url(#hairGrad)"
      />
      <ellipse cx="40" cy="17" rx="11" ry="5" fill="url(#hairGrad)" />
      {/* Side hair */}
      <path d="M26 28 C25 24 25 30 27 34" stroke="#2d1b69" strokeWidth="2.5" strokeLinecap="round" fill="none" />
      <path d="M54 28 C55 24 55 30 53 34" stroke="#2d1b69" strokeWidth="2.5" strokeLinecap="round" fill="none" />

      {/* Ears */}
      <ellipse cx="26.5" cy="33" rx="2.5" ry="3" fill="#FDBCB4" />
      <ellipse cx="53.5" cy="33" rx="2.5" ry="3" fill="#FDBCB4" />

      {/* Eyes */}
      {/* Eye whites */}
      <ellipse cx="35" cy="31" rx="4" ry="3.5" fill="white" />
      <ellipse cx="45" cy="31" rx="4" ry="3.5" fill="white" />
      {/* Iris */}
      <circle cx="35.5" cy="31.5" r="2.2" fill="#4338CA" />
      <circle cx="45.5" cy="31.5" r="2.2" fill="#4338CA" />
      {/* Pupil */}
      <circle cx="35.8" cy="31.5" r="1.1" fill="#1e1b4b" />
      <circle cx="45.8" cy="31.5" r="1.1" fill="#1e1b4b" />
      {/* Eye shine */}
      <circle cx="36.3" cy="30.8" r="0.5" fill="white" />
      <circle cx="46.3" cy="30.8" r="0.5" fill="white" />
      {/* Eyebrows */}
      <path d="M31.5 27 Q35 25.5 38.5 27" stroke="#2d1b69" strokeWidth="1.3" strokeLinecap="round" fill="none" />
      <path d="M41.5 27 Q45 25.5 48.5 27" stroke="#2d1b69" strokeWidth="1.3" strokeLinecap="round" fill="none" />

      {/* Nose */}
      <path d="M39 34 Q40 37 41 34" stroke="#e8a090" strokeWidth="1" strokeLinecap="round" fill="none" />
      <circle cx="38.2" cy="36.2" r="1" fill="#e8a090" opacity="0.5" />
      <circle cx="41.8" cy="36.2" r="1" fill="#e8a090" opacity="0.5" />

      {/* Smile */}
      <path d="M35.5 40 Q40 44 44.5 40" stroke="#d4756b" strokeWidth="1.3" strokeLinecap="round" fill="none" />
      {/* Subtle cheeks */}
      <circle cx="31" cy="38" r="3.5" fill="#FFB3A7" opacity="0.25" />
      <circle cx="49" cy="38" r="3.5" fill="#FFB3A7" opacity="0.25" />

      {/* Shirt collar */}
      <path d="M35 52 L37 56 L40 54 L43 56 L45 52" fill="white" opacity="0.9" />

      {/* Tie / badge hint */}
      <path d="M39 56 L40 64 L41 56" fill="url(#tieGrad)" opacity="0.8" />

      <defs>
        <radialGradient id="bgGrad" cx="40%" cy="35%" r="60%">
          <stop offset="0%" stopColor="#e0e7ff" />
          <stop offset="100%" stopColor="#c7d2fe" />
        </radialGradient>
        <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#4338CA" />
          <stop offset="100%" stopColor="#3730a3" />
        </linearGradient>
        <linearGradient id="jacketGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#4f46e5" />
          <stop offset="100%" stopColor="#3730a3" />
        </linearGradient>
        <linearGradient id="hairGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#3d2b8e" />
          <stop offset="100%" stopColor="#2d1b69" />
        </linearGradient>
        <linearGradient id="tieGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#6366f1" />
          <stop offset="100%" stopColor="#4338ca" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export default function ExpertAssistant() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [visible, setVisible] = useState(false);
  const [typing, setTyping] = useState(false);
  const [displayedText, setDisplayedText] = useState("");
  const [pulse, setPulse] = useState(false);

  const tip = TIPS[pathname] ?? DEFAULT_TIP;

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 1200);
    return () => clearTimeout(t);
  }, []);

  useEffect(() => {
    const t = setTimeout(() => setPulse(true), 3000);
    const t2 = setTimeout(() => setPulse(false), 5000);
    return () => { clearTimeout(t); clearTimeout(t2); };
  }, [pathname]);

  useEffect(() => {
    if (!open) { setDisplayedText(""); return; }
    setTyping(true);
    setDisplayedText("");
    let i = 0;
    const msg = tip.message;
    const interval = setInterval(() => {
      if (i < msg.length) {
        setDisplayedText(msg.slice(0, i + 1));
        i++;
      } else {
        setTyping(false);
        clearInterval(interval);
      }
    }, 18);
    return () => clearInterval(interval);
  }, [open, tip.message]);

  if (!visible) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">

      {/* Chat panel */}
      {open && (
        <div className="w-80 bg-white rounded-2xl shadow-2xl border border-slate-100 overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-300">
          {/* Header */}
          <div className="bg-gradient-to-r from-indigo-600 to-violet-600 px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-full overflow-hidden bg-indigo-200 flex-shrink-0 ring-2 ring-white/30">
                <AvatarSVG />
              </div>
              <div>
                <p className="text-white font-semibold text-sm leading-tight">Sophia</p>
                <div className="flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  <p className="text-indigo-200 text-[10px] font-medium">Expert · Intelligence Stratégique</p>
                </div>
              </div>
            </div>
            <button
              onClick={() => setOpen(false)}
              className="text-white/60 hover:text-white transition-colors p-1 rounded-lg hover:bg-white/10"
            >
              <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
                <path d="M12 4L4 12M4 4l8 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
              </svg>
            </button>
          </div>

          {/* Body */}
          <div className="p-4 space-y-3">
            {/* Message bubble */}
            <div className="flex items-start gap-2.5">
              <div className="w-7 h-7 rounded-full overflow-hidden flex-shrink-0 mt-0.5 ring-1 ring-indigo-100">
                <AvatarSVG />
              </div>
              <div className="flex-1 bg-slate-50 rounded-2xl rounded-tl-none px-3.5 py-2.5 border border-slate-100">
                <p className="text-slate-700 text-sm leading-relaxed">
                  {displayedText}
                  {typing && <span className="inline-block w-1 h-3.5 bg-indigo-400 ml-0.5 animate-pulse rounded-sm" />}
                </p>
              </div>
            </div>

            {/* Insight card */}
            {!typing && tip.insight && (
              <div className="ml-9 bg-indigo-50 border border-indigo-100 rounded-xl p-3 animate-in fade-in duration-500 delay-300">
                <div className="flex items-start gap-2">
                  <svg className="w-3.5 h-3.5 text-indigo-500 flex-shrink-0 mt-0.5" viewBox="0 0 14 14" fill="currentColor">
                    <path d="M7 1a6 6 0 100 12A6 6 0 007 1zm0 9a.75.75 0 110-1.5A.75.75 0 017 10zm.75-3.25a.75.75 0 01-1.5 0V5a.75.75 0 011.5 0v1.75z" />
                  </svg>
                  <p className="text-indigo-700 text-xs leading-relaxed">{tip.insight}</p>
                </div>
              </div>
            )}

            {/* Quick actions */}
            {!typing && (
              <div className="ml-9 flex flex-wrap gap-2 animate-in fade-in duration-500">
                {["Analyser maintenant", "Générer un rapport"].map((action) => (
                  <button
                    key={action}
                    className="text-xs font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 border border-indigo-100 px-3 py-1.5 rounded-full transition-colors"
                  >
                    {action}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Input */}
          <div className="px-4 pb-4">
            <div className="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 focus-within:border-indigo-300 transition-colors">
              <input
                type="text"
                placeholder="Posez une question à Sophia…"
                className="flex-1 bg-transparent text-sm text-slate-700 placeholder-slate-400 outline-none"
              />
              <button className="w-6 h-6 flex items-center justify-center rounded-lg bg-indigo-600 hover:bg-indigo-700 transition-colors flex-shrink-0">
                <svg className="w-3.5 h-3.5 text-white" viewBox="0 0 14 14" fill="none">
                  <path d="M2 7h10M7.5 3L12 7l-4.5 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Floating avatar button */}
      <div className="relative">
        {/* Notification pulse ring */}
        {pulse && !open && (
          <span className="absolute inset-0 rounded-full animate-ping bg-indigo-400 opacity-30" />
        )}

        {/* New message badge */}
        {!open && (
          <span className="absolute -top-1 -right-1 w-4 h-4 bg-indigo-500 rounded-full border-2 border-white flex items-center justify-center z-10">
            <span className="text-white text-[8px] font-black">1</span>
          </span>
        )}

        <button
          onClick={() => setOpen((v) => !v)}
          className="w-14 h-14 rounded-full shadow-xl hover:shadow-2xl transition-all hover:scale-105 active:scale-95 overflow-hidden ring-2 ring-white ring-offset-2 ring-offset-slate-50"
          title="Sophia — Expert en Intelligence Stratégique"
        >
          <AvatarSVG />
        </button>
      </div>

      {/* Tooltip bubble (quand fermé) */}
      {!open && visible && (
        <div className="absolute bottom-16 right-0 mb-1 pointer-events-none">
          <div className="bg-slate-900 text-white text-xs font-medium px-3 py-1.5 rounded-xl shadow-lg whitespace-nowrap opacity-0 group-hover:opacity-100">
            Sophia · Expert IA
            <div className="absolute bottom-0 right-4 translate-y-full w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-slate-900" />
          </div>
        </div>
      )}
    </div>
  );
}
