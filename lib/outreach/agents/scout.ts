// Agent Scout : découverte de prospects sans site internet via Google Places,
// puis insertion en base (déduplication par googlePlaceId).

import { prisma } from "../../db";
import type { AgentSummary, ScoutParams } from "../types";
import { searchBusinessesWithoutWebsite } from "../places";

export async function runScout(params: ScoutParams): Promise<AgentSummary> {
  let processed = 0;
  let created = 0;
  let skipped = 0;
  const details: string[] = [];

  for (const category of params.categories) {
    for (const city of params.cities) {
      const businesses = await searchBusinessesWithoutWebsite(
        category,
        city,
        params.maxPerSearch
      );
      details.push(`${category}/${city} : ${businesses.length} sans site`);

      for (const biz of businesses) {
        processed++;

        const existing = biz.googlePlaceId
          ? await prisma.prospect.findUnique({
              where: { googlePlaceId: biz.googlePlaceId },
            })
          : null;

        if (existing) {
          skipped++;
          continue;
        }

        await prisma.prospect.create({
          data: {
            name: biz.name,
            category: biz.category,
            city: biz.city,
            address: biz.address,
            phone: biz.phone,
            email: biz.email,
            googlePlaceId: biz.googlePlaceId,
            rating: biz.rating,
            reviewCount: biz.reviewCount ?? 0,
            source: biz.source,
          },
        });
        created++;
      }
    }
  }

  return { agent: "scout", processed, created, skipped, details };
}
