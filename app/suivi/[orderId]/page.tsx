import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getOrderTrackingView, type OrderTrackingView, type TrackingStep } from "@/lib/shopify/tracking";
import { DeliveryPromise } from "@/components/DeliveryPromise";

// Page publique de suivi de commande — hors admin, hors /shopify.
// Différenciant « transparence logistique » (docs/ARCHITECTURE_BOUTIQUE.md §2).
// Rendu dynamique : les données de suivi dépendent de la requête (jamais mises
// en cache au build), et l'accès base/Admin API se fait à la demande.
export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Suivi de commande",
  description: "Suivez votre commande en toute transparence, étape par étape.",
  robots: { index: false, follow: false }, // page personnelle : pas d'indexation
};

function formatDateLong(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
}

function formatDateTime(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleString("fr-FR", { day: "numeric", month: "long", hour: "2-digit", minute: "2-digit" });
}

function StepIcon({ step }: { step: TrackingStep }) {
  if (step.completed && !step.current) {
    // Étape franchie
    return (
      <span
        aria-hidden="true"
        className="flex h-9 w-9 items-center justify-center rounded-full bg-emerald-500 text-white shadow-sm"
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M3 8.5l3.5 3.5L13 4.5" />
        </svg>
      </span>
    );
  }
  if (step.current) {
    // Étape en cours
    return (
      <span
        aria-hidden="true"
        className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-600 text-white shadow-sm ring-4 ring-indigo-100"
      >
        <span className="h-2.5 w-2.5 rounded-full bg-white animate-pulse" />
      </span>
    );
  }
  // Étape à venir
  return (
    <span
      aria-hidden="true"
      className="flex h-9 w-9 items-center justify-center rounded-full border-2 border-slate-200 bg-white text-slate-300"
    >
      <span className="h-2.5 w-2.5 rounded-full bg-slate-200" />
    </span>
  );
}

function TrackingTimeline({ view }: { view: OrderTrackingView }) {
  const currentIndex = view.steps.findIndex((s) => s.current);
  return (
    <ol className="relative" aria-label="Progression de la livraison">
      {view.steps.map((step, i) => {
        const isLast = i === view.steps.length - 1;
        // Le segment reliant à l'étape suivante est vert si l'étape actuelle est franchie.
        const connectorDone = i < currentIndex;
        return (
          <li key={step.status} className="relative flex gap-4 pb-8 last:pb-0">
            {!isLast && (
              <span
                aria-hidden="true"
                className={`absolute left-[17px] top-9 h-[calc(100%-1.25rem)] w-0.5 ${
                  connectorDone ? "bg-emerald-400" : "bg-slate-200"
                }`}
              />
            )}
            <div className="relative z-10 flex-shrink-0">
              <StepIcon step={step} />
            </div>
            <div className="pt-1">
              <p
                className={`text-sm font-semibold ${
                  step.current ? "text-indigo-700" : step.completed ? "text-slate-800" : "text-slate-400"
                }`}
              >
                {step.label}
                {step.current && (
                  <span className="ml-2 inline-flex items-center rounded-full bg-indigo-50 px-2 py-0.5 text-[11px] font-medium text-indigo-600">
                    En cours
                  </span>
                )}
              </p>
              <p className={`mt-0.5 text-sm ${step.completed || step.current ? "text-slate-500" : "text-slate-400"}`}>
                {step.description}
              </p>
            </div>
          </li>
        );
      })}
    </ol>
  );
}

async function TrackingContent({ orderId }: { orderId: string }) {
  const view = await getOrderTrackingView(orderId);
  if (!view) notFound();

  return (
    <div className="mx-auto w-full max-w-xl px-4 py-8 sm:py-12">
      {/* En-tête */}
      <header className="mb-6 text-center">
        <div className="mx-auto mb-4 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-600 shadow-sm">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M3 7l9-4 9 4v10l-9 4-9-4V7z" />
            <path d="M3 7l9 4 9-4M12 11v10" />
          </svg>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Suivi de votre commande</h1>
        <p className="mt-1 text-sm text-slate-500">
          Commande <span className="font-semibold text-slate-700">{view.orderNumber}</span>
        </p>
      </header>

      {view.isDemo && (
        <div
          role="status"
          className="mb-5 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800"
        >
          Aperçu de démonstration : la boutique n&apos;est pas encore connectée. Les statuts réels
          s&apos;afficheront automatiquement dès la mise en ligne.
        </div>
      )}

      {/* Carte statut + date estimée */}
      <section
        aria-label="Statut actuel"
        className="mb-6 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
      >
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Statut actuel</p>
            <p className="mt-1 text-lg font-bold text-indigo-700">{view.statusLabel}</p>
          </div>
          <div className="rounded-xl bg-slate-50 px-4 py-3 text-center sm:text-right">
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">Livraison estimée</p>
            <p className="mt-1 text-sm font-semibold text-slate-800">
              {view.estimatedDelivery ? formatDateLong(view.estimatedDelivery) : "À confirmer"}
            </p>
          </div>
        </div>

        {(view.trackingCompany || view.trackingUrl) && (
          <div className="mt-4 flex flex-wrap items-center gap-3 border-t border-slate-100 pt-4 text-sm">
            {view.trackingCompany && (
              <span className="text-slate-500">
                Transporteur : <span className="font-medium text-slate-700">{view.trackingCompany}</span>
              </span>
            )}
            {view.trackingUrl && (
              <a
                href={view.trackingUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 font-medium text-indigo-600 hover:text-indigo-800 hover:underline"
              >
                Suivre chez le transporteur
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M2 10L10 2M5 2h5v5" />
                </svg>
              </a>
            )}
          </div>
        )}
      </section>

      {/* Chronologie */}
      <section aria-label="Étapes de livraison" className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="mb-5 text-sm font-semibold text-slate-900">Progression</h2>
        <TrackingTimeline view={view} />
      </section>

      {/* Réassurance */}
      <div className="mt-6">
        <DeliveryPromise />
      </div>

      <p className="mt-6 text-center text-xs text-slate-400">
        Dernière mise à jour : {formatDateTime(view.updatedAt)}
      </p>
    </div>
  );
}

export default async function SuiviPage(props: PageProps<"/suivi/[orderId]">) {
  const { orderId } = await props.params;
  return (
    <main className="min-h-screen bg-slate-50">
      <TrackingContent orderId={orderId} />
    </main>
  );
}
