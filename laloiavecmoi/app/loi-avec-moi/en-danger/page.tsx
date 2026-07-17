"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

type Aide = {
  emoji: string;
  t: string;
  d: string;
  numeros: { label: string; tel: string; note?: string }[];
  lien?: { label: string; url: string };
};

const aides: Aide[] = [
  {
    emoji: "🆘",
    t: "Danger immédiat, urgence vitale",
    d: "Vous êtes en danger maintenant, ou quelqu'un l'est. N'hésitez pas, c'est gratuit et joignable 24h/24.",
    numeros: [
      { label: "Urgence (police, pompiers, ambulance)", tel: "112", note: "24h/24" },
      { label: "Police", tel: "101", note: "24h/24" },
    ],
  },
  {
    emoji: "💜",
    t: "Violences conjugales ou familiales",
    d: "Pour toute personne — femme ou homme — victime ou témoin de violences à la maison. Écoute gratuite et confidentielle.",
    numeros: [
      { label: "Écoute Violences Conjugales (FR)", tel: "0800 30 030", note: "8h–20h, 7j/7 · la nuit, renvoi vers le 107" },
      { label: "1712 (Flandre / NL)", tel: "1712" },
    ],
    lien: { label: "ecouteviolencesconjugales.be (tchat + infos)", url: "https://www.ecouteviolencesconjugales.be/" },
  },
  {
    emoji: "🛑",
    t: "Violences sexuelles, viol, agression",
    d: "Écoute spécialisée, anonyme et gratuite. Il existe aussi des Centres de Prise en charge des Violences Sexuelles (CPVS).",
    numeros: [
      { label: "SOS Viol", tel: "0800 98 100" },
    ],
    lien: { label: "Centres de Prise en charge des Violences Sexuelles (officiel)", url: "https://www.violencessexuelles.be/" },
  },
  {
    emoji: "🧒",
    t: "Enfant ou jeune en difficulté",
    d: "Pour un·e jeune qui a peur, qui subit quelque chose, ou qui a juste besoin de parler à quelqu'un.",
    numeros: [
      { label: "Écoute-Enfants", tel: "103", note: "pour les enfants et les jeunes" },
      { label: "Child Focus (enfant disparu / abusé)", tel: "116000", note: "24h/24" },
    ],
  },
  {
    emoji: "🫂",
    t: "Mal-être, détresse, pensées noires",
    d: "Si tout est lourd, si vous avez des idées suicidaires, vous n'êtes pas seul·e. Des personnes écoutent, sans juger, à toute heure.",
    numeros: [
      { label: "Télé-Accueil", tel: "107", note: "écoute anonyme 24h/24" },
      { label: "Centre de Prévention du Suicide", tel: "0800 32 123", note: "24h/24" },
    ],
  },
];

const readText = `En danger : où aller. Pour toute personne, femme ou homme. ${aides
  .map((a) => a.t + ". " + a.d + " Numéros : " + a.numeros.map((n) => n.label + " " + n.tel).join(", ") + ".")
  .join(" ")} Pour un animal en danger, appelez la police 101. Tous ces numéros sont gratuits, anonymes et confidentiels.`;

export default function EnDangerPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi</span>
          </Link>
          <Link href="/loi-avec-moi/mes-droits-maintenant" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Mes droits →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(244,63,94,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            En danger ? Où aller
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Vous n&apos;êtes pas seul·e</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Pour <strong className="text-white">toute personne</strong> en danger — femme ou homme — et pour les animaux.
            Des aides gratuites, anonymes et confidentielles. Touchez un numéro pour appeler directement.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      <section className="py-14 px-6 max-w-3xl mx-auto space-y-5">
        {aides.map((a, i) => (
          <div key={i} className="rounded-2xl border border-slate-200 p-6">
            <div className="flex items-start gap-3">
              <span className="text-3xl flex-shrink-0" aria-hidden>{a.emoji}</span>
              <div className="flex-1">
                <h2 className="text-lg font-bold tracking-tight">{a.t}</h2>
                <p className="text-slate-600 text-sm mt-1.5 leading-relaxed">{a.d}</p>
                <div className="mt-4 flex flex-col gap-2">
                  {a.numeros.map((n) => (
                    <a
                      key={n.tel}
                      href={`tel:${n.tel.replace(/\s/g, "")}`}
                      className="flex items-center justify-between gap-3 rounded-xl bg-rose-50 hover:bg-rose-100 border border-rose-200 px-4 py-3 transition-colors"
                    >
                      <span className="text-left">
                        <span className="block text-sm font-semibold text-slate-900">{n.label}</span>
                        {n.note && <span className="block text-xs text-slate-500">{n.note}</span>}
                      </span>
                      <span className="flex items-center gap-1.5 text-rose-700 font-bold text-sm whitespace-nowrap">📞 {n.tel}</span>
                    </a>
                  ))}
                </div>
                {a.lien && (
                  <a href={a.lien.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-xs font-medium text-indigo-700 mt-3 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-3 py-2 transition-colors">
                    🔗 {a.lien.label}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
                  </a>
                )}
              </div>
            </div>
          </div>
        ))}

        {/* Animaux */}
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-6">
          <div className="flex items-start gap-3">
            <span className="text-3xl flex-shrink-0" aria-hidden>🐾</span>
            <div>
              <h2 className="text-lg font-bold tracking-tight">Un animal en danger</h2>
              <p className="text-slate-600 text-sm mt-1.5 leading-relaxed">
                Animal blessé, maltraité ou abandonné : la maltraitance est une infraction. On vous guide selon la situation.
              </p>
              <Link href="/loi-avec-moi/animaux" className="inline-block mt-3 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-semibold rounded-lg px-4 py-2 transition-colors">
                Voir « Protéger les animaux » →
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="pb-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Ces lignes d&apos;écoute sont <strong>gratuites, anonymes et pour tout le monde</strong> (les hommes
            aussi sont concernés). Numéros vérifiés auprès de sources officielles belges (Centre de Crise National,
            services régionaux). En cas de danger immédiat, appelez toujours le <strong>112</strong>.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La Loi Avec Moi »</Link>
      </footer>
    </main>
  );
}
