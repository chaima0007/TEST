import Link from "next/link";

export const metadata = { title: "Conditions générales de vente — Caelum" };

export default function CGV() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link href="/" className="text-sm text-slate-500 hover:text-slate-900">← Retour</Link>
        </div>
      </header>
      <article className="max-w-3xl mx-auto px-6 py-14 prose prose-slate">
        <h1 className="text-3xl font-bold tracking-tight">Conditions générales de vente</h1>
        <div className="mt-6 space-y-5 text-slate-600 leading-relaxed text-sm">
          <p><strong>1. Objet</strong> — Les présentes conditions régissent les prestations de Caelum (création de sites web, tableaux de bord, automatisations, business plans).</p>
          <p><strong>2. Devis</strong> — Toute prestation fait l'objet d'un devis gratuit. Les travaux ne démarrent qu'après acceptation écrite du devis et versement de l'acompte éventuel.</p>
          <p><strong>3. Prix &amp; paiement</strong> — Les prix sont indiqués hors TVA le cas échéant. Le paiement s'effectue selon les modalités du devis (acompte au démarrage, solde à la livraison).</p>
          <p><strong>4. Délais</strong> — Les délais annoncés sont indicatifs et donnés de bonne foi. Caelum s'engage à informer le client de tout retard.</p>
          <p><strong>5. Livraison &amp; révisions</strong> — Le nombre de révisions incluses est précisé au devis. Le client dispose d'un délai raisonnable pour valider les livrables.</p>
          <p><strong>6. Responsabilité</strong> — Caelum est tenu à une obligation de moyens. Sa responsabilité ne saurait excéder le montant de la prestation concernée.</p>
          <p><strong>7. Droit applicable</strong> — Les présentes conditions sont soumises au droit belge. Tout litige relève des tribunaux compétents de Bruxelles.</p>
        </div>
        <p className="mt-10 text-xs text-slate-400">Dernière mise à jour : 2026. Document à faire valider par un juriste pour une conformité complète.</p>
      </article>
    </main>
  );
}
