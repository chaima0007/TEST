"use client";

import Link from "next/link";
import { useState } from "react";
import AgentAvocat from "@/components/AgentAvocat";
import textesData from "@/data/belgium/_textes_legaux.json";

// Quiz « Connais-tu tes droits ? » (Belgique) — complet, par catégories.
// Chaque question est adossée à une fiche du site (sourcée officiellement) et,
// quand c'est pertinent, au TEXTE DE LOI derrière : année, pourquoi il a été
// créé, lien vers le texte officiel original (registre _textes_legaux.json).

type TexteLoi = {
  cle: string;
  nom: string;
  niveau: string;
  url: string;
  annee: number;
  contexte: string;
};

const TEXTES: Record<string, TexteLoi> = Object.fromEntries(
  (textesData.textes as TexteLoi[]).map((t) => [t.cle, t]),
);

type Categorie = {
  id: string;
  emoji: string;
  label: string;
  desc: string;
};

const CATEGORIES: Categorie[] = [
  { id: "conso", emoji: "🛒", label: "Consommation & achats", desc: "Achats, garanties, contrats, voyages" },
  { id: "logement", emoji: "🏠", label: "Logement", desc: "Bail, garantie locative, domicile" },
  { id: "travail", emoji: "💼", label: "Travail & entreprendre", desc: "Chômage, harcèlement au travail, indépendants" },
  { id: "famille", emoji: "👪", label: "Famille & jeunes", desc: "Couple, enfants, école, numéros d'aide" },
  { id: "justice", emoji: "⚖️", label: "Justice & droits fondamentaux", desc: "Constitution, avocat, recours, harcèlement" },
  { id: "argent", emoji: "💶", label: "Argent, impôts & dettes", desc: "Dettes, plans de paiement, recouvrement" },
  { id: "viePrivee", emoji: "🔐", label: "Vie privée & numérique", desc: "RGPD, données, cyberharcèlement" },
];

type Question = {
  cat: string;
  q: string;
  options: string[];
  correct: number;
  explication: string;
  fiche: { href: string; label: string };
  texte?: string; // clé du texte de loi dans le registre
};

