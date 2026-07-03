import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "CompeteIQ",
};

// Embedded App Home layout. App Bridge requires the api-key meta tag to be
// parsed before its script runs, and the script itself must load synchronously
// (no async/defer) so the admin can render the app frame without flicker.
export default function ShopifyLayout({ children }: { children: React.ReactNode }) {
  const apiKey = process.env.SHOPIFY_API_KEY ?? "";

  return (
    <div className="bg-white min-h-screen">
      <meta name="shopify-api-key" content={apiKey} />
      {/* eslint-disable-next-line @next/next/no-sync-scripts */}
      <script src="https://cdn.shopify.com/shopifycloud/app-bridge.js" />
      {/* eslint-disable-next-line @next/next/no-sync-scripts */}
      <script src="https://cdn.shopify.com/shopifycloud/polaris.js" />
      <ui-nav-menu>
        <a href="/shopify" rel="home">
          Accueil
        </a>
        <a href="/shopify/competitors">Concurrents</a>
        <a href="/shopify/settings">Paramètres</a>
      </ui-nav-menu>
      {children}
    </div>
  );
}
