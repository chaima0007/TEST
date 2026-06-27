"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

const cards = [
  {
    id: "arrestation",
    tag: "Police / Arrestation",
    color: "border-indigo-200",
    title: "Si vous êtes arrêté·e ou interrogé·e",
    intro: "Restez calme. La loi vous protège. Voici vos droits, garantis en Belgique :",
    rights: [
      "Vous avez le droit de garder le silence. Vous n'êtes pas obligé·e de répondre, et votre silence ne peut pas être retenu contre vous.",
      "Vous avez le droit à un avocat (droit Salduz) : une concertation confidentielle de 30 minutes avant la première audition, et son assistance pendant les interrogatoires.",
      "Vous avez le droit de prévenir une personne de confiance (famille, proche) de votre arrestation.",
      "Vous avez le droit de voir un médecin si vous êtes blessé·e, malade ou avez besoin de soins.",
      "Une arrestation ne peut durer que 48 heures maximum sans décision d'un juge d'instruction.",
    ],
    numbers: [
      { label: "Aide juridique (avocat gratuit selon revenus)", value: "Bureau d'Aide Juridique — demandez « pro deo »" },
    ],
    safe: "Phrase à retenir et à dire calmement : « Je souhaite garder le silence et parler à mon avocat. »",
  },
  {
    id: "carte-identite",
    tag: "Perte ou vol de carte d'identité",
    color: "border-amber-200",
    title: "Carte d'identité perdue ou volée",
    intro: "Agissez vite pour éviter qu'on utilise vos papiers. Les étapes, dans l'ordre :",
    rights: [
      "Appelez DOC STOP immédiatement : c'est gratuit, 24h/24, partout dans le monde. Votre carte est bloquée tout de suite.",
      "En cas de VOL : portez plainte à la police la plus proche pour obtenir un procès-verbal.",
      "Déclarez la perte ou le vol au service population de votre commune.",
      "La commune vous remet une attestation provisoire (valable un mois) en attendant la nouvelle carte.",
      "Votre carte est signalée sur checkdoc.be : les banques et administrations sauront qu'elle n'est plus valable.",
    ],
    numbers: [
      { label: "DOC STOP (blocage gratuit 24h/24)", value: "00800 2123 2123  ·  +32 2 488 2123" },
      { label: "Card Stop (cartes bancaires)", value: "078 170 170" },
    ],
    safe: "Bon réflexe : bloquez d'abord (DOC STOP), portez plainte ensuite, puis allez à la commune.",
  },
  {
    id: "violence",
    tag: "Si on vous fait du mal",
    color: "border-rose-200",
    title: "Violence, agression, harcèlement",
    intro: "Vous n'êtes pas seul·e, et ce n'est pas votre faute. Mettez-vous d'abord en sécurité :",
    rights: [
      "En cas de danger immédiat, appelez la police (101) ou le numéro d'urgence européen (112).",
      "Vous avez le droit de porter plainte. La police est obligée d'enregistrer votre plainte.",
      "Gardez les preuves : messages, photos, certificats médicaux, témoignages, dates et lieux.",
      "Vous pouvez être accompagné·e par une personne de confiance ou une association d'aide aux victimes.",
      "Pour le harcèlement, nous avons des lettres pré-écrites (école, avocat, juge) prêtes à envoyer.",
    ],
    numbers: [
      { label: "Police (urgence)", value: "101" },
      { label: "Urgence européenne", value: "112" },
      { label: "Écoute violences (Belgique)", value: "1712 — gratuit & confidentiel" },
    ],
    safe: "Vous avez le droit d'être protégé·e. Demander de l'aide est un acte de courage, pas de faiblesse.",
  },
];

function plain(c: typeof cards[number]) {
  return `${c.title}. ${c.intro} ${c.rights.join(" ")} ${c.safe}`;
}

export default function MesDroitsMaintenantPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi</span>
          </Link>
          <Link href="/loi-avec-moi/modeles" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Lettres pré-écrites →</Link>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            <span className="w-2 h-2 rounded-full bg-rose-400" />
            Mes droits, maintenant
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">
            Vos droits, accessibles en un instant
          </h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Dans un moment difficile, on n&apos;a pas le temps de chercher. Voici vos droits essentiels,
            expliqués simplement — et lisibles à voix haute si vous ne pouvez pas lire.
          </p>
        </div>
      </section>

      {/* Cards */}
      <section className="py-16 px-6 max-w-3xl mx-auto space-y-8">
        {cards.map((c) => (
          <div key={c.id} id={c.id} className={`rounded-2xl border-2 ${c.color} p-7`}>
            <div className="flex items-center justify-between gap-3 flex-wrap">
              <span className="text-xs font-bold uppercase tracking-wide text-slate-500">{c.tag}</span>
              <ReadAloud text={plain(c)} label="Écouter mes droits" />
            </div>
            <h2 className="text-2xl font-bold tracking-tight mt-3">{c.title}</h2>
            <p className="text-slate-600 mt-2">{c.intro}</p>
            <ul className="mt-5 space-y-3">
              {c.rights.map((r, i) => (
                <li key={i} className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-600 text-white text-xs font-bold flex items-center justify-center mt-0.5">{i + 1}</span>
                  <span className="text-slate-700 text-sm leading-relaxed">{r}</span>
                </li>
              ))}
            </ul>
            {c.numbers.length > 0 && (
              <div className="mt-6 space-y-2">
                {c.numbers.map((n) => (
                  <div key={n.label} className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 bg-slate-50 rounded-xl border border-slate-200 px-4 py-3">
                    <span className="text-sm text-slate-600">{n.label}</span>
                    <span className="font-bold text-slate-900">{n.value}</span>
                  </div>
                ))}
              </div>
            )}
            <div className="mt-5 rounded-xl bg-indigo-50 border border-indigo-100 px-4 py-3">
              <p className="text-sm text-indigo-900 font-medium">💡 {c.safe}</p>
            </div>
          </div>
        ))}
      </section>

      {/* Disclaimer */}
      <section className="pb-10 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Ces informations sont générales et tirées de sources officielles belges (SPF Justice, IBZ,
            Belgium.be). Elles vous aident à <strong>comprendre et agir</strong>, mais ne remplacent pas
            l&apos;avis d&apos;un avocat pour votre situation précise. En cas de doute, contactez un
            professionnel ou l&apos;aide juridique.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La Loi Avec Moi »</Link>
      </footer>
    </main>
  );
}
