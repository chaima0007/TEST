import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-food-famine-accountability-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Right to Food Famine Accountability Engine Agent",
  domain: "right_to_food_famine_accountability",
  total_entities: 8,
  avg_composite: 62.85,
  confidence_score: 0.91,
  avg_estimated_right_to_food_famine_accountability_index: 6.29,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: { aid_blockade_starvation: 3, intentional_famine_weapon: 2, ihl_food_violation: 2, accountability_gap_famine: 1 },
  top_risk_entities: [
    "Gaza/Palestine — Famine Intentionnelle 2024, Aide Bloquée & Violations DIH Massives",
    "Soudan/Darfour — 8.5M Risque Famine, Aid Bloquée Khartoum & Arme Affamement",
    "Yémen/Hodeidah — Blocus Port Grain, 21M Insécurité Alimentaire & Responsabilité Coaltion",
  ],
  critical_alerts: [
    "Gaza/Palestine: intentional_famine_weapon",
    "Soudan/Darfour: aid_blockade_starvation",
    "Yémen/Hodeidah: aid_blockade_starvation",
    "Myanmar/Chin-Kachin: ihl_food_violation",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  data_sources: [
    "fao_right_to_food_guidelines_2022",
    "un_sr_food_report_2023",
    "oxfam_famine_accountability_2023",
    "icrc_starvation_ihl_2023",
  ],
  entities: [
    { id: "RF-001", name: "Gaza/Palestine — Famine Intentionnelle 2024, Aide Bloquée & Violations DIH Massives", country: "MENA", sector: "IPC Phase 5 Famine Confirmée Nord Gaza Mars 2024, 2M Personnes Assiégées, Aide ONU Bloquée Checkpoints & Amendement Rome Affamement Crime Guerre Applicable", composite_score: 96.2, aid_blockade_starvation_score: 98.0, intentional_famine_weapon_score: 97.0, ihl_food_violation_score: 95.0, accountability_gap_famine_score: 95.0, risk_level: "critique", primary_pattern: "intentional_famine_weapon", key_signals: ["Famine intentionnelle confirmée à Gaza — IPC Phase 5 (famine) confirmée au nord de Gaza en mars 2024, avec utilisation documentée de l'alimentation comme arme de guerre par le blocus israélien, constituant un crime de guerre selon l'Article 8(2)(b)(xxv) du Statut de Rome", "Aide humanitaire systématiquement bloquée — convois WFP/UNRWA bloqués aux checkpoints, destructions d'entrepôts alimentaires, 500 calouries/jour par personne documentées (seuil survie : 1600), violation flagrante DIH Article 70 Protocole I Genève", "Activer la CPI pour poursuites crime de guerre d'affamement à Gaza et exiger l'accès immédiat humanitaire illimité via corridor maritime et terrestre supervisé par ONU"], estimated_right_to_food_famine_accountability_index: 9.62, last_updated: "2026-06-21" },
    { id: "RF-002", name: "Soudan/Darfour — 8.5M Risque Famine, Aide Bloquée Khartoum & Arme Affamement", country: "Afrique de l'Est", sector: "8.5M Personnes IPC4-5 Sudan 2024, RSF Pillage WFP Entrepôts, SAF Restrictions Passage Humanitaire Darfour & Première Famine Officielle Afrique 21e Siècle", composite_score: 91.8, aid_blockade_starvation_score: 92.0, intentional_famine_weapon_score: 93.0, ihl_food_violation_score: 90.0, accountability_gap_famine_score: 92.0, risk_level: "critique", primary_pattern: "intentional_famine_weapon", key_signals: ["Première famine officielle du XXIe siècle en Afrique au Soudan — IPC Phase 5 confirmée au Darfour en 2024, avec 8.5 millions en risque immédiat, pillage systématique des entrepôts WFP par les RSF et blocage SAF des corridors humanitaires", "Arme de famine utilisée par les deux belligérants — tant les Forces Armées Soudanaises (SAF) que les Forces de Soutien Rapide (RSF) ont délibérément restreint l'aide alimentaire comme tactique de guerre, crime de guerre selon DIH", "Activer d'urgence le mécanisme du Conseil de Sécurité ONU sur protection civils (résolution 2417) pour forcer l'accès humanitaire au Darfour et Khartoum et financer 2 milliards USD d'aide alimentaire d'urgence"], estimated_right_to_food_famine_accountability_index: 9.18, last_updated: "2026-06-21" },
    { id: "RF-003", name: "Yémen/Hodeidah — Blocus Port Grain, 21M Insécurité Alimentaire & Responsabilité Coalition", country: "MENA", sector: "21M Personnes Insécurité Alimentaire Yemen 2024, Port Hodeidah Bloqué Coalition 2015-22, 70% Imports Food Via Hodeidah & Destruction Infrastructure Eau/Agriculture Documentée", composite_score: 88.4, aid_blockade_starvation_score: 90.0, intentional_famine_weapon_score: 85.0, ihl_food_violation_score: 90.0, accountability_gap_famine_score: 89.0, risk_level: "critique", primary_pattern: "aid_blockade_starvation", key_signals: ["Blocus alimentaire maritime documenté au Yémen — la coalition saoudienne a bloqué le port de Hodeidah (70% des importations alimentaires yéménites) de 2015 à 2022, causant une crise alimentaire grave pour 21 millions de personnes selon WFP", "Destruction infrastructure critique — frappes aériennes ayant ciblé des fermes, systèmes d'irrigation et marchés alimentaires yéménites, violations DIH Articles 54 et 55 Protocole I sur protection des biens indispensables à la survie", "Établir un mécanisme international d'enquête sur les violations DIH alimentaires au Yémen et exiger des comptes de la coalition pour le blocus de Hodeidah devant le Conseil des Droits de l'Homme ONU"], estimated_right_to_food_famine_accountability_index: 8.84, last_updated: "2026-06-21" },
    { id: "RF-004", name: "Myanmar/Chin-Kachin — Aide Bloquée Junte, Villages Brûlés & 3M Déplacés Sans Nourriture", country: "Asie du Sud-Est", sector: "3M Déplacés Internes Myanmar 2024, Junte Bloc Aid ONG Zones Opposition, Villages Agriculture Incendiés Chin/Kachin/Sagaing & Criminalisation Aide Humanitaire", composite_score: 84.7, aid_blockade_starvation_score: 88.0, intentional_famine_weapon_score: 85.0, ihl_food_violation_score: 82.0, accountability_gap_famine_score: 84.0, risk_level: "critique", primary_pattern: "aid_blockade_starvation", key_signals: ["Criminalisation de l'aide humanitaire au Myanmar — la junte militaire a criminalisé l'assistance aux zones contrôlées par la résistance, avec arrestation de travailleurs humanitaires et confiscation de nourriture destinée aux déplacés", "Destruction systématique des moyens de subsistance — incendie délibéré de villages et de réserves de riz dans les États Chin, Kachin et Sagaing, stratégie documentée par Fortify Rights constituant crime de guerre DIH", "Activer une résolution du Conseil de Sécurité ONU sur l'accès humanitaire au Myanmar et sanctions ciblées contre les généraux responsables du blocage de l'aide alimentaire"], estimated_right_to_food_famine_accountability_index: 8.47, last_updated: "2026-06-21" },
    { id: "RF-005", name: "Éthiopie/Tigré — Famine Délibérée 2020-22, Siège Documenté & Manque Responsabilité", country: "Afrique de l'Est", sector: "500 000 Morts Famine Tigré Estimés 2020-22, Siège Fédéral/Amhara/Érythrée, Aide Bloquée 2 Ans & Commission Enquête ONU Accès Refusé", composite_score: 53.6, aid_blockade_starvation_score: 55.0, intentional_famine_weapon_score: 55.0, ihl_food_violation_score: 52.0, accountability_gap_famine_score: 52.0, risk_level: "élevé", primary_pattern: "accountability_gap_famine", key_signals: ["Famine délibérée la plus meurtrière récente — jusqu'à 500 000 morts estimés au Tigré entre 2020-2022, résultat d'un siège délibéré par forces fédérales, Amhara et érythréennes bloquant aide humanitaire pendant 2 ans", "Impunité totale après l'accord de paix — l'accord de Pretoria de novembre 2022 a été conclu sans mécanisme de justice transitionnelle ni responsabilité pour la famine délibérée, permettant aux responsables de continuer à gouverner", "Exiger que l'Accord de Pretoria intègre un mécanisme de justice transitionnelle sur les crimes de famine au Tigré et qu'une commission ONU indépendante documente les violations pour futures poursuites"], estimated_right_to_food_famine_accountability_index: 5.36, last_updated: "2026-06-21" },
    { id: "RF-006", name: "Corée du Nord — 42% Population Sous-Alimentée, Aide Détournée & Refus Accès Moniteurs", country: "Asie du Nord-Est", sector: "42% Population Sous-Alimentation FAO, Aide WFP Détournée Élites/Armée Documentée, Refus Accès Moniteurs Indépendants & Réforme Marchés Jangmadang Partielle", composite_score: 49.3, aid_blockade_starvation_score: 48.0, intentional_famine_weapon_score: 52.0, ihl_food_violation_score: 48.0, accountability_gap_famine_score: 49.0, risk_level: "élevé", primary_pattern: "intentional_famine_weapon", key_signals: ["Détournement systémique de l'aide alimentaire — le régime nord-coréen détourne l'aide alimentaire internationale vers l'armée et la nomenklatura, laissant 42% de la population en sous-alimentation chronique selon FAO, violation du droit à l'alimentation comme outil politique", "Opacité totale — Pyongyang refuse l'accès à tous les moniteurs alimentaires indépendants depuis 2019, rendant impossible la vérification de l'utilisation de l'aide et la documentation des violations du droit à la nourriture", "Conditionner l'aide alimentaire à la Corée du Nord à un accès de monitoring indépendant WFP et exiger que le Conseil de Sécurité traite la famine comme menace à la paix et sécurité internationales"], estimated_right_to_food_famine_accountability_index: 4.93, last_updated: "2026-06-21" },
    { id: "RF-007", name: "FAO/WFP — Droit Alimentation Guidelines 2004, IPC Famine Classification & Monitoring", country: "Global", composite_score: 23.1, aid_blockade_starvation_score: 22.0, intentional_famine_weapon_score: 20.0, ihl_food_violation_score: 25.0, accountability_gap_famine_score: 25.0, risk_level: "modéré", primary_pattern: "accountability_gap_famine", key_signals: ["FAO/WFP comme systèmes d'alerte précoce — les Directives sur le Droit à l'Alimentation FAO 2004 et le système IPC (Integrated Food Security Phase Classification) fournissent des standards et mécanismes de documentation essentiels mais sans pouvoir de sanction", "Financement chroniquement insuffisant — le WFP est financé à 50% en 2024 par rapport aux besoins, forçant des coupures dans les rations alimentaires pour réfugiés et populations en crise, malgré des famines actives documentées", "Tripler le financement du WFP et rendre les contributions des pays G7 contraignantes à hauteur de 0.1% du PIB pour le Programme Alimentaire Mondial selon les recommandations du Comité de Sécurité Alimentaire Mondiale"], estimated_right_to_food_famine_accountability_index: 2.31, last_updated: "2026-06-21" },
    { id: "RF-008", name: "OHCHR/Rapporteur Spécial Alimentation — Mandat, Général Comentaire 12 PIDESC & DIH", country: "Global", composite_score: 4.35, aid_blockade_starvation_score: 4.0, intentional_famine_weapon_score: 4.0, ihl_food_violation_score: 5.0, accountability_gap_famine_score: 4.5, risk_level: "faible", primary_pattern: "ihl_food_violation", key_signals: ["Cadre normatif solide — l'Observation Générale 12 du PIDESC (1999) et le mandat du Rapporteur Spécial ONU sur le droit à l'alimentation constituent la base légale contraignante du droit à l'alimentation pour 170+ États parties", "Amendement DIH sur affamement — l'amendement au Statut de Rome (2019) criminalisant l'affamement dans les conflits non-internationaux renforce le cadre pénal, mais sa faible ratification (26 États) limite son application", "Accélérer la ratification de l'amendement Statut de Rome sur l'affamement et renforcer le mandat du Rapporteur Spécial pour inclure enquêtes sur site dans les zones de conflit actif"], estimated_right_to_food_famine_accountability_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/right-to-food-famine-accountability-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
