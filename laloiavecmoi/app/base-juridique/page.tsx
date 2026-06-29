import Link from "next/link";
import fs from "node:fs";
import path from "node:path";
import BaseJuridiqueClient from "./BaseJuridiqueClient";

// Page "Base juridique vérifiée" — INDEX LÉGER + recherche (rendu statique).
// On ne charge PAS les 242 réponses complètes (trop lourd) : on passe un index compact
// (domaine + questions) ; les réponses complètes vivent sur /loi/[domaine] (rapides).

type FaitLeger = { id: string; question: string };
type ModuleLeger = { module: string; titre: string; theme: string; faits: FaitLeger[] };

// Classement en grands thèmes (premier mot-clé trouvé dans le slug l'emporte).
// Permet un filtre par thème côté client sans surcharger l'interface.
const THEMES: [string, string[]][] = [
  ["Logement & cadre de vie", ["bail", "logement", "colocation", "copropriete", "expulsion", "breyne", "marchand_de_sommeil", "occupation_sans_titre", "saisie_immobiliere", "urbanisme", "malfacons", "expropriation", "precompte", "achat_logement", "voisinage", "eau", "energie", "dechets"]],
  ["Famille, couple & enfants", ["couple", "divorce", "filiation", "naissance", "adoption", "garde_enfants", "conge_maternite", "pension_alimentaire", "tutelle", "voyage_mineur", "enfants_places", "maltraitance", "violences_conjugales", "violences_sexuelles", "procreation", "famille", "aidant"]],
  ["Décès, succession & fin de vie", ["deces", "succession", "testament", "donation", "fin_de_vie", "don_organes"]],
  ["Travail & emploi", ["travail", "chomage", "licenciement", "premier_emploi", "job_etudiant", "conges_thematiques", "burnout", "accident_travail", "maladie_professionnelle", "incapacite", "statut_social_artiste", "fonction_publique", "independant", "harcelement", "discrimination", "sexisme", "benevolat", "titres_services"]],
  ["Argent, impôts & dettes", ["banque", "credit", "surendettement", "saisies", "recouvrement", "impots", "epargne", "pension", "grapa", "revenu_integration", "allocations", "bourse", "service_bancaire", "aide_urgence"]],
  ["Santé & handicap", ["sante", "assurance_maladie", "assurance_hospitalisation", "mutuelle", "dossier_medical", "drogues", "handicap", "soins", "aide_medicale", "ivg"]],
  ["Justice & recours", ["justice", "aide_juridique", "casier", "mediation", "recours", "plaintes", "sanctions", "litiges", "legalisation", "protection_personne"]],
  ["Mobilité & véhicule", ["permis_conduire", "voiture", "assurance_auto", "circulation", "transport", "mobilite", "accidents_route"]],
  ["Consommation & arnaques", ["consommation", "produits_defectueux", "vices_caches", "telecom", "publicite", "voyage", "occasion", "fraude", "assurance"]],
  ["Papiers, citoyenneté & Europe", ["etrangers", "nationalite", "citoyen", "vote", "equivalence", "transfrontalier", "europeen", "documents_identite", "changement_nom", "changement_mention_sexe", "adresse", "domiciliation", "gouvernement", "enseignement", "enfant"]],
  ["Vie privée & numérique", ["vie_privee", "droit_image", "rgpd"]],
];

function themePour(slug: string): string {
  for (const [nom, kws] of THEMES) {
    for (const k of kws) if (slug.includes(k)) return nom;
  }
  return "Autres";
}

function chargerIndex(): ModuleLeger[] {
  const dir = path.join(process.cwd(), "data", "belgium");
  let fichiers: string[] = [];
  try {
    fichiers = fs.readdirSync(dir).filter((f) => f.endsWith(".json") && !f.startsWith("_"));
  } catch {
    return [];
  }
  const mods: ModuleLeger[] = [];
  for (const f of fichiers.sort()) {
    try {
      const d = JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8"));
      if (d && Array.isArray(d.faits) && d.faits.length) {
        mods.push({
          module: d.module,
          titre: d.titre,
          theme: themePour(d.module),
          faits: d.faits.map((x: { id: string; question: string }) => ({ id: x.id, question: x.question })),
        });
      }
    } catch {
      /* ignore */
    }
  }
  return mods.sort((a, b) => (a.titre || "").localeCompare(b.titre || ""));
}

// Rendu statique : index figé au build → page légère servie instantanément, tient la charge.
export const dynamic = "force-static";

export const metadata = {
  title: "Base juridique vérifiée — La Loi Avec Moi",
  description:
    "Toutes nos réponses juridiques par domaine, chacune sourcée et datée. Recherchez votre question ou choisissez un domaine.",
};

export default function BaseJuridiquePage() {
  const index = chargerIndex();
  const totalFaits = index.reduce((n, m) => n + m.faits.length, 0);

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi</span>
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">
            ← Accueil
          </Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-blue-950 to-slate-900 text-white py-16 px-6">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold">Base juridique vérifiée</h1>
          <p className="mt-3 text-blue-100 max-w-2xl">
            {totalFaits} réponses sur {index.length} domaines — chacune sourcée et datée. Cherchez votre question
            ou choisissez un domaine.
          </p>
        </div>
      </section>

      <div className="max-w-5xl mx-auto px-6 pt-6">
        <p className="text-sm rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-600">
          🌐 <strong>Une autre langue ?</strong> Cette page peut être traduite automatiquement par votre navigateur
          (menu « Traduire »). Version néerlandaise : <a href="/de-wet-met-mij" className="text-indigo-700 hover:underline">de wet met mij</a>.
          La traduction automatique peut comporter des imprécisions — le texte sourcé de référence reste en français.
        </p>
      </div>

      <BaseJuridiqueClient index={index} />
    </main>
  );
}
