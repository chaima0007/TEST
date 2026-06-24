"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

type Canal = {
  emoji: string;
  t: string;
  d: string;
  lien: { label: string; url: string };
  tel?: { label: string; tel: string };
};

const canaux: Canal[] = [
  {
    emoji: "🏛️",
    t: "Le CPAS de votre commune",
    d: "C'est le point d'entrée officiel. Le CPAS (Centre Public d'Action Sociale) peut vous donner une aide alimentaire, des colis, parfois des repas, et vous orienter. Demandez un rendez-vous — c'est un droit, pas une faveur.",
    lien: { label: "Comprendre l'aide du CPAS (SPP Intégration sociale)", url: "https://www.mi-is.be/fr" },
  },
  {
    emoji: "🤝",
    t: "La Croix-Rouge de Belgique",
    d: "Colis alimentaires et épiceries sociales partout dans le pays. Une carte officielle vous montre les points de distribution près de chez vous — avec les adresses, toujours à jour.",
    lien: { label: "Trouver un point d'aide alimentaire (carte officielle)", url: "https://aide-alimentaire.croix-rouge.be/" },
  },
  {
    emoji: "🍲",
    t: "Les Restos du Cœur de Belgique",
    d: "Repas chauds et colis alimentaires, dans de nombreuses villes. Accueil sans jugement.",
    lien: { label: "Les Restos du Cœur — l'aide alimentaire", url: "https://restosducoeur.be/fr/nos-services/l-aide-alimentaire" },
  },
  {
    emoji: "🛒",
    t: "Les épiceries sociales",
    d: "Des magasins solidaires où acheter des produits à prix très réduits, avec dignité. Le CPAS ou la Croix-Rouge vous indiquent la plus proche.",
    lien: { label: "Aide alimentaire & restos sociaux (annuaire)", url: "https://pro.guidesocial.be/Aide-alimentaire" },
  },
];

const readText = `Où aller si vous avez faim, en Belgique. Demander de l'aide alimentaire est un droit, pas une honte. ${canaux
  .map((c) => c.t + ". " + c.d)
  .join(" ")} À Bruxelles, un numéro d'urgence sociale existe : le 0800 35 243. Tout le monde peut traverser une période difficile.`;

export default function AideAlimentairePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi/en-danger" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">En danger →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.2),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Si vous avez faim
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Trouver de l&apos;aide alimentaire</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Demander à manger, c&apos;est un <strong className="text-white">droit, pas une honte</strong>. Tout le monde
            peut traverser une période difficile. Voici où aller, près de chez vous.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      <section className="py-14 px-6 max-w-3xl mx-auto space-y-5">
        {canaux.map((c, i) => (
          <div key={i} className="rounded-2xl border border-slate-200 p-6">
            <div className="flex items-start gap-3">
              <span className="text-3xl flex-shrink-0" aria-hidden>{c.emoji}</span>
              <div>
                <h2 className="text-lg font-bold tracking-tight">{c.t}</h2>
                <p className="text-slate-700 text-sm mt-2 leading-relaxed">{c.d}</p>
                <a href={c.lien.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-xs font-medium text-indigo-700 mt-3 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-3 py-2 transition-colors">
                  🔗 {c.lien.label}
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
                </a>
              </div>
            </div>
          </div>
        ))}

        {/* Urgence sociale Bruxelles */}
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6">
          <h2 className="text-lg font-bold tracking-tight">Urgence sociale à Bruxelles</h2>
          <p className="text-slate-700 text-sm mt-2 leading-relaxed">
            Besoin urgent (manger, dormir) en Région bruxelloise ? Un numéro d&apos;aide sociale d&apos;urgence répond :
          </p>
          <a href="tel:080035243" className="inline-flex items-center gap-2 mt-3 bg-rose-600 hover:bg-rose-700 text-white text-sm font-semibold rounded-lg px-4 py-2 transition-colors">
            📞 Urgence sociale Bruxelles — 0800 35 243
          </a>
        </div>
      </section>

      <section className="pb-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ L&apos;accès à l&apos;aide alimentaire peut demander quelques justificatifs (situation, revenus), mais
            l&apos;<strong>accueil et l&apos;écoute sont pour tout le monde</strong>. Informations tirées de sources
            officielles et associatives belges. Le CPAS de votre commune est le meilleur premier contact.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
