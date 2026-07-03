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

// The /shopify segment renders inside the Shopify admin iframe: it must allow
// admin frame-ancestors, load App Bridge/Polaris from cdn.shopify.com, and
// must NOT send X-Frame-Options.
const shopifyEmbeddedHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  {
    key: "Content-Security-Policy",
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' https://cdn.shopify.com",
      "style-src 'self' 'unsafe-inline' https://cdn.shopify.com",
      "img-src 'self' data: https:",
      "font-src 'self' https://cdn.shopify.com",
      "connect-src 'self' https://cdn.shopify.com https://*.shopify.com https://*.myshopify.com",
      "frame-ancestors https://*.myshopify.com https://admin.shopify.com",
    ].join("; "),
  },
];

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "logo.clearbit.com" },
      { protocol: "https", hostname: "*.githubusercontent.com" },
    ],
  },
  async headers() {
    return [
      {
        source: "/((?!shopify).*)",
        headers: securityHeaders,
      },
      {
        source: "/shopify/:path*",
        headers: shopifyEmbeddedHeaders,
      },
      {
        source: "/shopify",
        headers: shopifyEmbeddedHeaders,
      },
    ];
  },
  serverExternalPackages: ["@prisma/adapter-libsql", "@libsql/client"],
};

export default nextConfig;
