"use client";

import Link from "next/link";
import { useState } from "react";
import ReadAloud from "@/components/ReadAloud";

const letters = [
  {
    id: "plainte",
    tag: "Police",
    title: "Déposer une plainte",
    desc: "Pour signaler une agression, un vol, des menaces ou du harcèlement à la police.",
    body: `Objet : Dépôt de plainte

Madame, Monsieur,

Par la présente, je souhaite déposer plainte concernant les faits suivants :

[Décrivez ce qui s'est passé : quoi, quand, où, qui était présent.]

Ces faits m'ont causé le préjudice suivant :
[Expliquez les conséquences : blessures, peur, dommages, etc.]

Je joins les éléments de preuve dont je dispose :
[Liste : messages, photos, certificat médical, témoignages…]

Je vous demande d'enregistrer cette plainte et de me remettre une copie du procès-verbal.

Je reste à votre disposition pour toute information complémentaire.

Nom et prénom : ______________________
Adresse : ______________________
Date : ______________________
Signature : ______________________`,
  },
  {
    id: "harcelement-ecole",
    tag: "École",
    title: "Signaler un harcèlement à l'école",
    desc: "Pour alerter la direction et demander que des mesures soient prises.",
    body: `Objet : Signalement d'une situation de harcèlement

Madame la Directrice, Monsieur le Directeur,

Je me permets de vous écrire car [mon enfant / je] subit une situation de harcèlement au sein de l'établissement.

Voici les faits constatés :
[Décrivez : insultes, mises à l'écart, violences, messages… avec dates si possible.]

Cette situation a les conséquences suivantes :
[Angoisse, refus d'aller en cours, baisse des résultats, etc.]

Je vous demande de bien vouloir :
- prendre des mesures pour faire cesser ces faits,
- me tenir informé·e des actions mises en place,
- organiser un entretien dans les meilleurs délais.

Je compte sur votre engagement pour garantir un environnement sûr.

Nom et prénom : ______________________
Lien avec l'élève : ______________________
Date : ______________________
Signature : ______________________`,
  },
  {
    id: "avocat",
    tag: "Avocat",
    title: "Demander l'aide d'un avocat",
    desc: "Pour solliciter un avocat, y compris l'aide juridique gratuite (« pro deo ») selon vos revenus.",
    body: `Objet : Demande d'assistance juridique

Maître,

Je souhaite être assisté·e par un avocat concernant la situation suivante :

[Expliquez brièvement votre problème.]

Mes ressources étant limitées, je souhaite savoir si je peux bénéficier de l'aide juridique
(« pro deo »), totalement ou partiellement gratuite.

Je vous remercie de me préciser les documents à fournir et un rendez-vous possible.

Dans l'attente de votre réponse, je vous prie d'agréer mes salutations respectueuses.

Nom et prénom : ______________________
Téléphone / e-mail : ______________________
Date : ______________________
Signature : ______________________`,
  },
  {
    id: "juge-jeunesse",
    tag: "Justice des jeunes",
    title: "Écrire à mon juge de la jeunesse",
    desc: "Pour un·e jeune qui veut être entendu·e ou demander quelque chose à son juge.",
    body: `Objet : Demande à être entendu·e

Madame la Juge, Monsieur le Juge,

Je m'appelle [prénom et nom] et j'ai [âge] ans. Vous suivez ma situation.

Je voudrais vous parler de quelque chose qui est important pour moi :
[Dis ce que tu ressens et ce que tu voudrais : voir ta famille, changer de lieu, être écouté·e…]

Voici ce que je souhaite vous demander :
[Ta demande, simplement.]

J'aimerais beaucoup que vous m'écoutiez. Je sais que j'ai le droit d'être entendu·e
et d'être aidé·e par un avocat.

Merci de m'avoir lu.

Prénom et nom : ______________________
Date : ______________________`,
  },
];

function LetterCard({ l }: { l: typeof letters[number] }) {
  const [copied, setCopied] = useState(false);

  function copy() {
    if (typeof navigator !== "undefined" && navigator.clipboard) {
      navigator.clipboard.writeText(l.body).then(() => {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      });
    }
  }

  return (
    <div id={l.id} className="rounded-2xl border border-slate-200 overflow-hidden">
      <div className="p-6 border-b border-slate-100">
        <span className="text-xs font-bold uppercase tracking-wide text-indigo-600">{l.tag}</span>
        <h2 className="text-xl font-bold tracking-tight mt-1">{l.title}</h2>
        <p className="text-slate-600 text-sm mt-1.5">{l.desc}</p>
        <div className="flex items-center gap-3 mt-4 flex-wrap">
          <button
            type="button"
            onClick={copy}
            className="inline-flex items-center gap-2 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-full px-4 py-2 transition-colors"
          >
            {copied ? "✓ Copié !" : "Copier le texte"}
          </button>
          <ReadAloud text={l.body} label="Écouter le modèle" />
        </div>
      </div>
      <pre className="p-6 bg-slate-50 text-sm text-slate-700 whitespace-pre-wrap font-sans leading-relaxed">{l.body}</pre>
    </div>
  );
}

export default function ModelesPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi/mes-droits-maintenant" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Mes droits maintenant →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Lettres prêtes à envoyer
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">
            Les mots, on vous les donne
          </h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Pas besoin de savoir écrire une lettre officielle. Copiez le modèle, remplacez les parties
            entre crochets, et envoyez. Vous pouvez aussi l&apos;écouter à voix haute.
          </p>
        </div>
      </section>

      <section className="pt-12 px-6 max-w-3xl mx-auto">
        <Link
          href="/loi-avec-moi/documents"
          className="group flex items-center justify-between gap-4 rounded-2xl border border-indigo-200 bg-indigo-50 p-5 hover:bg-indigo-100 transition-colors"
        >
          <div>
            <p className="font-bold tracking-tight text-indigo-900">✨ Besoin d&apos;une lettre personnalisée ?</p>
            <p className="text-indigo-800/90 text-sm mt-1 leading-relaxed">
              Notre générateur remplit le document avec vos infos et le met en forme — prêt à imprimer ou en PDF.
            </p>
          </div>
          <span className="flex-shrink-0 inline-flex items-center gap-1.5 rounded-xl bg-indigo-600 group-hover:bg-indigo-700 px-4 py-2.5 text-sm font-semibold text-white transition-colors">
            Générateur →
          </span>
        </Link>
      </section>

      <section className="py-12 px-6 max-w-3xl mx-auto space-y-8">
        {letters.map((l) => (
          <LetterCard key={l.id} l={l} />
        ))}
      </section>

      <section className="pb-10 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Ces modèles sont des aides générales pour vous faire gagner du temps. Pour une situation
            grave ou complexe, faites-vous accompagner par un avocat (l&apos;aide juridique « pro deo »
            peut être gratuite selon vos revenus).
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
