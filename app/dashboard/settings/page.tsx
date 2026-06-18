"use client";

import { useState } from "react";

// ── Icons ────────────────────────────────────────────────────────────────────

function IconUser() {
  return (
    <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
      <circle cx="8" cy="5" r="3" stroke="currentColor" strokeWidth="1.4" />
      <path d="M2 14c0-3.314 2.686-5 6-5s6 1.686 6 5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
    </svg>
  );
}

function IconTeam() {
  return (
    <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
      <circle cx="6" cy="5" r="2.5" stroke="currentColor" strokeWidth="1.4" />
      <circle cx="11" cy="5" r="2" stroke="currentColor" strokeWidth="1.4" />
      <path d="M1 14c0-2.761 2.239-4 5-4s5 1.239 5 4" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
      <path d="M13 10c1.5.4 2.5 1.4 2.5 3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
    </svg>
  );
}

function IconSecurity() {
  return (
    <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
      <path d="M8 2L3 4.5v4C3 11.5 5.2 13.8 8 14.5c2.8-.7 5-3 5-6v-4L8 2z" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
      <path d="M5.5 8l2 2 3-3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function IconIntegrations() {
  return (
    <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
      <rect x="2" y="2" width="5" height="5" rx="1" stroke="currentColor" strokeWidth="1.4" />
      <rect x="9" y="2" width="5" height="5" rx="1" stroke="currentColor" strokeWidth="1.4" />
      <rect x="2" y="9" width="5" height="5" rx="1" stroke="currentColor" strokeWidth="1.4" />
      <rect x="9" y="9" width="5" height="5" rx="1" stroke="currentColor" strokeWidth="1.4" />
    </svg>
  );
}

function IconBilling() {
  return (
    <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
      <rect x="1" y="4" width="14" height="9" rx="1.5" stroke="currentColor" strokeWidth="1.4" />
      <path d="M1 7h14" stroke="currentColor" strokeWidth="1.4" />
      <path d="M4 10.5h3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
    </svg>
  );
}

function IconEye({ off }: { off?: boolean }) {
  return off ? (
    <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
      <path d="M2 2l12 12" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
      <path d="M6.7 6.7A2 2 0 0 0 9.3 9.3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
      <path d="M4.2 4.2C2.9 5.1 2 6.4 2 8c0 0 2 4 6 4a7 7 0 0 0 3.8-1.2" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
      <path d="M12.5 10.5C13.5 9.5 14 8.5 14 8c0 0-2-4-6-4a6.5 6.5 0 0 0-2.5.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
    </svg>
  ) : (
    <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none">
      <path d="M2 8s2-4 6-4 6 4 6 4-2 4-6 4-6-4-6-4z" stroke="currentColor" strokeWidth="1.4" />
      <circle cx="8" cy="8" r="2" stroke="currentColor" strokeWidth="1.4" />
    </svg>
  );
}

function IconSlack() {
  return (
    <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none">
      <path d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52z" fill="#E01E5A" />
      <path d="M6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313z" fill="#E01E5A" />
      <path d="M8.834 5.042a2.528 2.528 0 0 1-2.521-2.52A2.528 2.528 0 0 1 8.834 0a2.528 2.528 0 0 1 2.521 2.522v2.52H8.834z" fill="#36C5F0" />
      <path d="M8.834 6.313a2.528 2.528 0 0 1 2.521 2.521 2.528 2.528 0 0 1-2.521 2.521H2.522A2.528 2.528 0 0 1 0 8.834a2.528 2.528 0 0 1 2.522-2.521h6.312z" fill="#36C5F0" />
      <path d="M18.956 8.834a2.528 2.528 0 0 1 2.522-2.521A2.528 2.528 0 0 1 24 8.834a2.528 2.528 0 0 1-2.522 2.521h-2.522V8.834z" fill="#2EB67D" />
      <path d="M17.688 8.834a2.528 2.528 0 0 1-2.523 2.521 2.527 2.527 0 0 1-2.52-2.521V2.522A2.527 2.527 0 0 1 15.165 0a2.528 2.528 0 0 1 2.523 2.522v6.312z" fill="#2EB67D" />
      <path d="M15.165 18.956a2.528 2.528 0 0 1 2.523 2.522A2.528 2.528 0 0 1 15.165 24a2.527 2.527 0 0 1-2.52-2.522v-2.522h2.52z" fill="#ECB22E" />
      <path d="M15.165 17.688a2.527 2.527 0 0 1-2.52-2.523 2.526 2.526 0 0 1 2.52-2.52h6.313A2.527 2.527 0 0 1 24 15.165a2.528 2.528 0 0 1-2.522 2.523h-6.313z" fill="#ECB22E" />
    </svg>
  );
}

function IconGmail() {
  return (
    <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none">
      <path d="M2 6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6z" stroke="#EA4335" strokeWidth="1.5" />
      <path d="M2 6l10 7 10-7" stroke="#EA4335" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

function IconWebhook() {
  return (
    <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none">
      <path d="M5 5l-3 3 3 3M19 5l3 3-3 3M15 3l-6 18" stroke="#6366F1" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function IconZapier() {
  return (
    <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none">
      <path d="M12 2L14.5 9.5H22L16 14L18.5 21.5L12 17L5.5 21.5L8 14L2 9.5H9.5L12 2Z" fill="#FF4F00" />
    </svg>
  );
}

// ── Toggle ────────────────────────────────────────────────────────────────────

function Toggle({ value, onChange }: { value: boolean; onChange: () => void }) {
  return (
    <button
      role="switch"
      aria-checked={value}
      onClick={onChange}
      className={`relative w-11 h-6 rounded-full transition-colors flex-shrink-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 ${value ? "bg-indigo-600" : "bg-slate-200"}`}
    >
      <span
        className="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform"
        style={{ transform: value ? "translateX(20px)" : "translateX(0)" }}
      />
    </button>
  );
}

// ── Tab types ─────────────────────────────────────────────────────────────────

type TabKey = "profil" | "equipe" | "securite" | "integrations" | "facturation";

const TABS: { key: TabKey; label: string; icon: React.ReactNode }[] = [
  { key: "profil", label: "Profil", icon: <IconUser /> },
  { key: "equipe", label: "Équipe", icon: <IconTeam /> },
  { key: "securite", label: "Sécurité", icon: <IconSecurity /> },
  { key: "integrations", label: "Intégrations", icon: <IconIntegrations /> },
  { key: "facturation", label: "Facturation", icon: <IconBilling /> },
];

// ── Tab 1: Profil ─────────────────────────────────────────────────────────────

function TabProfil() {
  const [form, setForm] = useState({
    firstName: "Chaima",
    lastName: "Mhadbi",
    email: "retrouvetonsmile@gmail.com",
    company: "Caelum Partners",
    timezone: "Europe/Brussels",
    language: "fr",
  });
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="space-y-6">
      {saved && (
        <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 rounded-lg px-4 py-3 text-sm font-medium">
          <span className="text-base">✓</span> Profil mis à jour
        </div>
      )}

      <div className="bg-white rounded-xl border border-slate-200">
        <div className="px-6 py-4 border-b border-slate-100">
          <h3 className="font-semibold text-slate-900">Informations personnelles</h3>
          <p className="text-xs text-slate-400 mt-0.5">Vos informations de compte CompeteIQ</p>
        </div>
        <div className="p-6 space-y-6">
          {/* Avatar */}
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-white text-xl font-bold select-none shadow-sm flex-shrink-0">
              CM
            </div>
            <div>
              <p className="font-semibold text-slate-900">Chaima Mhadbi</p>
              <button className="mt-1 text-xs text-indigo-600 hover:text-indigo-800 font-medium transition-colors border border-indigo-200 rounded-md px-2.5 py-1 hover:bg-indigo-50">
                Changer la photo
              </button>
            </div>
          </div>

          {/* Name fields */}
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1.5">Prénom</label>
              <input
                type="text"
                value={form.firstName}
                onChange={(e) => setForm((p) => ({ ...p, firstName: e.target.value }))}
                className="w-full border border-slate-200 rounded-lg px-3.5 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent hover:border-slate-300 transition-all"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1.5">Nom</label>
              <input
                type="text"
                value={form.lastName}
                onChange={(e) => setForm((p) => ({ ...p, lastName: e.target.value }))}
                className="w-full border border-slate-200 rounded-lg px-3.5 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent hover:border-slate-300 transition-all"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1.5">Email</label>
              <input
                type="email"
                value={form.email}
                onChange={(e) => setForm((p) => ({ ...p, email: e.target.value }))}
                className="w-full border border-slate-200 rounded-lg px-3.5 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent hover:border-slate-300 transition-all"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1.5">Entreprise</label>
              <input
                type="text"
                value={form.company}
                onChange={(e) => setForm((p) => ({ ...p, company: e.target.value }))}
                className="w-full border border-slate-200 rounded-lg px-3.5 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent hover:border-slate-300 transition-all"
              />
            </div>
          </div>

          {/* Timezone & Language */}
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1.5">Fuseau horaire</label>
              <select
                value={form.timezone}
                onChange={(e) => setForm((p) => ({ ...p, timezone: e.target.value }))}
                className="w-full border border-slate-200 rounded-lg px-3.5 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent hover:border-slate-300 transition-all bg-white"
              >
                <option value="Europe/Brussels">(GMT+1) Europe/Bruxelles</option>
                <option value="Europe/Paris">(GMT+1) Europe/Paris</option>
                <option value="Europe/London">(GMT+0) Europe/Londres</option>
                <option value="America/New_York">(GMT-5) America/New_York</option>
                <option value="Asia/Tokyo">(GMT+9) Asia/Tokyo</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1.5">Langue</label>
              <select
                value={form.language}
                onChange={(e) => setForm((p) => ({ ...p, language: e.target.value }))}
                className="w-full border border-slate-200 rounded-lg px-3.5 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent hover:border-slate-300 transition-all bg-white"
              >
                <option value="fr">Français</option>
                <option value="en">English</option>
                <option value="de">Deutsch</option>
                <option value="es">Español</option>
              </select>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-100">
            <button
              onClick={handleSave}
              className="bg-indigo-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors shadow-sm"
            >
              Enregistrer les modifications
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Tab 2: Équipe ─────────────────────────────────────────────────────────────

const ROLE_STYLES: Record<string, string> = {
  Administrateur: "bg-indigo-100 text-indigo-700",
  Analyste: "bg-violet-100 text-violet-700",
  Lecteur: "bg-slate-100 text-slate-600",
};

const MEMBERS = [
  {
    initials: "CM",
    name: "Chaima Mhadbi",
    email: "retrouvetonsmile@gmail.com",
    role: "Administrateur",
    status: "Actif",
    isOwner: true,
  },
  {
    initials: "AL",
    name: "Alexandre Laurent",
    email: "a.laurent@caelumpartners.agency",
    role: "Analyste",
    status: "Actif",
    isOwner: false,
  },
  {
    initials: "SF",
    name: "Sophie Fontaine",
    email: "s.fontaine@caelumpartners.agency",
    role: "Lecteur",
    status: "Invité",
    isOwner: false,
  },
];

function TabEquipe() {
  const [showInviteForm, setShowInviteForm] = useState(false);
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState("Lecteur");

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-slate-200">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-slate-900">Membres de l&apos;équipe</h3>
            <p className="text-xs text-slate-400 mt-0.5">Gérez les accès à votre espace CompeteIQ</p>
          </div>
          <button
            onClick={() => setShowInviteForm((v) => !v)}
            className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors shadow-sm"
          >
            <span className="text-lg leading-none">+</span> Inviter un membre
          </button>
        </div>

        {/* Invite form */}
        {showInviteForm && (
          <div className="px-6 py-4 bg-indigo-50/50 border-b border-indigo-100">
            <p className="text-sm font-semibold text-slate-700 mb-3">Nouvelle invitation</p>
            <div className="flex gap-3 flex-wrap">
              <input
                type="email"
                placeholder="email@entreprise.com"
                value={inviteEmail}
                onChange={(e) => setInviteEmail(e.target.value)}
                className="flex-1 min-w-48 border border-slate-200 rounded-lg px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
              />
              <select
                value={inviteRole}
                onChange={(e) => setInviteRole(e.target.value)}
                className="border border-slate-200 rounded-lg px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
              >
                <option>Administrateur</option>
                <option>Analyste</option>
                <option>Lecteur</option>
              </select>
              <button
                onClick={() => { setShowInviteForm(false); setInviteEmail(""); }}
                className="bg-indigo-600 text-white px-4 py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors"
              >
                Envoyer l&apos;invitation
              </button>
            </div>
          </div>
        )}

        {/* Members table */}
        <div className="divide-y divide-slate-50">
          {MEMBERS.map((m) => (
            <div key={m.email} className="flex items-center gap-4 px-6 py-4 hover:bg-slate-50/50 transition-colors">
              <div className="w-9 h-9 rounded-full bg-gradient-to-br from-indigo-400 to-violet-500 flex items-center justify-center text-white text-xs font-bold flex-shrink-0 select-none">
                {m.initials}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-slate-900 truncate">{m.name}</p>
                <p className="text-xs text-slate-400 truncate">{m.email}</p>
              </div>
              <span className={`hidden sm:inline-flex text-xs font-semibold px-2.5 py-1 rounded-full ${ROLE_STYLES[m.role]}`}>
                {m.role}
              </span>
              <div className="flex items-center gap-1.5 text-xs font-medium">
                {m.status === "Actif" ? (
                  <span className="flex items-center gap-1.5 text-emerald-600">
                    <span className="w-2 h-2 bg-emerald-500 rounded-full" /> Actif
                  </span>
                ) : (
                  <span className="flex items-center gap-1.5 text-amber-600">
                    <span className="w-2 h-2 bg-amber-400 rounded-full border border-amber-300" /> Invité
                  </span>
                )}
              </div>
              <div className="flex items-center gap-2 flex-shrink-0">
                {m.isOwner ? (
                  <span className="text-xs text-slate-300">—</span>
                ) : m.status === "Invité" ? (
                  <>
                    <button className="text-xs text-indigo-600 hover:text-indigo-800 font-medium px-2.5 py-1.5 border border-indigo-200 rounded-md hover:bg-indigo-50 transition-colors">
                      Renvoyer
                    </button>
                    <button className="text-xs text-red-500 hover:text-red-700 font-medium px-2.5 py-1.5 border border-red-200 rounded-md hover:bg-red-50 transition-colors">
                      Supprimer
                    </button>
                  </>
                ) : (
                  <button className="text-xs text-red-500 hover:text-red-700 font-medium px-2.5 py-1.5 border border-red-200 rounded-md hover:bg-red-50 transition-colors">
                    Supprimer
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── Tab 3: Sécurité ────────────────────────────────────────────────────────────

function TabSecurite() {
  const [twoFA, setTwoFA] = useState(false);
  const [showKey, setShowKey] = useState(false);
  const [copied, setCopied] = useState(false);
  const [showRegenConfirm, setShowRegenConfirm] = useState(false);
  const API_KEY_REAL = "ciq_sk_live_caelum2026_xxxxxxxxxx";
  const API_KEY_MASKED = "ciq_••••••••••••••••••••••••••••••••";

  const handleCopy = () => {
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Password */}
      <div className="bg-white rounded-xl border border-slate-200">
        <div className="px-6 py-4 border-b border-slate-100">
          <h3 className="font-semibold text-slate-900">Mot de passe</h3>
          <p className="text-xs text-slate-400 mt-0.5">Modifiez votre mot de passe de connexion</p>
        </div>
        <div className="p-6 space-y-4">
          {[
            { label: "Mot de passe actuel", placeholder: "••••••••" },
            { label: "Nouveau mot de passe", placeholder: "••••••••" },
            { label: "Confirmer le nouveau mot de passe", placeholder: "••••••••" },
          ].map((f) => (
            <div key={f.label}>
              <label className="block text-xs font-semibold text-slate-600 mb-1.5">{f.label}</label>
              <input
                type="password"
                placeholder={f.placeholder}
                className="w-full border border-slate-200 rounded-lg px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent hover:border-slate-300 transition-all"
              />
            </div>
          ))}
          <div className="pt-2">
            <button className="bg-indigo-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors shadow-sm">
              Mettre à jour
            </button>
          </div>
        </div>
      </div>

      {/* 2FA */}
      <div className="bg-white rounded-xl border border-slate-200">
        <div className="px-6 py-4 border-b border-slate-100">
          <h3 className="font-semibold text-slate-900">Authentification à deux facteurs</h3>
          <p className="text-xs text-slate-400 mt-0.5">Ajoutez une couche de sécurité supplémentaire</p>
        </div>
        <div className="p-6">
          <div className="flex items-center justify-between">
            <div>
              {twoFA ? (
                <div>
                  <p className="text-sm font-medium text-slate-800">2FA activée via application d&apos;authentification</p>
                  <span className="inline-flex items-center gap-1.5 mt-1.5 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-full">
                    <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full" /> Activée
                  </span>
                </div>
              ) : (
                <div>
                  <p className="text-sm font-medium text-slate-800">Non configurée</p>
                  <div className="flex items-center gap-2 mt-1.5">
                    <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-amber-700 bg-amber-50 border border-amber-200 px-2.5 py-1 rounded-full">
                      <span className="w-1.5 h-1.5 bg-amber-400 rounded-full" /> Non configurée
                    </span>
                    <button className="text-xs text-indigo-600 hover:text-indigo-800 font-medium underline">
                      Configurer
                    </button>
                  </div>
                </div>
              )}
            </div>
            <Toggle value={twoFA} onChange={() => setTwoFA((v) => !v)} />
          </div>
        </div>
      </div>

      {/* API Key */}
      <div className="bg-white rounded-xl border border-slate-200">
        <div className="px-6 py-4 border-b border-slate-100">
          <h3 className="font-semibold text-slate-900">Clé API</h3>
          <p className="text-xs text-slate-400 mt-0.5">Accédez à l&apos;API REST CompeteIQ depuis vos applications</p>
        </div>
        <div className="p-6 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-600 mb-1.5">Clé API CompeteIQ</label>
            <div className="flex items-center gap-2">
              <code className="flex-1 text-xs font-mono text-slate-700 bg-slate-50 border border-slate-200 rounded-lg px-3.5 py-2.5 select-all overflow-hidden text-ellipsis whitespace-nowrap">
                {showKey ? API_KEY_REAL : API_KEY_MASKED}
              </code>
              <button
                onClick={() => setShowKey((v) => !v)}
                className="flex-shrink-0 p-2.5 border border-slate-200 rounded-lg text-slate-500 hover:bg-slate-50 hover:text-slate-800 transition-all"
                title={showKey ? "Masquer" : "Révéler"}
              >
                <IconEye off={showKey} />
              </button>
              <button
                onClick={handleCopy}
                className={`flex-shrink-0 px-3.5 py-2.5 border rounded-lg text-xs font-semibold transition-all ${
                  copied
                    ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                    : "border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-800"
                }`}
              >
                {copied ? "✓ Copié!" : "Copier"}
              </button>
            </div>
          </div>
          <div className="flex items-center gap-3">
            {!showRegenConfirm ? (
              <button
                onClick={() => setShowRegenConfirm(true)}
                className="flex items-center gap-2 px-4 py-2 border border-red-200 text-red-500 rounded-lg text-sm font-medium hover:bg-red-50 hover:border-red-300 hover:text-red-700 transition-all"
              >
                Régénérer
              </button>
            ) : (
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-600 font-medium">Êtes-vous sûr ?</span>
                <button
                  onClick={() => setShowRegenConfirm(false)}
                  className="px-3 py-1.5 bg-red-600 text-white rounded-lg text-xs font-semibold hover:bg-red-700 transition-colors"
                >
                  Confirmer
                </button>
                <button
                  onClick={() => setShowRegenConfirm(false)}
                  className="px-3 py-1.5 border border-slate-200 text-slate-600 rounded-lg text-xs font-medium hover:bg-slate-50 transition-colors"
                >
                  Annuler
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Active sessions */}
      <div className="bg-white rounded-xl border border-slate-200">
        <div className="px-6 py-4 border-b border-slate-100">
          <h3 className="font-semibold text-slate-900">Sessions actives</h3>
          <p className="text-xs text-slate-400 mt-0.5">Appareils actuellement connectés à votre compte</p>
        </div>
        <div className="divide-y divide-slate-50">
          {[
            {
              device: "Chrome / macOS",
              location: "Bruxelles, Belgique",
              when: null,
              current: true,
            },
            {
              device: "Safari / iPhone",
              location: "Paris, France",
              when: "il y a 2 jours",
              current: false,
            },
          ].map((s, i) => (
            <div key={i} className="flex items-center justify-between gap-4 px-6 py-4 hover:bg-slate-50/50 transition-colors">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-slate-100 flex items-center justify-center flex-shrink-0">
                  <svg className="w-4 h-4 text-slate-500" viewBox="0 0 16 16" fill="none">
                    <rect x="1" y="3" width="14" height="9" rx="1.5" stroke="currentColor" strokeWidth="1.4" />
                    <path d="M5 15h6M8 12v3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
                  </svg>
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-800">{s.device}</p>
                  <p className="text-xs text-slate-400">{s.location}{s.when ? ` — ${s.when}` : ""}</p>
                </div>
              </div>
              <div className="flex items-center gap-2 flex-shrink-0">
                {s.current ? (
                  <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-full">
                    Session actuelle
                  </span>
                ) : (
                  <button className="text-xs text-red-500 hover:text-red-700 font-medium px-2.5 py-1.5 border border-red-200 rounded-md hover:bg-red-50 transition-colors">
                    Révoquer
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── Tab 4: Intégrations ────────────────────────────────────────────────────────

const INTEGRATIONS = [
  {
    icon: <IconSlack />,
    name: "Slack",
    desc: "Notifications en temps réel",
    connected: true,
  },
  {
    icon: <IconGmail />,
    name: "Gmail",
    desc: "Alertes par email",
    connected: true,
  },
  {
    icon: <IconWebhook />,
    name: "Webhooks",
    desc: "API pour vos outils",
    connected: false,
  },
  {
    icon: <IconZapier />,
    name: "Zapier",
    desc: "Automatisations no-code",
    connected: false,
  },
];

function TabIntegrations() {
  return (
    <div className="space-y-6">
      <div className="grid sm:grid-cols-2 gap-4">
        {INTEGRATIONS.map((integ) => (
          <div
            key={integ.name}
            className="bg-white border border-slate-200 rounded-xl p-5 flex items-center gap-4 hover:shadow-sm transition-shadow"
          >
            <div className="flex-shrink-0 w-12 h-12 rounded-xl border border-slate-100 bg-slate-50 flex items-center justify-center">
              {integ.icon}
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-semibold text-slate-900 text-sm">{integ.name}</p>
              <p className="text-xs text-slate-400 mt-0.5">{integ.desc}</p>
              <div className="mt-2">
                {integ.connected ? (
                  <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-700">
                    <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full" /> Connecté
                  </span>
                ) : (
                  <span className="text-xs text-slate-400 font-medium">Non configuré</span>
                )}
              </div>
            </div>
            <div className="flex flex-col gap-2 flex-shrink-0">
              {integ.connected ? (
                <>
                  <button className="text-xs text-indigo-600 hover:text-indigo-800 font-medium px-3 py-1.5 border border-indigo-200 rounded-md hover:bg-indigo-50 transition-colors whitespace-nowrap">
                    Configurer
                  </button>
                  {integ.name !== "Gmail" && (
                    <button className="text-xs text-slate-500 hover:text-red-600 font-medium px-3 py-1.5 border border-slate-200 rounded-md hover:bg-red-50 hover:border-red-200 transition-colors whitespace-nowrap">
                      Déconnecter
                    </button>
                  )}
                </>
              ) : (
                <button className="text-xs text-indigo-600 hover:text-indigo-800 font-medium px-3 py-1.5 border border-indigo-200 rounded-md hover:bg-indigo-50 transition-colors whitespace-nowrap">
                  {integ.name === "Zapier" ? "Connecter" : "Configurer"}
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Tab 5: Facturation ─────────────────────────────────────────────────────────

const USAGE_BARS = [
  { label: "Concurrents surveillés", value: 5, max: 5, unit: "", pct: 100, color: "bg-red-500" },
  { label: "Alertes ce mois", value: 24, max: null, unit: "", pct: 30, color: "bg-emerald-500" },
  { label: "Rapports générés", value: 3, max: 10, unit: "", pct: 30, color: "bg-indigo-500" },
];

const BILLING_HISTORY = [
  { date: "18 mai 2026", desc: "CompeteIQ Professional", amount: "47€" },
  { date: "18 avril 2026", desc: "CompeteIQ Professional", amount: "47€" },
  { date: "18 mars 2026", desc: "CompeteIQ Professional", amount: "47€" },
];

function TabFacturation() {
  return (
    <div className="space-y-6">
      {/* Current plan */}
      <div className="bg-white rounded-xl border border-slate-200">
        <div className="px-6 py-4 border-b border-slate-100">
          <h3 className="font-semibold text-slate-900">Plan actuel</h3>
        </div>
        <div className="p-6">
          <div className="flex items-start justify-between gap-4">
            <div>
              <span className="inline-flex items-center text-xs font-bold text-indigo-700 bg-indigo-100 px-2.5 py-1 rounded-full uppercase tracking-wider mb-3">
                Professional
              </span>
              <p className="text-3xl font-bold text-slate-900">47€ <span className="text-base font-normal text-slate-400">/ mois</span></p>
              <p className="text-xs text-slate-400 mt-1">Renouvellement : 18 juillet 2026</p>
              <ul className="mt-4 space-y-1.5">
                {["5 concurrents", "Alertes illimitées", "Tous les agents", "Support prioritaire"].map((f) => (
                  <li key={f} className="flex items-center gap-2 text-sm text-slate-700">
                    <span className="text-emerald-500 font-bold">✓</span> {f}
                  </li>
                ))}
              </ul>
            </div>
            <button className="flex-shrink-0 border border-indigo-200 text-indigo-700 px-4 py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-50 transition-colors">
              Changer de plan
            </button>
          </div>
        </div>
      </div>

      {/* Usage */}
      <div className="bg-white rounded-xl border border-slate-200">
        <div className="px-6 py-4 border-b border-slate-100">
          <h3 className="font-semibold text-slate-900">Utilisation</h3>
        </div>
        <div className="p-6 space-y-5">
          {USAGE_BARS.map((bar) => (
            <div key={bar.label}>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-sm text-slate-700 font-medium">{bar.label}</span>
                <span className="text-xs text-slate-500 font-semibold">
                  {bar.value}{bar.max !== null ? `/${bar.max}` : "/∞"}
                </span>
              </div>
              <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${bar.color} transition-all`}
                  style={{ width: `${bar.pct}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Billing history */}
      <div className="bg-white rounded-xl border border-slate-200">
        <div className="px-6 py-4 border-b border-slate-100">
          <h3 className="font-semibold text-slate-900">Historique de facturation</h3>
        </div>
        <div className="divide-y divide-slate-50">
          {BILLING_HISTORY.map((row) => (
            <div key={row.date} className="flex items-center justify-between gap-4 px-6 py-4 hover:bg-slate-50/50 transition-colors">
              <div>
                <p className="text-sm font-medium text-slate-800">{row.desc}</p>
                <p className="text-xs text-slate-400 mt-0.5">{row.date}</p>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm font-semibold text-slate-900">{row.amount}</span>
                <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">
                  Payé ✓
                </span>
                <a
                  href="#"
                  className="text-xs text-indigo-600 hover:text-indigo-800 font-medium underline whitespace-nowrap"
                >
                  Télécharger
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState<TabKey>("profil");

  return (
    <div className="flex gap-8 items-start">
      {/* Left sidebar nav */}
      <nav className="w-52 flex-shrink-0 sticky top-6">
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-3 px-3">Paramètres</p>
        <ul className="space-y-0.5">
          {TABS.map((tab) => {
            const isActive = activeTab === tab.key;
            return (
              <li key={tab.key}>
                <button
                  onClick={() => setActiveTab(tab.key)}
                  className={`w-full flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm font-medium transition-all text-left ${
                    isActive
                      ? "bg-indigo-50 text-indigo-700"
                      : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                  }`}
                >
                  <span className={isActive ? "text-indigo-600" : "text-slate-400"}>
                    {tab.icon}
                  </span>
                  {tab.label}
                  {isActive && (
                    <span className="ml-auto w-1.5 h-1.5 rounded-full bg-indigo-500 flex-shrink-0" />
                  )}
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Main content */}
      <div className="flex-1 min-w-0 max-w-2xl">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-slate-900">
            {TABS.find((t) => t.key === activeTab)?.label}
          </h2>
          <p className="text-slate-500 text-sm mt-1">Gérez votre compte et vos préférences</p>
        </div>

        {activeTab === "profil" && <TabProfil />}
        {activeTab === "equipe" && <TabEquipe />}
        {activeTab === "securite" && <TabSecurite />}
        {activeTab === "integrations" && <TabIntegrations />}
        {activeTab === "facturation" && <TabFacturation />}
      </div>
    </div>
  );
}
