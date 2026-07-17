# Note de Divulgation d'Invention — CAE-INV-2025-004

**CONFIDENTIEL — PROPRIÉTÉ EXCLUSIVE CAELUM PARTNERS SPRL**

---

| Champ | Valeur |
|-------|--------|
| **Référence interne** | CAE-INV-2025-004 |
| **Nom commercial** | CaelumPulse™ |
| **Date de divulgation** | 21 juin 2025 |
| **Inventrice** | Chaima Mhadbi |
| **Titulaire** | Caelum Partners SPRL, Bruxelles, Belgique |

---

## Titre

**Interface de visualisation en temps réel de la distribution géographique des risques de violations des droits humains avec représentation circulaire normalisée par domaine thématique**

---

## Description

**Composant GaugeRing brevetable :**
```
viewBox="0 0 88 88" · r=36 · cx=44 · cy=44 · strokeWidth=8
offset = circumference - (value/100) × circumference
transform="rotate(-90 44 44)"  // départ à 12h
```

**Innovation :**
- Jauge circulaire SVG normalisée universellement comparable entre domaines
- Palette de couleurs sémantique : rouge (critique) → orange (élevé) → jaune (modéré) → vert (faible)
- Bascule automatique mock/live via d.payload??d sans refactorisation frontend
- Architecture sans état partagé (pas de useCallback/useMemo) → performance maximale
- Internationalisation native : labels français, entités multilingues

**Distribution visuelle brevetable :**
- Barres proportionnelles par niveau de risque avec largeur = (count/total)×100%
- Identification entité par entity_id mono-espace + nom complet + score /10 + badge niveau

---

## Revendications Préliminaires

1. Composant graphique de jauge circulaire SVG pour la représentation normalisée d'un score de risque [0–100].
2. Interface de tableau de bord comprenant ladite jauge et une distribution visuelle des niveaux de risque.
3. Architecture de bascule transparente entre données simulées et données temps-réel dans une interface de visualisation.

---

*Document rédigé le 21 juin 2025 — Caelum Partners SPRL*
