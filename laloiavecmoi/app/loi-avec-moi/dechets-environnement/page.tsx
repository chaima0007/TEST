"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

type Amende = {
  lieu: string;
  quoi: string;
  montant: string;
  note?: string;
};

const amendes: Amende[] = [
  {
    lieu: "Wallonie",
    quoi: "Mégot, canette, chewing-gum jetés par terre",
    montant: "200 €",
    note: "le montant a été doublé (avant : 100 €)",
  },
  {
    lieu: "Wallonie",
    quoi: "Emballages, bouteilles, sac-poubelle abandonnés",
    montant: "300 €",
    note: "avant : 150 €",
  },
  {
    lieu: "Bruxelles",
    quoi: "Mégot, canette, déchet selon le volume",
    montant: "75 à 350 €",
    note: "+ environ 100 € de frais de procédure",
  },
  {
    lieu: "Flandre",
    quoi: "Un simple mégot par terre (ex. Louvain)",
    montant: "jusqu'à 500 €",
  },
];

type Vie = {
  emoji: string;
  objet: string;
  duree: string;
};

const dureesVie: Vie[] = [
  { emoji: "🚬", objet: "Un mégot de cigarette", duree: "jusqu'à ~10–12 ans" },
  { emoji: "🍬", objet: "Un chewing-gum", duree: "~5 ans" },
  { emoji: "🥫", objet: "Une canette en aluminium", duree: "~200 ans" },
  { emoji: "🧴", objet: "Une bouteille en plastique", duree: "~450 ans" },
  { emoji: "🛍️", objet: "Un sac en plastique", duree: "plusieurs centaines d'années" },
  { emoji: "🍾", objet: "Une bouteille en verre", duree: "des milliers d'années" },
];

const readText = `Jeter un déchet par terre, ce n'est jamais « juste un petit papier ». Un seul mégot de cigarette peut contaminer jusqu'à cinq cents litres d'eau, et un mégot dans un litre d'eau peut suffire à tuer des poissons. Chaque année, la Wallonie ramasse environ dix-huit mille tonnes de déchets sauvages. En mer, les animaux — oiseaux, tortues, poissons — avalent le plastique et les mégots, et en meurent. Ce que vous risquez : en Wallonie, deux cents euros pour un mégot ou une canette, trois cents euros pour un emballage. À Bruxelles, de soixante-quinze à trois cent cinquante euros. En Flandre, jusqu'à cinq cents euros. Un mégot met jusqu'à douze ans à disparaître, une canette deux cents ans, une bouteille en plastique quatre cent cinquante ans. Le geste prend deux secondes. La nature, elle, met des siècles à réparer.`;

