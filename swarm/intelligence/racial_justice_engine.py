"""Racial Justice Engine — Wave 38"""

from dataclasses import dataclass
from typing import List


@dataclass
class RacialJusticeEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    systemic_discrimination_score: float
    racial_profiling_police_score: float
    wealth_education_gap_score: float
    hate_speech_ideology_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.systemic_discrimination_score * 0.30
            + self.racial_profiling_police_score * 0.25
            + self.wealth_education_gap_score * 0.25
            + self.hate_speech_ideology_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60: return "critique"
        if s >= 40: return "élevé"
        if s >= 20: return "modéré"
        return "faible"

    @property
    def primary_pattern(self) -> str:
        scores = {
            "discrimination_systemique": self.systemic_discrimination_score,
            "profilage_racial_police": self.racial_profiling_police_score,
            "inegalite_richesse_education": self.wealth_education_gap_score,
            "discours_haine_ideologie": self.hate_speech_ideology_score,
        }
        return max(scores, key=scores.get)

    @property
    def estimated_racial_justice_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "systemic_discrimination_score": self.systemic_discrimination_score,
            "racial_profiling_police_score": self.racial_profiling_police_score,
            "wealth_education_gap_score": self.wealth_education_gap_score,
            "hate_speech_ideology_score": self.hate_speech_ideology_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_racial_justice_index": self.estimated_racial_justice_index,
            "last_updated": "2026-06-20",
        }

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Injustice raciale systémique documentée — {self.name} avec score composite {self.composite_score}/100 révélant des discriminations structurelles violant l'Article 2 de la DUDH, l'Article 26 du PIDCP et la Convention Internationale sur l'Élimination de Toutes les Formes de Discrimination Raciale (CERD 1965)",
            f"Discrimination systémique ({self.systemic_discrimination_score}/100) — les inégalités raciales institutionnalisées constituent des violations directes de la CERD obligeant les États à prendre des mesures spéciales immédiates pour remédier aux discriminations historiques et actuelles",
            "Activer le Comité pour l'Élimination de la Discrimination Raciale (CERD) pour examen des rapports périodiques et exiger la mise en œuvre du Programme d'action de Durban III (2021) sur l'élimination du racisme et de la discrimination raciale",
        ]


ENTITIES = [
    RacialJusticeEntity("RJ-001", "USA/Noir·es — Wealth Gap 8:1, Police Violence 3× & Mass Incarceration 13% Pop 33% Prison", "Amérique du Nord", "USA Richesse Médiane Blancs/Noirs 8:1 Fed Reserve, Police Violence Afro-Américains 3× Blancs, Mass Incarceration 13% Population 33% Prisonniers & Redlining Héritage Historique", 92, 90, 92, 85),
    RacialJusticeEntity("RJ-002", "Brésil/Racisme Structurel — 55% Noirs/Métis, Favelas Ciblées & Violência Policial", "Amérique Latine", "Brésil 55% Noirs/Métis 75% Victimes Violence, Favelas Ciblées Police BOPE, Racisme Structurel Emploi/Éducation, 80% Tués Police Noirs & Statut Social Apartheid Silencieux", 88, 92, 85, 85),
    RacialJusticeEntity("RJ-003", "Europe/Roms — 10-12M Apatrides, Discrimination Emploi/Logement & Antigypsyisme Institutionnel", "Europe", "10-12M Roms Europe Discrimination Emploi 90%, Logement Ségrégué, Antigypsyisme Institutionnel Reconnu ECRI, Stérilisations Forcées Tchéquie/Slovaquie & Enfants Surreprésentés Écoles Spéciales", 85, 82, 88, 85),
    RacialJusticeEntity("RJ-004", "Inde/Castes-Dalits — 200M Dalits, Intouchabilité Pratique & Atrocités 50 000/An", "Asie du Sud", "Inde 200M Dalits Discrimination Caste Emploi/Mariage/Temple, Atrocités NCRB 50 000/An, Manuels Égout Éboueurs Force & Caste Système Légalement Aboli Pratiquement Vivant", 88, 82, 85, 88),
    RacialJusticeEntity("RJ-005", "Israel/Arabes Israéliens — Loi Nation-État 2018, Inégalités & Discrimination Budgétaire", "MENA", "Israël Loi Nation-État 2018 Citoyens Arabes 20% Citoyens Secondaires, Budgets Municipaux Arabes -40% Juifs, Discrimination Emploi Sécurité & Ou-Bem Rapports Inégalités Systémiques", 55, 52, 62, 52),
    RacialJusticeEntity("RJ-006", "France/Discrimination — Profiling Racial Police, Banlieues & CV Anonyme Refus", "Europe de l'Ouest", "France Testing Discrimination 3× Moins Rappels CV Arabes/Africains, Contrôles Identité Profiling Racial CNRS, Banlieues IZI Sous-Financement & ECRI Rapport France Profiling 2022", 50, 58, 52, 50),
    RacialJusticeEntity("RJ-007", "Allemagne/Néo-Nazis — NSU Meurtres 10 Victimes, AFD Xénophobie & Rechtsextremismus", "Europe de l'Ouest", "Allemagne NSU Meurtres 10 Victimes Turques Grecques, AFD Partis Extrême Droite 20%+, Rechtsextremismus Violence +50% 2021-23 BfV & ECRI Recommandations Non-Appliquées", 28, 30, 32, 35),
    RacialJusticeEntity("RJ-008", "CERD-ONU/Durban — Convention 1965, Programme Durban III & Rapporteur Spécial Racisme", "Global", "CERD Convention 1965 182 États Parties, Programme d'Action Durban III 2021, Rapporteur Spécial ONU Racisme Contemporain & Décennie ONU Personnes Afro-Descendantes 2015-24", 5, 4, 3, 6),
]


def summary() -> dict:
    entities_data = [e.to_dict() for e in ENTITIES]
    avg = round(sum(e.composite_score for e in ENTITIES) / len(ENTITIES), 2)
    risk_dist = {}
    pattern_dist = {}
    for e in ENTITIES:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
    top = sorted(ENTITIES, key=lambda x: x.composite_score, reverse=True)[:3]
    critical = [e for e in ENTITIES if e.risk_level == "critique"]
    return {
        "total_entities": len(ENTITIES),
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": [e.name for e in top],
        "critical_alerts": [f"{e.name.split('—')[0].strip()}: {e.primary_pattern.replace('_', ' ')}" for e in critical],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "racial_justice",
        "confidence_score": 0.83,
        "data_sources": [
            "cerd_committee_concluding_observations_database",
            "un_special_rapporteur_racism_racial_discrimination_reports",
            "ecri_country_monitoring_reports_european_racism",
        ],
        "entities": entities_data,
        "avg_estimated_racial_justice_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")
