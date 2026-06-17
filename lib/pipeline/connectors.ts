// ─── Étape 1 — Connecteurs de source ─────────────────────────────────────────
//
// IMPORTANT (légal & ToS) : un connecteur de PRODUCTION doit s'appuyer
// EXCLUSIVEMENT sur des sources légales — APIs officielles, flux RSS/JSON
// publiés, partenariats data. On NE fait PAS de scraping de LinkedIn, ni de
// rotation d'IP, ni de contournement de blocage : c'est contraire aux CGU et
// expose au RGPD (données personnelles de tiers). Tout nouveau connecteur
// implémente simplement `SourceConnector`.

export interface RawJobInput {
  /** Identifiant stable côté source, pour dédupliquer entre deux runs. */
  externalId: string;
  source: string;
  title: string;
  description: string;
  /** Budget tel qu'affiché par la source, brut (ex: "10 000 €", "TJM 500€/j"). */
  rawBudget?: string;
}

export interface SourceConnector {
  readonly name: string;
  fetchJobs(): Promise<RawJobInput[]>;
}

/**
 * Connecteur de démonstration : missions d'exemple, données fictives et légales.
 * Sert de référence d'implémentation et alimente la V1 sans clé API ni réseau.
 */
export class MockJobBoardConnector implements SourceConnector {
  readonly name = "mock-jobboard";

  async fetchJobs(): Promise<RawJobInput[]> {
    return [
      {
        externalId: "mock-001",
        source: this.name,
        title: "Développement d'une API Next.js + TypeScript",
        description:
          "Startup fintech cherche un freelance pour construire une API en Next.js et TypeScript avec Prisma. Mission de 3 mois, full remote. Budget 12 000 €.",
        rawBudget: "12 000 €",
      },
      {
        externalId: "mock-002",
        source: this.name,
        title: "Intégration design Tailwind sur dashboard React",
        description:
          "Besoin d'un intégrateur React/Tailwind senior pour reprendre un dashboard existant. 6 semaines, Paris ou remote. TJM autour de 450€/jour.",
        rawBudget: "450€/jour",
      },
      {
        externalId: "mock-003",
        source: this.name,
        title: "Petit script Python de scraping",
        description:
          "Recherche dev pour un script rapide. Budget très serré, 200€ maximum, livraison cette semaine.",
        rawBudget: "200€",
      },
      {
        externalId: "mock-004",
        source: this.name,
        title: "Refonte data engineering — pipelines SQL",
        description:
          "Grand compte recherche un data engineer senior (SQL, Python, dbt) pour 4 mois. Remote possible. Enveloppe 40 000 €.",
        rawBudget: "40 000 €",
      },
      {
        externalId: "mock-005",
        source: this.name,
        title: "Coup de main design Figma (non technique)",
        description:
          "Besoin d'aide ponctuelle sur des maquettes Figma. Pas de développement. Budget non précisé.",
      },
    ];
  }
}
