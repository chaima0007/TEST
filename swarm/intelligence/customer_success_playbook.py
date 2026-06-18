"""Customer Success Playbook — prescribes the right CS motion for each account based on health, lifecycle, and risk profile."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional


class LifecycleStage(str, Enum):
    ONBOARDING = "onboarding"       # 0-90 days post-signature
    ADOPTION = "adoption"           # 91-180 days, driving feature usage
    GROWTH = "growth"               # 181-365 days, expanding value
    MATURE = "mature"               # 365+ days, renewal horizon
    AT_RISK = "at_risk"             # any stage with churn signals


class PlaybookMotion(str, Enum):
    EXPAND = "expand"               # High health, growth signals — upsell / cross-sell
    RETAIN = "retain"               # Moderate health, protect renewal
    RESCUE = "rescue"               # Low health, churn risk — intervention required
    ONBOARD = "onboard"             # New account, activation-first
    ACCELERATE = "accelerate"       # Good health but underutilising — deepen adoption


class RiskLevel(str, Enum):
    LOW = "low"                     # health >= 75
    MEDIUM = "medium"               # health 50-74
    HIGH = "high"                   # health 25-49
    CRITICAL = "critical"           # health < 25


@dataclass
class CSPlaybookInput:
    account_id: str
    account_name: str
    segment: str                # enterprise / mid_market / smb
    arr_eur: float
    days_since_signature: int   # determines lifecycle stage candidate

    # Health dimensions (0-100 each)
    product_adoption_score: float   # feature/module usage breadth
    support_health_score: float     # ticket volume, CSAT, resolution time
    engagement_score: float         # logins, QBRs, champion activity
    nps_score: float                # -100 to +100

    # Renewal & growth context
    days_to_renewal: int            # days until contract renewal
    has_expansion_potential: bool   # CSM-assessed expansion opportunity
    competitive_pressure: bool      # known competitor activity
    executive_sponsor_active: bool  # C-level engagement present
    champion_strength: float        # 0-100

    # Usage signals
    dau_mau_ratio: float            # daily/monthly active user ratio 0-1
    features_adopted_pct: float     # % of purchased features actively used
    last_login_days_ago: int        # days since last user login

    # Escalation context
    open_escalations: int           # unresolved escalated tickets
    missed_qbr_count: int           # number of QBRs skipped by customer
    onboarding_complete: bool       # initial onboarding milestone reached


@dataclass
class CSPlaybookResult:
    account_id: str
    account_name: str
    segment: str
    arr_eur: float

    lifecycle_stage: LifecycleStage
    risk_level: RiskLevel
    playbook_motion: PlaybookMotion
    overall_health_score: float     # 0-100

    renewal_urgency: str            # immediate / high / medium / low
    expansion_readiness: str        # ready / building / not_ready

    key_risks: list[str]
    immediate_actions: list[str]
    playbook_steps: list[str]
    success_metrics: list[str]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["lifecycle_stage"] = self.lifecycle_stage.value
        d["risk_level"] = self.risk_level.value
        d["playbook_motion"] = self.playbook_motion.value
        return d


# ─── Scoring helpers ──────────────────────────────────────────────────────────

def _overall_health(inp: CSPlaybookInput) -> float:
    # nps normalised 0-100 from -100..+100
    nps_norm = (inp.nps_score + 100) / 2.0
    nps_norm = max(0.0, min(100.0, nps_norm))

    health = (
        inp.product_adoption_score * 0.30
        + inp.support_health_score * 0.20
        + inp.engagement_score * 0.25
        + nps_norm * 0.25
    )
    return round(max(0.0, min(100.0, health)), 1)


def _risk_level(health: float) -> RiskLevel:
    if health >= 75:
        return RiskLevel.LOW
    if health >= 50:
        return RiskLevel.MEDIUM
    if health >= 25:
        return RiskLevel.HIGH
    return RiskLevel.CRITICAL


def _lifecycle_stage(inp: CSPlaybookInput, health: float) -> LifecycleStage:
    d = inp.days_since_signature
    if inp.open_escalations >= 2 or health < 30 or (inp.competitive_pressure and health < 50):
        return LifecycleStage.AT_RISK
    if d <= 90:
        return LifecycleStage.ONBOARDING
    if d <= 180:
        return LifecycleStage.ADOPTION
    if d <= 365:
        return LifecycleStage.GROWTH
    return LifecycleStage.MATURE


def _renewal_urgency(inp: CSPlaybookInput) -> str:
    d = inp.days_to_renewal
    if d <= 30:
        return "immediate"
    if d <= 90:
        return "high"
    if d <= 180:
        return "medium"
    return "low"


def _expansion_readiness(inp: CSPlaybookInput, health: float) -> str:
    if health >= 70 and inp.has_expansion_potential and inp.champion_strength >= 60:
        return "ready"
    if health >= 50 and inp.has_expansion_potential:
        return "building"
    return "not_ready"


def _playbook_motion(
    inp: CSPlaybookInput,
    stage: LifecycleStage,
    risk: RiskLevel,
    readiness: str,
) -> PlaybookMotion:
    if stage == LifecycleStage.ONBOARDING:
        return PlaybookMotion.ONBOARD
    if stage == LifecycleStage.AT_RISK or risk == RiskLevel.CRITICAL:
        return PlaybookMotion.RESCUE
    if risk == RiskLevel.HIGH:
        return PlaybookMotion.RETAIN
    if readiness == "ready" and not inp.competitive_pressure:
        return PlaybookMotion.EXPAND
    if inp.features_adopted_pct < 50 and risk in (RiskLevel.LOW, RiskLevel.MEDIUM):
        return PlaybookMotion.ACCELERATE
    return PlaybookMotion.RETAIN


def _build_risks(inp: CSPlaybookInput, health: float, risk: RiskLevel) -> list[str]:
    risks: list[str] = []
    if inp.open_escalations >= 2:
        risks.append(f"{inp.open_escalations} escalades ouvertes — satisfaction critique")
    if inp.product_adoption_score < 40:
        risks.append(f"Adoption produit faible ({inp.product_adoption_score:.0f}/100) — risque de churn")
    if inp.last_login_days_ago > 14:
        risks.append(f"Dernière connexion il y a {inp.last_login_days_ago}j — désengagement utilisateur")
    if inp.competitive_pressure:
        risks.append("Pression concurrentielle active — protéger la relation en priorité")
    if inp.days_to_renewal <= 90 and risk in (RiskLevel.HIGH, RiskLevel.CRITICAL):
        risks.append(f"Renouvellement dans {inp.days_to_renewal}j — santé insuffisante pour sécuriser")
    if inp.nps_score < 0:
        risks.append(f"NPS négatif ({inp.nps_score:.0f}) — promoteur → détracteur, churn probable")
    if inp.missed_qbr_count >= 2:
        risks.append(f"{inp.missed_qbr_count} QBRs manqués — relation à risque")
    if inp.champion_strength < 30:
        risks.append("Champion faible ou absent — pas de relais interne")
    if inp.dau_mau_ratio < 0.15:
        risks.append(f"DAU/MAU à {inp.dau_mau_ratio:.0%} — usage irrégulier, valeur non perçue")
    if not inp.executive_sponsor_active and inp.arr_eur >= 100000:
        risks.append("Sponsor exécutif inactif sur un compte stratégique")
    return risks


def _build_actions(
    inp: CSPlaybookInput,
    motion: PlaybookMotion,
    urgency: str,
    readiness: str,
) -> list[str]:
    actions: list[str] = []

    if motion == PlaybookMotion.RESCUE:
        actions.append("Appel de récupération urgent avec le champion — comprendre les blocages")
        if inp.open_escalations >= 1:
            actions.append(f"Escalader les {inp.open_escalations} ticket(s) en attente — résoudre sous 48h")
        if not inp.executive_sponsor_active:
            actions.append("Engager le sponsor exécutif côté client et côté fournisseur")
        actions.append("Construire un plan de remédiation 30j avec jalons mesurables")
        if inp.competitive_pressure:
            actions.append("Préparer un briefing concurrentiel — renforcer la valeur différenciante")

    elif motion == PlaybookMotion.ONBOARD:
        actions.append("Lancer la séquence d'onboarding — kick-off et plan de succès J0-90")
        actions.append("Identifier et activer le champion interne dès la première semaine")
        if not inp.onboarding_complete:
            actions.append("Valider les jalons d'onboarding — objectifs, cas d'usage, KPIs")
        actions.append("Planifier un check-in bi-hebdomadaire jusqu'à l'adoption stable")

    elif motion == PlaybookMotion.ACCELERATE:
        actions.append(f"Session d'activation fonctionnelle — couvrir les {100-inp.features_adopted_pct:.0f}% de features non utilisées")
        actions.append("Organiser un atelier 'best practices' avec les utilisateurs clés")
        if inp.dau_mau_ratio < 0.2:
            actions.append("Investiguer les freins à l'usage quotidien — UX, formation, intégration")
        actions.append("Partager des cas d'usage clients similaires pour inspirer l'adoption")

    elif motion == PlaybookMotion.EXPAND:
        actions.append("Préparer une proposition d'expansion — licences, modules ou tier supérieur")
        if inp.has_expansion_potential:
            actions.append("Qualifier l'opportunité d'expansion avec le champion et le décideur budget")
        if inp.executive_sponsor_active:
            actions.append("Impliquer le sponsor exécutif dans la conversation d'expansion")
        actions.append("Planifier un QBR axé croissance — présenter les ROI atteints et les next steps")

    else:  # RETAIN
        if urgency in ("immediate", "high"):
            actions.append(f"Séquence de renouvellement urgente — {inp.days_to_renewal}j avant expiration")
        actions.append("QBR de santé — présenter les succès et aligner sur les objectifs année suivante")
        if inp.competitive_pressure:
            actions.append("Préparer un briefing ROI pour contrer la pression concurrentielle")
        if inp.missed_qbr_count >= 1:
            actions.append("Reprendre cadence QBR — proposer format flexible si besoin")

    # Universal
    if inp.last_login_days_ago > 7:
        actions.append(f"Campagne de réengagement utilisateur — dernière session il y a {inp.last_login_days_ago}j")
    if inp.nps_score < 20 and motion != PlaybookMotion.RESCUE:
        actions.append("Enquête NPS détaillée — identifier les axes d'amélioration prioritaires")

    return actions


def _build_playbook_steps(motion: PlaybookMotion, stage: LifecycleStage) -> list[str]:
    base: dict[PlaybookMotion, list[str]] = {
        PlaybookMotion.RESCUE: [
            "S1 : Appel d'urgence — diagnostic 360° des problèmes ouverts",
            "S2 : Plan de remédiation formalisé — responsables + dates + KPIs",
            "S3 : Résolution des escalades techniques en moins de 48h",
            "S4 : Check-in hebdomadaire de suivi pendant 4 semaines",
            "S5 : QBR de récupération — valider le retour à la santé",
            "S6 : Revue post-crise — leçons apprises, plan de prévention",
        ],
        PlaybookMotion.ONBOARD: [
            "S1 : Kick-off officiel — plan de succès 90j, parties prenantes identifiées",
            "S2 : Activation technique — intégrations, SSO, migration données",
            "S3 : Formation utilisateurs clés — scénarios métier prioritaires",
            "S4 : Check-in J30 — adoption initiale, blocages levés",
            "S5 : Check-in J60 — extension à d'autres équipes, cas d'usage avancés",
            "S6 : Revue J90 — validation objectifs, passage à la phase adoption",
        ],
        PlaybookMotion.ACCELERATE: [
            "S1 : Audit d'adoption — cartographier les features non utilisées",
            "S2 : Atelier d'activation — session pratique avec utilisateurs finaux",
            "S3 : Partage de best practices — cas d'usage sectoriels similaires",
            "S4 : Suivi hebdomadaire des métriques d'usage pendant 30j",
            "S5 : QBR d'adoption — présenter la progression et fixer les objectifs",
        ],
        PlaybookMotion.EXPAND: [
            "S1 : QBR de valeur — quantifier le ROI réalisé, ouvrir la discussion croissance",
            "S2 : Qualification expansion — identifier les nouveaux cas d'usage ou équipes",
            "S3 : Proposition commerciale — licences / modules / tier supérieur",
            "S4 : Présentation exécutive — ROI + business case expansion",
            "S5 : Négociation et signature — co-construire le plan de déploiement",
            "S6 : Kick-off expansion — reproduire le succès sur le nouveau périmètre",
        ],
        PlaybookMotion.RETAIN: [
            "S1 : QBR de santé — bilan valeur, objectifs année suivante",
            "S2 : Revue des risques identifiés — plan d'action correctif si nécessaire",
            "S3 : Engagement renouvellement — préparer et envoyer la proposition",
            "S4 : Traitement des objections — prix, fonctionnalités, concurrence",
            "S5 : Signature du renouvellement — confirmer les termes et lancer N+1",
        ],
    }
    return base.get(motion, [])


def _build_success_metrics(motion: PlaybookMotion) -> list[str]:
    metrics: dict[PlaybookMotion, list[str]] = {
        PlaybookMotion.RESCUE: [
            "Résolution de 100% des escalades ouvertes sous 48h",
            "Score de santé ≥ 50 dans les 30 jours",
            "NPS ≥ 0 en fin de programme de récupération",
            "Renouvellement sécurisé sans décote",
        ],
        PlaybookMotion.ONBOARD: [
            "100% des utilisateurs clés actifs à J30",
            "≥ 3 cas d'usage métier validés à J60",
            "Score d'adoption ≥ 60 à J90",
            "Champion identifié et engagé avant J15",
        ],
        PlaybookMotion.ACCELERATE: [
            "Features adoptées ≥ 70% sous 60 jours",
            "DAU/MAU ratio ≥ 0.25 sous 45 jours",
            "Score d'adoption ≥ 70 au prochain QBR",
            "Création de 2+ cas d'usage additionnels documentés",
        ],
        PlaybookMotion.EXPAND: [
            "Proposition d'expansion envoyée sous 14 jours",
            "Expansion signée ≥ 15% de l'ARR actuel",
            "NPS ≥ 40 maintenu post-expansion",
            "Nouveau périmètre en production sous 60 jours",
        ],
        PlaybookMotion.RETAIN: [
            "Renouvellement signé ≥ 60 jours avant échéance",
            "Score de santé ≥ 65 maintenu",
            "NPS stable ou en hausse",
            "Zéro escalade non résolue à la date de renouvellement",
        ],
    }
    return metrics.get(motion, [])


class CustomerSuccessPlaybookEngine:
    """Prescribes the right CS motion and playbook steps for each account."""

    def __init__(self) -> None:
        self._results: dict[str, CSPlaybookResult] = {}

    def prescribe(self, inp: CSPlaybookInput) -> CSPlaybookResult:
        health = _overall_health(inp)
        risk = _risk_level(health)
        stage = _lifecycle_stage(inp, health)
        urgency = _renewal_urgency(inp)
        readiness = _expansion_readiness(inp, health)
        motion = _playbook_motion(inp, stage, risk, readiness)
        risks = _build_risks(inp, health, risk)
        actions = _build_actions(inp, motion, urgency, readiness)
        steps = _build_playbook_steps(motion, stage)
        metrics = _build_success_metrics(motion)

        result = CSPlaybookResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            segment=inp.segment,
            arr_eur=inp.arr_eur,
            lifecycle_stage=stage,
            risk_level=risk,
            playbook_motion=motion,
            overall_health_score=health,
            renewal_urgency=urgency,
            expansion_readiness=readiness,
            key_risks=risks,
            immediate_actions=actions,
            playbook_steps=steps,
            success_metrics=metrics,
        )
        self._results[inp.account_id] = result
        return result

    def prescribe_batch(self, inputs: list[CSPlaybookInput]) -> list[CSPlaybookResult]:
        return sorted(
            [self.prescribe(inp) for inp in inputs],
            key=lambda r: r.overall_health_score,
            reverse=True,
        )

    def get(self, account_id: str) -> Optional[CSPlaybookResult]:
        return self._results.get(account_id)

    def all_accounts(self) -> list[CSPlaybookResult]:
        return sorted(self._results.values(), key=lambda r: r.overall_health_score, reverse=True)

    def by_motion(self, motion: PlaybookMotion) -> list[CSPlaybookResult]:
        return [r for r in self.all_accounts() if r.playbook_motion == motion]

    def by_stage(self, stage: LifecycleStage) -> list[CSPlaybookResult]:
        return [r for r in self.all_accounts() if r.lifecycle_stage == stage]

    def by_risk(self, risk: RiskLevel) -> list[CSPlaybookResult]:
        return [r for r in self.all_accounts() if r.risk_level == risk]

    def rescue_accounts(self) -> list[CSPlaybookResult]:
        return self.by_motion(PlaybookMotion.RESCUE)

    def expand_ready(self) -> list[CSPlaybookResult]:
        return [r for r in self.all_accounts() if r.expansion_readiness == "ready"]

    def renewal_urgent(self) -> list[CSPlaybookResult]:
        return [r for r in self.all_accounts() if r.renewal_urgency in ("immediate", "high")]

    def total_arr_at_risk(self) -> float:
        at_risk = [r for r in self._results.values() if r.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)]
        return round(sum(r.arr_eur for r in at_risk), 2)

    def total_arr_expansion_ready(self) -> float:
        return round(sum(r.arr_eur for r in self.expand_ready()), 2)

    def avg_health_score(self) -> float:
        vals = list(self._results.values())
        if not vals:
            return 0.0
        return round(sum(r.overall_health_score for r in vals) / len(vals), 1)

    def summary(self) -> dict:
        all_r = list(self._results.values())
        if not all_r:
            return {
                "total": 0,
                "motion_counts": {},
                "stage_counts": {},
                "risk_counts": {},
                "avg_health_score": 0.0,
                "total_arr_at_risk_eur": 0.0,
                "total_arr_expansion_ready_eur": 0.0,
                "rescue_count": 0,
                "expand_ready_count": 0,
                "renewal_urgent_count": 0,
            }
        motion_counts: dict[str, int] = {}
        stage_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        for r in all_r:
            motion_counts[r.playbook_motion.value] = motion_counts.get(r.playbook_motion.value, 0) + 1
            stage_counts[r.lifecycle_stage.value] = stage_counts.get(r.lifecycle_stage.value, 0) + 1
            risk_counts[r.risk_level.value] = risk_counts.get(r.risk_level.value, 0) + 1
        return {
            "total": len(all_r),
            "motion_counts": motion_counts,
            "stage_counts": stage_counts,
            "risk_counts": risk_counts,
            "avg_health_score": self.avg_health_score(),
            "total_arr_at_risk_eur": self.total_arr_at_risk(),
            "total_arr_expansion_ready_eur": self.total_arr_expansion_ready(),
            "rescue_count": len(self.rescue_accounts()),
            "expand_ready_count": len(self.expand_ready()),
            "renewal_urgent_count": len(self.renewal_urgent()),
        }

    def reset(self) -> None:
        self._results.clear()
