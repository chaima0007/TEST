import Link from "next/link";

export const metadata = {
  title: "Politique de confidentialité (RGPD) — La Loi Avec Moi",
  description: "Comment La Loi Avec Moi traite (ou ne traite pas) vos données personnelles, conformément au RGPD.",
};

export default function ConfidentialitePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="font-bold text-lg tracking-tight">La Loi Avec Moi</Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">← Accueil</Link>
        </div>
      </header>

      <article className="max-w-3xl mx-auto px-6 py-12 space-y-6">
        <h1 className="text-3xl font-bold">Politique de confidentialité</h1>
        <p className="text-slate-600 text-sm">Conformément au Règlement (UE) 2016/679 (RGPD).</p>

        <section>
          <h2 className="text-lg font-bold">Notre principe : le minimum de données</h2>
          <p className="text-slate-700 text-sm leading-relaxed mt-2">
            La Loi Avec Moi est conçu pour être consulté librement, sans créer de compte. La consultation des
            réponses juridiques ne nécessite pas de fournir de données personnelles.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-bold">Données éventuellement traitées</h2>
          <ul className="list-disc list-inside text-slate-700 text-sm mt-2 space-y-1">
            <li><strong>Mesure d'audience</strong> : statistiques anonymes/agrégées de fréquentation (si activées), sans vous identifier.</li>
            <li><strong>Contact volontaire</strong> : si vous nous écrivez, votre message et votre adresse e-mail, uniquement pour vous répondre.</li>
          </ul>
          <p className="text-xs text-amber-700 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 mt-2">
            ⚠️ À adapter selon les outils réellement activés (analytics, formulaire) au moment de la mise en ligne.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-bold">Vos droits (RGPD)</h2>
          <p className="text-slate-700 text-sm leading-relaxed mt-2">
            Vous disposez d'un droit d'accès, de rectification, d'effacement, d'opposition et de portabilité de vos
            données. Pour les exercer : chaima.caelumpartners@gmail.com. Vous pouvez aussi introduire une plainte auprès
            de l'Autorité de protection des données (APD).
          </p>
          <p className="text-slate-700 text-sm mt-2">
            APD : <a href="https://www.autoriteprotectiondonnees.be" target="_blank" rel="noopener noreferrer" className="text-indigo-700 hover:underline">autoriteprotectiondonnees.be</a>
          </p>
        </section>

        <section>
          <h2 className="text-lg font-bold">Cookies</h2>
          <p className="text-slate-700 text-sm leading-relaxed mt-2">
            Le site fonctionne sans cookies de suivi par défaut. Si une mesure d'audience est activée, elle le sera
            dans le respect du RGPD (consentement si nécessaire).
          </p>
        </section>
      </article>
    </main>
  );
}
