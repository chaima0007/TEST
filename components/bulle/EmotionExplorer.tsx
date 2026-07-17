"use client";

import { useState } from "react";
import { emotionsForBand, type AgeBand, type Emotion } from "@/lib/bulle/emotions";
import SpeakButton from "./SpeakButton";

const BANDS: { key: AgeBand; label: string }[] = [
  { key: "3-5", label: "3 à 5 ans" },
  { key: "6-8", label: "6 à 8 ans" },
  { key: "9-11", label: "9 à 11 ans" },
];

export default function EmotionExplorer() {
  const [band, setBand] = useState<AgeBand>("6-8");
  const [open, setOpen] = useState<Emotion | null>(null);
  const list = emotionsForBand(band);

  return (
    <div>
      {/* Sélecteur d’âge — adapte les cartes proposées. */}
      <div className="flex flex-wrap items-center gap-2" role="group" aria-label="Choisir la tranche d’âge">
        <span className="text-sm text-[var(--b-muted)]">J’ai&nbsp;:</span>
        {BANDS.map((b) => (
          <button
            key={b.key}
            type="button"
            onClick={() => setBand(b.key)}
            aria-pressed={band === b.key}
            className="tap px-4 text-sm"
            style={
              band === b.key
                ? { background: "var(--b-primary)", color: "#fff" }
                : { background: "#fff", color: "var(--b-ink)", borderColor: "#e6e1d6" }
            }
          >
            {b.label}
          </button>
        ))}
      </div>

      <p className="mt-4 text-[var(--b-muted)]">
        Touche l’émotion qui ressemble le plus à ce que tu ressens. Il n’y a pas de mauvaise réponse&nbsp;💛
      </p>

      {/* Grille de cartes émotions. */}
      <ul className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4" role="list">
        {list.map((e) => (
          <li key={e.id}>
            <button
              type="button"
              onClick={() => setOpen(e)}
              className="tap w-full flex-col p-4 text-center"
              style={{ background: e.color, color: "#2b2440", minHeight: 128 }}
              aria-label={`Émotion : ${e.name}`}
            >
              <span className="text-5xl" aria-hidden>
                {e.emoji}
              </span>
              <span className="mt-2 text-lg font-bold">{e.name}</span>
            </button>
          </li>
        ))}
      </ul>

      {/* Détail de l’émotion sélectionnée. */}
      {open && (
        <div
          className="fixed inset-0 z-50 flex items-end justify-center bg-black/40 p-3 sm:items-center"
          role="dialog"
          aria-modal="true"
          aria-label={`À propos de l’émotion ${open.name}`}
          onClick={() => setOpen(null)}
        >
          <div
            className="card w-full max-w-lg p-5"
            onClick={(ev) => ev.stopPropagation()}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-3">
                <span className="text-5xl" aria-hidden>
                  {open.emoji}
                </span>
                <div>
                  <h2 className="text-2xl font-extrabold">{open.name}</h2>
                  <p className="text-[var(--b-muted)]">{open.reassurance}</p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setOpen(null)}
                className="tap px-3"
                style={{ background: "#f1ede4" }}
                aria-label="Fermer"
              >
                ✕
              </button>
            </div>

            <Section title="Dans mon corps, je sens…" items={open.body} />
            <Section title="Ça peut arriver quand…" items={open.when} />
            <Section title="Ce qui peut m’aider" items={open.help} highlight={open.color} />

            <div className="mt-4">
              <SpeakButton
                label="Écouter cette carte"
                text={`${open.name}. ${open.reassurance}. Ce qui peut m’aider : ${open.help.join(", ")}.`}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Section({
  title,
  items,
  highlight,
}: {
  title: string;
  items: string[];
  highlight?: string;
}) {
  return (
    <div className="mt-4">
      <h3 className="font-bold">{title}</h3>
      <ul className="mt-2 flex flex-wrap gap-2" role="list">
        {items.map((it) => (
          <li
            key={it}
            className="rounded-full px-3 py-1.5 text-sm"
            style={{ background: highlight ?? "#f4f1ea", color: "#2b2440" }}
          >
            {it}
          </li>
        ))}
      </ul>
    </div>
  );
}
