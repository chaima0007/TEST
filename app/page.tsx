"use client";

import Link from "next/link";
import { useApp } from "@/lib/store";
import { PageHeader, Section, Loading } from "@/components/ui";
import {
  AVAILABILITY_META,
  MOOD_EMOJI,
  ENERGY_LABEL,
  NEED_TYPES,
} from "@/lib/content";
import type { Availability } from "@/lib/types";
import { computeCycle } from "@/lib/cycle";
import { todayIso, formatLongDate, formatTime } from "@/lib/date";

export default function TodayPage() {
  const { ready, state, setCheckIn, addNeed, clearNeeds } = useApp();
  if (!ready) return <Loading />;

  const today = todayIso();
  const me = state.checkins.moi;
  const partner = state.checkins.partenaire;
  const partnerName = state.people.partenaire.name;
  const cycle = computeCycle(state.cycle, today);
  const myNeeds = state.needs.filter((n) => n.person === "moi");

  const availabilities: Availability[] = ["vert", "orange", "rouge"];

  // Rituel suggéré selon l'ambiance du jour.
  const suggested =
    me?.availability === "rouge" || partner?.availability === "rouge"
      ? {
          slug: "desamorcer-une-tension",
          emoji: "🕊️",
          title: "Désamorcer une tension",
          why: "L'un de vous a besoin d'espace aujourd'hui.",
        }
      : me?.availability === "vert" && partner?.availability === "vert"
        ? {
            slug: "bilan-hebdo",
            emoji: "🗓️",
            title: "Bilan de couple",
            why: "Vous êtes tous les deux ouverts — profitez-en pour faire le point.",
          }
        : {
            slug: "exprimer-une-limite",
            emoji: "🧭",
            title: "Exprimer une limite",
            why: "Un bon réflexe pour dire les choses en douceur.",
          };

  return (
    <div>
      <PageHeader
        eyebrow={formatLongDate(today)}
        title="Aujourd'hui"
        subtitle="Un petit point sur toi, et sur l'ambiance à deux."
      />

      {/* Mon check-in */}
      <Section title="Comment tu te sens ?">
        <div className="card">
          <p className="text-xs text-muted mb-2">Humeur</p>
          <div className="flex justify-between mb-4">
            {MOOD_EMOJI.map((emoji, i) => {
              const val = i + 1;
              const on = (me?.mood ?? 0) === val;
              return (
                <button
                  key={val}
                  onClick={() => setCheckIn("moi", { mood: val })}
                  aria-label={`Humeur ${val} sur 5`}
                  className="text-3xl transition-transform"
                  style={{
                    transform: on ? "scale(1.15)" : "scale(1)",
                    opacity: on || me?.mood == null ? 1 : 0.4,
                  }}
                >
                  {emoji}
                </button>
              );
            })}
          </div>

          <p className="text-xs text-muted mb-2">Énergie</p>
          <div className="seg mb-4" style={{ display: "flex" }}>
            {ENERGY_LABEL.map((label, i) => {
              const val = i + 1;
              return (
                <button
                  key={val}
                  data-on={me?.energy === val}
                  onClick={() => setCheckIn("moi", { energy: val })}
                  style={{ flex: 1 }}
                >
                  {label}
                </button>
              );
            })}
          </div>

          <p className="text-xs text-muted mb-2">Ma disponibilité (code couleur)</p>
          <div className="grid grid-cols-3 gap-2">
            {availabilities.map((a) => {
              const meta = AVAILABILITY_META[a];
              const on = me?.availability === a;
              return (
                <button
                  key={a}
                  onClick={() => setCheckIn("moi", { availability: a })}
                  className={`chip ${meta.className}`}
                  style={{
                    flexDirection: "column",
                    height: "auto",
                    padding: "0.6rem 0.3rem",
                    borderWidth: on ? 2 : 1,
                    fontWeight: on ? 800 : 600,
                    minWidth: 0,
                    whiteSpace: "normal",
                    textAlign: "center",
                    lineHeight: 1.15,
                  }}
                >
                  <span className="text-lg" aria-hidden>
                    {meta.emoji}
                  </span>
                  {meta.label}
                </button>
              );
            })}
          </div>
          {me?.availability ? (
            <p className="text-xs text-muted mt-2">
              {AVAILABILITY_META[me.availability].desc}
            </p>
          ) : (
            <p className="text-xs text-muted mt-2">
              Touche une couleur pour partager ton ambiance du jour.
            </p>
          )}

          <textarea
            className="mt-3"
            rows={2}
            placeholder="Un mot sur ta journée (facultatif)…"
            value={me?.note ?? ""}
            onChange={(e) => setCheckIn("moi", { note: e.target.value })}
          />
        </div>
      </Section>

      {/* Ambiance de l'autre */}
      <Section title={`L'ambiance de ${partnerName}`}>
        {partner ? (
          <div className="card">
            <div className="flex items-center gap-3">
              <span className="text-3xl" aria-hidden>
                {state.people.partenaire.emoji}
              </span>
              <div className="flex-1">
                <span
                  className={`chip ${AVAILABILITY_META[partner.availability].className}`}
                >
                  {AVAILABILITY_META[partner.availability].emoji}{" "}
                  {AVAILABILITY_META[partner.availability].label}
                </span>
              </div>
              <span className="text-2xl" aria-hidden>
                {MOOD_EMOJI[partner.mood - 1]}
              </span>
            </div>
            <p className="text-sm text-muted mt-2">
              {AVAILABILITY_META[partner.availability].desc}
            </p>
            {partner.note ? (
              <p className="text-sm mt-2 italic">« {partner.note} »</p>
            ) : null}
          </div>
        ) : (
          <div className="card text-sm text-muted">
            {partnerName} n&apos;a pas encore fait son point aujourd&apos;hui.
          </div>
        )}
      </Section>

      {/* Signaux « J'ai besoin de… » */}
      <Section
        title="J'ai besoin de…"
        action={
          myNeeds.length > 0 ? (
            <button className="btn btn-ghost btn-sm" onClick={() => clearNeeds("moi")}>
              Effacer
            </button>
          ) : null
        }
      >
        <div className="card">
          <p className="text-xs text-muted mb-3">
            Un tap suffit — pas besoin de trouver les mots.
          </p>
          <div className="grid grid-cols-4 gap-2">
            {NEED_TYPES.map((n) => {
              const active = myNeeds.some((x) => x.needId === n.id);
              return (
                <button
                  key={n.id}
                  onClick={() => addNeed("moi", n.id)}
                  title={n.hint}
                  className="flex flex-col items-center gap-1 rounded-2xl py-2 px-1 border text-center"
                  style={{
                    borderColor: active ? "var(--brand)" : "var(--line)",
                    background: active ? "var(--brand-soft)" : "var(--surface)",
                    minWidth: 0,
                  }}
                >
                  <span className="text-2xl" aria-hidden>
                    {n.emoji}
                  </span>
                  <span className="text-[0.62rem] font-semibold leading-tight">
                    {n.label}
                  </span>
                </button>
              );
            })}
          </div>
          {myNeeds.length > 0 ? (
            <p className="text-xs text-muted mt-3">
              Envoyé à {partnerName} :{" "}
              {myNeeds
                .map((n) => {
                  const t = NEED_TYPES.find((x) => x.id === n.needId);
                  return `${t?.emoji ?? ""} ${t?.label ?? ""} (${formatTime(n.at)})`;
                })
                .join(" · ")}
            </p>
          ) : null}
        </div>
      </Section>

      {/* Cycle du jour */}
      {cycle ? (
        <Section title="Le rythme du corps">
          <Link href="/reglages" className="card block">
            <div className="flex items-center gap-3">
              <span className="text-3xl" aria-hidden>
                {cycle.emoji}
              </span>
              <div className="flex-1">
                <p className="font-semibold">
                  {cycle.label} · jour {cycle.dayOfCycle}
                </p>
                <p className="text-xs text-muted">
                  {partnerName} · {cycle.energy}
                </p>
              </div>
            </div>
            <p className="text-sm mt-2">💡 {cycle.tips[0]}</p>
          </Link>
        </Section>
      ) : null}

      {/* Rituel suggéré */}
      <Section title="Le rituel du jour">
        <Link href={`/rituels/${suggested.slug}`} className="card block">
          <div className="flex items-center gap-3">
            <span className="text-3xl" aria-hidden>
              {suggested.emoji}
            </span>
            <div className="flex-1">
              <p className="font-semibold">{suggested.title}</p>
              <p className="text-xs text-muted">{suggested.why}</p>
            </div>
            <span className="text-brand text-xl" aria-hidden>
              →
            </span>
          </div>
        </Link>
      </Section>
    </div>
  );
}
