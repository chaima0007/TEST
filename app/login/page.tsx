"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("demo@competeiq.com");
  const [password, setPassword] = useState("demo123");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Demo: accept demo credentials directly
    await new Promise((r) => setTimeout(r, 600));
    if (email === "demo@competeiq.com" && password === "demo123") {
      router.push("/dashboard");
    } else {
      setError("Email ou mot de passe incorrect. Essayez demo@competeiq.com / demo123");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-6">
            <div className="w-9 h-9 bg-indigo-600 rounded-xl flex items-center justify-center">
              <span className="text-white text-sm font-bold">IQ</span>
            </div>
            <span className="text-xl font-bold text-slate-900">CompeteIQ</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900">Connexion</h1>
          <p className="text-slate-500 text-sm mt-1">Accédez à votre tableau de bord</p>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-100 rounded-lg text-xs text-red-600">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Mot de passe</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 text-white py-2.5 rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors disabled:opacity-60 flex items-center justify-center gap-2"
            >
              {loading && <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>}
              {loading ? "Connexion..." : "Se connecter"}
            </button>
          </form>

          <div className="mt-4 p-3 bg-indigo-50 rounded-lg">
            <p className="text-xs text-indigo-700 font-medium">Compte démo :</p>
            <p className="text-xs text-indigo-600">Email : demo@competeiq.com</p>
            <p className="text-xs text-indigo-600">Mot de passe : demo123</p>
          </div>
        </div>

        <p className="text-center text-xs text-slate-400 mt-4">
          Pas encore de compte ?{" "}
          <Link href="/" className="text-indigo-600 hover:underline">
            Commencer gratuitement
          </Link>
        </p>
      </div>
    </div>
  );
}
