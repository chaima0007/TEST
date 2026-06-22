"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState, useEffect } from "react";

// ─── SVG Icons ──────────────────────────────────────────────────────────────

function IconDashboard({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="2" y="2" width="7" height="7" rx="1" />
      <rect x="11" y="2" width="7" height="7" rx="1" />
      <rect x="2" y="11" width="7" height="7" rx="1" />
      <rect x="11" y="11" width="7" height="7" rx="1" />
    </svg>
  );
}

function IconCompetitors({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 7h4v10H3V7zM8 4h4v13H8V4zM13 9h4v8h-4V9z" />
    </svg>
  );
}

function IconComparison({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 10a8 8 0 1 1 16 0A8 8 0 0 1 2 10zm8-5v5h3l-4 5-4-5h3V5h2z" />
    </svg>
  );
}

function IconPricing({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M17.707 9.293l-7-7A1 1 0 0 0 10 2H4a2 2 0 0 0-2 2v6a1 1 0 0 0 .293.707l7 7a1 1 0 0 0 1.414 0l7-7a1 1 0 0 0 0-1.414zM6 7a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconAlerts({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2a6 6 0 0 0-6 6v2.586l-.707.707A1 1 0 0 0 4 13h12a1 1 0 0 0 .707-1.707L16 10.586V8a6 6 0 0 0-6-6zM8.5 17a1.5 1.5 0 0 0 3 0H8.5z" />
    </svg>
  );
}

function IconReports({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M4 2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.414A2 2 0 0 0 17.414 6L13 1.586A2 2 0 0 0 11.586 2H4zm7 1.5V7h3.5L11 3.5zM6 11h8v1.5H6V11zm0 3h5v1.5H6V14zm0-6h3v1.5H6V8z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconAgents({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v1h8v-1zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-1a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v1h-3zM4.75 14.094A5.973 5.973 0 004 17v1H1v-1a3 3 0 013.75-2.906z" />
    </svg>
  );
}

function IconPortfolio({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clipRule="evenodd" />
      <path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z" />
    </svg>
  );
}

function IconEditorial({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
    </svg>
  );
}

function IconBranding({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clipRule="evenodd" />
    </svg>
  );
}

function IconHandshake({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M9 3.5a.5.5 0 0 0-.5.5v.793L7.146 5.146a.5.5 0 0 0 0 .708l1.5 1.5A.5.5 0 0 0 9 7.5h2a.5.5 0 0 0 .354-.146l1.5-1.5a.5.5 0 0 0 0-.708L11.5 4.793V4a.5.5 0 0 0-.5-.5H9z" />
      <path fillRule="evenodd" d="M2 9a1 1 0 0 1 1-1h1.293l1.147-1.146a.5.5 0 0 1 .353-.147h1.414l.94-.94A2 2 0 0 1 9.56 5h.88a2 2 0 0 1 1.414.586l.94.94h1.413a.5.5 0 0 1 .354.146L15.707 8H17a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-1.586l-1.207 1.207a1 1 0 0 1-.707.293H6.5a1 1 0 0 1-.707-.293L4.586 14H3a1 1 0 0 1-1-1V9zm3.086 0L3.5 10.586V12.5h.914l1.5 1.5h7.172l1.5-1.5h.914v-1.914L13.914 9h-1.207l-1.354-1.354A1 1 0 0 0 10.646 7.5H9.354a1 1 0 0 0-.707.293L7.293 9H5.086z" clipRule="evenodd" />
    </svg>
  );
}

function IconTarget({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm0-2a6 6 0 100-12 6 6 0 000 12zm0-2a4 4 0 100-8 4 4 0 000 8zm0-2a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
    </svg>
  );
}

function IconFinance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
    </svg>
  );
}

function IconLive({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zm6-4a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zm6-3a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
    </svg>
  );
}

function IconFlask({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M7 2a1 1 0 00-.707 1.707L7 4.414v3.758a1 1 0 01-.293.707l-4 4C.817 14.769 2.156 18 4.828 18h10.344c2.672 0 4.011-3.231 2.122-5.121l-4-4A1 1 0 0113 8.172V4.414l.707-.707A1 1 0 0013 2H7zm2 6.172V4h2v4.172a3 3 0 00.879 2.12l1.027 1.028a4 4 0 00-2.171.102l-.47.156a4 4 0 01-2.53 0l-.563-.187a1.993 1.993 0 00-.114-.035l1.063-1.063A3 3 0 009 8.172z" clipRule="evenodd" />
    </svg>
  );
}

function IconSector({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
      <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
    </svg>
  );
}

function IconPipeline({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 3a1 1 0 000 2h11a1 1 0 100-2H3zm0 4a1 1 0 000 2h7a1 1 0 100-2H3zm0 4a1 1 0 100 2h4a1 1 0 100-2H3zm12-4a3 3 0 11-6 0 3 3 0 016 0zm-1.5 0a1.5 1.5 0 10-3 0 1.5 1.5 0 003 0zM17 13a2 2 0 11-4 0 2 2 0 014 0z" clipRule="evenodd" />
    </svg>
  );
}

function IconEmail({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
      <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
    </svg>
  );
}

function IconMemory({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M9 9a2 2 0 114 0 2 2 0 01-4 0z" />
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a4 4 0 00-3.446 6.032l-2.261 2.26a1 1 0 101.414 1.415l2.261-2.261A4 4 0 1011 5z" clipRule="evenodd" />
    </svg>
  );
}

function IconCalendar({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
    </svg>
  );
}

function IconQuote({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h4a1 1 0 100-2H7z" clipRule="evenodd" />
    </svg>
  );
}

function IconSequence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 4a1 1 0 011-1h1a1 1 0 010 2H3a1 1 0 01-1-1zm4 0a1 1 0 011-1h10a1 1 0 110 2H7a1 1 0 01-1-1zM2 9a1 1 0 011-1h1a1 1 0 010 2H3a1 1 0 01-1-1zm4 0a1 1 0 011-1h10a1 1 0 110 2H7a1 1 0 01-1-1zM2 14a1 1 0 011-1h1a1 1 0 110 2H3a1 1 0 01-1-1zm4 0a1 1 0 011-1h10a1 1 0 110 2H7a1 1 0 01-1-1z" />
    </svg>
  );
}

function IconQualification({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
    </svg>
  );
}

function IconInvoice({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M5 2a2 2 0 00-2 2v14l3.5-2 3.5 2 3.5-2 3.5 2V4a2 2 0 00-2-2H5zm4.707 5.707a1 1 0 00-1.414-1.414l-3 3a1 1 0 000 1.414l3 3a1 1 0 001.414-1.414L7.414 11H13a1 1 0 100-2H7.414l2.293-2.293z" clipRule="evenodd" />
    </svg>
  );
}

function IconEnricher({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" clipRule="evenodd" />
    </svg>
  );
}

function IconLeadScorer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
    </svg>
  );
}

function IconFunnel({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-.293.707L13 9.414V15a1 1 0 01-.553.894l-4 2A1 1 0 017 17V9.414L3.293 5.707A1 1 0 013 5V3z" clipRule="evenodd" />
    </svg>
  );
}

function IconSubjectOptimizer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
      <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
    </svg>
  );
}

function IconMarket({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
      <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
    </svg>
  );
}

function IconDealAccelerator({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
    </svg>
  );
}

function IconContactPersonalizer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
      <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
    </svg>
  );
}

function IconCampaignROI({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
    </svg>
  );
}

function IconSalesCoach({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v1h8v-1zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-1a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v1h-3zM4.75 14.094A5.973 5.973 0 004 17v1H1v-1a3 3 0 013.75-2.906z" />
    </svg>
  );
}

function IconPricingOptimizer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M17.707 9.293l-7-7A1 1 0 0 0 10 2H4a2 2 0 0 0-2 2v6a1 1 0 0 0 .293.707l7 7a1 1 0 0 0 1.414 0l7-7a1 1 0 0 0 0-1.414zM6 7a1 1 0 1 1 0-2 1 1 0 0 1 0 2z" clipRule="evenodd" />
    </svg>
  );
}

function IconRevenueForecaster({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M5 3a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V5a2 2 0 00-2-2H5zm9 4a1 1 0 10-2 0v6a1 1 0 102 0V7zm-3 2a1 1 0 10-2 0v4a1 1 0 102 0V9zm-3 3a1 1 0 10-2 0v1a1 1 0 102 0v-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconChurnPredictor({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" clipRule="evenodd" />
    </svg>
  );
}

function IconLeadEnrichment({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-.293.707L13 9.414V15a1 1 0 01-.553.894l-4 2A1 1 0 017 17V9.414L3.293 5.707A1 1 0 013 5V4zm2 1v.586l3.707 3.707A1 1 0 019 10v6l2-1v-5a1 1 0 01.293-.707L15 5.586V5H5z" clipRule="evenodd" />
      <path d="M15 13a1 1 0 100 2h2a1 1 0 100-2h-2zm0-3a1 1 0 100 2h2a1 1 0 100-2h-2z" />
    </svg>
  );
}

function IconExpansionRevenue({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 1.414L10.586 9H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z" clipRule="evenodd" />
    </svg>
  );
}

function IconObjectionIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
    </svg>
  );
}

function IconWinLossIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3.586L7.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 10.586V7z" clipRule="evenodd" />
      <path d="M5.293 4.707a1 1 0 011.414 0L10 8l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
    </svg>
  );
}

function IconCustomerSuccessPlaybook({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
    </svg>
  );
}

function IconTerritoryOptimizer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
    </svg>
  );
}

function IconContractRenewal({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
    </svg>
  );
}

function IconPriceOptimization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
    </svg>
  );
}

function IconCompetitiveBattlecard({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 1.944A11.954 11.954 0 012.166 5C2.056 5.649 2 6.319 2 7c0 5.225 3.34 9.67 8 11.317C14.66 16.67 18 12.225 18 7c0-.682-.057-1.35-.166-2.001A11.954 11.954 0 0110 1.944zM11 14a1 1 0 11-2 0 1 1 0 012 0zm0-7a1 1 0 10-2 0v3a1 1 0 102 0V7z" clipRule="evenodd" />
    </svg>
  );
}

function IconDealRiskAnalyzer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconAccountHealthScorer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
    </svg>
  );
}

function IconForecastAccuracy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm2 10a1 1 0 10-2 0v2a1 1 0 102 0v-2zm2-5a1 1 0 011 1v6a1 1 0 11-2 0V8a1 1 0 011-1zm4 3a1 1 0 10-2 0v3a1 1 0 102 0v-3z" clipRule="evenodd" />
    </svg>
  );
}

function IconOnboardingRisk({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
    </svg>
  );
}

function IconRenewalIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
    </svg>
  );
}

function IconPipelineGap({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 3a1 1 0 000 2h11a1 1 0 100-2H3zm0 4a1 1 0 000 2h7a1 1 0 100-2H3zm0 4a1 1 0 100 2h4a1 1 0 100-2H3zm10 1a1 1 0 011-1h.5a1 1 0 110 2H14a1 1 0 01-1-1zm3-1a1 1 0 100 2h.5a1 1 0 100-2H16z" clipRule="evenodd" />
    </svg>
  );
}

function IconSalesVelocity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
    </svg>
  );
}

function IconCompetitiveWinLoss({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M9 12l-4-4 1.41-1.41L9 9.17l7.59-7.58L18 3z" />
      <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0-4a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconCLV({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
    </svg>
  );
}

function IconPipelineHealth({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" clipRule="evenodd" />
    </svg>
  );
}

function IconAccountPenetration({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
    </svg>
  );
}

function IconCompetitiveIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 1.944A11.954 11.954 0 012.166 5C2.056 5.649 2 6.319 2 7c0 5.225 3.34 9.67 8 11.317C14.66 16.67 18 12.225 18 7c0-.682-.057-1.35-.166-2.001A11.954 11.954 0 0110 1.944zM11 14a1 1 0 11-2 0 1 1 0 012 0zm0-7a1 1 0 10-2 0v3a1 1 0 102 0V7z" clipRule="evenodd" />
    </svg>
  );
}

function IconMeetingIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
    </svg>
  );
}

function IconForecastCommit({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm2 10a1 1 0 10-2 0v2a1 1 0 102 0v-2zm2-5a1 1 0 011 1v6a1 1 0 11-2 0V8a1 1 0 011-1zm4 3a1 1 0 10-2 0v3a1 1 0 102 0v-3z" clipRule="evenodd" />
    </svg>
  );
}

function IconDealMomentum({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
    </svg>
  );
}

function IconCompetitivePositioning({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 1.944A11.954 11.954 0 012.166 5C2.056 5.649 2 6.319 2 7c0 5.225 3.34 9.67 8 11.317C14.66 16.67 18 12.225 18 7c0-.682-.057-1.35-.166-2.001A11.954 11.954 0 0110 1.944zM11 14a1 1 0 11-2 0 1 1 0 012 0zm0-7a1 1 0 10-2 0v3a1 1 0 102 0V7z" clipRule="evenodd" />
    </svg>
  );
}

function IconPriceNegotiation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z" clipRule="evenodd" />
    </svg>
  );
}

function IconSalesCapacity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
      <path fillRule="evenodd" d="M16 8a1 1 0 011 1v4a1 1 0 11-2 0V9a1 1 0 011-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconDealVelocity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
      <circle cx="4" cy="10" r="1.5" />
      <circle cx="7" cy="7" r="1.5" />
      <circle cx="10" cy="5" r="1.5" />
    </svg>
  );
}

function IconSalesForecast({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" clipRule="evenodd" />
      <path d="M4 13l3-3 3 2 3-4 2 1" stroke="currentColor" strokeWidth="1" fill="none" strokeLinecap="round" strokeLinejoin="round" opacity="0.6" />
    </svg>
  );
}

function IconCompWinRate({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 2a8 8 0 100 16A8 8 0 0010 2zm0 2a6 6 0 110 12A6 6 0 0110 4z" clipRule="evenodd" opacity="0.3" />
      <path d="M10 5v5l3 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" fill="none" />
      <path d="M6 8l-2-2M14 8l2-2M10 14v2" stroke="currentColor" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.6" />
    </svg>
  );
}

function IconSalesRepBurnout({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2a5 5 0 100 10A5 5 0 0010 2zm0 2a3 3 0 110 6A3 3 0 0110 4z" opacity="0.5" />
      <path d="M10 9v3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" fill="none" />
      <circle cx="10" cy="14" r="1" />
      <path d="M2 17c0-2.2 3.6-4 8-4s8 1.8 8 4" opacity="0.3" />
      <path d="M15 4l1-1M5 4L4 3" stroke="currentColor" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.4" />
    </svg>
  );
}

function IconDealFragmentation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
      <path d="M6 5l-2-2M14 5l2-2M10 3V1" stroke="currentColor" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.4" />
    </svg>
  );
}

function IconMutualActionPlan({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" opacity="0.7" />
      <path d="M6 11l2 2 4-4" stroke="#34d399" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
    </svg>
  );
}

function IconEmailSentimentTracker({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" opacity="0.7" />
      <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" opacity="0.5" />
      <path d="M14 11l-3 3-1-1" stroke="#34d399" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" fill="none" />
    </svg>
  );
}

function IconRevenueLeakDetector({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" opacity="0.7" />
      <path d="M10 12v2M9 13h2" stroke="#f87171" strokeWidth="1.2" strokeLinecap="round" fill="none" />
    </svg>
  );
}

function IconConversationIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" opacity="0.7" />
    </svg>
  );
}

function IconObjectionPatternAnalyzer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" opacity="0.8" />
    </svg>
  );
}

function IconBuyingCommitteeMapper({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v1h8v-1zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-1a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v1h-3zM4.75 12.094A5.973 5.973 0 004 15v1H1v-1a3 3 0 013.75-2.906z" opacity="0.7" />
    </svg>
  );
}

function IconChampionRiskMonitor({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" opacity="0.7" />
      <path d="M13 14l-3-3-1 1" stroke="#f87171" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" fill="none" />
    </svg>
  );
}

function IconForecastConfidenceScorer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" clipRule="evenodd" opacity="0.7" />
    </svg>
  );
}

function IconDealVelocityTracker({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2a8 8 0 100 16A8 8 0 0010 2zm0 2a6 6 0 110 12A6 6 0 0110 4z" opacity="0.4" />
      <path d="M10 6v4l3 3" stroke="#818cf8" strokeWidth="1.5" strokeLinecap="round" fill="none" />
      <path d="M5 10h1M14 10h1M10 5v1" stroke="#818cf8" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.6" />
    </svg>
  );
}

function IconGhostingPredictor({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 2a7 7 0 00-7 7c0 2.5 1.3 4.7 3.2 6l.8.6V18h6v-2.4l.8-.6A7 7 0 0010 2zm-1 13h2v1H9v-1z" clipRule="evenodd" opacity="0.6" />
      <path d="M8 7c0-.6.4-1 1-1s1 .4 1 1-.4 1-1 1-1-.4-1-1zm3 0c0-.6.4-1 1-1s1 .4 1 1-.4 1-1 1-1-.4-1-1z" fill="#f87171" />
    </svg>
  );
}

function IconTerritoryWhitespace({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" opacity="0.7" />
      <path d="M8 10h4M10 8v4" stroke="#22d3ee" strokeWidth="1.2" strokeLinecap="round" fill="none" />
    </svg>
  );
}

function IconProspectDigitalFootprint({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" opacity="0.6" />
      <circle cx="10" cy="10" r="3" opacity="0.0" />
      <path d="M3 10a7 7 0 017-7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" fill="none" opacity="0.5" />
      <circle cx="16" cy="4" r="2.5" fill="#34d399" opacity="0.9" />
    </svg>
  );
}

function IconCallToneAnalyzer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z" opacity="0.7" />
      <path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z" />
      <path d="M6 8.5a.5.5 0 111 0 .5.5 0 01-1 0zm2.5 0a.5.5 0 111 0 .5.5 0 01-1 0zm2.5 0a.5.5 0 111 0 .5.5 0 01-1 0z" fill="#34d399" opacity="0.9" />
    </svg>
  );
}

function IconContractClauseRisk({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h4a1 1 0 100-2H7z" clipRule="evenodd" />
      <path d="M10 10.5a.5.5 0 11-1 0 .5.5 0 011 0zm0-3a.5.5 0 11-1 0 .5.5 0 011 0z" fill="#f87171" opacity="0.9" />
    </svg>
  );
}

function IconBuyerPersonaDrift({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="7" cy="6" r="3" />
      <path d="M1 17c0-3.3 2.7-6 6-6" opacity="0.5" />
      <circle cx="14" cy="9" r="2.5" opacity="0.7" />
      <path d="M9 17c0-2.8 2.2-5 5-5" opacity="0.35" />
      <path d="M10 4l3 3-3 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.8" />
    </svg>
  );
}

function IconCustomerExpansion({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="6" r="3" opacity="0.8" />
      <path d="M2 17c0-3.3 3.6-6 8-6s8 2.7 8 6" opacity="0.35" />
      <path fillRule="evenodd" d="M14 10a1 1 0 011 1v2h2a1 1 0 110 2h-2v2a1 1 0 11-2 0v-2h-2a1 1 0 110-2h2v-2a1 1 0 011-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconSalesCompIntel({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
      <path d="M15 3l-1.5 1.5M17 5l-1.5 1.5" stroke="currentColor" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.5" />
    </svg>
  );
}

function IconPricingElasticity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 14l4-4 3 3 4-6 3 2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <circle cx="7" cy="10" r="1.2" />
      <circle cx="10" cy="13" r="1.2" />
      <circle cx="14" cy="7" r="1.2" />
      <path fillRule="evenodd" d="M15 3a1 1 0 011 1v1h1a1 1 0 110 2h-1v1a1 1 0 11-2 0V7h-1a1 1 0 110-2h1V4a1 1 0 011-1z" clipRule="evenodd" opacity="0.6" />
    </svg>
  );
}

function IconRevenueLeakage({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V5z" clipRule="evenodd" opacity="0.5" />
      <path d="M8 10l-3 3M15 6l-3 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" fill="none" />
      <circle cx="5" cy="13" r="1.5" />
      <circle cx="12" cy="9" r="1.5" />
    </svg>
  );
}

function IconAccountScoring({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="6" r="3" />
      <path d="M2 17c0-3.3 3.6-6 8-6s8 2.7 8 6" opacity="0.4" />
      <path d="M12 12l1 1.5 2.5-3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
    </svg>
  );
}

function IconTerritoryPerformance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
      <path d="M10 7v1M10 12v1" stroke="white" strokeWidth="0.8" strokeLinecap="round" fill="none" opacity="0.6" />
      <path d="M13 8.5l1-1M7 8.5l-1-1" stroke="white" strokeWidth="0.8" strokeLinecap="round" fill="none" opacity="0.4" />
    </svg>
  );
}

function IconPipelineCoverage({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 6a1 1 0 011-1h8a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h5a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
      <circle cx="16" cy="14" r="3" opacity="0.8" />
      <path d="M15 14l1 1 1.5-1.5" stroke="white" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" fill="none" />
    </svg>
  );
}

function IconCustomerOnboarding({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
    </svg>
  );
}

function IconAccountExpansion({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 1.414L10.586 9H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z" clipRule="evenodd" />
      <path d="M5 14a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z" />
    </svg>
  );
}

function IconPartnerChannel({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v1h8v-1zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-1a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v1h-3zM4.75 14.094A5.973 5.973 0 004 17v1H1v-1a3 3 0 013.75-2.906z" />
    </svg>
  );
}

function IconQuotaGap({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" clipRule="evenodd" />
    </svg>
  );
}

function IconRevenueAttribution({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
    </svg>
  );
}

function IconEmailPersonalization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
      <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
      <path d="M14 11a1 1 0 100 2h2a1 1 0 100-2h-2zm0-3a1 1 0 100 2h2a1 1 0 100-2h-2z" fillOpacity="0.5" />
    </svg>
  );
}

function IconStakeholderMap({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
      <path d="M10 10a1 1 0 100-2 1 1 0 000 2zm3 2a1 1 0 100-2 1 1 0 000 2zm-6 0a1 1 0 100-2 1 1 0 000 2z" fillOpacity="0.5" />
    </svg>
  );
}

function IconSalesSkills({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 8.75l1.922.825a1 1 0 00.788 0l7-3a1 1 0 000-1.838l-7-3z" />
      <path d="M3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
    </svg>
  );
}

function IconBuyerIntent({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 2a8 8 0 100 16A8 8 0 0010 2zm0 2a6 6 0 110 12A6 6 0 0110 4z" clipRule="evenodd" opacity="0.3" />
      <path fillRule="evenodd" d="M10 5a5 5 0 110 10A5 5 0 0110 5zm0 2a3 3 0 100 6 3 3 0 000-6z" clipRule="evenodd" opacity="0.6" />
      <circle cx="10" cy="10" r="1.5" />
      <path d="M10 1v2M10 17v2M1 10h2M17 10h2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" fill="none" />
    </svg>
  );
}

function IconRepActivity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
      <path fillRule="evenodd" d="M15 8a1 1 0 011 1l.01 3H17a1 1 0 110 2h-1l-.01 1a1 1 0 11-2 0V14h-1a1 1 0 110-2h1V9a1 1 0 011-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconDealStageProgression({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 3a1 1 0 000 2h14a1 1 0 100-2H3zm2 4a1 1 0 000 2h10a1 1 0 100-2H5zm2 4a1 1 0 000 2h6a1 1 0 100-2H7zm2 4a1 1 0 000 2h2a1 1 0 100-2H9z" clipRule="evenodd" />
    </svg>
  );
}

function IconQuotaAttainment({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 2a8 8 0 100 16A8 8 0 0010 2zm0 2a6 6 0 110 12A6 6 0 0110 4z" clipRule="evenodd" opacity="0.4" />
      <path fillRule="evenodd" d="M10 5a5 5 0 110 10A5 5 0 0110 5zm0 2a3 3 0 100 6 3 3 0 000-6z" clipRule="evenodd" opacity="0.7" />
      <circle cx="10" cy="10" r="1.5" />
      <path d="M10 2v2M10 16v2M2 10h2M16 10h2M4.22 4.22l1.42 1.42M14.36 14.36l1.42 1.42" stroke="currentColor" strokeWidth="1" strokeLinecap="round" fill="none" />
    </svg>
  );
}

function IconLeadScoringIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
    </svg>
  );
}

function IconSalesCoachingEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 8.75l1.922.825a1 1 0 00.788 0l7-3a1 1 0 000-1.838l-7-3z" />
      <path d="M3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
    </svg>
  );
}

function IconPipelineVelocity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
    </svg>
  );
}

function IconOnboardingHealth({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
    </svg>
  );
}

function IconCompetitorIntel({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 1.944A11.954 11.954 0 012.166 5C2.056 5.649 2 6.319 2 7c0 5.225 3.34 9.67 8 11.317C14.66 16.67 18 12.225 18 7c0-.682-.057-1.35-.166-2.001A11.954 11.954 0 0110 1.944zM11 14a1 1 0 11-2 0 1 1 0 012 0zm0-7a1 1 0 10-2 0v3a1 1 0 102 0V7z" clipRule="evenodd" />
    </svg>
  );
}

function IconEmailSequence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 4a1 1 0 011-1h1a1 1 0 010 2H3a1 1 0 01-1-1zm4 0a1 1 0 011-1h10a1 1 0 110 2H7a1 1 0 01-1-1zM2 9a1 1 0 011-1h1a1 1 0 010 2H3a1 1 0 01-1-1zm4 0a1 1 0 011-1h10a1 1 0 110 2H7a1 1 0 01-1-1zM2 14a1 1 0 011-1h1a1 1 0 110 2H3a1 1 0 01-1-1zm4 0a1 1 0 011-1h10a1 1 0 110 2H7a1 1 0 01-1-1z" />
    </svg>
  );
}

function IconICPScorer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
    </svg>
  );
}

function IconAccountHealth({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
    </svg>
  );
}

function IconThreatIntel({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 1.944A11.954 11.954 0 012.166 5C2.056 5.649 2 6.319 2 7c0 5.225 3.34 9.67 8 11.317C14.66 16.67 18 12.225 18 7c0-.682-.057-1.35-.166-2.001A11.954 11.954 0 0110 1.944zM11 14a1 1 0 11-2 0 1 1 0 012 0zm0-7a1 1 0 10-2 0v3a1 1 0 102 0V7z" clipRule="evenodd" />
    </svg>
  );
}

function IconProposals({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h4a1 1 0 100-2H7z" clipRule="evenodd" />
    </svg>
  );
}

function IconRevenue({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
    </svg>
  );
}

function IconSecurity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
    </svg>
  );
}

function IconRetention({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
    </svg>
  );
}

function IconPriority({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
    </svg>
  );
}

function IconScorer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 9a1 1 0 000 2h2a1 1 0 100-2H7zm5 0a1 1 0 00-1 1v3a1 1 0 102 0v-3a1 1 0 00-1-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconScorecard({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h7a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h4a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconComposer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
    </svg>
  );
}

function IconForecast({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M5 3a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V5a2 2 0 00-2-2H5zm9 4a1 1 0 10-2 0v6a1 1 0 102 0V7zm-3 2a1 1 0 10-2 0v4a1 1 0 102 0V9zm-3 3a1 1 0 10-2 0v1a1 1 0 102 0v-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconObjection({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
    </svg>
  );
}

function IconSentiment({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
    </svg>
  );
}

function IconTemplates({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" />
    </svg>
  );
}

function IconPerformance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" clipRule="evenodd" />
    </svg>
  );
}

function IconDedup({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 4a1 1 0 011-1h4a1 1 0 010 2H6.414l2.293 2.293a1 1 0 01-1.414 1.414L5 6.414V8a1 1 0 01-2 0V4zm9 1a1 1 0 010-2h4a1 1 0 011 1v4a1 1 0 01-2 0V6.414l-2.293 2.293a1 1 0 11-1.414-1.414L13.586 5H12zm-9 7a1 1 0 012 0v1.586l2.293-2.293a1 1 0 111.414 1.414L6.414 15H8a1 1 0 010 2H4a1 1 0 01-1-1v-4zm13-1a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 010-2h1.586l-2.293-2.293a1 1 0 111.414-1.414L15 13.586V12a1 1 0 011-1z" clipRule="evenodd" />
    </svg>
  );
}

function IconTiming({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
    </svg>
  );
}

function IconWorkflow({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
    </svg>
  );
}

function IconReply({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M7.707 3.293a1 1 0 010 1.414L5.414 7H11a7 7 0 017 7v2a1 1 0 11-2 0v-2a5 5 0 00-5-5H5.414l2.293 2.293a1 1 0 11-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
    </svg>
  );
}

function IconFollowUp({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 14a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 5.677V16h3a1 1 0 110 2H6a1 1 0 110-2h3V5.677L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1z" />
    </svg>
  );
}

function IconSwarm({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="4" r="2" />
      <circle cx="4" cy="14" r="2" />
      <circle cx="16" cy="14" r="2" />
      <circle cx="10" cy="10" r="1.5" />
      <path d="M10 6L4 12M10 6L16 12M10 6v2.5M4 12l4-1M16 12l-4-1" strokeWidth="1" stroke="currentColor" fill="none" />
    </svg>
  );
}

function IconSettings({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 0 1-2.286.948c-1.372-.836-2.942.734-2.106 2.106a1.533 1.533 0 0 1-.948 2.287c-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 0 1 .948 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 0 1 2.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 0 1 2.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 0 1 .947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 0 1-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 0 1-2.287-.947zM10 13a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconProspectEngagementVelocity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 12l3-3 2 2 3-4 3 2 3-3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <circle cx="5" cy="9" r="1.2" fill="#34d399" />
      <circle cx="7" cy="11" r="1.2" fill="#34d399" />
      <circle cx="10" cy="7" r="1.2" fill="#818cf8" />
      <circle cx="13" cy="9" r="1.2" fill="#818cf8" />
      <circle cx="16" cy="6" r="1.2" fill="#fbbf24" />
    </svg>
  );
}

function IconSalesDataIntegrityMonitor({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" opacity={0.8} />
    </svg>
  );
}

function IconAccountExpansionIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 10a7 7 0 1114 0A7 7 0 013 10z" stroke="currentColor" strokeWidth="1.2" fill="none" opacity="0.4" />
      <path d="M10 6v4l3 2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <path d="M14 2l2 2-2 2M6 2L4 4l2 2" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.7" />
    </svg>
  );
}

function IconCustomerReferralIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="6" r="2.5" fill="currentColor" opacity={0.5} />
      <circle cx="4" cy="13" r="2" fill="currentColor" opacity={0.4} />
      <circle cx="16" cy="13" r="2" fill="currentColor" opacity={0.4} />
      <path d="M10 8.5L4.5 11.5M10 8.5L15.5 11.5" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
      <path d="M4.5 13L8 16M15.5 13L12 16" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.7" />
    </svg>
  );
}

function IconDealComplexityIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="10" r="7" fill="none" stroke="currentColor" strokeWidth="1.2" opacity={0.4} />
      <circle cx="10" cy="10" r="4" fill="none" stroke="currentColor" strokeWidth="1.5" opacity={0.6} />
      <circle cx="10" cy="10" r="1.5" fill="currentColor" opacity={0.8} />
      <path d="M10 3v4M10 13v4M3 10h4M13 10h4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.5" />
    </svg>
  );
}

function IconPipelineAgingIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="2" y="14" width="3" height="4" rx="1" fill="currentColor" opacity={0.4} />
      <rect x="6" y="10" width="3" height="8" rx="1" fill="currentColor" opacity={0.5} />
      <rect x="10" y="6" width="3" height="12" rx="1" fill="currentColor" opacity={0.6} />
      <rect x="14" y="2" width="3" height="16" rx="1" fill="currentColor" opacity={0.8} />
      <path d="M2 14L6 10L10 6L14 2" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.5" />
    </svg>
  );
}

function IconRepAttritionRiskEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="7" r="3" fill="currentColor" opacity={0.5} />
      <path d="M5 17c0-3.314 2.239-6 5-6s5 2.686 5 6" stroke="currentColor" strokeWidth="1.3" fill="none" strokeLinecap="round" opacity="0.7" />
      <path d="M15 5l2 2M15 7l2-2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

function IconCompetitiveWinProbabilityEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2l2 5h5l-4 3 1.5 5L10 12l-4.5 3L7 10 3 7h5z" fill="currentColor" opacity={0.8} />
    </svg>
  );
}

function IconDealContaminationRiskEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="10" r="7" fill="none" stroke="currentColor" strokeWidth="1.2" opacity={0.3} />
      <path d="M10 4v6l3 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" fill="none" opacity="0.6" />
      <path d="M7 3.5L5 5M13 3.5L15 5M4 9H2M18 9H16" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.5" />
      <circle cx="10" cy="10" r="1.5" fill="currentColor" opacity={0.9} />
    </svg>
  );
}

function IconSalesCapacityPlanningEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="4" cy="14" r="2" fill="currentColor" opacity={0.5} />
      <circle cx="9" cy="10" r="2" fill="currentColor" opacity={0.6} />
      <circle cx="14" cy="6" r="2" fill="currentColor" opacity={0.7} />
      <path d="M4 16h3M9 12h3M14 8h3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.6" />
      <path d="M4 14L9 10L14 6" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeDasharray="2 2" fill="none" opacity="0.4" />
    </svg>
  );
}

function IconForecastCalibrationEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="2" y="12" width="3" height="6" rx="0.5" fill="currentColor" opacity={0.4} />
      <rect x="6.5" y="8" width="3" height="10" rx="0.5" fill="currentColor" opacity={0.6} />
      <rect x="11" y="4" width="3" height="14" rx="0.5" fill="currentColor" opacity={0.8} />
      <path d="M3.5 12L8 8L12.5 4" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" fill="none" opacity="0.6" />
      <circle cx="14.5" cy="4" r="1.5" fill="currentColor" opacity={0.9} />
      <path d="M13 8l2-2M13 6l2 2" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.7" />
    </svg>
  );
}

function IconQuotaFairnessEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2l1.5 4.5h4.5l-3.6 2.7 1.4 4.3L10 11l-3.8 2.5 1.4-4.3L4 6.5h4.5z" fill="currentColor" opacity={0.7} />
      <path d="M3 16h6M11 16h6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.6" />
      <circle cx="6" cy="16" r="1.2" fill="currentColor" opacity={0.8} />
      <circle cx="14" cy="16" r="1.2" fill="currentColor" opacity={0.8} />
    </svg>
  );
}

function IconDealMultithreadingIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="4" r="2" fill="currentColor" opacity={0.6} />
      <circle cx="3" cy="16" r="2" fill="currentColor" opacity={0.5} />
      <circle cx="10" cy="16" r="2" fill="currentColor" opacity={0.5} />
      <circle cx="17" cy="16" r="2" fill="currentColor" opacity={0.5} />
      <path d="M10 6L3 14M10 6L10 14M10 6L17 14" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" opacity="0.8" />
    </svg>
  );
}

function IconSalesProcessCompliance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" opacity="0.5" />
      <path d="M4 4h12M4 8h8M4 12h5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.7" />
    </svg>
  );
}

function IconRepRampIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 14l4-8 3 4 3-6 4 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <path fillRule="evenodd" d="M15 3a1 1 0 011 1v1h1a1 1 0 110 2h-1v1a1 1 0 11-2 0V7h-1a1 1 0 110-2h1V4a1 1 0 011-1z" clipRule="evenodd" opacity="0.7" />
    </svg>
  );
}

function IconWinLossPatternEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 7l4 4 3-3 4 4 3-3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <circle cx="7" cy="11" r="1.5" fill="#34d399" />
      <circle cx="10" cy="8" r="1.5" fill="#f87171" />
      <circle cx="14" cy="12" r="1.5" fill="#34d399" />
      <path fillRule="evenodd" d="M2 15a1 1 0 011-1h14a1 1 0 110 2H3a1 1 0 01-1-1z" clipRule="evenodd" opacity="0.4" />
    </svg>
  );
}

function IconCustomerSentimentDecayEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 14l3-6 3 4 3-8 3 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.8" />
      <path d="M3 14l3-6 3 4 3-8 3 4" stroke="#ef4444" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.3" transform="translate(0, 2)" />
      <path d="M2 17h16" stroke="currentColor" strokeWidth="0.8" strokeLinecap="round" fill="none" opacity="0.3" />
      <circle cx="6" cy="8" r="1.5" fill="#f59e0b" opacity="0.8" />
      <circle cx="9" cy="12" r="1.5" fill="#f97316" opacity="0.8" />
      <circle cx="12" cy="4" r="1.5" fill="#ef4444" opacity="0.8" />
      <circle cx="15" cy="8" r="1.5" fill="#f97316" opacity="0.8" />
    </svg>
  );
}

function IconSalesCommissionClawbackRiskEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" opacity="0.6" />
      <path d="M6 3l-2 2M14 3l2 2" stroke="#f87171" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.8" />
      <path d="M3 9h2M15 9h2" stroke="currentColor" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.4" />
    </svg>
  );
}

function IconSalesProcessVelocityAnomalyEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 16l4-8 3 4 3-10 3 6 2-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.7" />
      <circle cx="6" cy="8" r="1.2" fill="#f59e0b" opacity="0.9" />
      <circle cx="9" cy="12" r="1.2" fill="#f97316" opacity="0.9" />
      <circle cx="12" cy="2" r="1.2" fill="#ef4444" opacity="0.9" />
      <circle cx="15" cy="8" r="1.2" fill="#f97316" opacity="0.9" />
      <path d="M1 17h18" stroke="currentColor" strokeWidth="0.6" strokeLinecap="round" fill="none" opacity="0.25" />
      <path d="M17 4l1 -1.5M18 4l-1-1.5" stroke="#ef4444" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.8" />
    </svg>
  );
}

function IconSalesForecastSandbaggingDetector({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 14l4-2 3 1 3-3 4 -1" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.6" />
      <path d="M2 8l4-5 3 2 3-4 4 1" stroke="#f59e0b" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.8" />
      <path d="M6 9v5M9 11v3M12 8v6M16 9v5" stroke="currentColor" strokeWidth="1" strokeLinecap="round" fill="none" opacity="0.2" />
      <rect x="4" y="13" width="4" height="4" rx="0.5" fill="#f59e0b" opacity="0.3" />
      <rect x="10" y="11" width="4" height="6" rx="0.5" fill="#f97316" opacity="0.3" />
      <path d="M16 4a2 2 0 100 -4 2 2 0 000 4z" stroke="#ef4444" strokeWidth="1" fill="none" opacity="0.7" />
      <path d="M15.3 1.7l1 1 1.5-1.5" stroke="#ef4444" strokeWidth="0.9" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0" />
    </svg>
  );
}

function IconCRMDataQualityRiskEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L13 11.414V15a1 1 0 01-.553.894l-4 2A1 1 0 017 17v-5.586L3.293 7.707A1 1 0 013 7V4z" opacity="0.3" />
      <path d="M5 4h10M5 4v2h10V4" stroke="currentColor" strokeWidth="0.8" fill="none" opacity="0.5" />
      <circle cx="15" cy="15" r="4" fill="currentColor" opacity="0.15" />
      <path d="M13.5 15.5l1 1 2-2" stroke="#f87171" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.9" />
      <circle cx="15" cy="15" r="4" stroke="#f87171" strokeWidth="0.9" fill="none" opacity="0.6" />
    </svg>
  );
}

function IconDealGhostingRiskEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2a7 7 0 110 14A7 7 0 0110 2z" opacity="0.2" />
      <path d="M10 2a7 7 0 110 14A7 7 0 0110 2z" fill="none" stroke="currentColor" strokeWidth="1.2" opacity="0.5" />
      <path d="M7 8c0-1.66 1.34-3 3-3s3 1.34 3 3c0 1.2-.7 2.24-1.73 2.74L11 13H9l-.27-2.26A3 3 0 017 8z" opacity="0.5" />
      <circle cx="10" cy="15" r="0.8" opacity="0.8" />
      <path d="M14 3l3 3-3 3" stroke="#fbbf24" strokeWidth="1.2" fill="none" strokeLinecap="round" opacity="0.0" />
      <path d="M16 6h-4" stroke="#fbbf24" strokeWidth="0.0" fill="none" />
      <path d="M4 4l12 12" stroke="#f87171" strokeWidth="1.5" strokeLinecap="round" opacity="0.6" />
    </svg>
  );
}

function IconSalesQuotaGamingDetectionEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 14l3-7 3 4 3-6 3 3" stroke="currentColor" strokeWidth="1.5" fill="none" strokeLinecap="round" strokeLinejoin="round" opacity="0.7" />
      <rect x="2" y="15" width="16" height="1.5" rx="0.75" opacity="0.3" />
      <path d="M14 2l2 2-2 2M16 4H11" stroke="#fbbf24" strokeWidth="1.3" strokeLinecap="round" fill="none" opacity="0.9" />
      <circle cx="15" cy="15" r="3.5" fill="#f87171" opacity="0.9" />
      <path d="M13.5 15h3M15 13.5v3" stroke="white" strokeWidth="1.3" strokeLinecap="round" fill="none" />
    </svg>
  );
}

function IconSalesDataExfiltrationRiskEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M4 3h12a1 1 0 011 1v8a1 1 0 01-1 1H4a1 1 0 01-1-1V4a1 1 0 011-1z" opacity="0.25" />
      <path d="M7 8h6M7 11h4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.6" />
      <circle cx="15" cy="15" r="4" fill="#f87171" opacity="0.9" />
      <path d="M15 13v2.5M15 16.5v.5" stroke="white" strokeWidth="1.4" strokeLinecap="round" fill="none" />
    </svg>
  );
}

function IconCompetitorWinLossIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 14l4-6 4 3 4-8 2 1" stroke="currentColor" strokeWidth="1.5" fill="none" strokeLinecap="round" strokeLinejoin="round" opacity="0.8" />
      <circle cx="3" cy="14" r="1.5" opacity="0.8" />
      <circle cx="7" cy="8" r="1.5" opacity="0.8" />
      <circle cx="11" cy="11" r="1.5" fill="#f87171" />
      <circle cx="15" cy="3" r="1.5" opacity="0.8" />
      <path d="M13 15l2-2 2 2-2 2-2-2z" opacity="0.5" />
    </svg>
  );
}

function IconAccountExecutiveRampVelocityEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 16l4-8 3 5 3-9 4 6" stroke="currentColor" strokeWidth="1.5" fill="none" strokeLinecap="round" strokeLinejoin="round" opacity="0.8" />
      <circle cx="10" cy="10" r="4" fill="none" stroke="currentColor" strokeWidth="1.2" opacity="0.3" />
      <circle cx="10" cy="10" r="4" fill="none" stroke="#34d399" strokeWidth="1.2"
        strokeDasharray="12 13" strokeLinecap="round" opacity="0.9" />
      <path d="M10 8v2.5l1.5 1" stroke="#34d399" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.9" />
      <path d="M15 4l1.5 1.5-1.5 1.5" stroke="#818cf8" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.8" />
    </svg>
  );
}

function IconSalesTerritoryOverlapConflictEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M4 4h5v5H4V4z" opacity="0.4" />
      <path d="M11 4h5v5h-5V4z" opacity="0.4" />
      <path d="M4 11h5v5H4v-5z" opacity="0.4" />
      <path d="M11 11h5v5h-5v-5z" opacity="0.4" />
      <circle cx="10" cy="10" r="3.5" fill="#f87171" opacity="0.85" />
      <path d="M8.5 10h3M10 8.5v3" stroke="white" strokeWidth="1.3" strokeLinecap="round" fill="none" />
    </svg>
  );
}

function IconSalesRepCapacityOverloadDetector({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" strokeWidth="1.5" opacity="0.3" />
      <circle cx="10" cy="10" r="8" fill="none" stroke="#fb923c" strokeWidth="1.5"
        strokeDasharray="30 20" strokeLinecap="round" opacity="0.8" />
      <path d="M10 4v6l4 2" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.9" />
      <circle cx="10" cy="10" r="1.5" fill="currentColor" opacity="0.9" />
      <path d="M16 4l1.5 1.5-1.5 1.5" stroke="#f87171" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.8" />
      <path d="M17.5 5.5h-3.5" stroke="#f87171" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.0" />
    </svg>
  );
}

function IconSalesCoachingEffectivenessEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Person with upward trend arrow (coaching = growth) */}
      <circle cx="10" cy="5" r="2.5" fill="none" stroke="currentColor" strokeWidth="1.3" />
      <path d="M6 19v-2a4 4 0 0 1 8 0v2" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
      <path d="M14 13l2-2 2 2" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" opacity="0.7" />
      <path d="M16 11v5" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" opacity="0.7" />
    </svg>
  );
}

function IconSalesProposalConversionIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Document with checkmark and conversion arrow */}
      <rect x="4" y="2" width="10" height="13" rx="1.5" fill="none" stroke="currentColor" strokeWidth="1.3" />
      <line x1="7" y1="6" x2="11" y2="6" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
      <line x1="7" y1="9" x2="11" y2="9" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
      <path d="M12 15l2 2 3-3" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function IconSalesTerritoryCoverageIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Map with pins representing territory coverage */}
      <path d="M3 4l4 2 6-3 4 2v11l-4-2-6 3-4-2V4z" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" />
      <circle cx="7" cy="9" r="1.5" fill="currentColor" opacity="0.9" />
      <circle cx="13" cy="7" r="1.5" fill="currentColor" opacity="0.6" />
      <line x1="7" y1="10.5" x2="13" y2="8.5" stroke="currentColor" strokeWidth="0.8" strokeDasharray="2 1.5" opacity="0.5" />
    </svg>
  );
}

function IconSalesCustomerRelationshipHealthEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Heart with pulse line (relationship health) */}
      <path d="M10 16s-7-4.5-7-8.5A4 4 0 0 1 10 5a4 4 0 0 1 7 2.5C17 11.5 10 16 10 16z"
        fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
      <polyline points="4,10 7,10 8.5,7 10,13 11.5,10 13,10 16,10"
        fill="none" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" strokeLinejoin="round" opacity="0.8" />
    </svg>
  );
}

function IconSalesForecastAccuracyIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 14l4-5 3 3 3-4 4 2" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M3 3v14h14" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
      <circle cx="16" cy="10" r="1.2" fill="currentColor" opacity="0.7" />
      <polyline points="14,6 16,10 18,8" fill="none" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" strokeLinejoin="round" opacity="0.7" />
    </svg>
  );
}

function IconSalesCoachingReceptivityIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Person with brain/arrow showing receptivity or block */}
      <circle cx="10" cy="5.5" r="2.5" opacity="0.7"/>
      <path d="M5 18 C5 14 7 12 10 12 C13 12 15 14 15 18" opacity="0.5" strokeLinecap="round"/>
      <path d="M13 7 L16 7 L16 10" strokeLinecap="round" strokeLinejoin="round" opacity="0.8"/>
      <path d="M13.5 7.5 L15 9" strokeLinecap="round" opacity="0.5"/>
    </svg>
  );
}

function IconSalesAccountExpansionIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="10" r="3.5" fill="none" stroke="currentColor" strokeWidth="1.3" />
      <circle cx="10" cy="10" r="6.5" fill="none" stroke="currentColor" strokeWidth="1.1" opacity="0.5" strokeDasharray="2 2" />
      <path d="M13 7l3-3m0 0h-2.5m2.5 0v2.5" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M10 6.5V10m0 0h3.5" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
    </svg>
  );
}

function IconSalesMeetingQualityIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="2" y="3" width="16" height="11" rx="2" fill="none" stroke="currentColor" strokeWidth="1.3" />
      <circle cx="7" cy="8.5" r="1.5" fill="currentColor" opacity="0.7" />
      <circle cx="10" cy="8.5" r="1.5" fill="currentColor" opacity="0.7" />
      <circle cx="13" cy="8.5" r="1.5" fill="currentColor" opacity="0.7" />
      <path d="M10 14v3m-3-1.5h6" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
    </svg>
  );
}

function IconSalesPricingNegotiationIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M4 10h12M10 4v12" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" opacity="0.4" />
      <circle cx="10" cy="10" r="6.5" fill="none" stroke="currentColor" strokeWidth="1.3" />
      <path d="M7.5 12.5c0-1 1-2 2.5-2s2.5.8 2.5 2" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
      <path d="M8 8c0-.6.4-1 1-1h2a1 1 0 0 1 0 2h-2a1 1 0 0 0 0 2h2a1 1 0 0 1 0 2" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
    </svg>
  );
}

function IconSalesInboundLeadResponseEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 7h4m0 0V4m0 3L3 4" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" opacity="0.7" />
      <path d="M5 10h10M5 13h7" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.6" />
      <rect x="2" y="6" width="16" height="11" rx="2" fill="none" stroke="currentColor" strokeWidth="1.3" />
      <circle cx="15" cy="8" r="1.5" fill="currentColor" opacity="0.8" />
    </svg>
  );
}

function IconSalesCompetitiveWinLossIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Trophy/shield with crossed swords — competitive win/loss */}
      <path d="M10 2L4 5v5c0 3.5 2.5 6.5 6 7.5C16 16.5 16 14 16 10V5L10 2z"
        fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" />
      <line x1="7" y1="8" x2="13" y2="12" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.8" />
      <line x1="13" y1="8" x2="7" y2="12" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.8" />
      <circle cx="10" cy="10" r="1.5" fill="currentColor" opacity="0.7" />
    </svg>
  );
}

function IconSalesOutboundProspectingIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Megaphone/loudspeaker with outward arrows — outbound prospecting */}
      <path d="M3 8v4l2 1V7L3 8z" fill="currentColor" opacity="0.7" />
      <path d="M5 7v6l8 3V4L5 7z" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" />
      <line x1="13" y1="9" x2="17" y2="7" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.8" />
      <line x1="13" y1="11" x2="17" y2="13" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.8" />
      <line x1="13" y1="10" x2="17" y2="10" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.6" />
    </svg>
  );
}

function IconSalesQuotaAttainmentIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Target with progress bar — quota attainment */}
      <circle cx="10" cy="10" r="7" fill="none" stroke="currentColor" strokeWidth="1.3" opacity="0.6" />
      <circle cx="10" cy="10" r="4" fill="none" stroke="currentColor" strokeWidth="1.2" opacity="0.7" />
      <circle cx="10" cy="10" r="1.5" fill="currentColor" opacity="0.9" />
      <path d="M10 3v1.5M10 15.5V17M3 10h1.5M15.5 10H17" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" opacity="0.5" />
    </svg>
  );
}

function IconSalesStakeholderMappingIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Network nodes — stakeholder mapping */}
      <circle cx="10" cy="5" r="2" fill="currentColor" opacity="0.9" />
      <circle cx="4" cy="14" r="2" fill="currentColor" opacity="0.7" />
      <circle cx="16" cy="14" r="2" fill="currentColor" opacity="0.7" />
      <line x1="10" y1="7" x2="4" y2="12" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.6" />
      <line x1="10" y1="7" x2="16" y2="12" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.6" />
      <line x1="4" y1="14" x2="16" y2="14" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" strokeDasharray="2 1.5" opacity="0.5" />
    </svg>
  );
}

function IconSalesBuyerResponseLatencyIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Clock with response bubble — buyer latency */}
      <circle cx="9" cy="10" r="6" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <path d="M9 7v3.5l2 1.5" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M16 5h-2.5a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1H16l1 1.5V6a1 1 0 0 0-1-1z" fill="currentColor" opacity="0.6"/>
    </svg>
  );
}

function IconSalesPipelineContaminationIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Biohazard-inspired — pipeline contamination */}
      <circle cx="10" cy="10" r="2.5" fill="currentColor"/>
      <path d="M10 2a8 8 0 0 1 6.9 12" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" opacity="0.8"/>
      <path d="M10 2a8 8 0 0 0-6.9 12" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" opacity="0.8"/>
      <path d="M3.1 14h13.8" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" opacity="0.8"/>
      <circle cx="10" cy="2" r="1.2" fill="currentColor" opacity="0.5"/>
      <circle cx="3.1" cy="14" r="1.2" fill="currentColor" opacity="0.5"/>
      <circle cx="16.9" cy="14" r="1.2" fill="currentColor" opacity="0.5"/>
    </svg>
  );
}

function IconSalesDealMomentumIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Arrow acceleration — deal momentum */}
      <path d="M3 10h10" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
      <path d="M10 6l4 4-4 4" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M3 6h5" fill="none" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" opacity="0.5"/>
      <path d="M3 14h5" fill="none" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" opacity="0.5"/>
    </svg>
  );
}

function IconSalesMultiChannelEngagementIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Multiple signal waves — multi-channel */}
      <circle cx="10" cy="10" r="2" fill="currentColor"/>
      <path d="M6 6a6 6 0 0 0 0 8" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
      <path d="M14 6a6 6 0 0 1 0 8" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
      <path d="M3.5 3.5a9.5 9.5 0 0 0 0 13" fill="none" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" opacity="0.5"/>
      <path d="M16.5 3.5a9.5 9.5 0 0 1 0 13" fill="none" stroke="currentColor" strokeWidth="1.1" strokeLinecap="round" opacity="0.5"/>
    </svg>
  );
}

function IconSalesRepRetentionRiskIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Person silhouette with exit arrow — retention risk */}
      <circle cx="8" cy="5" r="2.5" fill="currentColor" opacity="0.85"/>
      <path d="M3 17c0-3.314 2.239-6 5-6s5 2.686 5 6" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
      <path d="M14 8h4M16 6l2 2-2 2" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.8"/>
    </svg>
  );
}

function IconSalesPipelineHygieneIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Funnel with checkmark and warning — pipeline hygiene */}
      <path d="M3 3h14l-5 6v6l-4-2V9L3 3z" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
      <path d="M7 7l1.5 1.5L11 6" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.9"/>
      <circle cx="15" cy="15" r="3.5" fill="currentColor" opacity="0.2"/>
      <text x="15" y="17" textAnchor="middle" fontSize="5" fill="currentColor" fontWeight="bold">!</text>
    </svg>
  );
}

function IconSalesBuyerIntentSignalIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Heartbeat / pulse line — buyer intent signal */}
      <path d="M2 10h3l2-5 3 10 2-7 2 3h4" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      <circle cx="10" cy="10" r="1.5" fill="currentColor" opacity="0.6"/>
    </svg>
  );
}

function IconSalesNegotiationEffectivenessIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Handshake / two hands crossing — negotiation */}
      <path d="M3 12l4-4 3 2 4-5" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M1 15c2-1 4 0 5-1s3-3 5-2 4 1 4 3" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" opacity="0.7"/>
      <circle cx="14" cy="5" r="1.5" fill="currentColor" opacity="0.8"/>
    </svg>
  );
}

function IconSalesForecastSanityCheckIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Magnifying glass over bar chart — forecast sanity check */}
      <rect x="2" y="12" width="3" height="5" rx="0.5" fill="currentColor" opacity="0.7"/>
      <rect x="6" y="9" width="3" height="8" rx="0.5" fill="currentColor" opacity="0.85"/>
      <rect x="10" y="6" width="3" height="11" rx="0.5" fill="currentColor"/>
      <circle cx="15.5" cy="6" r="3" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <line x1="17.6" y1="8.1" x2="19" y2="9.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesOnboardingEffectivenessIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Rocket launching with upward arrow — ramp velocity */}
      <path d="M10 2c0 0-5 4-5 9a5 5 0 0 0 10 0c0-5-5-9-5-9z" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round"/>
      <circle cx="10" cy="11" r="1.8" fill="currentColor"/>
      <path d="M7 17l-1.5 2M13 17l1.5 2" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" opacity="0.6"/>
      <path d="M10 2 L10 0" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.5"/>
    </svg>
  );
}

function IconSalesConversationQualityIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Microphone with sound waves — call quality */}
      <rect x="8" y="2" width="4" height="8" rx="2" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <path d="M5 9a5 5 0 0 0 10 0" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
      <line x1="10" y1="14" x2="10" y2="18" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
      <line x1="7" y1="18" x2="13" y2="18" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
      <path d="M3 7 A7 7 0 0 1 17 7" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" opacity="0.4"/>
    </svg>
  );
}

function IconSalesEmailSequenceIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Envelope with send arrow — email sequence */}
      <rect x="2" y="5" width="16" height="11" rx="2" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <polyline points="2,5 10,12 18,5" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round"/>
      <line x1="13" y1="13" x2="17" y2="13" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.6"/>
      <polyline points="15,11 17,13 15,15" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" opacity="0.6"/>
    </svg>
  );
}

function IconSalesMultithreadingIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Network nodes — stakeholder multithreading */}
      <circle cx="10" cy="4" r="2" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <circle cx="3" cy="15" r="2" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <circle cx="10" cy="15" r="2" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <circle cx="17" cy="15" r="2" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <line x1="10" y1="6" x2="4" y2="13" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
      <line x1="10" y1="6" x2="10" y2="13" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
      <line x1="10" y1="6" x2="16" y2="13" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesSocialSellingIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* LinkedIn-style share/connect icon */}
      <circle cx="4" cy="10" r="2.5" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <circle cx="16" cy="4" r="2.5" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <circle cx="16" cy="16" r="2.5" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <line x1="6.2" y1="8.8" x2="13.8" y2="5.2" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
      <line x1="6.2" y1="11.2" x2="13.8" y2="14.8" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesCRMAdoptionIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Database with checkmark — CRM adoption */}
      <ellipse cx="10" cy="5" rx="7" ry="2.5" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <path d="M3 5 v5 c0 1.4 3.1 2.5 7 2.5 s7-1.1 7-2.5 V5" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <path d="M3 10 v4 c0 1.4 3.1 2.5 7 2.5 s7-1.1 7-2.5 v-4" fill="none" stroke="currentColor" strokeWidth="1.4"/>
      <polyline points="7,11 9,13 13,9" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconSalesDealDeskIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Scales/balance — deal desk pricing judgment */}
      <line x1="10" y1="3" x2="10" y2="17" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
      <line x1="4" y1="6" x2="16" y2="6" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
      <path d="M4 6 L2 11 A3 3 0 0 0 6 11 Z" fill="none" stroke="currentColor" strokeWidth="1.2"/>
      <path d="M16 6 L14 11 A3 3 0 0 0 18 11 Z" fill="none" stroke="currentColor" strokeWidth="1.2"/>
      <line x1="7" y1="17" x2="13" y2="17" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesBuyerMeetingQualityIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Calendar with checkmark — meeting quality */}
      <rect x="2" y="4" width="16" height="13" rx="2" strokeLinecap="round"/>
      <line x1="2" y1="8" x2="18" y2="8" strokeLinecap="round"/>
      <line x1="6" y1="2" x2="6" y2="6" strokeLinecap="round"/>
      <line x1="14" y1="2" x2="14" y2="6" strokeLinecap="round"/>
      <path d="M7 13 L9 15 L13 11" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconSalesDecisionCriteriaAlignmentIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Checklist with target — criteria alignment */}
      <rect x="3" y="2" width="14" height="16" rx="1.5" strokeLinecap="round"/>
      <path d="M7 7 L9 9 L13 6" strokeLinecap="round" strokeLinejoin="round"/>
      <line x1="7" y1="11" x2="13" y2="11" strokeLinecap="round"/>
      <line x1="7" y1="14" x2="11" y2="14" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesPricingConfidenceIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Coin with confidence arrow — pricing psychology */}
      <circle cx="10" cy="10" r="7" strokeLinecap="round"/>
      <path d="M10 6 C8.5 6 7.5 6.9 7.5 8 C7.5 9.1 8.5 9.5 10 10 C11.5 10.5 12.5 11 12.5 12.1 C12.5 13.2 11.5 14 10 14" strokeLinecap="round"/>
      <line x1="10" y1="5" x2="10" y2="6" strokeLinecap="round"/>
      <line x1="10" y1="14" x2="10" y2="15" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesBuyerEngagementVelocityIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Lightning bolt with pulse — engagement velocity */}
      <path d="M11 2 L6 11 L10 11 L9 18 L14 9 L10 9 Z" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconSalesNegotiationLeverageIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Balance scales — negotiation leverage */}
      <line x1="10" y1="3" x2="10" y2="17" strokeLinecap="round"/>
      <line x1="3" y1="6" x2="17" y2="6" strokeLinecap="round"/>
      <path d="M3 6 L1 10 L5 10 Z" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M17 6 L15 10 L19 10 Z" strokeLinecap="round" strokeLinejoin="round"/>
      <line x1="7" y1="17" x2="13" y2="17" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesPipelineHealthDegradationIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Stacked pipeline stages, narrowing downward — degrading pipeline */}
      <rect x="2" y="3" width="16" height="3" rx="1" />
      <rect x="4" y="8" width="12" height="3" rx="1" />
      <rect x="6" y="13" width="8" height="3" rx="1" />
      <path d="M10 16 L10 19 M8 17.5 L10 19 L12 17.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function IconSalesObjectionHandlingEffectivenessIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Shield with check/cross — objection defense */}
      <path d="M10 2 L17 5 L17 11 C17 14.5 13.5 17.5 10 19 C6.5 17.5 3 14.5 3 11 L3 5 Z" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M7 10 L9.5 12.5 L13 8" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconSalesDiscoveryQualityIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Magnifying glass with question mark — discovery quality */}
      <circle cx="8" cy="8" r="5"/>
      <line x1="12" y1="12" x2="17" y2="17" strokeLinecap="round"/>
      <path d="M6.5 7 C6.5 5.5 8 5 9 6 C9.5 6.8 9 7.5 8 8 L8 9" strokeLinecap="round" strokeLinejoin="round"/>
      <circle cx="8" cy="10.5" r="0.5" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconSalesCustomerSuccessHandoffQualityIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Two-way arrows with handshake — CS handoff quality */}
      <path d="M3 8 L8 5 L8 7 L12 7 L12 5 L17 8 L12 11 L12 9 L8 9 L8 11 Z" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M6 13 C6 13 8 15 10 15 C12 15 14 13 14 13" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesNegotiationDisciplineIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Handshake with dollar sign — negotiation discipline */}
      <path d="M2 11 L6 8 L9 10 L11 10 L14 8 L18 11" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M6 8 L6 6" strokeLinecap="round"/>
      <path d="M14 8 L14 6" strokeLinecap="round"/>
      <path d="M9 10 L9 15 M11 10 L11 15" strokeLinecap="round"/>
      <path d="M7.5 15 L12.5 15" strokeLinecap="round"/>
      <text x="10" y="5.5" textAnchor="middle" fontSize="4.5" fill="currentColor" stroke="none" fontWeight="bold">$</text>
    </svg>
  );
}

function IconSalesTerritoryWhitespaceIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Map with target pin + whitespace dots — territory coverage */}
      <rect x="2" y="3" width="16" height="13" rx="1.5" strokeLinejoin="round"/>
      <circle cx="10" cy="9" r="2.5" fill="none"/>
      <path d="M10 11.5 L10 14" strokeLinecap="round"/>
      <circle cx="4.5" cy="5.5" r="0.8" fill="currentColor" stroke="none"/>
      <circle cx="15.5" cy="5.5" r="0.8" fill="currentColor" stroke="none"/>
      <circle cx="4.5" cy="13.5" r="0.8" fill="currentColor" stroke="none"/>
      <circle cx="15.5" cy="13.5" r="0.8" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconSalesProofOfValueIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Diamond gem with ROI arrow — value proof */}
      <path d="M10 2 L14 7 L10 18 L6 7 Z" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M6 7 L14 7" strokeLinecap="round"/>
      <path d="M4 7 L6 7 L10 2 L14 7 L16 7" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M14 4 L17 2 L17 5" strokeLinecap="round" strokeLinejoin="round"/>
      <line x1="14" y1="4" x2="17" y2="2" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesBuyerEngagementIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Signal waves from person — buyer signal reception */}
      <circle cx="10" cy="7" r="2" fill="currentColor" stroke="none"/>
      <path d="M7 16 C7 12.5 13 12.5 13 16" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M4 9.5 C4 5.5 16 5.5 16 9.5" strokeLinecap="round"/>
      <path d="M6 3 C6 1 14 1 14 3" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesMultiThreadingIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Network nodes — multi-threading stakeholder map */}
      <circle cx="10" cy="4" r="1.5" fill="currentColor" stroke="none"/>
      <circle cx="3" cy="12" r="1.5" fill="currentColor" stroke="none"/>
      <circle cx="17" cy="12" r="1.5" fill="currentColor" stroke="none"/>
      <circle cx="7" cy="17" r="1.5" fill="currentColor" stroke="none"/>
      <circle cx="13" cy="17" r="1.5" fill="currentColor" stroke="none"/>
      <line x1="10" y1="5.5" x2="3" y2="10.5" strokeLinecap="round"/>
      <line x1="10" y1="5.5" x2="17" y2="10.5" strokeLinecap="round"/>
      <line x1="3" y1="13.5" x2="7" y2="15.5" strokeLinecap="round"/>
      <line x1="17" y1="13.5" x2="13" y2="15.5" strokeLinecap="round"/>
      <line x1="3" y1="12" x2="17" y2="12" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesPipelineGenerationVelocityIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Rocket with pipeline funnel — generation velocity */}
      <path d="M10 2 C10 2 13 5 13 9 L10 17 L7 9 C7 5 10 2 10 2Z" strokeLinecap="round" strokeLinejoin="round"/>
      <circle cx="10" cy="8" r="1.5" fill="currentColor" stroke="none"/>
      <path d="M3 11 L7 13" strokeLinecap="round"/>
      <path d="M17 11 L13 13" strokeLinecap="round"/>
      <path d="M5 6 L3 5 L4 7" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M15 6 L17 5 L16 7" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconSalesChampionStabilityIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Crown with stability check — champion stability */}
      <path d="M2 14 L5 7 L10 11 L15 7 L18 14 Z" strokeLinecap="round" strokeLinejoin="round"/>
      <line x1="2" y1="14" x2="18" y2="14" strokeLinecap="round"/>
      <circle cx="5" cy="7" r="1.5" fill="currentColor" stroke="none"/>
      <circle cx="10" cy="11" r="1.5" fill="currentColor" stroke="none"/>
      <circle cx="15" cy="7" r="1.5" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconSalesWinRateDecayIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Declining trend line with alert — win rate decay */}
      <path d="M2 5 L7 8 L11 6 L15 12 L18 15" strokeLinecap="round" strokeLinejoin="round"/>
      <circle cx="18" cy="15" r="2" fill="currentColor" stroke="none"/>
      <path d="M16 3 L18 1 L20 3" strokeLinecap="round" strokeLinejoin="round"/>
      <line x1="18" y1="1" x2="18" y2="6" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesRepOnboardingRampIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Rocket launch — ramp acceleration */}
      <path d="M10 2 C10 2 14 5 14 10 L10 18 L6 10 C6 5 10 2 10 2Z" strokeLinecap="round" strokeLinejoin="round"/>
      <circle cx="10" cy="9" r="1.5" fill="currentColor" stroke="none"/>
      <path d="M6 13 L4 15 L6 15 L6 17" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M14 13 L16 15 L14 15 L14 17" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconSalesQuotaAttainmentPatternIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Target with trend line — quota attainment pattern */}
      <circle cx="10" cy="10" r="8" strokeLinecap="round"/>
      <circle cx="10" cy="10" r="4" strokeLinecap="round"/>
      <circle cx="10" cy="10" r="1" fill="currentColor" stroke="none"/>
      <path d="M4 15 L8 11 L11 13 L16 7" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconSalesObjectionIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Shield with X — objection defense */}
      <path d="M10 2 L17 5 L17 11 C17 14.5 13.5 17.5 10 18.5 C6.5 17.5 3 14.5 3 11 L3 5 Z" strokeLinecap="round" strokeLinejoin="round"/>
      <line x1="7.5" y1="9" x2="12.5" y2="13" strokeLinecap="round"/>
      <line x1="12.5" y1="9" x2="7.5" y2="13" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesNegotiationIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Handshake — negotiation */}
      <path d="M2 11 L6 8 L9 10 L13 7 L18 9" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M6 8 L6 15" strokeLinecap="round"/>
      <path d="M13 7 L13 14" strokeLinecap="round"/>
      <line x1="3" y1="15" x2="17" y2="15" strokeLinecap="round"/>
      <circle cx="6" cy="6" r="2"/>
      <circle cx="13" cy="5" r="2"/>
    </svg>
  );
}

function IconSalesReferenceIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Quote/testimonial bubbles — customer evidence */}
      <rect x="2" y="3" width="11" height="8" rx="2" strokeLinecap="round"/>
      <path d="M5 14 L2 17 L7 14" strokeLinecap="round" strokeLinejoin="round"/>
      <line x1="5" y1="6" x2="10" y2="6" strokeLinecap="round"/>
      <line x1="5" y1="8.5" x2="9" y2="8.5" strokeLinecap="round"/>
      <circle cx="15" cy="14" r="3" strokeLinecap="round"/>
      <path d="M14 13.5 L14.8 14.5 L16.5 13" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconSalesPOCIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Microscope/lab flask — POC scientific evaluation */}
      <ellipse cx="10" cy="14" rx="5" ry="3" strokeLinecap="round"/>
      <path d="M7 14 L6 7 M13 14 L14 7" strokeLinecap="round"/>
      <line x1="6" y1="7" x2="14" y2="7" strokeLinecap="round"/>
      <circle cx="10" cy="4" r="2" strokeLinecap="round"/>
      <line x1="10" y1="6" x2="10" y2="7" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesTimeAllocationIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Clock face with segmented arc — time allocation */}
      <circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" strokeWidth="1.4" opacity="0.5"/>
      <path d="M10 10 L10 3" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round"/>
      <path d="M10 10 L15 12" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" opacity="0.7"/>
      <circle cx="10" cy="10" r="1.5" fill="currentColor"/>
      <path d="M10 2 A8 8 0 0 1 16.9 6" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" fill="none" opacity="0.8"/>
    </svg>
  );
}

function IconSalesConversationIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Speech bubble with sound-wave bars inside — conversation quality */}
      <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v8a1 1 0 01-1 1H7l-4 3V4z" strokeLinejoin="round" opacity="0.7"/>
      <path d="M7 8.5h1.5" strokeLinecap="round" strokeWidth="1.8"/>
      <path d="M10 6.5v4" strokeLinecap="round" strokeWidth="1.8"/>
      <path d="M12.5 7.5v2" strokeLinecap="round" strokeWidth="1.8"/>
    </svg>
  );
}

function IconSalesRepRampIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Staircase steps going up — rep ramp progression */}
      <path d="M2 16 L2 12 L6 12 L6 8 L10 8 L10 5 L14 5 L14 3 L18 3" strokeLinecap="round" strokeLinejoin="round" opacity="0.8"/>
      <circle cx="14" cy="3" r="1.5" fill="currentColor" stroke="none" opacity="0.9"/>
      <path d="M2 18 L18 18" strokeLinecap="round" opacity="0.3"/>
    </svg>
  );
}

function IconSalesObjectionHandlingIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Shield with X-then-check — objection turned to win */}
      <path d="M10 2 L17 5 L17 10 C17 14 10 18 10 18 C10 18 3 14 3 10 L3 5 Z" strokeLinejoin="round" opacity="0.6"/>
      <path d="M7 10 L9 12 L13 8" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"/>
    </svg>
  );
}

function IconSalesPricingDisciplineIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Price tag with checkmark/lock — pricing discipline */}
      <path d="M3 10 L10 3 L17 10 L10 17 Z" strokeLinejoin="round" opacity="0.6"/>
      <path d="M7 10 L9 12 L13 8" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"/>
      <circle cx="10" cy="10" r="1" fill="currentColor" stroke="none" opacity="0.0"/>
    </svg>
  );
}

function IconSalesCRMDataHygieneIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Database cylinder with scan line — CRM hygiene */}
      <ellipse cx="10" cy="5" rx="7" ry="2.2" opacity="0.7"/>
      <path d="M3 5 L3 15 C3 16.2 6.1 17.2 10 17.2 C13.9 17.2 17 16.2 17 15 L17 5" opacity="0.6"/>
      <ellipse cx="10" cy="15" rx="7" ry="2.2" opacity="0.4"/>
      <path d="M6 10 L14 10" strokeLinecap="round" strokeWidth="1.8" opacity="0.9"/>
      <path d="M8 12.5 L12 12.5" strokeLinecap="round" opacity="0.6"/>
    </svg>
  );
}

function IconSalesTerritoryConverageIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Map with pin and boundary outline — territory */}
      <path d="M10 2 C5 2 2 5.5 2 9 C2 13 10 18 10 18 C10 18 18 13 18 9 C18 5.5 15 2 10 2 Z" opacity="0.4"/>
      <circle cx="10" cy="9" r="2.5" fill="currentColor" opacity="0.8"/>
      <path d="M2 8 L8 10 L12 6 L18 8" strokeLinecap="round" opacity="0.5"/>
    </svg>
  );
}

function IconSalesCompetitiveIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Two crossed swords — competitive battle */}
      <path d="M3 3 L17 17" strokeLinecap="round" strokeWidth="1.8"/>
      <path d="M17 3 L3 17" strokeLinecap="round" strokeWidth="1.8"/>
      <circle cx="10" cy="10" r="2.5" fill="currentColor" stroke="none" opacity="0.5"/>
      <path d="M3 3 L5 5" strokeLinecap="round" strokeWidth="2.5" opacity="0.8"/>
      <path d="M15 3 L17 5" strokeLinecap="round" strokeWidth="2.5" opacity="0.8" transform="rotate(90 16 4)"/>
    </svg>
  );
}

function IconSalesCustomerLifecycleIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Circular lifecycle loop with arrow — customer journey */}
      <circle cx="10" cy="10" r="7" opacity="0.4"/>
      <path d="M10 3 A7 7 0 1 1 3.5 14.5" strokeLinecap="round"/>
      <path d="M3.5 14.5 L2 12 L5.5 12.5 Z" fill="currentColor" stroke="none" opacity="0.8"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" opacity="0.7"/>
    </svg>
  );
}

function IconSalesAccountPenetrationIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Concentric circles radiating out from center — territory penetration */}
      <circle cx="10" cy="10" r="2" fill="currentColor" />
      <circle cx="10" cy="10" r="5" fill="none" stroke="currentColor" strokeWidth="1.3" opacity="0.7" />
      <circle cx="10" cy="10" r="8.5" fill="none" stroke="currentColor" strokeWidth="1.1" opacity="0.4" />
      <circle cx="10" cy="4" r="1.2" fill="currentColor" opacity="0.8" />
      <circle cx="16" cy="10" r="1.2" fill="currentColor" opacity="0.6" />
      <circle cx="4" cy="10" r="1.2" fill="currentColor" opacity="0.4" />
    </svg>
  );
}

function IconSalesDealVelocityIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Arrow accelerating right — deal velocity */}
      <path d="M2 10h11M10 6l5 4-5 4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <circle cx="4" cy="10" r="1.2" fill="currentColor" opacity="0.5" />
      <circle cx="7" cy="10" r="1.2" fill="currentColor" opacity="0.65" />
      <circle cx="10" cy="10" r="1.2" fill="currentColor" opacity="0.8" />
    </svg>
  );
}

function IconPipelineGenerationEfficiencyEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Funnel with activity arrows entering top */}
      <path d="M3 3h14l-5 6v6l-4-2V9L3 3z" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
      <line x1="6" y1="1" x2="6" y2="3" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
      <line x1="10" y1="1" x2="10" y2="3" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
      <line x1="14" y1="1" x2="14" y2="3" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
      <circle cx="10" cy="15" r="1.5" fill="currentColor" opacity="0.7" />
    </svg>
  );
}

function IconSalesObjectionPatternIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      {/* Speech bubble with X marks representing objections */}
      <path d="M3 4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H8l-3 3v-3H4a1 1 0 0 1-1-1V4z"
        fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
      <line x1="6" y1="7" x2="8" y2="9" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
      <line x1="8" y1="7" x2="6" y2="9" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
      <line x1="11" y1="7" x2="13" y2="9" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
      <line x1="13" y1="7" x2="11" y2="9" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
    </svg>
  );
}

function IconSalesIncentiveCompensationRiskEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2l2.5 5 5.5.8-4 3.9.9 5.5L10 14.8l-4.9 2.4.9-5.5L2 7.8l5.5-.8L10 2z"
        fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinejoin="round" opacity="0.4" />
      <path d="M10 4l1.8 3.6 4 .6-2.9 2.8.7 4L10 13l-3.6 1.9.7-4L4.2 8.2l4-.6L10 4z"
        fill="#fbbf24" opacity="0.7" />
      <path d="M7 11l1.5 1.5L13 8" stroke="white" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.9" />
    </svg>
  );
}

function IconSalesCycleVelocityDegradationEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 16l3-5 3 2 3-4 3 3 2-2" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.4" />
      <path d="M2 18l3-6 3 3 3-5 3 4" stroke="#fb923c" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.9" />
      <path d="M14 6v4h4" stroke="#f87171" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.9" />
      <circle cx="14" cy="6" r="3.5" fill="none" stroke="#f87171" strokeWidth="1.3" opacity="0.7" />
    </svg>
  );
}

function IconCustomerExpansionRevenueLeakDetector({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2a8 8 0 1 1 0 16A8 8 0 0 1 10 2z" fill="none" stroke="currentColor" strokeWidth="1.3" opacity="0.3" />
      <path d="M10 2a8 8 0 0 1 0 16" fill="none" stroke="#fb923c" strokeWidth="1.5" strokeLinecap="round" opacity="0.8" />
      <path d="M10 6v5l3 3" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.7" />
      <circle cx="10" cy="10" r="1.5" fill="currentColor" opacity="0.8" />
      <path d="M7 3.5l-2 3h4l-2-3z" fill="#f87171" opacity="0.85" />
    </svg>
  );
}

function IconSalesForecastSandbaggingDetectionEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 16l3-6 3 3 3-5 3 3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.4" />
      <path d="M3 14l3-4 3 2 3-3.5 3 2" stroke="#fbbf24" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.9" />
      <circle cx="16" cy="10.5" r="2" fill="#fbbf24" opacity="0.9" />
      <path d="M15 10.5h2M16 9.5v2" stroke="white" strokeWidth="0.9" strokeLinecap="round" />
      <path d="M3 17h14" stroke="currentColor" strokeWidth="1" strokeLinecap="round" opacity="0.3" />
    </svg>
  );
}

function IconSalesRepBurnoutAttritionRiskEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="7" r="4" fill="none" stroke="currentColor" strokeWidth="1.4" opacity="0.7" />
      <path d="M4 17c0-3.3 2.7-6 6-6s6 2.7 6 6" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" opacity="0.5" />
      <path d="M10 10v4" stroke="#f87171" strokeWidth="1.3" strokeLinecap="round" opacity="0.9" />
      <path d="M8 14l2 2 2-2" stroke="#f87171" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.9" />
      <circle cx="16" cy="4" r="2.5" fill="#fbbf24" opacity="0.85" />
      <path d="M16 3v1.5M16 5.2v.3" stroke="white" strokeWidth="0.9" strokeLinecap="round" />
    </svg>
  );
}

function IconSalesCompetitiveWinRateErosionEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 15l4-5 3 2 4-6 3 3" stroke="#f87171" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.9" />
      <circle cx="3" cy="15" r="1.2" fill="#f87171" opacity="0.9" />
      <circle cx="17" cy="9" r="1.2" fill="#f87171" opacity="0.9" />
      <path d="M3 9l4-3 3 2 4-4 3 1" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.4" />
      <path d="M14 5h3v3" stroke="#fbbf24" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.8" />
    </svg>
  );
}

function IconSalesPipelineConcentrationRiskEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="2" y="13" width="3" height="5" rx="0.5" opacity="0.5" />
      <rect x="6.5" y="9" width="3" height="9" rx="0.5" opacity="0.5" />
      <rect x="11" y="4" width="3" height="14" rx="0.5" opacity="0.9" fill="#f87171" />
      <rect x="15.5" y="7" width="3" height="11" rx="0.5" opacity="0.5" />
      <circle cx="12.5" cy="4" r="2.5" fill="#fbbf24" opacity="0.9" />
      <path d="M11.5 4h2M12.5 3v2" stroke="white" strokeWidth="1" strokeLinecap="round" fill="none" />
    </svg>
  );
}

function IconCustomerLTVErosionDetector({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2C6.13 2 3 5.13 3 9s3.13 7 7 7 7-3.13 7-7-3.13-7-7-7z" opacity="0.2" />
      <path d="M10 2C6.13 2 3 5.13 3 9s3.13 7 7 7 7-3.13 7-7-3.13-7-7-7z" fill="none" stroke="currentColor" strokeWidth="1.3" opacity="0.6" />
      <path d="M6 9l2.5 2.5L14 6" stroke="#34d399" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.0" />
      <path d="M7 9l1.5 2 3.5-5" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity="0.8" />
      <path d="M9 14v3M11 14v3" stroke="#f87171" strokeWidth="1.3" strokeLinecap="round" fill="none" opacity="0.7" />
      <path d="M7.5 17h5" stroke="#f87171" strokeWidth="1.3" strokeLinecap="round" fill="none" opacity="0.7" />
      <path d="M14 4l2-2M16 6l-2-2" stroke="#fbbf24" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.8" />
    </svg>
  );
}

function IconSalesRepBurnoutDisengagementEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2a6 6 0 016 6c0 2.5-1.5 4.7-3.7 5.7L12 17H8l-.3-3.3C5.5 12.7 4 10.5 4 8a6 6 0 016-6z" opacity="0.35" />
      <path d="M8 17h4v1.5a.5.5 0 01-.5.5h-3a.5.5 0 01-.5-.5V17z" opacity="0.6" />
      <path d="M10 5v4l2.5 1.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" fill="none" opacity="0.9" />
      <circle cx="15" cy="5" r="2.5" fill="#f87171" opacity="0.9" />
      <path d="M14.25 5h1.5M15 4.25v1.5" stroke="white" strokeWidth="1.2" strokeLinecap="round" fill="none" />
    </svg>
  );
}

function IconSalesDiscountAbuseDetector({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M17.707 9.293a1 1 0 010 1.414l-7 7a1 1 0 01-1.414 0l-7-7A.997.997 0 012 10V5a3 3 0 013-3h5c.256 0 .512.098.707.293l7 7zM5 6a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" opacity="0.4" />
      <path d="M8 6l-2 8" stroke="#f87171" strokeWidth="1.4" strokeLinecap="round" fill="none" opacity="0.8" />
      <circle cx="6.5" cy="6.5" r="1.5" fill="#f87171" opacity="0.8" />
      <circle cx="9.5" cy="13.5" r="1.5" fill="#f87171" opacity="0.8" />
    </svg>
  );
}

function IconSalesActivityFabricationDetector({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 5a1 1 0 011-1h5a1 1 0 010 2H3a1 1 0 01-1-1zm0 5a1 1 0 011-1h5a1 1 0 010 2H3a1 1 0 01-1-1zm0 5a1 1 0 011-1h5a1 1 0 010 2H3a1 1 0 01-1-1z" opacity="0.5" />
      <path d="M10 6h7M10 11h5M10 16h3" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.35" />
      <circle cx="16" cy="4" r="3" fill="currentColor" opacity="0.15" />
      <path d="M14.5 4l1 1 1.5-1.5" stroke="#f87171" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <circle cx="16" cy="4" r="3" stroke="#f87171" strokeWidth="0.9" fill="none" opacity="0.7" />
    </svg>
  );
}

function IconSalesDataAccessAnomalyEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3 5a2 2 0 012-2h10a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2V5zm2 0v8h10V5H5z" clipRule="evenodd" opacity="0.5" />
      <path d="M7 8h6M7 11h4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" fill="none" opacity="0.6" />
      <circle cx="15" cy="15" r="3.5" fill="currentColor" opacity="0.15" />
      <path d="M13.5 15l1 1 2-2" stroke="#f87171" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <circle cx="15" cy="15" r="3.5" stroke="#f87171" strokeWidth="1" fill="none" opacity="0.8" />
    </svg>
  );
}

function IconRepIncentiveMisalignmentEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="2" y="10" width="3" height="8" rx="1" fill="currentColor" opacity={0.5} />
      <rect x="7" y="6" width="3" height="12" rx="1" fill="currentColor" opacity={0.7} />
      <rect x="12" y="2" width="3" height="16" rx="1" fill="currentColor" opacity={0.9} />
      <path d="M16 8l2-2M16 6l2 2" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.8" />
      <path d="M3.5 10L8.5 6L13.5 2" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeDasharray="2 2" fill="none" opacity="0.5" />
    </svg>
  );
}

function IconSalesBurnoutRiskEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="6" r="3" fill="currentColor" opacity={0.6} />
      <path d="M4 18c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="currentColor" strokeWidth="1.3" fill="none" strokeLinecap="round" opacity="0.5" />
      <path d="M10 10v4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.8" />
      <circle cx="10" cy="15" r="1" fill="currentColor" opacity={0.9} />
      <path d="M14 3l1.5-1.5M6 3L4.5 1.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.5" />
      <path d="M16 7l1.5.5M4 7L2.5 7.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.4" />
    </svg>
  );
}

function IconSalesValuePropositionDeteriorationIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Value prop: dollar sign with downward trend — deteriorating value */}
      <path d="M10 3 C8 3 7 4 7 5.5 C7 7 8.5 7.5 10 8 C11.5 8.5 13 9 13 10.5 C13 12 12 13 10 13" strokeLinecap="round"/>
      <line x1="10" y1="2" x2="10" y2="3" strokeLinecap="round"/>
      <line x1="10" y1="13" x2="10" y2="14" strokeLinecap="round"/>
      <path d="M3 16 L7 13 L10 15 L14 10 L17 12" strokeLinecap="round" strokeLinejoin="round" opacity="0.5"/>
      <circle cx="17" cy="12" r="1.5" fill="currentColor" stroke="none" opacity="0.8"/>
    </svg>
  );
}

function IconSalesTerritoryImbalanceCoverageGapEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Territory map: grid with unequal cells — imbalance */}
      <rect x="2" y="3" width="7" height="7" rx="0.8"/>
      <rect x="11" y="3" width="7" height="4" rx="0.8" opacity="0.5"/>
      <rect x="11" y="9" width="7" height="8" rx="0.8" opacity="0.5"/>
      <rect x="2" y="12" width="7" height="5" rx="0.8"/>
      <path d="M9 6.5 L11 6.5 M9 14.5 L11 11" strokeDasharray="1.5 1" opacity="0.6" strokeLinecap="round"/>
    </svg>
  );
}

function IconSalesCustomerHealthScoreDeteriorationEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Customer health: heartbeat / ECG pulse declining */}
      <path d="M2 10 L5 10 L6.5 6 L8 14 L9.5 10 L11 10 L12.5 8 L14 12 L15.5 10 L18 10" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.6"/>
      <path d="M2 15 L18 15" strokeDasharray="2 2" opacity="0.4"/>
    </svg>
  );
}

function IconSalesOnboardingRampIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Onboarding ramp: staircase steps with upward arrow */}
      <path d="M3 16 L3 13 L7 13 L7 10 L11 10 L11 7 L15 7 L15 4" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.6"/>
      <path d="M13 4 L15 4 L15 6" strokeLinecap="round" strokeLinejoin="round"/>
      <circle cx="5" cy="14.5" r="1.5" fill="currentColor" stroke="none" opacity="0.7"/>
    </svg>
  );
}

function IconSalesCompetitiveIntelligenceBattleCardEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Battle card: crossed swords with shield */}
      <path d="M4 4 L16 16 M16 4 L4 16" strokeLinecap="round" strokeWidth="1.6"/>
      <path d="M10 2 L12 5 L10 8 L8 5 Z" strokeLinejoin="round"/>
      <circle cx="10" cy="13" r="3" strokeWidth="1.3"/>
      <path d="M8.5 13 L9.5 14 L12 11.5" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconSalesMeetingQualityConversionIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Calendar with checkmark and upward arrow — meeting quality & conversion */}
      <rect x="3" y="4" width="14" height="12" rx="1.5"/>
      <path d="M3 7.5 L17 7.5"/>
      <path d="M7 3 L7 5.5 M13 3 L13 5.5" strokeLinecap="round"/>
      <path d="M7 11.5 L9 13.5 L13 10" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.6"/>
    </svg>
  );
}

function IconSalesDiscountLeakageMarginErosionIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Discount leak: money draining downward with percentage tag */}
      <circle cx="10" cy="5" r="3"/>
      <path d="M10 8 L10 14" strokeLinecap="round" strokeWidth="1.8"/>
      <path d="M7 12 L10 15 L13 12" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M5 16 L5 18 M8 17 L8 18 M11 16.5 L11 18 M14 16 L14 18" strokeLinecap="round" opacity="0.5"/>
      <text x="10" y="5.5" textAnchor="middle" fontSize="3.5" fill="currentColor" stroke="none" fontWeight="bold">%</text>
    </svg>
  );
}

function IconSalesBuyerPersonaMismatchIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Persona mismatch: two people, one with X — wrong person */}
      <circle cx="7" cy="6" r="2.5"/>
      <path d="M2 17 C2 13 12 13 12 17" strokeLinecap="round"/>
      <circle cx="15" cy="6" r="2.5" opacity="0.4"/>
      <line x1="12.5" y1="3.5" x2="17.5" y2="8.5" strokeLinecap="round" stroke="#ef4444" strokeWidth="1.8"/>
      <line x1="17.5" y1="3.5" x2="12.5" y2="8.5" strokeLinecap="round" stroke="#ef4444" strokeWidth="1.8"/>
    </svg>
  );
}

function IconSalesDealVelocityCollapseIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Velocity collapse: speedometer needle dropping */}
      <circle cx="10" cy="11" r="7" strokeWidth="1.4"/>
      <path d="M4 11 A6 6 0 0 1 16 11" strokeWidth="1.4" strokeLinecap="round"/>
      <line x1="10" y1="11" x2="6" y2="7" strokeWidth="2" strokeLinecap="round" stroke="currentColor"/>
      <circle cx="10" cy="11" r="1" fill="currentColor" stroke="none"/>
      <path d="M7 15 L10 17 L13 15" strokeLinecap="round" strokeLinejoin="round" opacity="0.5"/>
    </svg>
  );
}

function IconSalesRepBurnoutAttritionRiskIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Burnout: flame with person silhouette — rep at risk */}
      <path d="M10 17 C6 17 4 14 4 11 C4 8 6 6 8 5 C7 7 8 8 9 8 C9 5 11 3 13 2 C13 5 11 7 12 9 C13 7 14 6 15 7 C16 9 16 11 14 13 C13 15 12 17 10 17Z" strokeLinecap="round" strokeLinejoin="round"/>
      <circle cx="10" cy="12" r="1.5" fill="currentColor" stroke="none" opacity="0.6"/>
    </svg>
  );
}

function IconSalesQuotaSandbagOvercommitIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Quota bar: sandbagging low then surging — gaming detection */}
      <rect x="2" y="12" width="3" height="5" rx="0.5" fill="currentColor" stroke="none" opacity="0.4"/>
      <rect x="6" y="10" width="3" height="7" rx="0.5" fill="currentColor" stroke="none" opacity="0.5"/>
      <rect x="10" y="8" width="3" height="9" rx="0.5" fill="currentColor" stroke="none" opacity="0.6"/>
      <rect x="14" y="3" width="3" height="14" rx="0.5" fill="currentColor" stroke="none" opacity="0.9"/>
      <path d="M3 9 L9 8 L13 6 L17 2" strokeLinecap="round" strokeLinejoin="round" stroke="#eab308" strokeWidth="1.6"/>
      <circle cx="17" cy="2" r="1.2" fill="#eab308" stroke="none"/>
    </svg>
  );
}

function IconSalesChampionDepartureRelationshipContinuityEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Champion departure: person with exit arrow and broken link */}
      <circle cx="8" cy="6" r="3"/>
      <path d="M2 17 C2 13 14 13 14 17" strokeLinecap="round"/>
      <path d="M15 8 L18 8 M16.5 6 L18 8 L16.5 10" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.6" stroke="#ef4444"/>
      <path d="M10 11.5 L12 11.5" strokeLinecap="round" strokeWidth="1" strokeDasharray="1.5 1" opacity="0.5"/>
    </svg>
  );
}

function IconSalesProposalQualityWinRateIntelligenceEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Proposal quality: document with checkmark and ascending win bars */}
      <rect x="4" y="2" width="10" height="13" rx="1.2"/>
      <path d="M7 6 L13 6 M7 8.5 L11 8.5 M7 11 L10 11" strokeLinecap="round" strokeWidth="1.2"/>
      <path d="M6 13.5 L8 15.5 L14 10" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" stroke="#10b981"/>
    </svg>
  );
}

function IconSalesPriceSensitivityNegotiationLeverageEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Negotiation leverage: handshake with dollar split and tension arrows */}
      <path d="M4 10 L8 10 L10 7 L12 13 L14 10 L16 10" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.6"/>
      <path d="M2 14 L5 11 M18 14 L15 11" strokeLinecap="round" strokeWidth="1.2" opacity="0.5"/>
      <circle cx="10" cy="4" r="2.5" strokeWidth="1.3"/>
      <path d="M9 4 L9 3 M11 4 L11 5" strokeLinecap="round" strokeWidth="1.2"/>
      <path d="M8.5 3.2 L11.5 3.2 M8.5 4.8 L11.5 4.8" strokeLinecap="round" strokeWidth="0.9" opacity="0.7"/>
    </svg>
  );
}

function IconSalesDiscountApprovalAbuseMarginErosionEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Margin erosion: tag with discount slash and declining margin bar */}
      <path d="M3 10 L10 3 L17 3 L17 10 L10 17 Z" strokeLinejoin="round"/>
      <circle cx="14" cy="6" r="1.2" fill="currentColor" stroke="none"/>
      <path d="M7 13 L13 7" strokeLinecap="round" strokeWidth="1.8" stroke="#ef4444"/>
      <path d="M3 17 L6 15 L9 16.5 L12 14 L17 15" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.2" opacity="0.6" stroke="#ef4444"/>
    </svg>
  );
}

function IconSalesMultithreadingDepthRelationshipBreadthEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Multithreading: network nodes with varying connection density */}
      <circle cx="10" cy="4" r="1.5" fill="currentColor" stroke="none"/>
      <circle cx="3"  cy="14" r="1.5" fill="currentColor" stroke="none"/>
      <circle cx="17" cy="14" r="1.5" fill="currentColor" stroke="none"/>
      <circle cx="10" cy="16" r="1.5" fill="currentColor" stroke="none"/>
      <path d="M10 5.5 L3 12.5 M10 5.5 L17 12.5 M10 5.5 L10 14.5" strokeLinecap="round" strokeWidth="1.2"/>
      <path d="M3 12.5 L10 14.5 M17 12.5 L10 14.5 M3 12.5 L17 12.5" strokeLinecap="round" strokeWidth="0.9" opacity="0.5"/>
      <circle cx="17" cy="14" r="1.5" fill="none" stroke="#ef4444" strokeWidth="1.8"/>
    </svg>
  );
}

function IconSalesBuyerIntentSignalDecayEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Intent decay: wifi signal bars declining with downward trend */}
      <path d="M3 15 C3 11 17 11 17 15" strokeLinecap="round" strokeWidth="1.2" opacity="0.3"/>
      <path d="M5 12 C5 9.5 15 9.5 15 12" strokeLinecap="round" strokeWidth="1.2" opacity="0.5"/>
      <path d="M7 9.5 C7 7.5 13 7.5 13 9.5" strokeLinecap="round" strokeWidth="1.4"/>
      <circle cx="10" cy="7" r="1.2" fill="currentColor" stroke="none"/>
      <path d="M6 18 L10 14 L13 16 L17 11" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" stroke="#ef4444"/>
    </svg>
  );
}

function IconSalesCompetitiveWinLossPatternEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* Competitive: two swords crossing with win/loss bars */}
      <path d="M4 4 L16 16 M4 4 L7 4 M4 4 L4 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.6"/>
      <path d="M16 16 L13 16 M16 16 L16 13" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.6" stroke="#ef4444"/>
      <path d="M16 4 L4 16 M16 4 L13 4 M16 4 L16 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.3" opacity="0.55"/>
      <circle cx="10" cy="10" r="1.5" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconSalesPipelineStageInflationCrmHygieneEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.4" aria-hidden="true">
      {/* CRM hygiene: pipeline stages with inflation warning and data gap */}
      <rect x="2" y="13" width="3" height="5" rx="0.6" fill="currentColor" stroke="none" opacity="0.5"/>
      <rect x="6.5" y="9" width="3" height="9" rx="0.6" fill="currentColor" stroke="none" opacity="0.6"/>
      <rect x="11" y="5" width="3" height="13" rx="0.6" fill="currentColor" stroke="none"/>
      <path d="M15.5 2 L17 4 L15.5 6" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" stroke="#ef4444"/>
      <path d="M15.5 4 L12.5 4" strokeLinecap="round" strokeWidth="1.3" stroke="#ef4444"/>
      <circle cx="3.5" cy="10" r="1.2" fill="#f59e0b" stroke="none"/>
    </svg>
  );
}

function IconFreedomOfAssembly({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="5" cy="8" r="2" />
      <circle cx="12" cy="6" r="2" />
      <circle cx="19" cy="8" r="2" />
      <path d="M2 20c0-3 2-5 3-5s2 1 3 1 2-1 3-1 2 1 3 1 2-1 3-1 3 2 3 5" />
      <path d="M12 9v4" />
      <path d="M10 11h4" />
      <path d="M9 14l-1.5 2" />
      <path d="M15 14l1.5 2" />
    </svg>
  );
}

function IconArbitraryDetention({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="7" y="11" width="10" height="10" rx="1" />
      <path d="M9 11V7a3 3 0 0 1 6 0v4" />
      <circle cx="12" cy="16" r="1" fill="currentColor" />
      <path d="M5 8l-2 2" />
      <path d="M3 10v3" />
      <path d="M19 8l2 2" />
      <path d="M21 10v3" />
    </svg>
  );
}


function IconChevronLeft({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M12.707 5.293a1 1 0 0 1 0 1.414L9.414 10l3.293 3.293a1 1 0 0 1-1.414 1.414l-4-4a1 1 0 0 1 0-1.414l4-4a1 1 0 0 1 1.414 0z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconChevronRight({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M7.293 14.707a1 1 0 0 1 0-1.414L10.586 10 7.293 6.707a1 1 0 0 1 1.414-1.414l4 4a1 1 0 0 1 0 1.414l-4 4a1 1 0 0 1-1.414 0z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconLogout({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M3 3a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h6a1 1 0 1 0 0-2H4V5h5a1 1 0 1 0 0-2H3zm10.293 4.293a1 1 0 0 1 1.414 0l3 3a1 1 0 0 1 0 1.414l-3 3a1 1 0 0 1-1.414-1.414L14.586 11H8a1 1 0 1 1 0-2h6.586l-1.293-1.293a1 1 0 0 1 0-1.414z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconPipelineHygiene({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="2" y="4" width="4" height="12" rx="1"/>
      <rect x="8" y="6" width="4" height="10" rx="1"/>
      <rect x="14" y="8" width="4" height="8" rx="1"/>
      <path d="M1 17h18" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
      <circle cx="16" cy="4" r="2.5" fill="#ef4444"/>
      <path d="M15 3.5l.8.8 1.4-1.4" stroke="white" strokeWidth="0.8" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
    </svg>
  );
}

function IconCompetitiveWins({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M6 3l1.5 2.5H3L6 3zM14 3l2.5 2.5h-5L14 3z"/>
      <path d="M5.5 5.5L10 14l4.5-8.5" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
      <circle cx="10" cy="10" r="2"/>
      <path d="M10 16v2M8 18h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    </svg>
  );
}

function IconIntentDecay({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 10q3-6 7-6t7 6-7 6-7-6z" fill="none" stroke="currentColor" strokeWidth="1.5"/>
      <circle cx="10" cy="10" r="2"/>
      <path d="M5 15l3-3M15 15l-3-3" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" fill="none"/>
      <path d="M8 17h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" fill="none"/>
    </svg>
  );
}

function IconMultithreading({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="10" r="2"/>
      <circle cx="3" cy="5" r="1.5"/>
      <circle cx="17" cy="5" r="1.5"/>
      <circle cx="3" cy="15" r="1.5"/>
      <circle cx="17" cy="15" r="1.5"/>
      <circle cx="10" cy="2" r="1.5"/>
      <path d="M8 10L4.5 5.5M12 10l3.5-4.5M8 10L4.5 14.5M12 10l3.5 4.5M10 8V3.5" stroke="currentColor" strokeWidth="1" fill="none" strokeLinecap="round"/>
    </svg>
  );
}

function IconMarginErosion({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M17.707 9.293l-7-7A1 1 0 0 0 10 2H4a2 2 0 0 0-2 2v6c0 .266.105.52.293.707l7 7a1 1 0 0 0 1.414 0l7-7a1 1 0 0 0 0-1.414zM6 7a1 1 0 1 1 0-2 1 1 0 0 1 0 2z" clipRule="evenodd"/>
      <path d="M8 12l1.5 1.5L13 10" stroke="white" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
    </svg>
  );
}

function IconRepBurnout({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="7" r="3"/>
      <path d="M5 17c0-2.76 2.24-5 5-5s5 2.24 5 5" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
      <path d="M10 12l-.5 2.5M10 12l.5 2.5" stroke="currentColor" strokeWidth="1" strokeLinecap="round" fill="none"/>
      <path d="M14 4c.5-.5 1-1.5.5-2.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" fill="none"/>
      <path d="M16 6c.8-.3 1.5-1 1.5-2" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" fill="none"/>
    </svg>
  );
}

function IconDataAnalytics({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="12" width="3" height="6" rx="1" fill="currentColor" fillOpacity="0.7"/>
      <rect x="7" y="8"  width="3" height="10" rx="1" fill="currentColor" fillOpacity="0.7"/>
      <rect x="12" y="4" width="3" height="14" rx="1" fill="currentColor" fillOpacity="0.7"/>
      <path d="M3.5 10L8.5 6l5 3 3-4" stroke="currentColor" strokeWidth="1.2"/>
    </svg>
  );
}
function IconOrderManagement({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="7" width="16" height="11" rx="2" fillOpacity="0.1" fill="currentColor"/>
      <path d="M6 7V5a4 4 0 018 0v2"/>
      <path d="M7 12l2 2 4-4"/>
    </svg>
  );
}
function IconCustomerService({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="8" fillOpacity="0.1" fill="currentColor"/>
      <path d="M7 8h6M7 11h4"/>
      <circle cx="10" cy="5" r="1.5" fill="currentColor"/>
    </svg>
  );
}
function IconITSystems({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="3" width="16" height="11" rx="2" fillOpacity="0.1" fill="currentColor"/>
      <path d="M7 17h6M10 14v3"/>
      <circle cx="6" cy="7" r="1" fill="currentColor"/>
      <circle cx="10" cy="7" r="1" fill="currentColor"/>
      <circle cx="14" cy="7" r="1" fill="currentColor"/>
    </svg>
  );
}
function IconSecurityShield({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l7 3v5c0 4-3 7-7 8C7 17 4 14 3 10V5l7-3z" fillOpacity="0.15" fill="currentColor"/>
      <path d="M7 10l2 2 4-4"/>
    </svg>
  );
}

function IconAccountChurn({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="5" width="16" height="11" rx="2" fill="currentColor" fillOpacity="0.12"/>
      <path d="M2 8h16"/>
      <path d="M7 12l2 2 4-4" stroke="currentColor" strokeWidth="1.5"/>
      <path d="M14 3l2 2-2 2" fill="none"/>
      <path d="M16 5H6" strokeDasharray="2 1"/>
    </svg>
  );
}

function IconEthicsCompliance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l6 2.5v4.5c0 3.5-2.5 6.5-6 7.5C4.5 15.5 2 12.5 2 9V4.5L10 2z" fill="currentColor" fillOpacity="0.12"/>
      <path d="M7 10l2 2 4-4"/>
    </svg>
  );
}

function IconInnovationScout({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7" fill="currentColor" fillOpacity="0.1"/>
      <path d="M10 6v4l2.5 2.5"/>
      <path d="M14 4l1-1M16 8h1M14 12l1 1"/>
    </svg>
  );
}

function IconPRCrisis({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 5a2 2 0 012-2h8a2 2 0 012 2v5a2 2 0 01-2 2H7l-3 3V12H4a2 2 0 01-2-2V5z" fill="currentColor" fillOpacity="0.12"/>
      <path d="M10 8v1M10 6v.5"/>
    </svg>
  );
}

function IconKnowledgeGap({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="8" r="4" fill="currentColor" fillOpacity="0.12"/>
      <path d="M10 5v3l2 1"/>
      <path d="M5 15h10M7 17h6"/>
    </svg>
  );
}

function IconCertification({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="8" r="5" fill="currentColor" fillOpacity="0.12"/>
      <path d="M7 8l2 2 4-3"/>
      <path d="M7 14l-1 4 4-2 4 2-1-4"/>
    </svg>
  );
}

function IconLearningPath({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 17V7l7-4 7 4v10" fill="currentColor" fillOpacity="0.08"/>
      <path d="M8 17v-5h4v5"/>
      <path d="M3 7l7 4 7-4"/>
    </svg>
  );
}

function IconDataProtection({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="8" width="14" height="9" rx="2" fill="currentColor" fillOpacity="0.12"/>
      <path d="M7 8V6a3 3 0 016 0v2"/>
      <circle cx="10" cy="13" r="1.5" fill="currentColor"/>
      <path d="M10 13v2"/>
    </svg>
  );
}

function IconResourceOptimization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="12" width="4" height="6" rx="1" fill="currentColor" fillOpacity="0.15"/>
      <rect x="8" y="8" width="4" height="10" rx="1" fill="currentColor" fillOpacity="0.15"/>
      <rect x="14" y="4" width="4" height="14" rx="1" fill="currentColor" fillOpacity="0.15"/>
      <path d="M4 12l4-4 4 2 4-6"/>
    </svg>
  );
}
function IconOrgHealth({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="6" r="3" fill="currentColor" fillOpacity="0.15"/>
      <path d="M4 17c0-3.3 2.7-6 6-6s6 2.7 6 6"/>
      <path d="M10 11v3"/>
      <path d="M8 14h4"/>
    </svg>
  );
}
function IconLegalWatch({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2L3 6v4c0 4 3 7 7 8 4-1 7-4 7-8V6z" fill="currentColor" fillOpacity="0.12"/>
      <path d="M7 10l2 2 4-4"/>
    </svg>
  );
}
function IconQualityAssurance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7" fill="currentColor" fillOpacity="0.10"/>
      <path d="M7 10l2 2 4-4"/>
      <path d="M10 3v2M10 15v2M3 10h2M15 10h2"/>
    </svg>
  );
}
function IconSwarmOrchestration({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="2" fill="currentColor" fillOpacity="0.2"/>
      <circle cx="4" cy="5" r="1.5" fill="currentColor" fillOpacity="0.15"/>
      <circle cx="16" cy="5" r="1.5" fill="currentColor" fillOpacity="0.15"/>
      <circle cx="4" cy="15" r="1.5" fill="currentColor" fillOpacity="0.15"/>
      <circle cx="16" cy="15" r="1.5" fill="currentColor" fillOpacity="0.15"/>
      <path d="M5.5 6l3 3M14.5 6l-3 3M5.5 14l3-3M14.5 14l-3-3"/>
    </svg>
  );
}
function IconContinuousImprovement({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 14c1-2 2-4 4-5s4 0 6-2 3-4 4-5" fill="none"/>
      <path d="M15 7l2-2-2-2"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" fillOpacity="0.15"/>
    </svg>
  );
}
function IconStrategicRisk({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l8 15H2z" fill="currentColor" fillOpacity="0.12"/>
      <path d="M10 8v4"/>
      <circle cx="10" cy="14" r="0.75" fill="currentColor"/>
    </svg>
  );
}

function IconForesight({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7" fill="currentColor" fillOpacity="0.08"/>
      <path d="M10 3v2M10 15v2M3 10h2M15 10h2"/>
      <path d="M6 6l1.5 1.5M12.5 12.5L14 14M14 6l-1.5 1.5M7.5 12.5L6 14"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" fillOpacity="0.3"/>
    </svg>
  );
}
function IconEmotionalIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 17s-7-4.5-7-9a5 5 0 0110 0" fill="none"/>
      <path d="M10 17s7-4.5 7-9a5 5 0 00-10 0"/>
      <path d="M7 9c.5-1.5 2-2 3-1.5"/>
    </svg>
  );
}
function IconLogistics({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="1" y="8" width="11" height="7" rx="1" fill="currentColor" fillOpacity="0.1"/>
      <path d="M12 11h3l3 3v2h-3"/>
      <circle cx="5" cy="16" r="1.5"/>
      <circle cx="15" cy="16" r="1.5"/>
      <path d="M1 11h11"/>
    </svg>
  );
}
function IconRegulatoryCompliance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l7 3v5c0 4-3 7-7 8-4-1-7-4-7-8V5z" fill="currentColor" fillOpacity="0.1"/>
      <path d="M10 2l7 3v5c0 4-3 7-7 8-4-1-7-4-7-8V5z"/>
      <path d="M7 10l2 2 4-4"/>
    </svg>
  );
}
function IconSalesChannel({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="2.5" fill="currentColor" fillOpacity="0.2"/>
      <circle cx="3" cy="5" r="1.5"/>
      <circle cx="17" cy="5" r="1.5"/>
      <circle cx="3" cy="15" r="1.5"/>
      <circle cx="17" cy="15" r="1.5"/>
      <path d="M4.5 5.5L7.5 8M12.5 8l3-2.5M4.5 14.5l3-2.5M12.5 12l3 2.5"/>
    </svg>
  );
}
function IconMicroCulture({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="6" cy="7" r="2" fill="currentColor" fillOpacity="0.15"/>
      <circle cx="14" cy="7" r="2" fill="currentColor" fillOpacity="0.15"/>
      <circle cx="10" cy="13" r="2" fill="currentColor" fillOpacity="0.15"/>
      <path d="M8 7h4M7.2 8.5L10 13M12.8 8.5L10 13"/>
    </svg>
  );
}
function IconAnthropocene({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7" fill="currentColor" fillOpacity="0.08"/>
      <path d="M10 3c0 0-4 3-4 7s4 7 4 7"/>
      <path d="M10 3c0 0 4 3 4 7s-4 7-4 7"/>
      <path d="M3 10h14"/>
    </svg>
  );
}
function IconSyntheticConsciousness({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3" fill="currentColor" fillOpacity="0.2"/>
      <path d="M10 2v2M10 16v2M2 10h2M16 10h2"/>
      <path d="M4.9 4.9l1.4 1.4M13.7 13.7l1.4 1.4M4.9 15.1l1.4-1.4M13.7 6.3l1.4-1.4"/>
      <circle cx="10" cy="10" r="6" strokeDasharray="2 2"/>
    </svg>
  );
}
function IconSingularityEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 16L7 10l3 3 3-5 4-4" fill="none"/>
      <path d="M3 16L7 10l3 3 3-5 4-4"/>
      <circle cx="17" cy="4" r="1.5" fill="currentColor" fillOpacity="0.4"/>
      <path d="M10 2v3M14 3l-2 2"/>
    </svg>
  );
}
function IconPostQuantum({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="4" y="7" width="12" height="9" rx="1.5" fill="currentColor" fillOpacity="0.1"/>
      <path d="M7 7V5a3 3 0 016 0v2"/>
      <circle cx="10" cy="11.5" r="1.5" fill="currentColor" fillOpacity="0.4"/>
      <path d="M10 13v2"/>
      <path d="M3 4l2 2M15 4l2 2M3 16l2-2M15 16l2 2"/>
    </svg>
  );
}
function IconMemetic({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="2" fill="currentColor" fillOpacity="0.2"/>
      <circle cx="4" cy="6" r="1.5" fill="currentColor" fillOpacity="0.1"/>
      <circle cx="16" cy="6" r="1.5" fill="currentColor" fillOpacity="0.1"/>
      <circle cx="4" cy="14" r="1.5" fill="currentColor" fillOpacity="0.1"/>
      <circle cx="16" cy="14" r="1.5" fill="currentColor" fillOpacity="0.1"/>
      <path d="M5.5 6.5L8.5 9M11.5 11l3 2.5M14.5 6.5L11.5 9M8.5 11l-3 2.5"/>
    </svg>
  );
}
function IconGameTheory({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="2" width="7" height="7" rx="1" fill="currentColor" fillOpacity="0.1"/>
      <rect x="11" y="2" width="7" height="7" rx="1" fill="currentColor" fillOpacity="0.1"/>
      <rect x="2" y="11" width="7" height="7" rx="1" fill="currentColor" fillOpacity="0.1"/>
      <rect x="11" y="11" width="7" height="7" rx="1" fill="currentColor" fillOpacity="0.1"/>
      <path d="M5.5 5.5l9 9M14.5 5.5l-9 9" strokeDasharray="2 2"/>
    </svg>
  );
}
function IconBioCompute({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3" fill="currentColor" fillOpacity="0.15"/>
      <path d="M10 2c0 0 2 2 2 5s-2 5-2 8" strokeDasharray="1 1.5"/>
      <path d="M10 2c0 0-2 2-2 5s2 5 2 8" strokeDasharray="1 1.5"/>
      <path d="M5 5.5c1.5.5 9 .5 10 0M5 14.5c1.5-.5 9-.5 10 0"/>
    </svg>
  );
}
function IconComplexNetwork({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="2" fill="currentColor" fillOpacity="0.3"/>
      <circle cx="4" cy="4" r="1.5" fill="currentColor" fillOpacity="0.1"/>
      <circle cx="16" cy="4" r="1.5" fill="currentColor" fillOpacity="0.1"/>
      <circle cx="4" cy="16" r="1.5" fill="currentColor" fillOpacity="0.1"/>
      <circle cx="16" cy="16" r="1.5" fill="currentColor" fillOpacity="0.1"/>
      <path d="M5.5 4.5L8.5 9M11.5 9l2.5-4.5M8.5 11l-4 4.5M11.5 11l4 4.5"/>
    </svg>
  );
}
function IconDigitalSovereignty({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 1l8 4v5c0 4.5-3.5 7.5-8 9-4.5-1.5-8-4.5-8-9V5z" fill="currentColor" fillOpacity="0.08"/>
      <path d="M10 1l8 4v5c0 4.5-3.5 7.5-8 9-4.5-1.5-8-4.5-8-9V5z"/>
      <path d="M10 6v5l3 2" strokeLinecap="round"/>
      <circle cx="10" cy="6" r="1" fill="currentColor"/>
    </svg>
  );
}

function IconTemporalIntelligence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="8"/>
      <path d="M10 5v5l3.5 3.5"/>
      <path d="M5 1.5l2 2M15 1.5l-2 2" strokeWidth="1.2"/>
    </svg>
  );
}
function IconGeopolitical({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="8"/>
      <path d="M2 10h16M10 2c-2 2-3 5-3 8s1 6 3 8M10 2c2 2 3 5 3 8s-1 6-3 8"/>
      <path d="M4 6h12M4 14h12" strokeWidth="1.1"/>
    </svg>
  );
}
function IconPredictiveArbitrage({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polyline points="2,15 7,8 11,11 16,4"/>
      <path d="M16 4h-3M16 4v3" strokeWidth="1.8"/>
      <path d="M2 18h16" strokeWidth="1.1"/>
      <circle cx="7" cy="8" r="1.2" fill="currentColor"/>
      <circle cx="11" cy="11" r="1.2" fill="currentColor"/>
    </svg>
  );
}

function IconFractionalOwnership({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="8"/>
      <path d="M10 2v16M2 10h16" strokeWidth="1.2"/>
      <path d="M5.5 5.5l9 9M14.5 5.5l-9 9" strokeWidth="0.9"/>
    </svg>
  );
}
function IconEmotionalCapital({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 17s-7-4.5-7-9a5 5 0 0 1 7-4.58A5 5 0 0 1 17 8c0 4.5-7 9-7 9z" fill="currentColor" fillOpacity="0.1"/>
      <path d="M10 17s-7-4.5-7-9a5 5 0 0 1 7-4.58A5 5 0 0 1 17 8c0 4.5-7 9-7 9z"/>
    </svg>
  );
}
function IconRegenFinance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 14c0-3.3 2.7-6 6-6s6 2.7 6 6"/>
      <path d="M10 8V4M8 6l2-2 2 2"/>
      <path d="M6 17a4 4 0 0 1 8 0" strokeWidth="1.1"/>
    </svg>
  );
}
function IconSovereignAI({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="3" width="14" height="14" rx="2"/>
      <path d="M7 7h6M7 10h4M7 13h5"/>
      <circle cx="14" cy="13" r="2" fill="currentColor" fillOpacity="0.3"/>
      <path d="M13.5 13.5l1 1"/>
    </svg>
  );
}
function IconHyperpersonalization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="7" r="3"/>
      <path d="M4 18c0-3.3 2.7-6 6-6s6 2.7 6 6"/>
      <path d="M15 4l1.5-1.5M17 7h1.5M15 10l1.5 1.5" strokeWidth="1.2"/>
    </svg>
  );
}
function IconFluidDynamics({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 10c2-4 4-4 6 0s4 4 6 0" strokeLinecap="round"/>
      <path d="M2 6c2-3 4-3 6 0s4 3 6 0" strokeLinecap="round" strokeWidth="1.1"/>
      <path d="M2 14c2-3 4-3 6 0s4 3 6 0" strokeLinecap="round" strokeWidth="1.1"/>
    </svg>
  );
}
function IconCollectiveConsciousness({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3" fill="currentColor" fillOpacity="0.2"/>
      <circle cx="10" cy="10" r="3"/>
      <circle cx="10" cy="3" r="1.5"/><circle cx="17" cy="10" r="1.5"/><circle cx="10" cy="17" r="1.5"/><circle cx="3" cy="10" r="1.5"/>
      <path d="M10 6v1M14 10h-1M10 14v-1M6 10h1"/>
      <path d="M13.2 6.8l-.7.7M13.2 13.2l-.7-.7M6.8 13.2l.7-.7M6.8 6.8l.7.7" strokeWidth="1"/>
    </svg>
  );
}
function IconARNeural({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 8h14M3 12h14" strokeWidth="1.1"/>
      <rect x="1" y="6" width="18" height="8" rx="2"/>
      <circle cx="10" cy="10" r="2"/>
      <path d="M10 4V2M10 18v-2" strokeWidth="1.2"/>
    </svg>
  );
}
function IconTemporalEngineering({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <path d="M10 5v5l3 2"/>
      <path d="M3 10h1M16 10h1M10 3v1M10 16v1" strokeWidth="1.1"/>
      <path d="M5.5 5.5l.7.7M14.5 5.5l-.7.7" strokeWidth="1"/>
    </svg>
  );
}
function IconNeuroadaptiveUX({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <ellipse cx="10" cy="8" rx="7" ry="5"/>
      <path d="M5 11c0 3 2 5 5 6 3-1 5-3 5-6"/>
      <path d="M7 8h.01M10 6h.01M13 8h.01" strokeWidth="2"/>
    </svg>
  );
}
function IconBiomimetic({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2c0 0-6 4-6 9a6 6 0 0 0 12 0c0-5-6-9-6-9z" fill="currentColor" fillOpacity="0.08"/>
      <path d="M10 2c0 0-6 4-6 9a6 6 0 0 0 12 0c0-5-6-9-6-9z"/>
      <path d="M10 8v6M7 11l3-3 3 3" strokeLinecap="round"/>
    </svg>
  );
}
function IconDarkData({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="8" fill="currentColor" fillOpacity="0.06"/>
      <circle cx="10" cy="10" r="8"/>
      <path d="M10 6v4l2.5 2.5" strokeLinecap="round"/>
      <path d="M6 10a4 4 0 0 0 4 4" strokeLinecap="round"/>
      <circle cx="10" cy="10" r="1.5" fill="currentColor"/>
    </svg>
  );
}
function IconQuantumSocial({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3"/>
      <circle cx="3" cy="5" r="1.5" fill="currentColor" fillOpacity="0.5"/>
      <circle cx="17" cy="5" r="1.5" fill="currentColor" fillOpacity="0.5"/>
      <circle cx="3" cy="15" r="1.5" fill="currentColor" fillOpacity="0.5"/>
      <circle cx="17" cy="15" r="1.5" fill="currentColor" fillOpacity="0.5"/>
      <path d="M4.5 5.5L8 8.5M15.5 5.5L12 8.5M4.5 14.5L8 11.5M15.5 14.5L12 11.5"/>
    </svg>
  );
}
function IconSyntheticLiquidation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="5" width="16" height="11" rx="2"/>
      <path d="M6 5V4a4 4 0 0 1 8 0v1"/>
      <path d="M10 10v3M8 11l2-1 2 1" strokeWidth="1.2"/>
      <path d="M2 9h16" strokeWidth="1.1"/>
    </svg>
  );
}

function IconMetamorphic({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 10c0-4 3-7 7-7s7 3 7 7"/>
      <path d="M17 10c0 4-3 7-7 7"/>
      <path d="M3 10c0 4 3 7 7 7"/>
      <path d="M10 6l2 4-2 4"/>
      <path d="M8 10h4" strokeWidth="1.2"/>
    </svg>
  );
}
function IconPredictiveTalent({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="8" cy="7" r="3"/>
      <path d="M2 17c0-3 2.7-5 6-5s6 2 6 5"/>
      <path d="M14 9l2 2 3-3" strokeWidth="1.3"/>
    </svg>
  );
}
function IconPlanetaryIntel({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <ellipse cx="10" cy="10" rx="4" ry="7"/>
      <path d="M3 10h14" strokeWidth="1.1"/>
      <path d="M5 6h10M5 14h10" strokeWidth="0.9"/>
    </svg>
  );
}
function IconExistentialRisk({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2L2 16h16L10 2z"/>
      <path d="M10 8v4" strokeWidth="1.8"/>
      <circle cx="10" cy="14" r="0.8" fill="currentColor"/>
    </svg>
  );
}

function IconQuantumResilience({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <path d="M10 6v4l2.5 2.5"/>
      <path d="M6.5 6.5l1 1M13.5 6.5l-1 1M6.5 13.5l1-1M13.5 13.5l-1-1" strokeWidth="1"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" opacity="0.3"/>
    </svg>
  );
}
function IconBioDigital({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 10c0-3.3 2.7-6 6-6s6 2.7 6 6-2.7 6-6 6"/>
      <path d="M4 10c2 0 3-1 3-3s1-3 3-3"/>
      <path d="M10 17c-2 0-3-1-3-3"/>
      <circle cx="4" cy="10" r="1.5" fill="currentColor"/>
    </svg>
  );
}
function IconNeuroEconomic({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 10c0-2.8 2.2-5 5-5s5 2.2 5 5"/>
      <path d="M5 10c0 2 1 3.5 2.5 4.5"/>
      <path d="M15 10c0 2-1 3.5-2.5 4.5"/>
      <path d="M8 10h4M10 8v4" strokeWidth="1.2"/>
      <path d="M3 7l2 1M17 7l-2 1" strokeWidth="1"/>
    </svg>
  );
}
function IconCivilizationalMemory({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 17V8l7-5 7 5v9"/>
      <rect x="7" y="11" width="3" height="6" rx="0.5"/>
      <rect x="11" y="11" width="3" height="4" rx="0.5"/>
      <path d="M2 17h16" strokeWidth="1.2"/>
    </svg>
  );
}
function IconHyperconnectivity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="2"/>
      <circle cx="3" cy="5" r="1.5"/>
      <circle cx="17" cy="5" r="1.5"/>
      <circle cx="3" cy="15" r="1.5"/>
      <circle cx="17" cy="15" r="1.5"/>
      <path d="M4.5 5.5L8.5 8.5M15.5 5.5l-4 3M4.5 14.5L8.5 11.5M15.5 14.5l-4-3" strokeWidth="1.1"/>
    </svg>
  );
}
function IconAutoFinancial({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <path d="M10 6v2M10 12v2"/>
      <path d="M7.5 8.5A2.5 2.5 0 0 1 10 7.5h1.5a1.5 1.5 0 0 1 0 3h-3a1.5 1.5 0 0 0 0 3H10a2.5 2.5 0 0 0 2.5-1"/>
    </svg>
  );
}
function IconCollectiveAmplification({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="5" cy="8" r="2"/>
      <circle cx="15" cy="8" r="2"/>
      <circle cx="10" cy="14" r="2"/>
      <path d="M7 8h6M5.7 9.7L9 13M14.3 9.7L11 13" strokeWidth="1.1"/>
      <path d="M10 4v2" strokeWidth="1.2"/>
    </svg>
  );
}

function IconPostHuman({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="7" r="3"/>
      <path d="M4 17c0-3.3 2.7-6 6-6s6 2.7 6 6"/>
      <path d="M14 4l2-2M16 6h2M14 10l2 2" strokeWidth="1.1"/>
    </svg>
  );
}
function IconNarrativeControl({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 6h14M3 10h10M3 14h7"/>
      <circle cx="16" cy="14" r="2.5"/>
      <path d="M16 11.5v0M16 16.5v0" strokeWidth="2"/>
    </svg>
  );
}
function IconSemanticKG({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="2"/>
      <circle cx="4" cy="4" r="1.5"/>
      <circle cx="16" cy="4" r="1.5"/>
      <circle cx="4" cy="16" r="1.5"/>
      <circle cx="16" cy="16" r="1.5"/>
      <path d="M5.5 5.1L8.6 8.2M14.5 5.1L11.4 8.2M5.5 14.9L8.6 11.8M14.5 14.9L11.4 11.8" strokeWidth="1"/>
    </svg>
  );
}
function IconExponentialTech({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 16 Q5 14 8 10 Q11 6 14 4 Q16 3 18 2"/>
      <path d="M14 2h4v4" strokeWidth="1.3"/>
      <path d="M2 10h3M2 13h2" strokeWidth="1" opacity="0.5"/>
    </svg>
  );
}
function IconPsychographic({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 10c0-2.8 2.2-5 5-5s5 2.2 5 5c0 1.5-.7 2.9-1.7 3.8"/>
      <path d="M8 10c0-1.1.9-2 2-2s2 .9 2 2"/>
      <path d="M10 15v2M7 16l1-1M13 16l-1-1" strokeWidth="1.1"/>
    </svg>
  );
}
function IconEnergyTransition({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2v4M10 14v4M2 10h4M14 10h4"/>
      <circle cx="10" cy="10" r="3"/>
      <path d="M4.9 4.9l2.8 2.8M12.3 12.3l2.8 2.8M4.9 15.1l2.8-2.8M12.3 7.7l2.8-2.8" strokeWidth="1.1"/>
    </svg>
  );
}
function IconSyntheticMedia({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="4" width="12" height="9" rx="1"/>
      <path d="M14 8l4-2v8l-4-2"/>
      <path d="M6 8.5l3 2-3 2v-4z" fill="currentColor" opacity="0.4"/>
    </svg>
  );
}
function IconLongevityEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="7" r="3"/>
      <path d="M5 17v-1a5 5 0 0 1 10 0v1"/>
      <path d="M15 4c1.5.5 2.5 2 2.5 3.5 0 2-1.5 3.5-3.5 4" strokeWidth="1.1"/>
    </svg>
  );
}
function IconCryptoGovernance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2L4 5v5c0 3.5 2.7 6.7 6 7.5 3.3-.8 6-4 6-7.5V5l-6-3z"/>
      <path d="M7.5 10l2 2 3-3" strokeWidth="1.3"/>
    </svg>
  );
}
function IconAIAlignment({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="5" width="14" height="10" rx="2"/>
      <circle cx="7" cy="10" r="1.5"/>
      <circle cx="13" cy="10" r="1.5"/>
      <path d="M7 10h6" strokeWidth="1.1"/>
      <path d="M10 5V3M10 17v-2" strokeWidth="1.2"/>
    </svg>
  );
}
function IconDAOGovernance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3"/>
      <circle cx="3" cy="10" r="2"/>
      <circle cx="17" cy="10" r="2"/>
      <circle cx="10" cy="3" r="2"/>
      <circle cx="10" cy="17" r="2"/>
      <path d="M5 10h2M13 10h2M10 5v2M10 13v2" strokeWidth="1.1"/>
    </svg>
  );
}
function IconOmegaSynthesis({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2a8 8 0 1 0 0 16A8 8 0 0 0 10 2z"/>
      <path d="M6 14c0-2.2 1.8-4 4-4s4 1.8 4 4"/>
      <path d="M8 10c0-1.1.9-2 2-2s2 .9 2 2"/>
      <circle cx="10" cy="8" r="1" fill="currentColor"/>
    </svg>
  );
}

function IconAutonomousEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="10" width="4" height="7" rx="1"/>
      <rect x="8" y="7" width="4" height="10" rx="1"/>
      <rect x="13" y="4" width="4" height="13" rx="1"/>
      <path d="M5 7l3-3 4 2 4-4"/>
    </svg>
  );
}

function IconSyntheticBiology({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M7 3c0 3 6 3 6 6s-6 3-6 6"/>
      <path d="M13 3c0 3-6 3-6 6s6 3 6 6"/>
      <line x1="5" y1="6" x2="15" y2="6"/>
      <line x1="5" y1="10" x2="15" y2="10"/>
      <line x1="5" y1="14" x2="15" y2="14"/>
    </svg>
  );
}

function IconEmotionalContagion({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="8" r="3"/>
      <path d="M4 17c0-2.8 2.7-5 6-5s6 2.2 6 5"/>
      <path d="M2 10c1-1 2 1 3 0s2-2 3 0"/>
      <path d="M12 10c1-1 2 1 3 0s2-2 3 0"/>
    </svg>
  );
}

function IconCriticalResource({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l2.5 5h5l-4 3.5 1.5 5.5L10 13l-5 3 1.5-5.5L2.5 7h5z"/>
    </svg>
  );
}

function IconClimateTipping({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 14c2-4 4-6 8-6s6 2 8 6"/>
      <path d="M10 8V4"/>
      <path d="M7 5l3-3 3 3"/>
      <circle cx="10" cy="16" r="2"/>
    </svg>
  );
}

function IconDigitalTwin({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="5" width="6" height="10" rx="1"/>
      <rect x="12" y="5" width="6" height="10" rx="1"/>
      <path d="M8 10h4"/>
      <path d="M9 8l-1 2 1 2"/>
      <path d="M11 8l1 2-1 2"/>
    </svg>
  );
}


function IconUrbanIntel({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="10" width="4" height="8"/>
      <rect x="8" y="6" width="4" height="12"/>
      <rect x="14" y="3" width="4" height="15"/>
      <path d="M2 10l4-4 4 2 4-4 4 2"/>
    </svg>
  );
}

function IconSovereignDebt({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="8"/>
      <path d="M10 6v2m0 4v2"/>
      <path d="M7.5 8.5A2.5 2.5 0 0 1 10 7c1.38 0 2.5.84 2.5 2 0 1.5-2.5 2-2.5 3.5"/>
    </svg>
  );
}

function IconNeuroBCI({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M6 10c0-2.2 1.8-4 4-4s4 1.8 4 4c0 1.5-.8 2.8-2 3.5V16H8v-2.5C6.8 12.8 6 11.5 6 10z"/>
      <path d="M8 7.5c-.5-1-1.5-1.5-2-1"/>
      <path d="M12 7.5c.5-1 1.5-1.5 2-1"/>
      <path d="M2 10h2m14 0h-2"/>
    </svg>
  );
}

function IconSupplyChain({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="4" cy="10" r="2"/>
      <circle cx="10" cy="5" r="2"/>
      <circle cx="16" cy="10" r="2"/>
      <circle cx="10" cy="15" r="2"/>
      <path d="M6 10h2M12 10h2M10 7v2M10 13v-2"/>
    </svg>
  );
}

function IconAllianceFracture({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="5" cy="5" r="2"/>
      <circle cx="15" cy="5" r="2"/>
      <circle cx="5" cy="15" r="2"/>
      <circle cx="15" cy="15" r="2"/>
      <path d="M7 5h6M5 7v6M15 7v6M7 15h6"/>
      <path d="M9 9l2 2" strokeDasharray="2 1"/>
    </svg>
  );
}

function IconFirstPrinciples({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2v4M2 10h4M14 10h4M10 14v4"/>
      <circle cx="10" cy="10" r="3"/>
      <path d="M5.5 5.5l2 2M12.5 12.5l2 2M5.5 14.5l2-2M12.5 7.5l2-2"/>
    </svg>
  );
}

function IconBottleneckSniper({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 10h14"/>
      <path d="M3 6h6v8H3z"/>
      <circle cx="14" cy="10" r="3"/>
      <path d="M14 7v1M14 12v1M11 10h1M16 10h1"/>
    </svg>
  );
}

function IconEconomicSingularity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 16C4 12 6 8 8 6s4-2 10-4"/>
      <circle cx="18" cy="2" r="1.5" fill="currentColor"/>
      <path d="M2 18l16-16"/>
    </svg>
  );
}

function IconSystemAwareness({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3"/>
      <path d="M10 4a6 6 0 0 1 6 6"/>
      <path d="M10 16a6 6 0 0 1-6-6"/>
      <path d="M4 10a6 6 0 0 1 6-6"/>
      <path d="M16 10a6 6 0 0 1-6 6"/>
      <path d="M10 2v2M10 16v2M2 10H4M16 10h2"/>
    </svg>
  );
}

function IconDarkPattern({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="3" width="14" height="14" rx="2"/>
      <path d="M7 10h6M10 7l3 3-3 3"/>
      <circle cx="10" cy="10" r="1" fill="currentColor"/>
    </svg>
  );
}

function IconWaterGeo({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3c0 0-5 4-5 8a5 5 0 0010 0c0-4-5-8-5-8z"/>
      <path d="M7 13h6M6 10h8"/>
    </svg>
  );
}

function IconFoodSystem({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3v14M7 5c0 0-3 2-3 5s3 5 3 5"/>
      <path d="M13 5c0 0 3 2 3 5s-3 5-3 5"/>
      <path d="M6 10h8"/>
    </svg>
  );
}

function IconPension({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="6" r="3"/>
      <path d="M4 17c0-3.3 2.7-6 6-6s6 2.7 6 6"/>
      <path d="M7 17l1-3h4l1 3"/>
      <path d="M9 14h2"/>
    </svg>
  );
}

function IconCognitiveBias({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M6 10c0-2.2 1.8-4 4-4s4 1.8 4 4c0 1.5-.8 2.8-2 3.5V15h-4v-1.5C6.8 12.8 6 11.5 6 10z"/>
      <path d="M9 15h2M8 17h4"/>
      <path d="M4 10H3M17 10h-1M10 3V2M15 5l-.7.7M5 5l.7.7"/>
    </svg>
  );
}

function IconTechnoFeudal({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="7" y="2" width="6" height="5" rx="1"/>
      <path d="M4 17V9l6-2 6 2v8"/>
      <path d="M8 17v-4h4v4"/>
      <path d="M4 17h12"/>
    </svg>
  );
}

function IconCognitiveWarfare({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M6 10c0-2.2 1.8-4 4-4s4 1.8 4 4"/>
      <path d="M3 10h2M15 10h2"/>
      <path d="M10 6V4M14.2 5.8l-1.4 1.4M5.8 5.8l1.4 1.4"/>
      <path d="M8 13l-3 4M12 13l3 4"/>
      <path d="M10 10v4"/>
    </svg>
  );
}

function IconLongevityTech({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3a7 7 0 100 14A7 7 0 0010 3z"/>
      <path d="M10 7v3l2 2"/>
      <path d="M6 3.5L4 2M14 3.5l2-1.5"/>
    </svg>
  );
}

function IconPandemic({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3"/>
      <circle cx="10" cy="10" r="6" strokeDasharray="2 2"/>
      <path d="M10 4V2M10 18v-2M4 10H2M18 10h-2"/>
      <path d="M5.6 5.6L4.2 4.2M15.8 15.8l-1.4-1.4M14.4 5.6l1.4-1.4M4.2 15.8l1.4-1.4"/>
    </svg>
  );
}

function IconNuclear({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="2"/>
      <path d="M10 8V4M10 8l-3.5-2M10 8l3.5-2"/>
      <circle cx="10" cy="10" r="6"/>
      <path d="M6.3 14.5L4 17M13.7 14.5l2.3 2.5"/>
    </svg>
  );
}

function IconOcean({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 8c1.5 0 1.5-2 3-2s1.5 2 3 2 1.5-2 3-2 1.5 2 3 2 1.5-2 3-2"/>
      <path d="M2 12c1.5 0 1.5-2 3-2s1.5 2 3 2 1.5-2 3-2 1.5 2 3 2 1.5-2 3-2"/>
      <path d="M2 16c1.5 0 1.5-2 3-2s1.5 2 3 2 1.5-2 3-2 1.5 2 3 2 1.5-2 3-2"/>
    </svg>
  );
}

function IconSoftPower({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <path d="M10 3c-2 2-3 4.5-3 7s1 5 3 7"/>
      <path d="M10 3c2 2 3 4.5 3 7s-1 5-3 7"/>
      <path d="M3 10h14"/>
      <path d="M3.5 7h13M3.5 13h13"/>
    </svg>
  );
}

function IconCircularEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3a7 7 0 0 1 7 7"/>
      <path d="M17 10a7 7 0 0 1-7 7"/>
      <path d="M10 17a7 7 0 0 1-7-7"/>
      <path d="M3 10a7 7 0 0 1 7-7"/>
      <path d="M14 6l3-3 1 4-4-1"/>
      <circle cx="10" cy="10" r="2"/>
    </svg>
  );
}

function IconDigitalDemocracy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="5" width="14" height="10" rx="2"/>
      <path d="M7 9l2 2 4-4"/>
      <path d="M3 8h14"/>
    </svg>
  );
}

function IconSpaceEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="2"/>
      <ellipse cx="10" cy="10" rx="7" ry="3"/>
      <ellipse cx="10" cy="10" rx="3" ry="7"/>
      <circle cx="10" cy="3" r="1" fill="currentColor"/>
    </svg>
  );
}

function IconBehavioralFinance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 15l4-6 3 4 3-7 4 9"/>
      <path d="M3 5v12h14"/>
    </svg>
  );
}

function IconBiometricSurveillance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 4C7 4 4.5 6 4 9c-.5 3 1 6 6 7 5-1 6.5-4 6-7-.5-3-3-5-6-5z"/>
      <circle cx="10" cy="10" r="2"/>
      <path d="M10 8v-2M10 14v-2M8 10H6M14 10h-2"/>
    </svg>
  );
}

function IconGigEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="6" cy="6" r="2"/>
      <circle cx="14" cy="6" r="2"/>
      <circle cx="10" cy="14" r="2"/>
      <path d="M6 8v4M14 8v4M8 14h4"/>
    </svg>
  );
}

function IconSurveillanceCap({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="8" r="4"/>
      <path d="M10 12v5M7 17h6"/>
      <path d="M14 5l3-2M6 5L3 3"/>
    </svg>
  );
}

function IconNeuralLanguage({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 6h14M3 10h10M3 14h12"/>
      <circle cx="16" cy="10" r="2"/>
      <path d="M14 10h-1"/>
    </svg>
  );
}

function IconMilitaryAI({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6z"/>
    </svg>
  );
}

function IconMigrationCrisis({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 10h14M13 6l4 4-4 4"/>
      <circle cx="5" cy="10" r="2"/>
    </svg>
  );
}

function IconCorporateCapture({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="6" y="3" width="8" height="8" rx="1"/>
      <path d="M4 11v6h12v-6"/>
      <path d="M8 11v6M12 11v6"/>
    </svg>
  );
}

function IconEpigeneticHealth({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M7 4c0 0 2 2 2 6s-2 6-2 6"/>
      <path d="M13 4c0 0-2 2-2 6s2 6 2 6"/>
      <path d="M7 7h6M7 13h6"/>
    </svg>
  );
}

function IconCulturalHeritage({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 17V9l6-5 6 5v8"/>
      <rect x="8" y="13" width="4" height="4"/>
      <path d="M4 9h12"/>
    </svg>
  );
}

function IconHypersonic({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 10l12-6-2 6 2 6z"/>
      <path d="M14 7l4 3-4 3"/>
      <path d="M12 10h6"/>
    </svg>
  );
}

function IconWealthConcentration({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3"/>
      <path d="M10 3v2M10 15v2M3 10h2M15 10h2"/>
      <path d="M5.6 5.6l1.4 1.4M13 13l1.4 1.4M13 7l1.4-1.4M5.6 14.4l1.4-1.4"/>
    </svg>
  );
}

function IconPsychopolitics({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M6 10c0-2.2 1.8-4 4-4s4 1.8 4 4c0 1.5-.8 2.8-2 3.5V15h-4v-1.5C6.8 12.8 6 11.5 6 10z"/>
      <path d="M9 15h2"/>
      <path d="M4 6L2 4M16 6l2-4"/>
      <path d="M3 10H1M19 10h-2"/>
    </svg>
  );
}

// ─── Wave 345-360 icons ─────────────────────────────────────────────────────

function IconMethaneCrisis({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3c0 0-4 4-4 7a4 4 0 0 0 8 0c0-3-4-7-4-7z"/>
      <path d="M8 13c0 0-.5-2 2-2s2 2 2 2"/>
      <circle cx="4" cy="5" r="1"/>
      <circle cx="16" cy="5" r="1"/>
      <path d="M4 5c1 2 2 3 2 5"/>
    </svg>
  );
}

function IconAlgorithmicJustice({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2v3M10 5l-5 3M10 5l5 3"/>
      <path d="M5 8l-3 5h6L5 8zM15 8l-3 5h6l-3-5z"/>
      <path d="M3 16h14"/>
      <path d="M10 13v3"/>
    </svg>
  );
}

function IconRareEarth({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l2 4h4l-3 3 1 4-4-2-4 2 1-4-3-3h4z"/>
      <path d="M10 10l-6 6M10 10l6 6"/>
    </svg>
  );
}

function IconSocialCredit({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="7" r="3"/>
      <path d="M4 17c0-3.3 2.7-6 6-6s6 2.7 6 6"/>
      <path d="M14 3l1 1-1 1M16 4h-3"/>
      <path d="M6 3L5 4l1 1M4 4h3"/>
    </svg>
  );
}

function IconAltProtein({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 10c0-3.3 2.7-6 6-6s6 2.7 6 6-2.7 6-6 6"/>
      <path d="M10 4v12M4 10h12"/>
      <circle cx="7" cy="7" r="1" fill="currentColor"/>
      <circle cx="13" cy="7" r="1" fill="currentColor"/>
      <circle cx="7" cy="13" r="1" fill="currentColor"/>
    </svg>
  );
}

function IconGenAIEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l1 3h3l-2.5 2 1 3L10 8.5 7.5 10l1-3L6 5h3z"/>
      <path d="M3 14l3-3 4 2 4-4 3 1"/>
      <path d="M2 17h16"/>
    </svg>
  );
}

function IconInfraResilience({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 14h16"/>
      <path d="M4 14V9M8 14V7M12 14V9M16 14V7"/>
      <path d="M2 9l4-5 4 3 4-5 4 3"/>
    </svg>
  );
}

function IconFinancialCrime({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="6" width="14" height="9" rx="1"/>
      <path d="M7 6V4a3 3 0 0 1 6 0v2"/>
      <path d="M10 11v-2M10 13v0"/>
      <path d="M15 9l2-2M5 9L3 7"/>
    </svg>
  );
}

function IconDigitalTwins({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="5" width="6" height="10" rx="1"/>
      <rect x="12" y="5" width="6" height="10" rx="1"/>
      <path d="M8 10h4"/>
      <path d="M5 7h2M5 9h2M5 11h2M13 7h2M13 9h2M13 11h2"/>
    </svg>
  );
}

function IconUrbanHeat({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 16h14"/>
      <path d="M4 16V11h3v5M9 16V8h3v8M14 16V12h3v4"/>
      <circle cx="10" cy="4" r="2"/>
      <path d="M7 4H5M15 4h-2M10 2V1M10 7v1"/>
    </svg>
  );
}

function IconMisinformation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="2"/>
      <path d="M4 4l3 3M13 13l3 3M16 4l-3 3M7 13l-3 3"/>
      <circle cx="4" cy="4" r="1.5"/>
      <circle cx="16" cy="4" r="1.5"/>
      <circle cx="4" cy="16" r="1.5"/>
      <circle cx="16" cy="16" r="1.5"/>
    </svg>
  );
}

function IconSoilDegradation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 14h16"/>
      <path d="M4 14c0-4 2-6 3-8M7 14c1-3 1-5 3-6M10 14c0-2 2-4 3-5M13 14c1-2 2-3 3-4"/>
      <path d="M2 17c2-1 4-2 8-2s6 1 8 2" opacity=".5"/>
    </svg>
  );
}

function IconCyberSovereignty({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="8"/>
      <path d="M10 2c0 0-4 2-4 8s4 8 4 8M10 2c0 0 4 2 4 8s-4 8-4 8"/>
      <path d="M2 10h16"/>
      <path d="M13 6l2-2 2 2-2 2z"/>
    </svg>
  );
}

function IconAntibioticResistance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="4"/>
      <path d="M10 6V4M10 16v-2M6 10H4M16 10h-2"/>
      <path d="M7 7L5 5M15 15l-2-2M13 7l2-2M5 15l2-2"/>
      <path d="M8 10l4 0M10 8v4"/>
    </svg>
  );
}

function IconClimateFinance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3c-1.5 0-3 1-3 2.5C7 7 8.5 7.5 10 8s3 1 3 2.5C13 12 11.5 13 10 13s-3-1-3-2.5"/>
      <path d="M10 2v1M10 13v1"/>
      <path d="M5 16c1.5-1 3-1.5 5-1.5s3.5.5 5 1.5"/>
      <path d="M3 8l3-4M17 8l-3-4"/>
    </svg>
  );
}

function IconAIGovernance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M6 4h8l2 4-2 4H6L4 8z"/>
      <path d="M8 8h4M10 6v4"/>
      <path d="M7 12l-3 5h12l-3-5"/>
    </svg>
  );
}

// ─── Wave 361-368 icons ─────────────────────────────────────────────────────

function IconDemographicWinter({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2v2M5 5l1.5 1.5M15 5l-1.5 1.5"/>
      <circle cx="10" cy="9" r="3"/>
      <path d="M4 17c0-3 2.7-6 6-6s6 3 6 6"/>
      <path d="M7 17c0 0 .5-2 3-2s3 2 3 2" strokeDasharray="2 2"/>
    </svg>
  );
}

function IconSatelliteConstellation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3"/>
      <path d="M10 7V3M10 17v-4M7 10H3M17 10h-4"/>
      <circle cx="4" cy="4" r="1.5" fill="currentColor" stroke="none"/>
      <circle cx="16" cy="4" r="1.5" fill="currentColor" stroke="none"/>
      <circle cx="4" cy="16" r="1.5" fill="currentColor" stroke="none"/>
      <circle cx="16" cy="16" r="1.5" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconDeFiRisk({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l2 3h3l-2.5 2 1 3.5L10 9l-3.5 1.5 1-3.5L5 5h3z"/>
      <path d="M5 14l3 1 2-2 2 2 3-1"/>
      <path d="M3 17h14"/>
      <path d="M10 11v2"/>
    </svg>
  );
}

function IconCognitiveEnhancement({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M6 10c0-2.2 1.8-4 4-4s4 1.8 4 4-1.8 4-4 4"/>
      <path d="M10 6V4M14 8l1.5-1.5M14 12l1.5 1.5"/>
      <path d="M7 7.5L5 6M7 12.5L5 14"/>
      <circle cx="10" cy="10" r="1.5" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconTaxJustice({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l1.5 3h3l-2.5 2 1 3-3-2-3 2 1-3L5.5 5h3z"/>
      <path d="M3 16h14"/>
      <path d="M5 16V12l5 2 5-2v4"/>
    </svg>
  );
}

function IconArcticSovereignty({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="8"/>
      <path d="M10 2v4M10 14v4M6 6l2 4-2 4M14 6l-2 4 2 4"/>
      <path d="M2 10h4M14 10h4"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconQuantumDisruption({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3c-4 0-7 3-7 7s3 7 7 7 7-3 7-7-3-7-7-7z"/>
      <path d="M6 7l4 3 4-3M6 13l4-3 4 3"/>
      <path d="M10 6v8"/>
    </svg>
  );
}

function IconDigitalHealthSov({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3c-3.9 0-7 3.1-7 7 0 2.7 1.5 5 3.8 6.3L10 18l3.2-1.7C15.5 15 17 12.7 17 10c0-3.9-3.1-7-7-7z"/>
      <path d="M8 10h4M10 8v4"/>
    </svg>
  );
}

// ─── Wave 369-376 icons ─────────────────────────────────────────────────────

function IconCarbonCredit({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 16c2-4 4-6 5-6s3 2 5 6"/>
      <path d="M6 10c1-2 2-4 4-6 2 2 3 4 4 6"/>
      <path d="M8 4l2-2 2 2"/>
      <path d="M10 2v12"/>
      <path d="M3 17h14"/>
    </svg>
  );
}

function IconSpaceDebris({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3"/>
      <path d="M5 5l2 2M13 5l-2 2M5 15l2-2M13 15l-2-2"/>
      <circle cx="4" cy="7" r="1" fill="currentColor" stroke="none"/>
      <circle cx="16" cy="6" r="1" fill="currentColor" stroke="none"/>
      <circle cx="3" cy="13" r="1" fill="currentColor" stroke="none"/>
      <circle cx="15" cy="15" r="1" fill="currentColor" stroke="none"/>
      <circle cx="8" cy="3" r="1" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconDigitalColonialism({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <path d="M10 3c0 0-3 2-3 7s3 7 3 7M10 3c0 0 3 2 3 7s-3 7-3 7"/>
      <path d="M3 10h14"/>
      <path d="M7 6h6M7 14h6"/>
      <path d="M13 8l2-1"/>
    </svg>
  );
}

function IconOceanAcidification({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 14c1-2 2-3 3.5-3S9 12 10 12s2.5-1 3.5-1S16 12 17 14"/>
      <path d="M3 17c1-2 2-3 3.5-3S9 15 10 15s2.5-1 3.5-1S16 15 17 17"/>
      <path d="M10 3v5M8 4l2-2 2 2"/>
      <path d="M7 8h6"/>
    </svg>
  );
}

function IconNuclearFusion({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3"/>
      <ellipse cx="10" cy="10" rx="8" ry="3" transform="rotate(0)"/>
      <ellipse cx="10" cy="10" rx="8" ry="3" transform="rotate(60 10 10)"/>
      <ellipse cx="10" cy="10" rx="8" ry="3" transform="rotate(120 10 10)"/>
    </svg>
  );
}

function IconPostWork({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 10h10"/>
      <path d="M5 10l-3 5h16l-3-5"/>
      <path d="M8 5h4M10 3v4"/>
      <path d="M7 10V8M10 10V7M13 10V8"/>
      <path d="M6 15l1-2M14 15l-1-2M10 15v-2"/>
    </svg>
  );
}

function IconGeoengineering({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 12c2-4 4-6 7-6s5 2 7 6"/>
      <path d="M3 12c0 3 3 5 7 5s7-2 7-5"/>
      <path d="M10 6V2M8 3l2-2 2 2"/>
      <path d="M6 8l-3-2M14 8l3-2"/>
    </svg>
  );
}

function IconDigitalIdentity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="5" width="14" height="10" rx="1"/>
      <circle cx="7" cy="10" r="2"/>
      <path d="M11 8h5M11 10h4M11 12h3"/>
      <path d="M5 15l2-2"/>
    </svg>
  );
}

// ─── Wave 377-384 icons ─────────────────────────────────────────────────────

function IconGeneDrive({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M6 3c0 0 2 2 2 4S6 11 6 13s2 4 2 4"/>
      <path d="M14 3c0 0-2 2-2 4s2 4 2 4-2 2-2 4 2 4 2 4"/>
      <path d="M8 7h4M8 13h4M7 10h6"/>
    </svg>
  );
}

function IconSyntheticReality({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="5" width="16" height="10" rx="1"/>
      <circle cx="10" cy="10" r="3"/>
      <path d="M7 10c0-1.7 1.3-3 3-3"/>
      <path d="M13 10c0 1.7-1.3 3-3 3"/>
      <path d="M2 8l3 2-3 2M18 8l-3 2 3 2"/>
    </svg>
  );
}

function IconEnergyPoverty({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M11 2L7 10h5l-3 8 8-10h-5l3-6z"/>
      <path d="M3 14l2 2M3 10H1M3 6l2-2"/>
    </svg>
  );
}

function IconBatteryGeopolitics({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="7" width="14" height="7" rx="1"/>
      <path d="M16 9v3"/>
      <path d="M5 7V5h6v2"/>
      <path d="M5 10h4M5 13h2"/>
    </svg>
  );
}

function IconCorporateSurveillance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="3" width="16" height="12" rx="1"/>
      <path d="M2 15l16 0M8 18h4"/>
      <circle cx="10" cy="9" r="2"/>
      <path d="M7 9c0-1.7 1.3-3 3-3M13 9c0 1.7-1.3 3-3 3"/>
    </svg>
  );
}

function IconGlobalHealthSecurity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l6 3v5c0 4-2.7 7-6 8C7 17 4 14 4 10V5z"/>
      <path d="M8 10h4M10 8v4"/>
    </svg>
  );
}

function IconIndustrialPolicy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 16h16"/>
      <path d="M4 16V9l3-3v10M9 16V6l3-3v13M14 16V9l3-3v10"/>
      <path d="M2 13h2M8 13h2M14 13h2"/>
    </svg>
  );
}

function IconDarkWebEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <path d="M10 3c-2 1.5-3.5 4-3.5 7s1.5 5.5 3.5 7"/>
      <path d="M10 3c2 1.5 3.5 4 3.5 7s-1.5 5.5-3.5 7"/>
      <path d="M3 10h14"/>
      <path d="M5 6l2 1M15 6l-2 1M5 14l2-1M15 14l-2-1"/>
    </svg>
  );
}

function IconRefugeeCrisis({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="7" cy="5" r="2"/>
      <path d="M3 17c0-3.314 2.239-6 4-6s3 1 5 1 3-2 4-2"/>
      <path d="M11 10l3-2 3 2M14 8v5"/>
      <path d="M12 13l2 2 2-2"/>
    </svg>
  );
}

function IconCryptoRegulation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <path d="M8 7h3a2 2 0 0 1 0 4H8v4"/>
      <path d="M8 7V5M10 15v2"/>
      <path d="M14 4l3 3-3 3"/>
    </svg>
  );
}

function IconSmartCity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="10" width="5" height="8"/>
      <rect x="7.5" y="6" width="5" height="12"/>
      <rect x="13" y="8" width="5" height="10"/>
      <path d="M2 10l4-4 4-3 5 5"/>
      <circle cx="15" cy="4" r="1.5" fill="currentColor" stroke="none" opacity="0.7"/>
      <path d="M13 4 A2 2 0 0 1 17 4" opacity="0.5"/>
    </svg>
  );
}

function IconIPWarfare({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l2 4 4 1-3 3 1 4-4-2-4 2 1-4-3-3 4-1z"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" stroke="none" opacity="0.6"/>
      <path d="M3 17l4-4M17 17l-4-4"/>
    </svg>
  );
}

function IconDeepSeaMining({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 8c3-2 5-3 8-3s5 1 8 3"/>
      <path d="M2 8c0 5 3 9 8 9s8-4 8-9"/>
      <path d="M10 8v5"/>
      <path d="M8 11l2 2 2-2"/>
      <circle cx="10" cy="14.5" r="1" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconBiosurveillance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3"/>
      <path d="M10 2v2M10 16v2M2 10h2M16 10h2"/>
      <path d="M4.93 4.93l1.41 1.41M13.66 13.66l1.41 1.41M4.93 15.07l1.41-1.41M13.66 6.34l1.41-1.41"/>
      <circle cx="10" cy="10" r="6" opacity="0.3"/>
    </svg>
  );
}

function IconAgingInfra({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 17h16"/>
      <path d="M4 17V9l6-6 6 6v8"/>
      <path d="M8 17v-5h4v5"/>
      <path d="M3 12l1-1M17 12l-1-1"/>
      <path d="M7 7l1 1M13 7l-1 1" opacity="0.5"/>
    </svg>
  );
}

function IconWorkerAutomation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="7" y="2" width="6" height="5" rx="1"/>
      <path d="M10 7v3"/>
      <path d="M5 10h10"/>
      <path d="M5 10l-2 5M15 10l2 5"/>
      <path d="M3 15h4M13 15h4"/>
      <circle cx="10" cy="10" r="1.5" fill="currentColor" stroke="none" opacity="0.5"/>
    </svg>
  );
}

function IconAutonomousVehicle({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 12l2-5h10l2 5"/>
      <rect x="2" y="12" width="16" height="4" rx="2"/>
      <circle cx="6" cy="16" r="1.5"/>
      <circle cx="14" cy="16" r="1.5"/>
      <path d="M8 9h4" opacity="0.5"/>
      <circle cx="10" cy="6" r="2" opacity="0.6"/>
    </svg>
  );
}

function IconCBDC({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="8"/>
      <path d="M10 5v10M7 7.5h4.5a2 2 0 0 1 0 4H7a2 2 0 0 1 0-4z" opacity="0.7"/>
      <path d="M13 3l3-1M7 17l-3 1"/>
    </svg>
  );
}

function IconReproductiveRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="8" r="4"/>
      <path d="M10 12v7"/>
      <path d="M7 16h6"/>
      <path d="M14 4l3-3M16 4l1-3" opacity="0.5"/>
    </svg>
  );
}

function IconSupplyChainESG({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="3" cy="10" r="2"/>
      <circle cx="10" cy="4" r="2"/>
      <circle cx="17" cy="10" r="2"/>
      <circle cx="10" cy="16" r="2"/>
      <path d="M5 10h3M12 10h3M10 6v2M10 14v-2"/>
      <path d="M8 6l-3 3M14 6l-1 2" opacity="0.5"/>
    </svg>
  );
}

function IconNoisePollution({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 7h3l4-4v14l-4-4H3V7z"/>
      <path d="M14 7a5 5 0 0 1 0 6" opacity="0.8"/>
      <path d="M16 5a8 8 0 0 1 0 10" opacity="0.5"/>
      <line x1="2" y1="18" x2="18" y2="2" stroke="currentColor" strokeWidth="1.3" opacity="0.4"/>
    </svg>
  );
}

function IconCryptoMining({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="7" width="16" height="7" rx="1"/>
      <path d="M5 7V5M9 7V5M13 7V5M17 7V5" opacity="0.6"/>
      <path d="M5 14v2M9 14v2M13 14v2M17 14v2" opacity="0.6"/>
      <path d="M2 14l3-3 3 2 5-4 5 2" opacity="0.5" strokeWidth="1"/>
    </svg>
  );
}

function IconMetaverse({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 7l8-4 8 4v6l-8 4-8-4V7z"/>
      <path d="M2 7l8 4 8-4"/>
      <path d="M10 11v6"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" stroke="none" opacity="0.4"/>
    </svg>
  );
}

function IconNuclearWaste({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="3"/>
      <path d="M10 7V4M8.5 8l-2.6-1.5M11.5 8l2.6-1.5"/>
      <path d="M10 13v3M8.5 12l-2.6 1.5M11.5 12l2.6 1.5"/>
      <circle cx="10" cy="10" r="7" opacity="0.2"/>
    </svg>
  );
}

function IconOceanPlastic({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 13c2-1 4 0 6-1s4-2 6-1"/>
      <path d="M2 16c2-1 4 0 6-1s4-2 6-1"/>
      <path d="M5 10l1-4h3l-1 4M10 10l2-4h3l-2 4" opacity="0.6"/>
      <circle cx="4" cy="8" r="1" fill="currentColor" stroke="none" opacity="0.5"/>
    </svg>
  );
}

function IconLandGrab({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="12" width="16" height="5" rx="1"/>
      <path d="M5 12V8l3-3 3 3v4"/>
      <path d="M14 9l3 1v2"/>
      <path d="M3 17l4-4" opacity="0.5"/>
      <path d="M13 9l-2-3" opacity="0.5"/>
    </svg>
  );
}

function IconWaterPrivatization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2c0 0-6 6-6 10a6 6 0 0 0 12 0c0-4-6-10-6-10z"/>
      <path d="M7 14l6-4" opacity="0.7"/>
      <circle cx="13" cy="8" r="2" stroke="currentColor" opacity="0.6"/>
      <path d="M12 7l2 2" opacity="0.5"/>
    </svg>
  );
}

function IconTaxHaven({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <path d="M10 3c0 0 4 2 4 7s-4 7-4 7"/>
      <path d="M10 3c0 0-4 2-4 7s4 7 4 7"/>
      <path d="M3 10h14"/>
      <path d="M7 5.5l6 9" opacity="0.5" strokeWidth="1.2"/>
    </svg>
  );
}

function IconAutonomousWeapons({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 9h10l2 2-2 2H3l-1-2z"/>
      <circle cx="16" cy="11" r="1.5" fill="currentColor" stroke="none" opacity="0.7"/>
      <path d="M7 9V7M10 9V6" opacity="0.6"/>
      <path d="M17 7l1-2M17 15l1 2" opacity="0.4"/>
    </svg>
  );
}

function IconSpaceWeather({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="5" cy="10" r="3"/>
      <path d="M8 10h3"/>
      <path d="M11 7l1-3M11 10l2-1M11 13l1 3" opacity="0.7"/>
      <path d="M14 5l2 1-1 2M14 13l2 1-1 2" opacity="0.4"/>
    </svg>
  );
}

function IconPlatformEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="7" y="2" width="6" height="4" rx="1"/>
      <path d="M10 6v3"/>
      <circle cx="4" cy="13" r="2"/>
      <circle cx="10" cy="13" r="2"/>
      <circle cx="16" cy="13" r="2"/>
      <path d="M6 13h2M12 13h2"/>
      <path d="M4 15v2M10 15v2M16 15v2" opacity="0.5"/>
    </svg>
  );
}

function IconSoilCarbon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 12h16"/>
      <path d="M5 12V8c0-2 2-4 5-4s5 2 5 4v4"/>
      <path d="M5 16h10" opacity="0.5"/>
      <path d="M7 12v2M10 12v3M13 12v2" opacity="0.7"/>
    </svg>
  );
}

function IconUrbanMining({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="8" width="14" height="9" rx="1"/>
      <path d="M6 8V5h8v3"/>
      <path d="M8 13l2-2 2 2"/>
      <path d="M10 11v4" opacity="0.7"/>
      <circle cx="10" cy="5" r="1" fill="currentColor" stroke="none" opacity="0.6"/>
    </svg>
  );
}

function IconPharmaceutical({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="6" y="3" width="8" height="14" rx="3"/>
      <line x1="6" y1="10" x2="14" y2="10"/>
      <path d="M9 6.5h2M9 13.5h2" opacity="0.6"/>
    </svg>
  );
}

function IconAlgaeEnergy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 17c2-3 1-7 5-9s7 0 7-4"/>
      <path d="M3 14c2-2 2-6 5-8" opacity="0.5"/>
      <path d="M10 17V13"/>
      <circle cx="10" cy="12" r="2" fill="currentColor" stroke="none" opacity="0.5"/>
    </svg>
  );
}

function IconCarbonBorder({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="8" width="16" height="9" rx="1"/>
      <path d="M2 12h16" opacity="0.5"/>
      <path d="M7 5l3-3 3 3"/>
      <path d="M10 2v6"/>
      <path d="M5 15l2-2M15 15l-2-2" opacity="0.5"/>
    </svg>
  );
}

function IconSocialBond({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 14l3-8 4 6 2-4 3 6"/>
      <path d="M2 17h16"/>
      <circle cx="5" cy="14" r="1.2" fill="currentColor" stroke="none"/>
      <circle cx="15" cy="14" r="1.2" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconDigitalDivide({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="5" width="7" height="10" rx="1"/>
      <path d="M13 9h5M13 12h3" opacity="0.4"/>
      <path d="M9 10h2"/>
      <circle cx="15" cy="6" r="2.5" fill="none" stroke="currentColor"/>
      <line x1="13.5" y1="13" x2="16.5" y2="16" strokeWidth="1.3"/>
    </svg>
  );
}

function IconNeuroRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3c-3 0-5 2-5 5 0 1.5.5 3 2 4l1 4h4l1-4c1.5-1 2-2.5 2-4 0-3-2-5-5-5z"/>
      <path d="M8 12h4" opacity="0.6"/>
      <path d="M6 8c1 0 2 1 4 1s3-1 4-1" opacity="0.5"/>
    </svg>
  );
}

function IconWildfire({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2c0 3-3 4-3 7a3 3 0 0 0 6 0c0-2-1-3-1-5"/>
      <path d="M7 13c-2 0-3 1-3 3h12c0-2-1-3-3-3"/>
      <path d="M8 8c0 2-1 3-1 4" opacity="0.5"/>
    </svg>
  );
}

function IconForcedLabor({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="8" cy="5" r="2.5"/>
      <path d="M3 17c0-3 2-5 5-5s5 2 5 5"/>
      <path d="M14 10l3-2M17 8v5M14 13l3-1" opacity="0.6"/>
      <circle cx="15" cy="8" r="1" fill="currentColor" stroke="none" opacity="0.5"/>
    </svg>
  );
}


function IconOceanGovernance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 12c3-2 5 0 8 0s5-2 8 0"/>
      <path d="M2 15c3-2 5 0 8 0s5-2 8 0"/>
      <path d="M5 8l5-5 5 5"/>
      <path d="M10 3v5"/>
    </svg>
  );
}

function IconCriticalInfraCyber({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l7 3v5c0 4-3 7-7 8C7 17 4 14 3 10V5l7-3z"/>
      <path d="M7 10l2 2 4-4" opacity="0.8"/>
      <path d="M13 6l1-2" opacity="0.4"/>
    </svg>
  );
}

function IconHousingCrisis({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 10l8-7 8 7"/>
      <path d="M4 10v7h12v-7"/>
      <path d="M8 17v-5h4v5"/>
      <path d="M16 8l2 2" opacity="0.5"/>
      <line x1="2" y1="18" x2="18" y2="2" stroke="currentColor" strokeWidth="1.2" opacity="0.4"/>
    </svg>
  );
}

function IconClimateMigration({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="6" cy="6" r="2.5"/>
      <path d="M2 17c0-3 2-5 4-5"/>
      <path d="M9 13l5-3 4 2"/>
      <path d="M9 13v4M14 10v4M18 12v3" opacity="0.6"/>
      <path d="M6 9v2" opacity="0.5"/>
    </svg>
  );
}

function IconCoralReef({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 17V11c0-2 1.5-4 3-4"/>
      <path d="M8 7V4"/>
      <path d="M8 7c0-2 2-3 4-2"/>
      <path d="M12 5v3c0 2 2 3 2 5v4"/>
      <path d="M2 17h16"/>
      <path d="M6 12c-1 0-2 1-2 2" opacity="0.5"/>
    </svg>
  );
}

function IconLithiumRecycling({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="4" y="5" width="12" height="11" rx="1"/>
      <path d="M8 5V3h4v2"/>
      <path d="M7 11l2-2 2 2 2-2" opacity="0.7"/>
      <path d="M10 9v5" opacity="0.5"/>
      <circle cx="10" cy="13" r="1.2" fill="currentColor" stroke="none" opacity="0.6"/>
    </svg>
  );
}

function IconMicroplastics({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="5" cy="8" r="1.5" fill="currentColor" stroke="none" opacity="0.5"/>
      <circle cx="10" cy="5" r="1" fill="currentColor" stroke="none" opacity="0.6"/>
      <circle cx="15" cy="9" r="1.5" fill="currentColor" stroke="none" opacity="0.5"/>
      <circle cx="7" cy="13" r="1" fill="currentColor" stroke="none" opacity="0.4"/>
      <circle cx="13" cy="14" r="1.5" fill="currentColor" stroke="none" opacity="0.5"/>
      <path d="M3 10c3 2 5 3 8 2s5-2 7 0" opacity="0.4"/>
      <path d="M4 16h12" opacity="0.3"/>
    </svg>
  );
}

function IconInsuranceClimate({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l7 3v5c0 4-3 7-7 8C7 17 4 14 3 10V5l7-3z"/>
      <path d="M7 10l2 2 4-4"/>
      <path d="M16 3l2 1M14 16l2 2" opacity="0.4"/>
    </svg>
  );
}

function IconAcademicIntegrity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="4" width="14" height="13" rx="1"/>
      <path d="M7 8h6M7 11h4"/>
      <path d="M13 14l2-2-2-2" opacity="0.6"/>
      <path d="M3 4l4-2h6l4 2" opacity="0.5"/>
    </svg>
  );
}

function IconUrbanFlooding({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 9l7-7 7 7"/>
      <path d="M5 9v4"/>
      <path d="M15 9v4"/>
      <path d="M2 14c2 1 4-1 6 0s4 1 6 0"/>
      <path d="M2 17c2 1 4-1 6 0s4 1 6 0"/>
    </svg>
  );
}

function IconDigitalNomad({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="7" width="10" height="7" rx="1"/>
      <path d="M3 10h10M7 7V5M9 7V5"/>
      <circle cx="15" cy="6" r="3"/>
      <path d="M13 10l4-1" opacity="0.5"/>
      <path d="M13 13l4 1" opacity="0.4"/>
    </svg>
  );
}

function IconGeneticPrivacy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M8 2c-1 3 0 5 2 6s3 4 2 7"/>
      <path d="M12 2c1 3 0 5-2 6s-3 4-2 7"/>
      <path d="M6 7h8M6 13h8" opacity="0.5"/>
      <path d="M16 4l1-2M16 16l1 2" opacity="0.3"/>
    </svg>
  );
}

function IconSovereignWealth({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <path d="M7 13V8l6 5V8" opacity="0.8"/>
      <path d="M3 10h2M15 10h2" opacity="0.4"/>
      <path d="M10 3v2M10 15v2" opacity="0.4"/>
    </svg>
  );
}

// ─── Wave 433-440 icons ──────────────────────────────────────────────────────

function IconPermafrostMethane({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 12c2-2 3-4 8-4s6 2 8 4"/>
      <path d="M2 15c2-2 3-3 8-3s6 1 8 3"/>
      <path d="M7 8V5M10 7V3M13 8V5"/>
      <path d="M7 5c0-1.1.9-2 2-2h2"/>
    </svg>
  );
}

function IconFoodWaste({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M5 9V6c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2v3"/>
      <path d="M3 9h14l-1 8H4z"/>
      <path d="M8 4V2M12 4V2"/>
      <path d="M8 13l1-2 2 2 1-2"/>
    </svg>
  );
}

function IconRareDisease({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="8" r="4"/>
      <path d="M10 4v2M10 10v2M7 7H5M15 7h-2"/>
      <path d="M7 13c-2 1-3 2-3 4h12c0-2-1-3-3-4"/>
      <path d="M13 8l2 2"/>
    </svg>
  );
}

function IconChildOnlineSafety({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="6" r="3"/>
      <path d="M4 17c0-3.3 2.7-6 6-6s6 2.7 6 6"/>
      <path d="M14 10l2 2-2 2M16 12h-3"/>
      <path d="M3 3l14 14" opacity="0.3"/>
    </svg>
  );
}

function IconPsychedelicMedicine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="4"/>
      <path d="M10 6V4M10 16v-2M6 10H4M16 10h-2"/>
      <path d="M7.5 7.5L6 6M14 14l-1.5-1.5M12.5 7.5L14 6M6 14l1.5-1.5"/>
      <circle cx="10" cy="10" r="1.5" fill="currentColor" stroke="none" opacity="0.6"/>
    </svg>
  );
}

function IconNuclearDisarmament({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <path d="M10 3v4M10 13v4M3 10h4M13 10h4"/>
      <path d="M5.5 5.5l2.8 2.8M11.7 11.7l2.8 2.8M14.5 5.5l-2.8 2.8M8.3 11.7L5.5 14.5"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" stroke="none" opacity="0.4"/>
    </svg>
  );
}

function IconUrbanAirMobility({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3l-2 4H5l3 3-1 4 3-2 3 2-1-4 3-3h-3z"/>
      <path d="M3 16h14"/>
      <path d="M6 10l-2 2M14 10l2 2"/>
    </svg>
  );
}

function IconMediaIntegrity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="4" width="16" height="11" rx="1"/>
      <path d="M8 15l-2 3h8l-2-3"/>
      <path d="M7 8h6M7 11h4"/>
      <path d="M14 7l2-2M16 5l-2 2" opacity="0.6"/>
    </svg>
  );
}

// ─── Wave 441-448 icons ──────────────────────────────────────────────────────

function IconPandemicPrep({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <path d="M10 6v4l3 2"/>
      <path d="M6 3l-2-1M14 3l2-1M3 14l-1 2M17 14l1 2"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" stroke="none" opacity="0.4"/>
    </svg>
  );
}

function IconGlobalTaxReform({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="7"/>
      <path d="M10 3c0 0-3 2-3 7s3 7 3 7M10 3c0 0 3 2 3 7s-3 7-3 7"/>
      <path d="M3 10h14"/>
      <path d="M10 7c-1 0-2 .5-2 1.5S9 10 10 10s2 .5 2 1.5S11 13 10 13"/>
      <path d="M10 6v1M10 13v1"/>
    </svg>
  );
}

function IconPrisonReform({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="4" width="14" height="13" rx="1"/>
      <path d="M7 4V2M10 4V2M13 4V2"/>
      <path d="M7 4v13M10 4v13M13 4v13"/>
      <path d="M3 9h14M3 13h14"/>
    </svg>
  );
}

function IconAMRResponse({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <ellipse cx="10" cy="10" rx="4" ry="2" transform="rotate(45 10 10)"/>
      <ellipse cx="10" cy="10" rx="4" ry="2" transform="rotate(-45 10 10)"/>
      <circle cx="10" cy="10" r="1.5" fill="currentColor" stroke="none"/>
      <path d="M5 5l-2-2M15 5l2-2M5 15l-2 2M15 15l2 2"/>
    </svg>
  );
}

function IconTranshumanistEthics({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="7" r="3"/>
      <path d="M7 10c-2 1-3 3-3 5h12c0-2-1-4-3-5"/>
      <path d="M13 4l2-2M7 4L5 2"/>
      <path d="M10 4v-2"/>
      <path d="M15 10l2-1M5 10L3 9"/>
    </svg>
  );
}

function IconVerticalFarming({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="4" y="2" width="12" height="16" rx="1"/>
      <path d="M4 6h12M4 10h12M4 14h12"/>
      <path d="M8 4v2M12 4v2M8 8v2M12 8v2M8 12v2M12 12v2"/>
      <circle cx="8" cy="4" r="0.5" fill="currentColor" stroke="none"/>
      <circle cx="12" cy="4" r="0.5" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconSocialMediaMentalHealth({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3c-3.9 0-7 3.1-7 7 0 2.7 1.5 5.1 3.8 6.3L10 18l3.2-1.7C15.5 15.1 17 12.7 17 10c0-3.9-3.1-7-7-7z"/>
      <path d="M7 9l3 3 3-5"/>
      <path d="M15 4l2-2M13 3l1-2" opacity="0.5"/>
    </svg>
  );
}

function IconCleanWaterAccess({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2c0 0-6 6-6 10a6 6 0 0 0 12 0C16 8 10 2 10 2z"/>
      <path d="M7 15c1-1 1.5-2 3-2s2 1 3 2"/>
      <path d="M10 10v3"/>
    </svg>
  );
}

// ─── Wave 449-456 icons ──────────────────────────────────────────────────────

function IconLandDegradation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 14h16"/>
      <path d="M3 14c1-3 2-5 4-6M9 14c0-2 1-4 2-5M14 14c1-2 2-3 3-4"/>
      <path d="M2 17h16" opacity="0.3"/>
      <path d="M6 8l1-3 2 1 1-3" opacity="0.6"/>
    </svg>
  );
}

function IconElderCare({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="6" r="3"/>
      <path d="M7 10c-2 1-3 3-3 5h12c0-2-1-4-3-5"/>
      <path d="M7 15l-1 2M13 15l1 2"/>
      <path d="M5 14l-2 1M15 14l2 1"/>
    </svg>
  );
}

function IconDarkPatterns({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="4" width="14" height="12" rx="1"/>
      <path d="M7 8h6M7 10h4"/>
      <path d="M14 13l2 2"/>
      <circle cx="14" cy="13" r="0.5" fill="currentColor" stroke="none"/>
      <path d="M9 13h-2v2h2v-2z" fill="currentColor" stroke="none" opacity="0.4"/>
    </svg>
  );
}

function IconBiopiracy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3c-2 3-2 5 0 7s2 4 0 7"/>
      <path d="M10 7c2-1 4-1 5 1M10 13c2 1 4 1 5-1"/>
      <path d="M15 8l2-1M15 12l2 1"/>
      <path d="M10 10h-4M6 10l-2-2M6 10l-2 2"/>
    </svg>
  );
}

function IconElectoralIntegrity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="5" width="14" height="11" rx="1"/>
      <path d="M7 9l2 2 4-4"/>
      <path d="M10 3v2"/>
      <path d="M15 3l1-1M5 3L4 2"/>
    </svg>
  );
}

function IconPlatformLabor({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="6" r="3"/>
      <path d="M5 17v-2a5 5 0 0 1 10 0v2"/>
      <path d="M3 11l4 2M17 11l-4 2"/>
      <path d="M7 13v4M13 13v4"/>
    </svg>
  );
}

function IconCryptoFinancialCrime({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l2 3h3l-2.5 2 1 3.5L10 9l-3.5 1.5 1-3.5L5 5h3z"/>
      <path d="M5 14l3 1 2-2 2 2 3-1"/>
      <path d="M3 17h14"/>
      <path d="M14 8l3-2"/>
    </svg>
  );
}

function IconArcticSovereigntyRace({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="10" cy="10" r="8"/>
      <path d="M10 2v4M10 14v4"/>
      <path d="M2 10h4M14 10h4"/>
      <path d="M5 5l2 2M13 5l-2 2M5 15l2-2M13 15l-2-2"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" stroke="none" opacity="0.5"/>
    </svg>
  );
}

// ─── Wave 457-464 icons ──────────────────────────────────────────────────────

function IconRefugeeIntegration({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="7" cy="6" r="2.5"/>
      <path d="M4 17v-2c0-2.2 1.8-4 4-4"/>
      <circle cx="14" cy="9" r="2"/>
      <path d="M11 17v-1.5c0-1.9 1.6-3.5 3.5-3.5S18 13.6 18 15.5V17"/>
      <path d="M9 11l3-2"/>
    </svg>
  );
}

function IconESGGreenwash({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3c-2 3-1 5 1 6s3 3 1 7"/>
      <path d="M7 6c-2 1-3 3-2 5"/>
      <path d="M13 6c2 1 3 3 2 5"/>
      <path d="M4 17h12"/>
      <path d="M14 4l2-2M16 2l-1 3"/>
    </svg>
  );
}

function IconTelemedicine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="4" width="12" height="9" rx="1"/>
      <path d="M14 8l4-2v6l-4-2"/>
      <path d="M7 7v4M5 9h4"/>
    </svg>
  );
}

function IconAIBias({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3c-4 0-7 3-7 7s3 7 7 7 7-3 7-7-3-7-7-7z"/>
      <path d="M6 10h4M13 10h1"/>
      <path d="M10 7v3M10 10l-3 3"/>
      <path d="M10 7c-1-1-2-1-2 0s1 2 2 2" opacity="0.5"/>
    </svg>
  );
}

function IconSupplyChainTransparency({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 6h4l2 3 2-3h4"/>
      <path d="M3 6v8h14V6"/>
      <path d="M7 9v5M13 9v5"/>
      <path d="M9 9h2"/>
      <circle cx="5" cy="6" r="1" fill="currentColor" stroke="none"/>
      <circle cx="15" cy="6" r="1" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconAntiMoneyLaunderingHumanRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  )
}

function IconSettlerColonialismLandRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 6.75V15m6-6v8.25m.503 3.498l4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 00-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0z" />
    </svg>
  )
}

function IconDrugTrafficking({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2l8 4v8l-8 4-8-4V6z"/>
      <path d="M10 2v16M2 6l8 4 8-4"/>
      <path d="M6 8l4 2 4-2" opacity="0.5"/>
    </svg>
  );
}

function IconFoodSystemSovereignty({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 2c0 0-6 5-6 9a6 6 0 0 0 12 0C16 7 10 2 10 2z"/>
      <path d="M10 8v5M7 10h6"/>
      <path d="M8 13c0 1 1 2 2 2s2-1 2-2"/>
    </svg>
  );
}

function IconDigitalHealthSovereignty({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10 3c-3.9 0-7 3.1-7 7 0 2.7 1.5 5.1 3.8 6.3L10 18l3.2-1.7C15.5 15.1 17 12.7 17 10c0-3.9-3.1-7-7-7z"/>
      <path d="M7 10h6M10 7v6"/>
      <path d="M13 7l2-2" opacity="0.5"/>
    </svg>
  );
}

function IconNPS({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
    </svg>
  );
}

function IconSEORanking({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
    </svg>
  );
}

function IconClientRetention({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" />
    </svg>
  );
}

function IconUpsellOpportunity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fillRule="evenodd" d="M3.293 9.707a1 1 0 010-1.414l6-6a1 1 0 011.414 0l6 6a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L4.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
    </svg>
  );
}

function IconSocialROI({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zm6-4a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zm6-3a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
    </svg>
  );
}

function IconAgentOrchestrator({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="3" r="1.5" />
      <circle cx="3" cy="10" r="1.5" />
      <circle cx="17" cy="10" r="1.5" />
      <circle cx="7" cy="17" r="1.5" />
      <circle cx="13" cy="17" r="1.5" />
      <path d="M10 4.5L3 8.5M10 4.5L17 8.5M3 11.5L7 15.5M17 11.5L13 15.5M10 4.5v3" stroke="currentColor" strokeWidth="1" fill="none"/>
    </svg>
  );
}

function IconHybridInfra({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <rect x="2" y="11" width="5" height="7" rx="1" fill="currentColor" stroke="none" opacity="0.6"/>
      <rect x="7.5" y="7" width="5" height="11" rx="1" fill="currentColor" stroke="none" opacity="0.8"/>
      <rect x="13" y="3" width="5" height="15" rx="1" fill="currentColor" stroke="none"/>
      <path d="M1 10 Q5 6 10 9 Q15 12 19 4" strokeWidth="1.5" strokeLinecap="round"/>
    </svg>
  );
}

function IconPolycrisis({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <circle cx="10" cy="10" r="8" strokeDasharray="3 2"/>
      <path d="M10 2 L10 18M2 10 L18 10" strokeLinecap="round" opacity="0.5"/>
      <circle cx="10" cy="10" r="3" fill="currentColor" opacity="0.8"/>
      <path d="M5 5 L15 15M15 5 L5 15" strokeLinecap="round" opacity="0.6"/>
    </svg>
  );
}

function IconBlackSwan({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <path d="M10 2 C6 2 3 5 3 8 C3 12 7 15 10 18 C13 15 17 12 17 8 C17 5 14 2 10 2Z" fill="currentColor" opacity="0.2"/>
      <path d="M10 5 C8 5 6 7 7 9 C8 11 10 12 10 14" strokeLinecap="round"/>
      <path d="M10 14 L10 17" strokeLinecap="round" strokeWidth="2"/>
      <circle cx="13" cy="6" r="1.5" fill="currentColor"/>
    </svg>
  );
}

function IconCaelumSynthesis({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <circle cx="10" cy="10" r="8" opacity="0.3"/>
      <circle cx="10" cy="10" r="5" opacity="0.5"/>
      <circle cx="10" cy="10" r="2.5" fill="currentColor" opacity="0.9"/>
      <path d="M10 2 L10 5M10 15 L10 18M2 10 L5 10M15 10 L18 10" strokeLinecap="round" opacity="0.6"/>
      <path d="M4.6 4.6 L6.8 6.8M13.2 13.2 L15.4 15.4M15.4 4.6 L13.2 6.8M6.8 13.2 L4.6 15.4" strokeLinecap="round" opacity="0.4"/>
    </svg>
  );
}

function IconAntifragility({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <path d="M10 16 L10 4" strokeLinecap="round"/>
      <path d="M10 4 L6 8" strokeLinecap="round"/>
      <path d="M10 4 L14 8" strokeLinecap="round"/>
      <path d="M6 16 L6 10" strokeLinecap="round" opacity="0.5"/>
      <path d="M6 10 L4 12" strokeLinecap="round" opacity="0.5"/>
      <path d="M6 10 L8 12" strokeLinecap="round" opacity="0.5"/>
      <path d="M14 16 L14 10" strokeLinecap="round" opacity="0.5"/>
      <path d="M14 10 L12 12" strokeLinecap="round" opacity="0.5"/>
      <path d="M14 10 L16 12" strokeLinecap="round" opacity="0.5"/>
    </svg>
  );
}

function IconCivDebt({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <circle cx="10" cy="10" r="8" opacity="0.3"/>
      <path d="M10 2 L10 10" strokeLinecap="round"/>
      <path d="M10 10 L14 13" strokeLinecap="round"/>
      <circle cx="10" cy="10" r="1.5" fill="currentColor" opacity="0.8"/>
      <path d="M4 10 L16 10" strokeLinecap="round" strokeDasharray="1.5 1.5" opacity="0.4"/>
      <path d="M5 6 L15 14M5 14 L15 6" strokeLinecap="round" opacity="0.2"/>
    </svg>
  );
}

function IconNexusCrisis({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <path d="M10 2 L14 8 L18 6 L14 14 L10 18 L6 14 L2 6 L6 8 Z" opacity="0.3" fill="currentColor"/>
      <circle cx="10" cy="10" r="2.5" fill="currentColor" opacity="0.9"/>
      <path d="M10 4 L10 7M10 13 L10 16M4 10 L7 10M13 10 L16 10" strokeLinecap="round"/>
    </svg>
  );
}

function IconDemocraticDecay({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <path d="M4 14 L4 6 L10 3 L16 6 L16 14 L10 17 Z" opacity="0.3"/>
      <path d="M4 14 L10 17 L16 14" strokeLinecap="round"/>
      <path d="M7 9 L9 11 L13 7" strokeLinecap="round" strokeLinejoin="round" opacity="0.6"/>
      <path d="M10 2 L10 5" strokeLinecap="round" strokeWidth="2" opacity="0.8"/>
      <line x1="7" y1="14" x2="13" y2="14" strokeLinecap="round" opacity="0.4"/>
    </svg>
  );
}

function IconEconomicCoercion({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <path d="M3 10 L10 3 L17 10" strokeLinecap="round" strokeLinejoin="round" opacity="0.5"/>
      <path d="M5 17 L5 10 L15 10 L15 17" strokeLinecap="round" strokeLinejoin="round" opacity="0.4"/>
      <path d="M3 17 L17 17" strokeLinecap="round"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" opacity="0.8"/>
      <path d="M8 6 L10 4 L12 6" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconSocialCohesion({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <circle cx="7" cy="8" r="2.5" fill="currentColor" opacity="0.6"/>
      <circle cx="13" cy="8" r="2.5" fill="currentColor" opacity="0.6"/>
      <circle cx="10" cy="13" r="2.5" fill="currentColor" opacity="0.8"/>
      <path d="M7 8 L10 13 L13 8" strokeLinecap="round" strokeLinejoin="round" opacity="0.5"/>
      <path d="M7 8 L13 8" strokeLinecap="round" opacity="0.4"/>
    </svg>
  );
}

function IconHybridWarfare({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <polygon points="10,2 12,8 18,8 13,12 15,18 10,14 5,18 7,12 2,8 8,8" opacity="0.5" fill="currentColor" strokeWidth="0.5"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" opacity="0.9" stroke="none"/>
      <path d="M10 2 L10 5" strokeLinecap="round" strokeWidth="1" opacity="0.8"/>
      <path d="M18 10 L15 10" strokeLinecap="round" strokeWidth="1" opacity="0.8"/>
      <path d="M2 10 L5 10" strokeLinecap="round" strokeWidth="1" opacity="0.8"/>
    </svg>
  );
}

function IconTrustEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <path d="M10 2 L12 7 L17 7 L13 10 L15 15 L10 12 L5 15 L7 10 L3 7 L8 7 Z" opacity="0.5"/>
      <circle cx="10" cy="10" r="2.5" fill="currentColor" opacity="0.8" stroke="none"/>
      <path d="M10 4 L10 7" strokeLinecap="round" opacity="0.6"/>
    </svg>
  );
}

function IconEpistemicSecurity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <circle cx="10" cy="10" r="7" opacity="0.3"/>
      <path d="M7 10 L9 12 L13 8" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M10 3 L10 6" strokeLinecap="round" opacity="0.7"/>
      <path d="M10 14 L10 17" strokeLinecap="round" opacity="0.7"/>
      <path d="M3 10 L6 10" strokeLinecap="round" opacity="0.7"/>
      <path d="M14 10 L17 10" strokeLinecap="round" opacity="0.7"/>
    </svg>
  );
}

function IconAttentionEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <circle cx="10" cy="10" r="3" fill="currentColor" opacity="0.8" stroke="none"/>
      <circle cx="10" cy="10" r="5.5" opacity="0.5"/>
      <circle cx="10" cy="10" r="8" opacity="0.25"/>
      <path d="M4 4 L7 7" strokeLinecap="round" opacity="0.6"/>
      <path d="M16 4 L13 7" strokeLinecap="round" opacity="0.6"/>
    </svg>
  );
}

function IconSovereignAIEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <circle cx="10" cy="10" r="7" opacity="0.3"/>
      <path d="M7 10 C7 7 13 7 13 10 C13 13 7 13 7 10" opacity="0.6"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" opacity="0.9" stroke="none"/>
      <path d="M10 3 L10 6" strokeLinecap="round"/>
      <path d="M10 14 L10 17" strokeLinecap="round"/>
      <path d="M3 10 L6 10" strokeLinecap="round"/>
      <path d="M14 10 L17 10" strokeLinecap="round"/>
    </svg>
  );
}

function IconNarrativeSovereignty({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <path d="M3 6 Q10 3 17 6 L17 14 Q10 17 3 14 Z" opacity="0.3" fill="currentColor"/>
      <path d="M7 9 L13 9" strokeLinecap="round"/>
      <path d="M7 12 L11 12" strokeLinecap="round" opacity="0.6"/>
      <circle cx="10" cy="5" r="1.5" fill="currentColor" opacity="0.8" stroke="none"/>
    </svg>
  );
}

function IconBioPower({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <circle cx="10" cy="10" r="6" opacity="0.3"/>
      <path d="M10 4 L10 7 M10 13 L10 16 M4 10 L7 10 M13 10 L16 10" strokeLinecap="round" opacity="0.6"/>
      <path d="M7 7 L13 13 M13 7 L7 13" strokeLinecap="round" opacity="0.4"/>
      <circle cx="10" cy="10" r="2" fill="currentColor" opacity="0.9" stroke="none"/>
    </svg>
  );
}

function IconComplexityHorizonEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <path d="M2 15 Q5 8 10 10 Q15 12 18 5" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M2 18 L18 18" strokeLinecap="round" opacity="0.4"/>
      <circle cx="10" cy="10" r="1.5" fill="currentColor" opacity="0.8" stroke="none"/>
      <path d="M10 10 L10 4" strokeLinecap="round" strokeDasharray="1 2" opacity="0.5"/>
    </svg>
  );
}

function IconLongevityInequalityEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <path d="M4 16 L4 6" strokeLinecap="round" opacity="0.4"/>
      <path d="M10 16 L10 10" strokeLinecap="round" opacity="0.6"/>
      <path d="M16 16 L16 4" strokeLinecap="round" opacity="0.8"/>
      <path d="M2 16 L18 16" strokeLinecap="round"/>
      <circle cx="4" cy="6" r="1.5" fill="currentColor" opacity="0.5" stroke="none"/>
      <circle cx="10" cy="10" r="1.5" fill="currentColor" opacity="0.7" stroke="none"/>
      <circle cx="16" cy="4" r="1.5" fill="currentColor" opacity="0.9" stroke="none"/>
    </svg>
  );
}

function IconTechnoDarwinism({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <path d="M3 16 L6 10 L10 13 L14 6 L17 4" strokeLinecap="round" strokeLinejoin="round"/>
      <circle cx="6" cy="10" r="1.5" fill="currentColor" opacity="0.6" stroke="none"/>
      <circle cx="14" cy="6" r="1.5" fill="currentColor" opacity="0.8" stroke="none"/>
      <circle cx="17" cy="4" r="2" fill="currentColor" opacity="1" stroke="none"/>
      <path d="M3 17 L17 17" strokeLinecap="round" opacity="0.3"/>
    </svg>
  );
}

function IconBiosafetyInfrastructure({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1 1 .965 2.656-.174 3.408A7.547 7.547 0 0112 21a7.547 7.547 0 01-9.026-1.29c-1.139-.752-1.174-2.408-.174-3.408L4.2 15.3" />
    </svg>
  );
}
function IconFamineWeaponization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}
function IconDiasporaGeopolitics({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
    </svg>
  );
}
function IconMaternalMortality({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12a3 3 0 100-6 3 3 0 000 6zm0 0v3m-3 3h6" />
    </svg>
  );
}
function IconSmallArmsProliferation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 7h12l2 2-2 2H3V7zm12 2h6M9 11v4m0 0H6m3 0h3" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 9l3-3m0 0l2-2m-2 2l2 2m-2-2h-3" />
    </svg>
  );
}
function IconDebtTrapDiplomacy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}
function IconYouthBulge({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}
function IconRareEarthDominance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3" />
    </svg>
  );
}
function IconPensionCrisis({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}
function IconElectoralInterference({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 7h18M3 12h18M3 17h18M9 3l3 4 3-4M9 21l3-4 3 4" />
      <circle cx="12" cy="12" r="2" fill="currentColor" />
    </svg>
  );
}
function IconUrbanHeatCrisis({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1M4.22 4.22l.707.707m13.86 13.86.707.707M1 12h2m18 0h2M4.22 19.78l.707-.707m13.86-13.86.707-.707M12 7a5 5 0 100 10 5 5 0 000-10z" />
    </svg>
  );
}
function IconCriminalStateCapture({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4" />
    </svg>
  );
}
function IconSpaceMilitarization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2L9 8H3l5 4-2 7 6-4 6 4-2-7 5-4h-6z" />
      <circle cx="19" cy="5" r="2" fill="currentColor" opacity="0.7" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 7l2-2" />
    </svg>
  );
}
function IconAlgorithmicSurveillance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <ellipse cx="12" cy="12" rx="10" ry="5" />
      <circle cx="12" cy="12" r="3" fill="currentColor" opacity="0.6" />
      <path strokeLinecap="round" d="M2 12h2M20 12h2M12 2v2M12 20v2" opacity="0.5" />
    </svg>
  );
}
function IconRefugeeWeaponization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <circle cx="7" cy="6" r="2.5" />
      <circle cx="14" cy="6" r="2.5" opacity="0.7" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M2 20c0-4 2.5-6 5-6h4c2.5 0 5 2 5 6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 9l4 4-4 4" opacity="0.7" />
    </svg>
  );
}
function IconWaterWars({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2C12 2 7 8 7 12a5 5 0 0010 0c0-4-5-10-5-10z" />
      <path d="M5 16c0 2.5 3 4 7 4s7-1.5 7-4" opacity="0.6" />
      <path d="M3 19c1-1 2.5-1.5 4-1" opacity="0.5" />
      <path d="M21 19c-1-1-2.5-1.5-4-1" opacity="0.5" />
    </svg>
  );
}

function IconQuantumRace({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="2" fill="currentColor" />
      <ellipse cx="12" cy="12" rx="10" ry="4" />
      <ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)" />
      <ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)" />
    </svg>
  );
}

function IconArcticGeopolitics({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="9" />
      <path d="M12 3v3M12 18v3M3 12h3M18 12h3" opacity="0.5" />
      <path d="M12 3l-2 4h4l-2-4z" fill="currentColor" opacity="0.7" />
      <path d="M9 9l1.5 3h3L12 9H9z" fill="currentColor" opacity="0.5" />
    </svg>
  );
}

function IconFoodWeaponization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2c0 0-1 3-1 5s1 3 1 3 1-1 1-3-1-5-1-5z" fill="currentColor" opacity="0.7" />
      <path d="M9 4c0 0-2 2-2 4s1 3 1 3" opacity="0.6" />
      <path d="M15 4c0 0 2 2 2 4s-1 3-1 3" opacity="0.6" />
      <path d="M12 10v12" />
      <path d="M8 14h8" opacity="0.5" />
      <path d="M9 17h6" opacity="0.4" />
    </svg>
  );
}

function IconAIWeaponsRace({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="7" y="8" width="10" height="8" rx="2" />
      <path d="M9 8V6a3 3 0 016 0v2" />
      <circle cx="10" cy="12" r="1" fill="currentColor" />
      <circle cx="14" cy="12" r="1" fill="currentColor" />
      <path d="M5 12H7M17 12H19" opacity="0.6" />
      <path d="M12 16v3M10 19h4" opacity="0.5" />
    </svg>
  );
}

function IconPortLogisticsCapture({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2v6" />
      <path d="M8 8h8" />
      <path d="M5 8l-2 8h18l-2-8" />
      <path d="M3 16c0 2 2 4 9 4s9-2 9-4" opacity="0.6" />
      <circle cx="12" cy="4" r="1.5" fill="currentColor" opacity="0.7" />
      <path d="M9 12h6" opacity="0.5" />
    </svg>
  );
}

function IconResourceCurse({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2v4m0 0c-2.5 0-4.5 1.5-4.5 4 0 1.5.5 2.5 1.5 3.5L12 16l3-2.5c1-1 1.5-2 1.5-3.5 0-2.5-2-4-4.5-4zm0 14v4M8 20h8" />
      <circle cx="12" cy="6" r="1.5" fill="currentColor" />
    </svg>
  );
}

function IconShadowEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="12" cy="12" r="9" />
      <path strokeLinecap="round" d="M12 3a9 9 0 0 1 0 18" fill="currentColor" fillOpacity="0.3" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6M12 9v6" />
    </svg>
  );
}

function IconAIAlignmentRisk({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2L2 20h20L12 2zm0 6v5m0 3v1" />
      <circle cx="12" cy="18" r="0.5" fill="currentColor" />
    </svg>
  );
}

function IconTreatyErosion({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 3v6h-6" />
    </svg>
  );
}
function IconLinguisticSovereignty({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
    </svg>
  );
}
function IconPowerVacuum({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <circle cx="12" cy="12" r="3" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2v3M12 19v3M2 12h3M19 12h3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12" />
    </svg>
  );
}
function IconSeedSovereignty({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 22V12m0 0c0-4.4-3.6-8-8-8 0 4.4 3.6 8 8 8zm0 0c0-4.4 3.6-8 8-8 0 4.4-3.6 8-8 8z" />
    </svg>
  );
}
function IconFinancialContagion({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
    </svg>
  );
}

function IconDiasporaWeaponizationEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="8" cy="4" r="1.5" fill="currentColor" opacity="0.9" />
      <circle cx="2.5" cy="12" r="1.5" fill="currentColor" opacity="0.9" />
      <circle cx="13.5" cy="12" r="1.5" fill="currentColor" opacity="0.9" />
      <line x1="8" y1="5.5" x2="2.5" y2="10.5" opacity="0.7" />
      <line x1="8" y1="5.5" x2="13.5" y2="10.5" opacity="0.7" />
      <line x1="2.5" y1="12" x2="13.5" y2="12" opacity="0.5" />
    </svg>
  );
}

function IconSportwashingGeopoliticsEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 12h8" opacity="0.7" />
      <path d="M5 12V8c0-1.7 1.3-3 3-3s3 1.3 3 3v4" opacity="0.8" />
      <path d="M6 5.5L8 2l2 3.5" fill="currentColor" fillOpacity="0.6" opacity="0.9" />
      <line x1="8" y1="2" x2="8" y2="3.5" strokeWidth="1" />
      <path d="M3 12h10" strokeWidth="2" opacity="0.5" />
    </svg>
  );
}

function IconDeepSeaMiningEngine({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="8" y1="1" x2="8" y2="5" />
      <path d="M5 5h6" />
      <path d="M5 5c0 2-2 3-2 5h10c0-2-2-3-2-5" opacity="0.8" />
      <path d="M6 15h4" opacity="0.6" />
      <line x1="8" y1="10" x2="8" y2="15" opacity="0.7" />
    </svg>
  );
}

function IconMercenaryWarfare({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="8" y1="2" x2="8" y2="12" />
      <path d="M5 5l3-3 3 3" fill="currentColor" fillOpacity="0.4" />
      <path d="M4 7l4 1 4-1" opacity="0.7" />
      <path d="M6 12l-2 2" opacity="0.8" />
      <path d="M10 12l2 2" opacity="0.8" />
      <path d="M6 12h4" opacity="0.6" />
      <path d="M3 4l2 1M13 4l-2 1" opacity="0.5" strokeWidth="1" />
    </svg>
  );
}

function IconNuclearDeterrence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="8" cy="8" r="2" fill="currentColor" fillOpacity="0.5" />
      <path d="M8 2a6 6 0 0 1 6 6" opacity="0.8" />
      <path d="M8 2a6 6 0 0 0-6 6" opacity="0.8" />
      <path d="M2 8a6 6 0 0 0 6 6" opacity="0.8" />
      <path d="M14 8a6 6 0 0 1-6 6" opacity="0.8" />
      <line x1="8" y1="1" x2="8" y2="3" strokeWidth="2" opacity="0.9" />
      <line x1="15" y1="8" x2="13" y2="8" strokeWidth="2" opacity="0.9" />
      <line x1="1" y1="8" x2="3" y2="8" strokeWidth="2" opacity="0.9" />
      <line x1="8" y1="15" x2="8" y2="13" strokeWidth="2" opacity="0.9" />
    </svg>
  );
}

function IconSanctionsEvasion({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="8" cy="8" r="5.5" opacity="0.6" />
      <path d="M8 5v1.5" opacity="0.9" />
      <path d="M6 6.5c0-.8.9-1.5 2-1.5s2 .7 2 1.5c0 .7-.5 1.2-1.2 1.4L8 8" opacity="0.8" />
      <circle cx="8" cy="9.5" r="0.5" fill="currentColor" />
      <path d="M11 3L13 1M13 3L11 1" opacity="0.7" strokeWidth="1.2" />
    </svg>
  );
}

function IconPandemicBioweapons({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="8" cy="8" r="2.5" fill="currentColor" fillOpacity="0.4" />
      <path d="M8 1.5a6.5 6.5 0 0 1 5.63 9.75" opacity="0.8" />
      <path d="M8 1.5a6.5 6.5 0 0 0-5.63 9.75" opacity="0.8" />
      <path d="M2.37 11.25a6.5 6.5 0 0 0 11.26 0" opacity="0.8" />
      <circle cx="8" cy="1.5" r="1" fill="currentColor" opacity="0.7" />
      <circle cx="2.37" cy="11.25" r="1" fill="currentColor" opacity="0.7" />
      <circle cx="13.63" cy="11.25" r="1" fill="currentColor" opacity="0.7" />
    </svg>
  );
}

function IconSemiconductorWar({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="4" y="4" width="8" height="8" rx="1" opacity="0.8" />
      <path d="M6 4V2M8 4V2M10 4V2" opacity="0.7" />
      <path d="M6 14v-2M8 14v-2M10 14v-2" opacity="0.7" />
      <path d="M4 6H2M4 8H2M4 10H2" opacity="0.7" />
      <path d="M14 6h-2M14 8h-2M14 10h-2" opacity="0.7" />
      <circle cx="8" cy="8" r="1.5" fill="currentColor" opacity="0.9" />
    </svg>
  );
}

function IconCurrencyWar({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="8" cy="8" r="5.5" opacity="0.7" />
      <path d="M8 4v8M6 5.5h3a1.5 1.5 0 0 1 0 3H6" opacity="0.9" />
      <path d="M6 8.5h3.5" opacity="0.8" />
    </svg>
  );
}

function IconUnderseaCable({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 4c2 0 3 1 4 2s2 2 4 2 3-1 3-2" opacity="0.8" />
      <path d="M2 8c2 0 3 1 4 2s2 2 4 2 3-1 3-2" opacity="0.9" />
      <circle cx="2" cy="4" r="1" fill="currentColor" opacity="0.7" />
      <circle cx="14" cy="4" r="1" fill="currentColor" opacity="0.7" />
      <path d="M8 12v2M7 14h2" opacity="0.6" />
    </svg>
  );
}

function IconWarCrimes({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M14.5 9.5L4 20" /><path d="M9 4l11 11" /><path d="M4 9l5-5 2 2-5 5z" /><path d="M15 20l5-5-2-2-5 5z" />
    </svg>
  );
}


function IconRefugeeRefoulement({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="9" cy="6" r="2" /><path d="M6 20v-6l-2-2 2-4h6l2 4-2 2v6" /><path d="M18 8l3 3-3 3" /><path d="M21 11H15" />
    </svg>
  );
}

function IconProxyWarfare({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
    </svg>
  );
}

function IconTransnationalRepression({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/><path d="M4.93 4.93l14.14 14.14"/>
    </svg>
  );
}

function IconNuclearBlackmail({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <circle cx="12" cy="12" r="3"/><path d="M12 2v3"/><path d="M12 19v3"/><path d="M4.22 4.22l2.12 2.12"/><path d="M17.66 17.66l2.12 2.12"/><path d="M2 12h3"/><path d="M19 12h3"/><path d="M4.22 19.78l2.12-2.12"/><path d="M17.66 6.34l2.12-2.12"/>
    </svg>
  );
}

function IconForcedDisappearance({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <circle cx="12" cy="7" r="3"/><path d="M6 20v-2a4 4 0 0 1 4-4h4"/><path d="M16 14l4 4"/><path d="M20 14l-4 4"/>
    </svg>
  );
}

function IconCulturalProperty({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/><line x1="2" y1="2" x2="22" y2="22"/>
    </svg>
  );
}

function IconPsychologicalWarfare({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/><circle cx="12" cy="12" r="10"/><path d="M2 2l20 20"/>
    </svg>
  );
}

function IconEnvironmentalRacism({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M12 8v4"/><path d="M12 16h.01"/>
    </svg>
  );
}

function IconWaterWeaponization({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10"/><path d="M12 6v6l4 2"/><line x1="18" y1="6" x2="22" y2="2"/><line x1="22" y1="6" x2="18" y2="2"/>
    </svg>
  );
}

function IconJournalistMurder({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="15" x2="15" y2="15"/><line x1="9" y1="11" x2="12" y2="11"/><line x1="14" y1="11" x2="14.01" y2="11"/>
    </svg>
  );
}
function IconPrisonTorture({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <rect x="3" y="3" width="18" height="18" rx="2"/>
      <path d="M8 7h8M8 12h8M8 17h8"/>
      <path d="M3 9h2M3 12h2M3 15h2"/>
    </svg>
  );
}
function IconCasteDiscrimination({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 2L8 8H4l3.5 3-1.5 5L12 13l6 3-1.5-5L20 8h-4L12 2z"/>
      <path d="M7 21h10"/>
      <path d="M12 13v8"/>
    </svg>
  );
}

function IconSexualViolenceWartime({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2L8 6v6l4 4 4-4V6L12 2z"/>
      <path d="M8 6L4 8v4l4 2"/>
      <path d="M16 6l4 2v4l-4 2"/>
      <path d="M9 14l-2 6M15 14l2 6"/>
      <line x1="8" y1="20" x2="16" y2="20" strokeWidth="1" opacity="0.5"/>
    </svg>
  );
}

function IconPoliceBrutality({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 17l-6.2 4.3 2.4-7.4L2 9.4h7.6L12 2z"/>
      <line x1="6" y1="6" x2="18" y2="18" strokeWidth="2" opacity="0.8"/>
      <line x1="18" y1="6" x2="6" y2="18" strokeWidth="2" opacity="0.8"/>
    </svg>
  );
}


function IconHateCrime({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
      <line x1="12" y1="9" x2="12" y2="13"/>
      <line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
  );
}

function IconChildLabor({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="5" r="2.5"/>
      <path d="M12 8v5"/>
      <path d="M9 11l3 2 3-2"/>
      <path d="M8 20l4-7 4 7"/>
      <path d="M6 14l2-2M18 14l-2-2"/>
      <line x1="4" y1="17" x2="7" y2="17" strokeWidth="1.5"/>
      <line x1="17" y1="17" x2="20" y2="17" strokeWidth="1.5"/>
    </svg>
  );
}

function IconIndigenousLandRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2v10"/>
      <path d="M7 6l5-4 5 4"/>
      <path d="M5 10l7-4 7 4"/>
      <path d="M9 10c0 3-2 5-4 6M15 10c0 3 2 5 4 6"/>
      <path d="M6 20h12"/>
      <path d="M8 16c1.5 1 5.5 2.5 8 0"/>
    </svg>
  );
}

function IconForcedLaborRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} aria-hidden="true">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      <line x1={12} y1={8} x2={12} y2={12}/><line x1={12} y1={16} x2={12.01} y2={16}/>
    </svg>
  );
}

function IconLGBTQRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} aria-hidden="true">
      <circle cx={12} cy={12} r={10}/>
      <path d="M8 12l4-4 4 4M12 8v8"/>
    </svg>
  );
}

function IconDebtBondage({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="8" cy="5" r="2"/>
      <path d="M8 7v4"/>
      <path d="M6 11h4"/>
      <path d="M8 11v6"/>
      <path d="M5 17h6"/>
      <rect x="13" y="9" width="5" height="7" rx="1"/>
      <path d="M15 9V7a1 1 0 0 1 1-1v0a1 1 0 0 1 1 1v2"/>
      <circle cx="15.5" cy="13" r="0.8" fill="currentColor" stroke="none"/>
    </svg>
  );
}

function IconArmsEmbargoViolation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 12h8l2-3h5l1 3"/>
      <path d="M16 9l1-4h2"/>
      <circle cx="7" cy="15" r="1.5"/>
      <circle cx="17" cy="15" r="1.5"/>
      <line x1="4" y1="4" x2="20" y2="20" strokeWidth="1.5" opacity="0.6"/>
    </svg>
  );
}

function IconMinorityRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="7" cy="5" r="2"/>
      <circle cx="17" cy="5" r="2"/>
      <circle cx="12" cy="4" r="2"/>
      <path d="M5 11c0-1.7 1-3 2-3s2 1.3 2 3v6"/>
      <path d="M15 11c0-1.7 1-3 2-3s2 1.3 2 3v6"/>
      <path d="M10 10c0-1.7 1-3 2-3s2 1.3 2 3v7"/>
      <path d="M10 17h4M5 17h4M15 17h4"/>
      <path d="M12 14l1.5 1.5" opacity="0.5"/>
    </svg>
  );
}

function IconLgbtqRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 21C12 21 4 15 4 9a8 8 0 0 1 16 0c0 6-8 12-8 12z"/>
      <circle cx="12" cy="9" r="2.5"/>
    </svg>
  );
}

function IconRightToEducation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2 7l10-5 10 5-10 5z"/>
      <path d="M6 9.5V17c0 0 2 2 6 2s6-2 6-2V9.5"/>
      <path d="M22 7v6"/>
    </svg>
  );
}

function IconMigrantWorkerRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="9" cy="6" r="2.5"/>
      <path d="M4 20v-2a5 5 0 0 1 10 0v2"/>
      <rect x="15" y="10" width="6" height="5" rx="1"/>
      <path d="M17 10V8a2 2 0 0 1 2-2v0a2 2 0 0 1 2 2v2"/>
      <path d="M15 15l-1 4M21 15l1 4"/>
    </svg>
  );
}

// ─── Wave 196 Icons (missing) ────────────────────────────────────────────────

function IconToxicWasteEnvironmentalHealth({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}

function IconGigWorkersPlatformEconomy({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3" />
    </svg>
  );
}

function IconRefugeeAsylumRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
    </svg>
  );
}

function IconCorporateTaxEvasion({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
    </svg>
  );
}

function IconMentalHealthWorkplace({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.032-4.5-4.5-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.782 3.75 3.75 5.765 3.75 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
    </svg>
  );
}

function IconMediaCensorshipPress({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 01-2.25 2.25M16.5 7.5V18a2.25 2.25 0 002.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 002.25 2.25h13.5M6 7.5h3v3H6V7.5z" />
    </svg>
  );
}

function IconFastFashionTextile({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
    </svg>
  );
}

function IconElderlyCarePRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
    </svg>
  );
}

function IconGeneticDataPrivacy({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
    </svg>
  );
}

function IconSportsLaborMegaEvents({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 013 3h-15a3 3 0 013-3m9 0v-3.375c0-.621-.503-1.125-1.125-1.125h-.871M7.5 18.75v-3.375c0-.621.504-1.125 1.125-1.125h.872m5.007 0H9.497m5.007 0a7.454 7.454 0 01-.982-3.172M9.497 14.25a7.454 7.454 0 00.981-3.172M5.25 4.236c-.982.143-1.954.317-2.916.52A6.003 6.003 0 007.73 9.728M5.25 4.236V4.5c0 2.108.966 3.99 2.48 5.228M5.25 4.236V2.721C7.456 2.41 9.71 2.25 12 2.25c2.291 0 4.545.16 6.75.47v1.516M7.73 9.728a6.726 6.726 0 002.748 1.35m8.272-6.842V4.5c0 2.108-.966 3.99-2.48 5.228m2.48-5.492a46.32 46.32 0 012.916.52 6.003 6.003 0 01-5.395 4.972m0 0a6.726 6.726 0 01-2.749 1.35m0 0a6.772 6.772 0 01-3.044 0" />
    </svg>
  );
}

function IconPharmaAccessPatents({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
    </svg>
  );
}

function IconOceanFishingRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12.75 3.03v.568c0 .334.148.65.405.864l1.068.89c.442.369.535 1.01.216 1.49l-.51.766a2.25 2.25 0 01-1.161.886l-.143.048a1.107 1.107 0 00-.57 1.664c.369.555.169 1.307-.427 1.605L9 13.125l.423 1.059a.956.956 0 01-1.652.928l-.679-.906a1.125 1.125 0 00-1.906.172L4.5 15.75l-.612.153M12.75 3.031a9 9 0 00-8.862 12.872M12.75 3.031a9 9 0 016.69 14.036m0 0l-.177-.529A2.249 2.249 0 0017.128 15H16.5l-.324-.324a1.453 1.453 0 00-2.328.377l-.036.073a1.586 1.586 0 01-.982.816l-.99.282c-.55.157-.894.702-.8 1.267l.073.438c.08.474.49.821.97.821.846 0 1.598.542 1.865 1.345l.215.643" />
    </svg>
  );
}

function IconLandGrabbingAgribusiness({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 6.75V15m6-6v8.25m.503 3.498l4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 00-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0z" />
    </svg>
  );
}

function IconCryptoEnergyRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
    </svg>
  );
}

function IconColonialReparations({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
    </svg>
  );
}

function IconAIAlgorithmicBias({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 002.25-2.25V6.75a2.25 2.25 0 00-2.25-2.25H6.75A2.25 2.25 0 004.5 6.75v10.5a2.25 2.25 0 002.25 2.25zm.75-12h9v9h-9v-9z" />
    </svg>
  );
}

function IconConflictMineralsDRC({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
    </svg>
  );
}

function IconHumanTraffickingSlavery({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 10.5V6.75a4.5 4.5 0 119 0v3.75M3.75 21.75h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H3.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
    </svg>
  );
}

function IconWaterPollutionLiability({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c-4.97 0-9 3.582-9 8 0 4.418 4.03 8 9 8s9-3.582 9-8c0-4.418-4.03-8-9-8zM6.75 12.75c0 1.864 2.349 3.75 5.25 3.75s5.25-1.886 5.25-3.75M12 3v18" />
    </svg>
  );
}

function IconNuclearEnergyRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
    </svg>
  );
}

function IconEWasteRecycling({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 17.25v1.007a3 3 0 01-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0115 18.257V17.25m6-12V15a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 15V5.25m18 0A2.25 2.25 0 0018.75 3H5.25A2.25 2.25 0 003 5.25m18 0H3" />
    </svg>
  );
}

function IconDebtBondageMigrant({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}

function IconDeforestationPalmOil({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v18m0-18C8.686 3 6 6.686 6 11c0 2.21.895 4.21 2.343 5.657M12 3c3.314 0 6 3.686 6 8 0 2.21-.895 4.21-2.343 5.657M8.343 16.657C9.79 18.105 10.895 19 12 21m0 0c1.105-2 2.21-2.895 3.657-4.343" />
    </svg>
  );
}

function IconChildSoldiersArmed({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
    </svg>
  );
}

function IconSeedPatentsSovereignty({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
    </svg>
  );
}

function IconSpaceMiningRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15a4.5 4.5 0 004.5 4.5H18a3.75 3.75 0 001.332-7.257 3 3 0 00-3.758-3.848 5.25 5.25 0 00-10.233 2.33A4.502 4.502 0 002.25 15z" />
    </svg>
  );
}
function IconSurveillanceCapitalism({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" /><path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}
function IconMentalHealthSocialMedia({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
    </svg>
  );
}

function IconLithiumBatteryRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 10.5h.375c.621 0 1.125.504 1.125 1.125v2.25c0 .621-.504 1.125-1.125 1.125H21M3.75 18h15A2.25 2.25 0 0021 15.75v-6a2.25 2.25 0 00-2.25-2.25h-15A2.25 2.25 0 001.5 9.75v6A2.25 2.25 0 003.75 18z" />
    </svg>
  );
}
function IconDarkPatternsConsumer({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}
function IconLandRightsClimate({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
    </svg>
  );
}

function IconAgriculturalPesticides({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
    </svg>
  );
}
function IconHomelessnessHousing({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
    </svg>
  );
}
function IconWaterPrivatisation({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
    </svg>
  );
}

// ─── Nav structure ───────────────────────────────────────────────────────────

type NavItem = {
  href: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  exact?: boolean;
  badge?: number;
};

type NavSection = {
  title: string;
  items: NavItem[];
};

function IconLawfare() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v18M3 9l9-6 9 6M6 12l6-3 6 3M6 18H3l3-6 3 6H6zM18 18h-3l3-6 3 6h-3z" />
    </svg>
  );
}

function IconAISurveillance() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 3l1 2M15 3l-1 2M3 9l2 1M21 9l-2 1" />
    </svg>
  );
}

function IconTransnationalCrime() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2a2 2 0 100 4 2 2 0 000-4zM4 18a2 2 0 100 4 2 2 0 000-4zM20 18a2 2 0 100 4 2 2 0 000-4zM12 4L4 18M12 4l8 14M4 18h16" />
    </svg>
  );
}

function IconSpaceWarfare() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <circle cx="12" cy="12" r="3" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M2 12h4M18 12h4M12 2v4M12 18v4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 6l2.5 2.5M15.5 15.5L18 18M18 6l-2.5 2.5M8.5 15.5L6 18" />
    </svg>
  );
}

function IconFoodSecurity() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2v20M8 6c0 0 0 4 4 4s4-4 4-4M8 10c0 0-4 0-4 4h16c0-4-4-4-4-4M4 18h16" />
    </svg>
  );
}

function IconClimateGeopolitics() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9 9 0 100-18 9 9 0 000 18z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.6 9h16.8M3.6 15h16.8" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c-2.4 3-3 6-3 9s.6 6 3 9M12 3c2.4 3 3 6 3 9s-.6 6-3 9" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 7l2-2-2-2" />
    </svg>
  );
}

function IconGenderApartheid() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <circle cx="12" cy="8" r="4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12v8M9 17h6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 4l16 16" />
    </svg>
  );
}

function IconMaritimePiracy() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2M12 5a4 4 0 014 4H8a4 4 0 014-4zM8 9v1a9 9 0 008 0V9M12 19v2M5 12H3M21 12h-2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M7 19c1.333-2 2.667-3 5-3s3.667 1 5 3" />
    </svg>
  );
}
function IconChildSoldiers({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
    </svg>
  );
}
function IconCulturalGenocide({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253" />
    </svg>
  );
}
function IconStateTerrorism({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}
function IconEcocide({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3C8.5 3 5 6 5 10c0 2.5 1.5 4.5 3.5 5.5L7 21h10l-1.5-5.5C17.5 14.5 19 12.5 19 10c0-4-3.5-7-7-7z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v18M9 8c0 0 1.5 2 3 2s3-2 3-2" />
    </svg>
  );
}
function IconForcedSterilization({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
      <line x1="4" y1="4" x2="20" y2="20" strokeLinecap="round" />
    </svg>
  );
}
function IconPoliticalAssassination({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="12" cy="12" r="9" />
      <line x1="12" y1="3" x2="12" y2="21" strokeLinecap="round" />
      <line x1="3" y1="12" x2="21" y2="12" strokeLinecap="round" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  );
}
function IconDroneWarfare({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="12" cy="12" r="2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 10V7m0 10v-3M10 12H7m10 0h-3" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M7 7l-2-2m12 2l2-2M7 17l-2 2m12-2l2 2" />
      <circle cx="12" cy="12" r="7" strokeDasharray="3 2" />
    </svg>
  );
}
function IconEthnicCleansing({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 8a5 5 0 11-10 0 5 5 0 0110 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 20c0-3.314 4.03-6 9-6s9 2.686 9 6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 10l3 3-3 3" />
      <line x1="22" y1="13" x2="15" y2="13" strokeLinecap="round" />
    </svg>
  );
}
function IconReligiousPersecution({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <line x1="12" y1="3" x2="12" y2="10" strokeLinecap="round" />
      <line x1="9" y1="5.5" x2="15" y2="5.5" strokeLinecap="round" />
      <circle cx="12" cy="17" r="4" />
      <line x1="9.17" y1="14.17" x2="14.83" y2="19.83" strokeLinecap="round" />
      <line x1="14.83" y1="14.17" x2="9.17" y2="19.83" strokeLinecap="round" />
    </svg>
  );
}


function IconAntipersonnelMines({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="12" cy="14" r="5" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9V6M12 6l-2-2M12 6l2-2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 11.5L5 9M16.5 11.5L19 9" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 19l-2 2M15 19l2 2M12 19v2" />
    </svg>
  );
}

function IconFemicide({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="12" cy="8" r="4" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12v8M9 17h6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 5l3-3M17 5h3M17 5v3" />
    </svg>
  );
}

function IconPressFreedom({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3Z" />
    </svg>
  );
}

function IconRightToHealth({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v6m-3-3h6" />
    </svg>
  );
}

function IconDomesticViolence({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z" />
    </svg>
  );
}


function IconHousingRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 12L12 3l9 9" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 10v9a1 1 0 0 0 1 1h4v-5h4v5h4a1 1 0 0 0 1-1v-9" />
    </svg>
  );
}

function IconFoodSecurityRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z"/>
      <path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1={9} y1={9} x2={9.01} y2={9}/>
      <line x1={15} y1={9} x2={15.01} y2={9}/>
    </svg>
  );
}
function IconClimateRefugeeRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path d="M12 2C8 8 4 12 4 15a8 8 0 0 0 16 0c0-3-4-7-8-13z"/>
      <path d="M9 17c0-1.5 1.5-3 3-3s3 1.5 3 3"/>
    </svg>
  );
}

function IconSocialProtection({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2.25c-4.5 3-9 3.75-9 3.75S3 18 12 21.75C21 18 21 6 21 6s-4.5-.75-9-3.75Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.5c0 1.657 1.343 3 3 3s3-1.343 3-3S13.657 9.5 12 9.5a3 3 0 0 0-3 3Z" />
    </svg>
  );
}

// ─── Wave 38 icons ───────────────────────────────────────────────────────────

function IconRacialJustice({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2M12 3l-4 4h8l-4-4Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 7H4l-1 5h6l-1-5ZM16 7h4l1 5h-6l1-5Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 12c0 2.21 1.79 4 4 4s4-1.79 4-4M12 12c0 2.21 1.79 4 4 4s4-1.79 4-4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 21h6M12 19v2" />
    </svg>
  );
}

function IconDigitalRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <rect x="2" y="4" width="16" height="12" rx="2" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M10 16v2M6 18h8" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M16 8.5V7a2 2 0 1 1 4 0v1.5" />
      <rect x="15" y="8.5" width="6" height="4.5" rx="1" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="18" cy="10.75" r="0.75" fill="currentColor" stroke="none" />
    </svg>
  );
}

function IconClimateJustice({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2C8 2 5 5.5 5 9c0 2.8 1.6 5.2 4 6.5V17h6v-1.5c2.4-1.3 4-3.7 4-6.5 0-3.5-3-7-7-7Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 17v2a3 3 0 0 0 6 0v-2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M14 7c0 1.1-.9 2-2 2s-2-.9-2-2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v4" />
    </svg>
  );
}

// ─── Wave 39 icons ───────────────────────────────────────────────────────────

function IconEconomicRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="12" cy="12" r="9" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 7v1.5M12 15.5V17" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.5 14.5c0 1.1.9 2 2.5 2s2.5-.9 2.5-2-1-1.8-2.5-2-2.5-.9-2.5-2 .9-2 2.5-2 2.5.9 2.5 2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M16 8l2-2M16 8h2M16 8v2" />
    </svg>
  );
}

function IconChildRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="12" cy="6" r="3" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 21v-4a4 4 0 0 1 8 0v4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 11v4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 4l1.5-1.5M18 4h2M18 4v2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 6.5a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z" />
    </svg>
  );
}

function IconRefugeeRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l9-9 9 9" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 10v9a1 1 0 0 0 1 1h4v-5h4v5h4a1 1 0 0 0 1-1v-9" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 13a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 8l2-3" />
    </svg>
  );
}

function IconAntiTorture({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3C8.5 3 6 5.5 6 9c0 2.5 1.5 4.5 3.5 5.5V18h5v-3.5C16.5 13.5 18 11.5 18 9c0-3.5-2.5-6-6-6Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.5 18h5M10 21h4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 6l2 2M20 6l-2 2" />
    </svg>
  );
}


function IconElectoralRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 11l3 3 5-5" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 7h8" />
    </svg>
  );
}

function IconDeathPenalty({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3a2 2 0 0 0-2 2v6H7l-2 3h14l-2-3h-3V5a2 2 0 0 0-2-2Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 20h6M12 14v6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 8H4M20 8h-2" />
    </svg>
  );
}


function IconCorporateAccountability({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 21h18M3 10h18M5 6l7-3 7 3" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M7 21V10M17 21V10M12 21V10" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M10 14h4M10 17h4" />
    </svg>
  );
}

function IconRightToPrivacy({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2L4 6v6c0 5.25 3.5 10.15 8 11.35C16.5 22.15 20 17.25 20 12V6l-8-4Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4" />
    </svg>
  );
}

function IconAccessToJustice({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v3M5 8h14M8 8v8a4 4 0 0 0 8 0V8" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 20h18" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 8l-3 5h6l-3-5ZM18 8l-3 5h6l-3-5Z" />
    </svg>
  );
}

function IconHumanRightsDefenders({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2a5 5 0 1 0 0 10A5 5 0 0 0 12 2Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 20c0-3.31 4.03-6 9-6s9 2.69 9 6" />
    </svg>
  );
}

function IconGenderBasedViolence({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="12" cy="8" r="4" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12v8M9 17h6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 5l-3 3M16 5h3v3" />
    </svg>
  );
}

function IconRightToFood({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3C8 3 4 6 4 10c0 5 8 11 8 11s8-6 8-11c0-4-4-7-8-7Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 10a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z" />
    </svg>
  );
}

function IconAntiCorruption({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6z" />
      <line x1="4" y1="4" x2="20" y2="20" strokeLinecap="round" />
    </svg>
  );
}

function IconMinorityLanguageRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10" />
    </svg>
  );
}

function IconArmsTransferAccountability({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 15.75l-2.489-2.489m0 0a3.375 3.375 0 10-4.773-4.773 3.375 3.375 0 004.774 4.774zM21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3M12 12l2 2" />
    </svg>
  );
}

function IconRightToDevelopment({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
    </svg>
  );
}

function IconEnvironmentalRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
    </svg>
  );
}

function IconBioethicsRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 1-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21a48.25 48.25 0 0 1-8.135-.687c-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
    </svg>
  );
}

function IconBirthRegistration({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 9h3.75M15 12h3.75M15 15h3.75M4.5 19.5h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5zm6-10.125a1.875 1.875 0 11-3.75 0 1.875 1.875 0 013.75 0zm1.294 6.336a6.721 6.721 0 01-3.17.789 6.721 6.721 0 01-3.168-.789 3.376 3.376 0 016.338 0z" />
    </svg>
  );
}

function IconMigrantDomesticWorkers({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 21v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21m0 0h4.5V3.545M12.75 21h7.5V10.75M2.25 21h1.5m18 0h-18M2.25 9l4.5-1.636M18.75 3l-1.5.545m0 6.205l3 1m1.5.5l-1.5-.5" />
    </svg>
  );
}

function IconBioethics({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
    </svg>
  );
}

function IconSexWorkRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="12" cy="8" r="4" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12v10M8 18h8" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 5l2 2M17 5l-2 2" />
      <line x1="4" y1="20" x2="8" y2="16" strokeLinecap="round" />
    </svg>
  );
}

function IconEnvironmentalDefenders({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3C7 3 3 7 3 12c0 6 9 9 9 9s9-3 9-9c0-5-4-9-9-9Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3" />
      <line x1="3" y1="3" x2="7" y2="7" strokeLinecap="round" />
    </svg>
  );
}


function IconPeasantRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c0 0-7 4-7 9a7 7 0 0014 0c0-5-7-9-7-9z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12v9M9 18h6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 8h2M17 8h2" />
    </svg>
  );
}

function IconPrisonLabor({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <rect x="3" y="3" width="18" height="18" rx="2" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 3v18M16 3v18M3 8h18M3 16h18" />
      <circle cx="12" cy="12" r="2" strokeLinecap="round" />
    </svg>
  );
}

function IconCulturalHeritageDestruction({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 21h8M12 3l8 6H4l8-6zM5 9v8M19 9v8M9 9v8M15 9v8" />
      <line x1="4" y1="4" x2="20" y2="20" strokeLinecap="round" />
    </svg>
  );
}

function IconDrugPolicyHumanRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 3h6l2 4H7L9 3zM7 7v12a2 2 0 002 2h6a2 2 0 002-2V7H7z" />
      <line x1="3" y1="3" x2="21" y2="21" strokeLinecap="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 10v5" />
    </svg>
  );
}

function IconRightToTruth({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3a9 9 0 100 18A9 9 0 0012 3z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M7 16l-3 3M17 16l3 3" />
    </svg>
  );
}

function IconCounterterrorismAbuse({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3l8 4v5c0 4-3.5 7.5-8 9-4.5-1.5-8-5-8-9V7l8-4z" />
      <line x1="9" y1="9" x2="15" y2="15" strokeLinecap="round" />
      <line x1="15" y1="9" x2="9" y2="15" strokeLinecap="round" />
    </svg>
  );
}

function IconWhistleblowerProtection({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3a4 4 0 014 4v1h1a2 2 0 012 2v6a2 2 0 01-2 2H7a2 2 0 01-2-2v-6a2 2 0 012-2h1V7a4 4 0 014-4z" />
      <circle cx="12" cy="14" r="1.5" strokeLinecap="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 3l18 18" />
    </svg>
  );
}

function IconFoodSovereignty({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21C12 21 5 15 5 9a7 7 0 0114 0c0 6-7 12-7 12z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v6M9 12h6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 5L5 2M16 5l3-3" />
    </svg>
  );
}

function IconEconomicSanctions({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="12" cy="12" r="9" strokeLinecap="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v2M12 16v2M8 12H6M18 12h-2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M10 10l4 4M14 10l-4 4" />
    </svg>
  );
}

function IconJuvenileJustice({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="12" cy="7" r="3" strokeLinecap="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 21v-2a4 4 0 014-4h4a4 4 0 014 4v2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 12h18M8 12v4M16 12v4" />
    </svg>
  );
}

function IconBusinessHumanRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <rect x="2" y="7" width="20" height="14" rx="2" strokeLinecap="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12v4M10 14h4" />
      <line x1="4" y1="4" x2="20" y2="20" strokeLinecap="round" />
    </svg>
  );
}

function IconMigrantDetention({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 10h18M3 14h18M7 3v18M17 3v18" />
      <rect x="3" y="3" width="18" height="18" rx="2" strokeLinecap="round" />
      <circle cx="12" cy="12" r="2" strokeLinecap="round" />
    </svg>
  );
}

function IconSolitaryConfinement({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <rect x="4" y="4" width="16" height="16" rx="2" strokeLinecap="round" />
      <circle cx="12" cy="12" r="3" strokeLinecap="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 12H1M23 12h-3M12 4V1M12 23v-3" />
    </svg>
  );
}

function IconMedicalNeutrality({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2a10 10 0 100 20A10 10 0 0012 2z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6M12 9v6" />
      <line x1="4" y1="4" x2="20" y2="20" strokeLinecap="round" />
    </svg>
  );
}

function IconHumanRightsEducation({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3L2 8l10 5 10-5-10-5z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M2 17l10 5 10-5M2 12l10 5 10-5" />
      <line x1="5" y1="5" x2="19" y2="19" strokeLinecap="round" />
    </svg>
  );
}
function IconNuclearTestingLegacy({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="12" cy="12" r="4" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2v4M12 18v4M2 12h4M18 12h4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
    </svg>
  );
}
function IconClimateLossDamage({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 17l4-8 4 6 3-4 4 6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 21h18" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 3c1.5 1 2.5 2.5 2.5 4.5 0 2-1.5 3.5-2.5 4.5" />
    </svg>
  );
}
function IconPrisonOvercrowding({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <rect x="3" y="3" width="18" height="18" rx="2" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 3v18M16 3v18M3 9h18M3 15h18" />
    </svg>
  );
}
function IconStatelessness({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="12" cy="8" r="4" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
      <line x1="2" y1="2" x2="22" y2="22" strokeLinecap="round" />
    </svg>
  );
}
function IconChildMarriage({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2a3 3 0 100 6 3 3 0 000-6z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M7 22v-3a5 5 0 0110 0v3" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l3 3-3 3M7 8l-3 3 3 3" />
    </svg>
  );
}
function IconDigitalSurveillance({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
      <circle cx="12" cy="12" r="3" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2M12 19v2M3 12H1M23 12h-2" />
    </svg>
  );
}
function IconSocialMediaCensorship({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M18.364 5.636a9 9 0 010 12.728M15.536 8.464a5 5 0 010 7.072M5.636 5.636a9 9 0 000 12.728M8.464 8.464a5 5 0 000 7.072" />
      <line x1="3" y1="3" x2="21" y2="21" strokeLinecap="round" />
    </svg>
  );
}
function IconOrganTrafficking({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
      <line x1="3" y1="3" x2="21" y2="21" strokeLinecap="round" />
    </svg>
  );
}
function IconLandRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 21h18M3 10h18M3 7l9-4 9 4M4 10v11M20 10v11M8 10v11M12 10v11M16 10v11" />
    </svg>
  );
}
function IconForcedDisappearances({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="12" cy="8" r="4" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M20 4l-8 8M12 4l8 8" strokeDasharray="2 2" />
    </svg>
  );
}
function IconHumanTrafficking({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4-4 4M3 12h18" />
      <circle cx="7" cy="9" r="2" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 20v-2a4 4 0 014-4h2" />
    </svg>
  );
}
function IconDisabilityRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="12" cy="5" r="2" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v5l3 3M9 21c0-3 1.5-5 3-6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M16 14a5 5 0 11-10 0" />
    </svg>
  );
}
function IconColonialReparationsLegacy({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 6h18M3 12h18M3 18h18" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v18" />
      <circle cx="12" cy="12" r="3" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
function IconWaterRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2C12 2 5 10 5 15a7 7 0 0014 0C19 10 12 2 12 2z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 15a3 3 0 006 0" />
    </svg>
  );
}
function IconInternetShutdown({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 3l18 18" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.5 8.5A8.96 8.96 0 003 12c2 3 5.4 5 9 5a8.97 8.97 0 005.5-1.9" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6.1A9 9 0 0121 12c-.7 1.2-1.7 2.3-2.9 3.1" />
      <circle cx="12" cy="12" r="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
function IconAcademicFreedom({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3L2 8l10 5 10-5-10-5z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M2 8v8l10 5 10-5V8" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 13v8" />
    </svg>
  );
}
function IconRefugeeDetention({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <rect x="3" y="8" width="18" height="13" rx="1" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M7 8V6a5 5 0 0110 0v2" />
      <circle cx="12" cy="14" r="2" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 16v2" />
    </svg>
  );
}
function IconCorporateImpunity({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 21h18M9 21V9l3-6 3 6v12M5 21V13H3l9-10 9 10h-2v8" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M13 17h-2v4h2v-4z" />
    </svg>
  );
}
function IconGenderPayGap({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="8" cy="8" r="4" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="16" cy="8" r="4" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 12v8M5 17h6M16 12v4M13 19h6M16 16v4" />
    </svg>
  );
}
function IconIndigenousRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2l3 7h7l-5.5 4 2 7L12 16l-6.5 4 2-7L2 9h7z" />
    </svg>
  );
}
function IconArmsTrade({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 3H4a1 1 0 00-1 1v3l3 3h10l3-3V4a1 1 0 00-1-1h-5" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 9v12M18 9v4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 20h6M15 17l3 3 3-3" />
    </svg>
  );
}
function IconTransitionalJustice({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v4M8 7h8M6 7l-2 8h16l-2-8" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 15v4m6-4v4M7 19h10" />
      <circle cx="12" cy="5" r="1" />
    </svg>
  );
}
function IconClimateDisplacement({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 12a9 9 0 0118 0" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M7 17c0-2.8 2.2-5 5-5s5 2.2 5 5" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 7V3M9 5l3-2 3 2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 21h14" />
    </svg>
  );
}
function IconEnvironmentalCrime({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3C8 3 4 7 4 12s4 9 8 9 8-4 8-9-4-9-8-9z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c0 0 4 4 4 9M12 3c0 0-4 4-4 9" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 12h16" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 7l14 10M19 7L5 17" strokeDasharray="3 2" />
    </svg>
  );
}
function IconPretrialDetention({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <rect x="3" y="6" width="18" height="15" rx="2" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 10h18" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 6V4M16 6V4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 14v3M10.5 15.5h3" />
    </svg>
  );
}
function IconEmergencyPowersAbuse({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2L3 7v5c0 5.5 3.8 10.7 9 12 5.2-1.3 9-6.5 9-12V7L12 2z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4M12 16h.01" />
    </svg>
  );
}
function IconRacialProfiling({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="9" cy="7" r="4" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 8l2 2-2 2M21 10h-4" />
    </svg>
  );
}
function IconHateSpeechIncitement({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m0 3.75h.008v.008H12v-.008z" />
    </svg>
  );
}
function IconSlaveryReparations({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0 0 12 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 0 1-2.031.352 5.988 5.988 0 0 1-2.031-.352c-.483-.174-.711-.703-.589-1.202L18.75 4.971Zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 0 1-2.031.352 5.989 5.989 0 0 1-2.031-.352c-.483-.174-.711-.703-.589-1.202L5.25 4.971Z" />
    </svg>
  );
}
function IconConflictMinerals({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
    </svg>
  );
}
function IconMentalHealthRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456Z" />
    </svg>
  );
}
function IconAusteritySocialRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18 9 11.25l4.306 4.306a11.95 11.95 0 0 1 5.814-5.518l2.74-1.22m0 0-5.94-2.281m5.94 2.28-2.28 5.941" />
    </svg>
  );
}
function IconIntersexRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <circle cx="12" cy="8" r="4" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12v9M9 18h6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M7 5.5A5 5 0 0 1 17 5.5" />
    </svg>
  );
}
function IconClimateLitigationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
    </svg>
  );
}
function IconChildPovertySocialExclusion({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.182 15.182a4.5 4.5 0 0 1-6.364 0M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0ZM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75Zm-.375 0h.008v.015h-.008V9.75Zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75Zm-.375 0h.008v.015h-.008V9.75Z" />
    </svg>
  );
}
function IconElderAbuseRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12v4M10 14h4" />
    </svg>
  );
}
function IconSanitationRightsAccess({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
    </svg>
  );
}
function IconPrisonHealthcareDenial({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25Z" />
    </svg>
  );
}
function IconConscientiousObjectorRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 3v1.5M3 21v-6m0 0 2.77-.693a9 9 0 0 1 6.208.682l.108.054a9 9 0 0 0 6.086.71l3.114-.732a48.524 48.524 0 0 1-.005-10.499l-3.11.732a9 9 0 0 1-6.085-.711l-.108-.054a9 9 0 0 0-6.208-.682L3 4.5M3 15V4.5" />
    </svg>
  );
}

function IconWitchHuntPersecution({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
    </svg>
  );
}

function IconAlbinismRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
    </svg>
  );
}

function IconMenstrualHealthEducation({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 3.741-1.342m-7.482 0 7.482 0" />
    </svg>
  );
}

function IconFacialRecognitionSurveillance({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 3.75H6A2.25 2.25 0 0 0 3.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0 1 20.25 6v1.5m0 9V18A2.25 2.25 0 0 1 18 20.25h-1.5m-9 0H6A2.25 2.25 0 0 1 3.75 18v-1.5M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
    </svg>
  );
}

function IconArtisanalMiningRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 7.125C2.25 6.504 2.754 6 3.375 6h6c.621 0 1.125.504 1.125 1.125v3.75c0 .621-.504 1.125-1.125 1.125h-6a1.125 1.125 0 0 1-1.125-1.125v-3.75ZM14.25 8.625c0-.621.504-1.125 1.125-1.125h5.25c.621 0 1.125.504 1.125 1.125v8.25c0 .621-.504 1.125-1.125 1.125h-5.25a1.125 1.125 0 0 1-1.125-1.125v-8.25ZM3.75 16.125c0-.621.504-1.125 1.125-1.125h5.25c.621 0 1.125.504 1.125 1.125v2.25c0 .621-.504 1.125-1.125 1.125h-5.25a1.125 1.125 0 0 1-1.125-1.125v-2.25Z" />
    </svg>
  );
}

function IconNomadicPeoplesRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 21v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21m0 0h4.5V3.545M12.75 21h7.5V10.75M2.25 21h1.5m18 0h-18M2.25 9l4.5-1.636M18.75 3l-1.5.545m0 6.205 3 1m1.5.5-1.5-.5M6.75 7.364V3h-3v18m3-13.636 10.5-3.819" />
    </svg>
  );
}

function IconAccessMedicineInequality({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 1-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
    </svg>
  );
}

function IconInformalEconomyRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 0 0 .75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 0 0-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0 1 12 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 0 1-.673-.38m0 0A2.18 2.18 0 0 1 3 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 0 1 3.413-.387m7.5 0V5.25A2.25 2.25 0 0 0 13.5 3h-3a2.25 2.25 0 0 0-2.25 2.25v.894m7.5 0a48.667 48.667 0 0 0-7.5 0M12 12.75h.008v.008H12v-.008Z" />
    </svg>
  );
}

function IconSexEducationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
    </svg>
  );
}

function IconNeurorightMentalSovereignty({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15m-6.3-11.896c.251.023.501.05.75.082M19.8 15l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 1-6.23-.607L4.2 14M19.8 15l.9 2.25m-15.3-2.25-.9 2.25m0 0 .675 1.688a.75.75 0 0 0 1.412-.112L6 19.5m12.6-2.25-.675 1.688a.75.75 0 0 1-1.412-.112L16.5 19.5" />
    </svg>
  );
}

function IconEconomicDomesticAbuse({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18.75a60.07 60.07 0 0 1 15.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 0 1 3 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 0 0-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 0 1-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 0 0 3 15h-.75M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm3 0h.008v.008H18V10.5Zm-12 0h.008v.008H6V10.5Z" />
    </svg>
  );
}

function IconEcoGriefRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
    </svg>
  );
}

function IconNeurodiversityRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
    </svg>
  );
}

function IconGeneticDiscrimination({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 0 0-3.7-3.7 48.678 48.678 0 0 0-7.324 0 4.006 4.006 0 0 0-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 0 0 3.7 3.7 48.656 48.656 0 0 0 7.324 0 4.006 4.006 0 0 0 3.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3-3 3" />
    </svg>
  );
}

function IconMenopauseWorkplaceRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
    </svg>
  );
}

function IconObstetricViolenceRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
    </svg>
  );
}

function IconPeriodPovertyRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c-4.97 0-9 3.185-9 7.115 0 2.496 1.47 4.694 3.75 6.028V21l3-2 3 2v-4.857C15.53 14.809 21 12.61 21 10.115 21 6.185 16.97 3 12 3Z" />
    </svg>
  );
}

function IconRefugeeDigitalRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 5.25a3 3 0 0 1 3 3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 0 1 21.75 8.25Z" />
    </svg>
  );
}
function IconAlgorithmicBiasRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
    </svg>
  );
}
function IconHateSpeechPlatformRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 0 1-.923 1.785A5.969 5.969 0 0 0 6 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h.01M12 12h.01M15 12h.01" />
    </svg>
  );
}

function IconDigitalGenderGapRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 17.25v1.007a3 3 0 0 1-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0 1 15 18.257V17.25m6-12V15a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 15V5.25A2.25 2.25 0 0 1 5.25 3h13.5A2.25 2.25 0 0 1 21 5.25Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 8.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM12 8.25v4.5" />
    </svg>
  );
}

function IconUnpaidCareWorkRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9.75c.621 0 1.125.504 1.125 1.125v.375c0 .621-.504 1.125-1.125 1.125H8.25A1.125 1.125 0 0 1 7.125 11.25v-.375C7.125 10.254 7.629 9.75 8.25 9.75h7.5Z" />
    </svg>
  );
}

function IconYouthJusticeRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0 0 12 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 0 1-2.031.352 5.988 5.988 0 0 1-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.97Zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 0 1-2.031.352 5.989 5.989 0 0 1-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.97Z" />
    </svg>
  );
}

function IconLandGrabbingRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 9.75L21 6m0 0l-3.75-3.75M21 6H9" />
    </svg>
  );
}




function IconPrisonLaborRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM21.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM21.75 17.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
    </svg>
  );
}

function IconStatelessnessRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5} aria-hidden="true">
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 4.5 15 15" />
    </svg>
  );
}

function IconClimateForcedMigrationRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" />
    </svg>
  );
}

function IconChildLaborMiningRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
    </svg>
  );
}

function IconWaterRightsAccess({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.362 5.214A8.252 8.252 0 0 1 12 21 8.25 8.25 0 0 1 6.038 7.047 8.287 8.287 0 0 0 9 9.601a8.983 8.983 0 0 1 3.361-6.867 8.21 8.21 0 0 0 3 2.48Z" />
    </svg>
  );
}
function IconAISurveillanceRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 3.75H6A2.25 2.25 0 0 0 3.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0 1 20.25 6v1.5m0 9V18A2.25 2.25 0 0 1 18 20.25h-1.5m-9 0H6A2.25 2.25 0 0 1 3.75 18v-1.5M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
    </svg>
  );
}
function IconGigEconomyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 1.5H8.25A2.25 2.25 0 0 0 6 3.75v16.5a2.25 2.25 0 0 0 2.25 2.25h7.5A2.25 2.25 0 0 0 18 20.25V3.75a2.25 2.25 0 0 0-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 8.25h3m-3 3.75h3M9 21.75H6" />
    </svg>
  );
}
function IconEnforcedDisappearances({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
    </svg>
  );
}
function IconChildSoldiersRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
    </svg>
  );
}
function IconOlderPersonsRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z M12 14.25v3M10.5 16.5h3" />
    </svg>
  );
}
function IconMentalHealthRightsW78({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
    </svg>
  );
}
function IconDebtBondageRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
    </svg>
  );
}
function IconSeafarersMaritimeLaborRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M3 17l3-10h12l3 10"/>
      <path d="M12 3v4"/>
      <path d="M8 7h8"/>
      <path d="M2 20h20"/>
      <path d="M6 17c0 1.5 1.5 2 3 2s3-.5 3-2 1.5-2 3-2 3 .5 3 2"/>
    </svg>
  );
}
function IconCulturalMinorityRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <circle cx="12" cy="12" r="10"/>
      <path d="M2 12h20"/>
      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
      <path d="M9 5l3-3 3 3"/>
    </svg>
  );
}
function IconRightToStrikeLaborRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0"/>
      <path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v2"/>
      <path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8"/>
      <path d="M18 11a2 2 0 1 1 4 0v3a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>
    </svg>
  );
}

function IconJudicialIndependenceRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 2L3 7l9 5 9-5-9-5z"/>
      <path d="M3 12l9 5 9-5"/>
      <path d="M12 17v5"/>
      <path d="M8 19l-4 2"/>
      <path d="M16 19l4 2"/>
    </svg>
  );
}

function IconIndigenousDataSovereignty({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <circle cx="12" cy="12" r="10"/>
      <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>
      <path d="M2 12h20"/>
      <path d="M12 2v4M12 18v4"/>
    </svg>
  );
}

function IconFairTrialDueProcess({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
      <path d="M14 3h7v7"/>
      <path d="M21 3l-9 9"/>
      <path d="M7 13h5"/>
      <path d="M7 17h3"/>
    </svg>
  );
}

function IconRightToAsylumRefugeeProtection({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
      <polyline points="9 22 9 12 15 12 15 22"/>
      <circle cx="12" cy="7" r="1" fill="currentColor"/>
    </svg>
  );
}

function IconGenderBasedViolenceFemicide({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <circle cx="12" cy="8" r="4"/>
      <path d="M12 12v10"/>
      <path d="M9 19h6"/>
      <path d="M9 4.5L7 2.5"/>
      <path d="M15 4.5L17 2.5"/>
    </svg>
  );
}

function IconAntiCorruptionAccountability({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      <path d="M9 12l2 2 4-4"/>
    </svg>
  );
}

function IconDigitalPrivacySurveillanceRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
      <circle cx="12" cy="12" r="3"/>
      <line x1="1" y1="1" x2="23" y2="23"/>
    </svg>
  );
}

function IconFreedomOfAssemblyProtestRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
      <circle cx="9" cy="7" r="4"/>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    </svg>
  );
}

function IconHousingEvictionHomelessnessRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
      <polyline points="9 22 9 12 15 12 15 22"/>
      <line x1="12" y1="2" x2="12" y2="9"/>
      <line x1="9" y1="5.5" x2="15" y2="5.5"/>
    </svg>
  );
}

function IconChildTraffickingExploitationRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/>
      <circle cx="12" cy="10" r="3"/>
    </svg>
  );
}

function IconDisabilityRightsAccessibility({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <circle cx="12" cy="4" r="2"/>
      <path d="M19 13v-2a7 7 0 0 0-14 0v2"/>
      <path d="M5 13h14l-2 7H7l-2-7z"/>
    </svg>
  );
}

function IconAcademicFreedomEducationRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
      <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
    </svg>
  );
}

function IconMinorityReligiousFreedomRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 2L2 7l10 5 10-5-10-5z"/>
      <path d="M12 22V12"/>
      <path d="M7 9.5v5"/>
      <path d="M17 9.5v5"/>
      <circle cx="12" cy="12" r="2"/>
    </svg>
  );
}

function IconSexualOrientationLgbtqRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <circle cx="12" cy="12" r="10"/>
      <path d="M8 12l2 2 4-4"/>
      <path d="M12 6v2"/>
      <path d="M12 16v2"/>
    </svg>
  );
}

function IconFoodSovereigntyFamineRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 2a10 10 0 1 0 10 10"/>
      <path d="M12 8v4l3 3"/>
      <path d="M16 2l2 2-2 2"/>
      <path d="M18 4h4"/>
    </svg>
  );
}

function IconPressFreedomJournalistProtection({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/>
      <path d="M18 14h-8"/>
      <path d="M15 18h-5"/>
      <path d="M10 6h8v4h-8V6z"/>
    </svg>
  );
}

function IconClimateJusticeEnvironmentalDefenders({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 22V12"/>
      <path d="M5 12H2a10 10 0 0 0 20 0h-3"/>
      <path d="M12 2C6.5 2 2 6.5 2 12"/>
      <path d="M22 12c0-5.5-4.5-10-10-10"/>
      <path d="M9 12l3-3 3 3"/>
    </svg>
  );
}

function IconMigrantWorkerLaborExploitation({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
      <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
      <line x1="12" y1="12" x2="12" y2="16"/>
    </svg>
  );
}

function IconDeathPenaltyExtrajudicialKillings({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <circle cx="12" cy="12" r="10"/>
      <line x1="15" y1="9" x2="9" y2="15"/>
      <line x1="9" y1="9" x2="15" y2="15"/>
    </svg>
  );
}

function IconHumanRightsDefendersProtection({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
    </svg>
  );
}

function IconCybercrimeDigitalRightsExploitation({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
      <line x1="8" y1="21" x2="16" y2="21"/>
      <line x1="12" y1="17" x2="12" y2="21"/>
      <path d="M9 9l2 2 4-4"/>
    </svg>
  );
}

function IconNuclearRadiationCivilianRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <circle cx="12" cy="12" r="4"/>
      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
    </svg>
  );
}

function IconColonialReparationsMemoryRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 2L2 7l10 5 10-5-10-5z"/>
      <path d="M2 17l10 5 10-5"/>
      <path d="M2 12l10 5 10-5"/>
    </svg>
  );
}

function IconElderCareAgingRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
      <circle cx="9" cy="7" r="4"/>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
      <line x1="19" y1="8" x2="23" y2="8"/>
    </svg>
  );
}

function IconSportsAthleteRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <circle cx="12" cy="12" r="10"/>
      <path d="M12 8l-3 4h6l-3 4"/>
      <path d="M8.56 2.75c4.37 6.03 6.02 9.42 8.03 17.72m2.54-15.38c-3.72 4.35-8.94 5.66-16.88 5.85m19.5 1.9c-3.5-.93-6.63-.82-8.94 0-2.58.92-5.01 2.86-7.44 6.32"/>
    </svg>
  );
}

function IconPrisonRehabilitationReentryRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <rect x="3" y="3" width="18" height="18" rx="2"/>
      <line x1="9" y1="3" x2="9" y2="21"/>
      <line x1="15" y1="3" x2="15" y2="21"/>
      <path d="M12 8v8M9 12h6"/>
    </svg>
  );
}

function IconPovettySocialExclusionRights({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className ?? "w-4 h-4"}>
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
      <path d="M12 6v6l4 2"/>
      <line x1="2" y1="2" x2="22" y2="22"/>
    </svg>
  );
}

function IconArtsCulturalExpressionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2L2 7l10 5 10-5-10-5z" /><path d="M2 17l10 5 10-5" /><path d="M2 12l10 5 10-5" />
    </svg>
  );
}

function IconMentalHealthInvoluntaryTreatment({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v11m0 0H5a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4m0-6h10m-10 0v6m10-6h4a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-4m0-6v6" />
    </svg>
  );
}

function IconBorderCrossingDetentionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /><line x1="12" y1="15" x2="12" y2="19" />
    </svg>
  );
}

function IconStatelessPersonsRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="8" r="4" /><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" /><line x1="2" y1="12" x2="4" y2="12" /><line x1="20" y1="12" x2="22" y2="12" />
    </svg>
  );
}

function IconHumanTraffickingLaborExploitation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M23 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /><line x1="18" y1="8" x2="22" y2="8" /><line x1="20" y1="6" x2="20" y2="10" />
    </svg>
  );
}

function IconWaterSanitationAccessRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z" /><path d="M12 6v6l4 2" />
    </svg>
  );
}

function IconCorporateAccountabilityHumanRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="7" width="20" height="14" rx="2" ry="2" /><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2" /><line x1="12" y1="12" x2="12" y2="16" /><line x1="10" y1="14" x2="14" y2="14" />
    </svg>
  );
}

function IconCounterTerrorismRightsViolations({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  );
}

function IconIndigenousLandRightsExtraction({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="3 11 22 2 13 21 11 13 3 11" /><line x1="3" y1="21" x2="11" y2="13" />
    </svg>
  );
}

function IconReproductiveRightsBodlyAutonomy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" /><path d="M8 14s1.5 2 4 2 4-2 4-2" /><line x1="9" y1="9" x2="9.01" y2="9" /><line x1="15" y1="9" x2="15.01" y2="9" />
    </svg>
  );
}

function IconOnlineCensorshipPlatformGovernance({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" /><line x1="4.93" y1="4.93" x2="19.07" y2="19.07" /><path d="M9.17 9.17A4 4 0 0 0 8 12c0 2.21 1.79 4 4 4 1.06 0 2.02-.41 2.73-1.09" />
    </svg>
  );
}

function IconForcedDisappearancesExtrajudicial({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M23 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /><line x1="20" y1="8" x2="22" y2="8" />
    </svg>
  );
}

function IconArmedConflictCivilianProtection({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" /><polyline points="9 22 9 12 15 12 15 22" />
    </svg>
  );
}

function IconWhistleblowerLeakerProtection({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M18 8h1a4 4 0 0 1 0 8h-1" /><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z" /><line x1="6" y1="1" x2="6" y2="4" /><line x1="10" y1="1" x2="10" y2="4" /><line x1="14" y1="1" x2="14" y2="4" />
    </svg>
  );
}

function IconRacialDiscriminationSystemicRacism({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" /><path d="M8 12h8" /><path d="M12 8v8" /><path d="M4.93 4.93l14.14 14.14" />
    </svg>
  );
}

function IconCasteDiscriminationUntouchability({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><line x1="17" y1="11" x2="23" y2="11" /><line x1="17" y1="15" x2="23" y2="15" />
    </svg>
  );
}

function IconBioethicsGeneticPrivacyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M2 12h4" /><path d="M18 12h4" /><path d="M12 2v4" /><path d="M12 18v4" /><circle cx="12" cy="12" r="4" /><path d="M4.93 4.93l2.83 2.83" /><path d="M16.24 16.24l2.83 2.83" /><path d="M4.93 19.07l2.83-2.83" /><path d="M16.24 7.76l2.83-2.83" />
    </svg>
  );
}

function IconMinorityLanguageCulturalRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /><line x1="9" y1="10" x2="15" y2="10" /><line x1="12" y1="7" x2="12" y2="13" />
    </svg>
  );
}

function IconLandMineClusterMunitionsRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="3" /><path d="M12 2v3M12 19v3M2 12h3M19 12h3" /><path d="M4.93 4.93l2.12 2.12M16.95 16.95l2.12 2.12M4.93 19.07l2.12-2.12M16.95 7.05l2.12-2.12" />
    </svg>
  );
}

function IconRefugeeIntegrationInclusionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M22 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /><line x1="19" y1="8" x2="23" y2="12" /><line x1="23" y1="8" x2="19" y2="12" />
    </svg>
  );
}

function IconEconomicAusteritySocialRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="1" x2="12" y2="23" /><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /><line x1="5" y1="19" x2="8" y2="16" /><line x1="5" y1="13" x2="8" y2="16" />
    </svg>
  );
}

function IconAutonomousWeaponsAiWarfareRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="3" /><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" /><line x1="12" y1="9" x2="12" y2="6" />
    </svg>
  );
}

function IconSpaceRightsOuterSpaceMilitarization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2L8 6H4l2 4-4 2 4 2-2 4h4l4 4 4-4h4l-2-4 4-2-4-2 2-4h-4z" /><circle cx="12" cy="12" r="2" />
    </svg>
  );
}

function IconDigitalDivideAccessRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="3" width="20" height="14" rx="2" /><line x1="8" y1="21" x2="16" y2="21" /><line x1="12" y1="17" x2="12" y2="21" /><line x1="2" y1="10" x2="7" y2="10" /><line x1="2" y1="14" x2="5" y2="14" />
    </svg>
  );
}

function IconClimateChangeHumanRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z" /><path d="M12 6v6l4 2" /><path d="M8 12c0-2.21 1.79-4 4-4" /><path d="M17 16.5c-1.5 1-3 1.5-5 1.5" />
    </svg>
  );
}

function IconChildLaborExploitationRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="5" r="2" /><path d="M12 7v6" /><path d="M9 10l-2 5" /><path d="M15 10l2 5" /><path d="M9 22l3-5 3 5" /><path d="M6 15h12" />
    </svg>
  );
}

function IconLgbtqRightsCriminalization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" /><path d="M12 8v4" /><path d="M8 12h8" /><path d="M9 16l3-2 3 2" /><line x1="9" y1="9" x2="15" y2="15" />
    </svg>
  );
}

function IconPrisonConditionsDetentionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="1" /><line x1="3" y1="9" x2="21" y2="9" /><line x1="3" y1="15" x2="21" y2="15" /><line x1="9" y1="3" x2="9" y2="21" /><line x1="15" y1="3" x2="15" y2="21" />
    </svg>
  );
}

function IconFreedomAssemblyAssociationRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="9" cy="7" r="2" /><circle cx="15" cy="7" r="2" /><circle cx="12" cy="14" r="2" /><path d="M9 9c0 2 1.5 3 3 3s3-1 3-3" /><path d="M12 16v4" /><path d="M9 20h6" />
    </svg>
  );
}

function IconHousingEvictionDisplacementRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" /><polyline points="9 22 9 12 15 12 15 22" /><line x1="17" y1="9" x2="22" y2="4" /><line x1="19" y1="4" x2="22" y2="4" /><line x1="22" y1="4" x2="22" y2="7" />
    </svg>
  );
}

function IconMinorityReligiousRightsPersecution({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2l2 7h7l-5.5 4 2 7L12 16l-5.5 4 2-7L3 9h7z" /><line x1="12" y1="16" x2="12" y2="22" />
    </svg>
  );
}

function IconSocialMediaPoliticalCensorship({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="18" cy="5" r="3" /><circle cx="6" cy="12" r="3" /><circle cx="18" cy="19" r="3" /><line x1="8.59" y1="13.51" x2="15.42" y2="17.49" /><line x1="15.41" y1="6.51" x2="8.59" y2="10.49" /><line x1="3" y1="3" x2="21" y2="21" />
    </svg>
  );
}

function IconElderlyRightsAgeDiscrimination({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="7" r="4" /><path d="M6 21v-1a6 6 0 0 1 12 0v1" /><path d="M8 11l-2 6" /><path d="M16 11l2 6" /><line x1="10" y1="17" x2="14" y2="17" />
    </svg>
  );
}

function IconMigrationAsylumSeekersRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 12h18" /><path d="M3 12l4-4" /><path d="M3 12l4 4" /><path d="M21 12l-4-4" /><path d="M21 12l-4 4" /><circle cx="12" cy="12" r="3" />
    </svg>
  );
}

function IconAcademicFreedomUniversityRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 10v6M2 10l10-5 10 5-10 5z" /><path d="M6 12v5c3 3 9 3 12 0v-5" /><line x1="12" y1="22" x2="12" y2="17" />
    </svg>
  );
}

function IconForcedMarriageChildMarriageRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="9" cy="7" r="3" /><path d="M3 21v-1a6 6 0 0 1 9.17-5.07" /><circle cx="17" cy="15" r="4" /><line x1="17" y1="11" x2="17" y2="13" /><line x1="17" y1="17" x2="17" y2="19" /><line x1="13" y1="15" x2="15" y2="15" /><line x1="19" y1="15" x2="21" y2="15" />
    </svg>
  );
}

function IconNuclearWeaponsDisarmamentRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="3" /><path d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M2 12h3M19 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12" /><circle cx="12" cy="12" r="8" strokeDasharray="4 2" />
    </svg>
  );
}

function IconAntiCorruptionAccountabilityRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /><line x1="9" y1="12" x2="15" y2="12" /><line x1="12" y1="9" x2="12" y2="15" />
    </svg>
  );
}

function IconInternetShutdownDigitalRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 3l18 18" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.584 10.587a2 2 0 002.828 2.829" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.363 5.365A9.466 9.466 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17.593 17.593A9.467 9.467 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.98 9.98 0 013.093-4.655" />
    </svg>
  );
}

function IconStatelessnessCitizenshipRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 9.75l.75.75M13.5 9.75l-.75.75" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75h.008v.008H9v-.008zm6 0h.008v.008H15v-.008z" />
    </svg>
  );
}

function IconHumanTraffickingModernSlavery({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 10.5V6.75a4.5 4.5 0 119 0v3.75" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.375 7.5h17.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125H3.375A1.125 1.125 0 012.25 19.875V8.625c0-.621.504-1.125 1.125-1.125z" />
    </svg>
  );
}

function IconClimateDisplacementMigration({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9 9 0 100-18 9 9 0 000 18z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.6 9h16.8M3.6 15h16.8M12 3a15 15 0 010 18M12 3a15 15 0 000 18" />
    </svg>
  );
}

function IconChildLaborEducationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
    </svg>
  );
}

function IconColonialReparationsHistoricalJustice({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1.5M12 19.5V21M3 12h1.5M19.5 12H21M6.22 6.22l1.06 1.06M16.72 16.72l1.06 1.06M6.22 17.78l1.06-1.06M16.72 7.28l1.06-1.06" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12a3 3 0 106 0 3 3 0 00-6 0z" />
    </svg>
  );
}

function IconBiometricSurveillanceStateControl({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 3l1.5 1.5M15 3l-1.5 1.5M9 21l1.5-1.5M15 21l-1.5-1.5" />
    </svg>
  );
}

function IconFoodSovereigntyAgriculturalRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c0 0-4 4-4 9s4 9 4 9" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c0 0 4 4 4 9s-4 9-4 9" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 9h8M8 12h8M8 15h8" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 21h18" />
    </svg>
  );
}

function IconDebtTrapEconomicCoercionRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}

function IconEnvironmentalDefendersPersecution({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12.75 3.03v.568c0 .334.148.65.405.864l1.068.89c.442.369.535 1.01.216 1.49l-.51.766a2.25 2.25 0 01-1.161.886l-.143.048a1.107 1.107 0 00-.57 1.664c.369.555.169 1.307-.427 1.605L9 13.125l.423 1.059a.956.956 0 01-1.652.928l-.679-.906a1.125 1.125 0 00-1.906.172L4.5 15.75" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12z" />
    </svg>
  );
}

function IconReligiousLawLgbtqRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 9l6 6M15 9l-6 6" />
    </svg>
  );
}

function IconDisabilityRightsAbleism({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="12" cy="5" r="2" strokeLinecap="round" strokeLinejoin="round" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 7v6l3 3" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 13H5a2 2 0 00-2 2v2a2 2 0 002 2h14a2 2 0 002-2v-2a2 2 0 00-2-2h-4" />
    </svg>
  );
}

function IconGenocidePreventionAccountability({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
    </svg>
  );
}

function IconLaborUnionRightsFreedomAssociation({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}

function IconMaternalHealthRightsObstetricViolence({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v.75m0 3v.75m0 3v.75M12 15v.75" />
    </svg>
  );
}

function IconAcademicFreedomScholarPersecution({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.627 48.627 0 0112 20.904a48.627 48.627 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 0110.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.697 50.697 0 0112 13.489a50.702 50.702 0 017.74-3.342M6.75 15a.75.75 0 100-1.5.75.75 0 000 1.5zm0 0v-3.675A55.378 55.378 0 0112 8.443m-7.007 11.55A5.981 5.981 0 006.75 15.75v-1.5" />
    </svg>
  );
}

function IconClimateRefugeeDisplacementRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
    </svg>
  );
}

function IconStatelessPersonsNationalityRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 9h3.75M15 12h3.75M15 15h3.75M4.5 19.5h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5zm6-10.125a1.875 1.875 0 11-3.75 0 1.875 1.875 0 013.75 0zm1.294 6.336a6.721 6.721 0 01-3.17.789 6.721 6.721 0 01-3.168-.789 3.376 3.376 0 016.338 0z" />
    </svg>
  );
}

function IconIndigenousLandRightsTerritoralSovereignty({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 6.75V15m6-6v8.25m.503 3.498l4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 00-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0z" />
    </svg>
  );
}

function IconDigitalSurveillancePrivacyRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.964-7.178z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}

function IconMentalHealthRightsPsychiatricViolence({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
    </svg>
  );
}

function IconForcedDisappearanceExtrajudicialKilling({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}

function IconChildAgriculturalLabor({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1m8-9h1M3 12H2m15.364-6.364l.707.707M5.636 18.364l-.707.707M18.364 18.364l.707-.707M5.636 5.636l-.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
    </svg>
  );
}

function IconDigitalSurveillanceMassRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.964-7.178z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}

function IconForcedEvictionLandRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 21v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21m0 0h4.5V3.545M12.75 21h7.5V10.75M2.25 21h1.5m18 0h-18M2.25 9l4.5-1.636M18.75 3l-1.5.545m0 6.205l3 1m1.5.5l-1.5-.5M6.75 7.364V3h-3v18m3-13.636l10.5-3.819" />
    </svg>
  );
}

function IconRefugeesAsylumSeekersRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 9V5.25A2.25 2.25 0 0110.5 3h6a2.25 2.25 0 012.25 2.25v13.5A2.25 2.25 0 0116.5 21h-6a2.25 2.25 0 01-2.25-2.25V15m-3 0l-3-3m0 0l3-3m-3 3H15" />
    </svg>
  );
}

function IconBusinessTaxEvasionHumanRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
    </svg>
  )
}

function IconPandemicHealthEmergencyRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m0-10.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.75c0 5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.57-.598-3.75h-.152c-3.196 0-6.1-1.249-8.25-3.286zm0 13.036h.008v.008H12v-.008z" />
    </svg>
  )
}

function IconCorruptionHumanRightsNexus({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1M4.22 4.22l.707.707m12.728 12.728.707.707M3 12h1m16 0h1M4.927 19.073l.707-.707M18.364 5.636l.707-.707" />
      <circle cx="12" cy="12" r="4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3" />
    </svg>
  );
}

function IconReligiousPersecutionMinorityRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2L8 8H2l4.5 4-1.5 6L12 15l7 3-1.5-6L22 8h-6L12 2z" />
    </svg>
  );
}

function IconArmsTradeCivilianHarm({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 12h12M15 8l4 4-4 4M9 6H6a2 2 0 00-2 2v8a2 2 0 002 2h3" />
    </svg>
  );
}

function IconLgbtqRightsViolenceCriminalization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v2M12 18v2M4 12H2M22 12h-2" />
    </svg>
  );
}

function IconPressFreedomJournalistSafety({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10l6 6v8a2 2 0 01-2 2z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6M9 16h4M13 4v4h6" />
    </svg>
  );
}

function IconLandGrabbingDisplacementRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21" />
    </svg>
  );
}

function IconWaterPollutionEnvironmentalRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c-4.97 5.06-7 8.47-7 11a7 7 0 0014 0c0-2.53-2.03-5.94-7-11z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 15l1.5 1.5L14 13" />
    </svg>
  );
}

function IconEthnicMinorityRightsDiscrimination({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
    </svg>
  );
}

function IconHousingRightsForcedEvictions({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 3l6 6M21 3l-6 6" />
    </svg>
  );
}

function IconDeathPenaltyExecutionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}

function IconMigrantWorkersRightsKafala({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5l3 3m0 0l-3 3m3-3H9" />
    </svg>
  );
}

function IconTortureCruelTreatmentDetention({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
    </svg>
  );
}

function IconWomensRightsGenderBasedViolence({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="12" cy="8" r="4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12v9M9 18h6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 5l3-3M17 5h3M17 5v3" />
    </svg>
  );
}
function IconRacialJusticePoliceBrutality({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971z" />
    </svg>
  );
}
function IconInternetFreedomCensorship({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5a17.92 17.92 0 01-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 12H6" />
    </svg>
  );
}
function IconWarCrimesAccountability({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1M4.22 4.22l.707.707m12.728 12.728.707.707M1 12h2m18 0h2M4.22 19.78l.707-.707M18.364 5.636l.707-.707" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4" />
      <circle cx="12" cy="12" r="5" />
    </svg>
  );
}

function IconEnvironmentalDefendersRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3C8 3 4 7 4 11c0 5 8 10 8 10s8-5 8-10c0-4-4-8-8-8z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v18M8 7l4 4 4-4" />
    </svg>
  );
}

function IconAntiterrorismLawsRightsAbuse({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4" />
      <line x1="16" y1="8" x2="16" y2="8" strokeLinecap="round" />
    </svg>
  );
}

function IconChildMarriageForcedUnions({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="9" cy="7" r="3" />
      <circle cx="17" cy="7" r="2" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 10c-3 0-6 2-6 5v2h12v-2c0-3-3-5-6-5z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 9c2 0 4 1.5 4 3.5V14h-4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M13 16l-2-2" />
    </svg>
  );
}

function IconProtestFreedomAssemblyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2M7 8H5a2 2 0 00-2 2v6a2 2 0 002 2h2" />
      <rect x="7" y="4" width="10" height="16" rx="1" />
      <path strokeLinecap="round" d="M10 9h4M10 12h4M10 15h2" />
    </svg>
  );
}

function IconSexualViolenceConflictImpunity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4M12 16h.01" />
    </svg>
  );
}

function IconRightToEducationAccess({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 14l9-5-9-5-9 5 9 5z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 14l6.16-3.422A12 12 0 0120 16.722V21H4v-4.278a12 12 0 011.84-6.144L12 14z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 14v7" />
    </svg>
  );
}

function IconFairTrialDueProcessRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v4M4 7h16M6 7l-2 10h16L18 7" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 17h8M12 3l-4 4M12 3l4 4" />
      <line x1="12" y1="10" x2="12" y2="14" strokeLinecap="round" />
    </svg>
  );
}

function IconXenophobiaHateCrimeMinority({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="12" cy="8" r="4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 20v-1a6 6 0 0112 0v1" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 10l-4 4M15 10l4 4" />
    </svg>
  );
}

function IconNuclearTestingEnvironmentalRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="12" cy="12" r="3" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2v3M12 19v3M2 12h3M19 12h3" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12" />
    </svg>
  );
}

function IconSocialProtectionPovertyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}

function IconFreedomExpressionArtisticCensorship({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 21h18" />
    </svg>
  );
}

function IconDeathInCustodyPrisonConditions({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 21h16.5M8.25 21V6.75A2.25 2.25 0 0110.5 4.5h3a2.25 2.25 0 012.25 2.25V21M3.75 9h16.5M12 4.5v.75" />
    </svg>
  );
}

function IconDrugPolicyCriminalizationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}

function IconIndigenousLandCulturalRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
    </svg>
  );
}

function IconOrganTraffickingBodyAutonomyRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
    </svg>
  );
}

function IconSolitaryConfinementIsolationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
    </svg>
  );
}

function IconChildOnlineExploitationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 17.25v1.007a3 3 0 01-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0115 18.257V17.25m6-12V15a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 15V5.25m18 0A2.25 2.25 0 0018.75 3H5.25A2.25 2.25 0 003 5.25m18 0V12a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 12V5.25" />
    </svg>
  );
}

function IconForcedSterilizationReproductiveCoercion({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
    </svg>
  );
}

function IconAiSurveillanceBiometricRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 3.75H6A2.25 2.25 0 003.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0120.25 6v1.5m0 9V18A2.25 2.25 0 0118 20.25h-1.5m-9 0H6A2.25 2.25 0 013.75 18v-1.5M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );
}

function IconArmsEmbargoViolationsRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}

function IconNomadicPastoralistPeoplesRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 21v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21m0 0h4.5V3.545M12.75 21h7.5V10.75M2.25 21h1.5m18 0h-18M2.25 9l4.5-1.636M18.75 3l-1.5.545m0 6.205l3 1m1.5.5l-1.5-.5M6.75 7.364V3h-3v18m3-13.636l10.5-3.819" />
    </svg>
  );
}

function IconPrisonPrivatizationProfitRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
    </svg>
  );
}

function IconCulturalHeritageDestructionRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0012 9.75c-2.551 0-5.056.2-7.5.582V21M3 21h18M12 6.75h.008v.008H12V6.75z" />
    </svg>
  );
}

function IconColonialReparationsTransitionalJustice({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.97zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.97z" />
    </svg>
  );
}

function IconMiningExtractionCommunityRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M11.42 15.17L17.25 21A2.652 2.652 0 0021 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 11-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 004.486-6.336l-3.276 3.277a3.004 3.004 0 01-2.25-2.25l3.276-3.276a4.5 4.5 0 00-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437l1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008z" />
    </svg>
  );
}
function IconWaterScarcityConflictRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z" />
    </svg>
  );
}
function IconClimateJusticeLossDamageRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
    </svg>
  );
}
function IconBorderWallMigrationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21" />
    </svg>
  );
}
function IconSexualOrientationIdentityCriminalization({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
    </svg>
  );
}
function IconInventionsPortfolio({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
    </svg>
  );
}
function IconHumanTraffickingLaborExploitationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244" />
    </svg>
  );
}
function IconDisabilityRightsInclusiveSociety({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
    </svg>
  );
}
function IconElderRightsAgeism({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
    </svg>
  );
}
function IconAcidAttackGenderViolence({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}
function IconNuclearVictimsRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
    </svg>
  );
}
function IconWitchHuntAccusationPersecution({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
    </svg>
  );
}
function IconAntipersonnelMinesVictimRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.008v.008H12v-.008z" />
    </svg>
  );
}
function IconDeathPenaltyAbolitionRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.97zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.988 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.97z" />
    </svg>
  );
}
function IconStreetChildrenRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
    </svg>
  );
}
function IconBondedLaborDebtSlaveryRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244" />
    </svg>
  );
}
function IconForcedRecruitmentConscriptionRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
    </svg>
  );
}
function IconTransitionalJusticeTruthCommission({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.97zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.97z" />
    </svg>
  );
}
function IconReparationsGenocideVictims({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
    </svg>
  );
}
function IconRomaTravellerRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
    </svg>
  );
}

function IconLeprosyAffectedRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9-4.03-9-9-9zm0 4c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm0 10c-2.21 0-4.15-1.12-5.33-2.83C7.72 12.72 9.79 12 12 12s4.28.72 5.33 1.17C16.15 14.88 14.21 16 12 16z" /></svg>;
}
function IconFistulaObstetricRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>;
}
function IconHIVAIDSStigmaRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>;
}
function IconPovertyCriminalizationAntiHomelessLaws({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>;
}
function IconNonconsensualIntimateImageAbuse({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>;
}
function IconResidentialSchoolIndigenousAssimilation({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" /></svg>;
}
function IconAlbinismPersecutionRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" /></svg>;
}
function IconToxicWasteEnvironmentalRacismRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" /></svg>;
}
function IconJuvenileJusticeChildDetentionRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" /></svg>;
}

function IconInventionsShowcase({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" /></svg>;
}

function IconMentalHealthForcedTreatmentRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" /></svg>;
}

function IconHumanRightsDefendersAssassination({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m0-10.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.75c0 5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.57-.598-3.75h-.152c-3.196 0-6.1-1.249-8.25-3.286zm0 13.036h.008v.008H12v-.008z" /></svg>;
}

function IconAutonomousWeaponsLethalRoboticsRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>;
}
function IconChildMarriageForcedUnionRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" /></svg>;
}
function IconColonialReparationsRestitutionRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971z" /></svg>;
}
function IconRightToFoodFamineAccountability({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" /></svg>;
}
function IconDigitalDivideInternetAccessRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M8.288 15.038a5.25 5.25 0 017.424 0M5.106 11.856c3.807-3.808 9.98-3.808 13.788 0M1.924 8.674c5.565-5.565 14.587-5.565 20.152 0M12.53 18.22l-.53.53-.53-.53a.75.75 0 011.06 0z" /></svg>;
}
function IconHumanRightsEducationRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.627 48.627 0 0112 20.904a48.627 48.627 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 0110.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.697 50.697 0 0112 13.489a50.702 50.702 0 017.74-3.342M6.75 15a.75.75 0 100-1.5.75.75 0 000 1.5zm0 0v-3.675A55.378 55.378 0 0112 8.443m-7.007 11.55A5.981 5.981 0 006.75 15.75v-1.5" /></svg>;
}
function IconElderlyAbuseCareHomeRights({ className }: { className?: string }) {
  return <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" /></svg>;
}
function IconOrganTraffickingTransplantRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12v-1m0 0V9m0 2h1m-1 0h-1" />
    </svg>
  );
}
function IconEnforcedDisappearanceRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5" />
    </svg>
  );
}
function IconCulturalGenocideHeritageDestruction({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0012 9.75c-2.551 0-5.056.2-7.5.582V21" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18l6-6 6 6" />
    </svg>
  );
}
function IconMedicalExperimentationEthicsRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1 1 .03 2.698-1.32 2.698H4.12c-1.35 0-2.32-1.698-1.32-2.698L4.2 15.3" />
    </svg>
  );
}
function IconDomesticWorkerExploitationRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9H8.25" />
    </svg>
  );
}
function IconSurveillanceFacialRecognitionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M7 7l2 2M17 7l-2 2M7 17l2-2M17 17l-2-2" />
    </svg>
  );
}
function IconWitchcraftAccusationPersecution({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}
function IconAntiCorruptionWhistleblowerProtection({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.34 15.84c-.688-.06-1.386-.09-2.09-.09H7.5a4.5 4.5 0 110-9h.75c.704 0 1.402-.03 2.09-.09m0 9.18c.253.962.584 1.892.985 2.783.247.55.06 1.21-.463 1.511l-.657.38c-.551.318-1.26.117-1.527-.461a20.845 20.845 0 01-1.44-4.282m3.102.069a18.03 18.03 0 01-.59-4.59c0-1.586.205-3.124.59-4.59m0 9.18a23.848 23.848 0 018.835 2.535M10.34 6.66a23.847 23.847 0 008.835-2.535m0 0A23.74 23.74 0 0018.795 3m.38 1.125a23.91 23.91 0 011.014 5.395m-1.014 8.855c-.118.38-.245.754-.38 1.125m.38-1.125a23.91 23.91 0 001.014-5.395m0-3.46c.495.413.811 1.035.811 1.73 0 .695-.316 1.317-.811 1.73m0-3.46a24.347 24.347 0 010 3.46" />
    </svg>
  );
}
function IconApostasyBlasphemyPersecution({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5" />
    </svg>
  );
}
function IconThirdPartyWorkValidation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}
function IconCybersecurityDataProtection({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
    </svg>
  );
}
function IconActiveCyberDefenseHoneypot({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
    </svg>
  );
}
function IconPatentRevenuePrioritization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}
function IconPeasantLandTenureRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M20.893 13.393l-1.135-1.135a2.252 2.252 0 01-.421-.585l-1.08-2.16a.414.414 0 00-.663-.107.827.827 0 01-.812.21l-1.273-.363a.89.89 0 00-.738 1.595l.587.39c.59.395.674 1.23.172 1.732l-.2.2c-.212.212-.33.498-.33.796v.41c0 .409-.11.809-.32 1.158l-1.315 2.191a2.11 2.11 0 01-1.81 1.025 1.055 1.055 0 01-1.055-1.055v-1.172c0-.92-.56-1.747-1.414-2.089l-.655-.261a2.25 2.25 0 01-1.383-2.46l.007-.042a2.25 2.25 0 01.29-.787l.09-.15a2.25 2.25 0 012.37-1.048l1.178.236a1.125 1.125 0 001.302-.795l.208-.73a1.125 1.125 0 00-.578-1.315l-.665-.332-.091.091a2.25 2.25 0 01-1.591.659h-.18c-.249 0-.487.1-.662.274a.931.931 0 01-1.458-1.137l1.411-2.353a2.25 2.25 0 00.286-.76m11.928 9.869A9 9 0 008.965 3.525m11.928 9.868A9 9 0 118.965 3.525" />
    </svg>
  );
}
function IconSexWorkerRightsCriminalization({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
    </svg>
  );
}
function IconUnaccompaniedMigrantChildrenRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 10.5l2.25 2.25-2.25 2.25" />
    </svg>
  );
}
function IconCasteDiscriminationDalitRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
    </svg>
  );
}
function IconRuralWomenLandInheritanceRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
    </svg>
  );
}
function IconAfrodescendantReparationsRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971z" />
    </svg>
  );
}
function IconDeforestationIndigenousRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v18m0-18C9.5 3 7 5 7 8c0 2 1 3.5 2.5 4.5C7.5 13.5 6 15.5 6 18h12c0-2.5-1.5-4.5-3.5-5.5C16 11.5 17 10 17 8c0-3-2.5-5-5-5z" />
    </svg>
  );
}
function IconWildlifeTraffickingBiodiversityRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
    </svg>
  );
}
function IconMalnutritionChildNutritionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12v-2m0 0V8m0 2h2m-2 0H10" />
    </svg>
  );
}
function IconPrivateMilitaryContractorAccountability({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 01-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 011.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 00-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 01-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 00-3.375-3.375h-1.5a1.125 1.125 0 01-1.125-1.125v-1.5a3.375 3.375 0 00-3.375-3.375H9.75" />
    </svg>
  );
}
function IconInformationWarfareCivilianRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 01-2.25 2.25M16.5 7.5V18a2.25 2.25 0 002.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 002.25 2.25h13.5M6 7.5h3v3H6v-3z" />
    </svg>
  );
}
function IconSatelliteSurveillancePrivacyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.348 14.651a3.75 3.75 0 010-5.303m5.304 0a3.75 3.75 0 010 5.303m-7.425 2.122a6.75 6.75 0 010-9.546m9.546 0a6.75 6.75 0 010 9.546M5.106 18.894c-3.808-3.808-3.808-9.98 0-13.789m13.788 0c3.808 3.808 3.808 9.981 0 13.79M12 12h.008v.007H12V12zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
    </svg>
  );
}
function IconClimateFinanceLossDamage({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1M3 12h1m16 0h1M5.636 5.636l.707.707m11.314 11.314.707.707M5.636 18.364l.707-.707m11.314-11.314.707-.707M12 7a5 5 0 100 10A5 5 0 0012 7z" />
    </svg>
  );
}
function IconSexualViolenceConflictAccountability({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}
function IconChildrenArmedConflictGraveViolations({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
    </svg>
  );
}
function IconDigitalDivideInternetAccess({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
    </svg>
  );
}
function IconDisabilityRightsInclusion({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
    </svg>
  );
}
function IconElderRightsAgingPopulation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
    </svg>
  );
}
function IconHousingForcedEvictionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
    </svg>
  );
}
function IconWaterSanitationRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c-4.97 5.97-7.5 9.5-7.5 12a7.5 7.5 0 0015 0c0-2.5-2.53-6.03-7.5-12z" />
    </svg>
  );
}
function IconPrisonConditionsDetaineeRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
    </svg>
  );
}
function IconFreedomReligionBelief({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971z" />
    </svg>
  );
}
function IconMediaFreedomJournalistProtection({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 01-2.25 2.25M16.5 7.5V18a2.25 2.25 0 002.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 002.25 2.25h13.5M6 7.5h3v3H6v-3z" />
    </svg>
  );
}

function IconAntiTerrorismCounterExtremismRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}

function IconCorporateHumanRightsDueDiligence({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21" />
    </svg>
  );
}

function IconStatelessnessCitizenshipDeprivation({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 9h3.75M15 12h3.75M15 15h3.75M4.5 19.5h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5zm6-10.125a1.875 1.875 0 11-3.75 0 1.875 1.875 0 013.75 0zm1.294 6.336a6.721 6.721 0 01-3.17.789 6.721 6.721 0 01-3.168-.789 3.376 3.376 0 016.338 0z" />
    </svg>
  );
}

function IconRacialDiscriminationMinorityRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
    </svg>
  );
}

function IconFoodSovereigntyRightToFood({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
    </svg>
  );
}

function IconIPWatchGuardian({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
    </svg>
  );
}

function IconAccessToJusticeRuleOfLaw({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.97zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.97z" />
    </svg>
  );
}

function IconEconomicSocialRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
    </svg>
  );
}

function IconEnvironmentalRightsDefenders({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
    </svg>
  );
}

function IconNuclearWeaponsHumanitarianImpact({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}

function IconYouthRightsIntergenerationalJustice({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
    </svg>
  );
}

function IconHousingRightsEviction({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 21v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21m0 0h4.5V3.545M12.75 21h7.5V10.75M2.25 21h1.5m18 0h-18M2.25 9l4.5-1.636M18.75 3l-1.5.545m0 6.205l3 1m1.5.5l-1.5-.5M6.75 7.364V3h-3v18m3-13.636l10.5-3.819" />
    </svg>
  );
}

function IconReligiousFreedomPersecution({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
    </svg>
  );
}

function IconSexualReproductiveHealthRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
    </svg>
  );
}

function IconChildMarriageForcedUnion({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
    </svg>
  );
}

function IconInternetFreedomDigitalRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
    </svg>
  );
}

function IconIndigenousCulturalRightsLanguage({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 21l5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 016-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 01-3.827-5.802" />
    </svg>
  );
}

function IconLaborUnionCollectiveBargaining({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 00.75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 00-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0112 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 01-.673-.38m0 0A2.18 2.18 0 013 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m7.5 0V5.25A2.25 2.25 0 0013.5 3h-3a2.25 2.25 0 00-2.25 2.25v.894m7.5 0a48.667 48.667 0 00-7.5 0M12 12.75h.008v.008H12v-.008z" />
    </svg>
  );
}

function IconElderlyRightsAgeism({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
    </svg>
  );
}

function IconSocialMediaPlatformAccountability({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M7.217 10.907a2.25 2.25 0 100 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186l9.566-5.314m-9.566 7.5l9.566 5.314m0 0a2.25 2.25 0 103.935 2.186 2.25 2.25 0 00-3.935-2.186zm0-12.814a2.25 2.25 0 103.933-2.185 2.25 2.25 0 00-3.933 2.185z" />
    </svg>
  )
}

function IconRefugeeReturnVoluntaryRepatriation({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3" />
    </svg>
  )
}

function IconCorporateTaxJusticeDevelopment({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9l3-3 2.148 2.148A12.061 12.061 0 0116.5 7.605" />
    </svg>
  )
}

function IconPrisonConditionsTorture({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
    </svg>
  )
}

function IconAIAutonomousWeaponsHumanRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  )
}

function IconGenderPayGapEconomicRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
    </svg>
  )
}

function IconConflictMineralResources({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
    </svg>
  )
}

function IconAntiPersonnelMinesClusterMunitions({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  )
}

function IconPeacekeepingAccountabilityGovernance({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
    </svg>
  )
}

function IconDigitalSurveillanceMassMonitoring({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  )
}

function IconExtraordinaryRenditionSecretDetention({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25z" />
    </svg>
  )
}

function IconCriticalMineralsTransitionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
    </svg>
  )
}

function IconMegaInfrastructureConstructionLabor({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z" />
    </svg>
  )
}

function IconIccUniversalJurisdictionImpunity({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971z" />
    </svg>
  )
}

function IconDebtBondageMicrofinanceExploitation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  )
}

function IconSexualOrientationGenderIdentityRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 9l3-3m0 0h-3m3 0v3M6 15l-3 3m0 0h3m-3 0v-3" />
    </svg>
  )
}

function IconIndigenousCulturalGenocideAssimilation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253M3 12c0 .778.099 1.533.284 2.253" />
    </svg>
  )
}

function IconDisabilityRightsInclusiveDevelopment({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 6.75V9m0 0l-2.25 4.5M12 9l2.25 4.5M9.75 13.5H6a3 3 0 00-3 3v1.5m18-1.5a3 3 0 00-3-3h-3.75m-3.75 4.5h7.5" />
    </svg>
  )
}

function IconKafalaMigrantDomesticWorkers({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
    </svg>
  )
}

function IconWhistleblowerPressFreedom({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 01-2.25 2.25M16.5 7.5V18a2.25 2.25 0 002.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 002.25 2.25h13.5M6 7.5h3v3H6v-3z" />
    </svg>
  )
}

function IconNuclearTestingRadiationVictims({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1M4.22 4.22l.707.707m12.728 12.728.707.707M3 12H4m16 0h1M4.22 19.78l.707-.707m12.728-12.728.707-.707M12 7a5 5 0 100 10A5 5 0 0012 7z" />
    </svg>
  )
}

function IconStatelessPersonsDocumentationCrisis({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 9h3.75M15 12h3.75M15 15h3.75M4.5 19.5h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5zm6-10.125a1.875 1.875 0 11-3.75 0 1.875 1.875 0 013.75 0zm1.294 6.336a6.721 6.721 0 01-3.17.789 6.721 6.721 0 01-3.168-.789 3.376 3.376 0 016.338 0z" />
    </svg>
  )
}

function IconPrivateMilitaryContractorsAccountability({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
    </svg>
  )
}

function IconFemicideGenderBasedKillings({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 22c-4.97 0-9-4.03-9-9s4.03-9 9-9 9 4.03 9 9-4.03 9-9 9z"/>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3"/>
    </svg>
  )
}

function IconRomaniSintiAntiZiganism({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="12" cy="12" r="10"/>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h8M12 8v8"/>
    </svg>
  )
}

function IconColonialRestitutionHeritage({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
      <polyline points="9 22 9 12 15 12 15 22"/>
    </svg>
  )
}

function IconIntersexRightsBodily({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="12" cy="12" r="5" strokeLinecap="round" strokeLinejoin="round"/>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2v3M12 19v3M5.22 5.22l2.12 2.12M16.66 16.66l2.12 2.12M2 12h3M19 12h3M5.22 18.78l2.12-2.12M16.66 7.34l2.12-2.12"/>
    </svg>
  )
}

function IconMentalHealthDetention({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18"/>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12h.01"/>
    </svg>
  )
}

function IconPeasantRightsSmallFarmer({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 19V9l9-7 9 7v10M9 19v-5h6v5"/>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2M7 8l2 1M17 8l-2 1"/>
    </svg>
  )
}
function IconOrganTraffickingTransplant({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 0v2m0-2h2m-2 0H10" />
    </svg>
  )
}
function IconDigitalSurveillancePegasus({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 3l18 18" />
    </svg>
  )
}
function IconDeathPenaltyWrongfulExecution({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  )
}

function IconDeathPenaltyRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <circle cx={12} cy={12} r={10}/>
      <line x1={4.93} y1={4.93} x2={19.07} y2={19.07}/>
    </svg>
  );
}

function IconEnforcedDisappearancesExtrajudicial({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M17.25 12l4.5 4.5m0-4.5l-4.5 4.5" />
    </svg>
  )
}

function IconHousingForcedEvictionsRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 9.75l3 3" />
    </svg>
  )
}

function IconQuantumSurveillancePrivacy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="10" r="2" />
      <ellipse cx="10" cy="10" rx="8" ry="3" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <ellipse cx="10" cy="10" rx="3" ry="8" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <circle cx="10" cy="2" r="1" />
      <circle cx="10" cy="18" r="1" />
      <circle cx="2" cy="10" r="1" />
      <circle cx="18" cy="10" r="1" />
    </svg>
  );
}

function IconPostQuantumCryptography({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="5" y="9" width="10" height="8" rx="1" />
      <path d="M7 9V6a3 3 0 0 1 6 0v3" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <circle cx="10" cy="13" r="1.5" fill="white" />
      <path d="M16 4 Q18 6 16 8" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
      <path d="M17 5 Q19 7 17 9" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}

function IconQuantumSupremacyArmsRace({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="4" cy="4" r="2" />
      <circle cx="16" cy="4" r="2" />
      <circle cx="4" cy="16" r="2" />
      <circle cx="16" cy="16" r="2" />
      <circle cx="10" cy="10" r="2" />
      <line x1="4" y1="4" x2="10" y2="10" stroke="currentColor" strokeWidth="1" />
      <line x1="16" y1="4" x2="10" y2="10" stroke="currentColor" strokeWidth="1" />
      <line x1="4" y1="16" x2="10" y2="10" stroke="currentColor" strokeWidth="1" />
      <line x1="16" y1="16" x2="10" y2="10" stroke="currentColor" strokeWidth="1" />
      <line x1="4" y1="4" x2="16" y2="4" stroke="currentColor" strokeWidth="1" />
      <line x1="4" y1="16" x2="16" y2="16" stroke="currentColor" strokeWidth="1" />
    </svg>
  );
}

function IconBiotechGeneticDiscrimination({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2 C10 2 7 5 7 8 C7 11 10 12 10 12 C10 12 13 11 13 8 C13 5 10 2 10 2Z" opacity="0.7" />
      <path d="M10 12 C10 12 7 13 7 16 C7 19 10 19 10 19 C10 19 13 19 13 16 C13 13 10 12 10 12Z" opacity="0.7" />
      <line x1="6" y1="7" x2="14" y2="7" stroke="currentColor" strokeWidth="1" />
      <line x1="6" y1="10" x2="14" y2="10" stroke="currentColor" strokeWidth="1" />
      <line x1="6" y1="13" x2="14" y2="13" stroke="currentColor" strokeWidth="1" />
    </svg>
  );
}

function IconCarbonColonialismClimateJustice({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="10" r="7" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <path d="M3 10 Q6 6 10 8 Q14 10 17 7" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M10 3 L10 4 M10 16 L10 17" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M13 5 L11 8 M7 12 L9 15" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}

function IconDigitalFeudalismPlatformRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="2" y="12" width="4" height="6" rx="1" />
      <rect x="8" y="8" width="4" height="10" rx="1" />
      <rect x="14" y="4" width="4" height="14" rx="1" />
      <path d="M4 12 L4 8 L10 5 L10 8" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}

function IconNeurotechCognitiveLibertyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="8" r="5" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <path d="M7 8 Q10 5 13 8" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
      <path d="M10 13 L10 17" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M7 17 L13 17" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <circle cx="10" cy="8" r="1.5" />
    </svg>
  );
}

function IconSpaceColonizationIndigenousRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="10" r="4" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <path d="M10 2 L10 6 M10 14 L10 18 M2 10 L6 10 M14 10 L18 10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <circle cx="10" cy="10" r="1.5" />
      <path d="M5 5 L8 8 M12 12 L15 15" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}

function IconSyntheticBiologyBiosafetyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2 C8 4 6 6 6 9 C6 12 8 14 10 14 C12 14 14 12 14 9 C14 6 12 4 10 2Z" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <line x1="7" y1="7" x2="13" y2="7" stroke="currentColor" strokeWidth="1" />
      <line x1="7" y1="10" x2="13" y2="10" stroke="currentColor" strokeWidth="1" />
      <path d="M8 14 L7 18 M12 14 L13 18" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="6" y1="18" x2="14" y2="18" stroke="currentColor" strokeWidth="1.5" />
    </svg>
  );
}

function IconAlgorithmicJusticeBiasRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="2" y="14" width="3" height="4" rx="0.5" />
      <rect x="7" y="10" width="3" height="8" rx="0.5" />
      <rect x="12" y="6" width="3" height="12" rx="0.5" />
      <path d="M1 13 L6 9 L11 11 L16 5" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="16" cy="4" r="1.5" />
      <path d="M17 4 L19 2" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}

function IconWaterPrivatizationCommonsRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 2 C10 2 5 8 5 12 C5 15.3 7.2 18 10 18 C12.8 18 15 15.3 15 12 C15 8 10 2 10 2Z" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <path d="M7 12 Q10 10 13 12" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="10" y1="14" x2="10" y2="16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="2" y1="9" x2="4" y2="11" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
      <line x1="18" y1="9" x2="16" y2="11" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}

function IconPrisonIndustrialComplexRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="3" y="6" width="14" height="11" rx="1" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <path d="M3 10 L17 10" stroke="currentColor" strokeWidth="1" />
      <path d="M8 6 L8 3 L12 3 L12 6" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <rect x="8.5" y="12" width="3" height="5" rx="0.5" fill="currentColor" />
      <line x1="6" y1="13" x2="7.5" y2="13" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
      <line x1="12.5" y1="13" x2="14" y2="13" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}

function IconDarkWebCybercrimeRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="10" r="7" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <path d="M10 3 C10 3 7 6 7 10 C7 14 10 17 10 17 C10 17 13 14 13 10 C13 6 10 3 10 3Z" fill="none" stroke="currentColor" strokeWidth="1" />
      <path d="M3.5 7.5 L16.5 7.5 M3.5 12.5 L16.5 12.5" stroke="currentColor" strokeWidth="1" />
      <circle cx="10" cy="10" r="1.5" fill="currentColor" />
    </svg>
  );
}

function IconGigEconomyLaborExploitation({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="6" r="2.5" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <path d="M6 14 C6 11.8 7.8 10 10 10 C12.2 10 14 11.8 14 14" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M10 14 L10 18" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M7 16 L13 16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M15 8 L18 8 M16.5 6.5 L16.5 9.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="14" y1="5" x2="16" y2="3" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}

function IconIndigenousLanguageExtinction({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 5 L17 5 L17 13 L11 13 L8 17 L8 13 L3 13 Z" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round" />
      <line x1="6" y1="8" x2="14" y2="8" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
      <line x1="6" y1="10.5" x2="11" y2="10.5" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}
function IconDeepfakeSyntheticMediaRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="8" r="4" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <path d="M6 8 Q4 8 3 10 Q2 12 4 13 Q6 14 10 14 Q14 14 16 13 Q18 12 17 10 Q16 8 14 8" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
      <line x1="8" y1="6.5" x2="12" y2="9.5" stroke="currentColor" strokeWidth="1" strokeLinecap="round" opacity="0.6" />
    </svg>
  );
}
function IconOffshoreTaxHavenRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="10" r="7" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <path d="M10 3 Q13 7 13 10 Q13 13 10 17 Q7 13 7 10 Q7 7 10 3 Z" fill="none" stroke="currentColor" strokeWidth="1" />
      <line x1="3" y1="10" x2="17" y2="10" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
      <path d="M7 7 L13 7" stroke="currentColor" strokeWidth="0.8" strokeLinecap="round" strokeDasharray="2 1" />
    </svg>
  );
}
function IconStatelessnessDocumentRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="4" y="3" width="12" height="15" rx="1.5" fill="none" stroke="currentColor" strokeWidth="1.5" />
      <line x1="7" y1="7" x2="13" y2="7" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
      <line x1="7" y1="10" x2="13" y2="10" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
      <path d="M7 13 L10 13" stroke="currentColor" strokeWidth="1" strokeLinecap="round" />
      <circle cx="13" cy="14" r="2" fill="none" stroke="currentColor" strokeWidth="1" />
      <line x1="14.4" y1="15.4" x2="16" y2="17" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
    </svg>
  );
}
function IconConflictMineralSupplyChain({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <polygon points="10,3 14,8 10,7 6,8" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
      <path d="M6 8 L5 13 L10 15 L15 13 L14 8" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
      <line x1="10" y1="7" x2="10" y2="15" stroke="currentColor" strokeWidth="1" strokeLinecap="round" opacity="0.6" />
      <circle cx="10" cy="10" r="1.5" fill="currentColor" opacity="0.8" />
    </svg>
  );
}
function IconRefugeeCampRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 14 L10 5 L17 14 Z" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
      <path d="M6 14 L8 10 L10 14 Z" fill="none" stroke="currentColor" strokeWidth="1" strokeLinejoin="round" opacity="0.7" />
      <line x1="1" y1="14" x2="19" y2="14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <circle cx="15" cy="8" r="1.5" fill="none" stroke="currentColor" strokeWidth="1.2" />
    </svg>
  );
}
function IconPensionElderlyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="6" r="2.5" fill="none" stroke="currentColor" strokeWidth="1.4" />
      <path d="M7 9.5 C7 9.5 5 10 5 13 L5 16" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <path d="M13 9.5 C13 9.5 15 10 15 13 L15 16" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      <line x1="10" y1="9" x2="10" y2="14" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
      <path d="M13 12 L15.5 14 L17 13" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" opacity="0.7" />
    </svg>
  );
}
function IconDarkWebRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="10" r="7.5" fill="none" stroke="currentColor" strokeWidth="1.4" />
      <circle cx="10" cy="10" r="3" fill="none" stroke="currentColor" strokeWidth="1.2" />
      <line x1="10" y1="2.5" x2="10" y2="7" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.7" />
      <line x1="10" y1="13" x2="10" y2="17.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.7" />
      <line x1="2.5" y1="10" x2="7" y2="10" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.7" />
      <line x1="13" y1="10" x2="17.5" y2="10" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.7" />
      <circle cx="10" cy="10" r="1" fill="currentColor" />
    </svg>
  );
}
function IconArmsTradeRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M3 10 L8 10 L9 8 L11 12 L12 10 L17 10" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="16" cy="7" r="1.5" fill="none" stroke="currentColor" strokeWidth="1.2" />
      <line x1="16" y1="8.5" x2="16" y2="10" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
      <path d="M4 13 L7 13 M4 15 L9 15" stroke="currentColor" strokeWidth="1" strokeLinecap="round" opacity="0.6" />
      <circle cx="10" cy="5" r="2" fill="none" stroke="currentColor" strokeWidth="1.2" />
      <line x1="10" y1="7" x2="10" y2="10" stroke="currentColor" strokeWidth="1" strokeLinecap="round" opacity="0.7" />
    </svg>
  );
}
function IconRacialDiscriminationRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <circle cx="10" cy="10" r="7.5" fill="none" stroke="currentColor" strokeWidth="1.4" />
      <circle cx="7" cy="8" r="1.5" fill="currentColor" opacity="0.9" />
      <circle cx="13" cy="8" r="1.5" fill="currentColor" opacity="0.6" />
      <path d="M6 13 Q10 15.5 14 13" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
      <line x1="10" y1="2.5" x2="10" y2="5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.7" />
      <line x1="10" y1="15" x2="10" y2="17.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" opacity="0.7" />
    </svg>
  );
}
function IconCorporateImpunityLegal({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 3 L14 5 L14 10 C14 13 12 15.5 10 16.5 C8 15.5 6 13 6 10 L6 5 Z" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
      <line x1="8" y1="9" x2="12" y2="9" stroke="currentColor" strokeWidth="1" strokeLinecap="round" opacity="0.7" />
      <path d="M8 11.5 L9.5 13 L12 10.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" opacity="0" />
      <line x1="8" y1="9" x2="8" y2="13" stroke="currentColor" strokeWidth="1" strokeLinecap="round" opacity="0.6" />
      <line x1="10" y1="7" x2="10" y2="13" stroke="currentColor" strokeWidth="1" strokeLinecap="round" opacity="0.6" />
      <line x1="12" y1="9" x2="12" y2="13" stroke="currentColor" strokeWidth="1" strokeLinecap="round" opacity="0.6" />
    </svg>
  );
}

function IconWaterAccessRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c-4.97 0-9 3.582-9 8 0 4.418 4.03 8 9 8s9-3.582 9-8c0-4.418-4.03-8-9-8zM6.75 12.75c0 1.864 2.349 3.75 5.25 3.75s5.25-1.886 5.25-3.75" />
    </svg>
  );
}

function IconIndigenousPeoplesRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
    </svg>
  );
}

function IconAcademicFreedomSuppression({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.627 48.627 0 0112 20.904a48.627 48.627 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 0110.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.697 50.697 0 0112 13.489a50.702 50.702 0 017.74-3.342M6.75 15a.75.75 0 100-1.5.75.75 0 000 1.5zm0 0v-3.675A55.378 55.378 0 0112 8.443m-7.007 11.55A5.981 5.981 0 006.75 15.75v-1.5" />
    </svg>
  );
}

function IconForcedMarriageRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2m0 0a4 4 0 110 8 4 4 0 010-8zm-6 9a6 6 0 1112 0v2H6v-2z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 17l-2 2m8-2l2 2" />
    </svg>
  );
}

function IconChildMarriageLabor({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4" />
    </svg>
  );
}

function IconClimateRefugeesRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 12h18M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9" />
    </svg>
  );
}

function IconTransgenderRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="12" cy="8" r="4" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 12v9M9 18h6M17 3l4 4m0 0l-4 4m4-4H15" />
    </svg>
  );
}

function IconHousingEvictionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 3l6 6M9 3l-6 6" />
    </svg>
  );
}

function IconFoodSovereigntyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c-4.97 0-9 3.582-9 8 0 3.314 2.504 6.129 6 7.478V21h6v-2.522c3.496-1.349 6-4.164 6-7.478 0-4.418-4.03-8-9-8z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6M12 9v6" />
    </svg>
  );
}
function IconCorporateImpunityRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}
function IconInternetAccessRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.288 15.038a5.25 5.25 0 017.424 0M5.106 11.856c3.807-3.808 9.98-3.808 13.788 0M1.924 8.674c5.565-5.565 14.587-5.565 20.152 0M12.53 18.22l-.53.53-.53-.53a.75.75 0 011.06 0z" />
    </svg>
  );
}
function IconMedicalDebtRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3m0 0v3m0-3h3m-3 0H9" />
    </svg>
  );
}
function IconCulturalHeritageRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253" />
    </svg>
  );
}
function IconWhistleblowerRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.34 15.84c-.688-.06-1.386-.09-2.09-.09H7.5a4.5 4.5 0 110-9h.75c.704 0 1.402-.03 2.09-.09m0 9.18c.253.962.584 1.892.985 2.783.247.55.06 1.21-.463 1.511l-.657.38c-.551.318-1.26.117-1.527-.461a20.845 20.845 0 01-1.44-4.282m3.102.069a18.03 18.03 0 01-.59-4.59c0-1.586.205-3.124.59-4.59m0 9.18a23.848 23.848 0 018.835 2.535M10.34 6.66a23.847 23.847 0 008.835-2.535m0 0A23.74 23.74 0 0018.795 3m.38 1.125a23.91 23.91 0 011.014 5.395m-1.014 8.855c-.118.38-.245.754-.38 1.125m.38-1.125a23.91 23.91 0 001.014-5.395m0-3.46c.495.413.811 1.035.811 1.73 0 .695-.316 1.317-.811 1.73m0-3.46a24.347 24.347 0 010 3.46" />
    </svg>
  );
}

function IconEnvironmentalRacismRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="14" width="18" height="7" rx="1" />
      <path d="M7 14V9a5 5 0 0 1 10 0v5" />
      <path d="M12 4v2" />
      <path d="M8 7l-2-2" />
      <path d="M16 7l2-2" />
      <path d="M5 17h14" />
    </svg>
  );
}

function IconChildPovertyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="8" r="3" />
      <path d="M9 21v-4a3 3 0 0 1 6 0v4" />
      <path d="M6 21H3a1 1 0 0 1-1-1v-2a4 4 0 0 1 4-4h1" />
      <path d="M18 21h3a1 1 0 0 0 1-1v-2a4 4 0 0 0-4-4h-1" />
    </svg>
  );
}

function IconTorturePreventionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2L4 6v6c0 5.25 3.5 9.74 8 11 4.5-1.26 8-5.75 8-11V6l-8-4z" />
      <path d="M9 12l2 2 4-4" />
    </svg>
  );
}

function IconFreedomAssemblyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="9" cy="7" r="2" />
      <circle cx="15" cy="7" r="2" />
      <path d="M6 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2" />
      <path d="M3 21v-1a3 3 0 0 1 3-3" />
      <path d="M21 21v-1a3 3 0 0 0-3-3" />
    </svg>
  );
}

function IconCorporateTaxEvasionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="2" y="7" width="20" height="14" rx="2" />
      <path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2" />
      <path d="M12 12v4" />
      <path d="M10 14h4" />
    </svg>
  );
}

function IconGenderPayGapRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2a5 5 0 1 0 0 10A5 5 0 0 0 12 2Z" />
      <path d="M12 12v10" />
      <path d="M9 15h6" />
      <path d="M9 19h6" />
      <path d="M3 7l3 3" />
      <path d="M21 7l-3 3" />
    </svg>
  );
}

function IconHealthcareAccessRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2Z" />
      <path d="M12 8v8" />
      <path d="M8 12h8" />
    </svg>
  );
}

function IconAntiCorruptionRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2L3 7v5c0 5.25 3.75 10.15 9 11.35C17.25 22.15 21 17.25 21 12V7L12 2Z" />
      <path d="M9 12l2 2 4-4" />
    </svg>
  );
}

function IconBirthRegistrationRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7Z" />
      <circle cx={12} cy={9} r={2.5} />
    </svg>
  );
}

function IconHumanitarianAccessRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2Z" />
      <path d="M12 8v4l3 3" />
      <path d="M8 12H4" />
    </svg>
  );
}

function IconJournalismSafetyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 4h16v12H4z" />
      <path d="M8 8h8" />
      <path d="M8 11h5" />
      <path d="M8 20l4-4 4 4" />
    </svg>
  );
}

function IconDigitalPrivacyRights({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x={3} y={11} width={18} height={11} rx={2} />
      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
      <circle cx={12} cy={16} r={1} />
    </svg>
  );
}

function IconPrisonConditionsRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <rect x={3} y={3} width={18} height={18} rx={2}/>
      <line x1={8} y1={3} x2={8} y2={21}/><line x1={12} y1={3} x2={12} y2={21}/>
      <line x1={16} y1={3} x2={16} y2={21}/>
    </svg>
  );
}
function IconQuantumSurveillanceRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
      <circle cx={12} cy={12} r={3}/>
      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83"/>
    </svg>
  );
}
function IconQuantumBioethicsRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path d="M12 22V12M12 12C12 6 6 2 6 2s0 6 6 10M12 12c0-6 6-10 6-10s0 6-6 10"/>
      <path d="M7 22h10"/>
    </svg>
  );
}
function IconQuantumDigitalDivideRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <rect x={2} y={3} width={20} height={14} rx={2}/>
      <path d="M8 21h8M12 17v4"/>
      <path d="M7 8h2M11 8h6M7 12h4M15 12h2"/>
    </svg>
  );
}
function IconChildMarriageRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <circle cx={9} cy={7} r={3}/><path d="M3 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2"/>
      <line x1={18} y1={8} x2={23} y2={13}/><line x1={23} y1={8} x2={18} y2={13}/>
    </svg>
  );
}
function IconFreedomExpressionRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      <line x1={9} y1={10} x2={15} y2={10}/>
    </svg>
  );
}
function IconSanitationHygieneRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path d="M4 12h16M4 6h16M4 18h16"/><circle cx={20} cy={6} r={2}/><circle cx={20} cy={18} r={2}/>
    </svg>
  );
}

function IconHumanTraffickingRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path d="M12 2a4 4 0 1 0 0 8 4 4 0 0 0 0-8z"/><path d="M6 20v-2a6 6 0 0 1 6-6h0a6 6 0 0 1 6 6v2"/><path d="M3 17l2-2 2 2"/><path d="M19 17l2-2 2 2"/>
    </svg>
  );
}

function IconRightToEducationRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
    </svg>
  );
}

function IconSocialSecurityRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
  );
}

function IconAsylumRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
      <polyline points="9 22 9 12 15 12 15 22"/>
    </svg>
  );
}

function IconIndigenousKnowledgeRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/>
      <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>
      <path d="M2 12h20"/>
    </svg>
  );
}

function IconGenderBasedViolenceRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="8" r="4"/>
      <path d="M12 12v8"/>
      <path d="M8 16h8"/>
      <path d="M9 21l3-3 3 3"/>
    </svg>
  );
}

function IconChildLaborRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
      <circle cx="9" cy="7" r="4"/>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    </svg>
  );
}

function IconTaxJusticeRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="5" width="20" height="14" rx="2"/>
      <line x1="2" y1="10" x2="22" y2="10"/>
      <path d="M6 15h.01M10 15h4"/>
    </svg>
  );
}

function IconRightToFairTrialRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
  );
}

function IconEnvironmentalPollutionRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z"/>
      <path d="M12 8v4"/>
      <path d="M12 16h.01"/>
    </svg>
  );
}

function IconCollectiveBargainingRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
      <circle cx="9" cy="7" r="4"/>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    </svg>
  );
}

function IconWomenPoliticalRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="8" r="4"/>
      <path d="M12 12v4"/>
      <path d="M9 16l3 3 3-3"/>
      <path d="M8 20h8"/>
    </svg>
  );
}

function IconClimateChangeRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
    </svg>
  );
}

function IconForcedSterilizationRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
    </svg>
  );
}

function IconStatelessChildrenRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
      <circle cx="9" cy="7" r="4"/>
      <line x1="17" y1="11" x2="23" y2="11"/>
    </svg>
  );
}

function IconHateSpeechIncitementRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      <line x1="9" y1="10" x2="15" y2="10"/>
    </svg>
  );
}

function IconLandRestitutionRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
      <polyline points="9 22 9 12 15 12 15 22"/>
      <path d="M12 7v5"/>
    </svg>
  );
}

function IconOrganHarvestingRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
      <line x1="12" y1="10" x2="12" y2="14"/>
    </svg>
  );
}

function IconRightToNationalityRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
      <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
    </svg>
  );
}

function IconInternetCensorshipRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/>
      <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
      <path d="M2 12h20M12 2a15.3 15.3 0 0 1 0 20"/>
    </svg>
  );
}

function IconMedicalExperimentationRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 3h6M9 3v6l-4 8a2 2 0 0 0 1.8 2.9h10.4A2 2 0 0 0 19 17l-4-8V3"/>
      <line x1="6.5" y1="14" x2="17.5" y2="14"/>
      <path d="M12 10v4M10 12h4"/>
    </svg>
  );
}

function IconEconomicSanctionsRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="11" width="18" height="10" rx="2"/>
      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
      <line x1="2" y1="7" x2="22" y2="17"/>
      <circle cx="12" cy="16" r="1" fill="currentColor"/>
    </svg>
  );
}

function IconSolitaryConfinementRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="1"/>
      <line x1="7" y1="3" x2="7" y2="21"/>
      <line x1="11" y1="3" x2="11" y2="21"/>
      <line x1="15" y1="3" x2="15" y2="21"/>
      <circle cx="19" cy="12" r="1.5" fill="currentColor"/>
    </svg>
  );
}

function IconNetNeutralityRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <line x1="2" y1="6" x2="22" y2="6"/>
      <line x1="2" y1="12" x2="22" y2="12"/>
      <line x1="2" y1="18" x2="22" y2="18"/>
      <circle cx="6" cy="6" r="1.5" fill="currentColor"/>
      <circle cx="12" cy="12" r="1.5" fill="currentColor"/>
      <circle cx="18" cy="18" r="1.5" fill="currentColor"/>
      <line x1="6" y1="6" x2="6" y2="18"/>
    </svg>
  );
}

function IconRightToBeForgottenRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2L4 7v5c0 4.418 3.134 8.545 8 9.5 4.866-.955 8-5.082 8-9.5V7l-8-5z"/>
      <line x1="9" y1="9" x2="15" y2="15"/>
      <line x1="15" y1="9" x2="9" y2="15"/>
    </svg>
  );
}

function IconDigitalAccessibilityRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="4" r="1.5"/>
      <path d="M8 8h8l-1 5h-6L8 8z"/>
      <line x1="12" y1="13" x2="12" y2="20"/>
      <line x1="9" y1="20" x2="15" y2="20"/>
      <rect x="3" y="14" width="5" height="4" rx="1"/>
      <rect x="16" y="14" width="5" height="4" rx="1"/>
    </svg>
  );
}

function IconFreedomOfAssemblyRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 18c0-3 2-5 5-5h8c3 0 5 2 5 5"/>
      <circle cx="12" cy="7" r="3"/>
      <path d="M17 3l1 2-1 2"/>
      <path d="M19 5h3"/>
      <path d="M7 3l-1 2 1 2"/>
      <path d="M5 5H2"/>
    </svg>
  );
}

function IconRightToHousingRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 10.5L12 3l9 7.5"/>
      <path d="M5 9v11h14V9"/>
      <rect x="9" y="14" width="6" height="6"/>
      <path d="M9 14v6"/>
    </svg>
  );
}

function IconJuvenileJusticeRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="5" r="2"/>
      <path d="M12 7v5"/>
      <line x1="8" y1="21" x2="16" y2="21"/>
      <line x1="12" y1="9" x2="8" y2="21"/>
      <line x1="12" y1="9" x2="16" y2="21"/>
      <path d="M6 13h3.5M14.5 13H18"/>
      <path d="M6 13l2-3M18 13l-2-3"/>
    </svg>
  );
}

function IconArmsTradeHumanRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 12h10"/>
      <path d="M13 9l4 3-4 3"/>
      <path d="M17 12h2a2 2 0 0 0 2-2V8"/>
      <path d="M19 8l-2-2"/>
      <circle cx="6" cy="12" r="1.5"/>
      <path d="M10 7l1-3 2 1"/>
    </svg>
  );
}

function IconRightToTruthRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <circle cx="11" cy="11" r="7"/>
      <line x1="16.5" y1="16.5" x2="21" y2="21"/>
      <path d="M8 11h6"/>
      <path d="M11 8v6"/>
    </svg>
  );
}

function IconBiometricDataRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2C8.5 2 6 4.5 6 8c0 5 6 12 6 12s6-7 6-12c0-3.5-2.5-6-6-6z"/>
      <circle cx="12" cy="8" r="2"/>
      <path d="M9 8c0-1.7 1.3-3 3-3s3 1.3 3 3"/>
    </svg>
  );
}

function IconAntiCorruptionHumanRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 3l2 4h4l-3 3 1 4-4-2-4 2 1-4-3-3h4z"/>
      <line x1="18" y1="6" x2="22" y2="2"/>
      <line x1="20" y1="2" x2="22" y2="4"/>
      <path d="M3 21h8M7 21v-4"/>
      <path d="M14 21h7M17.5 21v-3"/>
    </svg>
  );
}

function IconWomenEconomicRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <circle cx="9" cy="5" r="2"/>
      <path d="M9 7v5M7 9h4"/>
      <path d="M9 12v3"/>
      <path d="M7 15h4"/>
      <polyline points="3,20 7,16 11,18 15,13 19,15 22,11"/>
      <polyline points="19,11 22,11 22,14"/>
    </svg>
  );
}

function IconDisabilityRightsCrpd({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="4" r="1.5"/>
      <path d="M9 8h4l1 4-3 1"/>
      <path d="M10 12l-1 5h6"/>
      <path d="M14 17l1 3"/>
      <path d="M11 22l-1-5"/>
      <path d="M17 10l1.5 5"/>
      <path d="M12 17c-2.8 0-5-2.2-5-5 0-1.5.7-2.9 1.7-3.8"/>
      <path d="M19 12a7 7 0 0 1-7 7"/>
    </svg>
  );
}

function IconRightToWorkRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="11" width="20" height="11" rx="2"/>
      <path d="M16 11V7a4 4 0 0 0-8 0v4"/>
      <path d="M12 15v3"/>
      <path d="M9 18h6"/>
    </svg>
  );
}

function IconOnlineHarassmentRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      <path d="M12 8v4"/>
      <path d="M12 16h.01"/>
    </svg>
  );
}

function IconRightToPrivacyRights({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
      <path d="M2 2l20 20"/>
      <path d="M10.5 10.5A4.95 4.95 0 0 1 12 10a5 5 0 0 1 4.95 4.35"/>
    </svg>
  );
}

function IconReligiousMinorityRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 2a2 2 0 011.6.8L17 7h3a1 1 0 01.8 1.6L18 12l2.8 3.4A1 1 0 0120 17h-3l-3.4 4.2A2 2 0 0112 22a2 2 0 01-1.6-.8L7 17H4a1 1 0 01-.8-1.6L6 12 3.2 8.6A1 1 0 014 7h3l3.4-4.2A2 2 0 0112 2z" />
    </svg>
  );
}

function IconRightToFoodRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3C8 3 4 7 4 12s4 9 8 9 8-4 8-9-4-9-8-9zm0 4v10M9 9c0-2 1.5-3 3-3s3 1 3 3" />
    </svg>
  );
}

function IconExtrajudicialKillingRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
    </svg>
  );
}

function IconCyberEspionageRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
    </svg>
  );
}

function IconRacismSystemicRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
    </svg>
  );
}

function IconClimateDisplacementRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
    </svg>
  );
}

function IconCasteDiscriminationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
    </svg>
  );
}

function IconIndigenousLanguageRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 21l5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 016-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 01-3.827-5.802" />
    </svg>
  );
}

function IconDigitalAuthoritarianismRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
    </svg>
  );
}

function IconHousingDiscriminationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
    </svg>
  );
}

function IconForcedLaborSupplyChainRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244" />
    </svg>
  );
}

function IconDeepfakeRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
    </svg>
  );
}

function IconOrganTraffickingRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
    </svg>
  );
}

function IconRightToStrikeRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.042 21.672L13.684 16.6m0 0l-2.51 2.225.569-9.47 5.227 7.917-3.286-.672zm-7.518-.267A8.25 8.25 0 1120.25 10.5M8.288 14.212A5.25 5.25 0 1117.25 10.5" />
    </svg>
  );
}

function IconJournalistProtectionRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 01-2.25 2.25M16.5 7.5V18a2.25 2.25 0 002.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 002.25 2.25h13.5M6 7.5h3v3H6v-3z" />
    </svg>
  );
}

function IconAntiMoneyLaunderingRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
    </svg>
  );
}

function IconSexualViolenceConflictRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}

function IconAlgorithmicDiscriminationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 3.75H6.912a2.25 2.25 0 00-2.15 1.588L2.35 13.177a2.25 2.25 0 00-.1.661V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 00-2.15-1.588H15M2.25 13.5h3.86a2.25 2.25 0 012.012 1.244l.256.512a2.25 2.25 0 002.013 1.244h3.218a2.25 2.25 0 002.013-1.244l.256-.512a2.25 2.25 0 012.013-1.244h3.859M12 3v8.25m0 0l-3-3m3 3l3-3" />
    </svg>
  );
}

function IconNuclearTestingRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
    </svg>
  );
}

function IconPoliticalPrisonerRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
    </svg>
  );
}

function IconSanctionsCivilianRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
    </svg>
  );
}

function IconRightToScienceRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
    </svg>
  );
}

function IconIndigenousSelfDeterminationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21" />
    </svg>
  );
}

function IconEcocideRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9-4.03-9-9-9zm0 0v9m0-9c2.21 0 4 3.582 4 8m-4-8c-2.21 0-4 3.582-4 8m4 0H3m9 0h9" />
    </svg>
  );
}

function IconPlatformWorkersRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 8.25h3m-3 3.75h3m-6-3.75H6.75m3.75 3.75H6.75" />
    </svg>
  );
}

function IconRightToWaterRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3.75v16.5M2.25 12h19.5M6.375 17.25a4.875 4.875 0 004.875-4.875V12m6.375 5.25a4.875 4.875 0 01-4.875-4.875V12m-9 8.25h16.5a1.5 1.5 0 001.5-1.5V5.25a1.5 1.5 0 00-1.5-1.5H3.75a1.5 1.5 0 00-1.5 1.5v13.5a1.5 1.5 0 001.5 1.5zm12.621-9.44c-1.409 1.41-4.242 1.061-4.242 1.061s-.349-2.833 1.06-4.242a2.25 2.25 0 013.182 3.182zM10.773 7.63c1.409 1.409 1.06 4.242 1.06 4.242S9 12.22 7.592 10.811a2.25 2.25 0 013.182-3.182z" />
    </svg>
  );
}

function IconLandMineVictimsRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
    </svg>
  );
}

function IconStatelessAdultRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 9h3.75M15 12h3.75M15 15h3.75M4.5 19.5h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5zm6-10.125a1.875 1.875 0 11-3.75 0 1.875 1.875 0 013.75 0zm1.294 6.336a6.721 6.721 0 01-3.17.789 6.721 6.721 0 01-3.168-.789 3.376 3.376 0 016.338 0z" />
    </svg>
  );
}

function IconArmedGroupRecruitmentRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}

function IconRightToDevelopmentRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
    </svg>
  );
}
function IconCulturalAppropriationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
    </svg>
  );
}
function IconHateSpeechOnlineRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
    </svg>
  );
}
function IconMassIncarcerationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21" />
    </svg>
  );
}

function IconColonialGenocideRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
    </svg>
  );
}

function IconDigitalDivideRuralRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.288 15.038a5.25 5.25 0 017.424 0M5.106 11.856c3.807-3.808 9.98-3.808 13.788 0M1.924 8.674c5.565-5.565 14.587-5.565 20.152 0M12.53 18.22l-.53.53-.53-.53a.75.75 0 011.06 0z" />
    </svg>
  );
}

function IconRefugeeIntegrationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
    </svg>
  );
}

function IconAiWeaponsRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
    </svg>
  );
}

function IconWaterConflictRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
    </svg>
  );
}

function IconSupplyChainTransparencyRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244" />
    </svg>
  );
}

function IconPostConflictReconstructionRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
    </svg>
  );
}

function IconClimateFinanceRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}

function IconRightToPeaceRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9-4.03-9-9-9zm0 0v18M3.6 9h16.8M3.6 15h16.8" />
    </svg>
  );
}

function IconGenderJusticeRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9-4.03-9-9-9zm0 14.25V12m0 0V6.75M12 12l4.5-4.5M12 12l-4.5-4.5" />
    </svg>
  );
}

function IconCommunityLandRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 6.75V15m6-6v8.25m.503 3.498l4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 00-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0z" />
    </svg>
  );
}

function IconMigrationGovernanceRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
    </svg>
  );
}

function IconRightToLeisureRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1m8-9h1M3 12H2m15.364-6.364.707.707M5.636 18.364l-.707.707M18.364 18.364l.707.707M5.636 5.636l-.707.707M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z" />
    </svg>
  );
}

function IconSocialProtectionRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
    </svg>
  );
}

function IconPrisonReformRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25z" />
    </svg>
  );
}

function IconCorporateAccountabilityRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z" />
    </svg>
  );
}

function IconEthnicCleansingRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}

function IconSpeechSurveillanceRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3z" />
    </svg>
  );
}

function IconLethalAutonomousWeaponsRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.362 5.214A8.252 8.252 0 0 1 12 21 8.25 8.25 0 0 1 6.038 7.047 8.287 8.287 0 0 0 9 9.601a8.983 8.983 0 0 1 3.361-6.867 8.21 8.21 0 0 0 3 2.48z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 18a3.75 3.75 0 0 0 .495-7.468 5.99 5.99 0 0 0-1.925 3.547 5.975 5.975 0 0 1-2.133-1.001A3.75 3.75 0 0 0 12 18z" />
    </svg>
  );
}

function IconProtestCriminalizationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0z" />
    </svg>
  );
}

function IconCobaltMiningRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6.429 9.75 2.25 12l4.179 2.25m0-4.5 5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0 4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0-5.571 3-5.571-3" />
    </svg>
  );
}

function IconCognitiveLibertyRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09zM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456zM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423z" />
    </svg>
  );
}

function IconRightToRepairRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M11.42 15.17 17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l5.654-4.654m5.65-4.654 3.029-2.498a1.875 1.875 0 0 1 2.582.14l.036.036a1.875 1.875 0 0 1 .14 2.582l-2.497 3.03m-6.321 4.484-1.43-1.43m6.321-4.484L17.25 6.75" />
    </svg>
  );
}

function IconNeuroethicsRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
    </svg>
  );
}

function IconSlappSuitRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0 0 12 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 0 1-2.031.352 5.988 5.988 0 0 1-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971Zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 0 1-2.031.352 5.989 5.989 0 0 1-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971Z" />
    </svg>
  );
}

function IconConversionTherapyRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
    </svg>
  );
}

function IconLgbtqCriminalizationRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 3l1.664 1.664M21 21l-1.5-1.5m-5.485-1.242L12 17.25 4.5 21V8.742m.164-4.078a2.15 2.15 0 0 1 1.743-1.342 48.507 48.507 0 0 1 11.186 0c1.1.128 1.907 1.077 1.907 2.185V19.5M4.664 4.664 19.5 19.5" />
    </svg>
  );
}

function IconFemicideAccountabilityRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m0-10.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.75c0 5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.57-.598-3.75h-.152c-3.196 0-6.1-1.25-8.25-3.286zm0 13.036h.008v.008H12v-.008z" />
    </svg>
  );
}

function IconStreetHarassmentRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0zM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
    </svg>
  );
}

function IconReproductiveCoercionRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z" />
    </svg>
  );
}

function IconEconomicAbuseRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18.75a60.07 60.07 0 0 1 15.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 0 1 3 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 0 0-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 0 1-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 0 0 3 15h-.75M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
    </svg>
  );
}

function IconMentalHealthDetentionRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.625 9.75a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 0 1 .778-.332 48.294 48.294 0 0 0 5.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" />
    </svg>
  );
}

function IconPsychiatricAbuseRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z" />
    </svg>
  );
}

function IconElderFinancialAbuseRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z" />
    </svg>
  );
}

function IconDigitalDivideRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.288 15.038a5.25 5.25 0 0 1 7.424 0M5.106 11.856c3.807-3.808 9.98-3.808 13.788 0M1.924 8.674c5.565-5.565 14.587-5.565 20.152 0M12.53 18.22l-.53.53-.53-.53a.75.75 0 0 1 1.06 0z" />
    </svg>
  );
}

function IconOnlineViolenceWomenRights({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0zm-9 3.75h.008v.008H12v-.008z" />
    </svg>
  );
}

function IconLandPollutionRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#84cc16" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2L2 7l10 5 10-5-10-5z" />
      <path d="M2 17l10 5 10-5" />
      <path d="M2 12l10 5 10-5" />
    </svg>
  );
}

function IconAirQualityRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#0ea5e9" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2" />
    </svg>
  );
}

function IconEndocrineDisruptorRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#a16207" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
      <line x1="12" y1="9" x2="12" y2="13" />
      <line x1="12" y1="17" x2="12.01" y2="17" />
    </svg>
  );
}

function IconFoodDesertRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M3 11l19-9-9 19-2-8-8-2z" />
    </svg>
  );
}

function IconOceanRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#0369a1" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1" />
      <path d="M2 12c.6.5 1.2 1 2.5 1C7 13 7 11 9.5 11c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1" />
      <path d="M2 18c.6.5 1.2 1 2.5 1C7 19 7 17 9.5 17c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1" />
    </svg>
  );
}

function IconToxicWasteDumpingRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#dc2626" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="12" cy="12" r="10" />
      <path d="M4.93 4.93l14.14 14.14" />
    </svg>
  );
}

function IconBiopiacyRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
  );
}

function IconConflictMineralRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#f59e0b" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
  );
}

function IconForcedRelocationRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#6b7280" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
    </svg>
  );
}

function IconWaterPrivatizationRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#06b6d4" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" />
    </svg>
  );
}

function IconSexualExploitationSupplyChainRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#be185d" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  );
}

function IconPesticideExposureRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#16a34a" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 22V12M12 12C12 12 7 9 7 4h10c0 5-5 8-5 8z" />
      <path d="M7 4C7 4 4 6 4 10" />
      <path d="M17 4C17 4 20 6 20 10" />
    </svg>
  );
}

function IconGarmentWorkerRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#e11d48" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M20.38 3.46L16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.57a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.57a2 2 0 0 0-1.34-2.23z" />
    </svg>
  );
}

function IconDeforestationRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#15803d" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M17 8C8 10 5.9 16.17 3.82 22H5c1-4 3-6 6-6 0 0-3.27-3.86 0-8 1.45-1.82 4-3 7-3s5.55 1.18 7 3c3.27 4.14 0 8 0 8 3 0 5 2 6 6h1.18C23.1 16.17 21 10 17 8z" />
    </svg>
  );
}

function IconMicaMiningRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#d97706" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M6 3h12l4 6-10 13L2 9z" />
      <path d="M11 3L8 9l4 13 4-13-3-6" />
      <path d="M2 9h20" />
    </svg>
  );
}

function IconClimateDisplacementRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#0284c7" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
      <path d="M9 22V12h6v10" />
      <path d="M12 7v1" />
    </svg>
  );
}

function IconIndigenousCulturalHeritageRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#7c2d12" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2L2 19h20L12 2z" />
      <path d="M12 7v6" />
      <circle cx="12" cy="17" r="1" fill="#7c2d12" />
    </svg>
  );
}

function IconDeepSeaMiningRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#1e3a8a" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M2 12h20" />
      <path d="M12 2v20" />
      <circle cx="12" cy="12" r="4" />
      <path d="M12 16v6" />
    </svg>
  );
}

function IconFastFashionRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#ec4899" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M20.38 3.46L16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.57a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.57a2 2 0 0 0-1.34-2.23z" />
    </svg>
  );
}

function IconWageTheftRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#b91c1c" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <line x1="12" y1="1" x2="12" y2="23" />
      <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
    </svg>
  );
}

function IconDroneSurveillanceRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#4338ca" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="12" cy="12" r="2" />
      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
      <path d="M2 12h20" />
    </svg>
  );
}

function IconPlasticPollutionRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#0891b2" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1" />
      <path d="M2 12c.6.5 1.2 1 2.5 1C7 13 7 11 9.5 11c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1" />
      <path d="M2 18c.6.5 1.2 1 2.5 1C7 19 7 17 9.5 17c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1" />
    </svg>
  );
}

function IconHeatStressLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#ea580c" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2v8" />
      <path d="m4.93 10.93 1.41 1.41" />
      <path d="M2 18h2" />
      <path d="M20 18h2" />
      <path d="m19.07 10.93-1.41 1.41" />
      <path d="M22 22H2" />
      <path d="m16 6-4 4-4-4" />
      <path d="M16 18a4 4 0 0 0-8 0" />
    </svg>
  );
}

function IconLithiumMiningRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#7e22ce" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
      <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
    </svg>
  );
}

function IconNuclearWasteRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#854d0e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="12" cy="12" r="10" />
      <circle cx="12" cy="12" r="2" />
      <path d="M12 2a10 10 0 0 1 8.66 5" />
      <path d="M12 2a10 10 0 0 0-8.66 5" />
      <path d="M12 22v-4" />
    </svg>
  );
}

function IconMigrantDomesticWorkerRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#0e7490" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
      <path d="M20 4l-8 4-8-4" />
    </svg>
  );
}

function IconPlatformWorkerRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#0369a1" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
      <line x1="8" y1="21" x2="16" y2="21" />
      <line x1="12" y1="17" x2="12" y2="21" />
    </svg>
  );
}

function IconRareEarthMiningRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#a16207" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="12" cy="12" r="3" />
      <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83" />
    </svg>
  );
}

function IconAgriculturalChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#15803d" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
      <path d="M9 12l2 2 4-4" />
    </svg>
  );
}

function IconZeroHourContractRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="12" cy="12" r="10" />
      <polyline points="12 6 12 12 16 14" />
    </svg>
  );
}

function IconNickelMiningRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#b45309" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M2 20h20" />
      <path d="M6 20V10l6-7 6 7v10" />
      <path d="M9 20v-5h6v5" />
    </svg>
  );
}

function IconColtanMiningRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#1d4ed8" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <rect x="2" y="7" width="20" height="14" rx="2" />
      <path d="M6 7V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v2" />
      <line x1="12" y1="12" x2="12" y2="16" />
      <line x1="9" y1="14" x2="15" y2="14" />
    </svg>
  );
}
function IconWhistleblowerProtectionRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#0f766e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M3 11l19-9-9 19-2-8-8-2z" />
    </svg>
  );
}
function IconEWasteRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#7c3aed" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <rect x="2" y="3" width="20" height="14" rx="2" />
      <path d="M8 21h8" />
      <path d="M12 17v4" />
      <path d="M9 10l6 0" />
      <path d="M12 7v6" />
    </svg>
  );
}
function IconSandMiningRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#b45309" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M2 20h20" />
      <path d="M6 20V10l4-6h4l4 6v10" />
      <path d="M10 20v-6h4v6" />
    </svg>
  );
}
function IconIvoryTradePoachinRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#78350f" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M7 3c0 8 4 13 9 13" />
      <path d="M17 3c0 8-4 13-9 13" />
    </svg>
  );
}
function IconGarmentFactoryFireRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#dc2626" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <rect x="3" y="10" width="18" height="11" rx="1" />
      <path d="M9 10V7h6v3" />
      <path d="M12 14c0-2 2-3 2-5" />
      <path d="M9 14c0-2 2-3 2-5" />
    </svg>
  );
}
function IconChildBrideEarlyMarriageRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#9333ea" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="12" cy="12" r="7" />
      <line x1="9" y1="9" x2="15" y2="15" />
      <line x1="15" y1="9" x2="9" y2="15" />
    </svg>
  );
}

function IconAsbestosSilicosisOccupationalRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#475569" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2C8 2 5 6 5 10c0 3 1 5 3 7l2 3h4l2-3c2-2 3-4 3-7 0-4-3-8-7-8z" />
      <circle cx="9" cy="9" r="1" fill="#475569" />
      <circle cx="15" cy="9" r="1" fill="#475569" />
      <circle cx="12" cy="13" r="1" fill="#475569" />
    </svg>
  );
}

function IconClusterBombCivilianHarmRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#b91c1c" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="12" cy="12" r="4" />
      <line x1="12" y1="2" x2="12" y2="6" />
      <line x1="12" y1="18" x2="12" y2="22" />
      <line x1="2" y1="12" x2="6" y2="12" />
      <line x1="18" y1="12" x2="22" y2="12" />
      <line x1="5" y1="5" x2="8" y2="8" />
      <line x1="16" y1="16" x2="19" y2="19" />
      <line x1="19" y1="5" x2="16" y2="8" />
      <line x1="8" y1="16" x2="5" y2="19" />
    </svg>
  );
}

function IconMicaChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#92400e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <polygon points="12,2 20,18 4,18" />
      <line x1="12" y1="10" x2="12" y2="14" />
      <circle cx="17" cy="8" r="2" />
      <line x1="17" y1="10" x2="17" y2="15" />
      <line x1="15" y1="12" x2="19" y2="12" />
    </svg>
  );
}

function IconTungstenConflictMiningRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#374151" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <rect x="3" y="8" width="18" height="10" rx="2" />
      <line x1="12" y1="3" x2="12" y2="8" />
      <line x1="9" y1="3" x2="15" y2="3" />
      <line x1="9" y1="13" x2="15" y2="13" />
      <line x1="12" y1="10" x2="12" y2="16" />
    </svg>
  );
}

function IconTinMiningArtisanalRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#6b7280" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <line x1="14" y1="4" x2="20" y2="10" />
      <line x1="4" y1="14" x2="10" y2="20" />
      <line x1="4" y1="14" x2="14" y2="4" />
      <circle cx="12" cy="12" r="2" />
      <line x1="3" y1="21" x2="7" y2="17" />
    </svg>
  );
}

function IconTantalumConflictMineralsRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#1e40af" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <rect x="2" y="4" width="20" height="16" rx="2" />
      <line x1="6" y1="8" x2="10" y2="8" />
      <line x1="6" y1="12" x2="9" y2="12" />
      <line x1="6" y1="16" x2="8" y2="16" />
      <polygon points="17,7 19,11 15,11" />
      <line x1="17" y1="12" x2="17" y2="14" />
    </svg>
  );
}
function IconLeatherTanneryChromiumRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#7c3aed" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <rect x="3" y="6" width="18" height="12" rx="2" />
      <circle cx="12" cy="12" r="3" />
      <line x1="12" y1="9" x2="12" y2="6" />
      <line x1="12" y1="15" x2="12" y2="18" />
    </svg>
  );
}
function IconBrickKilnBondedLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#c2410c" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <rect x="2" y="10" width="9" height="5" rx="1" />
      <rect x="13" y="10" width="9" height="5" rx="1" />
      <line x1="11" y1="12" x2="13" y2="12" />
      <rect x="5" y="4" width="14" height="5" rx="1" />
    </svg>
  );
}
function IconCamelJockeyChildRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#b45309" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M3 17 Q8 10 14 12 Q18 13 21 17" />
      <circle cx="17" cy="7" r="2" />
      <line x1="17" y1="9" x2="16" y2="12" />
    </svg>
  );
}

function IconTobaccoChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#7f1d1d" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2c-4 3-6 7-5 12" />
      <path d="M12 2c4 3 6 7 5 12" />
      <line x1="7" y1="14" x2="17" y2="14" />
      <circle cx="12" cy="18" r="2" />
    </svg>
  );
}

function IconShrimpFishingForcedLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#0c4a6e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M3 17 Q7 14 12 15 Q17 16 21 13" />
      <path d="M6 17 L4 21" />
      <path d="M18 13 L20 9" />
      <path d="M8 19 L10 19 L10 21 L8 21 Z" />
      <path d="M14 11 Q16 9 14 7 Q12 9 14 11" />
    </svg>
  );
}

function IconArtisanalGoldMercuryRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#713f12" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M8 16 L5 19 L8 22 L11 19 L8 16 Z" />
      <path d="M8 10 Q10 7 13 9 Q11 12 8 10 Z" />
      <text x="13" y="8" fontSize="6" stroke="#713f12" strokeWidth={1} fill="#713f12">Hg</text>
      <circle cx="17" cy="15" r="3" />
      <line x1="17" y1="12" x2="17" y2="8" />
    </svg>
  );
}

function IconSugarcaneLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#166534" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <line x1="12" y1="2" x2="12" y2="18" />
      <line x1="8" y1="6" x2="12" y2="4" />
      <line x1="8" y1="10" x2="12" y2="8" />
      <line x1="8" y1="14" x2="12" y2="12" />
      <path d="M8 20l8-4" />
    </svg>
  );
}

function IconPalmOilPeatlandRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#92400e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <line x1="12" y1="20" x2="12" y2="10" />
      <path d="M12 10 Q8 6 5 8" />
      <path d="M12 10 Q16 6 19 8" />
      <path d="M12 13 Q9 10 7 11" />
      <path d="M12 13 Q15 10 17 11" />
      <path d="M6 20 Q8 17 10 18" />
      <path d="M10 18 Q11 16 12 17" />
    </svg>
  );
}

function IconMatchstickChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#b91c1c" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <line x1="12" y1="22" x2="12" y2="8" />
      <circle cx="12" cy="6" r="2" />
      <path d="M10 4 Q12 1 14 4" />
      <circle cx="7" cy="18" r="2" />
      <line x1="7" y1="16" x2="7" y2="12" />
      <line x1="5" y1="14" x2="9" y2="14" />
    </svg>
  );
}

function IconUraniumMiningIndigenousRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#f59e0b" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="12" cy="12" r="3" />
      <ellipse cx="12" cy="12" rx="10" ry="4" />
      <ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)" />
      <ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)" />
    </svg>
  );
}

function IconBloodDiamondConflictMineralRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#dc2626" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M6 3 L2 9 L12 21 L22 9 L18 3 Z" />
      <path d="M2 9 L12 9 L22 9" />
      <path d="M6 3 L12 9 L18 3" />
      <path d="M9 15 Q10 17 9 19" />
      <path d="M13 13 Q14 15 13 17" />
    </svg>
  );
}

function IconIllegalFishingForcedLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#0369a1" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M3 17 L7 13 L13 13 L21 17 L21 19 L3 19 Z" />
      <path d="M7 13 L7 9 L15 9 L15 13" />
      <line x1="11" y1="9" x2="11" y2="5" />
      <path d="M8 5 L11 5 L14 5" />
      <path d="M5 20 Q6 22 7 20 Q8 22 9 20" />
      <path d="M14 17 L16 15 L18 17 L16 19 Z" />
    </svg>
  );
}

function IconTigerBoneTraditionalMedicineRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#92400e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M3 12c0-5 3-9 9-9s9 4 9 9" />
      <path d="M6 15c1-2 3-3 6-3s5 1 6 3" />
      <line x1="8" y1="10" x2="8" y2="12" />
      <line x1="16" y1="10" x2="16" y2="12" />
    </svg>
  );
}

function IconSharkFinFinningRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#1e40af" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M2 18 Q6 18 9 10 L14 18 Z" />
      <line x1="2" y1="18" x2="22" y2="18" />
      <path d="M14 18 Q17 16 20 18" />
    </svg>
  );
}

function IconIllegalHardwoodLoggingRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#166534" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <rect x="4" y="14" width="10" height="6" rx="1" />
      <line x1="9" y1="14" x2="9" y2="20" />
      <line x1="6" y1="17" x2="12" y2="17" />
      <path d="M14 16 L20 10" />
      <path d="M17 7 L21 11 L19 13 L15 9 Z" />
      <line x1="4" y1="14" x2="9" y2="4" />
    </svg>
  );
}

function IconBearBileFarmingRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#78350f" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="12" cy="8" r="4" />
      <path d="M8 12c-2 1-4 3-4 6h16c0-3-2-5-4-6" />
      <path d="M10 16l2 4 2-4" />
    </svg>
  );
}

function IconRhinocerosHornPoachinRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#166534" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M4 18c0-4 3-7 8-7s8 3 8 7" />
      <path d="M12 11V4l4 5" />
      <circle cx="12" cy="18" r="1" />
    </svg>
  );
}

function IconCocoaChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#92400e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <ellipse cx="12" cy="12" rx="5" ry="8" />
      <path d="M12 4V2" />
      <path d="M9 8l-3-2" />
      <path d="M15 8l3-2" />
      <circle cx="12" cy="19" r="2" />
    </svg>
  );
}

function IconCoffeeLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#78350f" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M18 8h1a4 4 0 0 1 0 8h-1" />
      <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z" />
      <line x1="6" y1="1" x2="6" y2="4" />
      <line x1="10" y1="1" x2="10" y2="4" />
      <line x1="14" y1="1" x2="14" y2="4" />
    </svg>
  );
}

function IconVanillaChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#92400e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2C8 2 5 7 5 12s3 10 7 10 7-5 7-10S16 2 12 2z" />
      <path d="M12 2v20" />
      <path d="M5 12h14" />
    </svg>
  );
}

function IconRubberPlantationLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#166534" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 22V10" />
      <path d="M12 10C12 10 8 8 6 4c4 0 6 2 6 6z" />
      <path d="M12 10C12 10 16 8 18 4c-4 0-6 2-6 6z" />
      <path d="M8 18c1-1 2-2 4-2s3 1 4 2" />
    </svg>
  );
}

function IconCottonChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#d97706" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="12" cy="8" r="4" />
      <path d="M8 8c-2-2-3-5-1-7" />
      <path d="M16 8c2-2 3-5 1-7" />
      <path d="M12 12v4" />
      <path d="M10 16l2 4 2-4" />
    </svg>
  );
}

function IconTeaWorkerRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#166534" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M17 8C8 10 5.9 16.17 3.82 22" />
      <path d="M9 8.27C10.65 8 12.37 8 14 9c2 1.2 2.5 3.5 2 5.5" />
      <path d="M12 18c-2 1-4 1-6 0" />
    </svg>
  );
}

function IconCutFlowerLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#be185d" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 22V12" />
      <path d="M12 12c0 0-4-2-4-6 2 0 4 2 4 6z" />
      <path d="M12 12c0 0 4-2 4-6-2 0-4 2-4 6z" />
      <circle cx="12" cy="7" r="2" />
      <path d="M8 20h8" />
    </svg>
  );
}

function IconSoyFarmingDeforestationRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#166534" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M17 10c0 4-5 9-5 9S7 14 7 10a5 5 0 0 1 10 0z" />
      <path d="M3 21l4-4" />
      <path d="M3 17l2 2" />
      <path d="M7 21l-2-2" />
    </svg>
  );
}

function IconAvocadoWaterTheftRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#16a34a" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2C8 2 5 6 5 11c0 4 3.5 7 7 7s7-3 7-7c0-5-3-9-7-9z" />
      <circle cx="12" cy="12" r="2" />
      <path d="M19 3l-3 3" />
      <path d="M21 6l-2-2" />
      <path d="M16 2l1 3" />
    </svg>
  );
}

function IconQuinoaLandGrabRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#92400e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2v10" />
      <path d="M9 5c0 0-2 1-2 3h6c0-2-2-3-4-3z" />
      <path d="M10 8c0 0-2 1-2 3h8c0-2-2-3-6-3z" />
      <path d="M3 20h18" />
      <path d="M5 20v-4h14v4" />
    </svg>
  );
}

function IconBananaPesticidePoisoningRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#eab308" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2C7 2 4 6 4 10c0 5 4 8 8 10 4-2 8-5 8-10 0-4-3-8-8-8z" />
      <path d="M12 7v5" />
      <circle cx="12" cy="15" r="1" />
    </svg>
  );
}

function IconGrapeHarvestLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#7c3aed" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="9" cy="11" r="2" />
      <circle cx="15" cy="11" r="2" />
      <circle cx="12" cy="15" r="2" />
      <circle cx="9" cy="7" r="2" />
      <circle cx="15" cy="7" r="2" />
      <path d="M12 3c2 0 3 1 3 2" />
    </svg>
  );
}

function IconSeafoodSupplyChainRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#0369a1" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M2 12c2-4 6-6 10-6s8 2 10 6c-2 4-6 6-10 6S4 16 2 12z" />
      <circle cx="12" cy="12" r="2" />
      <path d="M20 12l2 2-2 2" />
      <path d="M4 12L2 10l2-2" />
    </svg>
  );
}

function IconSheaButterLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#92400e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2c-4 0-7 3-7 7 0 5 7 13 7 13s7-8 7-13c0-4-3-7-7-7z" />
      <circle cx="12" cy="9" r="2" />
    </svg>
  );
}

function IconCashewChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#d97706" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 3c-3 0-6 2-7 6 1 2 3 4 7 4s6-2 7-4c-1-4-4-6-7-6z" />
      <path d="M12 13v5" />
      <path d="M8 16l4 4 4-4" />
    </svg>
  );
}

function IconMangoLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#b45309" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 20c-4 0-8-4-8-9 0-4 2-7 5-8l1-2h4l1 2c3 1 5 4 5 8 0 5-4 9-8 9z" />
      <path d="M12 2v3" />
      <path d="M9 4c1 1 2 2 3 3" />
    </svg>
  );
}

function IconJuteChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#92400e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <circle cx="12" cy="12" r="3" />
      <path d="M12 2v3M12 19v3M2 12h3M19 12h3" />
      <path d="M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1" />
    </svg>
  );
}

function IconSaltPansChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#64748b" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M3 20h18" />
      <path d="M5 20V10l7-7 7 7v10" />
      <path d="M9 20v-5h6v5" />
      <path d="M12 13v-2" />
    </svg>
  );
}

function IconPhosphateMiningIndigenousRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#b45309" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2L4 8v13h16V8L12 2z" />
      <path d="M9 21V9l3-4 3 4v12" />
      <circle cx="12" cy="14" r="2" />
    </svg>
  );
}

function IconCarpetWeavingChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#92400e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <rect x="3" y="3" width="18" height="18" rx="2" />
      <line x1="3" y1="9" x2="21" y2="9" />
      <line x1="3" y1="15" x2="21" y2="15" />
      <line x1="9" y1="3" x2="9" y2="21" />
      <line x1="15" y1="3" x2="15" y2="21" />
    </svg>
  );
}

function IconSilkProductionChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#7c3aed" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <ellipse cx="12" cy="12" rx="5" ry="8" />
      <path d="M12 4C10 2 7 2 6 4" />
      <path d="M12 20c2 2 5 2 6 0" />
      <path d="M7 12c-2 0-4-1-4-3" />
      <path d="M17 12c2 0 4-1 4-3" />
    </svg>
  );
}

function IconCharcoalBurningChildLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#1c1917" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2c0 0-6 6-6 12a6 6 0 0 0 12 0c0-6-6-12-6-12z" />
      <path d="M12 10c0 0-2 2-2 4a2 2 0 0 0 4 0c0-2-2-4-2-4z" />
    </svg>
  );
}

function IconNailSalonWorkerRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#ec4899" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M18 8h1a4 4 0 0 1 0 8h-1" />
      <path d="M5 8h13" />
      <path d="M7 8v10" />
      <path d="M5 18h10" />
      <circle cx="7" cy="5" r="2" />
    </svg>
  );
}

function IconRestavekChildDomesticLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#7c3aed" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
      <circle cx="12" cy="7" r="1" />
    </svg>
  );
}

function IconFishingVesselForcedLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#0369a1" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M22 18H2a4 4 0 0 0 4 4h12a4 4 0 0 0 4-4z" />
      <path d="M21 14l-9-10-9 10" />
      <path d="M12 4v10" />
    </svg>
  );
}

function IconSurrogacyExploitationRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#9d174d" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2a5 5 0 0 1 5 5v4a5 5 0 0 1-10 0V7a5 5 0 0 1 5-5z" />
      <path d="M7 13c-2 1-3 3-3 5h16c0-2-1-4-3-5" />
      <circle cx="12" cy="8" r="1" />
    </svg>
  );
}

function IconHairHarvestingLaborRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#92400e" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M6 3c0 0 2 2 2 6s-2 6-2 9" />
      <path d="M12 3c0 0 2 2 2 6s-2 6-2 9" />
      <path d="M18 3c0 0 2 2 2 6s-2 6-2 9" />
      <path d="M4 14h16" />
    </svg>
  );
}

function IconBloodPlasmaDonationRights() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="#b91c1c" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5">
      <path d="M12 2L8 8h8L12 2z" />
      <path d="M12 8v8" />
      <circle cx="12" cy="18" r="3" />
    </svg>
  );
}

function IconSpiceFarmChildLaborRights({ size = 18, color = "#d97706" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22V12" />
      <path d="M12 12C12 7 7 4 4 6" />
      <path d="M12 12C12 7 17 4 20 6" />
      <circle cx="12" cy="8" r="2" />
      <path d="M8 20h8" />
    </svg>
  );
}

function IconNutmegPlantationLaborRights({ size = 18, color = "#166534" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <ellipse cx="12" cy="9" rx="5" ry="6" />
      <path d="M12 15v7" />
      <path d="M9 18h6" />
      <path d="M10 6c0-2 1-3 2-3s2 1 2 3" />
    </svg>
  );
}

function IconCardamomChildLaborRights({ size = 18, color = "#92400e" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <rect x="8" y="5" width="8" height="11" rx="3" />
      <path d="M12 16v6" />
      <path d="M9 19h6" />
      <path d="M10 8l2 2 2-2" />
      <circle cx="12" cy="3" r="1.5" />
    </svg>
  );
}
function IconMineralWaterExtractionCommunityRights({ size = 18, color = "#0891b2" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2C8 8 5 12 5 16a7 7 0 0 0 14 0c0-4-3-8-7-14z" />
      <path d="M9 16h6" />
      <path d="M8 20l2-2" />
      <path d="M16 20l-2-2" />
      <path d="M12 22v-4" />
    </svg>
  );
}
function IconSandalwoodIllegalLoggingRights({ size = 18, color = "#854d0e" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22v-8" />
      <path d="M8 22h8" />
      <path d="M12 14c-4 0-7-3-7-7 0-2 2-5 7-5s7 3 7 5c0 4-3 7-7 7z" />
      <path d="M9 9l3 3 3-3" />
      <path d="M5 19l2-2" />
      <path d="M19 19l-2-2" />
    </svg>
  );
}
function IconElectronicGoldRecoveryRights({ size = 18, color = "#ca8a04" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="6" width="18" height="12" rx="2" />
      <path d="M7 10h2v4H7z" />
      <path d="M11 10h2v4h-2z" />
      <path d="M15 10h2v4h-2z" />
      <path d="M7 6V4" />
      <path d="M12 6V4" />
      <path d="M17 6V4" />
      <circle cx="19" cy="10" r="1" />
    </svg>
  );
}

function IconCannedTunaLaborRights({ size = 18, color = "#0c4a6e" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="8" width="18" height="10" rx="2" />
      <path d="M3 13h18" />
      <path d="M7 8V6a5 5 0 0 1 10 0v2" />
      <path d="M9 17c1-2 5-2 6 0" />
      <path d="M12 11v2" />
    </svg>
  );
}
function IconShrimpFarmingMangroveRights({ size = 18, color = "#065f46" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 3v10" />
      <path d="M9 6c-2 1-3 3-1 5" />
      <path d="M15 6c2 1 3 3 1 5" />
      <path d="M9 9c-3 1-4 4-2 6" />
      <path d="M15 9c3 1 4 4 2 6" />
      <path d="M8 18c1-3 3-4 4-4s3 1 4 4" />
      <path d="M5 21h14" />
    </svg>
  );
}
function IconLivestockAntibioticWorkerRights({ size = 18, color = "#7f1d1d" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <ellipse cx="9" cy="13" rx="5" ry="4" />
      <path d="M14 11c2-1 5 0 5 3" />
      <path d="M4 13v3" />
      <path d="M8 17v2" />
      <path d="M14 17v2" />
      <path d="M19 7h-4" />
      <path d="M17 5v4" />
      <circle cx="17" cy="9" r="1" />
    </svg>
  );
}

function IconBambooLaborRights({ size = 18, color = "#15803d" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <line x1="8" y1="2" x2="8" y2="22" />
      <line x1="16" y1="2" x2="16" y2="22" />
      <line x1="8" y1="8" x2="16" y2="8" />
      <line x1="8" y1="15" x2="16" y2="15" />
      <path d="M8 8 Q4 6 4 4M16 15 Q20 13 20 11" />
    </svg>
  );
}

function IconPearlDivingLaborRights({ size = 18, color = "#0369a1" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="15" r="3" />
      <path d="M12 4c-2 0-4 1.5-4 4 0 1.5.5 2.5 1 3.5" />
      <path d="M12 4c2 0 4 1.5 4 4 0 1.5-.5 2.5-1 3.5" />
      <path d="M8 20c-2-1-4-3-4-5" />
      <path d="M16 20c2-1 4-3 4-5" />
      <path d="M9 4.5 Q12 2 15 4.5" />
    </svg>
  );
}

function IconSeaweedFarmingLaborRights({ size = 18, color = "#065f46" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 20 Q10 16 12 12 Q14 8 12 4" />
      <path d="M12 14 Q8 12 7 8" />
      <path d="M12 10 Q16 8 17 4" />
      <path d="M12 17 Q8 19 6 22" />
      <path d="M12 17 Q16 19 18 22" />
    </svg>
  );
}
function IconLatexGloveFactoryLaborRights({ size = 18, color = "#1e40af" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M8 12V7a1 1 0 0 1 2 0v3M10 7V5a1 1 0 0 1 2 0v5M12 6V5a1 1 0 0 1 2 0v5M14 7a1 1 0 0 1 2 0v3l1 3a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4l1-3V9" />
    </svg>
  );
}
function IconCottonseedChildLaborRights({ size = 18, color = "#d97706" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="8" r="3" />
      <path d="M9 8 Q6 6 6 3" />
      <path d="M15 8 Q18 6 18 3" />
      <path d="M12 11 Q10 14 10 17" />
      <path d="M12 11 Q14 14 14 17" />
      <path d="M12 20v-3" />
      <circle cx="8" cy="20" r="1" />
      <circle cx="12" cy="21" r="1" />
      <circle cx="16" cy="20" r="1" />
    </svg>
  );
}
function IconTobaccoNicotinePoisoningRights({ size = 18, color = "#7f1d1d" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M6 18 Q8 14 7 10 Q6 7 9 6 Q11 5 12 7" />
      <path d="M9 6 Q10 3 13 4 Q15 5 14 8" />
      <path d="M15 18 Q17 14 16 10" />
      <path d="M12 7 Q15 9 14 14 Q13 17 15 18" />
      <path d="M7 15 Q9 13 11 15 Q13 17 15 15" />
    </svg>
  );
}
function IconGoldJewelryArtisanRights({ size = 18, color = "#ca8a04" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2l1.5 3h3l-2.5 2 1 3-3-1.5-3 1.5 1-3-2.5-2h3z" />
      <path d="M9 13l-2 3h10l-2-3" />
      <path d="M7 16l1 4h8l1-4" />
      <line x1="12" y1="8" x2="12" y2="13" />
    </svg>
  );
}
function IconStoneQuarrySilicosisRights({ size = 18, color = "#78716c" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <polygon points="3,20 8,8 13,14 17,6 21,20" />
      <path d="M6 17 Q9 15 12 17 Q15 15 18 17" />
      <path d="M10 20 Q12 14 14 20" />
      <circle cx="18" cy="7" r="2" />
    </svg>
  );
}
function IconFlowerPackingChemicalRights({ size = 18, color = "#be185d" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="9" r="2" />
      <path d="M12 7 Q14 4 17 5 Q18 8 15 9" />
      <path d="M12 7 Q10 4 7 5 Q6 8 9 9" />
      <path d="M14 9 Q17 10 17 13 Q14 14 12 11" />
      <path d="M10 9 Q7 10 7 13 Q10 14 12 11" />
      <path d="M12 11 Q12 14 10 16 Q8 17 9 19" />
      <path d="M12 11 Q13 15 15 16 Q16 18 15 19" />
      <path d="M12 19 L12 22" />
      <path d="M8 21 Q10 20 12 22 Q14 20 16 21" />
    </svg>
  );
}

function IconCeramicDustSilicosisRights({ size = 18, color = "#b45309" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 3h6l2 6H7L9 3z" />
      <path d="M7 9v8a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9" />
      <path d="M5 7c-1 1-1 3 0 4" />
      <path d="M19 7c1 1 1 3 0 4" />
      <path d="M10 13 Q12 11 14 13" />
      <path d="M9 16 Q12 14 15 16" />
    </svg>
  );
}

function IconLeadPaintManufacturingWorkerRights({ size = 18, color = "#475569" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <rect x="7" y="8" width="10" height="10" rx="1" />
      <path d="M10 8V6a2 2 0 0 1 4 0v2" />
      <path d="M12 13v2" />
      <circle cx="12" cy="12" r="1" />
      <path d="M4 19 Q6 17 8 18" />
      <path d="M3 16 Q5 14 7 15" />
      <path d="M19 5l2-2" />
      <path d="M17 4l1-3" />
      <path d="M20 8l3-1" />
    </svg>
  );
}

function IconCoalWasheryWorkerRights({ size = 18, color = "#1c1917" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 20 Q6 16 5 12 Q4 8 7 6 Q10 4 12 7 Q14 4 17 6 Q20 8 19 12 Q18 16 20 20" />
      <path d="M4 20 h16" />
      <path d="M9 20 Q10 17 12 16 Q14 17 15 20" />
      <path d="M8 12 Q10 10 12 12 Q14 10 16 12" />
      <path d="M9 15 Q12 13 15 15" />
    </svg>
  );
}

function IconIncenseStickChildLaborRights({ size = 18, color = "#6d28d9" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="22" x2="12" y2="6" />
      <path d="M12 6 Q10 4 11 2 Q12 4 14 2 Q13 4 12 6" />
      <path d="M9 8 Q7 7 8 5" />
      <path d="M15 8 Q17 7 16 5" />
      <path d="M10 12 Q8 11 9 9" />
      <path d="M14 12 Q16 11 15 9" />
    </svg>
  );
}

function IconMatchFactoryPhosphorusRights({ size = 18, color = "#dc2626" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <line x1="8" y1="20" x2="18" y2="6" />
      <circle cx="18" cy="5" r="2" />
      <path d="M16 3 Q20 2 21 5 Q20 8 17 7" />
      <path d="M4 20 h5" />
      <path d="M6 17 h4" />
    </svg>
  );
}

function IconFireworksFactoryChildLaborRights({ size = 18, color = "#ea580c" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="10" r="2" />
      <line x1="12" y1="8" x2="12" y2="3" />
      <line x1="14" y1="9" x2="18" y2="5" />
      <line x1="14" y1="11" x2="19" y2="12" />
      <line x1="10" y1="9" x2="6" y2="5" />
      <line x1="10" y1="11" x2="5" y2="12" />
      <line x1="12" y1="12" x2="12" y2="17" />
      <line x1="13" y1="12" x2="17" y2="16" />
      <line x1="11" y1="12" x2="7" y2="16" />
      <path d="M8 20 Q12 18 16 20" />
    </svg>
  );
}

function IconGlowingBlowingSilicosisRights({ size = 18, color = "#0891b2" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="10" r="5" />
      <path d="M12 15v7M9 20h6" />
      <path d="M8 6 Q6 3 8 2M16 6 Q18 3 16 2" />
    </svg>
  );
}

function IconAzoDyeTextileWorkerRights({ size = 18, color = "#7c3aed" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="8" width="18" height="10" rx="2" />
      <path d="M3 12h18" />
      <path d="M8 8V6a4 4 0 0 1 8 0v2" />
      <circle cx="8" cy="16" r="1.5" />
      <circle cx="16" cy="16" r="1.5" />
    </svg>
  );
}

function IconLeadBatteryRecyclingRights({ size = 18, color = "#64748b" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <rect x="4" y="7" width="16" height="11" rx="2" />
      <path d="M8 7V5M16 7V5" />
      <path d="M8 13h2M14 13h2M10 11v4" />
      <path d="M17 3 Q20 6 17 9M7 3 Q4 6 7 9" />
    </svg>
  );
}
function IconRubberTappingForcedLaborRights({ size = 18, color = "#16a34a" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22V10" />
      <path d="M12 10 Q8 8 6 4" />
      <path d="M12 10 Q16 8 18 4" />
      <path d="M12 10 Q9 12 8 16" />
      <path d="M8 16 Q9 18 12 19" />
      <path d="M10 14 Q7 15 6 18" />
      <circle cx="6" cy="19" r="1.5" />
    </svg>
  );
}
function IconVanillaFarmingLaborRights({ size = 18, color = "#7c3aed" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22V12" />
      <path d="M12 12 Q10 8 7 6" />
      <path d="M12 12 Q14 8 17 6" />
      <path d="M9 9 Q11 10 12 12" />
      <ellipse cx="12" cy="5" rx="3" ry="2" />
      <path d="M10 5 Q12 3 14 5" />
      <path d="M12 15 Q9 16 8 19M12 15 Q15 16 16 19" />
    </svg>
  );
}
function IconSisalCultivationLaborRights({ size = 18, color = "#b45309" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22v-8" />
      <path d="M12 14 Q7 12 4 7" />
      <path d="M12 14 Q17 12 20 7" />
      <path d="M12 14 Q8 14 5 11" />
      <path d="M12 14 Q16 14 19 11" />
      <path d="M12 14 Q10 16 9 20" />
      <path d="M12 14 Q14 16 15 20" />
    </svg>
  );
}

function IconHempFiberProcessingLaborRights({ size = 18, color = "#15803d" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2c0 0-5 4-5 10s5 10 5 10 5-4 5-10S12 2 12 2z" />
      <path d="M7 8h10" />
      <path d="M7 12h10" />
      <path d="M7 16h10" />
    </svg>
  );
}

function IconJuteMillWorkerRights({ size = 18, color = "#a16207" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <rect x="4" y="8" width="16" height="8" rx="4" />
      <path d="M4 12h16" />
      <path d="M8 8V6" />
      <path d="M16 8V6" />
      <path d="M6 16v2" />
      <path d="M18 16v2" />
    </svg>
  );
}

function IconAbacaFiberChildLaborRights({ size = 18, color = "#0369a1" }: { size?: number; color?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2 Q6 6 6 12 Q6 18 12 22 Q18 18 18 12 Q18 6 12 2z" />
      <path d="M12 2v20" />
      <path d="M6 12 Q9 10 12 11 Q15 10 18 12" />
      <path d="M7 7 Q10 9 12 8 Q14 9 17 7" />
      <path d="M7 17 Q10 15 12 16 Q14 15 17 17" />
    </svg>
  );
}

const navSections: NavSection[] = [
  {
    title: "ANALYSE",
    items: [
      { href: "/dashboard", label: "Tableau de bord", icon: IconDashboard, exact: true },
      { href: "/dashboard/compare", label: "Comparaison", icon: IconComparison },
      { href: "/dashboard/pricing", label: "Tarification", icon: IconPricing },
    ],
  },
  {
    title: "SURVEILLANCE",
    items: [
      { href: "/dashboard/competitors", label: "Concurrents", icon: IconCompetitors },
      { href: "/dashboard/alerts", label: "Alertes", icon: IconAlerts, badge: 3 },
      { href: "/dashboard/reports", label: "Rapports", icon: IconReports },
    ],
  },
  {
    title: "ESSAIM IA",
    items: [
      { href: "/dashboard/swarm", label: "50 Agents Swarm", icon: IconSwarm },
      { href: "/dashboard/live", label: "Activité Live", icon: IconLive },
      { href: "/dashboard/prospects", label: "Prospects", icon: IconTarget },
      { href: "/dashboard/pipeline", label: "Pipeline", icon: IconPipeline },
      { href: "/dashboard/sectors", label: "Secteurs", icon: IconSector },
      { href: "/dashboard/finance", label: "Finance", icon: IconFinance },
      { href: "/dashboard/negotiations", label: "Négociations", icon: IconHandshake },
      { href: "/dashboard/abtesting", label: "A/B Testing", icon: IconFlask },
      { href: "/dashboard/tracking", label: "Email Tracking", icon: IconEmail },
      { href: "/dashboard/campaigns", label: "Campagnes", icon: IconCalendar },
      { href: "/dashboard/memory", label: "Mémoire Prospects", icon: IconMemory },
      { href: "/dashboard/quotes", label: "Devis", icon: IconQuote },
      { href: "/dashboard/sequences", label: "Séquences Outreach", icon: IconSequence },
      { href: "/dashboard/funnel", label: "Funnel de Conversion", icon: IconFunnel },
      { href: "/dashboard/invoices", label: "Factures", icon: IconInvoice },
      { href: "/dashboard/qualification", label: "Qualification BANT", icon: IconQualification },
      { href: "/dashboard/followup", label: "Suivi Prioritaire", icon: IconFollowUp },
      { href: "/dashboard/replies", label: "Analyse Réponses", icon: IconReply },
      { href: "/dashboard/workflow", label: "Orchestrateur", icon: IconWorkflow },
      { href: "/dashboard/scorecard", label: "Scorecard Prospects", icon: IconScorecard },
      { href: "/dashboard/leads", label: "Scoring Leads", icon: IconLeadScorer },
      { href: "/dashboard/enricher", label: "Enrichissement", icon: IconEnricher },
      { href: "/dashboard/dedup", label: "Déduplication", icon: IconDedup },
      { href: "/dashboard/timing", label: "Timing Contact", icon: IconTiming },
      { href: "/dashboard/objections", label: "Objections", icon: IconObjection },
      { href: "/dashboard/sentiment", label: "Sentiment IA", icon: IconSentiment },
      { href: "/dashboard/templates", label: "Templates Email", icon: IconTemplates },
      { href: "/dashboard/performance", label: "Performance Agents", icon: IconPerformance },
      { href: "/dashboard/forecast", label: "Prévisions Ventes", icon: IconForecast },
      { href: "/dashboard/composer", label: "Compositeur Email", icon: IconComposer },
      { href: "/dashboard/scorer", label: "Threat Scoring", icon: IconScorer },
      { href: "/dashboard/priority", label: "Priorité Leads", icon: IconPriority },
      { href: "/dashboard/retention", label: "Rétention Clients", icon: IconRetention },
      { href: "/dashboard/subject-optimizer", label: "Sujets Email IA", icon: IconSubjectOptimizer },
      { href: "/dashboard/security", label: "Sécurité IA", icon: IconSecurity },
      { href: "/dashboard/revenue", label: "Prévisions Revenus", icon: IconRevenue },
      { href: "/dashboard/proposals", label: "Scoring Propositions", icon: IconProposals },
      { href: "/dashboard/threat-intel", label: "Intelligence Menaces", icon: IconThreatIntel },
      { href: "/dashboard/market-opportunities", label: "Opportunités Marché", icon: IconMarket },
      { href: "/dashboard/sales-coach", label: "Sales Coach IA", icon: IconSalesCoach },
      { href: "/dashboard/campaign-roi", label: "ROI Campagnes", icon: IconCampaignROI },
      { href: "/dashboard/contact-personalizer", label: "Perso. Contacts", icon: IconContactPersonalizer },
      { href: "/dashboard/deal-accelerator", label: "Deal Accelerator", icon: IconDealAccelerator },
      { href: "/dashboard/account-health", label: "Santé Comptes", icon: IconAccountHealth },
      { href: "/dashboard/icp-scorer", label: "Scoring ICP", icon: IconICPScorer },
      { href: "/dashboard/email-sequence-optimizer", label: "Séquences Email", icon: IconEmailSequence },
      { href: "/dashboard/competitor-intelligence", label: "Intel. Concurrents", icon: IconCompetitorIntel },
      { href: "/dashboard/pricing-optimizer", label: "Optimiseur Pricing", icon: IconPricingOptimizer },
      { href: "/dashboard/lead-enrichment", label: "Enrichissement Leads", icon: IconLeadEnrichment },
      { href: "/dashboard/churn-predictor", label: "Prédicteur Churn", icon: IconChurnPredictor },
      { href: "/dashboard/revenue-forecaster", label: "Forecast Revenus", icon: IconRevenueForecaster },
      { href: "/dashboard/onboarding-health", label: "Santé Onboarding", icon: IconOnboardingHealth },
      { href: "/dashboard/pipeline-velocity", label: "Vélocité Pipeline", icon: IconPipelineVelocity },
      { href: "/dashboard/objection-intelligence", label: "Intel. Objections", icon: IconObjectionIntelligence },
      { href: "/dashboard/expansion-revenue", label: "Revenus Expansion", icon: IconExpansionRevenue },
      { href: "/dashboard/win-loss-intelligence", label: "Analyse Win/Loss", icon: IconWinLossIntelligence },
      { href: "/dashboard/customer-success-playbook", label: "Playbook CS", icon: IconCustomerSuccessPlaybook },
      { href: "/dashboard/territory-optimizer", label: "Territoires", icon: IconTerritoryOptimizer },
      { href: "/dashboard/contract-renewal", label: "Renouvellements", icon: IconContractRenewal },
      { href: "/dashboard/sales-coaching-engine", label: "Coaching Ventes", icon: IconSalesCoachingEngine },
      { href: "/dashboard/lead-scoring-intelligence", label: "Scoring Leads IA", icon: IconLeadScoringIntelligence },
      { href: "/dashboard/competitive-battlecard", label: "Battlecards Concurrents", icon: IconCompetitiveBattlecard },
      { href: "/dashboard/price-optimization", label: "Optimisation Pricing", icon: IconPriceOptimization },
      { href: "/dashboard/deal-risk-analyzer", label: "Analyse Risque Deals", icon: IconDealRiskAnalyzer },
      { href: "/dashboard/account-health-scorer", label: "Santé Comptes IA", icon: IconAccountHealthScorer },
      { href: "/dashboard/forecast-accuracy-engine", label: "Précision Forecast", icon: IconForecastAccuracy },
      { href: "/dashboard/onboarding-risk-monitor", label: "Risques Onboarding", icon: IconOnboardingRisk },
      { href: "/dashboard/renewal-intelligence-engine", label: "Intelligence Renouvellement", icon: IconRenewalIntelligence },
      { href: "/dashboard/pipeline-gap-analyzer", label: "Analyse Gap Pipeline", icon: IconPipelineGap },
      { href: "/dashboard/sales-velocity", label: "Vélocité Commerciale", icon: IconSalesVelocity },
      { href: "/dashboard/competitive-win-loss", label: "Win-Loss Compétitif", icon: IconCompetitiveWinLoss },
      { href: "/dashboard/quota-attainment", label: "Prédiction Quota", icon: IconQuotaAttainment },
      { href: "/dashboard/deal-stage-progression", label: "Progression Deals", icon: IconDealStageProgression },
      { href: "/dashboard/rep-activity-intelligence", label: "Activité Commerciale", icon: IconRepActivity },
      { href: "/dashboard/customer-lifetime-value", label: "Valeur Client (CLV)", icon: IconCLV },
      { href: "/dashboard/meeting-intelligence", label: "Intelligence Réunions", icon: IconMeetingIntelligence },
      { href: "/dashboard/competitive-intelligence", label: "Intel. Compétitive", icon: IconCompetitiveIntelligence },
      { href: "/dashboard/account-penetration", label: "Pénétration Comptes", icon: IconAccountPenetration },
      { href: "/dashboard/pipeline-health-index", label: "Santé Pipeline (PHI)", icon: IconPipelineHealth },
      { href: "/dashboard/buyer-intent", label: "Buyer Intent", icon: IconBuyerIntent },
      { href: "/dashboard/deal-momentum", label: "Deal Momentum", icon: IconDealMomentum },
      { href: "/dashboard/forecast-commit", label: "Forecast Commit", icon: IconForecastCommit },
      { href: "/dashboard/sales-skills", label: "Sales Skills", icon: IconSalesSkills },
      { href: "/dashboard/stakeholder-map", label: "Stakeholder Map", icon: IconStakeholderMap },
      { href: "/dashboard/email-personalization", label: "Email Personalization", icon: IconEmailPersonalization },
      { href: "/dashboard/competitive-positioning", label: "Competitive Positioning", icon: IconCompetitivePositioning },
      { href: "/dashboard/revenue-attribution", label: "Revenue Attribution", icon: IconRevenueAttribution },
      { href: "/dashboard/quota-gap-analysis", label: "Quota Gap Analysis", icon: IconQuotaGap },
      { href: "/dashboard/partner-channel", label: "Partner Channel", icon: IconPartnerChannel },
      { href: "/dashboard/price-negotiation", label: "Price Negotiation", icon: IconPriceNegotiation },
      { href: "/dashboard/account-expansion", label: "Account Expansion", icon: IconAccountExpansion },
      { href: "/dashboard/customer-onboarding", label: "Customer Onboarding", icon: IconCustomerOnboarding },
      { href: "/dashboard/sales-capacity", label: "Sales Capacity", icon: IconSalesCapacity },
      { href: "/dashboard/sales-forecast", label: "Sales Forecast", icon: IconSalesForecast },
      { href: "/dashboard/deal-velocity", label: "Deal Velocity", icon: IconDealVelocity },
      { href: "/dashboard/pipeline-coverage", label: "Pipeline Coverage", icon: IconPipelineCoverage },
      { href: "/dashboard/territory-performance", label: "Territory Perf.", icon: IconTerritoryPerformance },
      { href: "/dashboard/competitive-win-rate", label: "Comp. Win Rate", icon: IconCompWinRate },
      { href: "/dashboard/account-scoring", label: "Account Scoring", icon: IconAccountScoring },
      { href: "/dashboard/revenue-leakage", label: "Revenue Leakage", icon: IconRevenueLeakage },
      { href: "/dashboard/sales-rep-burnout", label: "Rep Burnout", icon: IconSalesRepBurnout },
      { href: "/dashboard/pricing-elasticity", label: "Pricing Elasticity", icon: IconPricingElasticity },
      { href: "/dashboard/sales-compensation-intelligence", label: "Comp Intelligence", icon: IconSalesCompIntel },
      { href: "/dashboard/customer-expansion-readiness", label: "Expansion Readiness", icon: IconCustomerExpansion },
      { href: "/dashboard/deal-fragmentation", label: "Deal Fragmentation", icon: IconDealFragmentation },
      { href: "/dashboard/buyer-persona-drift", label: "Persona Drift", icon: IconBuyerPersonaDrift },
      { href: "/dashboard/contract-clause-risk", label: "Contract Clauses", icon: IconContractClauseRisk },
      { href: "/dashboard/call-tone-analyzer", label: "Call Tone AI", icon: IconCallToneAnalyzer },
      { href: "/dashboard/prospect-digital-footprint", label: "Digital Footprint", icon: IconProspectDigitalFootprint },
      { href: "/dashboard/mutual-action-plan", label: "MAP Tracker", icon: IconMutualActionPlan },
      { href: "/dashboard/territory-whitespace", label: "Territory WS", icon: IconTerritoryWhitespace },
      { href: "/dashboard/ghosting-predictor", label: "Ghost Predictor", icon: IconGhostingPredictor },
      { href: "/dashboard/conversation-intelligence", label: "Conv. Intelligence", icon: IconConversationIntelligence },
      { href: "/dashboard/revenue-leak-detector", label: "Revenue Leak", icon: IconRevenueLeakDetector },
      { href: "/dashboard/email-sentiment-tracker", label: "Email Sentiment", icon: IconEmailSentimentTracker },
      { href: "/dashboard/deal-velocity-tracker", label: "Deal Velocity", icon: IconDealVelocityTracker },
      { href: "/dashboard/forecast-confidence-scorer", label: "Forecast Conf.", icon: IconForecastConfidenceScorer },
      { href: "/dashboard/champion-risk-monitor", label: "Champion Risk", icon: IconChampionRiskMonitor },
      { href: "/dashboard/buying-committee-mapper", label: "Committee Map", icon: IconBuyingCommitteeMapper },
      { href: "/dashboard/objection-pattern-analyzer", label: "Objection Patterns", icon: IconObjectionPatternAnalyzer },
      { href: "/dashboard/win-loss-pattern-engine", label: "Win/Loss Patterns", icon: IconWinLossPatternEngine },
      { href: "/dashboard/rep-ramp-intelligence", label: "Rep Ramp Intel", icon: IconRepRampIntelligence },
      { href: "/dashboard/sales-process-compliance-monitor", label: "Process Compliance", icon: IconSalesProcessCompliance },
      { href: "/dashboard/prospect-engagement-velocity", label: "Prospect Velocity", icon: IconProspectEngagementVelocity },
      { href: "/dashboard/account-expansion-intelligence", label: "Account Expansion", icon: IconAccountExpansionIntelligence },
      { href: "/dashboard/sales-data-integrity-monitor", label: "Data Integrity", icon: IconSalesDataIntegrityMonitor },
      { href: "/dashboard/customer-referral-intelligence", label: "Referral Intel", icon: IconCustomerReferralIntelligence },
      { href: "/dashboard/deal-multithreading-intelligence", label: "Deal Threading", icon: IconDealMultithreadingIntelligence },
      { href: "/dashboard/rep-attrition-risk-engine", label: "Rep Attrition", icon: IconRepAttritionRiskEngine },
      { href: "/dashboard/pipeline-aging-intelligence", label: "Pipeline Aging", icon: IconPipelineAgingIntelligence },
      { href: "/dashboard/deal-complexity-intelligence", label: "Deal Complexity", icon: IconDealComplexityIntelligence },
      { href: "/dashboard/quota-fairness-engine", label: "Quota Fairness", icon: IconQuotaFairnessEngine },
      { href: "/dashboard/forecast-calibration-engine", label: "Forecast Calibration", icon: IconForecastCalibrationEngine },
      { href: "/dashboard/sales-capacity-planning-engine", label: "Sales Capacity", icon: IconSalesCapacityPlanningEngine },
      { href: "/dashboard/deal-contamination-risk-engine", label: "Deal Contamination", icon: IconDealContaminationRiskEngine },
      { href: "/dashboard/competitive-win-probability-engine", label: "Win Probability", icon: IconCompetitiveWinProbabilityEngine },
      { href: "/dashboard/sales-burnout-risk-engine", label: "Burnout Risk", icon: IconSalesBurnoutRiskEngine },
      { href: "/dashboard/rep-incentive-misalignment-engine", label: "Incentive Misalign.", icon: IconRepIncentiveMisalignmentEngine },
      { href: "/dashboard/sales-data-access-anomaly-engine", label: "Data Access Anomaly", icon: IconSalesDataAccessAnomalyEngine },
      { href: "/dashboard/sales-activity-fabrication-detector", label: "Activity Fabrication", icon: IconSalesActivityFabricationDetector },
      { href: "/dashboard/sales-commission-clawback-risk-engine", label: "Commission Clawback", icon: IconSalesCommissionClawbackRiskEngine },
      { href: "/dashboard/customer-sentiment-decay-engine", label: "Sentiment Decay", icon: IconCustomerSentimentDecayEngine },
      { href: "/dashboard/sales-process-velocity-anomaly-engine", label: "Process Velocity", icon: IconSalesProcessVelocityAnomalyEngine },
      { href: "/dashboard/sales-forecast-sandbagging-detector", label: "Forecast Sandbagging", icon: IconSalesForecastSandbaggingDetector },
      { href: "/dashboard/sales-discount-abuse-detector", label: "Discount Abuse", icon: IconSalesDiscountAbuseDetector },
      { href: "/dashboard/crm-data-quality-risk-engine", label: "CRM Data Quality", icon: IconCRMDataQualityRiskEngine },
      { href: "/dashboard/sales-rep-burnout-disengagement-engine", label: "Rep Burnout", icon: IconSalesRepBurnoutDisengagementEngine },
      { href: "/dashboard/competitor-win-loss-intelligence-engine", label: "Competitor Intel", icon: IconCompetitorWinLossIntelligenceEngine },
      { href: "/dashboard/sales-data-exfiltration-risk-engine", label: "Data Exfiltration", icon: IconSalesDataExfiltrationRiskEngine },
      { href: "/dashboard/sales-quota-gaming-detection-engine", label: "Quota Gaming", icon: IconSalesQuotaGamingDetectionEngine },
      { href: "/dashboard/deal-ghosting-risk-engine", label: "Deal Ghosting", icon: IconDealGhostingRiskEngine },
      { href: "/dashboard/account-executive-ramp-velocity-engine", label: "AE Ramp Velocity", icon: IconAccountExecutiveRampVelocityEngine },
      { href: "/dashboard/sales-territory-overlap-conflict-engine", label: "Territory Overlap", icon: IconSalesTerritoryOverlapConflictEngine },
      { href: "/dashboard/customer-ltv-erosion-detector", label: "LTV Erosion", icon: IconCustomerLTVErosionDetector },
      { href: "/dashboard/sales-pipeline-concentration-risk-engine", label: "Pipeline Concentration", icon: IconSalesPipelineConcentrationRiskEngine },
      { href: "/dashboard/sales-rep-capacity-overload-detector", label: "Rep Capacity", icon: IconSalesRepCapacityOverloadDetector },
      { href: "/dashboard/sales-competitive-win-rate-erosion-engine", label: "Win Rate Erosion", icon: IconSalesCompetitiveWinRateErosionEngine },
      { href: "/dashboard/sales-rep-burnout-attrition-risk-engine", label: "Rep Burnout Risk", icon: IconSalesRepBurnoutAttritionRiskEngine },
      { href: "/dashboard/sales-forecast-sandbagging-detection-engine", label: "Forecast Sandbagging", icon: IconSalesForecastSandbaggingDetectionEngine },
      { href: "/dashboard/customer-expansion-revenue-leak-detector", label: "Expansion Revenue Leak", icon: IconCustomerExpansionRevenueLeakDetector },
      { href: "/dashboard/sales-cycle-velocity-degradation-engine", label: "Cycle Velocity", icon: IconSalesCycleVelocityDegradationEngine },
      { href: "/dashboard/sales-incentive-compensation-risk-engine", label: "Incentive Comp Risk", icon: IconSalesIncentiveCompensationRiskEngine },
      { href: "/dashboard/sales-objection-pattern-intelligence-engine", label: "Objection Patterns", icon: IconSalesObjectionPatternIntelligenceEngine },
      { href: "/dashboard/pipeline-generation-efficiency-engine", label: "Pipeline Efficiency", icon: IconPipelineGenerationEfficiencyEngine },
      { href: "/dashboard/sales-coaching-effectiveness-engine", label: "Coaching Effectiveness", icon: IconSalesCoachingEffectivenessEngine },
      { href: "/dashboard/sales-proposal-conversion-intelligence-engine", label: "Proposal Conversion", icon: IconSalesProposalConversionIntelligenceEngine },
      { href: "/dashboard/sales-territory-coverage-intelligence-engine", label: "Territory Coverage", icon: IconSalesTerritoryCoverageIntelligenceEngine },
      { href: "/dashboard/sales-customer-relationship-health-engine", label: "Customer Relationship", icon: IconSalesCustomerRelationshipHealthEngine },
      { href: "/dashboard/sales-forecast-accuracy-intelligence-engine", label: "Forecast Accuracy", icon: IconSalesForecastAccuracyIntelligenceEngine },
      { href: "/dashboard/sales-account-expansion-intelligence-engine", label: "Account Expansion", icon: IconSalesAccountExpansionIntelligenceEngine },
      { href: "/dashboard/sales-meeting-quality-intelligence-engine", label: "Meeting Quality", icon: IconSalesMeetingQualityIntelligenceEngine },
      { href: "/dashboard/sales-pricing-negotiation-intelligence-engine", label: "Pricing Negotiation", icon: IconSalesPricingNegotiationIntelligenceEngine },
      { href: "/dashboard/sales-inbound-lead-response-engine", label: "Lead Response", icon: IconSalesInboundLeadResponseEngine },
      { href: "/dashboard/sales-competitive-win-loss-intelligence-engine", label: "Competitive W/L", icon: IconSalesCompetitiveWinLossIntelligenceEngine },
      { href: "/dashboard/sales-outbound-prospecting-intelligence-engine", label: "Outbound Prospect.", icon: IconSalesOutboundProspectingIntelligenceEngine },
      { href: "/dashboard/sales-quota-attainment-intelligence-engine", label: "Quota Attainment", icon: IconSalesQuotaAttainmentIntelligenceEngine },
      { href: "/dashboard/sales-stakeholder-mapping-intelligence-engine", label: "Stakeholder Mapping", icon: IconSalesStakeholderMappingIntelligenceEngine },
      { href: "/dashboard/sales-deal-momentum-intelligence-engine", label: "Deal Momentum", icon: IconSalesDealMomentumIntelligenceEngine },
      { href: "/dashboard/sales-pipeline-contamination-intelligence-engine", label: "Pipeline Contam.", icon: IconSalesPipelineContaminationIntelligenceEngine },
      { href: "/dashboard/sales-buyer-response-latency-intelligence-engine", label: "Buyer Latency", icon: IconSalesBuyerResponseLatencyIntelligenceEngine },
      { href: "/dashboard/sales-deal-velocity-intelligence-engine", label: "Deal Velocity", icon: IconSalesDealVelocityIntelligenceEngine },
      { href: "/dashboard/sales-account-penetration-intelligence-engine", label: "Acct. Penetration", icon: IconSalesAccountPenetrationIntelligenceEngine },
      { href: "/dashboard/sales-time-allocation-intelligence-engine", label: "Time Allocation", icon: IconSalesTimeAllocationIntelligenceEngine },
      { href: "/dashboard/sales-rep-retention-risk-intelligence-engine", label: "Rep Retention Risk", icon: IconSalesRepRetentionRiskIntelligenceEngine },
      { href: "/dashboard/sales-multi-channel-engagement-intelligence-engine", label: "Multi-Channel Eng.", icon: IconSalesMultiChannelEngagementIntelligenceEngine },
      { href: "/dashboard/sales-pipeline-hygiene-intelligence-engine", label: "Pipeline Hygiene", icon: IconSalesPipelineHygieneIntelligenceEngine },
      { href: "/dashboard/sales-buyer-intent-signal-intelligence-engine", label: "Buyer Intent", icon: IconSalesBuyerIntentSignalIntelligenceEngine },
      { href: "/dashboard/sales-negotiation-effectiveness-intelligence-engine", label: "Negotiation Eff.", icon: IconSalesNegotiationEffectivenessIntelligenceEngine },
      { href: "/dashboard/sales-forecast-sanity-check-intelligence-engine", label: "Forecast Sanity", icon: IconSalesForecastSanityCheckIntelligenceEngine },
      { href: "/dashboard/sales-onboarding-effectiveness-intelligence-engine", label: "Rep Onboarding", icon: IconSalesOnboardingEffectivenessIntelligenceEngine },
      { href: "/dashboard/sales-conversation-quality-intelligence-engine", label: "Conv. Quality", icon: IconSalesConversationQualityIntelligenceEngine },
      { href: "/dashboard/sales-email-sequence-intelligence-engine", label: "Email Sequences", icon: IconSalesEmailSequenceIntelligenceEngine },
      { href: "/dashboard/sales-multithreading-intelligence-engine", label: "Multithreading", icon: IconSalesMultithreadingIntelligenceEngine },
      { href: "/dashboard/sales-social-selling-intelligence-engine", label: "Social Selling", icon: IconSalesSocialSellingIntelligenceEngine },
      { href: "/dashboard/sales-crm-adoption-intelligence-engine", label: "CRM Adoption", icon: IconSalesCRMAdoptionIntelligenceEngine },
      { href: "/dashboard/sales-deal-desk-intelligence-engine", label: "Deal Desk", icon: IconSalesDealDeskIntelligenceEngine },
      { href: "/dashboard/sales-poc-intelligence-engine", label: "POC Execution", icon: IconSalesPOCIntelligenceEngine },
      { href: "/dashboard/sales-reference-intelligence-engine", label: "Ref. Evidence", icon: IconSalesReferenceIntelligenceEngine },
      { href: "/dashboard/sales-negotiation-intelligence-engine", label: "Negotiation", icon: IconSalesNegotiationIntelligenceEngine },
      { href: "/dashboard/sales-buyer-meeting-quality-intelligence-engine", label: "Meeting Quality", icon: IconSalesBuyerMeetingQualityIntelligenceEngine },
      { href: "/dashboard/sales-objection-intelligence-engine", label: "Objection Intel", icon: IconSalesObjectionIntelligenceEngine },
      { href: "/dashboard/sales-quota-attainment-pattern-intelligence-engine", label: "Quota Patterns", icon: IconSalesQuotaAttainmentPatternIntelligenceEngine },
      { href: "/dashboard/sales-rep-onboarding-ramp-intelligence-engine", label: "Onboarding Ramp", icon: IconSalesRepOnboardingRampIntelligenceEngine },
      { href: "/dashboard/sales-win-rate-decay-intelligence-engine", label: "Win Rate Decay", icon: IconSalesWinRateDecayIntelligenceEngine },
      { href: "/dashboard/sales-champion-stability-intelligence-engine", label: "Champion Stability", icon: IconSalesChampionStabilityIntelligenceEngine },
      { href: "/dashboard/sales-decision-criteria-alignment-intelligence-engine", label: "Criteria Alignment", icon: IconSalesDecisionCriteriaAlignmentIntelligenceEngine },
      { href: "/dashboard/sales-pricing-confidence-intelligence-engine", label: "Pricing Confidence", icon: IconSalesPricingConfidenceIntelligenceEngine },
      { href: "/dashboard/sales-buyer-engagement-velocity-intelligence-engine", label: "Engagement Velocity", icon: IconSalesBuyerEngagementVelocityIntelligenceEngine },
      { href: "/dashboard/sales-negotiation-leverage-intelligence-engine", label: "Negotiation Leverage", icon: IconSalesNegotiationLeverageIntelligenceEngine },
      { href: "/dashboard/sales-pipeline-health-degradation-intelligence-engine", label: "Pipeline Health", icon: IconSalesPipelineHealthDegradationIntelligenceEngine },
      { href: "/dashboard/sales-objection-handling-effectiveness-intelligence-engine", label: "Objection Handling", icon: IconSalesObjectionHandlingEffectivenessIntelligenceEngine },
      { href: "/dashboard/sales-discovery-quality-intelligence-engine", label: "Discovery Quality", icon: IconSalesDiscoveryQualityIntelligenceEngine },
      { href: "/dashboard/sales-customer-success-handoff-quality-intelligence-engine", label: "CS Handoff Quality", icon: IconSalesCustomerSuccessHandoffQualityIntelligenceEngine },
      { href: "/dashboard/sales-negotiation-discipline-intelligence-engine", label: "Negotiation Discipline", icon: IconSalesNegotiationDisciplineIntelligenceEngine },
      { href: "/dashboard/sales-territory-whitespace-intelligence-engine", label: "Territory Whitespace", icon: IconSalesTerritoryWhitespaceIntelligenceEngine },
      { href: "/dashboard/sales-proof-of-value-intelligence-engine", label: "Proof of Value", icon: IconSalesProofOfValueIntelligenceEngine },
      { href: "/dashboard/sales-pipeline-generation-velocity-intelligence-engine", label: "Pipeline Velocity", icon: IconSalesPipelineGenerationVelocityIntelligenceEngine },
      { href: "/dashboard/sales-multi-threading-intelligence-engine", label: "Multi-Threading", icon: IconSalesMultiThreadingIntelligenceEngine },
      { href: "/dashboard/sales-buyer-engagement-intelligence-engine", label: "Buyer Engagement", icon: IconSalesBuyerEngagementIntelligenceEngine },
      { href: "/dashboard/sales-conversation-intelligence-engine", label: "Conversation Intel", icon: IconSalesConversationIntelligenceEngine },
      { href: "/dashboard/sales-rep-ramp-intelligence-engine", label: "Rep Ramp", icon: IconSalesRepRampIntelligenceEngine },
      { href: "/dashboard/sales-pricing-discipline-intelligence-engine", label: "Pricing Discipline", icon: IconSalesPricingDisciplineIntelligenceEngine },
      { href: "/dashboard/sales-objection-handling-intelligence-engine", label: "Objection Handling", icon: IconSalesObjectionHandlingIntelligenceEngine },
      { href: "/dashboard/sales-crm-data-hygiene-intelligence-engine", label: "CRM Hygiene", icon: IconSalesCRMDataHygieneIntelligenceEngine },
      { href: "/dashboard/sales-customer-lifecycle-intelligence-engine", label: "Customer Lifecycle", icon: IconSalesCustomerLifecycleIntelligenceEngine },
      { href: "/dashboard/sales-competitive-intelligence-engine", label: "Competitive Intel", icon: IconSalesCompetitiveIntelligenceEngine },
      { href: "/dashboard/sales-territory-coverage-intelligence-engine", label: "Territory Coverage", icon: IconSalesTerritoryConverageIntelligenceEngine },
      { href: "/dashboard/sales-coaching-receptivity-intelligence-engine", label: "Coaching Receptivity", icon: IconSalesCoachingReceptivityIntelligenceEngine },
      { href: "/dashboard/sales-value-proposition-deterioration-intelligence-engine", label: "Value Prop. Det.", icon: IconSalesValuePropositionDeteriorationIntelligenceEngine },
      { href: "/dashboard/sales-quota-sandbag-overcommit-intelligence-engine", label: "Quota Gaming", icon: IconSalesQuotaSandbagOvercommitIntelligenceEngine },
      { href: "/dashboard/sales-rep-burnout-attrition-risk-intelligence-engine", label: "Burnout & Flight Risk", icon: IconSalesRepBurnoutAttritionRiskIntelligenceEngine },
      { href: "/dashboard/sales-deal-velocity-collapse-intelligence-engine", label: "Deal Velocity", icon: IconSalesDealVelocityCollapseIntelligenceEngine },
      { href: "/dashboard/sales-buyer-persona-mismatch-intelligence-engine", label: "Persona Mismatch", icon: IconSalesBuyerPersonaMismatchIntelligenceEngine },
      { href: "/dashboard/sales-discount-leakage-margin-erosion-intelligence-engine", label: "Discount Leakage", icon: IconSalesDiscountLeakageMarginErosionIntelligenceEngine },
      { href: "/dashboard/sales-meeting-quality-conversion-intelligence-engine", label: "Meeting Quality", icon: IconSalesMeetingQualityConversionIntelligenceEngine },
      { href: "/dashboard/sales-competitive-intelligence-battle-card-engine", label: "Competitive Intel", icon: IconSalesCompetitiveIntelligenceBattleCardEngine },
      { href: "/dashboard/sales-onboarding-ramp-intelligence-engine", label: "Onboarding Ramp", icon: IconSalesOnboardingRampIntelligenceEngine },
      { href: "/dashboard/sales-customer-health-score-deterioration-engine", label: "Customer Health", icon: IconSalesCustomerHealthScoreDeteriorationEngine },
      { href: "/dashboard/sales-territory-imbalance-coverage-gap-engine", label: "Territory Balance", icon: IconSalesTerritoryImbalanceCoverageGapEngine },
      { href: "/dashboard/sales-price-sensitivity-negotiation-leverage-engine", label: "Negotiation Leverage", icon: IconSalesPriceSensitivityNegotiationLeverageEngine },
      { href: "/dashboard/sales-proposal-quality-win-rate-intelligence-engine", label: "Proposal Quality", icon: IconSalesProposalQualityWinRateIntelligenceEngine },
      { href: "/dashboard/sales-champion-departure-relationship-continuity-engine", label: "Champion Risk", icon: IconSalesChampionDepartureRelationshipContinuityEngine },
      { href: "/dashboard/sales-pipeline-stage-inflation-crm-hygiene-engine", label: "Pipeline Hygiene", icon: IconSalesPipelineStageInflationCrmHygieneEngine },
      { href: "/dashboard/sales-competitive-win-loss-pattern-engine", label: "Competitive Wins", icon: IconSalesCompetitiveWinLossPatternEngine },
      { href: "/dashboard/sales-buyer-intent-signal-decay-engine", label: "Intent Decay", icon: IconSalesBuyerIntentSignalDecayEngine },
      { href: "/dashboard/sales-multithreading-depth-relationship-breadth-engine", label: "Multithreading", icon: IconSalesMultithreadingDepthRelationshipBreadthEngine },
      { href: "/dashboard/sales-discount-approval-abuse-margin-erosion-engine", label: "Margin Erosion", icon: IconSalesDiscountApprovalAbuseMarginErosionEngine },
      { href: "/dashboard/agents", label: "60 Agents Dir.", icon: IconAgents },
      { href: "/dashboard/branding", label: "LinkedIn & CV", icon: IconBranding },
      { href: "/dashboard/portfolio", label: "Portfolio", icon: IconPortfolio },
      { href: "/dashboard/editorial", label: "Calendrier Éditorial", icon: IconEditorial },
      { href: "/dashboard/sales-pipeline-stage-inflation-crm-hygiene-engine", label: "Pipeline Hygiene", icon: IconPipelineHygiene },
      { href: "/dashboard/sales-competitive-win-loss-pattern-engine", label: "Competitive Wins", icon: IconCompetitiveWins },
      { href: "/dashboard/sales-buyer-intent-signal-decay-engine", label: "Intent Decay", icon: IconIntentDecay },
      { href: "/dashboard/sales-multithreading-depth-relationship-breadth-engine", label: "Multithreading", icon: IconMultithreading },
      { href: "/dashboard/sales-discount-approval-abuse-margin-erosion-engine", label: "Margin Erosion", icon: IconMarginErosion },
      { href: "/dashboard/sales-rep-burnout-productivity-decay-engine", label: "Rep Burnout", icon: IconRepBurnout },
      { href: "/dashboard/sales-forecast-accuracy-commit-reliability-engine", label: "Forecast Reliability", icon: IconForecastAccuracy },
      { href: "/dashboard/sales-onboarding-ramp-velocity-engine", label: "Onboarding Ramp", icon: IconForecastAccuracy },
      { href: "/dashboard/sales-account-churn-early-warning-engine", label: "Churn Warning", icon: IconAccountChurn },
      { href: "/dashboard/sales-expansion-revenue-signal-engine", label: "Expansion Revenue", icon: IconExpansionRevenue },
      { href: "/dashboard/sales-deal-velocity-acceleration-engine", label: "Deal Velocity", icon: IconDealVelocity },
      { href: "/dashboard/invoice-intelligence-engine", label: "Facturation", icon: IconInvoice },
      { href: "/dashboard/order-management-intelligence-engine", label: "Commandes", icon: IconOrderManagement },
      { href: "/dashboard/customer-service-quality-engine", label: "Service Client", icon: IconCustomerService },
      { href: "/dashboard/it-systems-health-monitoring-engine", label: "IT Systèmes", icon: IconITSystems },
      { href: "/dashboard/swarm-security-shield-engine", label: "Bouclier Sécurité", icon: IconSecurityShield },
      { href: "/dashboard/data-analytics-intelligence-engine", label: "Analyse Données", icon: IconDataAnalytics },
      { href: "/dashboard/ethics-compliance-sentinel-engine", label: "Éthique & Conformité", icon: IconEthicsCompliance },
      { href: "/dashboard/innovation-scout-engine", label: "Scout Innovation", icon: IconInnovationScout },
      { href: "/dashboard/pr-crisis-management-engine", label: "PR & Crise", icon: IconPRCrisis },
      { href: "/dashboard/knowledge-gap-skills-analysis-engine", label: "Analyse Compétences", icon: IconKnowledgeGap },
      { href: "/dashboard/certification-standards-tracker-engine", label: "Certifications", icon: IconCertification },
      { href: "/dashboard/personalized-learning-path-engine", label: "Parcours Apprentissage", icon: IconLearningPath },
      { href: "/dashboard/data-protection-engine", label: "Protection Données", icon: IconDataProtection },
      { href: "/dashboard/resource-optimization-capacity-engine", label: "Optimisation Ressources", icon: IconResourceOptimization },
      { href: "/dashboard/organizational-health-culture-engine", label: "Santé Organisationnelle", icon: IconOrgHealth },
      { href: "/dashboard/legal-regulatory-watch-engine", label: "Veille Juridique", icon: IconLegalWatch },
      { href: "/dashboard/quality-assurance-process-engine", label: "Assurance Qualité", icon: IconQualityAssurance },
      { href: "/dashboard/swarm-orchestration-conflict-engine", label: "Orchestration Essaim", icon: IconSwarmOrchestration },
      { href: "/dashboard/continuous-improvement-excellence-engine", label: "Excellence Opérat.", icon: IconContinuousImprovement },
      { href: "/dashboard/strategic-risk-governance-engine", label: "Risque Stratégique", icon: IconStrategicRisk },
      { href: "/dashboard/strategic-foresight-simulation-engine", label: "Anticipation Stratégique", icon: IconForesight },
      { href: "/dashboard/emotional-intelligence-market-behavior-engine", label: "Intelligence Émotionnelle", icon: IconEmotionalIntelligence },
      { href: "/dashboard/logistics-prediction-flow-engine", label: "Prédiction Logistique", icon: IconLogistics },
      { href: "/dashboard/regulatory-compliance-legal-engine", label: "Conformité Réglementaire", icon: IconRegulatoryCompliance },
      { href: "/dashboard/sales-channel-partnership-engine", label: "Canaux de Vente", icon: IconSalesChannel },
      { href: "/dashboard/cultural-chronology-microculture-engine", label: "Chrono-Culture", icon: IconMicroCulture },
      { href: "/dashboard/anthropocene-terraforming-engine", label: "Anthropocène", icon: IconAnthropocene },
      { href: "/dashboard/synthetic-consciousness-alignment-engine", label: "Conscience Synthétique", icon: IconSyntheticConsciousness },
      { href: "/dashboard/singularity-economy-engine", label: "Économie Singularité", icon: IconSingularityEconomy },
      { href: "/dashboard/post-quantum-cryptography-engine", label: "Crypto Post-Quantique", icon: IconPostQuantum },
      { href: "/dashboard/memetic-resonance-engine", label: "Résonance Mémetique", icon: IconMemetic },
      { href: "/dashboard/game-theory-decision-engine", label: "Théorie des Jeux", icon: IconGameTheory },
      { href: "/dashboard/bio-computational-intelligence-engine", label: "Bio-Intelligence", icon: IconBioCompute },
      { href: "/dashboard/complex-network-physics-engine", label: "Physique Réseaux", icon: IconComplexNetwork },
      { href: "/dashboard/digital-sovereignty-engine", label: "Souveraineté Numérique", icon: IconDigitalSovereignty },
      { href: "/dashboard/temporal-intelligence-engine", label: "Intelligence Temporelle", icon: IconTemporalIntelligence },
      { href: "/dashboard/geopolitical-resilience-engine", label: "Résilience Géopolitique", icon: IconGeopolitical },
      { href: "/dashboard/predictive-arbitrage-engine", label: "Arbitrage Algorithmique", icon: IconPredictiveArbitrage },
      { href: "/dashboard/quantum-social-intelligence-engine", label: "Intelligence Sociale", icon: IconQuantumSocial },
      { href: "/dashboard/synthetic-asset-liquidation-engine", label: "Liquidation DeFi", icon: IconSyntheticLiquidation },
      { href: "/dashboard/fractional-ownership-engine", label: "Ownership Fractionné", icon: IconFractionalOwnership },
      { href: "/dashboard/emotional-capital-engine", label: "Capital Émotionnel", icon: IconEmotionalCapital },
      { href: "/dashboard/regenerative-finance-engine", label: "Finance Régénérative", icon: IconRegenFinance },
      { href: "/dashboard/cognitive-warfare-engine", label: "Guerre Cognitive", icon: IconCognitiveWarfare },
      { href: "/dashboard/sovereign-ai-governance-engine", label: "Gouvernance IA", icon: IconSovereignAI },
      { href: "/dashboard/hyperpersonalization-engine", label: "Hyperpersonnalisation", icon: IconHyperpersonalization },
      { href: "/dashboard/information-fluid-dynamics-engine", label: "Dynamique des Fluides", icon: IconFluidDynamics },
      { href: "/dashboard/collective-consciousness-orchestration-engine", label: "Conscience Collective", icon: IconCollectiveConsciousness },
      { href: "/dashboard/augmented-reality-neural-interface-engine", label: "AR & Interface Neuronale", icon: IconARNeural },
      { href: "/dashboard/temporal-engineering-engine", label: "Ingénierie Temporelle", icon: IconTemporalEngineering },
      { href: "/dashboard/neuroadaptive-ux-engine", label: "UX Neuroadaptif", icon: IconNeuroadaptiveUX },
      { href: "/dashboard/autonomous-supply-chain-engine", label: "Supply Chain Auto.", icon: IconSupplyChain },
      { href: "/dashboard/biomimetic-strategy-engine", label: "Stratégie Biomimétique", icon: IconBiomimetic },
      { href: "/dashboard/dark-data-intelligence-engine", label: "Dark Data", icon: IconDarkData },
      { href: "/dashboard/metamorphic-business-model-engine", label: "Modèle Métamorphique", icon: IconMetamorphic },
      { href: "/dashboard/predictive-talent-intelligence-engine", label: "Talent Intelligence", icon: IconPredictiveTalent },
      { href: "/dashboard/planetary-intelligence-engine", label: "Intelligence Planétaire", icon: IconPlanetaryIntel },
      { href: "/dashboard/existential-risk-engine", label: "Risque Existentiel", icon: IconExistentialRisk },
      { href: "/dashboard/quantum-resilience-engine", label: "Résilience Quantique", icon: IconQuantumResilience },
      { href: "/dashboard/bio-digital-convergence-engine", label: "Bio-Digital Convergence", icon: IconBioDigital },
      { href: "/dashboard/neuro-economic-decision-engine", label: "Neuro-Économie", icon: IconNeuroEconomic },
      { href: "/dashboard/civilizational-memory-engine", label: "Mémoire Civilisationnelle", icon: IconCivilizationalMemory },
      { href: "/dashboard/hyperconnectivity-fragility-engine", label: "Hyperconnectivité", icon: IconHyperconnectivity },
      { href: "/dashboard/autonomous-financial-ecosystem-engine", label: "Éco. Financier Auto.", icon: IconAutoFinancial },
      { href: "/dashboard/collective-intelligence-amplification-engine", label: "Intelligence Collective+", icon: IconCollectiveAmplification },
      { href: "/dashboard/sovereign-wealth-intelligence-engine", label: "Fonds Souverains", icon: IconSovereignWealth },
      { href: "/dashboard/post-human-augmentation-engine", label: "Augmentation Post-Humain", icon: IconPostHuman },
      { href: "/dashboard/narrative-control-engine", label: "Contrôle Narratif", icon: IconNarrativeControl },
      { href: "/dashboard/semantic-knowledge-graph-engine", label: "Graphe Sémantique", icon: IconSemanticKG },
      { href: "/dashboard/exponential-tech-convergence-engine", label: "Tech Exponentielle", icon: IconExponentialTech },
      { href: "/dashboard/psychographic-profiling-engine", label: "Profilage Psychographique", icon: IconPsychographic },
      { href: "/dashboard/energy-transition-intelligence-engine", label: "Transition Énergétique", icon: IconEnergyTransition },
      { href: "/dashboard/synthetic-media-detection-engine", label: "Médias Synthétiques", icon: IconSyntheticMedia },
      { href: "/dashboard/longevity-economy-engine", label: "Économie Longévité", icon: IconLongevityEconomy },
      { href: "/dashboard/space-economy-engine", label: "Économie Spatiale", icon: IconSpaceEconomy },
      { href: "/dashboard/crypto-economic-governance-engine", label: "Gouvernance DeFi", icon: IconCryptoGovernance },
      { href: "/dashboard/metacognitive-ai-alignment-engine", label: "Alignement IA", icon: IconAIAlignment },
      { href: "/dashboard/dao-governance-intelligence-engine", label: "Gouvernance DAO", icon: IconDAOGovernance },
      { href: "/dashboard/omega-synthesis-engine", label: "OMEGA Synthèse", icon: IconOmegaSynthesis },
      { href: "/dashboard/autonomous-agent-economy-engine", label: "Économie Agents IA", icon: IconAutonomousEconomy },
      { href: "/dashboard/synthetic-biology-risk-engine", label: "Biologie Synthétique", icon: IconSyntheticBiology },
      { href: "/dashboard/emotional-contagion-engine", label: "Contagion Émotionnelle", icon: IconEmotionalContagion },
      { href: "/dashboard/critical-resource-scarcity-engine", label: "Ressources Critiques", icon: IconCriticalResource },
      { href: "/dashboard/climate-tipping-points-engine", label: "Basculement Climatique", icon: IconClimateTipping },
      { href: "/dashboard/digital-twin-economy-engine", label: "Jumeaux Numériques", icon: IconDigitalTwin },
      { href: "/dashboard/quantum-computing-disruption-engine", label: "Disruption Quantique", icon: IconQuantumDisruption },
      { href: "/dashboard/urban-intelligence-engine", label: "Intelligence Urbaine", icon: IconUrbanIntel },
      { href: "/dashboard/sovereign-debt-crisis-engine", label: "Crise Dette Souveraine", icon: IconSovereignDebt },
      { href: "/dashboard/neuromorphic-bci-engine", label: "Interface Cerveau-Machine", icon: IconNeuroBCI },
      { href: "/dashboard/supply-chain-fragility-engine", label: "Fragilité Chaîne Appro.", icon: IconSupplyChain },
      { href: "/dashboard/geopolitical-alliance-fracture-engine", label: "Fractures Alliances", icon: IconAllianceFracture },
      { href: "/dashboard/first-principles-architecture-engine", label: "Premiers Principes", icon: IconFirstPrinciples },
      { href: "/dashboard/bottleneck-sniper-engine", label: "Bottleneck Sniper", icon: IconBottleneckSniper },
      { href: "/dashboard/economic-singularity-engine", label: "Singularité Économique", icon: IconEconomicSingularity },
      { href: "/dashboard/system-awareness-engine", label: "Conscience Systémique", icon: IconSystemAwareness },
      { href: "/dashboard/dark-pattern-manipulation-engine", label: "Dark Patterns", icon: IconDarkPattern },
      { href: "/dashboard/water-geopolitics-engine", label: "Géopolitique de l'Eau", icon: IconWaterGeo },
      { href: "/dashboard/food-system-collapse-engine", label: "Effondrement Alimentaire", icon: IconFoodSystem },
      { href: "/dashboard/pension-collapse-engine", label: "Effondrement Retraites", icon: IconPension },
      { href: "/dashboard/metacognitive-bias-engine", label: "Biais Métacognitifs", icon: IconCognitiveBias },
      { href: "/dashboard/techno-feudalism-engine", label: "Techno-Féodalisme", icon: IconTechnoFeudal },
      { href: "/dashboard/cognitive-warfare-engine-v2", label: "Guerre Cognitive", icon: IconCognitiveWarfare },
      { href: "/dashboard/longevity-tech-engine", label: "Tech Longévité", icon: IconLongevityTech },
      { href: "/dashboard/pandemic-intelligence-engine", label: "Intelligence Pandémique", icon: IconPandemic },
      { href: "/dashboard/nuclear-risk-engine", label: "Risque Nucléaire", icon: IconNuclear },
      { href: "/dashboard/ocean-intelligence-engine", label: "Intelligence Océanique", icon: IconOcean },
      { href: "/dashboard/soft-power-hegemony-engine", label: "Puissance Douce", icon: IconSoftPower },
      { href: "/dashboard/circular-economy-engine", label: "Économie Circulaire", icon: IconCircularEconomy },
      { href: "/dashboard/digital-democracy-engine", label: "Démocratie Numérique", icon: IconDigitalDemocracy },
      { href: "/dashboard/space-economy-sovereignty-engine", label: "Économie Spatiale", icon: IconSpaceEconomy },
      { href: "/dashboard/behavioral-finance-engine", label: "Finance Comportementale", icon: IconBehavioralFinance },
      { href: "/dashboard/biometric-surveillance-engine", label: "Surveillance Biométrique", icon: IconBiometricSurveillance },
      { href: "/dashboard/gig-economy-fragility-engine", label: "Économie Gig", icon: IconGigEconomy },
      { href: "/dashboard/surveillance-capitalism-engine", label: "Capitalisme Surveillance", icon: IconSurveillanceCap },
      { href: "/dashboard/neural-language-dominance-engine", label: "Dominance Linguistique", icon: IconNeuralLanguage },
      { href: "/dashboard/military-ai-engine", label: "IA Militaire", icon: IconMilitaryAI },
      { href: "/dashboard/migration-crisis-engine", label: "Crise Migratoire", icon: IconMigrationCrisis },
      { href: "/dashboard/corporate-capture-engine", label: "Capture Corporative", icon: IconCorporateCapture },
      { href: "/dashboard/epigenetic-health-engine", label: "Santé Épigénétique", icon: IconEpigeneticHealth },
      { href: "/dashboard/cultural-heritage-engine", label: "Patrimoine Culturel", icon: IconCulturalHeritage },
      { href: "/dashboard/hypersonic-weapons-engine", label: "Armes Hypersoniques", icon: IconHypersonic },
      { href: "/dashboard/wealth-concentration-engine", label: "Concentration Richesses", icon: IconWealthConcentration },
      { href: "/dashboard/psychopolitics-engine", label: "Psychopolitique", icon: IconPsychopolitics },
      { href: "/dashboard/methane-crisis-engine", label: "Crise Méthane", icon: IconMethaneCrisis },
      { href: "/dashboard/algorithmic-justice-engine", label: "Justice Algorithmique", icon: IconAlgorithmicJustice },
      { href: "/dashboard/rare-earth-intelligence-engine", label: "Terres Rares", icon: IconRareEarth },
      { href: "/dashboard/social-credit-engine", label: "Crédit Social", icon: IconSocialCredit },
      { href: "/dashboard/alternative-protein-engine", label: "Protéines Alternatives", icon: IconAltProtein },
      { href: "/dashboard/generative-ai-economy-engine", label: "IA Générative Éco.", icon: IconGenAIEconomy },
      { href: "/dashboard/infrastructure-resilience-engine", label: "Résilience Infra.", icon: IconInfraResilience },
      { href: "/dashboard/financial-crime-engine", label: "Crime Financier", icon: IconFinancialCrime },
      { href: "/dashboard/digital-twins-infrastructure-engine", label: "Jumeaux Numériques", icon: IconDigitalTwins },
      { href: "/dashboard/urban-heat-engine", label: "Chaleur Urbaine", icon: IconUrbanHeat },
      { href: "/dashboard/misinformation-ecosystem-engine", label: "Désinformation", icon: IconMisinformation },
      { href: "/dashboard/soil-degradation-engine", label: "Dégradation Sols", icon: IconSoilDegradation },
      { href: "/dashboard/cyber-sovereignty-engine", label: "Souveraineté Cyber", icon: IconCyberSovereignty },
      { href: "/dashboard/antibiotic-resistance-engine", label: "Résistance Antibio.", icon: IconAntibioticResistance },
      { href: "/dashboard/climate-finance-engine", label: "Finance Climatique", icon: IconClimateFinance },
      { href: "/dashboard/ai-governance-engine", label: "Gouvernance IA", icon: IconAIGovernance },
      { href: "/dashboard/demographic-winter-engine", label: "Hiver Démographique", icon: IconDemographicWinter },
      { href: "/dashboard/satellite-constellation-engine", label: "Constellations Sat.", icon: IconSatelliteConstellation },
      { href: "/dashboard/defi-systemic-risk-engine", label: "Risque Systémique DeFi", icon: IconDeFiRisk },
      { href: "/dashboard/cognitive-enhancement-engine", label: "Amélioration Cognitive", icon: IconCognitiveEnhancement },
      { href: "/dashboard/tax-justice-engine", label: "Justice Fiscale", icon: IconTaxJustice },
      { href: "/dashboard/arctic-sovereignty-engine", label: "Souveraineté Arctique", icon: IconArcticSovereignty },
      { href: "/dashboard/quantum-economic-disruption-engine", label: "Disruption Quantique", icon: IconQuantumDisruption },
      { href: "/dashboard/digital-health-sovereignty-engine", label: "Santé Numérique Souv.", icon: IconDigitalHealthSov },
      { href: "/dashboard/carbon-credit-engine", label: "Marchés Carbone", icon: IconCarbonCredit },
      { href: "/dashboard/space-debris-engine", label: "Débris Spatiaux", icon: IconSpaceDebris },
      { href: "/dashboard/digital-colonialism-engine", label: "Colonialisme Numérique", icon: IconDigitalColonialism },
      { href: "/dashboard/ocean-acidification-engine", label: "Acidification Océanique", icon: IconOceanAcidification },
      { href: "/dashboard/nuclear-fusion-engine", label: "Fusion Nucléaire", icon: IconNuclearFusion },
      { href: "/dashboard/post-work-ubi-engine", label: "Société Post-Travail", icon: IconPostWork },
      { href: "/dashboard/geoengineering-engine", label: "Géoingénierie", icon: IconGeoengineering },
      { href: "/dashboard/digital-identity-engine", label: "Identité Numérique", icon: IconDigitalIdentity },
      { href: "/dashboard/gene-drive-engine", label: "Gene Drive Extinction", icon: IconGeneDrive },
      { href: "/dashboard/synthetic-reality-engine", label: "Réalité Synthétique", icon: IconSyntheticReality },
      { href: "/dashboard/energy-poverty-engine", label: "Pauvreté Énergétique", icon: IconEnergyPoverty },
      { href: "/dashboard/battery-geopolitics-engine", label: "Géopolitique Batteries", icon: IconBatteryGeopolitics },
      { href: "/dashboard/corporate-surveillance-engine", label: "Surveillance Corp.", icon: IconCorporateSurveillance },
      { href: "/dashboard/global-health-security-engine", label: "Sécurité Sanitaire", icon: IconGlobalHealthSecurity },
      { href: "/dashboard/industrial-policy-engine", label: "Politique Industrielle", icon: IconIndustrialPolicy },
      { href: "/dashboard/dark-web-economy-engine", label: "Économie Dark Web", icon: IconDarkWebEconomy },
      { href: "/dashboard/refugee-crisis-engine", label: "Crise Réfugiés", icon: IconRefugeeCrisis },
      { href: "/dashboard/crypto-regulation-engine", label: "Régulation Crypto", icon: IconCryptoRegulation },
      { href: "/dashboard/food-security-engine", label: "Sécurité Alimentaire", icon: IconFoodSecurity },
      { href: "/dashboard/smart-city-engine", label: "Ville Intelligente", icon: IconSmartCity },
      { href: "/dashboard/ip-warfare-engine", label: "Guerre PI", icon: IconIPWarfare },
      { href: "/dashboard/deep-sea-mining-engine", label: "Mines Fond Marin", icon: IconDeepSeaMining },
      { href: "/dashboard/biosurveillance-engine", label: "Biosurveillance", icon: IconBiosurveillance },
      { href: "/dashboard/aging-infrastructure-engine", label: "Infra Vieillissante", icon: IconAgingInfra },
      { href: "/dashboard/worker-automation-engine", label: "Automatisation Emplois", icon: IconWorkerAutomation },
      { href: "/dashboard/autonomous-vehicle-engine", label: "Véhicules Autonomes", icon: IconAutonomousVehicle },
      { href: "/dashboard/cbdc-sovereignty-engine", label: "CBDC Souveraineté", icon: IconCBDC },
      { href: "/dashboard/reproductive-rights-engine", label: "Droits Reproductifs", icon: IconReproductiveRights },
      { href: "/dashboard/supply-chain-esg-engine", label: "ESG Chaîne Appro.", icon: IconSupplyChainESG },
      { href: "/dashboard/noise-pollution-engine", label: "Pollution Sonore", icon: IconNoisePollution },
      { href: "/dashboard/crypto-mining-engine", label: "Minage Crypto Env.", icon: IconCryptoMining },
      { href: "/dashboard/metaverse-governance-engine", label: "Gouvernance Métavers", icon: IconMetaverse },
      { href: "/dashboard/nuclear-waste-engine", label: "Déchets Nucléaires", icon: IconNuclearWaste },
      { href: "/dashboard/ocean-plastic-engine", label: "Plastique Océanique", icon: IconOceanPlastic },
      { href: "/dashboard/land-grab-engine", label: "Accaparement Terres", icon: IconLandGrab },
      { href: "/dashboard/water-privatization-engine", label: "Privatisation Eau", icon: IconWaterPrivatization },
      { href: "/dashboard/tax-haven-engine", label: "Paradis Fiscaux", icon: IconTaxHaven },
      { href: "/dashboard/autonomous-weapons-engine", label: "Armes Autonomes IA", icon: IconAutonomousWeapons },
      { href: "/dashboard/space-weather-engine", label: "Météo Spatiale", icon: IconSpaceWeather },
      { href: "/dashboard/platform-economy-engine", label: "Économie Plateforme", icon: IconPlatformEconomy },
      { href: "/dashboard/soil-carbon-engine", label: "Carbone Sol Agricole", icon: IconSoilCarbon },
      { href: "/dashboard/urban-mining-engine", label: "Minage Urbain Recyclage", icon: IconUrbanMining },
      { href: "/dashboard/pharmaceutical-access-engine", label: "Accès Médicaments", icon: IconPharmaceutical },
      { href: "/dashboard/algae-energy-engine", label: "Énergie Algues Bio", icon: IconAlgaeEnergy },
      { href: "/dashboard/carbon-border-engine", label: "Mécanisme Carbone Frontière", icon: IconCarbonBorder },
      { href: "/dashboard/social-bond-engine", label: "Obligations Sociales ESG", icon: IconSocialBond },
      { href: "/dashboard/digital-divide-engine", label: "Fracture Numérique", icon: IconDigitalDivide },
      { href: "/dashboard/neuro-rights-engine", label: "Neurodroits IA", icon: IconNeuroRights },
      { href: "/dashboard/wildfire-intelligence-engine", label: "Incendies Forêts", icon: IconWildfire },
      { href: "/dashboard/forced-labor-engine", label: "Travail Forcé Esclavage", icon: IconForcedLabor },
      { href: "/dashboard/child-marriage-engine", label: "Mariage Forcé Enfants", icon: IconChildMarriage },
      { href: "/dashboard/ocean-governance-engine", label: "Gouvernance Océans", icon: IconOceanGovernance },
      { href: "/dashboard/critical-infra-cyber-engine", label: "Cyber Infra Critique", icon: IconCriticalInfraCyber },
      { href: "/dashboard/housing-crisis-engine", label: "Crise Immobilière", icon: IconHousingCrisis },
      { href: "/dashboard/climate-migration-engine", label: "Migration Climatique", icon: IconClimateMigration },
      { href: "/dashboard/coral-reef-engine", label: "Récifs Coralliens", icon: IconCoralReef },
      { href: "/dashboard/lithium-battery-recycling-engine", label: "Recyclage Batteries Li", icon: IconLithiumRecycling },
      { href: "/dashboard/microplastics-health-engine", label: "Microplastiques Santé", icon: IconMicroplastics },
      { href: "/dashboard/insurance-climate-engine", label: "Assurance Climat", icon: IconInsuranceClimate },
      { href: "/dashboard/academic-integrity-engine", label: "Intégrité Académique", icon: IconAcademicIntegrity },
      { href: "/dashboard/urban-flooding-engine", label: "Inondations Urbaines", icon: IconUrbanFlooding },
      { href: "/dashboard/digital-nomad-engine", label: "Économie Nomades Numériques", icon: IconDigitalNomad },
      { href: "/dashboard/genetic-privacy-engine", label: "Confidentialité Génétique", icon: IconGeneticPrivacy },
      { href: "/dashboard/sovereign-wealth-engine", label: "Fonds Souverains Pouvoir", icon: IconSovereignWealth },
      { href: "/dashboard/permafrost-methane-engine", label: "Pergélisol Méthane Arctique", icon: IconPermafrostMethane },
      { href: "/dashboard/food-waste-economy-engine", label: "Gaspillage Alimentaire", icon: IconFoodWaste },
      { href: "/dashboard/rare-disease-engine", label: "Maladies Rares & Médicaments", icon: IconRareDisease },
      { href: "/dashboard/child-online-safety-engine", label: "Sécurité Enfants Numérique", icon: IconChildOnlineSafety },
      { href: "/dashboard/psychedelic-medicine-engine", label: "Médecine Psychédélique", icon: IconPsychedelicMedicine },
      { href: "/dashboard/nuclear-disarmament-engine", label: "Désarmement Nucléaire", icon: IconNuclearDisarmament },
      { href: "/dashboard/urban-air-mobility-engine", label: "Mobilité Aérienne Urbaine", icon: IconUrbanAirMobility },
      { href: "/dashboard/media-integrity-engine", label: "Intégrité Médias & DeepFakes", icon: IconMediaIntegrity },
      { href: "/dashboard/pandemic-preparedness-engine", label: "Préparation Pandémies", icon: IconPandemicPrep },
      { href: "/dashboard/global-tax-reform-engine", label: "Réforme Fiscale Mondiale", icon: IconGlobalTaxReform },
      { href: "/dashboard/prison-reform-engine", label: "Réforme Pénale & Justice", icon: IconPrisonReform },
      { href: "/dashboard/amr-global-response-engine", label: "Résistance Antimicrobiens", icon: IconAMRResponse },
      { href: "/dashboard/transhumanist-ethics-engine", label: "Éthique Transhumaniste", icon: IconTranshumanistEthics },
      { href: "/dashboard/vertical-farming-engine", label: "Agriculture Verticale", icon: IconVerticalFarming },
      { href: "/dashboard/social-media-mental-health-engine", label: "Réseaux Sociaux Santé Mentale", icon: IconSocialMediaMentalHealth },
      { href: "/dashboard/clean-water-access-engine", label: "Accès Eau Potable", icon: IconCleanWaterAccess },
      { href: "/dashboard/land-degradation-engine", label: "Dégradation Terres & Désert.", icon: IconLandDegradation },
      { href: "/dashboard/elder-care-crisis-engine", label: "Crise Soins Personnes Âgées", icon: IconElderCare },
      { href: "/dashboard/dark-patterns-engine", label: "Dark Patterns Manipulation", icon: IconDarkPatterns },
      { href: "/dashboard/biopiracy-engine", label: "Biopiraterie & Savoirs Trad.", icon: IconBiopiracy },
      { href: "/dashboard/electoral-integrity-engine", label: "Intégrité Électorale", icon: IconElectoralIntegrity },
      { href: "/dashboard/platform-labor-rights-engine", label: "Droits Travailleurs Plateforme", icon: IconPlatformLabor },
      { href: "/dashboard/crypto-financial-crime-engine", label: "Criminalité Financière Crypto", icon: IconCryptoFinancialCrime },
      { href: "/dashboard/arctic-sovereignty-race-engine", label: "Souveraineté Arctique", icon: IconArcticSovereigntyRace },
      { href: "/dashboard/refugee-integration-engine", label: "Intégration Réfugiés", icon: IconRefugeeIntegration },
      { href: "/dashboard/esg-greenwash-engine", label: "ESG Greenwashing Détection", icon: IconESGGreenwash },
      { href: "/dashboard/telemedicine-engine", label: "Télémédecine & Accès Santé", icon: IconTelemedicine },
      { href: "/dashboard/ai-bias-engine", label: "Biais IA & Discrimination", icon: IconAIBias },
      { href: "/dashboard/supply-chain-transparency-engine", label: "Traçabilité Chaîne Appro.", icon: IconSupplyChainTransparency },
      { href: "/dashboard/drug-trafficking-engine", label: "Trafic Drogues & Réseaux", icon: IconDrugTrafficking },
      { href: "/dashboard/food-system-sovereignty-engine", label: "Souveraineté Alimentaire", icon: IconFoodSystemSovereignty },
      { href: "/dashboard/digital-health-sovereignty-engine", label: "Souveraineté Santé Digitale", icon: IconDigitalHealthSovereignty },
      { href: "/dashboard/nps-satisfaction", label: "Satisfaction & NPS", icon: IconNPS },
      { href: "/dashboard/seo-ranking", label: "SEO & Positionnement", icon: IconSEORanking },
      { href: "/dashboard/client-retention", label: "Rétention Client", icon: IconClientRetention },
      { href: "/dashboard/upsell-opportunity", label: "Opportunités Upsell", icon: IconUpsellOpportunity },
      { href: "/dashboard/social-media-roi", label: "ROI Réseaux Sociaux", icon: IconSocialROI },
      { href: "/dashboard/agent-orchestrator", label: "Orchestrateur Agents IA", icon: IconAgentOrchestrator },
      { href: "/dashboard/hybrid-infrastructure", label: "Infrastructure Hybride", icon: IconHybridInfra },
      { href: "/dashboard/polycrisis-engine", label: "Polycrise Mondiale", icon: IconPolycrisis },
      { href: "/dashboard/black-swan-engine", label: "Cygne Noir — Risques Extrêmes", icon: IconBlackSwan },
      { href: "/dashboard/caelum-synthesis-engine", label: "Synthèse Méta-Intelligence", icon: IconCaelumSynthesis },
      { href: "/dashboard/antifragility-index-engine", label: "Indice d'Antifragilité", icon: IconAntifragility },
      { href: "/dashboard/civilizational-debt-engine", label: "Dette Civilisationnelle", icon: IconCivDebt },
      { href: "/dashboard/nexus-crisis-engine", label: "Nexus Eau-Alimentation-Énergie", icon: IconNexusCrisis },
      { href: "/dashboard/democratic-decay-engine", label: "Érosion Démocratique", icon: IconDemocraticDecay },
      { href: "/dashboard/economic-coercion-engine", label: "Coercition Économique", icon: IconEconomicCoercion },
      { href: "/dashboard/social-cohesion-engine", label: "Cohésion Sociale", icon: IconSocialCohesion },
      { href: "/dashboard/trust-economy-engine", label: "Capital-Confiance Mondial", icon: IconTrustEconomy },
      { href: "/dashboard/epistemic-security-engine", label: "Sécurité Épistémique", icon: IconEpistemicSecurity },
      { href: "/dashboard/attention-economy-engine", label: "Économie de l'Attention", icon: IconAttentionEconomy },
      { href: "/dashboard/hybrid-warfare-engine", label: "Guerre Hybride & Zone Grise", icon: IconHybridWarfare },
      { href: "/dashboard/sovereign-ai-engine", label: "Souveraineté IA Nationale", icon: IconSovereignAIEngine },
      { href: "/dashboard/complexity-horizon-engine", label: "Horizon de Complexité", icon: IconComplexityHorizonEngine },
      { href: "/dashboard/longevity-inequality-engine", label: "Inégalité de Longévité", icon: IconLongevityInequalityEngine },
      { href: "/dashboard/narrative-sovereignty-engine", label: "Souveraineté Narrative", icon: IconNarrativeSovereignty },
      { href: "/dashboard/biopower-engine", label: "Bio-Pouvoir & Corps", icon: IconBioPower },
      { href: "/dashboard/techno-darwinism-engine", label: "Techno-Darwinisme", icon: IconTechnoDarwinism },
      { href: "/dashboard/resource-curse-engine", label: "Malédiction des Ressources", icon: IconResourceCurse },
      { href: "/dashboard/shadow-economy-engine", label: "Économie de l'Ombre", icon: IconShadowEconomy },
      { href: "/dashboard/ai-alignment-risk-engine", label: "Risque Alignement IA", icon: IconAIAlignmentRisk },
      { href: "/dashboard/treaty-erosion-engine", label: "Érosion Ordre International", icon: IconTreatyErosion },
      { href: "/dashboard/linguistic-sovereignty-engine", label: "Souveraineté Linguistique", icon: IconLinguisticSovereignty },
      { href: "/dashboard/power-vacuum-engine", label: "Vides de Pouvoir", icon: IconPowerVacuum },
      { href: "/dashboard/seed-sovereignty-engine", label: "Souveraineté Semencière", icon: IconSeedSovereignty },
      { href: "/dashboard/academic-freedom-engine", label: "Liberté Académique", icon: IconAcademicFreedom },
      { href: "/dashboard/financial-contagion-engine", label: "Contagion Financière", icon: IconFinancialContagion },
      { href: "/dashboard/biosafety-infrastructure-engine", label: "Infrastructure Biosécurité", icon: IconBiosafetyInfrastructure },
      { href: "/dashboard/famine-weaponization-engine", label: "Arme Famine", icon: IconFamineWeaponization },
      { href: "/dashboard/diaspora-geopolitics-engine", label: "Géopolitique Diasporas", icon: IconDiasporaGeopolitics },
      { href: "/dashboard/maternal-mortality-engine", label: "Mortalité Maternelle", icon: IconMaternalMortality },
      { href: "/dashboard/small-arms-proliferation-engine", label: "Prolifération ALPC", icon: IconSmallArmsProliferation },
      { href: "/dashboard/debt-trap-diplomacy-engine", label: "Diplomatie Dette BRI", icon: IconDebtTrapDiplomacy },
      { href: "/dashboard/youth-bulge-engine", label: "Youth Bulge & Instabilité", icon: IconYouthBulge },
      { href: "/dashboard/rare-earth-dominance-engine", label: "Domination Terres Rares", icon: IconRareEarthDominance },
      { href: "/dashboard/pension-crisis-engine", label: "Crise des Retraites", icon: IconPensionCrisis },
      { href: "/dashboard/electoral-interference-engine", label: "Ingérence Électorale", icon: IconElectoralInterference },
      { href: "/dashboard/urban-heat-crisis-engine", label: "Crise Chaleur Urbaine", icon: IconUrbanHeatCrisis },
      { href: "/dashboard/criminal-state-capture-engine", label: "Capture Criminelle État", icon: IconCriminalStateCapture },
      { href: "/dashboard/space-militarization-engine", label: "Space Militarization", icon: IconSpaceMilitarization },
      { href: "/dashboard/algorithmic-surveillance-engine", label: "Algorithmic Surveillance", icon: IconAlgorithmicSurveillance },
      { href: "/dashboard/refugee-weaponization-engine", label: "Refugee Weaponization", icon: IconRefugeeWeaponization },
      { href: "/dashboard/water-wars-engine", label: "Water Wars", icon: IconWaterWars },
      { href: "/dashboard/quantum-race-engine", label: "Quantum Race", icon: IconQuantumRace },
      { href: "/dashboard/arctic-geopolitics-engine", label: "Arctic Geopolitics", icon: IconArcticGeopolitics },
      { href: "/dashboard/diaspora-weaponization-engine", label: "Diaspora Weaponization", icon: IconDiasporaWeaponizationEngine },
      { href: "/dashboard/sportwashing-geopolitics-engine", label: "Sportwashing Geopolitics", icon: IconSportwashingGeopoliticsEngine },
      { href: "/dashboard/mercenary-warfare-engine", label: "Mercenary Warfare", icon: IconMercenaryWarfare },
      { href: "/dashboard/deep-sea-mining-engine", label: "Deep Sea Mining", icon: IconDeepSeaMiningEngine },
      { href: "/dashboard/food-weaponization-engine", label: "Food Weaponization", icon: IconFoodWeaponization },
      { href: "/dashboard/ai-weapons-race-engine", label: "AI Weapons Race", icon: IconAIWeaponsRace },
      { href: "/dashboard/port-logistics-capture-engine", label: "Port Logistics Capture", icon: IconPortLogisticsCapture },
      { href: "/dashboard/nuclear-deterrence-engine", label: "Nuclear Deterrence", icon: IconNuclearDeterrence },
      { href: "/dashboard/sanctions-evasion-engine", label: "Sanctions Evasion", icon: IconSanctionsEvasion },
      { href: "/dashboard/pandemic-bioweapons-engine", label: "Pandemic Bioweapons", icon: IconPandemicBioweapons },
      { href: "/dashboard/semiconductor-war-engine", label: "Semiconductor War", icon: IconSemiconductorWar },
      { href: "/dashboard/currency-war-engine", label: "Currency War", icon: IconCurrencyWar },
      { href: "/dashboard/undersea-cable-engine", label: "Undersea Cable", icon: IconUnderseaCable },
      { href: "/dashboard/lawfare-engine", label: "Lawfare Engine", icon: IconLawfare },
      { href: "/dashboard/ai-surveillance-autocracy-engine", label: "AI Surveillance Autocracy", icon: IconAISurveillance },
      { href: "/dashboard/transnational-crime-engine", label: "Transnational Crime", icon: IconTransnationalCrime },
      { href: "/dashboard/space-warfare-engine", label: "Space Warfare", icon: IconSpaceWarfare },
      { href: "/dashboard/food-security-weaponization-engine", label: "Food Security Weaponization", icon: IconFoodSecurity },
      { href: "/dashboard/climate-geopolitics-engine", label: "Climate Geopolitics", icon: IconClimateGeopolitics },
      { href: "/dashboard/organ-trafficking-engine", label: "Organ Trafficking", icon: IconOrganTrafficking },
      { href: "/dashboard/gender-apartheid-engine", label: "Gender Apartheid", icon: IconGenderApartheid },
      { href: "/dashboard/maritime-piracy-engine", label: "Maritime Piracy", icon: IconMaritimePiracy },
      { href: "/dashboard/child-soldiers-engine", label: "Child Soldiers", icon: IconChildSoldiers },
      { href: "/dashboard/cultural-genocide-engine", label: "Cultural Genocide", icon: IconCulturalGenocide },
      { href: "/dashboard/state-terrorism-engine", label: "State Terrorism", icon: IconStateTerrorism },
      { href: "/dashboard/ecocide-engine", label: "Écocide", icon: IconEcocide },
      { href: "/dashboard/forced-sterilization-engine", label: "Stérilisations Forcées", icon: IconForcedSterilization },
      { href: "/dashboard/political-assassination-engine", label: "Assassinats Politiques", icon: IconPoliticalAssassination },
      { href: "/dashboard/drone-warfare-engine", label: "Drones Guerre", icon: IconDroneWarfare },
      { href: "/dashboard/ethnic-cleansing-engine", label: "Nettoyage Ethnique", icon: IconEthnicCleansing },
      { href: "/dashboard/religious-persecution-engine", label: "Persécution Religieuse", icon: IconReligiousPersecution },
      { href: "/dashboard/human-trafficking-engine", label: "Traite Humaine", icon: IconHumanTrafficking },
      { href: "/dashboard/antipersonnel-mines-engine", label: "Mines Antipersonnel", icon: IconAntipersonnelMines },
      { href: "/dashboard/femicide-engine", label: "Féminicides", icon: IconFemicide },
      { href: "/dashboard/war-crimes-siege-engine", label: "War Crimes Siege", icon: IconWarCrimes },
      { href: "/dashboard/internet-shutdown-engine", label: "Internet Shutdown", icon: IconInternetShutdown },
      { href: "/dashboard/refugee-refoulement-engine", label: "Refugee Refoulement", icon: IconRefugeeRefoulement },
      { href: "/dashboard/proxy-warfare-engine", label: "Proxy Warfare", icon: IconProxyWarfare },
      { href: "/dashboard/transnational-repression-engine", label: "Transnational Repression", icon: IconTransnationalRepression },
      { href: "/dashboard/nuclear-blackmail-engine", label: "Nuclear Blackmail", icon: IconNuclearBlackmail },
      { href: "/dashboard/forced-disappearance-engine", label: "Forced Disappearance", icon: IconForcedDisappearance },
      { href: "/dashboard/cultural-property-looting-engine", label: "Cultural Property", icon: IconCulturalProperty },
      { href: "/dashboard/psychological-warfare-engine", label: "Psychological Warfare", icon: IconPsychologicalWarfare },
      { href: "/dashboard/environmental-racism-engine", label: "Environmental Racism", icon: IconEnvironmentalRacism },
      { href: "/dashboard/water-weaponization-engine", label: "Water Weaponization", icon: IconWaterWeaponization },
      { href: "/dashboard/journalist-murder-engine", label: "Journalist Murder", icon: IconJournalistMurder },
      { href: "/dashboard/prison-torture-engine", label: "Prison Torture", icon: IconPrisonTorture },
      { href: "/dashboard/statelessness-engine", label: "Statelessness", icon: IconStatelessness },
      { href: "/dashboard/caste-discrimination-engine", label: "Caste Discrimination", icon: IconCasteDiscrimination },
      { href: "/dashboard/sexual-violence-wartime-engine", label: "Sexual Violence Wartime", icon: IconSexualViolenceWartime },
      { href: "/dashboard/police-brutality-engine", label: "Police Brutality", icon: IconPoliceBrutality },
      { href: "/dashboard/colonial-reparations-engine", label: "Colonial Reparations", icon: IconColonialReparationsLegacy },
      { href: "/dashboard/hate-crime-engine", label: "Hate Crime", icon: IconHateCrime },
      { href: "/dashboard/child-labor-engine", label: "Child Labor", icon: IconChildLabor },
      { href: "/dashboard/indigenous-land-rights-engine", label: "Indigenous Land Rights", icon: IconIndigenousLandRights },
      { href: "/dashboard/debt-bondage-engine", label: "Debt Bondage", icon: IconDebtBondage },
      { href: "/dashboard/arms-embargo-violation-engine", label: "Arms Embargo", icon: IconArmsEmbargoViolation },
      { href: "/dashboard/minority-rights-engine", label: "Minority Rights", icon: IconMinorityRights },
      { href: "/dashboard/lgbtq-rights-engine", label: "LGBTQ+ Rights", icon: IconLgbtqRights },
      { href: "/dashboard/right-to-education-engine", label: "Right to Education", icon: IconRightToEducation },
      { href: "/dashboard/migrant-worker-rights-engine", label: "Migrant Worker Rights", icon: IconMigrantWorkerRights },
      { href: "/dashboard/freedom-of-assembly-engine", label: "Freedom of Assembly", icon: IconFreedomOfAssembly },
      { href: "/dashboard/arbitrary-detention-engine", label: "Arbitrary Detention", icon: IconArbitraryDetention },
      { href: "/dashboard/disability-rights-engine", label: "Disability Rights", icon: IconDisabilityRights },
      { href: "/dashboard/press-freedom-engine", label: "Press Freedom", icon: IconPressFreedom },
      { href: "/dashboard/right-to-health-engine", label: "Right to Health", icon: IconRightToHealth },
      { href: "/dashboard/domestic-violence-engine", label: "Domestic Violence", icon: IconDomesticViolence },
      { href: "/dashboard/water-rights-engine", label: "Water Rights", icon: IconWaterRights },
      { href: "/dashboard/housing-rights-engine", label: "Housing Rights", icon: IconHousingRights },
      { href: "/dashboard/ai-surveillance-rights-engine", label: "Surveillance IA", icon: IconAISurveillanceRights },
      { href: "/dashboard/older-persons-rights-engine", label: "Droits Personnes Âgées", icon: IconOlderPersonsRights },
      { href: "/dashboard/mental-health-rights-engine", label: "Santé Mentale", icon: IconMentalHealthRightsW78 },
      { href: "/dashboard/debt-bondage-rights-engine", label: "Servitude Dette", icon: IconDebtBondageRights },
      { href: "/dashboard/gig-economy-rights-engine", label: "Économie Gig", icon: IconGigEconomyRights },
      { href: "/dashboard/enforced-disappearances-engine", label: "Disparitions Forcées", icon: IconEnforcedDisappearances },
      { href: "/dashboard/child-soldiers-rights-engine", label: "Enfants Soldats", icon: IconChildSoldiersRights },
      { href: "/dashboard/social-protection-engine", label: "Social Protection", icon: IconSocialProtection },
      { href: "/dashboard/racial-justice-engine", label: "Justice Raciale", icon: IconRacialJustice },
      { href: "/dashboard/digital-rights-engine", label: "Droits Numériques", icon: IconDigitalRights },
      { href: "/dashboard/climate-justice-engine", label: "Justice Climatique", icon: IconClimateJustice },
      { href: "/dashboard/economic-rights-engine", label: "Droits Économiques", icon: IconEconomicRights },
      { href: "/dashboard/child-rights-engine", label: "Droits Enfants", icon: IconChildRights },
      { href: "/dashboard/refugee-rights-engine", label: "Droits Réfugiés", icon: IconRefugeeRights },
      { href: "/dashboard/anti-torture-engine", label: "Anti-Torture", icon: IconAntiTorture },
      { href: "/dashboard/transitional-justice-engine", label: "Justice Transitionnelle", icon: IconTransitionalJustice },
      { href: "/dashboard/electoral-rights-engine", label: "Droits Électoraux", icon: IconElectoralRights },
      { href: "/dashboard/death-penalty-engine", label: "Peine de Mort", icon: IconDeathPenalty },
      { href: "/dashboard/indigenous-rights-engine", label: "Droits Autochtones", icon: IconIndigenousRights },
      { href: "/dashboard/corporate-accountability-engine", label: "Responsabilité Corp.", icon: IconCorporateAccountability },
      { href: "/dashboard/right-to-privacy-engine", label: "Droit à la Vie Privée", icon: IconRightToPrivacy },
      { href: "/dashboard/access-to-justice-engine", label: "Accès à la Justice", icon: IconAccessToJustice },
      { href: "/dashboard/human-rights-defenders-engine", label: "Défenseurs DH", icon: IconHumanRightsDefenders },
      { href: "/dashboard/gender-based-violence-engine", label: "Violence de Genre", icon: IconGenderBasedViolence },
      { href: "/dashboard/right-to-food-engine", label: "Droit à l'Alimentation", icon: IconRightToFood },
      { href: "/dashboard/anti-corruption-engine", label: "Anti-Corruption", icon: IconAntiCorruption },
      { href: "/dashboard/minority-language-rights-engine", label: "Langues Minoritaires", icon: IconMinorityLanguageRights },
      { href: "/dashboard/arms-transfer-accountability-engine", label: "Transferts d'Armes", icon: IconArmsTransferAccountability },
      { href: "/dashboard/right-to-development-engine", label: "Droit au Développement", icon: IconRightToDevelopment },
      { href: "/dashboard/environmental-rights-engine", label: "Droits Environnementaux", icon: IconEnvironmentalRights },
      { href: "/dashboard/bioethics-rights-engine", label: "Droits Bioéthique", icon: IconBioethicsRights },
      { href: "/dashboard/birth-registration-engine", label: "Enregistrement Naissance", icon: IconBirthRegistration },
      { href: "/dashboard/migrant-domestic-workers-engine", label: "Travailleurs Domestiques", icon: IconMigrantDomesticWorkers },
      { href: "/dashboard/bioethics-engine", label: "Bioéthique", icon: IconBioethics },
      { href: "/dashboard/sex-work-rights-engine", label: "Droits Travail Sexuel", icon: IconSexWorkRights },
      { href: "/dashboard/environmental-defenders-engine", label: "Défenseurs Environnement", icon: IconEnvironmentalDefenders },
      { href: "/dashboard/climate-displacement-engine", label: "Déplacement Climatique", icon: IconClimateDisplacement },
      { href: "/dashboard/peasant-rights-engine", label: "Droits Paysans", icon: IconPeasantRights },
      { href: "/dashboard/prison-labor-engine", label: "Travail Carcéral", icon: IconPrisonLabor },
      { href: "/dashboard/cultural-heritage-destruction-engine", label: "Destruction Patrimoine", icon: IconCulturalHeritageDestruction },
      { href: "/dashboard/drug-policy-human-rights-engine", label: "Politique Drogues DR", icon: IconDrugPolicyHumanRights },
      { href: "/dashboard/right-to-truth-engine", label: "Droit à la Vérité", icon: IconRightToTruth },
      { href: "/dashboard/counterterrorism-abuse-engine", label: "Abus Antiterrorisme", icon: IconCounterterrorismAbuse },
      { href: "/dashboard/whistleblower-protection-engine", label: "Lanceurs d'Alerte", icon: IconWhistleblowerProtection },
      { href: "/dashboard/food-sovereignty-engine", label: "Souveraineté Alimentaire", icon: IconFoodSovereignty },
      { href: "/dashboard/economic-sanctions-human-rights-engine", label: "Sanctions Économiques DR", icon: IconEconomicSanctions },
      { href: "/dashboard/juvenile-justice-engine", label: "Justice Juvénile", icon: IconJuvenileJustice },
      { href: "/dashboard/business-human-rights-engine", label: "Entreprises & Droits", icon: IconBusinessHumanRights },
      { href: "/dashboard/migrant-detention-engine", label: "Détention Migrants", icon: IconMigrantDetention },
      { href: "/dashboard/solitary-confinement-engine", label: "Isolement Cellulaire", icon: IconSolitaryConfinement },
      { href: "/dashboard/medical-neutrality-engine", label: "Neutralité Médicale", icon: IconMedicalNeutrality },
      { href: "/dashboard/human-rights-education-engine", label: "Éducation Droits Humains", icon: IconHumanRightsEducation },
      { href: "/dashboard/nuclear-testing-legacy-engine", label: "Héritage Tests Nucléaires", icon: IconNuclearTestingLegacy },
      { href: "/dashboard/climate-loss-damage-engine", label: "Pertes & Dommages Climat", icon: IconClimateLossDamage },
      { href: "/dashboard/prison-overcrowding-engine", label: "Surpopulation Carcérale", icon: IconPrisonOvercrowding },
      { href: "/dashboard/statelessness-engine", label: "Apatridie", icon: IconStatelessness },
      { href: "/dashboard/child-marriage-engine", label: "Mariages d'Enfants", icon: IconChildMarriage },
      { href: "/dashboard/digital-surveillance-engine", label: "Surveillance Digitale", icon: IconDigitalSurveillance },
      { href: "/dashboard/social-media-censorship-engine", label: "Censure Réseaux Sociaux", icon: IconSocialMediaCensorship },
      { href: "/dashboard/organ-trafficking-engine", label: "Trafic d'Organes", icon: IconOrganTrafficking },
      { href: "/dashboard/land-rights-engine", label: "Droits Fonciers", icon: IconLandRights },
      { href: "/dashboard/forced-disappearances-engine", label: "Disparitions Forcées", icon: IconForcedDisappearances },
      { href: "/dashboard/toxic-waste-environmental-racism-engine", label: "Racisme Environnemental", icon: IconToxicWasteEnvironmentalRacismRights },
      { href: "/dashboard/right-to-truth-transitional-justice-engine", label: "Droit à la Vérité", icon: IconRightToTruth },
      { href: "/dashboard/human-trafficking-engine", label: "Traite Êtres Humains", icon: IconHumanTrafficking },
      { href: "/dashboard/disability-rights-engine", label: "Droits Handicap", icon: IconDisabilityRights },
      { href: "/dashboard/colonial-reparations-engine", label: "Réparations Coloniales", icon: IconColonialReparationsLegacy },
      { href: "/dashboard/water-rights-engine", label: "Droit à l'Eau", icon: IconWaterRights },
      { href: "/dashboard/internet-shutdown-engine", label: "Coupures Internet", icon: IconInternetShutdown },
      { href: "/dashboard/academic-freedom-engine", label: "Liberté Académique", icon: IconAcademicFreedom },
      { href: "/dashboard/refugee-detention-engine", label: "Détention Réfugiés", icon: IconRefugeeDetention },
      { href: "/dashboard/corporate-impunity-engine", label: "Impunité Corporate", icon: IconCorporateImpunity },
      { href: "/dashboard/gender-pay-gap-engine", label: "Écart Salarial Genre", icon: IconGenderPayGap },
      { href: "/dashboard/indigenous-rights-engine", label: "Droits Autochtones", icon: IconIndigenousRights },
      { href: "/dashboard/arms-trade-engine", label: "Commerce des Armes", icon: IconArmsTrade },
      { href: "/dashboard/transitional-justice-engine", label: "Justice Transitionnelle", icon: IconTransitionalJustice },
      { href: "/dashboard/climate-displacement-engine", label: "Déplacements Climatiques", icon: IconClimateDisplacement },
      { href: "/dashboard/environmental-crime-engine", label: "Criminalité Environnem.", icon: IconEnvironmentalCrime },
      { href: "/dashboard/pretrial-detention-engine", label: "Détention Préventive", icon: IconPretrialDetention },
      { href: "/dashboard/emergency-powers-abuse-engine", label: "Abus Pouvoirs Urgence", icon: IconEmergencyPowersAbuse },
      { href: "/dashboard/racial-profiling-engine", label: "Profilage Racial", icon: IconRacialProfiling },
      { href: "/dashboard/hate-speech-incitement-engine", label: "Discours Haineux", icon: IconHateSpeechIncitement },
      { href: "/dashboard/slavery-reparations-engine", label: "Réparations Esclavage", icon: IconSlaveryReparations },
      { href: "/dashboard/conflict-minerals-engine", label: "Minerais Conflit", icon: IconConflictMinerals },
      { href: "/dashboard/austerity-social-rights-engine", label: "Austérité & Droits", icon: IconAusteritySocialRights },
      { href: "/dashboard/intersex-rights-engine", label: "Droits Intersexes", icon: IconIntersexRights },
      { href: "/dashboard/climate-litigation-rights-engine", label: "Litiges Climatiques", icon: IconClimateLitigationRights },
      { href: "/dashboard/child-poverty-social-exclusion-engine", label: "Pauvreté Enfants", icon: IconChildPovertySocialExclusion },
      { href: "/dashboard/elder-abuse-rights-engine", label: "Maltraitance Aînés", icon: IconElderAbuseRights },
      { href: "/dashboard/sanitation-rights-access-engine", label: "Droits Assainissement", icon: IconSanitationRightsAccess },
      { href: "/dashboard/prison-healthcare-denial-engine", label: "Santé Carcérale", icon: IconPrisonHealthcareDenial },
      { href: "/dashboard/conscientious-objector-rights-engine", label: "Objection Conscience", icon: IconConscientiousObjectorRights },
      { href: "/dashboard/witch-hunt-persecution-engine", label: "Chasse aux Sorcières", icon: IconWitchHuntPersecution },
      { href: "/dashboard/albinism-rights-engine", label: "Droits Albinisme", icon: IconAlbinismRights },
      { href: "/dashboard/menstrual-health-education-engine", label: "Santé Menstruelle", icon: IconMenstrualHealthEducation },
      { href: "/dashboard/facial-recognition-surveillance-engine", label: "Surveillance Biométrique", icon: IconFacialRecognitionSurveillance },
      { href: "/dashboard/artisanal-mining-rights-engine", label: "Mines Artisanales", icon: IconArtisanalMiningRights },
      { href: "/dashboard/nomadic-peoples-rights-engine", label: "Droits Peuples Nomades", icon: IconNomadicPeoplesRights },
      { href: "/dashboard/access-medicine-inequality-engine", label: "Accès Médicaments", icon: IconAccessMedicineInequality },
      { href: "/dashboard/informal-economy-rights-engine", label: "Économie Informelle", icon: IconInformalEconomyRights },
      { href: "/dashboard/sex-education-rights-engine", label: "Éducation Sexuelle", icon: IconSexEducationRights },
      { href: "/dashboard/neuroright-mental-sovereignty-engine", label: "Neurodroits Mentaux", icon: IconNeurorightMentalSovereignty },
      { href: "/dashboard/economic-domestic-abuse-engine", label: "Abus Économique Conjugal", icon: IconEconomicDomesticAbuse },
      { href: "/dashboard/eco-grief-rights-engine", label: "Deuil Écologique", icon: IconEcoGriefRights },
      { href: "/dashboard/neurodiversity-rights-engine", label: "Droits Neurodiversité", icon: IconNeurodiversityRights },
      { href: "/dashboard/genetic-discrimination-engine", label: "Discrimination Génétique", icon: IconGeneticDiscrimination },
      { href: "/dashboard/menopause-workplace-rights-engine", label: "Ménopause & Travail", icon: IconMenopauseWorkplaceRights },
      { href: "/dashboard/obstetric-violence-rights-engine", label: "Violence Obstétricale", icon: IconObstetricViolenceRights },
      { href: "/dashboard/period-poverty-rights-engine", label: "Précarité Menstruelle", icon: IconPeriodPovertyRights },
      { href: "/dashboard/refugee-digital-rights-engine", label: "Droits Numériques Réfugiés", icon: IconRefugeeDigitalRights },
      { href: "/dashboard/algorithmic-bias-rights-engine", label: "Biais Algorithmiques", icon: IconAlgorithmicBiasRights },
      { href: "/dashboard/hate-speech-platform-rights-engine", label: "Discours Haine Plateformes", icon: IconHateSpeechPlatformRights },
      { href: "/dashboard/digital-gender-gap-rights-engine", label: "Fracture Numérique Genre", icon: IconDigitalGenderGapRights },
      { href: "/dashboard/unpaid-care-work-rights-engine", label: "Travail Care Non Rémunéré", icon: IconUnpaidCareWorkRights },
      { href: "/dashboard/youth-justice-rights-engine", label: "Justice Jeunesse", icon: IconYouthJusticeRights },
      { href: "/dashboard/land-grabbing-rights-engine", label: "Accaparement Terres", icon: IconLandGrabbingRights },
      { href: "/dashboard/climate-forced-migration-rights-engine", label: "Migration Climatique Forcée", icon: IconClimateForcedMigrationRights },
      { href: "/dashboard/child-labor-mining-rights-engine", label: "Travail Minier Enfants", icon: IconChildLaborMiningRights },
      { href: "/dashboard/water-rights-access-engine", label: "Droits Accès à l'Eau", icon: IconWaterRightsAccess },
      { href: "/dashboard/prison-labor-rights-engine", label: "Travail Pénitentiaire", icon: IconPrisonLaborRights },
      { href: "/dashboard/statelessness-rights-engine", label: "Droits Apatrides", icon: IconStatelessnessRights },
      { href: "/dashboard/corporate-accountability-rights-engine", label: "Responsabilité Corp.", icon: IconCorporateAccountability },
      { href: "/dashboard/prison-torture-rights-engine", label: "Torture Carcérale", icon: IconPrisonTorture },
      { href: "/dashboard/seafarers-maritime-labor-rights-engine", label: "Marins & Maritime", icon: IconSeafarersMaritimeLaborRights },
      { href: "/dashboard/cultural-minority-rights-engine", label: "Droits Minorités Culturelles", icon: IconCulturalMinorityRights },
      { href: "/dashboard/right-to-strike-labor-engine", label: "Droit de Grève", icon: IconRightToStrikeLaborRights },
      { href: "/dashboard/judicial-independence-rights-engine", label: "Indépendance Judiciaire", icon: IconJudicialIndependenceRights },
      { href: "/dashboard/indigenous-data-sovereignty-engine", label: "Souveraineté Données Autochtones", icon: IconIndigenousDataSovereignty },
      { href: "/dashboard/fair-trial-due-process-engine", label: "Procès Équitable", icon: IconFairTrialDueProcess },
      { href: "/dashboard/right-to-asylum-refugee-protection-engine", label: "Droit d&apos;Asile & Réfugiés", icon: IconRightToAsylumRefugeeProtection },
      { href: "/dashboard/gender-based-violence-femicide-engine", label: "Violences Genre & Féminicide", icon: IconGenderBasedViolenceFemicide },
      { href: "/dashboard/anti-corruption-accountability-engine", label: "Anti-Corruption & Redevabilité", icon: IconAntiCorruptionAccountability },
      { href: "/dashboard/digital-privacy-surveillance-rights-engine", label: "Vie Privée Numérique", icon: IconDigitalPrivacySurveillanceRights },
      { href: "/dashboard/freedom-of-assembly-protest-rights-engine", label: "Liberté Réunion &amp; Manifestation", icon: IconFreedomOfAssemblyProtestRights },
      { href: "/dashboard/housing-eviction-homelessness-rights-engine", label: "Droit au Logement", icon: IconHousingEvictionHomelessnessRights },
      { href: "/dashboard/child-trafficking-exploitation-rights-engine", label: "Trafic Enfants & Exploitation", icon: IconChildTraffickingExploitationRights },
      { href: "/dashboard/disability-rights-accessibility-engine", label: "Droits Handicap & Accessibilité", icon: IconDisabilityRightsAccessibility },
      { href: "/dashboard/academic-freedom-education-rights-engine", label: "Liberté Académique", icon: IconAcademicFreedomEducationRights },
      { href: "/dashboard/minority-religious-freedom-rights-engine", label: "Liberté Religieuse Minorités", icon: IconMinorityReligiousFreedomRights },
      { href: "/dashboard/sexual-orientation-lgbtq-rights-engine", label: "Droits LGBTQ+", icon: IconSexualOrientationLgbtqRights },
      { href: "/dashboard/food-sovereignty-famine-rights-engine", label: "Souveraineté Alimentaire", icon: IconFoodSovereigntyFamineRights },
      { href: "/dashboard/press-freedom-journalist-protection-engine", label: "Liberté de la Presse", icon: IconPressFreedomJournalistProtection },
      { href: "/dashboard/climate-justice-environmental-defenders-engine", label: "Justice Climatique", icon: IconClimateJusticeEnvironmentalDefenders },
      { href: "/dashboard/migrant-worker-labor-exploitation-engine", label: "Travailleurs Migrants", icon: IconMigrantWorkerLaborExploitation },
      { href: "/dashboard/death-penalty-extrajudicial-killings-engine", label: "Peine de Mort & EJK", icon: IconDeathPenaltyExtrajudicialKillings },
      { href: "/dashboard/human-rights-defenders-protection-engine", label: "Défenseurs Droits Humains", icon: IconHumanRightsDefendersProtection },
      { href: "/dashboard/cybercrime-digital-rights-exploitation-engine", label: "Cybercriminalité & Droits", icon: IconCybercrimeDigitalRightsExploitation },
      { href: "/dashboard/nuclear-radiation-civilian-rights-engine", label: "Droits Nucléaire & Radiations", icon: IconNuclearRadiationCivilianRights },
      { href: "/dashboard/colonial-reparations-memory-rights-engine", label: "Réparations Coloniales", icon: IconColonialReparationsMemoryRights },
      { href: "/dashboard/elder-care-aging-rights-engine", label: "Droits Personnes Âgées", icon: IconElderCareAgingRights },
      { href: "/dashboard/sports-athlete-rights-engine", label: "Droits Athlètes & Sport", icon: IconSportsAthleteRights },
      { href: "/dashboard/prison-rehabilitation-reentry-rights-engine", label: "Réhabilitation Carcérale", icon: IconPrisonRehabilitationReentryRights },
      { href: "/dashboard/poverty-social-exclusion-rights-engine", label: "Pauvreté & Exclusion Sociale", icon: IconPovettySocialExclusionRights },
      { href: "/dashboard/arts-cultural-expression-rights-engine", label: "Expression Artistique & Culture", icon: IconArtsCulturalExpressionRights },
      { href: "/dashboard/mental-health-involuntary-treatment-engine", label: "Santé Mentale & Traitement Forcé", icon: IconMentalHealthInvoluntaryTreatment },
      { href: "/dashboard/border-crossing-detention-rights-engine", label: "Frontières & Détention", icon: IconBorderCrossingDetentionRights },
      { href: "/dashboard/stateless-persons-rights-engine", label: "Apatridie & Droits", icon: IconStatelessPersonsRights },
      { href: "/dashboard/human-trafficking-labor-exploitation-engine", label: "Traite Humaine & Exploitation", icon: IconHumanTraffickingLaborExploitation },
      { href: "/dashboard/water-sanitation-access-rights-engine", label: "Eau & Assainissement", icon: IconWaterSanitationAccessRights },
      { href: "/dashboard/corporate-accountability-human-rights-engine", label: "Responsabilité Entreprises", icon: IconCorporateAccountabilityHumanRights },
      { href: "/dashboard/counter-terrorism-rights-violations-engine", label: "Antiterrorisme & Droits", icon: IconCounterTerrorismRightsViolations },
      { href: "/dashboard/indigenous-land-rights-extraction-engine", label: "Terres Autochtones & Extraction", icon: IconIndigenousLandRightsExtraction },
      { href: "/dashboard/reproductive-rights-bodily-autonomy-engine", label: "Droits Reproductifs & Autonomie", icon: IconReproductiveRightsBodlyAutonomy },
      { href: "/dashboard/online-censorship-platform-governance-engine", label: "Censure En Ligne & Plateformes", icon: IconOnlineCensorshipPlatformGovernance },
      { href: "/dashboard/forced-disappearances-extrajudicial-engine", label: "Disparitions Forcées & Extrajudiciaires", icon: IconForcedDisappearancesExtrajudicial },
      { href: "/dashboard/armed-conflict-civilian-protection-engine", label: "Conflits Armés & Protection Civils", icon: IconArmedConflictCivilianProtection },
      { href: "/dashboard/whistleblower-leaker-protection-engine", label: "Lanceurs d&apos;Alerte & Protection Sources", icon: IconWhistleblowerLeakerProtection },
      { href: "/dashboard/racial-discrimination-systemic-racism-engine", label: "Discrimination Raciale & Racisme Systémique", icon: IconRacialDiscriminationSystemicRacism },
      { href: "/dashboard/caste-discrimination-untouchability-engine", label: "Discrimination de Caste & Intouchabilité", icon: IconCasteDiscriminationUntouchability },
      { href: "/dashboard/bioethics-genetic-privacy-rights-engine", label: "Bioéthique & Vie Privée Génétique", icon: IconBioethicsGeneticPrivacyRights },
      { href: "/dashboard/minority-language-cultural-rights-engine", label: "Droits Linguistiques & Culturels Minoritaires", icon: IconMinorityLanguageCulturalRights },
      { href: "/dashboard/land-mine-cluster-munitions-rights-engine", label: "Mines & Sous-Munitions Civiles", icon: IconLandMineClusterMunitionsRights },
      { href: "/dashboard/refugee-integration-inclusion-rights-engine", label: "Intégration Réfugiés & Inclusion", icon: IconRefugeeIntegrationInclusionRights },
      { href: "/dashboard/economic-austerity-social-rights-engine", label: "Austérité Économique & Droits Sociaux", icon: IconEconomicAusteritySocialRights },
      { href: "/dashboard/autonomous-weapons-ai-warfare-rights-engine", label: "Armes Autonomes & IA Militaire", icon: IconAutonomousWeaponsAiWarfareRights },
      { href: "/dashboard/space-rights-outer-space-militarization-engine", label: "Espace & Militarisation Orbitale", icon: IconSpaceRightsOuterSpaceMilitarization },
      { href: "/dashboard/digital-divide-access-rights-engine", label: "Fracture Numérique & Accès", icon: IconDigitalDivideAccessRights },
      { href: "/dashboard/climate-change-human-rights-engine", label: "Changement Climatique & Droits", icon: IconClimateChangeHumanRights },
      { href: "/dashboard/child-labor-exploitation-rights-engine", label: "Travail des Enfants & Exploitation", icon: IconChildLaborExploitationRights },
      { href: "/dashboard/lgbtq-rights-criminalization-engine", label: "Droits LGBTQ+ & Criminalisation", icon: IconLgbtqRightsCriminalization },
      { href: "/dashboard/prison-conditions-detention-rights-engine", label: "Conditions Détention & Droits Prisonniers", icon: IconPrisonConditionsDetentionRights },
      { href: "/dashboard/freedom-assembly-association-rights-engine", label: "Liberté Réunion & Association", icon: IconFreedomAssemblyAssociationRights },
      { href: "/dashboard/housing-eviction-displacement-rights-engine", label: "Logement & Expulsions Forcées", icon: IconHousingEvictionDisplacementRights },
      { href: "/dashboard/minority-religious-rights-persecution-engine", label: "Persécution Religieuse Minorités", icon: IconMinorityReligiousRightsPersecution },
      { href: "/dashboard/social-media-political-censorship-engine", label: "Censure Politique Réseaux Sociaux", icon: IconSocialMediaPoliticalCensorship },
      { href: "/dashboard/disability-rights-accessibility-engine", label: "Droits Handicapés & Accessibilité", icon: IconDisabilityRightsAccessibility },
      { href: "/dashboard/elderly-rights-age-discrimination-engine", label: "Droits Aînés & Discrimination Âge", icon: IconElderlyRightsAgeDiscrimination },
      { href: "/dashboard/migration-asylum-seekers-rights-engine", label: "Migration & Droits Demandeurs Asile", icon: IconMigrationAsylumSeekersRights },
      { href: "/dashboard/academic-freedom-university-rights-engine", label: "Liberté Académique & Universités", icon: IconAcademicFreedomUniversityRights },
      { href: "/dashboard/forced-marriage-child-marriage-rights-engine", label: "Mariage Forcé & Mariage Enfants", icon: IconForcedMarriageChildMarriageRights },
      { href: "/dashboard/nuclear-weapons-disarmament-rights-engine", label: "Armes Nucléaires & Désarmement", icon: IconNuclearWeaponsDisarmamentRights },
      { href: "/dashboard/anti-corruption-accountability-rights-engine", label: "Anti-Corruption & Redevabilité", icon: IconAntiCorruptionAccountabilityRights },
      { href: "/dashboard/internet-shutdown-digital-rights-engine", label: "Coupures Internet & Droits Numériques", icon: IconInternetShutdownDigitalRights },
      { href: "/dashboard/statelessness-citizenship-rights-engine", label: "Apatridie & Droits à la Nationalité", icon: IconStatelessnessCitizenshipRights },
      { href: "/dashboard/colonial-reparations-historical-justice-engine", label: "Réparations Coloniales & Justice Historique", icon: IconColonialReparationsHistoricalJustice },
      { href: "/dashboard/biometric-surveillance-state-control-engine", label: "Surveillance Biométrique & Contrôle Étatique", icon: IconBiometricSurveillanceStateControl },
      { href: "/dashboard/food-sovereignty-agricultural-rights-engine", label: "Souveraineté Alimentaire & Droits Agricoles", icon: IconFoodSovereigntyAgriculturalRights },
      { href: "/dashboard/debt-trap-economic-coercion-rights-engine", label: "Piège de la Dette & Coercition Économique", icon: IconDebtTrapEconomicCoercionRights },
      { href: "/dashboard/environmental-defenders-persecution-engine", label: "Défenseurs Environnementaux Persécutés", icon: IconEnvironmentalDefendersPersecution },
      { href: "/dashboard/religious-law-lgbtq-rights-engine", label: "Droit Religieux & Droits LGBTQ+", icon: IconReligiousLawLgbtqRights },
      { href: "/dashboard/disability-rights-ableism-engine", label: "Droits Handicap & Validisme Systémique", icon: IconDisabilityRightsAbleism },
      { href: "/dashboard/genocide-prevention-accountability-engine", label: "Prévention Génocide & Responsabilité", icon: IconGenocidePreventionAccountability },
      { href: "/dashboard/labor-union-rights-freedom-association-engine", label: "Syndicats & Liberté d'Association", icon: IconLaborUnionRightsFreedomAssociation },
      { href: "/dashboard/maternal-health-rights-obstetric-violence-engine", label: "Santé Maternelle & Violence Obstétricale", icon: IconMaternalHealthRightsObstetricViolence },
      { href: "/dashboard/academic-freedom-scholar-persecution-engine", label: "Liberté Académique & Persécution Chercheurs", icon: IconAcademicFreedomScholarPersecution },
      { href: "/dashboard/climate-refugee-displacement-rights-engine", label: "Réfugiés Climatiques & Droits Déplacement", icon: IconClimateRefugeeDisplacementRights },
      { href: "/dashboard/stateless-persons-nationality-rights-engine", label: "Apatrides & Droits à la Nationalité", icon: IconStatelessPersonsNationalityRights },
      { href: "/dashboard/human-trafficking-modern-slavery-engine", label: "Traite Humaine & Esclavage Moderne", icon: IconHumanTraffickingModernSlavery },
      { href: "/dashboard/climate-displacement-migration-engine", label: "Déplacements Climatiques & Migration", icon: IconClimateDisplacementMigration },
      { href: "/dashboard/child-labor-education-rights-engine", label: "Travail Enfants & Droits à l'Éducation", icon: IconChildLaborEducationRights },
      { href: "/dashboard/indigenous-land-rights-territorial-sovereignty-engine", label: "Droits Fonciers Autochtones & Souveraineté", icon: IconIndigenousLandRightsTerritoralSovereignty },
      { href: "/dashboard/digital-surveillance-privacy-rights-engine", label: "Surveillance Digitale & Droits à la Vie Privée", icon: IconDigitalSurveillancePrivacyRights },
      { href: "/dashboard/food-sovereignty-famine-rights-engine", label: "Souveraineté Alimentaire & Droits Face à la Famine", icon: IconFoodSovereigntyFamineRights },
      { href: "/dashboard/mental-health-rights-psychiatric-violence-engine", label: "Santé Mentale & Violence Psychiatrique", icon: IconMentalHealthRightsPsychiatricViolence },
      { href: "/dashboard/forced-disappearance-extrajudicial-killing-engine", label: "Disparitions Forcées & Exécutions Extrajudiciaires", icon: IconForcedDisappearanceExtrajudicialKilling },
      { href: "/dashboard/refugees-asylum-seekers-rights-engine", label: "Droits Réfugiés & Demandeurs d&apos;Asile", icon: IconRefugeesAsylumSeekersRights },
      { href: "/dashboard/corruption-human-rights-nexus-engine", label: "Corruption &amp; Droits Humains", icon: IconCorruptionHumanRightsNexus },
      { href: "/dashboard/religious-persecution-minority-rights-engine", label: "Persécution Religieuse", icon: IconReligiousPersecutionMinorityRights },
      { href: "/dashboard/arms-trade-civilian-harm-engine", label: "Commerce Armes &amp; Civils", icon: IconArmsTradeCivilianHarm },
      { href: "/dashboard/lgbtq-rights-violence-criminalization-engine", label: "Droits LGBTQ+", icon: IconLgbtqRightsViolenceCriminalization },
      { href: "/dashboard/press-freedom-journalist-safety-engine", label: "Liberté de la Presse", icon: IconPressFreedomJournalistSafety },
      { href: "/dashboard/land-grabbing-displacement-rights-engine", label: "Accaparement Terres", icon: IconLandGrabbingDisplacementRights },
      { href: "/dashboard/water-pollution-environmental-rights-engine", label: "Pollution Eau & Environnement", icon: IconWaterPollutionEnvironmentalRights },
      { href: "/dashboard/ethnic-minority-rights-discrimination-engine", label: "Minorités Ethniques", icon: IconEthnicMinorityRightsDiscrimination },
      { href: "/dashboard/housing-rights-forced-evictions-engine", label: "Droit au Logement", icon: IconHousingRightsForcedEvictions },
      { href: "/dashboard/death-penalty-execution-rights-engine", label: "Peine de Mort", icon: IconDeathPenaltyExecutionRights },
      { href: "/dashboard/migrant-workers-rights-kafala-engine", label: "Travailleurs Migrants", icon: IconMigrantWorkersRightsKafala },
      { href: "/dashboard/torture-cruel-treatment-detention-engine", label: "Torture & Détention", icon: IconTortureCruelTreatmentDetention },
      { href: "/dashboard/womens-rights-gender-based-violence-engine", label: "Droits des Femmes", icon: IconWomensRightsGenderBasedViolence },
      { href: "/dashboard/racial-justice-police-brutality-engine", label: "Justice Raciale & Police", icon: IconRacialJusticePoliceBrutality },
      { href: "/dashboard/internet-freedom-censorship-engine", label: "Liberté Internet", icon: IconInternetFreedomCensorship },
      { href: "/dashboard/war-crimes-accountability-engine", label: "Crimes de Guerre", icon: IconWarCrimesAccountability },
      { href: "/dashboard/environmental-defenders-rights-engine", label: "Défenseurs Env.", icon: IconEnvironmentalDefendersRights },
      { href: "/dashboard/antiterrorism-laws-rights-abuse-engine", label: "Lois Antiterro", icon: IconAntiterrorismLawsRightsAbuse },
      { href: "/dashboard/child-marriage-forced-unions-engine", label: "Mariage Enfants", icon: IconChildMarriageForcedUnions },
      { href: "/dashboard/protest-freedom-assembly-rights-engine", label: "Liberté Manifestation", icon: IconProtestFreedomAssemblyRights },
      { href: "/dashboard/sexual-violence-conflict-impunity-engine", label: "Violences Conflits", icon: IconSexualViolenceConflictImpunity },
      { href: "/dashboard/right-to-education-access-engine", label: "Droit à l'Éducation", icon: IconRightToEducationAccess },
      { href: "/dashboard/fair-trial-due-process-rights-engine", label: "Procès Équitable", icon: IconFairTrialDueProcessRights },
      { href: "/dashboard/xenophobia-hate-crime-minority-engine", label: "Xénophobie & Haine", icon: IconXenophobiaHateCrimeMinority },
      { href: "/dashboard/nuclear-testing-environmental-rights-engine", label: "Tests Nucléaires", icon: IconNuclearTestingEnvironmentalRights },
      { href: "/dashboard/social-protection-poverty-rights-engine", label: "Protection Sociale", icon: IconSocialProtectionPovertyRights },
      { href: "/dashboard/freedom-expression-artistic-censorship-engine", label: "Liberté Artistique", icon: IconFreedomExpressionArtisticCensorship },
      { href: "/dashboard/death-in-custody-prison-conditions-engine", label: "Mort en Détention", icon: IconDeathInCustodyPrisonConditions },
      { href: "/dashboard/drug-policy-criminalization-rights-engine", label: "Politique Drogues", icon: IconDrugPolicyCriminalizationRights },
      { href: "/dashboard/indigenous-land-cultural-rights-engine", label: "Droits Peuples Autochtones", icon: IconIndigenousLandCulturalRights },
      { href: "/dashboard/organ-trafficking-body-autonomy-rights-engine", label: "Trafic d&apos;Organes", icon: IconOrganTraffickingBodyAutonomyRights },
      { href: "/dashboard/solitary-confinement-isolation-rights-engine", label: "Isolement Carcéral", icon: IconSolitaryConfinementIsolationRights },
      { href: "/dashboard/child-online-exploitation-rights-engine", label: "Exploitation Enfants Ligne", icon: IconChildOnlineExploitationRights },
      { href: "/dashboard/forced-sterilization-reproductive-coercion-engine", label: "Stérilisation Forcée", icon: IconForcedSterilizationReproductiveCoercion },
      { href: "/dashboard/ai-surveillance-biometric-rights-engine", label: "Surveillance IA & Biométrie", icon: IconAiSurveillanceBiometricRights },
      { href: "/dashboard/arms-embargo-violations-rights-engine", label: "Embargo Armes", icon: IconArmsEmbargoViolationsRights },
      { href: "/dashboard/nomadic-pastoralist-peoples-rights-engine", label: "Peuples Nomades", icon: IconNomadicPastoralistPeoplesRights },
      { href: "/dashboard/prison-privatization-profit-rights-engine", label: "Prisons Privées", icon: IconPrisonPrivatizationProfitRights },
      { href: "/dashboard/cultural-heritage-destruction-rights-engine", label: "Patrimoine Culturel", icon: IconCulturalHeritageDestructionRights },
      { href: "/dashboard/colonial-reparations-transitional-justice-engine", label: "Réparations Coloniales", icon: IconColonialReparationsTransitionalJustice },
      { href: "/dashboard/mining-extraction-community-rights-engine", label: "Droits Communautés Mines", icon: IconMiningExtractionCommunityRights },
      { href: "/dashboard/water-scarcity-conflict-rights-engine", label: "Conflits Hydriques", icon: IconWaterScarcityConflictRights },
      { href: "/dashboard/climate-justice-loss-damage-rights-engine", label: "Justice Climatique", icon: IconClimateJusticeLossDamageRights },
      { href: "/dashboard/border-wall-migration-rights-engine", label: "Murs Frontaliers", icon: IconBorderWallMigrationRights },
      { href: "/dashboard/sexual-orientation-identity-criminalization-engine", label: "Criminalisation SOGIE", icon: IconSexualOrientationIdentityCriminalization },
      { href: "/dashboard/witch-hunt-accusation-persecution-engine", label: "Chasses aux Sorcières", icon: IconWitchHuntAccusationPersecution },
      { href: "/dashboard/antipersonnel-mines-victim-rights-engine", label: "Victimes Mines", icon: IconAntipersonnelMinesVictimRights },
      { href: "/dashboard/death-penalty-abolition-rights-engine", label: "Peine de Mort", icon: IconDeathPenaltyAbolitionRights },
      { href: "/dashboard/transitional-justice-truth-commission-engine", label: "Justice Transitionnelle", icon: IconTransitionalJusticeTruthCommission },
      { href: "/dashboard/reparations-genocide-victims-engine", label: "Réparations Génocide", icon: IconReparationsGenocideVictims },
      { href: "/dashboard/roma-traveller-rights-engine", label: "Droits Roms & Gens du Voyage", icon: IconRomaTravellerRights },
      { href: "/dashboard/street-children-rights-engine", label: "Enfants des Rues", icon: IconStreetChildrenRights },
      { href: "/dashboard/bonded-labor-debt-slavery-rights-engine", label: "Servitude par Dette", icon: IconBondedLaborDebtSlaveryRights },
      { href: "/dashboard/forced-recruitment-conscription-rights-engine", label: "Recrutement Forcé", icon: IconForcedRecruitmentConscriptionRights },
      { href: "/dashboard/elder-rights-ageism-engine", label: "Droits Personnes Âgées", icon: IconElderRightsAgeism },
      { href: "/dashboard/acid-attack-gender-violence-engine", label: "Attaques Acide", icon: IconAcidAttackGenderViolence },
      { href: "/dashboard/nuclear-victims-rights-engine", label: "Victimes Nucléaires", icon: IconNuclearVictimsRights },
      { href: "/dashboard/human-trafficking-labor-exploitation-rights-engine", label: "Traite Humaine", icon: IconHumanTraffickingLaborExploitationRights },
      { href: "/dashboard/disability-rights-inclusive-society-engine", label: "Droits Handicap", icon: IconDisabilityRightsInclusiveSociety },
      { href: "/dashboard/inventions-portfolio-engine", label: "Brevets Caelum", icon: IconInventionsPortfolio },
      { href: "/dashboard/inventions-showcase", label: "Vitrine Brevets Caelum", icon: IconInventionsShowcase },
      { href: "/dashboard/leprosy-affected-rights-engine", label: "Lèpre & Stigmatisation", icon: IconLeprosyAffectedRights },
      { href: "/dashboard/fistula-obstetric-rights-engine", label: "Fistule Obstétrique", icon: IconFistulaObstetricRights },
      { href: "/dashboard/hiv-aids-stigma-rights-engine", label: "VIH/SIDA Stigma Droits", icon: IconHIVAIDSStigmaRights },
      { href: "/dashboard/poverty-criminalization-anti-homeless-laws-engine", label: "Criminalisation Pauvreté", icon: IconPovertyCriminalizationAntiHomelessLaws },
      { href: "/dashboard/nonconsensual-intimate-image-abuse-engine", label: "Abus Image Intime", icon: IconNonconsensualIntimateImageAbuse },
      { href: "/dashboard/residential-school-indigenous-assimilation-engine", label: "Pensionnats Autochtones", icon: IconResidentialSchoolIndigenousAssimilation },
      { href: "/dashboard/albinism-persecution-rights-engine", label: "Persécution Albinisme", icon: IconAlbinismPersecutionRights },
      { href: "/dashboard/toxic-waste-environmental-racism-rights-engine", label: "Racisme Environnemental", icon: IconToxicWasteEnvironmentalRacismRights },
      { href: "/dashboard/juvenile-justice-child-detention-rights-engine", label: "Justice Juvénile", icon: IconJuvenileJusticeChildDetentionRights },
      { href: "/dashboard/mental-health-forced-treatment-rights-engine", label: "Santé Mentale Forcée", icon: IconMentalHealthForcedTreatmentRights },
      { href: "/dashboard/human-rights-defenders-assassination-engine", label: "Défenseurs DH Assassinés", icon: IconHumanRightsDefendersAssassination },
      { href: "/dashboard/autonomous-weapons-lethal-robotics-rights-engine", label: "Armes Autonomes LAWS", icon: IconAutonomousWeaponsLethalRoboticsRights },
      { href: "/dashboard/child-marriage-forced-union-rights-engine", label: "Mariage Forcé Enfants", icon: IconChildMarriageForcedUnionRights },
      { href: "/dashboard/colonial-reparations-restitution-rights-engine", label: "Réparations Coloniales", icon: IconColonialReparationsRestitutionRights },
      { href: "/dashboard/right-to-food-famine-accountability-engine", label: "Droit Alimentation Famine", icon: IconRightToFoodFamineAccountability },
      { href: "/dashboard/digital-divide-internet-access-rights-engine", label: "Fracture Numérique", icon: IconDigitalDivideInternetAccessRights },
      { href: "/dashboard/human-rights-education-rights-engine", label: "Éducation Droits Humains", icon: IconHumanRightsEducationRights },
      { href: "/dashboard/elderly-abuse-care-home-rights-engine", label: "Maltraitance Personnes Âgées", icon: IconElderlyAbuseCareHomeRights },
      { href: "/dashboard/organ-trafficking-transplant-rights-engine", label: "Trafic d'Organes", icon: IconOrganTraffickingTransplantRights },
      { href: "/dashboard/enforced-disappearance-rights-engine", label: "Disparitions Forcées", icon: IconEnforcedDisappearanceRights },
      { href: "/dashboard/cultural-genocide-heritage-destruction-engine", label: "Génocide Culturel", icon: IconCulturalGenocideHeritageDestruction },
      { href: "/dashboard/medical-experimentation-ethics-rights-engine", label: "Éthique Médicale", icon: IconMedicalExperimentationEthicsRights },
      { href: "/dashboard/domestic-worker-exploitation-rights-engine", label: "Travailleurs Dom.", icon: IconDomesticWorkerExploitationRights },
      { href: "/dashboard/surveillance-facial-recognition-rights-engine", label: "Surveillance IA", icon: IconSurveillanceFacialRecognitionRights },
      { href: "/dashboard/witchcraft-accusation-persecution-engine", label: "Accusations Sorcellerie", icon: IconWitchcraftAccusationPersecution },
      { href: "/dashboard/anti-corruption-whistleblower-protection-engine", label: "Lanceurs d'Alerte", icon: IconAntiCorruptionWhistleblowerProtection },
      { href: "/dashboard/apostasy-blasphemy-persecution-engine", label: "Apostasie & Blasphème", icon: IconApostasyBlasphemyPersecution },
      { href: "/dashboard/third-party-work-validation-engine", label: "Validation Tiers", icon: IconThirdPartyWorkValidation },
      { href: "/dashboard/cybersecurity-data-protection-engine", label: "Cybersécurité", icon: IconCybersecurityDataProtection },
      { href: "/dashboard/active-cyber-defense-honeypot-engine", label: "Défense Cyber", icon: IconActiveCyberDefenseHoneypot },
      { href: "/dashboard/patent-revenue-prioritization-engine", label: "Revenus Brevets", icon: IconPatentRevenuePrioritization },
      { href: "/dashboard/peasant-land-tenure-rights-engine", label: "Droits Fonciers Paysans", icon: IconPeasantLandTenureRights },
      { href: "/dashboard/sex-worker-rights-criminalization-engine", label: "Droits Trav. du Sexe", icon: IconSexWorkerRightsCriminalization },
      { href: "/dashboard/unaccompanied-migrant-children-rights-engine", label: "Enfants Migrants", icon: IconUnaccompaniedMigrantChildrenRights },
      { href: "/dashboard/caste-discrimination-dalit-rights-engine", label: "Discrimination Caste", icon: IconCasteDiscriminationDalitRights },
      { href: "/dashboard/rural-women-land-inheritance-rights-engine", label: "Femmes Rurales Terres", icon: IconRuralWomenLandInheritanceRights },
      { href: "/dashboard/afrodescendant-reparations-rights-engine", label: "Réparations Afrodesc.", icon: IconAfrodescendantReparationsRights },
      { href: "/dashboard/deforestation-indigenous-rights-engine", label: "Déforestation & Autochtones", icon: IconDeforestationIndigenousRights },
      { href: "/dashboard/wildlife-trafficking-biodiversity-rights-engine", label: "Trafic Faune Sauvage", icon: IconWildlifeTraffickingBiodiversityRights },
      { href: "/dashboard/malnutrition-child-nutrition-rights-engine", label: "Malnutrition Enfants", icon: IconMalnutritionChildNutritionRights },
      { href: "/dashboard/private-military-contractor-accountability-engine", label: "Contractants Militaires", icon: IconPrivateMilitaryContractorAccountability },
      { href: "/dashboard/information-warfare-civilian-rights-engine", label: "Guerre Information", icon: IconInformationWarfareCivilianRights },
      { href: "/dashboard/satellite-surveillance-privacy-rights-engine", label: "Surveillance Satellite", icon: IconSatelliteSurveillancePrivacyRights },
      { href: "/dashboard/climate-finance-loss-damage-rights-engine", label: "Financement Climatique L&D", icon: IconClimateFinanceLossDamage },
      { href: "/dashboard/sexual-violence-conflict-accountability-engine", label: "Violence Sexuelle Conflit", icon: IconSexualViolenceConflictAccountability },
      { href: "/dashboard/children-armed-conflict-grave-violations-engine", label: "Enfants Conflits Armés", icon: IconChildrenArmedConflictGraveViolations },
      { href: "/dashboard/disability-rights-inclusion-engine", label: "Droits Handicap CDPH", icon: IconDisabilityRightsInclusion },
      { href: "/dashboard/elder-rights-aging-population-engine", label: "Droits des Aînés", icon: IconElderRightsAgingPopulation },
      { href: "/dashboard/housing-forced-eviction-rights-engine", label: "Logement & Expulsions Forcées", icon: IconHousingForcedEvictionRights },
      { href: "/dashboard/water-sanitation-rights-engine", label: "Droit à l'Eau WASH", icon: IconWaterSanitationRights },
      { href: "/dashboard/prison-conditions-detainee-rights-engine", label: "Conditions Carcérales", icon: IconPrisonConditionsDetaineeRights },
      { href: "/dashboard/freedom-religion-belief-engine", label: "Liberté Religion", icon: IconFreedomReligionBelief },
      { href: "/dashboard/media-freedom-journalist-protection-engine", label: "Liberté Presse", icon: IconMediaFreedomJournalistProtection },
      { href: "/dashboard/anti-terrorism-counter-extremism-rights-engine", label: "Anti-Terrorisme & Droits", icon: IconAntiTerrorismCounterExtremismRights },
      { href: "/dashboard/corporate-human-rights-due-diligence-engine", label: "Vigilance Corp. Droits", icon: IconCorporateHumanRightsDueDiligence },
      { href: "/dashboard/statelessness-citizenship-deprivation-engine", label: "Apatridie & Nationalité", icon: IconStatelessnessCitizenshipDeprivation },
      { href: "/dashboard/racial-discrimination-minority-rights-engine", label: "Discrimination Raciale", icon: IconRacialDiscriminationMinorityRights },
      { href: "/dashboard/food-sovereignty-right-to-food-engine", label: "Souveraineté Alimentaire", icon: IconFoodSovereigntyRightToFood },
      { href: "/dashboard/digital-surveillance-privacy-rights-engine", label: "Surveillance Numérique", icon: IconDigitalSurveillancePrivacyRights },
      { href: "/dashboard/ip-watch-guardian", label: "IP Watch Guardian", icon: IconIPWatchGuardian },
      { href: "/dashboard/access-to-justice-rule-of-law-engine", label: "Accès Justice & État de Droit", icon: IconAccessToJusticeRuleOfLaw },
      { href: "/dashboard/economic-social-rights-engine", label: "Droits Économiques & Sociaux", icon: IconEconomicSocialRights },
      { href: "/dashboard/environmental-rights-defenders-engine", label: "Défenseurs Environnement", icon: IconEnvironmentalRightsDefenders },
      { href: "/dashboard/nuclear-weapons-humanitarian-impact-engine", label: "Armes Nucléaires &amp; Humanitaire", icon: IconNuclearWeaponsHumanitarianImpact },
      { href: "/dashboard/youth-rights-intergenerational-justice-engine", label: "Droits Jeunesse", icon: IconYouthRightsIntergenerationalJustice },
      { href: "/dashboard/business-tax-evasion-human-rights-engine", label: "Évasion Fiscale &amp; Droits", icon: IconBusinessTaxEvasionHumanRights },
      { href: "/dashboard/pandemic-health-emergency-rights-engine", label: "Urgences Sanitaires", icon: IconPandemicHealthEmergencyRights },
      { href: "/dashboard/housing-rights-eviction-engine", label: "Droit au Logement", icon: IconHousingRightsEviction },
      { href: "/dashboard/religious-freedom-persecution-engine", label: "Liberté Religieuse", icon: IconReligiousFreedomPersecution },
      { href: "/dashboard/sexual-reproductive-health-rights-engine", label: "Droits Sexuels &amp; Reproductifs", icon: IconSexualReproductiveHealthRights },
      { href: "/dashboard/child-marriage-forced-union-engine", label: "Mariage Enfants &amp; Unions Forcées", icon: IconChildMarriageForcedUnion },
      { href: "/dashboard/internet-freedom-digital-rights-engine", label: "Liberté Internet &amp; Droits Numériques", icon: IconInternetFreedomDigitalRights },
      { href: "/dashboard/indigenous-cultural-rights-language-engine", label: "Droits Culturels Autochtones", icon: IconIndigenousCulturalRightsLanguage },
      { href: "/dashboard/labor-union-collective-bargaining-engine", label: "Droits Syndicaux", icon: IconLaborUnionCollectiveBargaining },
      { href: "/dashboard/elderly-rights-ageism-engine", label: "Droits Personnes Âgées", icon: IconElderlyRightsAgeism },
      { href: "/dashboard/anti-money-laundering-human-rights-engine", label: "Blanchiment &amp; Droits", icon: IconAntiMoneyLaunderingHumanRights },
      { href: "/dashboard/settler-colonialism-land-rights-engine", label: "Colonialisme &amp; Droits Fonciers", icon: IconSettlerColonialismLandRights },
      { href: "/dashboard/social-media-platform-accountability-engine", label: "Responsabilité Plateformes", icon: IconSocialMediaPlatformAccountability },
      { href: "/dashboard/refugee-return-voluntary-repatriation-engine", label: "Retour Réfugiés", icon: IconRefugeeReturnVoluntaryRepatriation },
      { href: "/dashboard/corporate-tax-justice-development-engine", label: "Justice Fiscale Corporative", icon: IconCorporateTaxJusticeDevelopment },
      { href: "/dashboard/prison-conditions-torture-engine", label: "Conditions Carcérales &amp; Torture", icon: IconPrisonConditionsTorture },
      { href: "/dashboard/ai-autonomous-weapons-human-rights-engine", label: "IA &amp; Armes Autonomes", icon: IconAIAutonomousWeaponsHumanRights },
      { href: "/dashboard/gender-pay-gap-economic-rights-engine", label: "Écart Salarial Femmes", icon: IconGenderPayGapEconomicRights },
      { href: "/dashboard/conflict-mineral-resources-engine", label: "Minerais de Conflit", icon: IconConflictMineralResources },
      { href: "/dashboard/stateless-persons-documentation-engine", label: "Apatridie & Documentation", icon: IconStatelessPersonsNationalityRights },
      { href: "/dashboard/anti-personnel-mines-cluster-munitions-engine", label: "Mines Antipersonnel", icon: IconAntiPersonnelMinesClusterMunitions },
      { href: "/dashboard/peacekeeping-accountability-governance-engine", label: "Responsabilité OMP", icon: IconPeacekeepingAccountabilityGovernance },
      { href: "/dashboard/trafficking-forced-labor-modern-slavery-engine", label: "Traite & Esclavage Moderne", icon: IconHumanTraffickingModernSlavery },
      { href: "/dashboard/arbitrary-detention-political-prisoners-engine", label: "Détention Arbitraire", icon: IconArbitraryDetention },
      { href: "/dashboard/land-rights-eviction-indigenous-territories-engine", label: "Droits Fonciers Autochtones", icon: IconIndigenousLandRightsExtraction },
      { href: "/dashboard/digital-surveillance-mass-monitoring-engine", label: "Surveillance Numérique", icon: IconDigitalSurveillanceMassMonitoring },
      { href: "/dashboard/child-soldiers-armed-recruitment-engine", label: "Enfants Soldats", icon: IconChildSoldiers },
      { href: "/dashboard/sexual-violence-conflict-weapon-engine", label: "Violence Sexuelle Conflit", icon: IconSexualViolenceWartime },
      { href: "/dashboard/environmental-defenders-killings-engine", label: "Défenseurs Environnement", icon: IconEnvironmentalDefendersRights },
      { href: "/dashboard/access-water-sanitation-rights-engine", label: "Droit à l&apos;Eau", icon: IconWaterSanitationRights },
      { href: "/dashboard/lgbtqi-rights-criminalization-engine", label: "Droits LGBTQI+", icon: IconLgbtqRightsCriminalization },
      { href: "/dashboard/corporate-impunity-accountability-engine", label: "Impunité Corporate", icon: IconCorporateImpunity },
      { href: "/dashboard/freedom-religion-belief-persecution-engine", label: "Liberté Religion", icon: IconFreedomReligionBelief },
      { href: "/dashboard/extraordinary-rendition-secret-detention-engine", label: "Renditions Secrètes", icon: IconExtraordinaryRenditionSecretDetention },
      { href: "/dashboard/critical-minerals-transition-rights-engine", label: "Minéraux Critiques", icon: IconCriticalMineralsTransitionRights },
      { href: "/dashboard/mega-infrastructure-construction-labor-engine", label: "Infrastructures Méga", icon: IconMegaInfrastructureConstructionLabor },
      { href: "/dashboard/biometric-border-surveillance-migration-engine", label: "Surveillance Frontières", icon: IconBiometricSurveillance },
      { href: "/dashboard/agribusiness-land-grab-community-rights-engine", label: "Accaparement Terres", icon: IconLandGrabbingRights },
      { href: "/dashboard/icc-universal-jurisdiction-impunity-engine", label: "CPI & Impunité", icon: IconIccUniversalJurisdictionImpunity },
      { href: "/dashboard/stateless-persons-nationality-rights-engine", label: "Apatridie & Nationalité", icon: IconStatelessPersonsNationalityRights },
      { href: "/dashboard/whistleblower-protection-corporate-accountability-engine", label: "Lanceurs d'Alerte", icon: IconWhistleblowerProtection },
      { href: "/dashboard/housing-forced-evictions-gentrification-engine", label: "Expulsions & Logement", icon: IconHousingRightsForcedEvictions },
      { href: "/dashboard/disability-rights-social-exclusion-engine", label: "Droits Handicapés", icon: IconDisabilityRights },
      { href: "/dashboard/organ-trafficking-human-parts-engine", label: "Trafic d'Organes", icon: IconOrganTrafficking },
      { href: "/dashboard/online-censorship-internet-freedom-engine", label: "Censure Internet", icon: IconInternetFreedomCensorship },
      { href: "/dashboard/prison-labor-exploitation-rehabilitation-engine", label: "Travail Carcéral & Réhabilitation", icon: IconPrisonRehabilitationReentryRights },
      { href: "/dashboard/sex-work-criminalization-trafficking-engine", label: "Criminalisation Travail Sexuel", icon: IconSexWorkerRightsCriminalization },
      { href: "/dashboard/forced-marriage-honor-violence-engine", label: "Mariages Forcés & Crimes d'Honneur", icon: IconChildMarriageForcedUnion },
      { href: "/dashboard/autonomous-weapons-killer-robots-engine", label: "Armes Autonomes Létales", icon: IconAIAutonomousWeaponsHumanRights },
      { href: "/dashboard/pharmaceutical-access-medicine-rights-engine", label: "Accès Médicaments", icon: IconPandemicHealthEmergencyRights },
      { href: "/dashboard/modern-slavery-forced-labor-contemporary-engine", label: "Esclavage Moderne", icon: IconHumanTraffickingModernSlavery },
      { href: "/dashboard/climate-justice-climate-refugees-rights-engine", label: "Justice Climatique", icon: IconClimateJustice },
      { href: "/dashboard/food-right-agribusiness-hunger-engine", label: "Droit à l&apos;Alimentation", icon: IconFoodSovereigntyRightToFood },
      { href: "/dashboard/genocide-prevention-early-warning-engine", label: "Prévention Génocide & Alerte", icon: IconGenocidePreventionAccountability },
      { href: "/dashboard/child-soldiers-armed-recruitment-contemporain-engine", label: "Enfants Soldats Contemporain", icon: IconChildSoldiers },
      { href: "/dashboard/solitary-confinement-torture-methods-engine", label: "Isolement & Torture", icon: IconSolitaryConfinement },
      { href: "/dashboard/debt-bondage-microfinance-exploitation-engine", label: "Microfinance & Servitude Dette", icon: IconDebtBondageMicrofinanceExploitation },
      { href: "/dashboard/sexual-orientation-gender-identity-rights-engine", label: "Droits SOGI & LGBTQ+", icon: IconSexualOrientationGenderIdentityRights },
      { href: "/dashboard/indigenous-cultural-genocide-assimilation-engine", label: "Génocide Culturel Autochtone", icon: IconIndigenousCulturalGenocideAssimilation },
      { href: "/dashboard/disability-rights-inclusive-development-engine", label: "Droits Handicap & Inclusion", icon: IconDisabilityRightsInclusiveDevelopment },
      { href: "/dashboard/kafala-migrant-domestic-workers-rights-engine", label: "Kafala & Travailleurs Migrants", icon: IconKafalaMigrantDomesticWorkers },
      { href: "/dashboard/whistleblower-press-freedom-protection-engine", label: "Liberté Presse & Lanceurs Alerte", icon: IconWhistleblowerPressFreedom },
      { href: "/dashboard/nuclear-testing-radiation-victims-engine", label: "Victimes Tests Nucléaires", icon: IconNuclearTestingRadiationVictims },
      { href: "/dashboard/stateless-persons-documentation-crisis-engine", label: "Apatrides & Crise Docs", icon: IconStatelessPersonsDocumentationCrisis },
      { href: "/dashboard/private-military-contractors-accountability-engine", label: "Contractants Militaires PMC", icon: IconPrivateMilitaryContractorsAccountability },
      { href: "/dashboard/femicide-gender-based-killings-engine", label: "Féminicide & Crimes Genre", icon: IconFemicideGenderBasedKillings },
      { href: "/dashboard/romani-sinti-anti-ziganism-rights-engine", label: "Droits Roms & Anti-Tziganisme", icon: IconRomaniSintiAntiZiganism },
      { href: "/dashboard/colonial-restitution-cultural-heritage-engine", label: "Restitution Coloniale & Patrimoine", icon: IconColonialRestitutionHeritage },
      { href: "/dashboard/intersex-rights-bodily-integrity-engine", label: "Droits Intersexes & Intégrité Corporelle", icon: IconIntersexRightsBodily },
      { href: "/dashboard/mental-health-detention-psychiatric-rights-engine", label: "Détention Psychiatrique & Droits Santé Mentale", icon: IconMentalHealthDetention },
      { href: "/dashboard/peasant-rights-small-farmer-displacement-engine", label: "Droits Paysans & Déplacement Agricole", icon: IconPeasantRightsSmallFarmer },
      { href: "/dashboard/organ-trafficking-transplant-tourism-engine", label: "Trafic Organes & Tourisme Transplant", icon: IconOrganTraffickingTransplant },
      { href: "/dashboard/digital-surveillance-pegasus-spyware-engine", label: "Surveillance Numérique & Pegasus", icon: IconDigitalSurveillancePegasus },
      { href: "/dashboard/death-penalty-wrongful-execution-engine", label: "Peine de Mort & Exécutions Erronées", icon: IconDeathPenaltyWrongfulExecution },
      { href: "/dashboard/enforced-disappearances-extrajudicial-engine", label: "Disparitions Forcées & Extrajudiciaires", icon: IconEnforcedDisappearancesExtrajudicial },
      { href: "/dashboard/housing-forced-evictions-rights-engine", label: "Logement & Expulsions Forcées W187", icon: IconHousingForcedEvictionsRights },
      { href: "/dashboard/quantum-surveillance-privacy-rights-engine", label: "Surveillance Quantique", icon: IconQuantumSurveillancePrivacy },
      { href: "/dashboard/post-quantum-cryptography-rights-engine", label: "Cryptographie Post-Quantique", icon: IconPostQuantumCryptography },
      { href: "/dashboard/quantum-supremacy-arms-race-engine", label: "Suprématie Quantique", icon: IconQuantumSupremacyArmsRace },
      { href: "/dashboard/biotech-genetic-discrimination-rights-engine", label: "Génétique & Discrimination", icon: IconBiotechGeneticDiscrimination },
      { href: "/dashboard/carbon-colonialism-climate-justice-engine", label: "Colonialisme Carbone", icon: IconCarbonColonialismClimateJustice },
      { href: "/dashboard/digital-feudalism-platform-rights-engine", label: "Féodalisme Numérique", icon: IconDigitalFeudalismPlatformRights },
      { href: "/dashboard/neurotech-cognitive-liberty-rights-engine", label: "Neurotechnologie & Liberté", icon: IconNeurotechCognitiveLibertyRights },
      { href: "/dashboard/space-colonization-indigenous-rights-engine", label: "Espace & Droits Autochtones", icon: IconSpaceColonizationIndigenousRights },
      { href: "/dashboard/synthetic-biology-biosafety-rights-engine", label: "Biologie Synthétique", icon: IconSyntheticBiologyBiosafetyRights },
    ],
  },
  {
    title: "QUANTUM",
    items: [
      { href: "/dashboard/quantum-surveillance-privacy-rights-engine", label: "Surveillance Quantique", icon: IconQuantumSurveillancePrivacy },
      { href: "/dashboard/post-quantum-cryptography-rights-engine", label: "Cryptographie Post-Quantum", icon: IconPostQuantumCryptography },
      { href: "/dashboard/quantum-supremacy-arms-race-engine", label: "Suprématie Quantique", icon: IconQuantumSupremacyArmsRace },
    ],
  },
  {
    title: "WAVE 191",
    items: [
      { href: "/dashboard/algorithmic-justice-bias-rights-engine", label: "Justice Algorithmique", icon: IconAlgorithmicJusticeBiasRights },
      { href: "/dashboard/water-privatization-commons-rights-engine", label: "Eau & Droits Communs", icon: IconWaterPrivatizationCommonsRights },
      { href: "/dashboard/prison-industrial-complex-rights-engine", label: "Complexe Carcéral", icon: IconPrisonIndustrialComplexRights },
    ],
  },
  {
    title: "DROITS NUMÉRIQUES — WAVE 192",
    items: [
      { href: "/dashboard/dark-web-cybercrime-rights-engine", label: "Dark Web & Cybercrime", icon: IconDarkWebCybercrimeRights },
      { href: "/dashboard/gig-economy-labor-exploitation-engine", label: "Économie Gig & Travail", icon: IconGigEconomyLaborExploitation },
      { href: "/dashboard/indigenous-language-extinction-rights-engine", label: "Langues Autochtones", icon: IconIndigenousLanguageExtinction },
    ],
  },
  {
    title: "DROITS — WAVE 193",
    items: [
      { href: "/dashboard/deepfake-synthetic-media-rights-engine", label: "Deepfake & Médias Synth.", icon: IconDeepfakeSyntheticMediaRights },
      { href: "/dashboard/offshore-tax-haven-rights-engine", label: "Paradis Fiscaux", icon: IconOffshoreTaxHavenRights },
      { href: "/dashboard/statelessness-document-rights-engine", label: "Apatridie & Documents", icon: IconStatelessnessDocumentRights },
    ],
  },
  {
    title: "DROITS — WAVE 194",
    items: [
      { href: "/dashboard/conflict-mineral-supply-chain-engine", label: "Minéraux de Conflit", icon: IconConflictMineralSupplyChain },
      { href: "/dashboard/refugee-camp-rights-engine", label: "Camps de Réfugiés", icon: IconRefugeeCampRights },
      { href: "/dashboard/corporate-impunity-legal-gap-engine", label: "Impunité Corporative", icon: IconCorporateImpunityLegal },
    ],
  },
  {
    title: "DROITS — WAVE 195",
    items: [
      { href: "/dashboard/child-agricultural-labor-engine", label: "Travail Agricole Enfants", icon: IconChildAgriculturalLabor },
      { href: "/dashboard/digital-surveillance-rights-engine", label: "Surveillance Numérique", icon: IconDigitalSurveillanceMassRights },
      { href: "/dashboard/forced-eviction-land-rights-engine", label: "Expulsion & Droits Fonciers", icon: IconForcedEvictionLandRights },
    ],
  },
  {
    title: "DROITS — WAVE 196",
    items: [
      { href: "/dashboard/toxic-waste-environmental-health-engine", label: "Déchets Toxiques & Santé", icon: IconToxicWasteEnvironmentalHealth },
      { href: "/dashboard/prison-labor-rights-engine", label: "Travail Pénitentiaire", icon: IconPrisonLaborRights },
      { href: "/dashboard/gig-workers-platform-economy-engine", label: "Économie Plateformes", icon: IconGigWorkersPlatformEconomy },
    ],
  },
  {
    title: "DROITS — WAVE 197",
    items: [
      { href: "/dashboard/water-access-rights-engine", label: "Droits d'Accès à l'Eau", icon: IconWaterAccessRights },
      { href: "/dashboard/indigenous-peoples-rights-engine", label: "Peuples Autochtones", icon: IconIndigenousPeoplesRights },
      { href: "/dashboard/academic-freedom-suppression-engine", label: "Liberté Académique", icon: IconAcademicFreedomSuppression },
    ],
  },
  {
    title: "DROITS — WAVE 198",
    items: [
      { href: "/dashboard/gender-pay-gap-discrimination-engine", label: "Discrimination Salariale Genre", icon: IconGenderPayGap },
      { href: "/dashboard/refugee-asylum-rights-engine", label: "Droits des Réfugiés", icon: IconRefugeeAsylumRights },
      { href: "/dashboard/corporate-tax-evasion-engine", label: "Évasion Fiscale Corp.", icon: IconCorporateTaxEvasion },
    ],
  },
  {
    title: "DROITS — WAVE 199",
    items: [
      { href: "/dashboard/mental-health-workplace-rights-engine", label: "Santé Mentale Travail", icon: IconMentalHealthWorkplace },
      { href: "/dashboard/media-censorship-press-freedom-engine", label: "Censure & Liberté Presse", icon: IconMediaCensorshipPress },
      { href: "/dashboard/disability-rights-accessibility-engine", label: "Droits Handicap", icon: IconDisabilityRightsAccessibility },
    ],
  },
  {
    title: "DROITS — WAVE 200",
    items: [
      { href: "/dashboard/fast-fashion-textile-rights-engine", label: "Fast Fashion & Textiles", icon: IconFastFashionTextile },
      { href: "/dashboard/elderly-care-rights-engine", label: "Droits Personnes Âgées", icon: IconElderlyCarePRights },
      { href: "/dashboard/genetic-data-privacy-rights-engine", label: "Données Génétiques", icon: IconGeneticDataPrivacy },
    ],
  },
  {
    title: "DROITS — WAVE 201",
    items: [
      { href: "/dashboard/artisanal-mining-rights-engine", label: "Mines Artisanales", icon: IconArtisanalMiningRights },
      { href: "/dashboard/sports-labor-mega-events-engine", label: "Sport & Droits Travail", icon: IconSportsLaborMegaEvents },
      { href: "/dashboard/pharmaceutical-access-patents-engine", label: "Accès Médicaments", icon: IconPharmaAccessPatents },
    ],
  },
  {
    title: "DROITS — WAVE 202",
    items: [
      { href: "/dashboard/ocean-fishing-rights-engine", label: "Pêche & Droits Maritimes", icon: IconOceanFishingRights },
      { href: "/dashboard/land-grabbing-agribusiness-engine", label: "Accaparement Terres", icon: IconLandGrabbingAgribusiness },
      { href: "/dashboard/biometric-surveillance-rights-engine", label: "Surveillance Biométrique", icon: IconBiometricSurveillance },
    ],
  },
  {
    title: "DROITS — WAVE 203",
    items: [
      { href: "/dashboard/crypto-energy-rights-engine", label: "Crypto Énergie & Droits", icon: IconCryptoEnergyRights },
      { href: "/dashboard/colonial-reparations-rights-engine", label: "Réparations Coloniales", icon: IconColonialReparations },
      { href: "/dashboard/ai-algorithmic-bias-rights-engine", label: "Biais IA & Discrimination", icon: IconAIAlgorithmicBias },
    ],
  },
  {
    title: "DROITS — WAVE 204",
    items: [
      { href: "/dashboard/conflict-minerals-drc-engine", label: "Minerais Conflit RDC", icon: IconConflictMineralsDRC },
      { href: "/dashboard/human-trafficking-modern-slavery-engine", label: "Traite & Esclavage Moderne", icon: IconHumanTraffickingSlavery },
      { href: "/dashboard/water-pollution-corporate-liability-engine", label: "Pollution Eau Corp.", icon: IconWaterPollutionLiability },
    ],
  },
  {
    title: "DROITS — WAVE 205",
    items: [
      { href: "/dashboard/nuclear-energy-community-rights-engine", label: "Nucléaire & Communautés", icon: IconNuclearEnergyRights },
      { href: "/dashboard/e-waste-recycling-rights-engine", label: "Déchets Électroniques", icon: IconEWasteRecycling },
      { href: "/dashboard/debt-bondage-migrant-workers-engine", label: "Servitude Dettes Migrants", icon: IconDebtBondageMigrant },
    ],
  },
  {
    title: "DROITS — WAVE 206",
    items: [
      { href: "/dashboard/deforestation-palm-oil-rights-engine", label: "Déforestation & Huile Palme", icon: IconDeforestationPalmOil },
      { href: "/dashboard/child-soldiers-armed-groups-engine", label: "Enfants Soldats", icon: IconChildSoldiersArmed },
      { href: "/dashboard/seed-patents-food-sovereignty-engine", label: "Brevets Semences", icon: IconSeedPatentsSovereignty },
    ],
  },
  {
    label: "DROITS — WAVE 208",
    items: [
      { href: "/dashboard/space-mining-rights-engine", label: "Space Mining Rights", icon: IconSpaceMiningRights },
      { href: "/dashboard/surveillance-capitalism-rights-engine", label: "Surveillance Capitalism", icon: IconSurveillanceCapitalism },
      { href: "/dashboard/mental-health-social-media-rights-engine", label: "Mental Health Social Media", icon: IconMentalHealthSocialMedia },
    ],
  },
  {
    title: "DROITS — WAVE 207",
    items: [
      { href: "/dashboard/lithium-battery-rights-engine", label: "Lithium Battery Rights", icon: IconLithiumBatteryRights },
      { href: "/dashboard/dark-patterns-consumer-rights-engine", label: "Dark Patterns Consumer", icon: IconDarkPatternsConsumer },
      { href: "/dashboard/land-rights-climate-displacement-engine", label: "Land Rights Climate", icon: IconLandRightsClimate },
    ],
  },
  {
    label: "DROITS — WAVE 209",
    items: [
      { href: "/dashboard/agricultural-pesticides-rights-engine", label: "Agricultural Pesticides", icon: IconAgriculturalPesticides },
      { href: "/dashboard/homelessness-housing-rights-engine", label: "Homelessness Housing", icon: IconHomelessnessHousing },
      { href: "/dashboard/water-privatisation-rights-engine", label: "Water Privatisation", icon: IconWaterPrivatisation },
    ],
  },
  {
    label: "DROITS — WAVE 210",
    items: [
      { href: "/dashboard/forced-marriage-rights-engine", label: "Mariages Forcés", icon: IconForcedMarriageRights },
      { href: "/dashboard/statelessness-rights-engine", label: "Apatridie", icon: IconStatelessnessRights },
      { href: "/dashboard/child-marriage-labor-engine", label: "Mariages & Travail Enfants", icon: IconChildMarriageLabor },
    ],
  },
  {
    label: "DROITS — WAVE 211",
    items: [
      { href: "/dashboard/digital-colonialism-rights-engine", label: "Colonialisme Numérique", icon: IconDigitalColonialism },
      { href: "/dashboard/reproductive-rights-engine", label: "Droits Reproductifs", icon: IconReproductiveRights },
      { href: "/dashboard/indigenous-land-rights-engine", label: "Droits Fonciers Autochtones", icon: IconIndigenousLandRights },
    ],
  },
  {
    label: "DROITS — WAVE 212",
    items: [
      { href: "/dashboard/climate-refugees-rights-engine", label: "Réfugiés Climatiques", icon: IconClimateRefugeesRights },
      { href: "/dashboard/transgender-rights-engine", label: "Droits Trans", icon: IconTransgenderRights },
      { href: "/dashboard/housing-eviction-rights-engine", label: "Expulsions Logement", icon: IconHousingEvictionRights },
    ],
  },
  {
    label: "DROITS — WAVE 213",
    items: [
      { href: "/dashboard/food-sovereignty-rights-engine", label: "Souveraineté Alimentaire", icon: IconFoodSovereigntyRights },
      { href: "/dashboard/corporate-impunity-rights-engine", label: "Impunité Corporative", icon: IconCorporateImpunityRights },
      { href: "/dashboard/internet-access-rights-engine", label: "Accès Internet", icon: IconInternetAccessRights },
    ],
  },
  {
    label: "DROITS — WAVE 214",
    items: [
      { href: "/dashboard/medical-debt-rights-engine", label: "Dettes Médicales", icon: IconMedicalDebtRights },
      { href: "/dashboard/cultural-heritage-rights-engine", label: "Patrimoine Culturel", icon: IconCulturalHeritageRights },
      { href: "/dashboard/whistleblower-rights-engine", label: "Lanceurs d'Alerte", icon: IconWhistleblowerRights },
    ],
  },
  {
    label: "DROITS — WAVE 215",
    items: [
      { href: "/dashboard/refugee-camp-rights-engine", label: "Camps de Réfugiés", icon: IconRefugeeCampRights },
      { href: "/dashboard/pension-elderly-rights-engine", label: "Pension & Personnes Âgées", icon: IconPensionElderlyRights },
      { href: "/dashboard/dark-web-rights-engine", label: "Droits & Dark Web", icon: IconDarkWebRights },
    ],
  },
  {
    label: "DROITS — WAVE 216",
    items: [
      { href: "/dashboard/arms-trade-rights-engine", label: "Commerce d'Armes", icon: IconArmsTradeRights },
      { href: "/dashboard/disability-rights-engine", label: "Droits Handicap", icon: IconDisabilityRights },
      { href: "/dashboard/racial-discrimination-rights-engine", label: "Discrimination Raciale", icon: IconRacialDiscriminationRights },
    ],
  },
  {
    label: "DROITS — WAVE 217",
    items: [
      { href: "/dashboard/environmental-racism-rights-engine", label: "Racisme Environnemental", icon: IconEnvironmentalRacismRights },
      { href: "/dashboard/migrant-worker-rights-engine", label: "Travailleurs Migrants", icon: IconMigrantWorkerRights },
      { href: "/dashboard/child-poverty-rights-engine", label: "Pauvreté Enfants", icon: IconChildPovertyRights },
    ],
  },
  {
    label: "DROITS — WAVE 218",
    items: [
      { href: "/dashboard/torture-prevention-rights-engine", label: "Prévention Torture", icon: IconTorturePreventionRights },
      { href: "/dashboard/freedom-assembly-rights-engine", label: "Liberté de Réunion", icon: IconFreedomAssemblyRights },
      { href: "/dashboard/corporate-tax-evasion-rights-engine", label: "Évasion Fiscale Entreprises", icon: IconCorporateTaxEvasionRights },
    ],
  },
  {
    label: "DROITS — WAVE 219",
    items: [
      { href: "/dashboard/gender-pay-gap-rights-engine", label: "Écart Salarial Femmes", icon: IconGenderPayGapRights },
      { href: "/dashboard/healthcare-access-rights-engine", label: "Accès aux Soins", icon: IconHealthcareAccessRights },
      { href: "/dashboard/anti-corruption-rights-engine", label: "Droits Anticorruption", icon: IconAntiCorruptionRights },
    ],
  },
  {
    label: "DROITS — WAVE 220",
    items: [
      { href: "/dashboard/birth-registration-rights-engine", label: "Enreg. Naissances Droits", icon: IconBirthRegistrationRights },
      { href: "/dashboard/humanitarian-access-rights-engine", label: "Accès Humanitaire Conflits", icon: IconHumanitarianAccessRights },
      { href: "/dashboard/journalism-safety-rights-engine", label: "Sécurité Journalistes Presse", icon: IconJournalismSafetyRights },
    ],
  },
  {
    title: "DROITS — WAVE 221",
    items: [
      { href: "/dashboard/statelessness-rights-engine", label: "Apatridie & Nationalité", icon: IconStatelessnessRights },
      { href: "/dashboard/water-access-rights-engine", label: "Eau Potable & WASH", icon: IconWaterAccessRights },
      { href: "/dashboard/digital-privacy-rights-engine", label: "Vie Privée Numérique", icon: IconDigitalPrivacyRights },
    ],
  },
  {
    title: "DROITS — WAVE 222",
    items: [
      { label: "Travail Forcé & Esclavage", href: "/dashboard/forced-labor-rights-engine", icon: IconForcedLaborRights },
      { label: "Droits Fonciers Autochtones", href: "/dashboard/indigenous-land-rights-engine", icon: IconIndigenousLandRights },
      { label: "Droits LGBTQ+", href: "/dashboard/lgbtq-rights-engine", icon: IconLGBTQRights },
    ],
  },
  {
    title: "DROITS — WAVE 223",
    items: [
      { label: "Sécurité Alimentaire", href: "/dashboard/food-security-rights-engine", icon: IconFoodSecurityRights },
      { label: "Réfugiés Climatiques", href: "/dashboard/climate-refugee-rights-engine", icon: IconClimateRefugeeRights },
      { label: "Droit au Logement", href: "/dashboard/housing-rights-engine", icon: IconHousingRights },
    ],
  },
  {
    title: "DROITS — WAVE 224",
    items: [
      { label: "Maltraitance Seniors", href: "/dashboard/elder-abuse-rights-engine", icon: IconElderAbuseRights },
      { label: "Accès Internet", href: "/dashboard/internet-access-rights-engine", icon: IconInternetAccessRights },
      { label: "Conditions Détention", href: "/dashboard/prison-conditions-rights-engine", icon: IconPrisonConditionsRights },
    ],
  },
  {
    title: "DROITS — WAVE 225",
    items: [
      { label: "Accaparement Terres", href: "/dashboard/land-grabbing-rights-engine", icon: IconLandGrabbingRights },
      { label: "Droits Minorités", href: "/dashboard/minority-rights-engine", icon: IconMinorityRights },
      { label: "Peine de Mort", href: "/dashboard/death-penalty-rights-engine", icon: IconDeathPenaltyRights },
    ],
  },
  {
    title: "QUANTIQUE — WAVE 226",
    items: [
      { label: "Surveillance Quantique", href: "/dashboard/quantum-surveillance-rights-engine", icon: IconQuantumSurveillanceRights },
      { label: "Bioéthique Quantique", href: "/dashboard/quantum-bioethics-rights-engine", icon: IconQuantumBioethicsRights },
      { label: "Fracture Quantique", href: "/dashboard/quantum-digital-divide-rights-engine", icon: IconQuantumDigitalDivideRights },
    ],
  },
  {
    title: "DROITS — WAVE 227",
    items: [
      { label: "Mariage Enfants & MGF", href: "/dashboard/child-marriage-rights-engine", icon: IconChildMarriageRights },
      { label: "Liberté Expression", href: "/dashboard/freedom-expression-rights-engine", icon: IconFreedomExpressionRights },
      { label: "Assainissement & Hygiène", href: "/dashboard/sanitation-hygiene-rights-engine", icon: IconSanitationHygieneRights },
    ],
  },
  {
    title: "DROITS — WAVE 228",
    items: [
      { label: "Traite des Êtres Humains", href: "/dashboard/human-trafficking-rights-engine", icon: IconHumanTraffickingRights },
      { label: "Droit à l'Éducation", href: "/dashboard/right-to-education-rights-engine", icon: IconRightToEducationRights },
      { label: "Protection Sociale", href: "/dashboard/social-security-rights-engine", icon: IconSocialSecurityRights },
    ],
  },
  {
    title: "DROITS — WAVE 229",
    items: [
      { label: "Droit d'Asile", href: "/dashboard/asylum-rights-engine", icon: IconAsylumRights },
      { label: "Santé Mentale", href: "/dashboard/mental-health-rights-engine", icon: IconMentalHealthRights },
      { label: "Savoirs Autochtones", href: "/dashboard/indigenous-knowledge-rights-engine", icon: IconIndigenousKnowledgeRights },
    ],
  },
  {
    title: "DROITS — WAVE 230",
    items: [
      { href: "/dashboard/gender-based-violence-rights-engine", label: "Violences de Genre", icon: IconGenderBasedViolenceRights },
      { href: "/dashboard/child-labor-rights-engine", label: "Travail des Enfants", icon: IconChildLaborRights },
      { href: "/dashboard/tax-justice-rights-engine", label: "Justice Fiscale", icon: IconTaxJusticeRights },
    ],
  },
  {
    title: "DROITS — WAVE 231",
    items: [
      { href: "/dashboard/right-to-fair-trial-rights-engine", label: "Procès Équitable", icon: IconRightToFairTrialRights },
      { href: "/dashboard/environmental-pollution-rights-engine", label: "Pollution Environnementale", icon: IconEnvironmentalPollutionRights },
      { href: "/dashboard/collective-bargaining-rights-engine", label: "Négociation Collective", icon: IconCollectiveBargainingRights },
    ],
  },
  {
    title: "DROITS — WAVE 232",
    items: [
      { href: "/dashboard/women-political-rights-engine", label: "Droits Politiques Femmes", icon: IconWomenPoliticalRights },
      { href: "/dashboard/climate-change-rights-engine", label: "Changement Climatique", icon: IconClimateChangeRights },
      { href: "/dashboard/forced-sterilization-rights-engine", label: "Stérilisation Forcée", icon: IconForcedSterilizationRights },
    ],
  },
  {
    title: "DROITS — WAVE 233",
    items: [
      { href: "/dashboard/stateless-children-rights-engine", label: "Enfants Apatrides", icon: IconStatelessChildrenRights },
      { href: "/dashboard/hate-speech-incitement-rights-engine", label: "Discours Haineux", icon: IconHateSpeechIncitementRights },
      { href: "/dashboard/land-restitution-rights-engine", label: "Restitution des Terres", icon: IconLandRestitutionRights },
    ],
  },
  {
    title: "DROITS — WAVE 234",
    items: [
      { href: "/dashboard/organ-harvesting-rights-engine", label: "Trafic d'Organes", icon: IconOrganHarvestingRights },
      { href: "/dashboard/right-to-nationality-rights-engine", label: "Droit à la Nationalité", icon: IconRightToNationalityRights },
      { href: "/dashboard/internet-censorship-rights-engine", label: "Censure Internet", icon: IconInternetCensorshipRights },
    ],
  },
  {
    title: "DROITS — WAVE 235",
    items: [
      { href: "/dashboard/medical-experimentation-rights-engine", label: "Expérimentation Médicale", icon: IconMedicalExperimentationRights },
      { href: "/dashboard/economic-sanctions-rights-engine", label: "Sanctions Économiques", icon: IconEconomicSanctionsRights },
      { href: "/dashboard/solitary-confinement-rights-engine", label: "Confinement Solitaire", icon: IconSolitaryConfinementRights },
    ],
  },
  {
    title: "DROITS — WAVE 236",
    items: [
      { href: "/dashboard/net-neutrality-rights-engine", label: "Neutralité du Net", icon: IconNetNeutralityRights },
      { href: "/dashboard/right-to-be-forgotten-rights-engine", label: "Droit à l'Oubli", icon: IconRightToBeForgottenRights },
      { href: "/dashboard/digital-accessibility-rights-engine", label: "Accessibilité Numérique", icon: IconDigitalAccessibilityRights },
    ],
  },
  {
    title: "DROITS — WAVE 237",
    items: [
      { href: "/dashboard/freedom-of-assembly-rights-engine", label: "Liberté de Réunion", icon: IconFreedomOfAssemblyRights },
      { href: "/dashboard/right-to-housing-rights-engine", label: "Droit au Logement", icon: IconRightToHousingRights },
      { href: "/dashboard/juvenile-justice-rights-engine", label: "Justice des Mineurs", icon: IconJuvenileJusticeRights },
    ],
  },
  {
    title: "DROITS — WAVE 238",
    items: [
      { href: "/dashboard/arms-trade-human-rights-engine", label: "Commerce des Armes", icon: IconArmsTradeHumanRights },
      { href: "/dashboard/right-to-truth-rights-engine", label: "Droit à la Vérité", icon: IconRightToTruthRights },
      { href: "/dashboard/biometric-data-rights-engine", label: "Données Biométriques", icon: IconBiometricDataRights },
    ],
  },
  {
    title: "DROITS — WAVE 239",
    items: [
      { href: "/dashboard/anti-corruption-human-rights-engine", label: "Anti-Corruption", icon: IconAntiCorruptionHumanRights },
      { href: "/dashboard/women-economic-rights-engine", label: "Droits Éco. Femmes", icon: IconWomenEconomicRights },
      { href: "/dashboard/disability-rights-crpd-engine", label: "Droits Handicap CRPD", icon: IconDisabilityRightsCrpd },
    ],
  },
  {
    title: "DROITS — WAVE 240",
    items: [
      { href: "/dashboard/right-to-work-rights-engine", label: "Droit au Travail Décent", icon: IconRightToWorkRights },
      { href: "/dashboard/online-harassment-rights-engine", label: "Harcèlement en Ligne", icon: IconOnlineHarassmentRights },
      { href: "/dashboard/right-to-privacy-rights-engine", label: "Droit à la Vie Privée", icon: IconRightToPrivacyRights },
    ],
  },
  {
    title: "DROITS — WAVE 241",
    items: [
      { href: "/dashboard/religious-minority-rights-engine", label: "Religious Minority Rights", icon: IconReligiousMinorityRights },
      { href: "/dashboard/right-to-food-rights-engine", label: "Right to Food Rights", icon: IconRightToFoodRights },
      { href: "/dashboard/extrajudicial-killing-rights-engine", label: "Extrajudicial Killing Rights", icon: IconExtrajudicialKillingRights },
    ],
  },
  {
    title: "DROITS — WAVE 242",
    items: [
      { href: "/dashboard/cyber-espionage-rights-engine", label: "Cyber Espionage Rights", icon: IconCyberEspionageRights },
      { href: "/dashboard/racism-systemic-rights-engine", label: "Racism Systemic Rights", icon: IconRacismSystemicRights },
      { href: "/dashboard/climate-displacement-rights-engine", label: "Climate Displacement Rights", icon: IconClimateDisplacementRights },
    ],
  },
  {
    title: "DROITS — WAVE 243",
    items: [
      { href: "/dashboard/caste-discrimination-rights-engine", label: "Caste Discrimination Rights", icon: IconCasteDiscriminationRights },
      { href: "/dashboard/indigenous-language-rights-engine", label: "Indigenous Language Rights", icon: IconIndigenousLanguageRights },
      { href: "/dashboard/digital-authoritarianism-rights-engine", label: "Digital Authoritarianism Rights", icon: IconDigitalAuthoritarianismRights },
    ],
  },
  {
    title: "DROITS — WAVE 244",
    items: [
      { href: "/dashboard/housing-discrimination-rights-engine", label: "Housing Discrimination Rights", icon: IconHousingDiscriminationRights },
      { href: "/dashboard/forced-labor-supply-chain-rights-engine", label: "Forced Labor Supply Chain Rights", icon: IconForcedLaborSupplyChainRights },
      { href: "/dashboard/deepfake-rights-engine", label: "Deepfake Rights", icon: IconDeepfakeRights },
    ],
  },
  {
    title: "DROITS — WAVE 245",
    items: [
      { href: "/dashboard/organ-trafficking-rights-engine", label: "Organ Trafficking Rights", icon: IconOrganTraffickingRights, color: "#dc2626" },
      { href: "/dashboard/right-to-strike-rights-engine", label: "Right to Strike Rights", icon: IconRightToStrikeRights, color: "#ea580c" },
      { href: "/dashboard/journalist-protection-rights-engine", label: "Journalist Protection Rights", icon: IconJournalistProtectionRights, color: "#0369a1" },
    ],
  },
  {
    title: "DROITS — WAVE 246",
    items: [
      { href: "/dashboard/anti-money-laundering-rights-engine", label: "Anti-Money Laundering Rights", icon: IconAntiMoneyLaunderingRights, color: "#065f46" },
      { href: "/dashboard/sexual-violence-conflict-rights-engine", label: "Sexual Violence Conflict Rights", icon: IconSexualViolenceConflictRights, color: "#9f1239" },
      { href: "/dashboard/algorithmic-discrimination-rights-engine", label: "Algorithmic Discrimination Rights", icon: IconAlgorithmicDiscriminationRights, color: "#4338ca" },
    ],
  },
  {
    title: "DROITS — WAVE 247",
    items: [
      { href: "/dashboard/nuclear-testing-rights-engine", label: "Nuclear Testing Rights", icon: IconNuclearTestingRights, color: "#7f1d1d" },
      { href: "/dashboard/political-prisoner-rights-engine", label: "Political Prisoner Rights", icon: IconPoliticalPrisonerRights, color: "#1e3a5f" },
      { href: "/dashboard/sanctions-civilian-rights-engine", label: "Sanctions Civilian Rights", icon: IconSanctionsCivilianRights, color: "#44403c" },
    ],
  },
  {
    title: "DROITS — WAVE 248",
    items: [
      { href: "/dashboard/right-to-science-rights-engine", label: "Right to Science Rights", icon: IconRightToScienceRights, color: "#0c4a6e" },
      { href: "/dashboard/indigenous-self-determination-rights-engine", label: "Indigenous Self Determination Rights", icon: IconIndigenousSelfDeterminationRights, color: "#14532d" },
      { href: "/dashboard/ecocide-rights-engine", label: "Ecocide Rights", icon: IconEcocideRights, color: "#166534" },
    ],
  },
  {
    title: "DROITS — WAVE 249",
    items: [
      { href: "/dashboard/platform-workers-rights-engine", label: "Platform Workers Rights", icon: IconPlatformWorkersRights, color: "#1e40af" },
      { href: "/dashboard/right-to-water-rights-engine", label: "Right to Water Rights", icon: IconRightToWaterRights, color: "#0369a1" },
      { href: "/dashboard/land-mine-victims-rights-engine", label: "Land Mine Victims Rights", icon: IconLandMineVictimsRights, color: "#92400e" },
    ],
  },
  {
    title: "DROITS — WAVE 250",
    items: [
      { href: "/dashboard/stateless-adult-rights-engine", label: "Stateless Adult Rights", icon: IconStatelessAdultRights, color: "#374151" },
      { href: "/dashboard/armed-group-recruitment-rights-engine", label: "Armed Group Recruitment Rights", icon: IconArmedGroupRecruitmentRights, color: "#7f1d1d" },
      { href: "/dashboard/right-to-development-rights-engine", label: "Right to Development Rights", icon: IconRightToDevelopmentRights, color: "#065f46" },
    ],
  },
  {
    title: "DROITS — WAVE 251",
    items: [
      { href: "/dashboard/cultural-appropriation-rights-engine", label: "Cultural Appropriation Rights", icon: IconCulturalAppropriationRights, color: "#92400e" },
      { href: "/dashboard/hate-speech-online-rights-engine", label: "Hate Speech Online Rights", icon: IconHateSpeechOnlineRights, color: "#dc2626" },
      { href: "/dashboard/mass-incarceration-rights-engine", label: "Mass Incarceration Rights", icon: IconMassIncarcerationRights, color: "#1e3a5f" },
    ],
  },
  {
    title: "DROITS — WAVE 252",
    items: [
      { href: "/dashboard/colonial-genocide-rights-engine", label: "Colonial Genocide Rights", icon: IconColonialGenocideRights, color: "#7c2d12" },
      { href: "/dashboard/digital-divide-rural-rights-engine", label: "Digital Divide Rural Rights", icon: IconDigitalDivideRuralRights, color: "#166534" },
      { href: "/dashboard/refugee-integration-rights-engine", label: "Refugee Integration Rights", icon: IconRefugeeIntegrationRights, color: "#1e40af" },
    ],
  },
  {
    title: "DROITS — WAVE 253",
    items: [
      { href: "/dashboard/ai-weapons-rights-engine", label: "AI Weapons Rights", icon: IconAiWeaponsRights, color: "#1e293b" },
      { href: "/dashboard/water-conflict-rights-engine", label: "Water Conflict Rights", icon: IconWaterConflictRights, color: "#0369a1" },
      { href: "/dashboard/supply-chain-transparency-rights-engine", label: "Supply Chain Transparency Rights", icon: IconSupplyChainTransparencyRights, color: "#1d4ed8" },
    ],
  },
  {
    title: "DROITS — WAVE 254",
    items: [
      { href: "/dashboard/post-conflict-reconstruction-rights-engine", label: "Post-Conflict Reconstruction Rights", icon: IconPostConflictReconstructionRights, color: "#4b5563" },
      { href: "/dashboard/climate-finance-rights-engine", label: "Climate Finance Rights", icon: IconClimateFinanceRights, color: "#166534" },
      { href: "/dashboard/right-to-peace-rights-engine", label: "Right to Peace Rights", icon: IconRightToPeaceRights, color: "#0c4a6e" },
    ],
  },
  {
    title: "DROITS — WAVE 255",
    items: [
      { href: "/dashboard/gender-justice-rights-engine", label: "Gender Justice Rights", icon: IconGenderJusticeRights, color: "#db2777" },
      { href: "/dashboard/community-land-rights-engine", label: "Community Land Rights", icon: IconCommunityLandRights, color: "#15803d" },
      { href: "/dashboard/migration-governance-rights-engine", label: "Migration Governance Rights", icon: IconMigrationGovernanceRights, color: "#0284c7" },
    ],
  },
  {
    title: "DROITS — WAVE 256",
    items: [
      { label: "Right to Leisure Rights", href: "/dashboard/right-to-leisure-rights-engine", icon: IconRightToLeisureRights, color: "#6d28d9" },
      { label: "Social Protection Rights", href: "/dashboard/social-protection-rights-engine", icon: IconSocialProtectionRights, color: "#0891b2" },
      { label: "Prison Reform Rights", href: "/dashboard/prison-reform-rights-engine", icon: IconPrisonReformRights, color: "#374151" },
    ],
  },
  {
    title: "DROITS — WAVE 257",
    items: [
      { label: "Corporate Accountability Rights", href: "/dashboard/corporate-accountability-rights-engine", icon: IconCorporateAccountabilityRights, color: "#b45309" },
      { label: "Ethnic Cleansing Rights", href: "/dashboard/ethnic-cleansing-rights-engine", icon: IconEthnicCleansingRights, color: "#7c3aed" },
      { label: "Speech Surveillance Rights", href: "/dashboard/speech-surveillance-rights-engine", icon: IconSpeechSurveillanceRights, color: "#0f766e" },
    ],
  },
  {
    title: "DROITS — WAVE 258",
    items: [
      { label: "Lethal Autonomous Weapons Rights", href: "/dashboard/lethal-autonomous-weapons-rights-engine", icon: IconLethalAutonomousWeaponsRights, color: "#dc2626" },
      { label: "Protest Criminalization Rights", href: "/dashboard/protest-criminalization-rights-engine", icon: IconProtestCriminalizationRights, color: "#ea580c" },
      { label: "Cobalt Mining Rights", href: "/dashboard/cobalt-mining-rights-engine", icon: IconCobaltMiningRights, color: "#92400e" },
    ],
  },
  {
    title: "DROITS — WAVE 259",
    items: [
      { label: "Cognitive Liberty Rights", href: "/dashboard/cognitive-liberty-rights-engine", icon: IconCognitiveLibertyRights, color: "#6366f1" },
      { label: "Right to Repair Rights", href: "/dashboard/right-to-repair-rights-engine", icon: IconRightToRepairRights, color: "#16a34a" },
      { label: "Neuroethics Rights", href: "/dashboard/neuroethics-rights-engine", icon: IconNeuroethicsRights, color: "#8b5cf6" },
    ],
  },
  {
    title: "DROITS — WAVE 260",
    items: [
      { label: "SLAPP Suit Rights", href: "/dashboard/slapp-suit-rights-engine", icon: IconSlappSuitRights, color: "#f59e0b" },
      { label: "Conversion Therapy Rights", href: "/dashboard/conversion-therapy-rights-engine", icon: IconConversionTherapyRights, color: "#ec4899" },
      { label: "LGBTQ Criminalization Rights", href: "/dashboard/lgbtq-criminalization-rights-engine", icon: IconLgbtqCriminalizationRights, color: "#a855f7" },
    ],
  },
  {
    title: "DROITS — WAVE 261",
    items: [
      { label: "Femicide Accountability Rights", href: "/dashboard/femicide-accountability-rights-engine", icon: IconFemicideAccountabilityRights, color: "#be123c" },
      { label: "Street Harassment Rights", href: "/dashboard/street-harassment-rights-engine", icon: IconStreetHarassmentRights, color: "#ea580c" },
      { label: "Reproductive Coercion Rights", href: "/dashboard/reproductive-coercion-rights-engine", icon: IconReproductiveCoercionRights, color: "#be185d" },
    ],
  },
  {
    title: "DROITS — WAVE 262",
    items: [
      { label: "Economic Abuse Rights", href: "/dashboard/economic-abuse-rights-engine", icon: IconEconomicAbuseRights, color: "#ca8a04" },
      { label: "Mental Health Detention Rights", href: "/dashboard/mental-health-detention-rights-engine", icon: IconMentalHealthDetentionRights, color: "#7e22ce" },
      { label: "Psychiatric Abuse Rights", href: "/dashboard/psychiatric-abuse-rights-engine", icon: IconPsychiatricAbuseRights, color: "#1e3a5f" },
    ],
  },
  {
    title: "DROITS — WAVE 263",
    items: [
      { label: "Elder Financial Abuse Rights", href: "/dashboard/elder-financial-abuse-rights-engine", icon: IconElderFinancialAbuseRights, color: "#b45309" },
      { label: "Digital Divide Rights", href: "/dashboard/digital-divide-rights-engine", icon: IconDigitalDivideRights, color: "#0284c7" },
      { label: "Online Violence Women Rights", href: "/dashboard/online-violence-women-rights-engine", icon: IconOnlineViolenceWomenRights, color: "#db2777" },
    ],
  },
  {
    title: "DROITS — WAVE 264",
    items: [
      { href: "/dashboard/land-pollution-rights", label: "Pollution des Terres", icon: IconLandPollutionRights },
      { href: "/dashboard/air-quality-rights", label: "Qualité de l&apos;Air", icon: IconAirQualityRights },
      { href: "/dashboard/endocrine-disruptor-rights", label: "Perturbateurs Endocriniens", icon: IconEndocrineDisruptorRights },
    ],
  },
  {
    title: "DROITS — WAVE 265",
    items: [
      { href: "/dashboard/food-desert-rights", label: "Déserts Alimentaires", icon: IconFoodDesertRights },
      { href: "/dashboard/ocean-rights", label: "Droits Océaniques", icon: IconOceanRights },
      { href: "/dashboard/toxic-waste-dumping-rights", label: "Déchets Toxiques", icon: IconToxicWasteDumpingRights },
    ],
  },
  {
    title: "DROITS — WAVE 266",
    items: [
      { href: "/dashboard/biopiracy-rights", label: "Biopiraterie", icon: IconBiopiacyRights },
      { href: "/dashboard/conflict-mineral-rights", label: "Minérais de Conflit", icon: IconConflictMineralRights },
      { href: "/dashboard/forced-relocation-rights", label: "Déplacements Forcés", icon: IconForcedRelocationRights },
    ],
  },
  {
    title: "DROITS — WAVE 267",
    items: [
      { href: "/dashboard/water-privatization-rights", label: "Privatisation de l'Eau", icon: IconWaterPrivatizationRights },
      { href: "/dashboard/artisanal-mining-rights", label: "Mines Artisanales", icon: IconArtisanalMiningRights },
      { href: "/dashboard/sexual-exploitation-supply-chain", label: "Exploitation Sexuelle", icon: IconSexualExploitationSupplyChainRights },
    ],
  },
  {
    title: "DROITS — WAVE 268",
    items: [
      { href: "/dashboard/pesticide-exposure-rights", label: "Exposition aux Pesticides", icon: IconPesticideExposureRights },
      { href: "/dashboard/garment-worker-rights", label: "Travailleurs du Textile", icon: IconGarmentWorkerRights },
      { href: "/dashboard/cobalt-mining-rights", label: "Mines de Cobalt", icon: IconCobaltMiningRights },
    ],
  },
  {
    title: "DROITS — WAVE 269",
    items: [
      { href: "/dashboard/deforestation-rights", label: "Droits contre la Déforestation", icon: IconDeforestationRights },
      { href: "/dashboard/mica-mining-rights", label: "Extraction du Mica", icon: IconMicaMiningRights },
      { href: "/dashboard/climate-displacement-rights", label: "Déplacés Climatiques", icon: IconClimateDisplacementRights },
    ],
  },
  {
    title: "DROITS — WAVE 270",
    items: [
      { href: "/dashboard/indigenous-cultural-heritage-rights", label: "Patrimoine Autochtone", icon: IconIndigenousCulturalHeritageRights },
      { href: "/dashboard/deep-sea-mining-rights", label: "Mines des Fonds Marins", icon: IconDeepSeaMiningRights },
      { href: "/dashboard/fast-fashion-rights", label: "Fast Fashion", icon: IconFastFashionRights },
    ],
  },
  {
    title: "DROITS — WAVE 271",
    items: [
      { href: "/dashboard/wage-theft-rights", label: "Vol de Salaire", icon: IconWageTheftRights },
      { href: "/dashboard/drone-surveillance-rights", label: "Surveillance par Drones", icon: IconDroneSurveillanceRights },
      { href: "/dashboard/plastic-pollution-rights", label: "Pollution Plastique", icon: IconPlasticPollutionRights },
    ],
  },
  {
    title: "DROITS — WAVE 272",
    items: [
      { href: "/dashboard/supply-chain-transparency-rights", label: "Transparence des Chaînes", icon: IconSupplyChainTransparencyRights },
      { href: "/dashboard/heat-stress-labor-rights", label: "Stress Thermique au Travail", icon: IconHeatStressLaborRights },
      { href: "/dashboard/lithium-mining-rights", label: "Mines de Lithium", icon: IconLithiumMiningRights },
    ],
  },
  {
    title: "DROITS — WAVE 273",
    items: [
      { href: "/dashboard/nuclear-waste-rights", label: "Déchets Nucléaires", icon: IconNuclearWasteRights },
      { href: "/dashboard/migrant-domestic-worker-rights", label: "Travailleurs Domestiques Migrants", icon: IconMigrantDomesticWorkerRights },
      { href: "/dashboard/informal-economy-rights", label: "Économie Informelle", icon: IconInformalEconomyRights },
    ],
  },
  {
    title: "DROITS — WAVE 274",
    items: [
      { href: "/dashboard/platform-worker-rights", label: "Travailleurs de Plateformes", icon: IconPlatformWorkerRights },
      { href: "/dashboard/rare-earth-mining-rights", label: "Mines de Terres Rares", icon: IconRareEarthMiningRights },
      { href: "/dashboard/agricultural-child-labor-rights", label: "Travail Enfant Agricole", icon: IconAgriculturalChildLaborRights },
    ],
  },
  {
    title: "DROITS — WAVE 275",
    items: [
      { href: "/dashboard/zero-hour-contract-rights", label: "Contrats Zéro Heure", icon: IconZeroHourContractRights },
      { href: "/dashboard/nickel-mining-rights", label: "Mines de Nickel", icon: IconNickelMiningRights },
      { href: "/dashboard/coltan-mining-rights", label: "Mines de Coltan", icon: IconColtanMiningRights },
    ],
  },
  {
    title: "DROITS — WAVE 276",
    items: [
      { href: "/dashboard/whistleblower-protection-rights", label: "Lanceurs d'Alerte", icon: IconWhistleblowerProtectionRights },
      { href: "/dashboard/e-waste-rights", label: "Déchets Électroniques", icon: IconEWasteRights },
      { href: "/dashboard/sand-mining-rights", label: "Extraction de Sable", icon: IconSandMiningRights },
    ],
  },
  {
    title: "DROITS — WAVE 277",
    items: [
      { href: "/dashboard/ivory-trade-poaching-rights", label: "Commerce d'Ivoire", icon: IconIvoryTradePoachinRights },
      { href: "/dashboard/garment-factory-fire-rights", label: "Incendies Usines Textiles", icon: IconGarmentFactoryFireRights },
      { href: "/dashboard/child-bride-early-marriage-rights", label: "Mariage Précoce", icon: IconChildBrideEarlyMarriageRights },
    ],
  },
  {
    title: "DROITS — WAVE 278",
    items: [
      { href: "/dashboard/asbestos-silicosis-occupational-rights", label: "Amiante et Silicose", icon: IconAsbestosSilicosisOccupationalRights },
      { href: "/dashboard/cluster-bomb-civilian-harm-rights", label: "Bombes à Sous-Munitions", icon: IconClusterBombCivilianHarmRights },
      { href: "/dashboard/mica-child-labor-rights", label: "Travail Enfant Mines Mica", icon: IconMicaChildLaborRights },
    ],
  },
  {
    title: "DROITS — WAVE 279",
    items: [
      { href: "/dashboard/tungsten-conflict-mining-rights", label: "Tungstène Zones de Conflit", icon: IconTungstenConflictMiningRights },
      { href: "/dashboard/tin-mining-artisanal-rights", label: "Mines d'Étain Artisanales", icon: IconTinMiningArtisanalRights },
      { href: "/dashboard/tantalum-conflict-minerals-rights", label: "Tantale Minerais Conflit", icon: IconTantalumConflictMineralsRights },
    ],
  },
  {
    title: "DROITS — WAVE 280",
    items: [
      { href: "/dashboard/leather-tannery-chromium-rights", label: "Tanneries Chrome Hexavalent", icon: IconLeatherTanneryChromiumRights },
      { href: "/dashboard/brick-kiln-bonded-labor-rights", label: "Travail Servitude Briqueteries", icon: IconBrickKilnBondedLaborRights },
      { href: "/dashboard/camel-jockey-child-rights", label: "Enfants Jockeys Chameaux", icon: IconCamelJockeyChildRights },
    ],
  },
  {
    title: "DROITS — WAVE 281",
    items: [
      { href: "/dashboard/tobacco-child-labor-rights", label: "Travail Enfant Tabac", icon: IconTobaccoChildLaborRights },
      { href: "/dashboard/shrimp-fishing-forced-labor-rights", label: "Esclavage Crevettiers", icon: IconShrimpFishingForcedLaborRights },
      { href: "/dashboard/artisanal-gold-mercury-rights", label: "Orpaillage et Mercure", icon: IconArtisanalGoldMercuryRights },
    ],
  },
  {
    title: "DROITS — WAVE 282",
    items: [
      { href: "/dashboard/sugarcane-labor-rights", label: "Travailleurs Canne à Sucre", icon: IconSugarcaneLaborRights },
      { href: "/dashboard/palm-oil-peatland-rights", label: "Huile de Palme Tourbières", icon: IconPalmOilPeatlandRights },
      { href: "/dashboard/matchstick-child-labor-rights", label: "Enfants Fabriques Allumettes", icon: IconMatchstickChildLaborRights },
    ],
  },
  {
    title: "DROITS — WAVE 283",
    items: [
      { href: "/dashboard/uranium-mining-indigenous-rights", label: "Uranium Terres Autochtones", icon: IconUraniumMiningIndigenousRights },
      { href: "/dashboard/blood-diamond-conflict-mineral-rights", label: "Diamants du Sang", icon: IconBloodDiamondConflictMineralRights },
      { href: "/dashboard/illegal-fishing-forced-labor-rights", label: "Pêche Illégale Esclavage", icon: IconIllegalFishingForcedLaborRights },
    ],
  },
  {
    title: "DROITS — WAVE 284",
    items: [
      { href: "/dashboard/tiger-bone-traditional-medicine-rights", label: "Os de Tigre Médecine", icon: IconTigerBoneTraditionalMedicineRights },
      { href: "/dashboard/shark-fin-finning-rights", label: "Aileronage Requins", icon: IconSharkFinFinningRights },
      { href: "/dashboard/illegal-hardwood-logging-rights", label: "Bois Précieux Illégaux", icon: IconIllegalHardwoodLoggingRights },
    ],
  },
  {
    title: "DROITS — WAVE 285",
    items: [
      { href: "/dashboard/bear-bile-farming-rights", label: "Élevage Ours pour Bile", icon: IconBearBileFarmingRights },
      { href: "/dashboard/rhinoceros-horn-poaching-rights", label: "Braconnage Rhinocéros", icon: IconRhinocerosHornPoachinRights },
      { href: "/dashboard/cocoa-child-labor-rights", label: "Travail Enfant Cacao", icon: IconCocoaChildLaborRights },
    ],
  },
  {
    title: "DROITS — WAVE 286",
    items: [
      { href: "/dashboard/coffee-labor-rights", label: "Droits Travailleurs Café", icon: IconCoffeeLaborRights },
      { href: "/dashboard/vanilla-child-labor-rights", label: "Travail Enfant Vanille", icon: IconVanillaChildLaborRights },
      { href: "/dashboard/rubber-plantation-labor-rights", label: "Travail Plantation Caoutchouc", icon: IconRubberPlantationLaborRights },
    ],
  },
  {
    title: "DROITS — WAVE 287",
    items: [
      { href: "/dashboard/cotton-child-labor-rights", label: "Travail Enfant Coton", icon: IconCottonChildLaborRights },
      { href: "/dashboard/tea-worker-rights", label: "Droits Cueilleuses de Thé", icon: IconTeaWorkerRights },
      { href: "/dashboard/cut-flower-labor-rights", label: "Droits Travailleurs Fleurs Coupées", icon: IconCutFlowerLaborRights },
    ],
  },
  {
    title: "DROITS — WAVE 288",
    items: [
      { href: "/dashboard/soy-farming-deforestation-rights", label: "Déforestation Soja", icon: IconSoyFarmingDeforestationRights },
      { href: "/dashboard/avocado-water-theft-rights", label: "Vol d'Eau Avocats", icon: IconAvocadoWaterTheftRights },
      { href: "/dashboard/quinoa-land-grab-rights", label: "Accaparement Terres Quinoa", icon: IconQuinoaLandGrabRights },
    ],
  },
  {
    title: "DROITS — WAVE 289",
    items: [
      { href: "/dashboard/banana-pesticide-poisoning-rights", label: "Empoisonnement Pesticides Banane", icon: IconBananaPesticidePoisoningRights },
      { href: "/dashboard/grape-harvest-labor-rights", label: "Droits Vendangeurs Migrants", icon: IconGrapeHarvestLaborRights },
      { href: "/dashboard/seafood-supply-chain-rights", label: "Droits Chaîne Fruits de Mer", icon: IconSeafoodSupplyChainRights },
    ],
  },
  {
    title: "DROITS — WAVE 290",
    items: [
      { href: "/dashboard/shea-butter-labor-rights", label: "Droits Travailleurs Karité", icon: IconSheaButterLaborRights },
      { href: "/dashboard/cashew-child-labor-rights", label: "Travail Enfant Anacarde", icon: IconCashewChildLaborRights },
      { href: "/dashboard/mango-labor-rights", label: "Droits Travailleurs Mangue", icon: IconMangoLaborRights },
    ],
  },
  {
    title: "DROITS — WAVE 291",
    items: [
      { href: "/dashboard/jute-child-labor-rights", label: "Travail Enfant Moulins Jute", icon: IconJuteChildLaborRights },
      { href: "/dashboard/salt-pans-child-labor-rights", label: "Travail Enfant Marais Salants", icon: IconSaltPansChildLaborRights },
      { href: "/dashboard/phosphate-mining-indigenous-rights", label: "Droits Autochtones Phosphate", icon: IconPhosphateMiningIndigenousRights },
    ],
  },
  {
    title: "DROITS — WAVE 292",
    items: [
      { href: "/dashboard/carpet-weaving-child-labor-rights", label: "Travail Enfant Tissage Tapis", icon: IconCarpetWeavingChildLaborRights },
      { href: "/dashboard/silk-production-child-labor-rights", label: "Travail Enfant Production Soie", icon: IconSilkProductionChildLaborRights },
      { href: "/dashboard/charcoal-burning-child-labor-rights", label: "Travail Enfant Charbon de Bois", icon: IconCharcoalBurningChildLaborRights },
    ],
  },
  {
    title: "DROITS — WAVE 293",
    items: [
      { href: "/dashboard/nail-salon-worker-rights", label: "Droits Travailleurs Manucure", icon: IconNailSalonWorkerRights },
      { href: "/dashboard/restavek-child-domestic-labor-rights", label: "Enfants Domestiques Restavèk", icon: IconRestavekChildDomesticLaborRights },
      { href: "/dashboard/fishing-vessel-forced-labor-rights", label: "Travail Forcé Bateaux Pêche", icon: IconFishingVesselForcedLaborRights },
    ],
  },
  {
    title: "DROITS — WAVE 294",
    items: [
      { href: "/dashboard/surrogacy-exploitation-rights", label: "Exploitation Mères Porteuses", icon: IconSurrogacyExploitationRights },
      { href: "/dashboard/hair-harvesting-labor-rights", label: "Droits Récolte Cheveux", icon: IconHairHarvestingLaborRights },
      { href: "/dashboard/blood-plasma-donation-rights", label: "Droits Donneurs Plasma Sanguin", icon: IconBloodPlasmaDonationRights },
    ],
  },
  {
    title: "DROITS — WAVE 295",
    items: [
      { href: "/dashboard/spice-farm-child-labor-rights", label: "Droits Enfants Fermes Épices", icon: IconSpiceFarmChildLaborRights, color: "#d97706" },
      { href: "/dashboard/nutmeg-plantation-labor-rights", label: "Droits Travail Plantation Noix Muscade", icon: IconNutmegPlantationLaborRights, color: "#166534" },
      { href: "/dashboard/cardamom-child-labor-rights", label: "Droits Enfants Cardamome", icon: IconCardamomChildLaborRights, color: "#92400e" },
    ],
  },
  {
    title: "DROITS — WAVE 296",
    items: [
      { label: "Droits Communautés Extraction Eau Minérale", href: "/dashboard/mineral-water-extraction-community-rights", icon: IconMineralWaterExtractionCommunityRights, color: "#0891b2" },
      { label: "Droits Bois Santal Exploitation Illégale", href: "/dashboard/sandalwood-illegal-logging-rights", icon: IconSandalwoodIllegalLoggingRights, color: "#854d0e" },
      { label: "Droits Récupération Or Électronique", href: "/dashboard/electronic-gold-recovery-rights", icon: IconElectronicGoldRecoveryRights, color: "#ca8a04" },
    ],
  },
  {
    title: "DROITS — WAVE 297",
    items: [
      { label: "Droits Travailleurs Thon en Conserve", href: "/dashboard/canned-tuna-labor-rights", icon: IconCannedTunaLaborRights, color: "#0c4a6e" },
      { label: "Droits Crevetticulture Mangrove", href: "/dashboard/shrimp-farming-mangrove-rights", icon: IconShrimpFarmingMangroveRights, color: "#065f46" },
      { label: "Droits Travailleurs Antibiotiques Élevage", href: "/dashboard/livestock-antibiotic-worker-rights", icon: IconLivestockAntibioticWorkerRights, color: "#7f1d1d" },
    ],
  },
  {
    title: "DROITS — WAVE 298",
    items: [
      { label: "Droits Travailleurs Bambou", href: "/dashboard/bamboo-labor-rights", icon: IconBambooLaborRights, color: "#15803d" },
      { label: "Droits Plongeurs Perles", href: "/dashboard/pearl-diving-labor-rights", icon: IconPearlDivingLaborRights, color: "#0369a1" },
      { label: "Droits Aquaculteurs Algues", href: "/dashboard/seaweed-farming-labor-rights", icon: IconSeaweedFarmingLaborRights, color: "#065f46" },
    ],
  },
  {
    title: "DROITS — WAVE 299",
    items: [
      { label: "Droits Travailleurs Usines Gants Latex", href: "/dashboard/latex-glove-factory-labor-rights", icon: IconLatexGloveFactoryLaborRights, color: "#1e40af" },
      { label: "Droits Enfants Graines Coton", href: "/dashboard/cottonseed-child-labor-rights", icon: IconCottonseedChildLaborRights, color: "#d97706" },
      { label: "Droits Intoxication Nicotine Tabac", href: "/dashboard/tobacco-nicotine-poisoning-rights", icon: IconTobaccoNicotinePoisoningRights, color: "#7f1d1d" },
    ],
  },
  {
    title: "DROITS — WAVE 300",
    items: [
      { label: "Droits Artisans Bijouterie Or", href: "/dashboard/gold-jewelry-artisan-rights", icon: IconGoldJewelryArtisanRights, color: "#ca8a04" },
      { label: "Droits Carriers Silicose Pierre", href: "/dashboard/stone-quarry-silicosis-rights", icon: IconStoneQuarrySilicosisRights, color: "#78716c" },
      { label: "Droits Emballeurs Fleurs Pesticides", href: "/dashboard/flower-packing-chemical-rights", icon: IconFlowerPackingChemicalRights, color: "#be185d" },
    ],
  },
  {
    title: "DROITS — WAVE 301",
    items: [
      { label: "Droits Travailleurs Silicose Céramique", href: "/dashboard/ceramic-dust-silicosis-rights", icon: IconCeramicDustSilicosisRights, color: "#b45309" },
      { label: "Droits Travailleurs Peintures Plomb", href: "/dashboard/lead-paint-manufacturing-worker-rights", icon: IconLeadPaintManufacturingWorkerRights, color: "#475569" },
      { label: "Droits Travailleurs Laveries Charbon", href: "/dashboard/coal-washery-worker-rights", icon: IconCoalWasheryWorkerRights, color: "#1c1917" },
    ],
  },
  {
    title: "DROITS — WAVE 302",
    items: [
      { label: "Droits Enfants Fabrication Encens", href: "/dashboard/incense-stick-child-labor-rights", icon: IconIncenseStickChildLaborRights, color: "#6d28d9" },
      { label: "Droits Travailleurs Phosphore Allumettes", href: "/dashboard/match-factory-phosphorus-rights", icon: IconMatchFactoryPhosphorusRights, color: "#dc2626" },
      { label: "Droits Enfants Fabriques Feux d&apos;Artifice", href: "/dashboard/fireworks-factory-child-labor-rights", icon: IconFireworksFactoryChildLaborRights, color: "#ea580c" },
    ],
  },
  {
    title: "DROITS — WAVE 303",
    items: [
      { label: "Droits Souffleurs Verre Silicose", href: "/dashboard/glass-blowing-silicosis-rights", icon: IconGlowingBlowingSilicosisRights, color: "#0891b2" },
      { label: "Droits Travailleurs Textiles Colorants Azo", href: "/dashboard/azo-dye-textile-worker-rights", icon: IconAzoDyeTextileWorkerRights, color: "#7c3aed" },
      { label: "Droits Recycleurs Batteries Plomb", href: "/dashboard/lead-battery-recycling-rights", icon: IconLeadBatteryRecyclingRights, color: "#64748b" },
    ],
  },
  {
    title: "DROITS — WAVE 304",
    items: [
      { label: "Droits Travailleurs Saignée Caoutchouc", href: "/dashboard/rubber-tapping-forced-labor-rights", icon: IconRubberTappingForcedLaborRights, color: "#16a34a" },
      { label: "Droits Travailleurs Cultures Vanille", href: "/dashboard/vanilla-farming-labor-rights", icon: IconVanillaFarmingLaborRights, color: "#7c3aed" },
      { label: "Droits Travailleurs Sisal", href: "/dashboard/sisal-cultivation-labor-rights", icon: IconSisalCultivationLaborRights, color: "#b45309" },
    ],
  },
  {
    title: "DROITS — WAVE 305",
    items: [
      { label: "Droits Travailleurs Fibre Chanvre", href: "/dashboard/hemp-fiber-processing-labor-rights", icon: IconHempFiberProcessingLaborRights, color: "#15803d" },
      { label: "Droits Travailleurs Filatures Jute", href: "/dashboard/jute-mill-worker-rights", icon: IconJuteMillWorkerRights, color: "#a16207" },
      { label: "Droits Enfants Fibres Abaca", href: "/dashboard/abaca-fiber-child-labor-rights", icon: IconAbacaFiberChildLaborRights, color: "#0369a1" },
    ],
  },
  {
    title: "COMPTE",
    items: [
      { href: "/dashboard/settings", label: "Paramètres", icon: IconSettings },
    ],
  },
];

// ─── Inner nav content ───────────────────────────────────────────────────────

function NavContent({
  collapsed,
  onClose,
}: {
  collapsed: boolean;
  onClose?: () => void;
}) {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    router.push("/login");
  };

  return (
    <>
      {/* Logo / brand */}
      <div
        className={`border-b border-slate-800 flex items-center ${
          collapsed ? "justify-center py-5 px-2" : "justify-between py-5 px-4"
        }`}
      >
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center flex-shrink-0">
            <span className="text-white text-xs font-bold">IQ</span>
          </div>
          {!collapsed && (
            <span className="text-white font-bold text-base truncate">CompeteIQ</span>
          )}
        </div>
        {!collapsed && onClose && (
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white text-xl leading-none p-1 transition-colors"
            aria-label="Fermer le menu"
          >
            ×
          </button>
        )}
      </div>

      {/* Navigation sections */}
      <nav className="flex-1 overflow-y-auto px-2 py-3 space-y-4">
        {navSections.map((section) => (
          <div key={section.title}>
            {/* Section label — hidden when collapsed */}
            {!collapsed && (
              <p className="px-3 mb-1 text-[10px] font-semibold tracking-widest text-slate-500 uppercase select-none">
                {section.title}
              </p>
            )}
            {collapsed && (
              <div className="border-t border-slate-800 my-2 mx-2" />
            )}

            <ul className="space-y-0.5">
              {section.items.map((item) => {
                const isActive = item.exact
                  ? pathname === item.href
                  : pathname.startsWith(item.href);
                const Icon = item.icon;

                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      onClick={onClose}
                      title={collapsed ? item.label : undefined}
                      className={`flex items-center gap-3 rounded-md text-sm font-medium transition-colors relative
                        ${collapsed ? "justify-center px-2 py-2.5" : "px-3 py-2"}
                        ${
                          isActive
                            ? "bg-blue-600 text-white"
                            : "text-slate-400 hover:bg-slate-800 hover:text-white"
                        }`}
                    >
                      {/* Icon + optional badge wrapper */}
                      <span className="relative flex-shrink-0">
                        <Icon className="w-5 h-5" />
                        {item.badge !== undefined && item.badge > 0 && (
                          <span className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-red-500 text-white text-[9px] font-bold rounded-full flex items-center justify-center leading-none">
                            {item.badge > 9 ? "9+" : item.badge}
                          </span>
                        )}
                      </span>

                      {!collapsed && (
                        <>
                          <span className="flex-1 truncate">{item.label}</span>
                          {/* Badge also shows inline when expanded */}
                          {item.badge !== undefined && item.badge > 0 && (
                            <span className="ml-auto bg-red-500 text-white text-[10px] font-bold rounded-full min-w-[18px] h-[18px] flex items-center justify-center px-1">
                              {item.badge > 9 ? "9+" : item.badge}
                            </span>
                          )}
                        </>
                      )}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>

      {/* User profile */}
      <div
        className={`border-t border-slate-800 ${collapsed ? "px-2 py-3" : "px-3 py-3"}`}
      >
        <div
          className={`flex items-center gap-3 ${collapsed ? "justify-center" : ""}`}
        >
          <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
            DU
          </div>
          {!collapsed && (
            <>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-white font-medium truncate">Demo User</p>
                <p className="text-xs text-slate-400 truncate">demo@competeiq.com</p>
              </div>
              <button
                onClick={handleLogout}
                title="Déconnexion"
                className="text-slate-500 hover:text-slate-200 transition-colors p-1 rounded hover:bg-slate-800 flex-shrink-0"
                aria-label="Déconnexion"
              >
                <IconLogout className="w-4 h-4" />
              </button>
            </>
          )}
        </div>
        {/* Logout when collapsed — separate row */}
        {collapsed && (
          <button
            onClick={handleLogout}
            title="Déconnexion"
            className="mt-2 w-full flex justify-center text-slate-500 hover:text-slate-200 transition-colors p-1.5 rounded hover:bg-slate-800"
            aria-label="Déconnexion"
          >
            <IconLogout className="w-4 h-4" />
          </button>
        )}
      </div>
    </>
  );
}

// ─── Desktop sidebar shell with collapse toggle ──────────────────────────────

function DesktopSidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={`hidden md:flex flex-col flex-shrink-0 min-h-screen bg-slate-900 transition-all duration-200 ${
        collapsed ? "w-16" : "w-64"
      }`}
    >
      <div className="flex-1 flex flex-col min-h-0">
        <NavContent collapsed={collapsed} />
      </div>

      {/* Collapse toggle */}
      <button
        onClick={() => setCollapsed((c) => !c)}
        className={`flex items-center gap-2 border-t border-slate-800 text-slate-500 hover:text-white hover:bg-slate-800 transition-colors text-xs font-medium py-3 px-4 ${
          collapsed ? "justify-center px-2" : ""
        }`}
        aria-label={collapsed ? "Déplier le menu" : "Replier le menu"}
      >
        {collapsed ? (
          <IconChevronRight className="w-4 h-4" />
        ) : (
          <>
            <IconChevronLeft className="w-4 h-4" />
            <span>Réduire</span>
          </>
        )}
      </button>
    </aside>
  );
}

// ─── Mobile drawer ───────────────────────────────────────────────────────────

function MobileSidebar() {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, []);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="md:hidden fixed top-4 left-4 z-40 w-9 h-9 bg-slate-900 rounded-lg flex items-center justify-center text-white shadow-lg"
        aria-label="Ouvrir le menu"
      >
        <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5" aria-hidden="true">
          <path
            fillRule="evenodd"
            d="M3 5h14a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2zm0 4h14a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2zm0 4h14a1 1 0 0 1 0 2H3a1 1 0 0 1 0-2z"
            clipRule="evenodd"
          />
        </svg>
      </button>

      {open && (
        <>
          <div
            className="md:hidden fixed inset-0 z-40 bg-black/50"
            onClick={() => setOpen(false)}
          />
          <aside className="md:hidden fixed inset-y-0 left-0 z-50 w-72 bg-slate-900 flex flex-col shadow-2xl">
            <NavContent collapsed={false} onClose={() => setOpen(false)} />
          </aside>
        </>
      )}
    </>
  );
}

// ─── Default export ──────────────────────────────────────────────────────────

export default function Sidebar() {
  return (
    <>
      <DesktopSidebar />
      <MobileSidebar />
    </>
  );
}
