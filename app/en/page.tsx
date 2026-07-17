"use client";

import Link from "next/link";
import { useState, useEffect } from "react";

// English homepage — Caelum (B2B). Mirrors the French home (/) for the many English
// speakers among Brussels/EU businesses. The rest of the site can be auto-translated
// via the 🌐 bar; this page is a native English entry point.

const navLinks = [
  { label: "Services", href: "#services" },
  { label: "2026 Compliance", href: "/conformite-2026" },
  { label: "Pricing", href: "/tarifs" },
  { label: "Why us", href: "#unique" },
  { label: "Contact", href: "/contact" },
];

const services = [
  {
    title: "Custom websites",
    desc: "Modern, fast, polished sites that inspire trust from the first second. Built for your customers, not just to look pretty.",
    points: ["Modern & responsive design", "Mobile-first and fast", "Delivered in days"],
    accent: "from-indigo-500/15 to-indigo-600/5",
    ring: "text-indigo-300",
  },
  {
    title: "Dashboards",
    desc: "See your business at a glance: sales, customers, performance. Your data, finally clear and usable.",
    points: ["Tailored to your needs", "Real-time data", "Easy to use daily"],
    accent: "from-emerald-500/15 to-emerald-600/5",
    ring: "text-emerald-400",
  },
  {
    title: "Regulatory compliance",
    desc: "E-invoicing, GDPR, NIS2, CSRD and more. We find what actually applies to you — and we look for the public subsidy that funds it.",
    points: ["Free 1-minute self-check", "Sourced from official law", "Funding angle included"],
    accent: "from-amber-500/15 to-amber-600/5",
    ring: "text-amber-400",
  },
];

const unique = [
  {
    title: "Compliance + funding, in one place",
    desc: "Where most stop at telling you what's wrong, we link each obligation to the real regional subsidies that can fund the fix (Wallonia, Flanders). The net cost often drops sharply.",
  },
  {
    title: "Everything is sourced and traceable",
    desc: "Every answer points to an official legal text or public dataset you can verify — never an opinion. You always know where the information comes from.",
  },
  {
    title: "A free self-diagnosis that actually helps",
    desc: "In one minute, our simulator tells you which 2026 rules apply, gives you a live \"am I compliant?\" score, and generates a timestamped self-assessment record — no strings attached.",
  },
  {
    title: "Belgium-native, multilingual",
    desc: "Built around Belgian and EU law, region by region (Wallonia, Brussels, Flanders), and available in French, Dutch and English — with on-the-fly translation for the rest of Europe.",
  },
  {
    title: "AI speed, human reliability",
    desc: "We use automation to move fast, but every deliverable is checked by a human before it reaches you. Speed without the guesswork.",
  },
  {
    title: "Radical honesty",
    desc: "We tell you what truly concerns you — no useless work, no empty promises. If a subsidy needs a labelled provider we don't yet qualify for, we say so.",
  },
];

const steps = [
  { n: "1", title: "We listen", desc: "We understand your real need — no jargon. A simple 20-minute talk." },
  { n: "2", title: "We design", desc: "A clear solution and a transparent quote. You approve before we start." },
  { n: "3", title: "We deliver fast", desc: "A working result in days, and we stay available afterwards." },
];

