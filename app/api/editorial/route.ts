import { NextResponse } from "next/server";
import { EDITORIAL_ITEMS, WEEKLY_THEMES, TYPE_META, STATUS_META } from "@/lib/editorial-data";

export async function GET() {
  return NextResponse.json({
    items: EDITORIAL_ITEMS,
    themes: WEEKLY_THEMES,
    type_meta: TYPE_META,
    status_meta: STATUS_META,
  });
}
