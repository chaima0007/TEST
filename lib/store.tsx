"use client";

import { useSyncExternalStore } from "react";
import type {
  AppState,
  CheckIn,
  CycleSettings,
  LimitEntry,
  PersonId,
  Sensitivity,
} from "./types";
import { seedState, STATE_VERSION } from "./seed";
import { todayIso } from "./date";

const STORAGE_KEY = "nous.state.v1";

function newId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `id-${Date.now()}-${Math.floor(Math.random() * 1e6)}`;
}

// --- Store externe (module-level) ---------------------------------------
// Un seul état vivant, lu par les composants via useSyncExternalStore.
// Rendu serveur = graine stable ; le vrai état est chargé côté client.

const SERVER_SNAPSHOT: AppState = seedState("2000-01-01");
let clientState: AppState | null = null;
const listeners = new Set<() => void>();

function load(): AppState {
  const fresh = seedState(todayIso());
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return fresh;
    const parsed = JSON.parse(raw) as AppState;
    if (!parsed || parsed.version !== STATE_VERSION) return fresh;
    return parsed;
  } catch {
    return fresh;
  }
}

function getClientSnapshot(): AppState {
  if (clientState === null) clientState = load();
  return clientState;
}

function getServerSnapshot(): AppState {
  return SERVER_SNAPSHOT;
}

function subscribe(cb: () => void): () => void {
  listeners.add(cb);
  return () => listeners.delete(cb);
}

function mutate(updater: (s: AppState) => AppState): void {
  const base = getClientSnapshot();
  clientState = updater(base);
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(clientState));
  } catch {
    /* quota / navigation privée : on ignore */
  }
  listeners.forEach((l) => l());
}

// --- Actions ------------------------------------------------------------

const actions = {
  setCheckIn(person: PersonId, patch: Partial<CheckIn>) {
    mutate((s) => {
      const prev: CheckIn = s.checkins[person] ?? {
        date: todayIso(),
        mood: 3,
        energy: 3,
        availability: "vert",
      };
      return {
        ...s,
        checkins: { ...s.checkins, [person]: { ...prev, date: todayIso(), ...patch } },
      };
    });
  },
  addNeed(person: PersonId, needId: string) {
    mutate((s) => ({
      ...s,
      needs: [...s.needs, { id: newId(), person, needId, at: new Date().toISOString() }],
    }));
  },
  clearNeeds(person: PersonId) {
    mutate((s) => ({ ...s, needs: s.needs.filter((n) => n.person !== person) }));
  },
  addLimit(entry: Omit<LimitEntry, "id">) {
    mutate((s) => ({ ...s, limits: [...s.limits, { ...entry, id: newId() }] }));
  },
  updateLimit(id: string, patch: Partial<LimitEntry>) {
    mutate((s) => ({
      ...s,
      limits: s.limits.map((l) => (l.id === id ? { ...l, ...patch } : l)),
    }));
  },
  removeLimit(id: string) {
    mutate((s) => ({ ...s, limits: s.limits.filter((l) => l.id !== id) }));
  },
  addSensitivity(entry: Omit<Sensitivity, "id">) {
    mutate((s) => ({ ...s, sensitivities: [...s.sensitivities, { ...entry, id: newId() }] }));
  },
  removeSensitivity(id: string) {
    mutate((s) => ({ ...s, sensitivities: s.sensitivities.filter((x) => x.id !== id) }));
  },
  setCycle(patch: Partial<CycleSettings>) {
    mutate((s) => ({ ...s, cycle: { ...s.cycle, ...patch } }));
  },
  setName(person: PersonId, name: string) {
    mutate((s) => ({
      ...s,
      people: { ...s.people, [person]: { ...s.people[person], name } },
    }));
  },
  reset() {
    mutate(() => seedState(todayIso()));
  },
};

// Vrai après l'hydratation (sans effet ni setState → compatible lint React 19).
function subscribeNoop(): () => void {
  return () => {};
}

type Store = typeof actions & {
  ready: boolean;
  state: AppState;
};

export function useApp(): Store {
  const state = useSyncExternalStore(subscribe, getClientSnapshot, getServerSnapshot);
  const ready = useSyncExternalStore(
    subscribeNoop,
    () => true,
    () => false,
  );
  return { ready, state, ...actions };
}
