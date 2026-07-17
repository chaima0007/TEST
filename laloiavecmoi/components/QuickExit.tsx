"use client";

// Bouton « Quitter vite » — standard des sites d'aide (violences, harcèlement).
// Un enfant ou une victime surpris·e en train de chercher de l'aide peut quitter
// la page immédiatement : remplacement de l'historique (bouton retour ne revient
// pas ici) et redirection vers un site neutre.

export default function QuickExit() {
  return (
    <button
      onClick={() => {
        window.location.replace("https://www.google.be");
      }}
      aria-label="Quitter cette page rapidement"
      className="fixed bottom-4 right-4 z-50 rounded-full bg-slate-900 text-white text-sm font-semibold px-4 py-2.5 shadow-lg hover:bg-slate-700 transition-colors"
    >
      🚪 Quitter vite
    </button>
  );
}
