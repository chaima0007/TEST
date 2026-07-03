"use client";

import { useState } from "react";

// Settings page pattern: grouped sections with a clear save action.
export default function ShopifySettingsPage() {
  const [frequency, setFrequency] = useState("daily");
  const [priceAlerts, setPriceAlerts] = useState(true);
  const [newsAlerts, setNewsAlerts] = useState(true);
  const [saving, setSaving] = useState(false);

  const save = async () => {
    setSaving(true);
    try {
      // Preferences are demo-only for now; persisting them server-side would
      // go through an authenticated /api/shopify route like the competitors data.
      await new Promise((resolve) => setTimeout(resolve, 300));
      window.shopify?.toast.show("Paramètres enregistrés");
    } finally {
      setSaving(false);
    }
  };

  return (
    <s-page heading="Paramètres">
      <s-section heading="Alertes concurrentielles">
        <s-paragraph>
          Choisissez les événements concurrents qui déclenchent une notification dans votre admin.
        </s-paragraph>
        <s-stack direction="block" gap="base">
          <s-switch
            label="Alertes de changement de prix"
            checked={priceAlerts || undefined}
            onChange={() => setPriceAlerts((v) => !v)}
          />
          <s-switch
            label="Alertes d'actualités (levées de fonds, lancements produits)"
            checked={newsAlerts || undefined}
            onChange={() => setNewsAlerts((v) => !v)}
          />
          <s-select
            label="Fréquence du résumé"
            value={frequency}
            onChange={(event: React.ChangeEvent<HTMLSelectElement>) => setFrequency(event.target.value)}
          >
            <s-option value="realtime">Temps réel</s-option>
            <s-option value="daily">Quotidien</s-option>
            <s-option value="weekly">Hebdomadaire</s-option>
          </s-select>
        </s-stack>
      </s-section>

      <s-section heading="Enregistrer">
        <s-button variant="primary" onClick={save} disabled={saving || undefined}>
          {saving ? "Enregistrement…" : "Enregistrer les paramètres"}
        </s-button>
      </s-section>
    </s-page>
  );
}