export default function HomeEN() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <div className="min-h-screen bg-white text-slate-900 overflow-x-hidden">
      {/* Navigation */}
      <nav className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${scrolled ? "bg-white/95 backdrop-blur-md shadow-sm border-b border-slate-100" : "bg-transparent"}`}>
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center shadow-sm">
              <span className="text-white text-xs font-black tracking-tight">C</span>
            </div>
            <span className={`text-lg font-bold transition-colors ${scrolled ? "text-slate-900" : "text-white"}`}>Caelum</span>
          </div>

          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((l) => (
              <a key={l.label} href={l.href}
                className={`px-4 py-2 text-sm rounded-lg transition-colors font-medium ${scrolled ? "text-slate-600 hover:text-slate-900 hover:bg-slate-100" : "text-slate-200 hover:text-white hover:bg-white/10"}`}>
                {l.label}
              </a>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <Link href="/" className={`text-sm font-semibold px-3 py-2 rounded-lg border transition-colors ${scrolled ? "border-slate-300 text-slate-700 hover:bg-slate-100" : "border-white/30 text-white hover:bg-white/10"}`}>
              FR
            </Link>
            <Link href="/contact"
              className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors shadow-sm">
              Get a quote
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden pt-16 text-center px-6">
        <div className="absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_60%_0%,rgba(37,99,235,0.25),transparent_65%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_15%_85%,rgba(124,58,237,0.18),transparent_60%)]" />

        <div className="relative z-10 max-w-4xl">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-8">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            Web &amp; data studio — Brussels
          </span>

          <h1 className="text-4xl sm:text-6xl font-bold tracking-tight text-white leading-[1.1]">
            Digital tools
            <span className="block bg-gradient-to-r from-indigo-300 to-sky-300 bg-clip-text text-transparent">
              that move your business forward
            </span>
          </h1>

          <p className="text-lg sm:text-xl text-slate-300 mt-6 max-w-2xl mx-auto leading-relaxed">
            Custom websites, dashboards and regulatory compliance.
            <span className="block mt-2 text-white font-medium">Agency quality, at a Brussels freelancer&apos;s price.</span>
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-10">
            <Link href="/contact"
              className="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-indigo-600/20">
              Start a project
            </Link>
            <a href="#unique"
              className="w-full sm:w-auto bg-white/10 hover:bg-white/15 border border-white/15 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors">
              Why we&apos;re different
            </a>
          </div>

          <p className="text-slate-400 text-sm mt-6">Reply within 24h · First talk, no commitment</p>
        </div>
      </section>

      {/* Services */}
      <section id="services" className="py-24 px-6 max-w-7xl mx-auto">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <span className="text-indigo-600 font-semibold text-sm uppercase tracking-wide">Our services</span>
          <h2 className="text-3xl sm:text-4xl font-bold mt-3">What we build for you</h2>
          <p className="text-slate-500 mt-4">Distinct skills, one standard: concrete work that genuinely serves you.</p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((s) => (
            <div key={s.title} className={`rounded-2xl border border-slate-200 p-7 bg-gradient-to-b ${s.accent} hover:shadow-lg hover:-translate-y-1 transition-all`}>
              <h3 className="text-xl font-bold">{s.title}</h3>
              <p className="text-slate-600 mt-3 text-sm leading-relaxed">{s.desc}</p>
              <ul className="mt-5 space-y-2">
                {s.points.map((p) => (
                  <li key={p} className="flex items-center gap-2 text-sm text-slate-700">
                    <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-emerald-500 flex-shrink-0">
                      <path fillRule="evenodd" d="M16.7 5.3a1 1 0 010 1.4l-7.5 7.5a1 1 0 01-1.4 0L3.3 9.7a1 1 0 011.4-1.4L8.5 12l6.8-6.8a1 1 0 011.4 0z" clipRule="evenodd" />
                    </svg>
                    {p}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* What makes us unique */}
      <section id="unique" className="py-24 px-6 bg-slate-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <span className="text-indigo-600 font-semibold text-sm uppercase tracking-wide">Why Caelum</span>
            <h2 className="text-3xl sm:text-4xl font-bold mt-3">What makes us different on the market</h2>
            <p className="text-slate-500 mt-4">Not slogans — things we actually built and can prove.</p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {unique.map((u, i) => (
              <div key={u.title} className="rounded-2xl border border-slate-200 bg-white p-7 hover:shadow-lg transition-shadow">
                <div className="w-10 h-10 rounded-xl bg-indigo-600 text-white font-bold flex items-center justify-center mb-4">{i + 1}</div>
                <h3 className="text-lg font-bold tracking-tight">{u.title}</h3>
                <p className="text-slate-600 mt-2 text-sm leading-relaxed">{u.desc}</p>
              </div>
            ))}
          </div>
          <div className="mt-10 text-center">
            <Link href="/conformite-2026" className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-indigo-600/20">
              Run the free 1-minute check
            </Link>
          </div>
        </div>
      </section>

      {/* Method */}
      <section className="py-24 px-6 max-w-7xl mx-auto">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <span className="text-indigo-600 font-semibold text-sm uppercase tracking-wide">Our method</span>
          <h2 className="text-3xl sm:text-4xl font-bold mt-3">Simple, fast, no surprises</h2>
          <p className="text-slate-500 mt-4">From your idea to a result online, in three clear steps.</p>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          {steps.map((st) => (
            <div key={st.n} className="relative bg-white rounded-2xl border border-slate-200 p-7">
              <div className="w-11 h-11 rounded-full bg-indigo-600 text-white font-bold flex items-center justify-center text-lg mb-4">{st.n}</div>
              <h3 className="text-lg font-bold">{st.title}</h3>
              <p className="text-slate-600 mt-2 text-sm leading-relaxed">{st.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-24 px-6">
        <div className="max-w-4xl mx-auto rounded-3xl bg-gradient-to-br from-slate-900 to-slate-950 px-8 py-16 text-center relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(37,99,235,0.25),transparent_60%)]" />
          <div className="relative z-10">
            <h2 className="text-3xl sm:text-4xl font-bold text-white">An idea? A need?</h2>
            <p className="text-slate-300 mt-4 max-w-xl mx-auto">
              Let&apos;s talk for 20 minutes, no commitment. We&apos;ll honestly tell you what we can
              do for you — and what it costs.
            </p>
            <Link href="/contact"
              className="inline-block mt-8 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-indigo-600/30">
              Get a free quote
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-100 py-10 px-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-slate-500">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-md flex items-center justify-center">
              <span className="text-white text-[10px] font-black">C</span>
            </div>
            <span className="font-semibold text-slate-700">Caelum</span>
            <span className="text-slate-400">· Web &amp; data studio · Brussels</span>
          </div>
          <div className="flex items-center gap-4 flex-wrap">
            <Link href="/" className="hover:text-slate-900">Français</Link>
            <a href="#services" className="hover:text-slate-900">Services</a>
            <Link href="/conformite-2026" className="hover:text-slate-900">Compliance</Link>
            <Link href="/contact" className="hover:text-slate-900">Contact</Link>
            <Link href="/mentions-legales" className="hover:text-slate-900">Legal</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
