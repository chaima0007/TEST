import Link from "next/link";
import BulleHeader from "@/components/bulle/BulleHeader";
import { SOURCES, CONSULTED_ON } from "@/lib/bulle/sources";

export const metadata = {
  title: "Bulle — Promesses, sources & méthode",
};

const PROMISES = [
  { emoji: "🙈", t: "Jamais de surveillance", d: "Bulle n’est pas un outil de contrôle. Aucun suivi de position, aucun historique d’activité de l’enfant, aucun rapport aux parents sur « ce qu’a fait » l’enfant. L’app aide à parler, pas à espionner." },
  { emoji: "🔐", t: "Sécurité par design", d: "Aucun chat ouvert, aucun contact avec des inconnus, aucun lien vers l’extérieur côté enfant, aucune publicité ciblée." },
  { emoji: "📵", t: "Minimisation des données", d: "Aucune donnée personnelle d’enfant n’est demandée ni stockée. Pas de nom, pas de photo, pas de compte. Les préférences d’affichage restent en mémoire, le temps de la visite." },
  { emoji: "🧭", t: "Portail parental", d: "L’espace adulte est protégé par un « parental gate » : une petite opération que les jeunes enfants ne réalisent pas seuls." },
  { emoji: "📚", t: "Contenu fondé, jamais inventé", d: "Chaque conseil renvoie à un organisme reconnu ou un ouvrage de référence, avec l’année de publication." },
  { emoji: "♿", t: "Accessible à tous", d: "Grandes cibles tactiles, lecture à voix haute sur l’appareil, option gros texte, respect des préférences de mouvement réduit, focus clavier visibles." },
];

export default function PromessesPage() {
  const sources = Object.values(SOURCES);
  return (
    <main>
      <BulleHeader />
      <h1 className="text-3xl font-extrabold">Nos promesses, nos sources, notre méthode</h1>
      <p className="mt-2 max-w-2xl text-[var(--b-muted)]">
        La confiance est le cœur du sujet. Voici, sans détour, ce que Bulle fait et ne fait pas.
      </p>

      <section className="mt-8" aria-labelledby="promesses">
        <h2 id="promesses" className="text-xl font-bold">
          Ce que nous promettons
        </h2>
        <ul className="mt-4 grid gap-3 sm:grid-cols-2" role="list">
          {PROMISES.map((p) => (
            <li key={p.t} className="card p-4">
              <div className="text-2xl" aria-hidden>
                {p.emoji}
              </div>
              <h3 className="mt-1 font-bold">{p.t}</h3>
              <p className="text-sm text-[var(--b-muted)]">{p.d}</p>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-10" aria-labelledby="sources">
        <h2 id="sources" className="text-xl font-bold">
          Nos sources
        </h2>
        <p className="mt-1 text-sm text-[var(--b-muted)]">
          Organismes publics, recherche clinique et ouvrages de référence. Consultées le {CONSULTED_ON}.
        </p>
        <ul className="mt-4 space-y-3" role="list">
          {sources.map((s) => (
            <li key={s.id} className="card p-4">
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <h3 className="font-bold">{s.org}</h3>
                <span className="rounded-full bg-[#f4f1ea] px-2.5 py-0.5 text-xs text-[var(--b-muted)]">
                  {s.kind} · {s.year}
                </span>
              </div>
              <p className="mt-1 text-sm text-[var(--b-ink)]/85">{s.ref}</p>
              <a
                href={s.url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-1 inline-block text-sm underline"
              >
                {s.url}
              </a>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-10" aria-labelledby="methode">
        <h2 id="methode" className="text-xl font-bold">
          Notre méthode
        </h2>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-[var(--b-ink)]/85">
          <li>Deux expériences distinctes&nbsp;: côté enfant ludique et rassurant, côté parent sobre et clair.</li>
          <li>Contenu adapté à l’âge (3-5, 6-8, 9-11 ans) et co-régulé&nbsp;: les rituels se font à deux.</li>
          <li>Aucune émotion « négative »&nbsp;: on accueille le ressenti, on encadre le comportement.</li>
          <li>Zéro conseil inventé&nbsp;: chaque fiche est reliée à une source datée et vérifiable.</li>
        </ul>
      </section>

      <section className="mt-10" aria-labelledby="rgpd">
        <h2 id="rgpd" className="text-xl font-bold">
          RGPD & protection des mineurs — cadre du MVP
        </h2>
        <div className="card mt-3 border-l-4 border-[var(--b-primary)] p-4 text-sm text-[var(--b-ink)]/85">
          <p>
            Ce MVP fonctionne avec des <strong>données de démonstration fictives</strong> et ne
            collecte <strong>aucune vraie donnée d’enfant</strong>.
          </p>
          <p className="mt-2">
            Les données d’enfants relèvent d’une protection renforcée. Avant toute mise en service
            avec de vraies données, sont requis&nbsp;: une <strong>AIPD/DPIA</strong> (analyse
            d’impact), le <strong>consentement parental</strong>, une <strong>base légale</strong>
            claire, et une conception « <strong>age-appropriate design</strong> » (minimisation,
            transparence, pas de profilage). Ce contenu est informatif et ne remplace pas l’avis
            d’un·e professionnel·le de santé.
          </p>
        </div>
      </section>

      <p className="mt-10 text-center">
        <Link href="/bulle" className="tap px-6" style={{ background: "var(--b-primary)", color: "#fff" }}>
          ← Revenir à l’accueil
        </Link>
      </p>
    </main>
  );
}