const questions: Question[] = [
  /* ── 🛒 Consommation & achats ─────────────────────────────── */
  {
    cat: "conso",
    q: "Vous achetez un objet en ligne. Combien de temps avez-vous, en principe, pour vous rétracter sans justification ?",
    options: ["48 heures", "14 jours", "Aucun délai, c'est définitif"],
    correct: 1,
    explication:
      "Pour un achat à distance, vous disposez en principe de 14 jours pour vous rétracter sans devoir vous justifier. Attention : certains achats (sur mesure, contenus numériques téléchargés…) en sont exclus.",
    fiche: { href: "/loi-avec-moi/consommation", label: "Fiche Consommation & achats" },
    texte: "code_droit_economique",
  },
  {
    cat: "conso",
    q: "Un appareil neuf acheté en magasin tombe en panne après 8 mois. Êtes-vous couvert·e ?",
    options: [
      "Non, la garantie du magasin est payante",
      "Oui : une garantie légale de 2 ans s'applique",
      "Seulement si vous avez gardé la boîte",
    ],
    correct: 1,
    explication:
      "Une garantie légale de 2 ans s'applique sur un produit neuf acheté par un consommateur auprès d'une entreprise dans l'UE. C'est un droit gratuit, qui s'ajoute à toute garantie commerciale payante.",
    fiche: { href: "/loi-avec-moi/consommation", label: "Fiche Consommation & achats" },
    texte: "code_droit_economique",
  },
  {
    cat: "conso",
    q: "Vous avez signé un contrat contenant une clause abusive. Cette clause s'applique-t-elle ?",
    options: [
      "Oui : signé, c'est signé",
      "Non : une clause abusive est nulle, même signée",
      "Oui, sauf si vous avez signé sous la contrainte",
    ],
    correct: 1,
    explication:
      "Une clause abusive (qui crée un déséquilibre manifeste au détriment du consommateur) est réputée NULLE : elle ne s'applique pas, même si vous avez signé. Le reste du contrat, lui, continue en principe à s'appliquer.",
    fiche: { href: "/loi/clauses_abusives", label: "Fiche Clauses abusives" },
    texte: "code_droit_economique",
  },
  {
    cat: "conso",
    q: "Votre voyage à forfait est annulé par l'organisateur. À quoi avez-vous droit ?",
    options: [
      "À un bon d'achat uniquement",
      "Au remboursement de vos paiements",
      "À rien : c'est le risque du voyage",
    ],
    correct: 1,
    explication:
      "Si l'organisateur annule votre voyage à forfait, vous avez droit au remboursement des paiements effectués. Un bon à valoir peut vous être proposé, mais vous n'êtes pas obligé·e de l'accepter.",
    fiche: { href: "/loi/voyages", label: "Fiche Voyages à forfait" },
  },

  /* ── 🏠 Logement ──────────────────────────────────────────── */
  {
    cat: "logement",
    q: "Votre bailleur demande une garantie locative sur un compte bloqué. Quel est le maximum légal ?",
    options: ["1 mois de loyer", "2 mois de loyer", "6 mois de loyer"],
    correct: 1,
    explication:
      "Pour une garantie versée sur un compte individualisé bloqué à votre nom, le plafond est de 2 mois de loyer. L'argent reste à votre nom : le bailleur ne peut pas le garder « en liquide ».",
    fiche: { href: "/loi/garantie_locative", label: "Fiche Garantie locative" },
    texte: "decret_wallon_bail",
  },
  {
    cat: "logement",
    q: "Pourquoi faire un état des lieux d'entrée détaillé quand on loue un logement ?",
    options: [
      "C'est juste une formalité sans valeur",
      "Sans lui, difficile de prouver que les dégâts ne sont pas de vous — votre garantie est en jeu",
      "Uniquement pour les logements neufs",
    ],
    correct: 1,
    explication:
      "L'état des lieux d'entrée est votre meilleure protection : à la sortie, on compare. Sans état des lieux détaillé, prouver que les dégâts existaient déjà devient très difficile — et votre garantie locative est en jeu.",
    fiche: { href: "/loi/garantie_locative", label: "Fiche Garantie locative" },
    texte: "decret_wallon_bail",
  },
  {
    cat: "logement",
    q: "Votre bailleur (ou la police, sans mandat) peut-il entrer chez vous sans votre accord ?",
    options: [
      "Oui, le bailleur est propriétaire",
      "Non : le domicile est inviolable, sauf dans les cas prévus par la loi",
      "Oui, mais uniquement en journée",
    ],
    correct: 1,
    explication:
      "La Constitution garantit que le domicile est inviolable : personne — pas même votre bailleur — ne peut entrer chez vous sans votre accord, hors les cas prévus par la loi (p. ex. un mandat dans une enquête).",
    fiche: { href: "/loi/constitution_droits_fondamentaux", label: "Fiche Constitution & droits fondamentaux" },
    texte: "constitution",
  },
  {
    cat: "logement",
    q: "Quel juge est le « juge de proximité », compétent notamment pour le voisinage et les baux ?",
    options: ["Le juge de paix", "La Cour de cassation", "Le Conseil d'État"],
    correct: 0,
    explication:
      "Le juge de paix est le juge de proximité : voisinage, baux, petites créances… Et sa conciliation est gratuite — souvent le meilleur premier pas avant tout procès.",
    fiche: { href: "/loi-avec-moi/voisinage", label: "Fiche Conflits de voisinage" },
    texte: "code_judiciaire",
  },

  /* ── 💼 Travail & entreprendre ────────────────────────────── */
  {
    cat: "travail",
    q: "Vous êtes au chômage et on vous propose un petit boulot ponctuel. Que devez-vous faire ?",
    options: [
      "Travailler au moins 3 heures, c'est obligatoire",
      "Déclarer l'activité AVANT de commencer",
      "Rien, tant que c'est moins d'une journée",
    ],
    correct: 1,
    explication:
      "Il n'existe pas de règle de « 3 heures minimum ». Le principe est la déclaration : vous devez déclarer une activité ou un travail AVANT de le commencer (carte de contrôle). Un jour travaillé n'est en général pas indemnisé.",
    fiche: { href: "/loi-avec-moi/chomage", label: "Fiche Chômage & travail" },
  },
  {
    cat: "travail",
    q: "Vous voulez lancer votre activité d'indépendant. Quand devez-vous être inscrit·e à la BCE ?",
    options: [
      "Dans l'année qui suit le démarrage",
      "Au plus tard le jour du début de l'activité",
      "Seulement si vous dépassez un certain chiffre d'affaires",
    ],
    correct: 1,
    explication:
      "Toute activité doit être enregistrée à la Banque-Carrefour des Entreprises (BCE) au plus tard le jour du début de l'activité, via un guichet d'entreprises agréé. Votre numéro d'entreprise devient votre numéro de TVA.",
    fiche: { href: "/loi-avec-moi/creer-entreprise", label: "Fiche Créer son entreprise" },
  },
  {
    cat: "travail",
    q: "Vous êtes harcelé·e au travail. Quelle personne est spécialement prévue, en interne, pour vous aider en confiance ?",
    options: [
      "Le comptable de l'entreprise",
      "La personne de confiance ou le conseiller en prévention",
      "Personne : il faut aller directement au tribunal",
    ],
    correct: 1,
    explication:
      "La loi sur le bien-être au travail impose un dispositif contre les risques psychosociaux : vous pouvez saisir, en toute confidentialité, la personne de confiance ou le conseiller en prévention aspects psychosociaux — sans passer d'abord par un tribunal.",
    fiche: { href: "/loi/harcelement_violences", label: "Fiche Harcèlement & violences" },
    texte: "bien_etre_travail",
  },

  /* ── 👪 Famille & jeunes ──────────────────────────────────── */
  {
    cat: "famille",
    q: "Vous vivez en couple sans être mariés ni en cohabitation légale (cohabitation de fait). Si votre partenaire décède, héritez-vous automatiquement ?",
    options: [
      "Oui, comme un couple marié",
      "Non, vous n'avez droit à rien automatiquement",
      "Oui, mais seulement la moitié",
    ],
    correct: 1,
    explication:
      "En cohabitation de fait, aucun lien juridique n'est créé : le survivant n'hérite de rien automatiquement. La cohabitation légale (déclaration à la commune) ou le mariage offrent une protection bien plus forte.",
    fiche: { href: "/loi-avec-moi/famille", label: "Fiche Famille & vie privée" },
  },
  {
    cat: "famille",
    q: "L'accès à l'école peut-il être payant pour un enfant en obligation scolaire ?",
    options: [
      "Oui, chaque école fixe son prix",
      "Non : la Constitution garantit l'accès gratuit jusqu'à la fin de l'obligation scolaire",
      "Seulement dans l'enseignement communal",
    ],
    correct: 1,
    explication:
      "L'article 24 de la Constitution garantit que l'accès à l'enseignement est gratuit jusqu'à la fin de l'obligation scolaire. Certains frais limités existent, mais l'accès lui-même ne peut pas se vendre.",
    fiche: { href: "/loi/constitution_droits_fondamentaux", label: "Fiche Constitution & droits fondamentaux" },
    texte: "constitution",
  },
  {
    cat: "famille",
    q: "Un enfant belge de moins de 12 ans part en voyage à l'étranger. Quel est son document d'identité ?",
    options: ["Le carnet de vaccination", "La Kids-ID", "Aucun document avant 12 ans"],
    correct: 1,
    explication:
      "La Kids-ID est le document d'identité des enfants belges de moins de 12 ans pour voyager. Pensez à la demander à la commune bien à l'avance — et selon la situation, une autorisation parentale peut être utile.",
    fiche: { href: "/loi/voyage_mineur", label: "Fiche Voyage d'un mineur" },
  },
  {
    cat: "famille",
    q: "Tu es jeune et tu as besoin de parler à quelqu'un. Quel numéro est gratuit et anonyme ?",
    options: ["Le 103 (Écoute-Enfants)", "Le 1307", "Aucun numéro n'est gratuit"],
    correct: 0,
    explication:
      "Le 103, c'est Écoute-Enfants : gratuit, anonyme, pour parler de tout — peurs, famille, harcèlement, idées noires. Et en danger immédiat, c'est le 112.",
    fiche: { href: "/loi-avec-moi/jeunes", label: "Espace enfants & jeunes" },
  },

  /* ── ⚖️ Justice & droits fondamentaux ─────────────────────── */
  {
    cat: "justice",
    q: "Quel texte est « au-dessus » de toutes les autres lois belges ?",
    options: ["Le Code civil", "La Constitution", "Le Code pénal"],
    correct: 1,
    explication:
      "La Constitution est la norme suprême de la Belgique : toutes les autres lois doivent la respecter. Son Titre II (articles 8 à 32) liste vos droits fondamentaux — égalité, vie privée, liberté d'expression…",
    fiche: { href: "/loi/constitution_droits_fondamentaux", label: "Fiche Constitution & droits fondamentaux" },
    texte: "constitution",
  },
  {
    cat: "justice",
    q: "Conflit avec un voisin. Quelle démarche est GRATUITE et peut donner un accord ayant la valeur d'un jugement ?",
    options: [
      "La conciliation devant le juge de paix",
      "Engager directement un huissier",
      "Porter plainte à la police",
    ],
    correct: 0,
    explication:
      "La conciliation devant le juge de paix est gratuite et facultative. Si un accord est trouvé, le procès-verbal a la valeur d'un jugement. C'est souvent la meilleure première étape pour un conflit de voisinage.",
    fiche: { href: "/loi-avec-moi/voisinage", label: "Fiche Conflits de voisinage" },
    texte: "code_judiciaire",
  },
  {
    cat: "justice",
    q: "Harceler quelqu'un (en vrai ou en ligne), est-ce puni par la loi ?",
    options: [
      "Non, sauf s'il y a des coups",
      "Oui : le harcèlement est une infraction pénale",
      "Seulement entre adultes",
    ],
    correct: 1,
    explication:
      "Oui. Le harcèlement est une infraction (article 442bis du Code pénal) — y compris le cyberharcèlement. On peut porter plainte, et les mineurs ont des aides dédiées (103 Écoute-Enfants, Child Focus 116 000).",
    fiche: { href: "/loi/harcelement_violences", label: "Fiche Harcèlement & violences" },
    texte: "code_penal",
  },
  {
    cat: "justice",
    q: "Vous n'avez pas les moyens de payer un avocat. Que prévoit la loi ?",
    options: [
      "Rien : pas d'argent, pas d'avocat",
      "L'aide juridique (« pro deo ») : un avocat gratuit ou presque, selon vos revenus",
      "Un avocat gratuit, mais uniquement au pénal",
    ],
    correct: 1,
    explication:
      "L'aide juridique de deuxième ligne (Code judiciaire, art. 508/1 et suivants) donne droit à un avocat entièrement ou partiellement gratuit selon vos revenus — dans toutes les matières, pas seulement au pénal.",
    fiche: { href: "/loi-avec-moi/trouver-un-avocat", label: "Trouver le bon avocat (et le pro deo)" },
    texte: "code_judiciaire",
  },
  {
    cat: "justice",
    q: "Vous recevez une décision administrative défavorable. Quel est le réflexe n°1 ?",
    options: [
      "Attendre de voir si ça se confirme",
      "Repérer tout de suite la date de notification et le délai de recours",
      "La jeter si vous n'êtes pas d'accord",
    ],
    correct: 1,
    explication:
      "Le piège n°1 en administratif, c'est le délai. Notez la date de réception et cherchez le délai de recours (souvent au bas du courrier). Le recours administratif et le Médiateur fédéral sont gratuits.",
    fiche: { href: "/loi-avec-moi/demarches", label: "Fiche Démarches administratives" },
  },

  /* ── 💶 Argent, impôts & dettes ───────────────────────────── */
  {
    cat: "argent",
    q: "Vos dettes sont devenues impossibles à rembourser. Existe-t-il une procédure pour repartir ?",
    options: [
      "Non, les dettes durent toute la vie",
      "Oui : le règlement collectif de dettes, devant le tribunal du travail",
      "Oui, mais uniquement pour les entreprises",
    ],
    correct: 1,
    explication:
      "Le règlement collectif de dettes (Code judiciaire, art. 1675/2 et suivants) permet à une personne surendettée d'obtenir un plan encadré par un médiateur de dettes — et de repartir sur des bases saines. Les poursuites sont suspendues pendant la procédure.",
    fiche: { href: "/loi/surendettement_reglement_collectif_dettes", label: "Fiche Surendettement" },
    texte: "code_judiciaire",
  },
  {
    cat: "argent",
    q: "Vous ne pouvez pas payer votre impôt en une fois. Quel est le bon réflexe ?",
    options: [
      "Ne rien faire et attendre le rappel",
      "Demander un plan de paiement AVANT que la dette ne s'aggrave",
      "Changer de compte bancaire",
    ],
    correct: 1,
    explication:
      "Le SPF Finances accorde des plans de paiement : la clé est de demander AVANT que la dette ne s'aggrave et ne déclenche des poursuites. Une demande simple peut souvent se faire en ligne via MyMinfin.",
    fiche: { href: "/loi/plan_paiement_fiscal", label: "Fiche Plan de paiement fiscal" },
  },
  {
    cat: "argent",
    q: "Quelqu'un vous doit de l'argent et fait la sourde oreille. Quelle est la première étape formelle ?",
    options: [
      "Poster son nom sur les réseaux sociaux",
      "Envoyer une mise en demeure écrite",
      "Saisir directement ses biens",
    ],
    correct: 1,
    explication:
      "La mise en demeure est le courrier formel qui réclame officiellement le paiement et fixe un délai — étape quasi indispensable avant toute action. (Humilier quelqu'un en ligne peut, à l'inverse, vous mettre en tort.)",
    fiche: { href: "/loi/recouvrement_amiable", label: "Fiche Recouvrement amiable" },
  },

  /* ── 🔐 Vie privée & numérique ────────────────────────────── */
  {
    cat: "viePrivee",
    q: "Une entreprise détient des données personnelles sur vous. Pouvez-vous demander à y accéder et à les faire corriger ?",
    options: [
      "Non, c'est sa propriété",
      "Oui, le RGPD vous en donne le droit",
      "Seulement via un avocat",
    ],
    correct: 1,
    explication:
      "Le RGPD vous donne le droit d'accéder à vos données, de les corriger, et souvent de les faire effacer. En cas de blocage, vous pouvez porter plainte gratuitement auprès de l'Autorité de protection des données (APD).",
    fiche: { href: "/loi-avec-moi/famille", label: "Fiche Famille & vie privée (RGPD)" },
    texte: "rgpd",
  },
  {
    cat: "viePrivee",
    q: "Qui peut lire vos messages privés ou fouiller votre téléphone « juste pour voir » ?",
    options: [
      "Vos parents, votre employeur, la police : tout le monde",
      "Personne, en principe : la vie privée est protégée par la Constitution",
      "Votre employeur, s'il paie le téléphone",
    ],
    correct: 1,
    explication:
      "L'article 22 de la Constitution garantit à chacun le respect de sa vie privée et familiale. Des exceptions existent (prévues par la loi, p. ex. une enquête judiciaire), mais le principe est la protection.",
    fiche: { href: "/loi/constitution_droits_fondamentaux", label: "Fiche Constitution & droits fondamentaux" },
    texte: "constitution",
  },
  {
    cat: "viePrivee",
    q: "Tu es victime de cyberharcèlement. Que faut-il faire AVANT de bloquer et tout supprimer ?",
    options: [
      "Rien, il faut tout effacer au plus vite",
      "Garder des captures d'écran datées : ce sont tes preuves",
      "Répondre pour te défendre",
    ],
    correct: 1,
    explication:
      "Avant de bloquer (ce qui est une bonne idée), garde des captures d'écran datées des messages : ce sont les preuves indispensables pour un signalement à la plateforme ou une plainte. Ne réponds pas — cela alimente le harcèlement.",
    fiche: { href: "/loi/harcelement_violences", label: "Fiche Harcèlement & violences" },
    texte: "code_penal",
  },
];

