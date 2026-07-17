/**
 * error-db — CaelumSwarm™ error tracking database
 *
 * Persistent JSON-file storage for tracking build errors, CI failures,
 * sidebar conflicts, engine bugs, and route security issues.
 * No external dependency — uses Node.js fs module only.
 */

import fs from "fs";
import path from "path";

export type ErrorType =
  | "build"
  | "ci"
  | "type"
  | "sidebar"
  | "engine"
  | "route"
  | "oom";

export type ErrorStatus = "open" | "fixed" | "recurring";

export interface ErrorRecord {
  id: number;
  timestamp: string;
  error_type: ErrorType;
  file_path: string | null;
  description: string;
  cause: string;
  fix_applied: string | null;
  resolution_time_minutes: number | null;
  wave: number | null;
  recurrence_count: number;
  status: ErrorStatus;
}

export interface ErrorFilter {
  error_type?: ErrorType;
  status?: ErrorStatus;
  wave?: number;
  min_recurrence?: number;
}

interface DBSchema {
  version: number;
  last_id: number;
  errors: ErrorRecord[];
}

const DB_PATH = path.resolve(process.cwd(), "data/errors.json");

function readDB(): DBSchema {
  try {
    if (!fs.existsSync(DB_PATH)) {
      return { version: 1, last_id: 0, errors: [] };
    }
    const raw = fs.readFileSync(DB_PATH, "utf-8");
    return JSON.parse(raw) as DBSchema;
  } catch {
    // Return empty DB on parse error — never crash the app
    console.warn("[ErrorDB] Could not read DB, starting fresh:", DB_PATH);
    return { version: 1, last_id: 0, errors: [] };
  }
}

function writeDB(db: DBSchema): void {
  const dir = path.dirname(DB_PATH);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2), "utf-8");
}

/**
 * ErrorDB singleton — JSON-backed error tracking store.
 */
export class ErrorDB {
  private static instance: ErrorDB;

  private constructor() {}

  static getInstance(): ErrorDB {
    if (!ErrorDB.instance) {
      ErrorDB.instance = new ErrorDB();
    }
    return ErrorDB.instance;
  }

  /**
   * Insert a new error record.
   * If an identical description already exists as "open", increments
   * recurrence_count and marks it "recurring" instead of inserting a duplicate.
   */
  insert(
    params: Omit<ErrorRecord, "id" | "timestamp" | "recurrence_count" | "status">
  ): ErrorRecord {
    const db = readDB();

    // Check for existing open error with same description (dedup logic)
    const existing = db.errors.find(
      (e) =>
        e.description === params.description &&
        (e.status === "open" || e.status === "recurring")
    );

    if (existing) {
      existing.recurrence_count += 1;
      existing.status = "recurring";
      // Update cause/file if provided
      if (params.cause) existing.cause = params.cause;
      if (params.file_path) existing.file_path = params.file_path;
      writeDB(db);
      return existing;
    }

    const record: ErrorRecord = {
      id: db.last_id + 1,
      timestamp: new Date().toISOString(),
      recurrence_count: 1,
      status: "open",
      ...params,
    };
    db.last_id = record.id;
    db.errors.push(record);
    writeDB(db);
    return record;
  }

  /**
   * Insert a record without dedup (used for seeding historical data).
   */
  insertRaw(record: Omit<ErrorRecord, "id">): ErrorRecord {
    const db = readDB();
    const full: ErrorRecord = { id: db.last_id + 1, ...record };
    db.last_id = full.id;
    db.errors.push(full);
    writeDB(db);
    return full;
  }

  /**
   * Mark an error as fixed.
   */
  markFixed(
    id: number,
    fix_applied: string,
    resolution_time_minutes?: number
  ): ErrorRecord | null {
    const db = readDB();
    const record = db.errors.find((e) => e.id === id);
    if (!record) return null;
    record.status = "fixed";
    record.fix_applied = fix_applied;
    if (resolution_time_minutes !== undefined) {
      record.resolution_time_minutes = resolution_time_minutes;
    }
    writeDB(db);
    return record;
  }

  /**
   * Return all errors, optionally filtered.
   */
  getErrors(filter?: ErrorFilter): ErrorRecord[] {
    const db = readDB();
    let results = db.errors;

    if (filter?.error_type) {
      results = results.filter((e) => e.error_type === filter.error_type);
    }
    if (filter?.status) {
      results = results.filter((e) => e.status === filter.status);
    }
    if (filter?.wave !== undefined) {
      results = results.filter((e) => e.wave === filter.wave);
    }
    if (filter?.min_recurrence !== undefined) {
      results = results.filter(
        (e) => e.recurrence_count >= filter.min_recurrence!
      );
    }

    return results;
  }

  /**
   * Return errors that recurred at least once (recurrence_count > 1).
   */
  getRecurring(): ErrorRecord[] {
    return this.getErrors({ min_recurrence: 2 });
  }

  /**
   * Return a single error by id.
   */
  getById(id: number): ErrorRecord | null {
    const db = readDB();
    return db.errors.find((e) => e.id === id) ?? null;
  }

  /**
   * Return total count and a breakdown by type and status.
   */
  getSummary(): {
    total: number;
    by_type: Record<ErrorType, number>;
    by_status: Record<ErrorStatus, number>;
    recurring_count: number;
  } {
    const errors = this.getErrors();

    const by_type: Record<string, number> = {};
    const by_status: Record<string, number> = {};
    let recurring_count = 0;

    for (const e of errors) {
      by_type[e.error_type] = (by_type[e.error_type] ?? 0) + 1;
      by_status[e.status] = (by_status[e.status] ?? 0) + 1;
      if (e.recurrence_count > 1) recurring_count++;
    }

    return {
      total: errors.length,
      by_type: by_type as Record<ErrorType, number>,
      by_status: by_status as Record<ErrorStatus, number>,
      recurring_count,
    };
  }
}
