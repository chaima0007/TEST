import Link from "next/link";

export default function BulleHome() {
  return (
    <main>
      <div className="text-center">
        <div className="text-6xl" aria-hidden>
          🫧
        </div>
        <h1 className="mt-2 text-4xl font-extrabold tracking-tight sm:text-5xl">Bulle</h1>
        <p className="mx-auto mt-3 max-w-xl text-lg text-[var(--b-muted)]">
          Une bulle douce pour <strong>parler ensemble</strong> — nommer les émotions et désamorcer
          les conflits, à hauteur d’enfant.
        </p>
      </div>

      {/* Deux portes : côté enfant (ludique) et côté parent (portail parental). */}
      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        <Link
          href="/bulle/enfant"
          className="tap flex-col items-start p-6 text-left"
          style={{ background: "linear-gradient(135deg,#ffe1c4,#ffd0e0)", minHeight: 180 }}
        >
          <span className="text-5xl" aria-hidden>
            🧒
          </span>
          <span className="mt-3 text-2xl font-extrabold">Je suis l’enfant</span>
          <span className="mt-1 text-[var(--b-ink)]/80">
            Mes cartes émotions, mes rituels, mon coin calme.
          </span>
        </Link>

        <Link
          href="/bulle/parent"
          className="tap flex-col items-start p-6 text-left"
          style={{ background: "linear-gradient(135deg,#e7e0ff,#d4efe6)", minHeight: 180 }}
        >
          <span className="text-5xl" aria-hidden>
            🧑‍🍼
          </span>
          <span className="mt-3 text-2xl font-extrabold">Je suis le parent</span>
          <span className="mt-1 text-[var(--b-ink)]/80">
            Conseils sourcés (pédopsy & organismes officiels). Accès adulte.
          </span>
        </Link>
      </div>

      {/* Badges de confiance — le cœur du positionnement. */}
      <section className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-4" aria-label="Nos engagements">
        <Badge emoji="🙈" title="Aucune surveillance" text="On aide à parler, jamais à espionner l’enfant." />
        <Badge emoji="📵" title="Aucune collecte" text="Données de démo fictives. Rien n’est envoyé." />
        <Badge emoji="🚫" title="Ni pub ni tiers" text="Pas de publicité, pas de contact extérieur." />
        <Badge emoji="📚" title="Contenu sourcé" text="Chaque conseil cite un organisme reconnu et daté." />
      </section>

      <p className="mt-8 text-center text-sm text-[var(--b-muted)]">
        <Link href="/bulle/promesses" className="underline">
          Nos promesses, nos sources et notre méthode →
        </Link>
      </p>
    </main>
  );
}

function Badge({ emoji, title, text }: { emoji: string; title: string; text: string }) {
  return (
    <div className="card p-4">
      <div className="text-2xl" aria-hidden>
        {emoji}
      </div>
      <h2 className="mt-1 font-bold">{title}</h2>
      <p className="text-sm text-[var(--b-muted)]">{text}</p>
    </div>
  );
}
