"use client";

import { useEffect, useState } from "react";

interface CompetitorSummary {
  id: string;
  name: string;
  industry: string;
  threatLevel: "high" | "medium" | "low";
  marketShare: number;
  latestNews: string | null;
}

interface ShopInfo {
  name: string;
  productCount: number;
}

// App Home landing page, rendered inside the Shopify admin iframe.
export default function ShopifyHomePage() {
  const [shopInfo, setShopInfo] = useState<ShopInfo | null>(null);
  const [competitors, setCompetitors] = useState<CompetitorSummary[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Direct API access: App Bridge intercepts fetch() and authenticates
    // shopify:admin requests with the merchant's session.
    fetch("shopify:admin/api/graphql.json", {
      method: "POST",
      body: JSON.stringify({
        query: `query HomeShopInfo { shop { name } productsCount { count } }`,
      }),
    })
      .then((res) => res.json())
      .then(({ data }) =>
        setShopInfo({ name: data.shop.name, productCount: data.productsCount.count }),
      )
      .catch(() => setShopInfo(null));

    // Backend call: App Bridge adds the session token as a Bearer header on
    // same-origin requests; the server verifies it in lib/shopify/authenticate.
    fetch("/api/shopify/competitors")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setCompetitors)
      .catch(() => setError("Impossible de charger les données concurrentielles."));
  }, []);

  const highThreats = competitors?.filter((c) => c.threatLevel === "high") ?? [];

  return (
    <s-page heading={shopInfo ? `Bienvenue, ${shopInfo.name}` : "CompeteIQ"}>
      <s-section heading="Vue d'ensemble">
        <s-paragraph>
          CompeteIQ surveille vos concurrents — prix, fonctionnalités et actualités — directement
          depuis votre admin Shopify.
        </s-paragraph>
        <s-stack direction="inline" gap="base">
          <s-box padding="base" borderWidth="base" borderRadius="base">
            <s-heading>{competitors ? String(competitors.length) : "—"}</s-heading>
            <s-text color="subdued">Concurrents suivis</s-text>
          </s-box>
          <s-box padding="base" borderWidth="base" borderRadius="base">
            <s-heading>{competitors ? String(highThreats.length) : "—"}</s-heading>
            <s-text color="subdued">Menaces élevées</s-text>
          </s-box>
          <s-box padding="base" borderWidth="base" borderRadius="base">
            <s-heading>{shopInfo ? String(shopInfo.productCount) : "—"}</s-heading>
            <s-text color="subdued">Produits dans votre boutique</s-text>
          </s-box>
        </s-stack>
      </s-section>

      {error ? (
        <s-section>
          <s-banner tone="warning">{error}</s-banner>
        </s-section>
      ) : null}

      {highThreats.length > 0 ? (
        <s-section heading="Alertes concurrentielles">
          <s-banner tone="critical">
            {highThreats.length} concurrent{highThreats.length > 1 ? "s" : ""} à menace élevée
            nécessite{highThreats.length > 1 ? "nt" : ""} votre attention.
          </s-banner>
          <s-unordered-list>
            {highThreats.slice(0, 3).map((c) => (
              <s-list-item key={c.id}>
                <s-text>{c.name}</s-text>
                {c.latestNews ? <s-text color="subdued"> — {c.latestNews}</s-text> : null}
              </s-list-item>
            ))}
          </s-unordered-list>
          <s-button href="/shopify/competitors" variant="primary">
            Voir tous les concurrents
          </s-button>
        </s-section>
      ) : null}

      <s-box slot="aside" padding="base">
        <s-section heading="Premiers pas">
          <s-paragraph>
            Consultez la liste des concurrents, puis ajustez vos préférences d&apos;alertes dans les
            paramètres.
          </s-paragraph>
          <s-stack direction="block" gap="base">
            <s-link href="/shopify/competitors">Explorer les concurrents</s-link>
            <s-link href="/shopify/settings">Configurer les alertes</s-link>
          </s-stack>
        </s-section>
      </s-box>
    </s-page>
  );
}
