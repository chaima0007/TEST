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
      { href: "/dashboard/agents", label: "60 Agents Dir.", icon: IconAgents },
      { href: "/dashboard/branding", label: "LinkedIn & CV", icon: IconBranding },
      { href: "/dashboard/portfolio", label: "Portfolio", icon: IconPortfolio },
      { href: "/dashboard/editorial", label: "Calendrier Éditorial", icon: IconEditorial },
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
