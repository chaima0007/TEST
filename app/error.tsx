"use client"

import { useEffect } from "react"
import Link from "next/link"

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error)
  }, [error])

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-4 relative overflow-hidden">
      {/* Subtle dot texture */}
      <div
        className="absolute inset-0 opacity-30"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='2' cy='2' r='1.5' fill='%23f59e0b' fill-opacity='0.2'/%3E%3C/svg%3E")`,
          backgroundSize: "20px 20px",
        }}
      />

      <div className="relative z-10 text-center max-w-md">
        {/* Warning triangle icon */}
        <div className="flex justify-center mb-6">
          <div className="w-20 h-20 rounded-2xl bg-amber-50 border border-amber-100 flex items-center justify-center shadow-sm">
            <svg
              width="40"
              height="40"
              viewBox="0 0 40 40"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path
                d="M20 4L37 34H3L20 4Z"
                fill="#FEF3C7"
                stroke="#F59E0B"
                strokeWidth="2.5"
                strokeLinejoin="round"
              />
              <line
                x1="20"
                y1="15"
                x2="20"
                y2="24"
                stroke="#D97706"
                strokeWidth="2.5"
                strokeLinecap="round"
              />
              <circle cx="20" cy="29" r="1.5" fill="#D97706" />
            </svg>
          </div>
        </div>

        {/* Error title */}
        <h1 className="text-2xl font-bold text-slate-900 mb-2">
          Une erreur est survenue
        </h1>
        <p className="text-slate-500 text-sm leading-relaxed mb-8">
          Quelque chose s&apos;est mal passé. Notre équipe a été notifiée.
        </p>

        {/* Digest code (discrete) */}
        {error.digest && (
          <p className="text-xs text-slate-300 font-mono mb-6">
            Réf : {error.digest}
          </p>
        )}

        {/* Action buttons */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <button
            onClick={reset}
            className="bg-amber-500 text-white px-6 py-2.5 rounded-xl text-sm font-semibold shadow-md shadow-amber-100 hover:bg-amber-600 hover:shadow-amber-200 transition-all"
          >
            Réessayer
          </button>
          <Link
            href="/dashboard"
            className="border border-slate-200 text-slate-700 bg-white px-6 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50 transition-all shadow-sm"
          >
            Retour au tableau de bord
          </Link>
        </div>
      </div>
    </div>
  )
}
