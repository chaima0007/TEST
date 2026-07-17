"use client";

import { useState } from "react";
import { RITUALS, type Ritual, type StepWho } from "@/lib/bulle/rituels";
import SpeakButton from "./SpeakButton";

const WHO_LABEL: Record<StepWho, { label: string; emoji: string; bg: string }> = {
  ensemble: { label: "Ensemble", emoji: "👨‍👧", bg: "#e7e0ff" },
  parent: { label: "Le parent", emoji: "🫂", bg: "#dff3ea" },
  enfant: { label: "L’enfant", emoji: "🧒", bg: "#fde9d6" },
};

export default function RitualsScreen() {
  const [active, setActive] = useState<Ritual | null>(null);
  const [i, setI] = useState(0);

  if (active) {
    const step = active.steps[i];
    const who = WHO_LABEL[step.who];
    const isLast = i === active.steps.length - 1;
    return (
      <div>
        <button
          type="button"
          onClick={() => {
            setActive(null);
            setI(0);
          }}
          className="tap px-4 text-sm"
          style={{ background: "#fff", borderColor: "#e6e1d6" }}
        >
          ← Choisir un autre rituel
        </button>

        <div className="card mt-4 p-5" style={{ borderTop: `6px solid ${active.color}` }}>
          <div className="flex items-center justify-between gap-3">
            <h2 className="text-xl font-extrabold">
              <span aria-hidden>{active.emoji}</span> {active.title}
            </h2>
            <span className="text-sm text-[var(--b-muted)]">
              Étape {i + 1}/{active.steps.length}
            </span>
          </div>

          {/* Qui parle / qui fait — invite à se passer le téléphone. */}
          <div
            className="mt-4 inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-sm font-semibold"
            style={{ background: who.bg }}
          >
            <span aria-hidden>{who.emoji}</span> À {who.label}
          </div>

          <p className="mt-4 text-2xl font-semibold leading-snug">{step.text}</p>
          {step.hint && (
            <p className="mt-2 text-[var(--b-muted)]">💡 {step.hint}</p>
          )}

          <div className="mt-5 flex flex-wrap items-center gap-2">
            <SpeakButton text={step.text} />
            <div className="grow" />
            {i > 0 && (
              <button
                type="button"
                onClick={() => setI((n) => n - 1)}
                className="tap px-5"
                style={{ background: "#f1ede4" }}
              >
                Précédent
              </button>
            )}
            {!isLast ? (
              <button
                type="button"
                onClick={() => setI((n) => n + 1)}
                className="tap px-6"
                style={{ background: "var(--b-primary)", color: "#fff" }}
              >
                Suivant →
              </button>
            ) : (
              <button
                type="button"
                onClick={() => {
                  setActive(null);
                  setI(0);
                }}
                className="tap px-6"
                style={{ background: "#2fa574", color: "#fff" }}
              >
                Terminé 🎉
              </button>
            )}
          </div>

          {isLast && (
            <p className="mt-5 rounded-2xl p-4 text-center italic" style={{ background: active.color }}>
              « {active.closing} »
            </p>
          )}
        </div>
      </div>
    );
  }

  return (
    <ul className="grid gap-3 sm:grid-cols-2" role="list">
      {RITUALS.map((r) => (
        <li key={r.id}>
          <button
            type="button"
            onClick={() => {
              setActive(r);
              setI(0);
            }}
            className="tap w-full flex-col items-start p-5 text-left"
            style={{ background: "#fff", borderColor: "#efe9dd", minHeight: 132 }}
          >
            <div className="flex w-full items-center justify-between">
              <span className="text-3xl" aria-hidden>
                {r.emoji}
              </span>
              <span className="rounded-full bg-[#f4f1ea] px-3 py-1 text-xs text-[var(--b-muted)]">
                {r.durationMin} min · {r.bands[0].split("-")[0]}–
                {r.bands[r.bands.length - 1].split("-")[1]} ans
              </span>
            </div>
            <span className="mt-3 text-lg font-bold">{r.title}</span>
            <span className="mt-1 text-sm text-[var(--b-muted)]">{r.subtitle}</span>
          </button>
        </li>
      ))}
    </ul>
  );
}
