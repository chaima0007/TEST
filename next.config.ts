import type { NextConfig } from "next";

const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
  {
    key: "Content-Security-Policy",
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "font-src 'self'",
      "connect-src 'self'",
      "frame-ancestors 'none'",
    ].join("; "),
  },
];

const nextConfig: NextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  // Memory & build optimizations — source: next/dist/docs/01-app/02-guides/memory-usage.md
  productionBrowserSourceMaps: false,
  experimental: {
    webpackMemoryOptimizations: true,
    webpackBuildWorker: true,
    // Réduit le footprint mémoire au démarrage du build (grosse app : milliers
    // d'icônes + centaines de dashboards) — source: memory-usage.md §preloadEntriesOnStart
    preloadEntriesOnStart: false,
    // Pas de source maps serveur en prod → économie RAM build — source: memory-usage.md
    serverSourceMaps: false,
  },
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "logo.clearbit.com" },
      { protocol: "https", hostname: "*.githubusercontent.com" },
    ],
  },
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: securityHeaders,
      },
    ];
  },
  serverExternalPackages: ["@prisma/adapter-libsql", "@libsql/client"],
};

export default nextConfig;
