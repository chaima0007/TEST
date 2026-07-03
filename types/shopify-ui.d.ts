import type * as React from "react";

// Polaris web components (cdn.shopify.com/shopifycloud/polaris.js) and
// App Bridge web components (cdn.shopify.com/shopifycloud/app-bridge.js)
// are custom elements, so JSX needs them declared. Attributes are kebab-case
// strings, hence the permissive index signature.
type WebComponentProps = React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement> & {
  [attribute: string]: unknown;
};

declare module "react" {
  namespace JSX {
    interface IntrinsicElements {
      // Polaris web components
      "s-page": WebComponentProps;
      "s-section": WebComponentProps;
      "s-heading": WebComponentProps;
      "s-paragraph": WebComponentProps;
      "s-text": WebComponentProps;
      "s-button": WebComponentProps;
      "s-link": WebComponentProps;
      "s-badge": WebComponentProps;
      "s-banner": WebComponentProps;
      "s-box": WebComponentProps;
      "s-stack": WebComponentProps;
      "s-grid": WebComponentProps;
      "s-divider": WebComponentProps;
      "s-spinner": WebComponentProps;
      "s-table": WebComponentProps;
      "s-table-header-row": WebComponentProps;
      "s-table-header": WebComponentProps;
      "s-table-body": WebComponentProps;
      "s-table-row": WebComponentProps;
      "s-table-cell": WebComponentProps;
      "s-select": WebComponentProps;
      "s-option": WebComponentProps;
      "s-text-field": WebComponentProps;
      "s-switch": WebComponentProps;
      "s-unordered-list": WebComponentProps;
      "s-list-item": WebComponentProps;
      // App Bridge web components
      "ui-nav-menu": WebComponentProps;
      "ui-title-bar": WebComponentProps;
      "ui-save-bar": WebComponentProps;
    }
  }
}

// Global provided by App Bridge inside the Shopify admin.
interface ShopifyGlobal {
  idToken(): Promise<string>;
  toast: {
    show(message: string, options?: { isError?: boolean; duration?: number }): void;
  };
  config?: { shop?: string; locale?: string };
  environment?: { embedded?: boolean; mobile?: boolean; pos?: boolean };
}

declare global {
  interface Window {
    shopify?: ShopifyGlobal;
  }
}

export {};
