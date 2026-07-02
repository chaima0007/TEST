// Recherche Google Places API (New) : établissements SANS site internet.

import type { DiscoveredBusiness } from "./types";
import { outreach } from "./config";

const PLACES_URL = "https://places.googleapis.com/v1/places:searchText";

const FIELD_MASK =
  "places.id,places.displayName,places.websiteUri,places.formattedAddress,places.nationalPhoneNumber,places.rating,places.userRatingCount,nextPageToken";

interface PlaceResult {
  id: string;
  displayName?: { text?: string };
  websiteUri?: string;
  formattedAddress?: string;
  nationalPhoneNumber?: string;
  rating?: number;
  userRatingCount?: number;
}

interface SearchTextResponse {
  places?: PlaceResult[];
  nextPageToken?: string;
}

export async function searchBusinessesWithoutWebsite(
  category: string,
  city: string,
  maxResults = 60
): Promise<DiscoveredBusiness[]> {
  if (!outreach.googlePlacesApiKey) {
    throw new Error("GOOGLE_PLACES_API_KEY manquante — configurez-la dans .env");
  }

  const results: DiscoveredBusiness[] = [];
  let pageToken: string | undefined;
  let fetched = 0;

  do {
    const body: Record<string, unknown> = {
      textQuery: `${category} à ${city}`,
      pageSize: 20,
    };
    if (pageToken) body.pageToken = pageToken;

    const res = await fetch(PLACES_URL, {
      method: "POST",
      headers: {
        "X-Goog-Api-Key": outreach.googlePlacesApiKey,
        "Content-Type": "application/json",
        "X-Goog-FieldMask": FIELD_MASK,
      },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const errorBody = await res.text();
      throw new Error(
        `Google Places API : erreur ${res.status} pour "${category} à ${city}" — ${errorBody}`
      );
    }

    const data = (await res.json()) as SearchTextResponse;
    const places = data.places ?? [];
    fetched += places.length;

    for (const place of places) {
      // On ne garde que les établissements sans site internet
      if (place.websiteUri && place.websiteUri.trim() !== "") continue;
      if (!place.id || !place.displayName?.text) continue;

      results.push({
        name: place.displayName.text,
        category,
        city,
        address: place.formattedAddress || undefined,
        phone: place.nationalPhoneNumber || undefined,
        email: undefined, // Places API ne fournit pas d'email
        googlePlaceId: place.id,
        rating: place.rating,
        reviewCount: place.userRatingCount,
        source: "places",
      });
    }

    pageToken = data.nextPageToken;
  } while (pageToken && fetched < maxResults);

  return results.slice(0, maxResults);
}
