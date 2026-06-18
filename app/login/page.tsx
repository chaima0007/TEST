"use client";

import Link from "next/link";
import { useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";

// ── SVG dot-grid background pattern ──────────────────────────────────────────
function DotPattern() {
  return (
    <svg
      className="absolute inset-0 w-full h-full opacity-[0.12]"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <pattern id="dots" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
          <circle cx="2" cy="2" r="1.5" fill="white" />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#dots)" />
    </svg>
  );
}

// ── Eye icon toggle ───────────────────────────────────────────────────────────
function EyeIcon({ open }: { open: boolean }) {
  if (open) {
    return (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
        <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
    </svg>
  );
}

// ── Spinner ───────────────────────────────────────────────────────────────────
function Spinner() {
  return (
    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin flex-shrink-0" />
  );
}

// ── Login form (needs useSearchParams, wrapped in Suspense) ───────────────────
function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, rememberMe }),
      });

      if (res.ok) {
        const next = searchParams.get("next");
        const safePath =
          next && next.startsWith("/") && !next.startsWith("//")
            ? next
            : "/dashboard";
        router.push(safePath);
      } else {
        const data = (await res.json().catch(() => ({}))) as { error?: string };
        setError(data.error ?? "Identifiants invalides. Veuillez réessayer.");
        setLoading(false);
      }
    } catch {
      setError("Une erreur réseau est survenue. Veuillez réessayer.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">

      {/* ── LEFT — Brand panel (hidden on mobile) ────────────────────────── */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden flex-col justify-between p-12"
        style={{ background: "linear-gradient(135deg, #1e1b4b 0%, #312e81 45%, #4c1d95 100%)" }}
      >
        {/* Dot-grid background */}
        <DotPattern />

        {/* Radial glow */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_30%_20%,rgba(167,139,250,0.15),transparent_60%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_70%_80%,rgba(99,102,241,0.12),transparent_60%)]" />

        {/* Logo */}
        <div className="relative z-10 flex items-center gap-3">
          <div className="w-11 h-11 bg-white rounded-xl flex items-center justify-center shadow-lg flex-shrink-0">
            <span className="text-indigo-900 text-sm font-black tracking-tight">CIQ</span>
          </div>
          <span className="text-white text-xl font-bold tracking-tight">CompeteIQ</span>
        </div>

        {/* Center content */}
        <div className="relative z-10 flex-1 flex flex-col justify-center py-16">
          {/* Tagline */}
          <h2 className="text-3xl font-black text-white leading-tight mb-4 max-w-xs">
            Intelligence concurrentielle de niveau enterprise
          </h2>
          <p className="text-indigo-300 text-sm font-light mb-10 max-w-xs leading-relaxed">
            La plateforme de veille stratégique des équipes commerciales qui gagnent.
          </p>

          {/* Feature highlights */}
          <ul className="space-y-4 mb-12">
            {[
              "Surveillance en temps réel de vos concurrents",
              "Agents IA spécialisés opérationnels 24/7",
              "Plans d'action générés en 30 secondes",
            ].map((feat) => (
              <li key={feat} className="flex items-start gap-3">
                <span className="w-5 h-5 rounded-full bg-indigo-500/30 border border-indigo-400/50 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg viewBox="0 0 12 12" fill="none" className="w-3 h-3">
                    <path d="M2 6l2.5 2.5L10 3.5" stroke="#a5b4fc" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </span>
                <span className="text-indigo-100 text-sm font-medium leading-snug">{feat}</span>
              </li>
            ))}
          </ul>

          {/* Social proof */}
          <div className="border-t border-white/10 pt-8">
            <div className="flex items-center gap-3 mb-2">
              {/* Avatar stack */}
              <div className="flex -space-x-2">
                {["#6366f1", "#8b5cf6", "#a78bfa", "#7c3aed"].map((color, i) => (
                  <div
                    key={i}
                    className="w-7 h-7 rounded-full border-2 border-indigo-900 flex items-center justify-center text-white text-[10px] font-bold"
                    style={{ backgroundColor: color }}
                  >
                    {["A", "B", "C", "+"][i]}
                  </div>
                ))}
              </div>
              <p className="text-indigo-200 text-xs font-medium">
                Utilisé par <span className="text-white font-bold">240+</span> équipes commerciales en Europe
              </p>
            </div>
            <div className="flex items-center gap-1 mt-3">
              {[...Array(5)].map((_, i) => (
                <svg key={i} viewBox="0 0 16 16" fill="#fbbf24" className="w-3.5 h-3.5">
                  <path d="M8 1.25l1.686 3.416 3.764.547-2.725 2.655.643 3.748L8 9.772l-3.368 1.844.643-3.748L2.55 5.213l3.764-.547L8 1.25Z" />
                </svg>
              ))}
              <span className="text-indigo-300 text-xs ml-1">4,9/5 satisfaction client</span>
            </div>
          </div>
        </div>

        {/* Bottom branding */}
        <div className="relative z-10">
          <p className="text-indigo-400/60 text-xs">
            © 2026 CompeteIQ · Caelum Partners
          </p>
        </div>
      </div>

      {/* ── RIGHT — Login form ────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 py-12 bg-white">
        {/* Mobile logo */}
        <div className="lg:hidden flex items-center gap-2.5 mb-8">
          <div className="w-9 h-9 bg-indigo-600 rounded-xl flex items-center justify-center">
            <span className="text-white text-xs font-black">CIQ</span>
          </div>
          <span className="text-slate-900 text-lg font-bold">CompeteIQ</span>
        </div>

        <div className="w-full max-w-sm">
          {/* Heading */}
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-slate-900 mb-1">Bon retour 👋</h1>
            <p className="text-slate-500 text-sm">
              Connectez-vous à votre espace CompeteIQ
            </p>
          </div>

          {/* Error banner */}
          {error && (
            <div className="mb-5 flex items-start gap-2.5 p-3.5 bg-red-50 border border-red-200 rounded-xl">
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-red-500 flex-shrink-0 mt-0.5">
                <path fillRule="evenodd" d="M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0Zm-8-5a.75.75 0 0 1 .75.75v4.5a.75.75 0 0 1-1.5 0v-4.5A.75.75 0 0 1 10 5Zm0 10a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z" clipRule="evenodd" />
              </svg>
              <p className="text-sm text-red-700 font-medium">{error}</p>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1.5 uppercase tracking-wide">
                Adresse email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="vous@entreprise.com"
                className={`w-full border rounded-xl px-3.5 py-2.5 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition ${
                  error ? "border-red-300 bg-red-50/30" : "border-slate-200 bg-white"
                }`}
                required
                autoComplete="email"
                autoFocus
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1.5 uppercase tracking-wide">
                Mot de passe
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className={`w-full border rounded-xl px-3.5 py-2.5 pr-10 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition ${
                    error ? "border-red-300 bg-red-50/30" : "border-slate-200 bg-white"
                  }`}
                  required
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((p) => !p)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                  tabIndex={-1}
                  aria-label={showPassword ? "Masquer le mot de passe" : "Afficher le mot de passe"}
                >
                  <EyeIcon open={showPassword} />
                </button>
              </div>
            </div>

            {/* Remember me + forgot password */}
            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="w-3.5 h-3.5 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
                />
                <span className="text-xs text-slate-600">Se souvenir de moi</span>
              </label>
              <a
                href="#"
                className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 transition-colors"
              >
                Mot de passe oublié ?
              </a>
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 py-3 rounded-xl text-sm font-bold text-white transition-all disabled:opacity-70 disabled:cursor-not-allowed hover:-translate-y-0.5 active:translate-y-0"
              style={{
                background: loading
                  ? "#6366f1"
                  : "linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #7c3aed 100%)",
                boxShadow: loading ? "none" : "0 4px 16px rgba(99,102,241,0.35)",
              }}
            >
              {loading && <Spinner />}
              {loading ? "Connexion en cours…" : "Se connecter"}
            </button>
          </form>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-100" />
            </div>
            <div className="relative flex justify-center">
              <span className="px-3 bg-white text-xs text-slate-400 font-medium">ou</span>
            </div>
          </div>

          {/* Demo CTA */}
          <a
            href="mailto:demo@competeiq.com"
            className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-semibold text-indigo-700 border-2 border-indigo-200 hover:border-indigo-400 hover:bg-indigo-50 transition-all"
          >
            <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 flex-shrink-0">
              <path d="M3 4a2 2 0 0 0-2 2v1.161l8.441 4.221a1.25 1.25 0 0 0 1.118 0L19 7.162V6a2 2 0 0 0-2-2H3Z" />
              <path d="m19 8.839-7.77 3.885a2.75 2.75 0 0 1-2.46 0L1 8.839V14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8.839Z" />
            </svg>
            Demander une démo
          </a>

          {/* Demo hint */}
          <div className="mt-5 p-3.5 bg-indigo-50 border border-indigo-100 rounded-xl">
            <p className="text-xs font-semibold text-indigo-800 mb-0.5">Compte démo disponible</p>
            <p className="text-xs text-indigo-600 mb-2">Explorez la plateforme sans engagement.</p>
            <button
              type="button"
              onClick={async () => {
                const res = await fetch("/api/auth/demo-credentials");
                if (res.ok) {
                  const { email, password } = (await res.json()) as {
                    email: string;
                    password: string;
                  };
                  setEmail(email);
                  setPassword(password);
                }
              }}
              className="text-xs text-indigo-700 font-bold hover:underline"
            >
              Remplir automatiquement →
            </button>
          </div>

          {/* Footer */}
          <p className="text-center text-[11px] text-slate-400 mt-6 leading-relaxed">
            © 2026 CompeteIQ · Caelum Partners ·{" "}
            <Link href="#" className="hover:text-slate-600 transition-colors">
              Politique de confidentialité
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

// ── Page export ───────────────────────────────────────────────────────────────
export default function LoginPage() {
  return (
    <Suspense>
      <LoginForm />
    </Suspense>
  );
}
