"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

const fiches = [
  {
    title: "Un licenciement suit des règles strictes",
    text: "L'employeur doit notifier le licenciement par courrier recommandé ou par huissier. Un licenciement verbal ou par simple message ne respecte pas la forme légale.",
    ref: "SPF Emploi — fin du contrat de travail",
    url: "https://emploi.belgique.be/fr/themes/contrats-de-travail/fin-du-contrat-de-travail/fin-du-contrat-duree-indeterminee-licenciement",
  },
  {
    title: "Vous avez droit à un préavis (ou une indemnité)",
    text: "La durée du préavis dépend de votre ancienneté. Si l'employeur ne le respecte pas, il vous doit une indemnité compensatoire correspondante.",
    ref: "SPF Emploi — congé moyennant préavis",
    url: "https://emploi.belgique.be/fr/themes/contrats-de-travail/fin-du-contrat-de-travail/fin-du-contrat-duree-indeterminee-3",
  },
  {
    title: "Le document C4 vous est dû à la fin",
    text: "À la fin de tout contrat, l'employeur doit vous remettre le C4. Il sert à faire valoir vos droits au chômage auprès de l'ONEM.",
    ref: "ONEM (officiel)",
    url: "https://www.onem.be/fr",
  },
  {
    title: "Un salaire minimum est garanti",
    text: "Un revenu minimum mensuel moyen garanti (RMMMG) existe en Belgique. Des minimums plus élevés peuvent s'appliquer selon votre secteur (commission paritaire).",
    ref: "SPF Emploi — rémunération",
    url: "https://emploi.belgique.be/fr/themes/remuneration",
  },
  {
    title: "Vous avez droit à des congés payés",
    text: "Un travailleur à temps plein (semaine de 5 jours) a droit à au moins 20 jours de congés légaux par an, s'il a travaillé l'année précédente.",
    ref: "SPF Emploi — vacances annuelles",
    url: "https://emploi.belgique.be/fr/themes/vacances-annuelles",
  },
  {
    title: "Le règlement de travail doit vous être accessible",
    text: "Votre entreprise doit avoir un règlement de travail et vous en remettre une copie. Il fixe horaires, sanctions, et vos droits internes.",
    ref: "SPF Emploi — règlement de travail",
    url: "https://emploi.belgique.be/fr/themes/reglementation-du-travail/reglement-de-travail",
  },
];

const readText = `Vos droits au travail. ${fiches.map((f) => f.title + ". " + f.text).join(" ")}`;

export default function TravailPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">L</span>
            </div>
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi/logement" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Droits logement →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Travail & emploi
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Vos droits au travail</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Contrat, préavis, licenciement, salaire, congés : l'essentiel à connaître pour ne pas se
            laisser faire — avec la référence officielle à l'appui.
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
            ⚖️ Le droit du travail évolue (des mesures changent au fil des réformes) et dépend de votre
            secteur. Ces fiches donnent les grands principes. En cas de litige, contactez votre syndicat,
            l'inspection du travail, ou un avocat (aide juridique possible).
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
