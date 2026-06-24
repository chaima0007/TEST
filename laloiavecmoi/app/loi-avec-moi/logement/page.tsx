"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

const fiches = [
  {
    title: "La garantie locative est plafonnée",
    text: "Sur un compte bloqué à votre nom, la garantie ne peut pas dépasser 2 mois de loyer (dans toutes les régions). Sous forme de garantie bancaire, elle peut aller jusqu'à 3 mois.",
    ref: "Belgium.be — la garantie locative",
    url: "https://www.belgium.be/fr/logement/location/garantie_locative",
  },
  {
    title: "La garantie doit vous être rendue",
    text: "À la fin du bail, le propriétaire doit libérer votre garantie. À Bruxelles, il a 2 mois après votre départ — au-delà, une indemnité de retard peut s'appliquer.",
    ref: "Bruxelles Logement (officiel régional)",
    url: "https://logement.brussels/louer/le-bail/la-garantie-locative/",
  },
  {
    title: "Un état des lieux vous protège",
    text: "L'état des lieux d'entrée (et de sortie) fixe l'état du logement. Sans lui, il est très difficile pour le propriétaire de vous réclamer des dégâts.",
    ref: "Belgium.be — la location",
    url: "https://www.belgium.be/fr/logement/location",
  },
  {
    title: "Vous pouvez donner congé avec préavis",
    text: "Dans un bail de 9 ans, le locataire peut résilier à tout moment avec un préavis de 3 mois (une indemnité peut être due les premières années).",
    ref: "Logement Wallonie (officiel régional)",
    url: "https://logement.wallonie.be/fr/louer",
  },
  {
    title: "Le loyer ne s'indexe qu'une fois par an",
    text: "Le propriétaire peut indexer le loyer une fois par an maximum, à la date anniversaire du bail, et seulement si le bail le prévoit par écrit.",
    ref: "Belgium.be — l'indexation du loyer",
    url: "https://www.belgium.be/fr/logement/location",
  },
  {
    title: "Les grosses réparations sont pour le propriétaire",
    text: "L'entretien courant est à votre charge ; les grosses réparations (toiture, chauffage, vétusté) sont à la charge du propriétaire.",
    ref: "Wonen in Vlaanderen (officiel régional)",
    url: "https://www.vlaanderen.be/wonen-en-energie/huren-en-verhuren",
  },
];

const readText = `Vos droits en logement. ${fiches.map((f) => f.title + ". " + f.text).join(" ")}`;

export default function LogementPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi/travail" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Droits au travail →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Logement & bail
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Vos droits de locataire</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Caution, état des lieux, préavis, réparations : ce que la loi prévoit, expliqué simplement —
            avec la référence officielle à montrer si besoin.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      <section className="py-16 px-6 max-w-3xl mx-auto space-y-5">
        {fiches.map((f, i) => (
          <div key={i} className="rounded-2xl border border-slate-200 p-6">
            <div className="flex items-start gap-3">
              <span className="flex-shrink-0 w-7 h-7 rounded-full bg-indigo-600 text-white text-sm font-bold flex items-center justify-center mt-0.5">{i + 1}</span>
              <div>
                <h2 className="text-lg font-bold tracking-tight">{f.title}</h2>
                <p className="text-slate-700 text-sm mt-2 leading-relaxed">{f.text}</p>
                <a href={f.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-xs font-medium text-indigo-700 mt-3 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-3 py-2 transition-colors">
                  🔗 Source officielle : {f.ref}
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
                </a>
              </div>
            </div>
          </div>
        ))}
      </section>

      <section className="pb-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Le bail est <strong>régionalisé</strong> en Belgique : les règles varient légèrement entre
            Bruxelles, la Wallonie et la Flandre. Ces fiches donnent les grands principes. Pour un litige,
            faites-vous accompagner (avocat, aide juridique, ou un service logement de votre région).
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
