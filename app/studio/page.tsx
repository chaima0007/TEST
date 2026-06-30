"use client";

import { useCallback, useMemo, useRef, useState } from "react";
import {
  DMC_PALETTE,
  SYMBOLS,
  nearestThreadIndex,
  type Thread,
} from "@/lib/palette";

const FREE_MAX_COLS = 50; // au-delà = offre payante
const CELL = 16; // px par maille à l'écran

interface UsedThread extends Thread {
  index: number; // index palette
  symbol: string;
  count: number;
}

interface Pattern {
  cols: number;
  rows: number;
  grid: number[]; // index palette, ligne par ligne
  used: UsedThread[];
  symbolByIndex: Record<number, string>;
}

export default function StudioPage() {
  const [imgEl, setImgEl] = useState<HTMLImageElement | null>(null);
  const [cols, setCols] = useState(40);
  const [showSymbols, setShowSymbols] = useState(true);
  const [pattern, setPattern] = useState<Pattern | null>(null);
  const [premium, setPremium] = useState(false);
  const [showPaywall, setShowPaywall] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const loadFile = useCallback((file: File) => {
    if (!file.type.startsWith("image/")) return;
    const reader = new FileReader();
    reader.onload = () => {
      const img = new Image();
      img.onload = () => {
        setImgEl(img);
        setPattern(null);
      };
      img.src = reader.result as string;
    };
    reader.readAsDataURL(file);
  }, []);

  const draw = useCallback(
    (p: Pattern, symbols: boolean, isPremium: boolean) => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;
      const W = p.cols * CELL;
      const H = p.rows * CELL;
      canvas.width = W;
      canvas.height = H;

      // Cases colorées
      for (let y = 0; y < p.rows; y++) {
        for (let x = 0; x < p.cols; x++) {
          const idx = p.grid[y * p.cols + x];
          ctx.fillStyle = DMC_PALETTE[idx].hex;
          ctx.fillRect(x * CELL, y * CELL, CELL, CELL);
        }
      }

      // Symboles
      if (symbols) {
        ctx.font = `${CELL - 5}px monospace`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        for (let y = 0; y < p.rows; y++) {
          for (let x = 0; x < p.cols; x++) {
            const idx = p.grid[y * p.cols + x];
            const [r, g, b] = hexRgb(DMC_PALETTE[idx].hex);
            const lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
            ctx.fillStyle = lum > 0.55 ? "#333" : "#eee";
            ctx.fillText(
              p.symbolByIndex[idx],
              x * CELL + CELL / 2,
              y * CELL + CELL / 2 + 1,
            );
          }
        }
      }

      // Grille fine + lignes maîtresses tous les 10
      ctx.lineWidth = 1;
      for (let x = 0; x <= p.cols; x++) {
        ctx.strokeStyle = x % 10 === 0 ? "#1e293b" : "rgba(0,0,0,0.18)";
        ctx.beginPath();
        ctx.moveTo(x * CELL + 0.5, 0);
        ctx.lineTo(x * CELL + 0.5, H);
        ctx.stroke();
      }
      for (let y = 0; y <= p.rows; y++) {
        ctx.strokeStyle = y % 10 === 0 ? "#1e293b" : "rgba(0,0,0,0.18)";
        ctx.beginPath();
        ctx.moveTo(0, y * CELL + 0.5);
        ctx.lineTo(W, y * CELL + 0.5);
        ctx.stroke();
      }

      // Filigrane si non-premium
      if (!isPremium) {
        ctx.save();
        ctx.font = `bold ${Math.max(18, W / 16)}px sans-serif`;
        ctx.fillStyle = "rgba(15,23,42,0.18)";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.translate(W / 2, H / 2);
        ctx.rotate(-Math.PI / 8);
        ctx.fillText("MOTIF STUDIO — aperçu", 0, 0);
        ctx.restore();
      }
    },
    [],
  );

  const generate = useCallback(() => {
    if (!imgEl) return;
    if (cols > FREE_MAX_COLS && !premium) {
      setShowPaywall(true);
      return;
    }
    const ratio = imgEl.height / imgEl.width;
    const rows = Math.max(1, Math.round(cols * ratio));

    // Réduction de l'image à la résolution de la grille.
    const tmp = document.createElement("canvas");
    tmp.width = cols;
    tmp.height = rows;
    const tctx = tmp.getContext("2d", { willReadFrequently: true });
    if (!tctx) return;
    tctx.drawImage(imgEl, 0, 0, cols, rows);
    const data = tctx.getImageData(0, 0, cols, rows).data;

    const grid: number[] = new Array(cols * rows);
    const counts: Record<number, number> = {};
    for (let i = 0; i < cols * rows; i++) {
      const r = data[i * 4];
      const g = data[i * 4 + 1];
      const b = data[i * 4 + 2];
      const idx = nearestThreadIndex(r, g, b);
      grid[i] = idx;
      counts[idx] = (counts[idx] || 0) + 1;
    }

    const usedIdx = Object.keys(counts)
      .map(Number)
      .sort((a, b) => counts[b] - counts[a]);

    const symbolByIndex: Record<number, string> = {};
    const used: UsedThread[] = usedIdx.map((idx, i) => {
      const symbol = SYMBOLS[i % SYMBOLS.length];
      symbolByIndex[idx] = symbol;
      return { ...DMC_PALETTE[idx], index: idx, symbol, count: counts[idx] };
    });

    const next: Pattern = { cols, rows, grid, used, symbolByIndex };
    setPattern(next);
    requestAnimationFrame(() => draw(next, showSymbols, premium));
  }, [imgEl, cols, premium, showSymbols, draw]);

  const toggleSymbols = () => {
    const next = !showSymbols;
    setShowSymbols(next);
    if (pattern) draw(pattern, next, premium);
  };

  const exportPng = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const a = document.createElement("a");
    a.download = "motif-studio-patron.png";
    a.href = canvas.toDataURL("image/png");
    a.click();
  };

  const unlock = () => {
    // MVP : on simule l'achat. En prod, ce bouton ouvre Stripe/Lemon Squeezy
    // et le retour de paiement positionne premium=true.
    setPremium(true);
    setShowPaywall(false);
    if (pattern) draw(pattern, showSymbols, true);
  };

  const stats = useMemo(() => {
    if (!pattern) return null;
    return {
      total: pattern.cols * pattern.rows,
      colors: pattern.used.length,
      dims: `${pattern.cols} × ${pattern.rows} mailles`,
    };
  }, [pattern]);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* Header */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <span className="text-xl">🧵</span>
            <span className="text-lg font-bold tracking-tight">
              Motif Studio
            </span>
            <span className="ml-2 rounded-full bg-indigo-100 px-2 py-0.5 text-xs font-semibold text-indigo-700">
              beta
            </span>
          </div>
          <a
            href="#offre"
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700"
          >
            Passer en illimité — 6 €/mois
          </a>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">
        <div className="mb-8 max-w-2xl">
          <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Transformez une photo en patron de broderie
          </h1>
          <p className="mt-3 text-slate-600">
            Point de croix, perles Hama, diamond painting, pixel art. Importez
            une image, on génère la grille, les symboles et la liste des fils
            DMC à acheter. Export imprimable en un clic.
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-[320px_1fr]">
          {/* Panneau de contrôle */}
          <aside className="space-y-5">
            <div
              onDragOver={(e) => {
                e.preventDefault();
                setDragOver(true);
              }}
              onDragLeave={() => setDragOver(false)}
              onDrop={(e) => {
                e.preventDefault();
                setDragOver(false);
                const f = e.dataTransfer.files?.[0];
                if (f) loadFile(f);
              }}
              className={`rounded-xl border-2 border-dashed p-6 text-center transition ${
                dragOver
                  ? "border-indigo-500 bg-indigo-50"
                  : "border-slate-300 bg-white"
              }`}
            >
              <p className="text-sm text-slate-500">
                Glissez une image ici, ou
              </p>
              <label className="mt-2 inline-block cursor-pointer rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-700">
                Choisir un fichier
                <input
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={(e) => {
                    const f = e.target.files?.[0];
                    if (f) loadFile(f);
                  }}
                />
              </label>
              {imgEl && (
                <p className="mt-3 text-xs text-emerald-600">
                  Image chargée ✓ ({imgEl.width}×{imgEl.height}px)
                </p>
              )}
            </div>

            <div className="rounded-xl border border-slate-200 bg-white p-5">
              <label className="flex items-center justify-between text-sm font-medium">
                <span>Largeur de la grille</span>
                <span className="font-mono text-indigo-600">
                  {cols} mailles
                </span>
              </label>
              <input
                type="range"
                min={10}
                max={120}
                value={cols}
                onChange={(e) => setCols(Number(e.target.value))}
                className="mt-3 w-full accent-indigo-600"
              />
              <p className="mt-1 text-xs text-slate-400">
                Gratuit jusqu&apos;à {FREE_MAX_COLS} mailles · au-delà = offre
                payante
              </p>

              <label className="mt-4 flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={showSymbols}
                  onChange={toggleSymbols}
                  className="accent-indigo-600"
                />
                Afficher les symboles
              </label>

              <button
                onClick={generate}
                disabled={!imgEl}
                className="mt-5 w-full rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-40"
              >
                Générer le patron
              </button>
            </div>

            {stats && (
              <div className="rounded-xl border border-slate-200 bg-white p-5 text-sm">
                <h3 className="mb-2 font-semibold">Récapitulatif</h3>
                <dl className="space-y-1 text-slate-600">
                  <div className="flex justify-between">
                    <dt>Dimensions</dt>
                    <dd className="font-mono">{stats.dims}</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt>Total mailles</dt>
                    <dd className="font-mono">{stats.total}</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt>Couleurs de fil</dt>
                    <dd className="font-mono">{stats.colors}</dd>
                  </div>
                </dl>
                <button
                  onClick={exportPng}
                  className="mt-4 w-full rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold hover:bg-slate-50"
                >
                  Exporter en PNG{!premium && " (filigrané)"}
                </button>
                {!premium && (
                  <button
                    onClick={() => setShowPaywall(true)}
                    className="mt-2 w-full rounded-lg bg-amber-500 px-4 py-2 text-sm font-semibold text-white hover:bg-amber-600"
                  >
                    PDF imprimable sans filigrane — 4,99 €
                  </button>
                )}
              </div>
            )}
          </aside>

          {/* Aperçu */}
          <section className="min-w-0">
            <div className="overflow-auto rounded-xl border border-slate-200 bg-white p-4">
              {pattern ? (
                <canvas ref={canvasRef} className="mx-auto block" />
              ) : (
                <div className="flex h-96 items-center justify-center text-center text-slate-400">
                  <p>
                    Importez une image et cliquez sur
                    <br />
                    <span className="font-semibold">
                      « Générer le patron »
                    </span>
                  </p>
                </div>
              )}
            </div>

            {/* Légende des fils */}
            {pattern && (
              <div className="mt-6 rounded-xl border border-slate-200 bg-white p-5">
                <h3 className="mb-3 font-semibold">
                  Légende des fils ({pattern.used.length} couleurs)
                </h3>
                <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 text-sm sm:grid-cols-3">
                  {pattern.used.map((t) => (
                    <div key={t.index} className="flex items-center gap-2">
                      <span className="w-5 text-center font-mono text-base">
                        {t.symbol}
                      </span>
                      <span
                        className="h-4 w-4 shrink-0 rounded border border-slate-300"
                        style={{ background: t.hex }}
                      />
                      <span className="font-mono text-xs text-slate-500">
                        {t.code}
                      </span>
                      <span className="truncate text-slate-700">{t.name}</span>
                      <span className="ml-auto font-mono text-xs text-slate-400">
                        ×{t.count}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
        </div>

        {/* Offre */}
        <section
          id="offre"
          className="mt-12 rounded-2xl border border-slate-200 bg-white p-8"
        >
          <h2 className="text-xl font-bold">Tarifs</h2>
          <div className="mt-5 grid gap-5 sm:grid-cols-3">
            <PriceCard
              title="Découverte"
              price="0 €"
              features={[
                "Grille jusqu'à 50 mailles",
                "Aperçu + symboles",
                "Export PNG filigrané",
              ]}
            />
            <PriceCard
              title="Patron unique"
              price="4,99 €"
              highlight
              features={[
                "PDF imprimable A4",
                "Sans filigrane",
                "Légende des fils complète",
                "Grande grille",
              ]}
            />
            <PriceCard
              title="Vendeurs"
              price="6 €/mois"
              features={[
                "Patrons illimités",
                "Export PDF + PNG HD",
                "Idéal revente Etsy",
              ]}
            />
          </div>
        </section>
      </main>

      {/* Paywall */}
      {showPaywall && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
            <h3 className="text-lg font-bold">Débloquez votre patron</h3>
            <p className="mt-2 text-sm text-slate-600">
              Le PDF imprimable sans filigrane et les grandes grilles font
              partie de l&apos;offre payante. En production, ce bouton ouvre le
              paiement Stripe / Lemon Squeezy.
            </p>
            <div className="mt-5 flex gap-3">
              <button
                onClick={unlock}
                className="flex-1 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700"
              >
                Simuler le paiement (démo)
              </button>
              <button
                onClick={() => setShowPaywall(false)}
                className="rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold hover:bg-slate-50"
              >
                Annuler
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function PriceCard({
  title,
  price,
  features,
  highlight,
}: {
  title: string;
  price: string;
  features: string[];
  highlight?: boolean;
}) {
  return (
    <div
      className={`rounded-xl border p-5 ${
        highlight
          ? "border-indigo-300 bg-indigo-50/50 ring-1 ring-indigo-200"
          : "border-slate-200"
      }`}
    >
      <h3 className="font-semibold">{title}</h3>
      <p className="mt-1 text-2xl font-bold">{price}</p>
      <ul className="mt-4 space-y-1.5 text-sm text-slate-600">
        {features.map((f) => (
          <li key={f} className="flex items-start gap-2">
            <span className="text-emerald-500">✓</span>
            {f}
          </li>
        ))}
      </ul>
    </div>
  );
}

function hexRgb(hex: string): [number, number, number] {
  const h = hex.replace("#", "");
  return [
    parseInt(h.slice(0, 2), 16),
    parseInt(h.slice(2, 4), 16),
    parseInt(h.slice(4, 6), 16),
  ];
}
