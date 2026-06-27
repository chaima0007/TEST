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
    d: "Vous êtes en danger maintenant, ou quelqu'un l'est. C'est gratuit, et joignable 24h/24.",
    numeros: [
      { label: "Urgence européenne (tous secours)", tel: "112", note: "24h/24, partout en UE" },
      { label: "Police / Gendarmerie", tel: "17", note: "24h/24" },
      { label: "SAMU (urgence médicale)", tel: "15", note: "24h/24" },
      { label: "Pompiers", tel: "18", note: "24h/24" },
      { label: "Urgence par SMS (sourds/malentendants)", tel: "114", note: "envoyez un SMS gratuit au 114" },
    ],
  },
  {
    emoji: "💜",
    t: "Violences conjugales ou sexistes",
    d: "Pour toute personne victime ou témoin de violences. Écoute anonyme et gratuite. En danger immédiat : 17 ou 112.",
    numeros: [
      { label: "Violences Femmes Info", tel: "3919", note: "anonyme et gratuit, 7j/7" },
    ],
    lien: { label: "arretonslesviolences.gouv.fr (officiel, tchat 24h/24)", url: "https://arretonslesviolences.gouv.fr/" },
  },
  {
    emoji: "🧒",
    t: "Enfant en danger",
    d: "Pour un enfant victime ou témoin de violences, de maltraitance ou de négligence.",
    numeros: [
      { label: "Allô Enfance en Danger", tel: "119", note: "24h/24, 7j/7, gratuit" },
    ],
  },
  {
    emoji: "📱",
    t: "Cyberharcèlement, violences numériques",
    d: "Harcèlement en ligne, photos intimes diffusées, rumeurs : vous n'êtes pas seul·e.",
    numeros: [
      { label: "Net Écoute / 3018", tel: "3018", note: "gratuit, anonyme, confidentiel" },
    ],
    lien: { label: "e-enfance.org / 3018 (officiel)", url: "https://e-enfance.org/" },
  },
  {
    emoji: "🫂",
    t: "Mal-être, pensées suicidaires",
    d: "Si tout est lourd, si vous avez des idées noires, des professionnels écoutent, sans juger, à toute heure.",
    numeros: [
      { label: "Numéro national de prévention du suicide", tel: "3114", note: "24h/24, 7j/7, gratuit" },
    ],
  },
];

const readText = `En danger, en France : où aller. Pour toute personne. ${aides
  .map((a) => a.t + ". " + a.d + " Numéros : " + a.numeros.map((n) => n.label + " " + n.tel).join(", ") + ".")
  .join(" ")} Tous ces numéros sont gratuits, anonymes et confidentiels. En cas de danger immédiat, appelez toujours le 112 ou le 17.`;

export default function EnDangerFrancePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/la-loi-avec-moi-france" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">L</span>
            </div>
            <span className="font-bold text-lg tracking-tight">La loi avec moi <span className="text-blue-700">· France</span></span>
          </Link>
          <Link href="/la-loi-avec-moi-france" className="text-sm font-semibold text-blue-700 hover:text-blue-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(244,63,94,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            En danger ? Où aller · France
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Vous n&apos;êtes pas seul·e</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Pour <strong className="text-white">toute personne</strong> en danger en France. Des aides gratuites,
            anonymes et confidentielles. Touchez un numéro pour appeler directement.
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
                  <a href={a.lien.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-xs font-medium text-blue-700 mt-3 bg-blue-50 border border-blue-200 hover:bg-blue-100 rounded-lg px-3 py-2 transition-colors">
                    🔗 {a.lien.label}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
                  </a>
                )}
              </div>
            </div>
          </div>
        ))}
      </section>

      <section className="pb-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Ces numéros sont <strong>gratuits, anonymes et pour tout le monde</strong>. Numéros vérifiés auprès de
            sources officielles françaises (service-public.fr, ministère de l&apos;Intérieur). En cas de danger
            immédiat, appelez toujours le <strong>112</strong> ou le <strong>17</strong>.
          </p>
        </div>
        <div className="mt-5 flex flex-col gap-2.5">
          <a href="https://www.service-public.gouv.fr/particuliers/vosdroits/F33954" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-blue-50 border border-blue-200 hover:bg-blue-100 rounded-lg px-4 py-2.5 transition-colors">
            🔗 service-public.fr — numéros d&apos;urgence (officiel)
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </a>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/la-loi-avec-moi-france" className="hover:text-slate-900">← Retour à « La loi avec moi · France »</Link>
      </footer>
    </main>
  );
}
