import type { NextConfig } from "next";

const securityHeaders = [
  // Prevent MIME-type sniffing
  { key: "X-Content-Type-Options", value: "nosniff" },
  // Deny framing entirely (defence-in-depth alongside CSP frame-ancestors)
  { key: "X-Frame-Options", value: "DENY" },
  // Enforce HTTPS for 2 years, include subdomains, request preload listing
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },
  // Limit referrer information to same origin
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  // Disable sensitive hardware APIs and payment handler
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=(), payment=()" },
  // Legacy XSS filter (still respected by some older browsers)
  { key: "X-XSS-Protection", value: "1; mode=block" },
  // Prevent cross-origin window references (tab-napping / Spectre mitigations)
  { key: "Cross-Origin-Opener-Policy", value: "same-origin" },
  // Prevent other origins from embedding our resources
  { key: "Cross-Origin-Resource-Policy", value: "same-origin" },
  {
    key: "Content-Security-Policy",
    value: [
      "default-src 'self'",
      // Removed 'unsafe-eval' and 'unsafe-inline' — Next.js 16 uses nonces/hashes instead
      "script-src 'self'",
      // Inline styles are required by Tailwind CSS utility classes
      "style-src 'self' 'unsafe-inline'",
      // Allow images from known external domains (Clearbit logos, GitHub avatars) and data URIs
      "img-src 'self' data: https://logo.clearbit.com https://*.githubusercontent.com",
      "font-src 'self'",
      "connect-src 'self'",
      // Block Flash, Java, and other legacy plugins
      "object-src 'none'",
      // Prevent base-tag injection attacks
      "base-uri 'self'",
      // Restrict form submissions to same origin
      "form-action 'self'",
      // Block all framing — redundant with X-Frame-Options but CSP takes precedence in modern browsers
      "frame-ancestors 'none'",
      // Force HTTPS for all sub-resource requests
      "upgrade-insecure-requests",
    ].join("; "),
  },
];

const nextConfig: NextConfig = {
  // Remove the X-Powered-By: Next.js header to avoid fingerprinting
  poweredByHeader: false,
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
