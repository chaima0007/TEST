"use client";

import { useState } from "react";
import { useApp } from "@/lib/store";
import { PageHeader, Section, Loading } from "@/components/ui";
import { SOURCES } from "@/lib/content";
import { computeCycle } from "@/lib/cycle";
import { todayIso } from "@/lib/date";
import type { PersonId } from "@/lib/types";

export default function ReglagesPage() {
  const { ready, state, setCycle, setName, reset } = useApp();
  const [confirmReset, setConfirmReset] = useState(false);

  if (!ready) return <Loading />;

  const { cycle, people } = state;
  const info = computeCycle(cycle, todayIso());

  return (
    <div>
      <PageHeader eyebrow="Réglages" title="Vous deux" subtitle="Personnalise l'app et gère tes données." />

      {/* Profils */}
      <Section title="Prénoms">
        <div className="card flex flex-col gap-3">
          {(Object.keys(people) as PersonId[]).map((p) => (
            <div key={p}>
              <label className="text-xs text-muted">
                {p === "moi" ? "Toi" : "Ton/ta partenaire"} {people[p].emoji}
              </label>
              <input
                value={people[p].name}
                onChange={(e) => setName(p, e.target.value)}
                maxLength={24}
              />
            </div>
          ))}
        </div>
      </Section>

      {/* Cycle */}
      <Section title="Rythme du corps (cycle)">
        <div className="card flex flex-col gap-3">
          <label className="flex items-center justify-between gap-3">
            <span className="text-sm">Suivre un cycle</span>
            <input
              type="checkbox"
              checked={cycle.enabled}
              onChange={(e) => setCycle({ enabled: e.target.checked })}
              style={{ width: "auto" }}
            />
          </label>

          {cycle.enabled ? (
            <>
              <div>
                <label className="text-xs text-muted">Pour qui ?</label>
                <select
                  value={cycle.person}
                  onChange={(e) => setCycle({ person: e.target.value as PersonId })}
                >
                  {(Object.keys(people) as PersonId[]).map((p) => (
                    <option key={p} value={p}>
                      {people[p].emoji} {people[p].name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-xs text-muted">Début des dernières règles</label>
                <input
                  type="date"
                  value={cycle.lastPeriodStart}
                  max={todayIso()}
                  onChange={(e) => setCycle({ lastPeriodStart: e.target.value })}
                />
              </div>

              <div className="flex gap-2">
                <div className="flex-1">
                  <label className="text-xs text-muted">Durée du cycle (j)</label>
                  <input
                    type="number"
                    min={20}
                    max={45}
                    value={cycle.cycleLength}
                    onChange={(e) =>
                      setCycle({ cycleLength: Number(e.target.value) })
                    }
                  />
                </div>
                <div className="flex-1">
                  <label className="text-xs text-muted">Durée des règles (j)</label>
                  <input
                    type="number"
                    min={2}
                    max={10}
                    value={cycle.periodLength}
                    onChange={(e) =>
                      setCycle({ periodLength: Number(e.target.value) })
                    }
                  />
                </div>
              </div>

              {info ? (
                <div
                  className="rounded-2xl p-3"
                  style={{ background: "var(--lilac-soft)" }}
                >
                  <p className="font-semibold text-sm">
                    {info.emoji} {info.label} · jour {info.dayOfCycle}
                  </p>
                  <p className="text-xs text-muted mt-1">{info.summary}</p>
                  <ul className="text-sm mt-2 flex flex-col gap-1">
                    {info.tips.map((t, i) => (
                      <li key={i}>💡 {t}</li>
                    ))}
                  </ul>
                </div>
              ) : null}

              <p className="text-xs text-muted">
                ⚠️ Information de bien-être, à titre indicatif. Ce n&apos;est ni un
                avis médical, ni une méthode de contraception.
              </p>
            </>
          ) : null}
        </div>
      </Section>

      {/* Confidentialité */}
      <Section title="Confidentialité">
        <div className="card">
          <p className="text-sm">
            🔒 <strong>Tout reste sur cet appareil.</strong> Tes données sont
            stockées localement, dans ton navigateur. Rien n&apos;est envoyé à un
            serveur, aucun compte n&apos;est requis.
          </p>
          <p className="text-xs text-muted mt-2">
            Vider les données du navigateur effacera aussi le contenu de l&apos;app.
          </p>
        </div>
      </Section>

      {/* Sources */}
      <Section title="Sur quoi ça repose">
        <div className="card">
          <ul className="flex flex-col gap-3">
            {SOURCES.map((s) => (
              <li key={s.key}>
                <p className="text-sm font-semibold">{s.label}</p>
                <p className="text-xs text-muted">{s.detail}</p>
              </li>
            ))}
          </ul>
        </div>
      </Section>

      {/* Données de démo */}
      <Section title="Données">
        <div className="card">
          {!confirmReset ? (
            <button className="btn btn-ghost" onClick={() => setConfirmReset(true)}>
              Réinitialiser les données de démo
            </button>
          ) : (
            <div className="flex flex-col gap-2">
              <p className="text-sm">
                Effacer tes modifications et recharger la démo fictive ?
              </p>
              <div className="flex gap-2">
                <button
                  className="btn btn-primary btn-sm"
                  onClick={() => {
                    reset();
                    setConfirmReset(false);
                  }}
                >
                  Oui, réinitialiser
                </button>
                <button
                  className="btn btn-ghost btn-sm"
                  onClick={() => setConfirmReset(false)}
                >
                  Annuler
                </button>
              </div>
            </div>
          )}
          <p className="text-xs text-muted mt-3">
            Les données pré-remplies (Alex, ses limites, ses allergies…) sont
            <strong> fictives</strong> et servent uniquement à la démonstration.
          </p>
        </div>
      </Section>

      <p className="text-center text-xs text-muted mt-6 mb-2">
        Nous · prototype local — fait avec soin 🤍
      </p>
    </div>
  );
}
