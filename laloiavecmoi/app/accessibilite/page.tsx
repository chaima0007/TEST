import Link from "next/link";

export const metadata = {
  title: "Déclaration d'accessibilité — La Loi Avec Moi",
  description: "Notre engagement d'accessibilité numérique (WCAG 2.2 AA / European Accessibility Act).",
};

export default function AccessibilitePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="font-bold text-lg tracking-tight">La Loi Avec Moi</Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">← Accueil</Link>
        </div>
      </header>

      <article className="max-w-3xl mx-auto px-6 py-12 space-y-6">
        <h1 className="text-3xl font-bold">Déclaration d'accessibilité</h1>

        <section>
          <h2 className="text-lg font-bold">Notre engagement</h2>
          <p className="text-slate-700 text-sm leading-relaxed mt-2">
            La Loi Avec Moi veut être accessible à toutes et tous, y compris aux personnes en situation de handicap.
            Nous visons la conformité au standard <strong>WCAG 2.2 niveau AA</strong> et nous inscrivons dans l'esprit
            de l'European Accessibility Act (accès numérique pour tous).
          </p>
        </section>

        <section>
          <h2 className="text-lg font-bold">Ce que nous faisons</h2>
          <ul className="list-disc list-inside text-slate-700 text-sm mt-2 space-y-1">
            <li>Contrastes élevés, texte lisible et agrandissable.</li>
            <li>Navigation au clavier et focus visible.</li>
            <li>Langage clair, sans jargon non expliqué.</li>
            <li>Lecture audio des modèles de documents (synthèse vocale).</li>
            <li>Aide à la traduction (langue de votre choix via le navigateur).</li>
          </ul>
        </section>

        <section>
          <h2 className="text-lg font-bold">Amélioration continue</h2>
          <p className="text-slate-700 text-sm leading-relaxed mt-2">
            L'accessibilité est un travail continu : certaines pages peuvent encore être améliorées. Un test par des
            utilisateurs concernés est prévu. Si vous rencontrez un obstacle, dites-le nous : nous corrigerons.
          </p>
          <p className="text-slate-700 text-sm mt-2">Contact accessibilité : chaima.caelumpartners@gmail.com.</p>
        </section>
      </article>
    </main>
  );
}
