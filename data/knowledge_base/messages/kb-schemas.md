# KB Message — Schémas de données

**Type :** Knowledge Base Message  
**Scope :** Data Schemas & Types  
**Caelum Partners — Internal Dev Reference**

---

## Schéma Engine Score

```typescript
interface EngineScore {
  engine_id: string;           // ex: "land-grabbing-rights-engine"
  engine_name: string;         // ex: "Land Grabbing Rights Engine"
  entity_id: string;           // ex: "cambodia"
  entity_name: string;         // ex: "Cambodge"
  composite_score: number;     // 0-100
  severity: "critique" | "élevé" | "modéré" | "faible";
  sub_scores: SubScore[];
  estimated_index: number;     // composite_score / 100 * 10, arrondi 2 décimales
  primary_pattern: string;     // description du risque principal
  data_sources: string[];      // ONG, ONU, académique
  last_updated: string;        // ISO 8601
}

interface SubScore {
  sub_id: string;
  sub_name: string;
  score: number;               // 0-100
  weight: number;              // 0.20 à 0.30
  weighted_contribution: number;
}
```

---

## Schéma Distribution Obligatoire (8 entités par engine)

```typescript
interface EngineDistribution {
  critique: Entity[];    // 4 entités — score ≥ 60
  elevé: Entity[];       // 2 entités — score ≥ 40 et < 60
  modéré: Entity[];      // 1 entité  — score ≥ 20 et < 40
  faible: Entity[];      // 1 entité  — score < 20
}
```

**Distribution OBLIGATOIRE :** 4 critique / 2 élevé / 1 modéré / 1 faible

---

## Schéma Pondération Sous-scores

```typescript
const WEIGHTS = {
  sub1: 0.30,
  sub2: 0.25,
  sub3: 0.25,
  sub4: 0.20
} as const;

// Calcul composite_score
const composite_score = 
  sub1_score * WEIGHTS.sub1 +
  sub2_score * WEIGHTS.sub2 +
  sub3_score * WEIGHTS.sub3 +
  sub4_score * WEIGHTS.sub4;

// Calcul estimated_index
const estimated_index = Math.round(composite_score / 100 * 10 * 100) / 100;
```

---

## Schéma Rapport PDF

```typescript
interface ReportRequest {
  engine_ids: string[];        // 1 à 11 engines
  entity_filter?: string[];    // optionnel — filtrer entités
  severity_filter?: Severity[]; // optionnel — filtrer sévérité
  format: "pdf" | "json";
  language: "fr" | "en";
  include_sources: boolean;
  period: {
    start: string;             // ISO 8601
    end: string;               // ISO 8601
  };
}

interface ReportResponse {
  report_id: string;
  download_url: string;        // URL pré-signée, expire dans 1h
  generated_at: string;
  page_count: number;
  engines_covered: string[];
}
```

---

## Schéma Alerte Critique

```typescript
interface Alert {
  alert_id: string;
  engine_id: string;
  entity_id: string;
  entity_name: string;
  composite_score: number;
  severity: "critique";        // Les alertes sont toujours "critique"
  triggered_at: string;        // ISO 8601
  threshold: 60;               // Fixe — seuil critique
  acknowledged: boolean;
  acknowledged_by?: string;
  acknowledged_at?: string;
}
```

---

## Schéma KB Search

```typescript
interface KBSearchRequest {
  query: string;               // Texte de recherche
  engine_filter?: string[];    // Filtrer par engine
  severity_filter?: Severity[];
  limit?: number;              // Default: 10, Max: 50
  offset?: number;             // Pour pagination
}

interface KBSearchResponse {
  results: KBResult[];
  total: number;
  query_time_ms: number;
}

interface KBResult {
  id: string;
  engine_id: string;
  entity_id: string;
  content_type: "score" | "pattern" | "source" | "alert";
  excerpt: string;
  relevance_score: number;     // 0-1
  metadata: Record<string, unknown>;
}
```

---

## Seuils de sévérité (constants)

```typescript
const SEVERITY_THRESHOLDS = {
  critique: 60,    // score ≥ 60
  élevé: 40,       // score ≥ 40 et < 60
  modéré: 20,      // score ≥ 20 et < 40
  faible: 0        // score < 20
} as const;
```
