"use client";

import { useState } from "react";

const GROUNDING = [
  { n: 5, sense: "choses que je peux VOIR", emoji: "👀" },
  { n: 4, sense: "choses que je peux TOUCHER", emoji: "✋" },
  { n: 3, sense: "sons que je peux ENTENDRE", emoji: "👂" },
  { n: 2, sense: "odeurs que je peux SENTIR", emoji: "👃" },
  { n: 1, sense: "chose que j’aime chez moi", emoji: "💛" },
];

export default function CalmTools() {
  const [tool, setTool] = useState<"respire" | "ancrage">("respire");

  return (
    <div>
      <div className="flex gap-2" role="tablist" aria-label="Outils pour se calmer">
        <button
          type="button"
          role="tab"
          aria-selected={tool === "respire"}
          onClick={() => setTool("respire")}
          className="tap px-5"
          style={tool === "respire" ? tabOn : tabOff}
        >
          🎈 Respirer
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={tool === "ancrage"}
          onClick={() => setTool("ancrage")}
          className="tap px-5"
          style={tool === "ancrage" ? tabOn : tabOff}
        >
          🌈 5-4-3-2-1
        </button>
      </div>

      {tool === "respire" ? (
        <div className="card mt-4 flex flex-col items-center p-8 text-center">
          <div
            className="breathe flex h-48 w-48 items-center justify-center rounded-full text-lg font-bold"
            style={{ background: "radial-gradient(circle, #b6e3d4, #6d5ae6)", color: "#fff" }}
            aria-hidden
          >
            Souffle…
          </div>
          <p className="mt-6 max-w-sm text-lg">
            Regarde le ballon. Quand il grandit, j’inspire par le nez. Quand il rétrécit, je souffle
            tout doucement par la bouche.
          </p>
          <p className="mt-2 text-[var(--b-muted)]">On le fait ensemble, 3 fois. Pas de chrono, pas de pression.</p>
        </div>
      ) : (
        <div className="card mt-4 p-6">
          <p className="text-lg">Pour revenir au calme, je cherche autour de moi&nbsp;:</p>
          <ul className="mt-4 space-y-3" role="list">
            {GROUNDING.map((g) => (
              <li
                key={g.n}
                className="flex items-center gap-4 rounded-2xl p-3"
                style={{ background: "#f6f3ec" }}
              >
                <span
                  className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full text-xl font-extrabold"
                  style={{ background: "#e7e0ff", color: "#4b3fb0" }}
                >
                  {g.n}
                </span>
                <span className="text-lg">
                  <span aria-hidden>{g.emoji} </span>
                  {g.sense}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

const tabOn = { background: "var(--b-primary)", color: "#fff" } as const;
const tabOff = { background: "#fff", color: "var(--b-ink)", borderColor: "#e6e1d6" } as const;
