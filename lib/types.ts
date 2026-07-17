// Types partagés de l'app. Tout est stocké localement (voir lib/store.tsx).

export type PersonId = "moi" | "partenaire";

export type Availability = "vert" | "orange" | "rouge";

export interface Person {
  id: PersonId;
  name: string;
  emoji: string;
}

export interface CheckIn {
  date: string; // YYYY-MM-DD
  mood: number; // 1..5
  energy: number; // 1..5
  availability: Availability;
  note?: string;
}

// Un signal « J'ai besoin de… » posé à un instant t.
export interface NeedSignal {
  id: string;
  person: PersonId;
  needId: string;
  at: string; // ISO datetime
}

export type LimitLevel = "oui" | "peut-etre" | "non";

export interface LimitEntry {
  id: string;
  person: PersonId;
  area: string; // clé de domaine (voir CONSENT_AREAS)
  item: string;
  level: LimitLevel;
  note?: string;
}

export type SensitivityKind = "allergie" | "intolerance" | "sensorielle" | "sujet";
export type Severity = "leger" | "moyen" | "fort";

export interface Sensitivity {
  id: string;
  person: PersonId;
  kind: SensitivityKind;
  label: string;
  severity: Severity;
  note?: string;
}

export interface CycleSettings {
  enabled: boolean;
  person: PersonId;
  lastPeriodStart: string; // YYYY-MM-DD
  cycleLength: number; // jours
  periodLength: number; // jours
}

export interface AppState {
  version: number;
  people: Record<PersonId, Person>;
  checkins: Partial<Record<PersonId, CheckIn>>;
  needs: NeedSignal[];
  limits: LimitEntry[];
  sensitivities: Sensitivity[];
  cycle: CycleSettings;
}
