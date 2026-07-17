import Link from "next/link";
import BulleHeader from "@/components/bulle/BulleHeader";

const TILES = [
  {
    href: "/bulle/enfant/emotions",
    emoji: "🃏",
    title: "Mes émotions",
    text: "Trouver le mot pour ce que je ressens.",
    bg: "linear-gradient(135deg,#ffe59a,#ffc7a8)",
  },
  {
    href: "/bulle/enfant/rituels",
    emoji: "🪄",
    title: "Nos rituels",
    text: "Des petits jeux pour parler avec papa ou maman.",
    bg: "linear-gradient(135deg,#c9c2ec,#b9d4f1)",
  },
  {
    href: "/bulle/enfant/calme",
    emoji: "🎈",
    title: "Mon coin calme",
    text: "Respirer et redevenir tranquille.",
    bg: "linear-gradient(135deg,#b6e3d4,#d6e5a3)",
  },
];

export default function EnfantHome() {
  return (
    <main>
      <BulleHeader />
      <h1 className="text-3xl font-extrabold">Coucou&nbsp;! Qu’est-ce qu’on fait&nbsp;?</h1>
      <p className="mt-2 text-[var(--b-muted)]">Touche une grande carte pour commencer.</p>

      <div className="mt-6 grid gap-4 sm:grid-cols-3">
        {TILES.map((t) => (
          <Link
            key={t.href}
            href={t.href}
            className="tap flex-col items-start p-6 text-left"
            style={{ background: t.bg, minHeight: 180 }}
          >
            <span className="text-5xl" aria-hidden>
              {t.emoji}
            </span>
            <span className="mt-3 text-2xl font-extrabold">{t.title}</span>
            <span className="mt-1 text-[var(--b-ink)]/80">{t.text}</span>
          </Link>
        ))}
      </div>
    </main>
  );
}
