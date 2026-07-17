"use client";

import { useState } from "react";
import Link from "next/link";
import { PageHeader, Section } from "@/components/ui";
import { RITUALS } from "@/lib/rituals";
import { FEELINGS, NEEDS, assembleNvc } from "@/lib/nvc";

export default function RituelsPage() {
  return (
    <div>
      <PageHeader
        eyebrow="Mieux se parler"
        title="Rituels"
        subtitle="Des façons de dire les choses, inspirées d'approches reconnues."
      />

      <Section title="Traducteur — dire en douceur">
        <Translator />
      </Section>

      <Section title="Les rituels guidés">
        <div className="flex flex-col gap-3">
          {RITUALS.map((r) => (
            <Link key={r.slug} href={`/rituels/${r.slug}`} className="card block">
              <div className="flex items-center gap-3">
                <span className="text-3xl" aria-hidden>
                  {r.emoji}
                </span>
                <div className="flex-1">
                  <p className="font-semibold">{r.title}</p>
                  <p className="text-xs text-muted">{r.tagline}</p>
                </div>
                <div className="text-right">
                  <span className="text-brand text-xl" aria-hidden>
                    →
                  </span>
                  <p className="text-[0.65rem] text-muted mt-1">{r.duration}</p>
                </div>
              </div>
              <p className="text-[0.65rem] text-muted mt-2">📚 {r.sourceLabel}</p>
            </Link>
          ))}
        </div>
      </Section>

      <p className="text-xs text-muted px-6 mt-4">
        Ces rituels sont des outils de dialogue, pas un substitut à un
        accompagnement (thérapie de couple, professionnel de santé) quand c&apos;est
        nécessaire.
      </p>
    </div>
  );
}

function Translator() {
  const [observation, setObservation] = useState("");
  const [feeling, setFeeling] = useState<string | undefined>();
  const [need, setNeed] = useState<string | undefined>();
  const [request, setRequest] = useState("");
  const [copied, setCopied] = useState(false);

  const message = assembleNvc({ observation, feeling, need, request });

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(message);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      /* clipboard indisponible */
    }
  };

  return (
    <div className="card flex flex-col gap-3">
      <p className="text-xs text-muted">
        Transforme un ressenti brut en un message en « je », selon le modèle
        OSBD de la CNV.
      </p>

      <div>
        <label className="text-xs text-muted">La situation (les faits)</label>
        <input
          placeholder="tu as annulé notre soirée à la dernière minute…"
          value={observation}
          onChange={(e) => setObservation(e.target.value)}
        />
      </div>

      <div>
        <label className="text-xs text-muted">Je me sens…</label>
        <div className="flex flex-wrap gap-1 mt-1">
          {FEELINGS.map((f) => (
            <button
              key={f}
              className="chip"
              onClick={() => setFeeling(feeling === f ? undefined : f)}
              style={{
                borderColor: feeling === f ? "var(--brand)" : "var(--line)",
                background: feeling === f ? "var(--brand-soft)" : "var(--surface)",
                fontWeight: 500,
              }}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="text-xs text-muted">…parce que j&apos;ai besoin…</label>
        <div className="flex flex-wrap gap-1 mt-1">
          {NEEDS.map((n) => (
            <button
              key={n}
              className="chip"
              onClick={() => setNeed(need === n ? undefined : n)}
              style={{
                borderColor: need === n ? "var(--brand)" : "var(--line)",
                background: need === n ? "var(--brand-soft)" : "var(--surface)",
                fontWeight: 500,
              }}
            >
              {n}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="text-xs text-muted">Ma demande (facultatif)</label>
        <input
          placeholder="qu'on se prévienne à l'avance la prochaine fois"
          value={request}
          onChange={(e) => setRequest(e.target.value)}
        />
      </div>

      {message ? (
        <div
          className="rounded-2xl p-3"
          style={{ background: "var(--lilac-soft)", color: "var(--foreground)" }}
        >
          <p className="text-sm leading-relaxed">💬 {message}</p>
          <button className="btn btn-ghost btn-sm mt-2" onClick={copy}>
            {copied ? "Copié ✓" : "Copier le message"}
          </button>
        </div>
      ) : (
        <p className="text-xs text-muted">
          Choisis un ressenti et un besoin pour voir le message se construire.
        </p>
      )}
    </div>
  );
}