function verdict(score: number, total: number) {
  const pct = (score / total) * 100;
  if (pct >= 80)
    return {
      titre: "Vous connaissez bien vos droits 👏",
      texte:
        "Beau score ! Vous avez les bons réflexes. Gardez ce site sous la main pour les détails et les sources officielles.",
      accent: "emerald" as const,
    };
  if (pct >= 50)
    return {
      titre: "Bonne base, à consolider 💪",
      texte:
        "Vous connaissez l'essentiel, mais quelques pièges classiques subsistent. Relisez les fiches liées aux questions ratées.",
      accent: "sky" as const,
    };
  return {
    titre: "Pas de panique — on est là pour ça 🤝",
    texte:
      "Personne ne naît en connaissant ses droits. Le bon réflexe, c'est justement de venir vérifier. Explorez les fiches : tout est sourcé et expliqué simplement.",
    accent: "indigo" as const,
  };
}

export default function QuizPage() {
  const [catSel, setCatSel] = useState<string | null>(null); // null = écran de choix
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [score, setScore] = useState(0);
  const [answered, setAnswered] = useState(false);
  const [finished, setFinished] = useState(false);

  const jeu = catSel === "tout" ? questions : questions.filter((q) => q.cat === catSel);
  const total = jeu.length;
  const question = jeu[current];
  const catInfo = CATEGORIES.find((c) => c.id === catSel);

  function demarrer(id: string) {
    setCatSel(id);
    setCurrent(0);
    setSelected(null);
    setScore(0);
    setAnswered(false);
    setFinished(false);
  }

  function choose(i: number) {
    if (answered) return;
    setSelected(i);
    setAnswered(true);
    if (i === question.correct) setScore((s) => s + 1);
  }

  function next() {
    if (current + 1 >= total) {
      setFinished(true);
      return;
    }
    setCurrent((c) => c + 1);
    setSelected(null);
    setAnswered(false);
  }

  const v = finished ? verdict(score, total) : null;

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

      <section className="hero-encre text-white py-16 px-6">
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="eyebrow inline-block text-[#d6b87c] mb-5">Quiz · Connais-tu tes droits ?</span>
          <h1 className="text-3xl sm:text-5xl tracking-tight leading-tight">
            Le droit belge, <em>en t&apos;amusant</em>
          </h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            {questions.length} questions, {CATEGORIES.length} catégories. Chaque réponse est expliquée, renvoie vers
            une fiche <strong className="text-white">sourcée officiellement</strong> — et vous montre le
            <strong className="text-white"> texte de loi</strong> derrière : son année, pourquoi il a été créé,
            et le lien pour le lire en version originale.
          </p>
        </div>
      </section>

      <section className="py-12 px-6 max-w-2xl mx-auto">
        {catSel === null ? (
          <>
            {/* Écran de choix de catégorie */}
            <h2 className="text-2xl tracking-tight text-center">Choisissez votre terrain</h2>
            <div className="mt-8 grid sm:grid-cols-2 gap-3">
              {CATEGORIES.map((c) => {
                const n = questions.filter((q) => q.cat === c.id).length;
                return (
                  <button
                    key={c.id}
                    onClick={() => demarrer(c.id)}
                    className="text-left rounded-lg border border-[#e7e0d3] bg-white p-5 hover:border-[#b08d3e] hover:-translate-y-0.5 transition-all"
                  >
                    <div className="text-2xl">{c.emoji}</div>
                    <div className="mt-2 font-bold">{c.label}</div>
                    <p className="text-sm text-slate-500 mt-0.5">{c.desc}</p>
                    <p className="text-xs font-semibold text-[#7e6234] mt-2">{n} questions</p>
                  </button>
                );
              })}
            </div>
            <button
              onClick={() => demarrer("tout")}
              className="mt-6 w-full rounded-lg bg-[#1b2432] hover:bg-[#2e3d5c] text-white font-semibold py-4 transition-colors"
            >
              🏆 Le grand quiz complet — {questions.length} questions
            </button>
          </>
        ) : !finished ? (
          <>
            {/* Progression */}
            <div className="flex items-center justify-between text-sm font-medium text-slate-500">
              <span>
                {catSel === "tout" ? "🏆 Grand quiz" : `${catInfo?.emoji} ${catInfo?.label}`} · Question {current + 1} / {total}
              </span>
              <span>Score : {score}</span>
            </div>
            <div className="mt-2 h-2 rounded-full bg-slate-100 overflow-hidden">
              <div
                className="h-full bg-[#b08d3e] transition-all"
                style={{ width: `${((current + (answered ? 1 : 0)) / total) * 100}%` }}
              />
            </div>

            {/* Question */}
            <h2 className="mt-8 text-xl tracking-tight leading-snug">{question.q}</h2>
            <div className="mt-6 space-y-3">
              {question.options.map((opt, i) => {
                const isCorrect = i === question.correct;
                const isChosen = i === selected;
                let cls = "border-slate-200 hover:border-[#b08d3e] hover:bg-[#fbf8f2]";
                if (answered && isCorrect) cls = "border-emerald-400 bg-emerald-50";
                else if (answered && isChosen && !isCorrect) cls = "border-rose-400 bg-rose-50";
                else if (answered) cls = "border-slate-200 opacity-60";
                return (
                  <button
                    key={i}
                    onClick={() => choose(i)}
                    disabled={answered}
                    className={`w-full text-left rounded-lg border-2 p-4 text-sm font-medium transition-colors ${cls}`}
                  >
                    <span className="inline-flex items-center gap-3">
                      <span className="flex-shrink-0 w-6 h-6 rounded-full border border-current flex items-center justify-center text-xs">
                        {String.fromCharCode(65 + i)}
                      </span>
                      {opt}
                      {answered && isCorrect && <span className="ml-1">✓</span>}
                      {answered && isChosen && !isCorrect && <span className="ml-1">✗</span>}
                    </span>
                  </button>
                );
              })}
            </div>

            {/* Explication */}
            {answered && (
              <div className="mt-6 rounded-lg border-2 border-[#e7e0d3] bg-[#fbf8f2] p-5">
                <p className="text-slate-800 text-sm leading-relaxed">
                  {selected === question.correct ? "✅ Bonne réponse ! " : "💡 La bonne réponse : "}
                  {question.explication}
                </p>
                <Link
                  href={question.fiche.href}
                  className="mt-3 inline-flex items-center gap-1.5 text-sm font-semibold text-[#2e3d5c] hover:text-[#1b2432] underline decoration-[#d6b87c]"
                >
                  📄 {question.fiche.label} →
                </Link>

                {/* Le texte de loi derrière ce droit : année, pourquoi, accès à l'original */}
                {question.texte && TEXTES[question.texte] && (
                  <div className="mt-4 rounded-lg border border-[#d6b87c]/50 bg-[#b08d3e]/[0.07] p-4">
                    <p className="eyebrow text-[#7e6234]">📜 Le texte de loi derrière ce droit</p>
                    <p className="mt-1.5 text-sm font-semibold text-slate-900">
                      {TEXTES[question.texte].nom}{" "}
                      <span className="font-normal text-[#7e6234]">· depuis {TEXTES[question.texte].annee}</span>
                    </p>
                    <p className="mt-1 text-xs text-slate-600 leading-relaxed">
                      {TEXTES[question.texte].contexte}
                    </p>
                    <a
                      href={TEXTES[question.texte].url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-2 inline-flex items-center gap-1 text-xs font-semibold text-[#7e6234] underline hover:text-[#b08d3e]"
                    >
                      Lire le texte officiel original ↗
                    </a>
                  </div>
                )}
              </div>
            )}

            {answered && (
              <button
                onClick={next}
                className="mt-6 w-full rounded-lg bg-[#1b2432] hover:bg-[#2e3d5c] text-white font-semibold py-3.5 transition-colors"
              >
                {current + 1 >= total ? "Voir mon résultat" : "Question suivante →"}
              </button>
            )}
          </>
        ) : (
          <>
            {/* Résultat */}
            <div className="text-center">
              <p className="text-sm font-medium text-slate-500">
                {catSel === "tout" ? "Grand quiz complet" : catInfo?.label}
              </p>
              <p className="mt-1 text-5xl font-black tracking-tight text-[#1b2432]">
                {score}<span className="text-2xl text-slate-400"> / {total}</span>
              </p>
            </div>

            <div className="mt-8 rounded-lg border border-[#e7e0d3] bg-[#fbf8f2] p-5">
              <AgentAvocat
                name="Léa"
                role="Votre assistante juridique"
                accent={v!.accent}
                message={v!.texte}
              />
            </div>

            <h2 className="mt-8 text-2xl tracking-tight text-center">{v!.titre}</h2>

            <div className="mt-8 flex flex-col gap-3">
              <button
                onClick={() => setCatSel(null)}
                className="w-full rounded-lg bg-[#1b2432] hover:bg-[#2e3d5c] text-white font-semibold py-3.5 transition-colors"
              >
                🔄 Choisir une autre catégorie
              </button>
              <Link
                href="/loi-avec-moi/textes-de-loi"
                className="w-full text-center rounded-lg border-2 border-[#e7e0d3] hover:border-[#b08d3e] text-[#2e3d5c] font-semibold py-3.5 transition-colors"
              >
                📜 Lire les textes de loi originaux →
              </Link>
              <Link
                href="/loi-avec-moi"
                className="w-full text-center rounded-lg border-2 border-[#e7e0d3] hover:border-[#b08d3e] text-[#2e3d5c] font-semibold py-3.5 transition-colors"
              >
                Explorer tous les sujets →
              </Link>
            </div>

            <p className="mt-6 text-center text-xs text-slate-400 leading-relaxed">
              Ce quiz est éducatif et simplifié. Pour votre situation précise, consultez les fiches (sourcées
              officiellement) ou un professionnel.
            </p>
          </>
        )}
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à tous les sujets</Link>
      </footer>
    </main>
  );
}
