"use client";

import { useEffect, useState } from "react";

interface CompetitorRow {
  id: string;
  name: string;
  website: string;
  industry: string;
  threatLevel: "high" | "medium" | "low";
  marketShare: number;
  lastUpdated: string;
  startingPrice: number;
}

const THREAT_TONE: Record<string, string> = { high: "critical", medium: "warning", low: "success" };
const THREAT_LABEL: Record<string, string> = { high: "Élevée", medium: "Moyenne", low: "Faible" };

// Resource index page pattern: a table of tracked competitors.
export default function ShopifyCompetitorsPage() {
  const [rows, setRows] = useState<CompetitorRow[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/shopify/competitors")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setRows)
      .catch(() => setError("Impossible de charger les concurrents."));
  }, []);

  return (
    <s-page heading="Concurrents">
      {error ? (
        <s-section>
          <s-banner tone="critical">{error}</s-banner>
        </s-section>
      ) : null}

      {rows === null && !error ? (
        <s-section>
          <s-spinner accessibilityLabel="Chargement des concurrents" />
        </s-section>
      ) : null}

      {rows && rows.length === 0 ? (
        <s-section heading="Aucun concurrent suivi">
          <s-paragraph>
            CompeteIQ n&apos;a pas encore de concurrents configurés pour votre boutique. Ajoutez vos
            premiers concurrents pour commencer à recevoir des analyses de prix et des alertes.
          </s-paragraph>
        </s-section>
      ) : null}

      {rows && rows.length > 0 ? (
        <s-section heading="Concurrents suivis" padding="none">
          <s-table>
            <s-table-header-row>
              <s-table-header listSlot="primary">Concurrent</s-table-header>
              <s-table-header>Secteur</s-table-header>
              <s-table-header>Menace</s-table-header>
              <s-table-header>Part de marché</s-table-header>
              <s-table-header>À partir de</s-table-header>
              <s-table-header>Mis à jour</s-table-header>
            </s-table-header-row>
            <s-table-body>
              {rows.map((row) => (
                <s-table-row key={row.id}>
                  <s-table-cell>
                    <s-stack direction="block">
                      <s-text>{row.name}</s-text>
                      <s-text color="subdued">{row.website}</s-text>
                    </s-stack>
                  </s-table-cell>
                  <s-table-cell>{row.industry}</s-table-cell>
                  <s-table-cell>
                    <s-badge tone={THREAT_TONE[row.threatLevel]}>
                      {THREAT_LABEL[row.threatLevel]}
                    </s-badge>
                  </s-table-cell>
                  <s-table-cell>{row.marketShare.toFixed(1)} %</s-table-cell>
                  <s-table-cell>{row.startingPrice ? `${row.startingPrice} €/mois` : "—"}</s-table-cell>
                  <s-table-cell>{row.lastUpdated}</s-table-cell>
                </s-table-row>
              ))}
            </s-table-body>
          </s-table>
        </s-section>
      ) : null}
    </s-page>
  );
}
