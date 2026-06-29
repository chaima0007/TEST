import Link from "next/link";

// Outil de clarté « AI Act : suis-je concerné ? » — Caelum.
// Réponse directe à l'opportunité détectée par la veille (OPP-AI-ACT) : les PME sont perdues
// sur les dates et croient avoir jusqu'en 2027. Honnêteté : on clarifie, on ne vend pas
// une plateforme à 30k€ (le marché en est inondé). Si high-risk → voir un professionnel.

export const dynamic = "force-static";
export const metadata = {
  title: "AI Act : suis-je concerné ? Les dates et obligations clés (clair) — Caelum",
  description:
    "Règlement IA (UE) 2024/1689 expliqué simplement : qui est concerné, ce qui s'applique déjà, l'échéance du 2 août 2026 (transparence), les sanctions — sans jargon ni peur.",
};

const dates = [
  { d: "2 février 2025", t: "Pratiques interdites + obligation de littératie IA (Art. 4)", etat: "en vigueur" },
  { d: "2 août 2025", t: "Obligations des modèles d'IA à usage général (GPAI)", etat: "en vigueur" },
  { d: "2 août 2026", t: "Transparence GÉNÉRALE (Art. 50) — information « vous parlez à une IA » (50(1)) + étiquetage des deepfakes (50(4)), côté déployeurs. NON reportée, même pour les PME.", etat: "imminent" },
  { d: "2 décembre 2026", t: "Marquage MACHINE-READABLE des contenus générés par IA (Art. 50(2), FOURNISSEURS) — uniquement pour les systèmes déjà sur le marché avant le 02/08/2026 (période transitoire de 4 mois). Les systèmes lancés après le 02/08/2026 : tout dès le 02/08/2026.", etat: "imminent" },
  { d: "2 février 2027", t: "Interopérabilité de la détection des marquages (Code de pratique sur la transparence)", etat: "à venir" },
  { d: "2027-2028", t: "Obligations des systèmes à haut risque (reportées par le Digital Omnibus)", etat: "à venir" },
];

const buckets = [
  { n: "Interdit", d: "Pratiques prohibées (ex. notation sociale, manipulation). Interdites depuis février 2025.", c: "rose" },
  { n: "Haut risque", d: "RH (recrutement), accès au crédit/assurance, éducation, infrastructures critiques, composant de sécurité d'un produit réglementé. Obligations lourdes.", c: "amber" },
  { n: "Risque limité", d: "Chatbots, contenus générés par IA destinés au public → obligation de TRANSPARENCE (informer l'utilisateur). C'est le cas le plus fréquent en PME.", c: "indigo" },
  { n: "Risque minimal", d: "La majorité des usages (outils internes, productivité). Pas d'obligation substantielle.", c: "emerald" },
];

export default function AiActPage() {
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

      <section className="bg-gradient-to-b from-slate-950 to-slate-900 text-white py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-5">
            Règlement IA (UE) 2024/1689
          </span>
          <h1 className="text-3xl sm:text-4xl font-bold">AI Act : suis-je concerné ?</h1>
          <p className="mt-3 text-slate-300 max-w-2xl">
            Beaucoup d'entreprises pensent avoir jusqu'en 2027. C'est faux pour plusieurs obligations.
            Voici l'essentiel, en clair — sans jargon, sans peur, sans plateforme à 30 000 €.
          </p>
        </div>
      </section>

      <section className="max-w-4xl mx-auto px-6 py-12">
        {/* Le piège des dates */}
        <h2 className="text-xl font-bold">Les dates qui comptent</h2>
        <div className="mt-4 grid gap-3">
          {dates.map((x) => (
            <div key={x.d} className={`rounded-xl border p-4 flex items-start justify-between gap-3 ${x.etat === "imminent" ? "border-amber-300 bg-amber-50" : x.etat === "en vigueur" ? "border-emerald-200 bg-emerald-50" : "border-slate-200"}`}>
              <div>
                <p className="font-semibold text-slate-900">{x.d}</p>
                <p className="text-sm text-slate-600 mt-0.5">{x.t}</p>
              </div>
              <span className={`text-xs font-bold whitespace-nowrap ${x.etat === "imminent" ? "text-amber-700" : x.etat === "en vigueur" ? "text-emerald-700" : "text-slate-500"}`}>{x.etat}</span>
            </div>
          ))}
        </div>
        <p className="text-sm text-slate-500 mt-3">
          ⚠️ Ne pas confondre deux échéances distinctes : les obligations <strong>générales</strong> de transparence
          (Art. 50 — chatbot, deepfakes) s'appliquent dès le <strong>2 août 2026</strong> ; le <strong>marquage
          machine-readable</strong> des contenus générés par IA (<strong>Art. 50(2), fournisseurs</strong>) bénéficie
          d'un délai au <strong>2 décembre 2026</strong> pour les systèmes déjà sur le marché. Le Digital Omnibus a
          reporté le <strong>haut risque</strong> (2027-2028) mais <strong>pas</strong> la transparence. « Report » ≠ « exemption ».
        </p>

        {/* Les 4 niveaux */}
        <h2 className="text-xl font-bold mt-10">Dans quelle catégorie êtes-vous ?</h2>
        <div className="mt-4 grid sm:grid-cols-2 gap-4">
          {buckets.map((b) => (
            <div key={b.n} className="rounded-2xl border border-slate-200 p-5">
              <h3 className="font-bold text-slate-900">{b.n}</h3>
              <p className="text-sm text-slate-600 mt-1.5">{b.d}</p>
            </div>
          ))}
        </div>

        {/* Sanctions */}
        <div className="mt-10 rounded-2xl border border-rose-200 bg-rose-50 p-5">
          <h2 className="font-bold text-rose-900">Sanctions (Art. 99)</h2>
          <p className="text-sm text-rose-800 mt-2">
            Jusqu'à <strong>35 M€ ou 7 %</strong> du CA mondial (pratiques interdites), <strong>15 M€ ou 3 %</strong>
            (manquement haut risque), <strong>7,5 M€ ou 1 %</strong> (information incorrecte). Plafonds réduits pour les PME.
          </p>
        </div>

        {/* Porte de sortie honnête */}
        <div className="mt-8 rounded-3xl bg-gradient-to-br from-emerald-600 to-emerald-700 text-white p-8 text-center">
          <h2 className="text-2xl font-bold">Pour la plupart des PME : pas de panique.</h2>
          <p className="mt-3 text-emerald-50 max-w-2xl mx-auto leading-relaxed">
            La majorité des usages sont « risque limité » (transparence) ou « minimal ». Vous avez surtout besoin de
            <strong> clarté</strong> : un inventaire de vos IA + une classification. Pas d'une plateforme à 30 000 €.
            Si vous êtes en haut risque, on vous le dit honnêtement et on vous oriente vers un professionnel.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center mt-6">
            <Link href="/conformite-2026" className="bg-white text-emerald-700 font-semibold px-6 py-3 rounded-xl hover:bg-emerald-50 transition-colors">Vérifier ma situation</Link>
            <Link href="/conformite/ai-act" className="border border-white/40 text-white font-semibold px-6 py-3 rounded-xl hover:bg-white/10 transition-colors">La fiche sourcée</Link>
          </div>
        </div>

        <p className="text-center text-xs text-slate-400 mt-6">
          Source : Règlement (UE) 2024/1689 (AI Act), Art. 4, 50, 51, 99 ; Digital Omnibus (accord mai 2026).
          Information générale, pas un conseil juridique individualisé.
        </p>
      </section>
    </main>
  );
}
