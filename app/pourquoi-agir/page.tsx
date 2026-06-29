import Link from "next/link";

// Section marketing « Pourquoi agir » — Caelum.
// Met en évidence les conséquences financières/juridiques RÉELLES (sourcées) de la non-conformité
// PUIS rassure immédiatement (porte de sortie : simulateur + financement + accompagnement).
// Honnêteté : on informe avec les sanctions prévues par la loi, on ne « vend pas la peur ».

export const dynamic = "force-static";
export const metadata = {
  title: "Pourquoi agir : ce que la non-conformité coûte vraiment — Caelum",
  description:
    "GDPR, NIS2, CSRD, e-facturation : les sanctions réelles prévues par la loi — et comment les rendre gérables, sereinement, avec les aides qui financent la mise en conformité.",
};

const risques = [
  { norme: "RGPD", slug: "rgpd", chiffre: "jusqu'à 20 M€ ou 4 % du CA mondial", detail: "Le montant le plus élevé des deux s'applique. Toute entreprise traitant des données est concernée." },
  { norme: "NIS2", slug: "nis2", chiffre: "jusqu'à 10 M€ ou 2 % du CA mondial", detail: "Et surtout : responsabilité personnelle du dirigeant. Ce n'est plus un sujet IT." },
  { norme: "CSDDD — devoir de vigilance", slug: "csddd", chiffre: "amendes jusqu'à 3 % du CA mondial net", detail: "Détail fixé à la transposition ; vos grands clients répercutent leurs exigences sur vous." },
  { norme: "CSRD — reporting durabilité", slug: "csrd", chiffre: "sanctions par État membre + risque réputationnel", detail: "Être hors champ ne protège pas : l'effet cascade vous atteint via vos donneurs d'ordre." },
  { norme: "E-facturation B2B", slug: "e-facturation", chiffre: "amendes graduées (1 500 € → 3 000 € → 5 000 €) + perte de la déduction TVA", detail: "Le PDF simple n'a plus de valeur fiscale depuis le 01/01/2026." },
];

export default function PourquoiAgir() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg">Caelum</span>
          </Link>
          <Link href="/conformite-2026" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Suis-je concerné ?</Link>
        </div>
      </header>

      {/* Le risque réel */}
      <section className="bg-gradient-to-b from-slate-950 to-slate-900 text-white py-16 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-rose-500/15 border border-rose-400/30 text-rose-200 text-sm font-medium mb-5">
            Ce que la non-conformité coûte vraiment
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold leading-tight">
            La loi ne prévient pas.
            <span className="block bg-gradient-to-r from-rose-300 to-amber-300 bg-clip-text text-transparent">Elle sanctionne.</span>
          </h1>
          <p className="mt-5 text-slate-300 max-w-2xl mx-auto">
            Voici les sanctions <strong>réellement prévues par la loi</strong> en 2026 — pas des estimations,
            pas de la peur. Chaque chiffre renvoie à sa source officielle.
          </p>
        </div>
      </section>

      <section className="max-w-4xl mx-auto px-6 py-12">
        <div className="grid gap-4">
          {risques.map((r) => (
            <Link key={r.slug} href={`/conformite/${r.slug}`} className="rounded-2xl border border-slate-200 p-5 hover:border-rose-300 hover:shadow-sm transition-all">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h2 className="font-bold text-slate-900">{r.norme}</h2>
                  <p className="text-sm text-slate-600 mt-1">{r.detail}</p>
                </div>
                <span className="text-sm font-bold text-rose-700 text-right whitespace-nowrap max-w-[40%]">{r.chiffre}</span>
              </div>
              <span className="inline-block mt-2 text-sm font-semibold text-indigo-700">Voir la fiche sourcée →</span>
            </Link>
          ))}
        </div>

        {/* La porte de sortie — non anxiogène */}
        <div className="mt-10 rounded-3xl bg-gradient-to-br from-emerald-600 to-emerald-700 text-white p-8 text-center">
          <h2 className="text-2xl sm:text-3xl font-bold">Mais pas de panique.</h2>
          <p className="mt-3 text-emerald-50 max-w-2xl mx-auto leading-relaxed">
            On ne vend pas la peur. Ces chiffres existent, c'est tout — notre rôle est de les rendre
            <strong> gérables</strong>. En 1 minute, on vous dit ce qui vous concerne <em>vraiment</em>,
            on vous met en règle, et on cherche <strong>l'aide publique qui finance</strong> la mise en conformité.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center mt-7">
            <Link href="/conformite-2026" className="bg-white text-emerald-700 font-semibold px-6 py-3 rounded-xl hover:bg-emerald-50 transition-colors">
              Faire le test gratuit (1 min)
            </Link>
            <Link href="/calculateur-aide-nette" className="border border-white/40 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/10 transition-colors">
              Calculer mon coût net (après aide)
            </Link>
          </div>
        </div>

        <div className="mt-8 grid sm:grid-cols-3 gap-4 text-center">
          {[
            { t: "Sourcé", d: "Chaque sanction renvoie au texte officiel." },
            { t: "Finançable", d: "Des aides régionales couvrent une partie du coût." },
            { t: "Serein", d: "On informe et on accompagne — sans dramatiser." },
          ].map((c) => (
            <div key={c.t} className="rounded-2xl border border-slate-200 p-5">
              <p className="font-bold text-slate-900">{c.t}</p>
              <p className="text-sm text-slate-600 mt-1">{c.d}</p>
            </div>
          ))}
        </div>

        <p className="text-center text-xs text-slate-400 mt-6">
          Montants = plafonds/sanctions prévus par les réglementations citées (voir chaque fiche). Les informations
          ne constituent pas un conseil juridique individualisé.
        </p>
      </section>
    </main>
  );
}
