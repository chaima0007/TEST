import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[digitalrights] SWARM_API_URL is not set")
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digitalrights`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return NextResponse.json(await sealResponse(data))
  } catch {
    return NextResponse.json(await sealResponse({ error: "upstream_error" }), { status: 502 })
  }
}
