"use client";

import { useState, type FormEvent, type ReactNode } from "react";

/**
 * Portail parental ("parental gate") — pratique standard des apps enfants
 * (recommandations Apple Kids / Google Families) : on demande une opération
 * de calcul qu’un jeune enfant ne fait pas seul, pour confirmer qu’un adulte
 * est présent avant d’ouvrir l’espace parent.
 *
 * Confidentialité : aucune donnée n’est stockée ni envoyée. Le résultat n’est
 * qu’un état d’affichage en mémoire. Ce n’est pas une mesure de sécurité forte,
 * seulement une barrière d’attention adaptée aux enfants.
 */

// Nombres fixes (pas de Math.random pour rester déterministe / testable).
const A = 7;
const B = 8;

export default function ParentalGate({ children }: { children: ReactNode }) {
  const [ok, setOk] = useState(false);
  const [value, setValue] = useState("");
  const [error, setError] = useState(false);

  if (ok) return <>{children}</>;

  function submit(e: FormEvent) {
    e.preventDefault();
    if (value.trim() === String(A * B)) {
      setOk(true);
    } else {
      setError(true);
    }
  }

  return (
    <div className="card mx-auto max-w-md p-6 text-center">
      <div className="text-4xl" aria-hidden>
        🔒
      </div>
      <h1 className="mt-2 text-2xl font-extrabold">Espace des parents</h1>
      <p className="mt-2 text-[var(--b-muted)]">
        Cet espace contient des informations pour les adultes. Pour continuer, réponds à cette petite
        question&nbsp;:
      </p>

      <form onSubmit={submit} className="mt-5">
        <label htmlFor="gate" className="block text-lg font-semibold">
          Combien font {A} × {B} ?
        </label>
        <input
          id="gate"
          inputMode="numeric"
          autoComplete="off"
          value={value}
          onChange={(e) => {
            setValue(e.target.value);
            setError(false);
          }}
          className="mt-3 w-40 rounded-xl border-2 border-[#e0dae9] px-4 py-3 text-center text-xl"
          aria-invalid={error}
          aria-describedby={error ? "gate-err" : undefined}
        />
        {error && (
          <p id="gate-err" className="mt-2 text-sm text-[#c0392b]" role="alert">
            Ce n’est pas le bon nombre. Réessaie.
          </p>
        )}
        <div className="mt-4">
          <button
            type="submit"
            className="tap px-6"
            style={{ background: "var(--b-primary)", color: "#fff" }}
          >
            Entrer
          </button>
        </div>
      </form>
    </div>
  );
}
