import { NextRequest, NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";
import { getErrors, getSummary, logError, markFixed } from "@/lib/error-tracker";
import type { ErrorType, ErrorStatus } from "@/lib/error-db";

if (!process.env.SWARM_API_URL) {
  console.warn(
    "[api/errors] SWARM_API_URL is not set — running in local/offline mode"
  );
}

/**
 * GET /api/errors
 *
 * Query params (all optional):
 *   ?type=build|ci|type|sidebar|engine|route|oom
 *   ?status=open|fixed|recurring
 *   ?wave=<number>
 *   ?min_recurrence=<number>
 *   ?summary=true  → returns aggregate counts only
 *
 * Returns a sealed payload containing the list of matched error records
 * (or a summary object if ?summary=true).
 */
export async function GET(req: NextRequest) {
  const { searchParams } = req.nextUrl;

  const summaryOnly = searchParams.get("summary") === "true";

  if (summaryOnly) {
    const summary = getSummary();
    return NextResponse.json(
      sealResponse({ summary }),
      { status: 200, headers: { "Cache-Control": "no-store" } }
    );
  }

  const filter: {
    error_type?: ErrorType;
    status?: ErrorStatus;
    wave?: number;
    min_recurrence?: number;
  } = {};

  const typeParam = searchParams.get("type");
  if (typeParam) filter.error_type = typeParam as ErrorType;

  const statusParam = searchParams.get("status");
  if (statusParam) filter.status = statusParam as ErrorStatus;

  const waveParam = searchParams.get("wave");
  if (waveParam) filter.wave = parseInt(waveParam, 10);

  const recurrenceParam = searchParams.get("min_recurrence");
  if (recurrenceParam) filter.min_recurrence = parseInt(recurrenceParam, 10);

  const errors = getErrors(Object.keys(filter).length ? filter : undefined);

  return NextResponse.json(
    sealResponse({ errors, total: errors.length }),
    {
      status: 200,
      headers: { "Cache-Control": "no-store" },
      next: { revalidate: 30 },
    } as never
  );
}

/**
 * POST /api/errors
 *
 * Body: { error_type, description, cause, file_path?, fix_applied?,
 *         resolution_time_minutes?, wave? }
 *
 * Creates (or increments recurrence of) an error record.
 */
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { error_type, description, cause } = body;

    if (!error_type || !description || !cause) {
      return NextResponse.json(
        sealResponse({ error: "error_type, description and cause are required" }),
        { status: 400 }
      );
    }

    const record = logError({
      error_type,
      description,
      cause,
      file_path: body.file_path,
      fix_applied: body.fix_applied,
      resolution_time_minutes: body.resolution_time_minutes,
      wave: body.wave,
    });

    return NextResponse.json(sealResponse({ record }), { status: 201 });
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Invalid JSON body" }),
      { status: 502 }
    );
  }
}

/**
 * PATCH /api/errors
 *
 * Body: { id, fix_applied, resolution_time_minutes? }
 *
 * Marks an error as fixed.
 */
export async function PATCH(req: NextRequest) {
  try {
    const body = await req.json();
    const { id, fix_applied, resolution_time_minutes } = body;

    if (!id || !fix_applied) {
      return NextResponse.json(
        sealResponse({ error: "id and fix_applied are required" }),
        { status: 400 }
      );
    }

    const record = markFixed(Number(id), fix_applied, resolution_time_minutes);

    if (!record) {
      return NextResponse.json(
        sealResponse({ error: `Error id ${id} not found` }),
        { status: 404 }
      );
    }

    return NextResponse.json(sealResponse({ record }), { status: 200 });
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Invalid JSON body" }),
      { status: 502 }
    );
  }
}