export default function DechetsEnvironnementPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi</span>
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-teal-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(20,184,166,0.26),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Déchets & environnement
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">« Ce n&apos;est qu&apos;un petit papier »</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Le geste prend deux secondes. Mais ce petit papier, ce mégot, cette canette vont rester là
            <strong className="text-white"> des années, parfois des siècles</strong> — et faire du mal au vivant.
            Voici la vérité, et ce que vous risquez.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Le cœur : impact émotionnel chiffré */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight text-center">Un seul geste, des dégâts immenses</h2>
        <div className="mt-8 grid sm:grid-cols-3 gap-4">
          <div className="rounded-2xl border border-teal-200 bg-teal-50 p-6 text-center">
            <div className="text-4xl font-black text-teal-700">500 L</div>
            <p className="text-sm text-slate-700 mt-2 leading-relaxed">
              d&apos;eau qu&apos;<strong>un seul mégot</strong> peut contaminer. Un mégot dans un litre d&apos;eau peut suffire à tuer des poissons.
            </p>
          </div>
          <div className="rounded-2xl border border-teal-200 bg-teal-50 p-6 text-center">
            <div className="text-4xl font-black text-teal-700">18 000 t</div>
            <p className="text-sm text-slate-700 mt-2 leading-relaxed">
              de déchets sauvages ramassés <strong>chaque année en Wallonie</strong> (étude 2018). Payés par tous.
            </p>
          </div>
          <div className="rounded-2xl border border-teal-200 bg-teal-50 p-6 text-center">
            <div className="text-4xl font-black text-teal-700">🐢</div>
            <p className="text-sm text-slate-700 mt-2 leading-relaxed">
              En mer, oiseaux, tortues et poissons <strong>avalent le plastique et les mégots</strong> — et en meurent, étouffés ou empoisonnés.
            </p>
          </div>
        </div>
      </section>

      {/* Combien de temps ça reste */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Combien de temps votre déchet va rester là</h2>
          <p className="text-slate-600 mt-2 text-sm leading-relaxed">
            Un déchet jeté aujourd&apos;hui sera peut-être encore là quand vos petits-enfants seront grands.
            Estimations couramment admises (le plastique ne disparaît pas vraiment : il se fragmente en microplastiques).
          </p>
          <div className="mt-6 space-y-2.5">
            {dureesVie.map((v) => (
              <div key={v.objet} className="flex items-center gap-4 bg-white rounded-xl border border-slate-200 px-5 py-3.5">
                <span className="text-2xl flex-shrink-0" aria-hidden>{v.emoji}</span>
                <span className="flex-1 font-semibold text-slate-800 text-sm">{v.objet}</span>
                <span className="text-sm font-bold text-teal-700 whitespace-nowrap">{v.duree}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Ce que tu risques */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">⚖️ Ce que vous risquez (et c&apos;est cher)</h2>
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">
          Jeter un déchet dans la rue, en forêt ou à la mer est une infraction sanctionnée partout en Belgique.
          Les montants ont été augmentés ces dernières années.
        </p>
        <div className="mt-6 space-y-3">
          {amendes.map((a, i) => (
            <div key={i} className="flex items-start gap-4 rounded-2xl border border-rose-200 bg-rose-50 p-5">
              <span className="flex-shrink-0 text-xs font-bold text-rose-700 bg-white border border-rose-200 rounded-full px-3 py-1 mt-0.5">{a.lieu}</span>
              <div className="flex-1">
                <p className="text-sm font-semibold text-slate-900">{a.quoi}</p>
                {a.note && <p className="text-xs text-slate-500 mt-0.5">{a.note}</p>}
              </div>
              <span className="text-lg font-black text-rose-700 whitespace-nowrap">{a.montant}</span>
            </div>
          ))}
        </div>
        <p className="text-xs text-slate-400 mt-4 leading-relaxed">
          Les « dépôts clandestins » (sacs entiers, encombrants abandonnés) sont punis encore plus lourdement et
          peuvent mener à des poursuites pénales.
        </p>
      </section>

      {/* Le bon geste */}
      <section className="pb-8 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-emerald-200 bg-emerald-50 p-6 text-center">
          <h2 className="text-xl font-bold tracking-tight text-emerald-900">💚 Le bon réflexe est simple</h2>
          <p className="text-emerald-900/80 text-sm mt-2 leading-relaxed max-w-xl mx-auto">
            Gardez votre déchet jusqu&apos;à une poubelle, un cendrier de poche pour les mégots, et triez chez vous.
            Deux secondes d&apos;attention, et la nature — et les animaux — vous disent merci pour des siècles.
          </p>
        </div>
      </section>

      {/* Sources */}
      <section className="pb-12 px-6 max-w-3xl mx-auto">
        <h2 className="text-lg font-bold tracking-tight">Sources officielles</h2>
        <div className="mt-4 flex flex-col gap-2.5">
          <a href="https://www.bewapp.be/" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
            🔗 Be WaPP — la Wallonie plus propre (officiel)
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </a>
          <a href="https://www.arp-gan.be/fr/amendes" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
            🔗 Bruxelles-Propreté — les amendes (officiel)
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </a>
        </div>
        <div className="mt-6 rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Les montants des amendes varient selon la Région et la commune et sont régulièrement revus à la hausse.
            Les durées de décomposition sont des estimations couramment admises par les organismes environnementaux.
            Pour le montant exact dans votre commune, consultez son règlement (sanctions administratives — GAS).
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La Loi Avec Moi »</Link>
      </footer>
    </main>
  );
}
