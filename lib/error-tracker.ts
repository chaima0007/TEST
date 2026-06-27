/**
 * error-tracker — CaelumSwarm™ convenience helpers for error logging
 *
 * Thin façade over ErrorDB. Use these helpers in any engine, route,
 * or script to record errors without importing the full DB class.
 *
 * Usage:
 *   import { logError, markFixed, getRecurring } from "@/lib/error-tracker"
 *   await logError({ error_type: "sidebar", description: "...", cause: "..." })
 */

import { ErrorDB, type ErrorType, type ErrorRecord, type ErrorFilter } from "./error-db";

export interface LogErrorParams {
  error_type: ErrorType;
  description: string;
  cause: string;
  file_path?: string;
  fix_applied?: string;
  resolution_time_minutes?: number;
  wave?: number;
}

/**
 * Log a new error (or increment recurrence if same description already open).
 * Returns the created or updated ErrorRecord.
 */
export function logError(params: LogErrorParams): ErrorRecord {
  const db = ErrorDB.getInstance();
  return db.insert({
    error_type: params.error_type,
    description: params.description,
    cause: params.cause,
    file_path: params.file_path ?? null,
    fix_applied: params.fix_applied ?? null,
    resolution_time_minutes: params.resolution_time_minutes ?? null,
    wave: params.wave ?? null,
  });
}

/**
 * Mark an existing error as fixed.
 * @param id — the error id returned by logError
 * @param fix — description of what was done to fix it
 * @param resolutionMinutes — optional time to fix (minutes)
 */
export function markFixed(
  id: number,
  fix: string,
  resolutionMinutes?: number
): ErrorRecord | null {
  const db = ErrorDB.getInstance();
  return db.markFixed(id, fix, resolutionMinutes);
}

/**
 * Return all errors that recurred more than once.
 * These are the patterns worth documenting in AGENTS.md / CLAUDE.md.
 */
export function getRecurring(): ErrorRecord[] {
  const db = ErrorDB.getInstance();
  return db.getRecurring();
}

/**
 * Return all errors, optionally filtered.
 * @param filter — optional { error_type, status, wave, min_recurrence }
 */
export function getErrors(filter?: ErrorFilter): ErrorRecord[] {
  const db = ErrorDB.getInstance();
  return db.getErrors(filter);
}

/**
 * Return a summary of the error DB (totals, breakdown by type and status).
 */
export function getSummary() {
  const db = ErrorDB.getInstance();
  return db.getSummary();
}

/**
 * Return a single error by id.
 */
export function getErrorById(id: number): ErrorRecord | null {
  const db = ErrorDB.getInstance();
  return db.getById(id);
}
