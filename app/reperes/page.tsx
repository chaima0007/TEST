"use client";

import { useState } from "react";
import { useApp } from "@/lib/store";
import { PageHeader, Section, Loading } from "@/components/ui";
import {
  CONSENT_AREAS,
  LIMIT_META,
  SEVERITY_META,
} from "@/lib/content";
import type {
  LimitLevel,
  PersonId,
  Sensitivity,
  SensitivityKind,
  Severity,
} from "@/lib/types";

const KIND_META: Record<SensitivityKind, { emoji: string; label: string }> = {
  allergie: { emoji: "⚠️", label: "Allergie" },
  intolerance: { emoji: "🍽️", label: "Intolérance" },
  sensorielle: { emoji: "🎧", label: "Sensorielle" },
  sujet: { emoji: "🚧", label: "Sujet sensible" },
};

export default function ReperesPage() {
  const {
    ready,
    state,
    addLimit,
    updateLimit,
    removeLimit,
    addSensitivity,
    removeSensitivity,
  } = useApp();
  const [person, setPerson] = useState<PersonId>("partenaire");

  if (!ready) return <Loading />;

  const people = state.people;
  const limits = state.limits.filter((l) => l.person === person);
  const sensitivities = state.sensitivities.filter((s) => s.person === person);

  return (
    <div>
      <PageHeader
        eyebrow="Comprendre l'autre"
        title="Repères"
        subtitle="Les limites, les oui, et les sensibilités de chacun — au même endroit."
      />

      {/* Sélecteur de personne */}
      <div className="px-4">
        <div className="seg" style={{ display: "flex", width: "100%" }}>
          {(Object.keys(people) as PersonId[]).map((p) => (
            <button
              key={p}
              data-on={person === p}
              onClick={() => setPerson(p)}
              style={{ flex: 1 }}
            >
              {people[p].emoji} {people[p].name}
            </button>
          ))}
        </div>
      </div>

      {/* Carte des limites */}
      <Section title="Carte des limites & consentement">
        <div className="flex flex-col gap-3">
          {CONSENT_AREAS.map((area) => {
            const items = limits.filter((l) => l.area === area.id);
            return (
              <div key={area.id} className="card">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xl" aria-hidden>
                    {area.emoji}
                  </span>
                  <h3 className="font-semibold text-sm flex-1">{area.label}</h3>
                </div>

                {items.length > 0 ? (
                  <ul className="flex flex-col gap-2 mb-2">
                    {items.map((l) => (
                      <li
                        key={l.id}
                        className="flex items-start gap-2 border-t pt-2"
                        style={{ borderColor: "var(--line)" }}
                      >
                        <div className="flex-1">
                          <p className="text-sm font-medium">{l.item}</p>
                          {l.note ? (
                            <p className="text-xs text-muted">{l.note}</p>
                          ) : null}
                        </div>
                        <LevelToggle
                          value={l.level}
                          onChange={(level) => updateLimit(l.id, { level })}
                        />
                        <button
                          aria-label="Supprimer"
                          onClick={() => removeLimit(l.id)}
                          className="text-muted text-sm px-1"
                        >
                          ✕
                        </button>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-xs text-muted mb-2">
                    Rien de noté ici pour l&apos;instant.
                  </p>
                )}

                <AddLimit
                  suggestions={area.examples}
                  onAdd={(item, level, note) =>
                    addLimit({ person, area: area.id, item, level, note })
                  }
                />
              </div>
            );
          })}
        </div>
      </Section>

      {/* Allergies & sensibilités */}
      <Section title="Allergies & sensibilités">
        <div className="card">
          {sensitivities.length > 0 ? (
            <ul className="flex flex-col gap-2 mb-3">
              {sensitivities.map((s) => (
                <li key={s.id} className="flex items-start gap-2">
                  <span className="text-lg" aria-hidden>
                    {KIND_META[s.kind].emoji}
                  </span>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{s.label}</p>
                    {s.note ? <p className="text-xs text-muted">{s.note}</p> : null}
                  </div>
                  <span className={`chip ${SEVERITY_META[s.severity].className}`}>
                    {SEVERITY_META[s.severity].label}
                  </span>
                  <button
                    aria-label="Supprimer"
                    onClick={() => removeSensitivity(s.id)}
                    className="text-muted text-sm px-1"
                  >
                    ✕
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-muted mb-3">
              Aucune sensibilité notée pour {people[person].name}.
            </p>
          )}
          <AddSensitivity
            onAdd={(entry) => addSensitivity({ ...entry, person })}
          />
        </div>
      </Section>

      <p className="text-xs text-muted px-6 mt-4">
        Ces repères se remplissent à deux, petit à petit. Ils se discutent — ils
        ne remplacent pas une conversation.
      </p>
    </div>
  );
}

function LevelToggle({
  value,
  onChange,
}: {
  value: LimitLevel;
  onChange: (v: LimitLevel) => void;
}) {
  const order: LimitLevel[] = ["oui", "peut-etre", "non"];
  return (
    <button
      onClick={() => onChange(order[(order.indexOf(value) + 1) % order.length])}
      className={`chip ${LIMIT_META[value].className}`}
      title="Changer le niveau"
    >
      {LIMIT_META[value].emoji} {LIMIT_META[value].label}
    </button>
  );
}

function AddLimit({
  suggestions,
  onAdd,
}: {
  suggestions: string[];
  onAdd: (item: string, level: LimitLevel, note?: string) => void;
}) {
  const [open, setOpen] = useState(false);
  const [item, setItem] = useState("");
  const [level, setLevel] = useState<LimitLevel>("peut-etre");
  const [note, setNote] = useState("");

  if (!open) {
    return (
      <button className="btn btn-ghost btn-sm" onClick={() => setOpen(true)}>
        + Ajouter
      </button>
    );
  }

  const submit = () => {
    if (!item.trim()) return;
    onAdd(item.trim(), level, note.trim() || undefined);
    setItem("");
    setNote("");
    setLevel("peut-etre");
    setOpen(false);
  };

  return (
    <div className="flex flex-col gap-2 mt-1">
      <div className="flex flex-wrap gap-1">
        {suggestions.map((s) => (
          <button
            key={s}
            className="chip"
            onClick={() => setItem(s)}
            style={{ fontWeight: 500 }}
          >
            {s}
          </button>
        ))}
      </div>
      <input
        placeholder="Ce dont on parle…"
        value={item}
        onChange={(e) => setItem(e.target.value)}
      />
      <div className="seg" style={{ display: "flex" }}>
        {(["oui", "peut-etre", "non"] as LimitLevel[]).map((lv) => (
          <button
            key={lv}
            data-on={level === lv}
            onClick={() => setLevel(lv)}
            style={{ flex: 1 }}
          >
            {LIMIT_META[lv].emoji} {LIMIT_META[lv].label}
          </button>
        ))}
      </div>
      <input
        placeholder="Précision (facultatif)…"
        value={note}
        onChange={(e) => setNote(e.target.value)}
      />
      <div className="flex gap-2">
        <button className="btn btn-primary btn-sm" onClick={submit}>
          Enregistrer
        </button>
        <button className="btn btn-ghost btn-sm" onClick={() => setOpen(false)}>
          Annuler
        </button>
      </div>
    </div>
  );
}

function AddSensitivity({
  onAdd,
}: {
  onAdd: (entry: Omit<Sensitivity, "id" | "person">) => void;
}) {
  const [open, setOpen] = useState(false);
  const [kind, setKind] = useState<SensitivityKind>("allergie");
  const [label, setLabel] = useState("");
  const [severity, setSeverity] = useState<Severity>("moyen");
  const [note, setNote] = useState("");

  if (!open) {
    return (
      <button className="btn btn-ghost btn-sm" onClick={() => setOpen(true)}>
        + Ajouter une sensibilité
      </button>
    );
  }

  const submit = () => {
    if (!label.trim()) return;
    onAdd({ kind, label: label.trim(), severity, note: note.trim() || undefined });
    setLabel("");
    setNote("");
    setKind("allergie");
    setSeverity("moyen");
    setOpen(false);
  };

  return (
    <div className="flex flex-col gap-2">
      <select value={kind} onChange={(e) => setKind(e.target.value as SensitivityKind)}>
        {(Object.keys(KIND_META) as SensitivityKind[]).map((k) => (
          <option key={k} value={k}>
            {KIND_META[k].emoji} {KIND_META[k].label}
          </option>
        ))}
      </select>
      <input
        placeholder="Quoi ? (ex : arachides, bruit fort…)"
        value={label}
        onChange={(e) => setLabel(e.target.value)}
      />
      <div className="seg" style={{ display: "flex" }}>
        {(["leger", "moyen", "fort"] as Severity[]).map((sv) => (
          <button
            key={sv}
            data-on={severity === sv}
            onClick={() => setSeverity(sv)}
            style={{ flex: 1 }}
          >
            {SEVERITY_META[sv].label}
          </button>
        ))}
      </div>
      <input
        placeholder="Précision (facultatif)…"
        value={note}
        onChange={(e) => setNote(e.target.value)}
      />
      <div className="flex gap-2">
        <button className="btn btn-primary btn-sm" onClick={submit}>
          Enregistrer
        </button>
        <button className="btn btn-ghost btn-sm" onClick={() => setOpen(false)}>
          Annuler
        </button>
      </div>
    </div>
  );
}
