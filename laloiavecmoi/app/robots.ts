import type { MetadataRoute } from "next";

// À adapter avec ton domaine définitif (ex. https://laloiavecmoi.be).
const BASE = "https://laloiavecmoi.be";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: "*", allow: "/" },
    sitemap: `${BASE}/sitemap.xml`,
  };
}
