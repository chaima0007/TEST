"use client";

import { use, useMemo, useState } from "react";
import Link from "next/link";
import { getRitual } from "@/lib/rituals";

export default function RitualPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = use(params);
  const ritual = getRitual(slug);

  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [copied, setCopied] = useState(false);

  const summary = useMemo(() => {
    if (!ritual?.summaryTemplate) return "";
    const arr = ritual.steps.map((_, i) => answers[i] ?? "");
    return ritual.summaryTemplate(arr);
  }, [ritual, answers]);

  if (!ritual) {
    return (
      <div className="px-5 pt-16 text-center">
        <p className="text-4xl mb-2" aria-hidden>
          🤷
        </p>
        <p className="text-muted mb-4">Ce rituel n&apos;existe pas.</p>
        <Link href="/rituels" className="btn btn-ghost">
          Retour aux rituels
        </Link>
      </div>
    );
  }

  const total = ritual.steps.length;
  const isLast = step === total - 1;
  const current = ritual.steps[step];

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(summary);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      /* clipboard indisponible */
    }
  };

  return (
    <div>
      <header className="px-5 pt-6 pb-2">
        <Link href="/rituels" className="text-sm text-muted">
          ← Rituels
        </Link>
        <div className="flex items-center gap-3 mt-3">
          <span className="text-4xl" aria-hidden>
            {ritual.emoji}
          </span>
          <div>
            <h1 className="text-xl font-bold">{ritual.title}</h1>
            <p className="text-xs text-muted">
              {ritual.duration} · 📚 {ritual.sourceLabel}
            </p>
          </div>
        </div>
        <p className="text-sm text-muted mt-3">{ritual.intro}</p>
      </header>

      {/* Progression */}
      <div className="px-5 mt-2">
        <div
          className="h-1.5 rounded-full overflow-hidden"
          style={{ background: "var(--line)" }}
        >
          <div
            className="h-full rounded-full transition-all"
            style={{
              width: `${((step + 1) / total) * 100}%`,
              background: "var(--brand)",
            }}
          />
        </div>
        <p className="text-xs text-muted mt-1">
          Étape {step + 1} / {total}
        </p>
      </div>

      {/* Étape courante */}
      <div className="px-4 mt-3">
        <div className="card">
          <p className="eyebrow mb-1">{current.title}</p>
          <p className="text-[0.95rem] mb-3">{current.prompt}</p>

          {current.examples ? (
            <ul className="text-xs text-muted mb-3 flex flex-col gap-1">
              {current.examples.map((ex, i) => (
                <li key={i}>· {ex}</li>
              ))}
            </ul>
          ) : null}

          {current.placeholder ? (
            <textarea
              rows={3}
              placeholder={current.placeholder}
              value={answers[step] ?? ""}
              onChange={(e) =>
                setAnswers((a) => ({ ...a, [step]: e.target.value }))
              }
            />
          ) : null}
        </div>

        {/* Message assemblé (dernière étape) */}
        {isLast && ritual.summaryTemplate && summary ? (
          <div
            className="rounded-2xl p-3 mt-3"
            style={{ background: "var(--lilac-soft)" }}
          >
            <p className="eyebrow mb-1">Ton message</p>
            <p className="text-sm leading-relaxed">💬 {summary}</p>
            <button className="btn btn-ghost btn-sm mt-2" onClick={copy}>
              {copied ? "Copié ✓" : "Copier"}
            </button>
          </div>
        ) : null}

        {/* Navigation */}
        <div className="flex gap-2 mt-4">
          {step > 0 ? (
            <button
              className="btn btn-ghost"
              onClick={() => setStep((s) => s - 1)}
            >
              Précédent
            </button>
          ) : null}
          {!isLast ? (
            <button
              className="btn btn-primary"
              onClick={() => setStep((s) => s + 1)}
            >
              Suivant
            </button>
          ) : (
            <Link href="/rituels" className="btn btn-primary">
              Terminer
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
