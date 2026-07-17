"use client";

import Link from "next/link";
import { useState } from "react";
import { CONSEILS, CATEGORIES, type ConseilCategory } from "@/lib/bulle/conseils";
import { getSource } from "@/lib/bulle/sources";

export default function ParentSpace() {
  const [cat, setCat] = useState<ConseilCategory | "tous">("tous");
  const list = cat === "tous" ? CONSEILS : CONSEILS.filter((c) => c.category === cat);

  return (
    <div>
      <div className="card p-5">
        <h1 className="text-2xl font-extrabold">Espace des parents</h1>
        <p className="mt-2 text-[var(--b-muted)]">
          Des repères courts et concrets, jamais moralisateurs. Chaque fiche renvoie à un organisme
          reconnu ou un ouvrage de référence, avec l’année.{" "}
          <strong>Informatif — ne remplace pas l’avis d’un professionnel.</strong>
        </p>
      </div>

      {/* Filtres par thème. */}
      <div className="mt-5 flex flex-wrap gap-2" role="group" aria-label="Filtrer par thème">
        <Chip active={cat === "tous"} onClick={() => setCat("tous")} label="Tout" emoji="✨" />
        {CATEGORIES.map((c) => (
          <Chip
            key={c.key}
            active={cat === c.key}
            onClick={() => setCat(c.key)}
            label={c.label}
            emoji={c.emoji}
          />
        ))}
      </div>

      <ul className="mt-5 grid gap-4 sm:grid-cols-2" role="list">
        {list.map((c) => {
          const s = getSource(c.sourceId);
          return (
            <li key={c.id} className="card flex flex-col p-5">
              <span className="text-xs font-semibold uppercase tracking-wide text-[var(--b-primary)]">
                {CATEGORIES.find((x) => x.key === c.category)?.label}
              </span>
              <h2 className="mt-1 text-lg font-bold">{c.title}</h2>
              <p className="mt-2 text-sm text-[var(--b-ink)]/85">{c.body}</p>
              <p className="mt-3 rounded-xl bg-[#f6f3ec] p-3 text-sm">
                <strong>À essayer&nbsp;:</strong> {c.tryThis}
              </p>
              <p className="mt-3 text-xs text-[var(--b-muted)]">
                Source&nbsp;:{" "}
                <a href={s.url} target="_blank" rel="noopener noreferrer" className="underline">
                  {s.org}
                </a>{" "}
                — {s.ref} ({s.year}).
              </p>
            </li>
          );
        })}
      </ul>

      <p className="mt-6 text-sm text-[var(--b-muted)]">
        <Link href="/bulle/promesses" className="underline">
          Voir toutes les sources, la méthode et notre engagement RGPD →
        </Link>
      </p>
    </div>
  );
}

function Chip({
  active,
  onClick,
  label,
  emoji,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  emoji: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className="tap px-4 text-sm"
      style={
        active
          ? { background: "var(--b-primary)", color: "#fff" }
          : { background: "#fff", color: "var(--b-ink)", borderColor: "#e6e1d6" }
      }
    >
      <span aria-hidden>{emoji}</span> {label}
    </button>
  );
}
