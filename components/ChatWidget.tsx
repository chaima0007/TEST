"use client";

import { useState } from "react";

// Assistant FAQ 24/7 — répond aux questions courantes sans IA externe (fiable,
// gratuit, sans hallucination). Pour les demandes précises, oriente vers /contact.

interface Msg { from: "bot" | "user"; text: string }

// Base de connaissances : mots-clés → réponse
const KB: { keys: string[]; answer: string }[] = [
  { keys: ["prix", "tarif", "coût", "cout", "combien", "budget"],
    answer: "Nos tarifs de départ : Site web dès 500 €, Tableau de bord dès 800 €, Automatisation dès 300 €, Business plan dès 400 €. Le devis final est gratuit et personnalisé selon votre besoin. Voir la page Tarifs pour le détail." },
  { keys: ["délai", "delai", "temps", "rapide", "quand", "combien de temps", "express"],
    answer: "La plupart des sites sont livrés en quelques jours. On propose même un site express en 48h pour les projets simples, et un devis en 1h. Les projets plus complexes prennent 1 à 2 semaines." },
  { keys: ["service", "faites", "proposez", "quoi", "offre"],
    answer: "On crée 4 choses sur-mesure : 🌐 Sites web, 📊 Tableaux de bord, 🤖 Automatisations, et 📈 Business plans. Tout est conçu spécifiquement pour votre activité." },
  { keys: ["audit", "gratuit", "essai", "test"],
    answer: "Oui ! On offre un audit express GRATUIT en 24h de votre site ou de votre besoin, sans engagement. Laissez vos coordonnées sur la page Contact pour en profiter." },
  { keys: ["contact", "joindre", "rendez-vous", "rdv", "parler", "appel"],
    answer: "Avec plaisir ! Remplissez le formulaire sur la page Contact — on vous recontacte sous 24h pour discuter de votre projet, sans engagement." },
  { keys: ["site web", "site internet", "vitrine"],
    answer: "On crée des sites web modernes, rapides et responsives, livrés en quelques jours, dès 500 €. Parfait pour donner une image pro à votre activité." },
  { keys: ["dashboard", "tableau de bord", "données", "donnees", "statistique"],
    answer: "On construit des tableaux de bord sur-mesure pour suivre votre activité (ventes, clients, performance) en temps réel, dès 800 €." },
  { keys: ["automatis", "automatique", "tâche", "tache", "gagner du temps"],
    answer: "On automatise vos tâches répétitives (toujours de façon supervisée et fiable), dès 300 €. Vous gagnez du temps, avec moins d'erreurs." },
  { keys: ["business plan", "plan d'affaire", "stratégie", "strategie", "lever des fonds"],
    answer: "On rédige des business plans pro (analyse marché, chiffrage, stratégie, présentation prête à pitcher), dès 400 €." },
  { keys: ["confiance", "fiable", "garantie", "sérieux", "serieux", "qualité", "qualite"],
    answer: "Notre force : chaque livrable passe par plusieurs contrôles qualité automatiques avant de vous être remis. Devis transparent, prix annoncé = prix facturé, et on ajuste jusqu'à votre satisfaction." },
];

const FALLBACK = "Bonne question ! Pour une réponse précise sur votre projet, le mieux est de laisser un message sur la page Contact — on vous répond sous 24h. 😊";
const GREETING = "Bonjour 👋 Je suis l'assistant de Caelum. Posez-moi une question sur nos services, nos tarifs ou nos délais !";

function findAnswer(q: string): string {
  const low = q.toLowerCase();
  let best: { score: number; answer: string } | null = null;
  for (const item of KB) {
    const score = item.keys.filter((k) => low.includes(k)).length;
    if (score > 0 && (!best || score > best.score)) best = { score, answer: item.answer };
  }
  return best ? best.answer : FALLBACK;
}

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [msgs, setMsgs] = useState<Msg[]>([{ from: "bot", text: GREETING }]);

  function send() {
    const q = input.trim();
    if (!q) return;
    const answer = findAnswer(q);
    setMsgs((m) => [...m, { from: "user", text: q }, { from: "bot", text: answer }]);
    setInput("");
  }

  return (
    <>
      {/* Bouton flottant */}
      {!open && (
        <button onClick={() => setOpen(true)}
          className="fixed bottom-5 right-5 z-50 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg shadow-blue-600/30 w-14 h-14 flex items-center justify-center transition-transform hover:scale-105"
          aria-label="Ouvrir l'assistant">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-6 h-6">
            <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </button>
      )}

      {/* Fenêtre de chat */}
      {open && (
        <div className="fixed bottom-5 right-5 z-50 w-[92vw] max-w-sm bg-white rounded-2xl shadow-2xl border border-slate-200 flex flex-col overflow-hidden" style={{ height: "70vh", maxHeight: 540 }}>
          <div className="bg-gradient-to-r from-blue-600 to-violet-600 text-white px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-300" />
              <span className="font-semibold text-sm">Assistant Caelum · en ligne 24/7</span>
            </div>
            <button onClick={() => setOpen(false)} aria-label="Fermer" className="text-white/80 hover:text-white text-lg leading-none">✕</button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-slate-50">
            {msgs.map((m, i) => (
              <div key={i} className={`flex ${m.from === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[80%] rounded-2xl px-3.5 py-2 text-sm leading-relaxed ${m.from === "user" ? "bg-blue-600 text-white" : "bg-white border border-slate-200 text-slate-700"}`}>
                  {m.text}
                </div>
              </div>
            ))}
          </div>

          <div className="p-3 border-t border-slate-100 flex gap-2">
            <input value={input} onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") send(); }}
              placeholder="Votre question…"
              className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <button onClick={send} className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 text-sm font-medium">Envoyer</button>
          </div>
        </div>
      )}
    </>
  );
}
