/**
 * digital-seal — CaelumSwarm™ response integrity utility
 *
 * Wraps a JSON payload with a lightweight metadata envelope so that
 * every engine endpoint returns a consistently shaped object that
 * consumers can validate client-side.
 */

export interface SealedPayload<T = unknown> {
  payload: T;
  sealed: true;
  ts: string;
}

/**
 * Wraps `data` in a sealed envelope.
 * Usage:  NextResponse.json(sealResponse(data))
 */
export function sealResponse<T>(data: T): SealedPayload<T> {
  return {
    payload: data,
    sealed: true,
    ts: new Date().toISOString(),
  };
}
