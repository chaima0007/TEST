export const meta = {
  name: 'panel-couple',
  description:
    "Panel d'experts (produit, relation, sécurité, critique) qui audite le MVP « Nous » et produit un backlog priorisé avec un incrément à construire.",
  whenToUse:
    "Pour faire évoluer l'app couple « Nous » : audit multi-perspectives du code réel puis synthèse priorisée.",
  phases: [
    { title: 'Audit', detail: 'chaque expert audite le code réel du MVP' },
    { title: 'Synthèse', detail: 'backlog priorisé + incrément recommandé' },
  ],
}

const AUDIT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['expert', 'findings', 'proposals'],
  properties: {
    expert: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['title', 'severity', 'area'],
        properties: {
          title: { type: 'string' },
          severity: { type: 'string', enum: ['faible', 'moyen', 'fort'] },
          area: { type: 'string' },
          file: { type: 'string' },
        },
      },
    },
    proposals: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['title', 'why', 'impact', 'effort'],
        properties: {
          title: { type: 'string' },
          why: { type: 'string' },
          impact: { type: 'integer', minimum: 1, maximum: 5 },
          effort: { type: 'integer', minimum: 1, maximum: 5 },
        },
      },
    },
  },
}

const BACKLOG_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['topPick', 'backlog', 'guardrails'],
  properties: {
    topPick: {
      type: 'object',
      additionalProperties: false,
      required: ['title', 'why', 'plan'],
      properties: {
        title: { type: 'string' },
        why: { type: 'string' },
        plan: { type: 'array', items: { type: 'string' } },
      },
    },
    backlog: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['title', 'rationale', 'impact', 'effort', 'priority'],
        properties: {
          title: { type: 'string' },
          rationale: { type: 'string' },
          impact: { type: 'integer', minimum: 1, maximum: 5 },
          effort: { type: 'integer', minimum: 1, maximum: 5 },
          priority: { type: 'string', enum: ['P0', 'P1', 'P2'] },
        },
      },
    },
    guardrails: { type: 'array', items: { type: 'string' } },
  },
}

const EXPERTS = [
  {
    type: 'produit-ux',
    label: 'produit-ux',
    prompt:
      "Audite le MVP « Nous » sous l'angle PRODUIT / UX. Lis app/, components/, lib/. " +
      "Identifie frictions, manques d'utilisabilité mobile, valeur en solo. " +
      'Renvoie tes constats et 3 à 5 propositions concrètes chiffrées (impact 1-5, effort 1-5).',
  },
  {
    type: 'relation-communication',
    label: 'relation',
    prompt:
      "Audite le MVP « Nous » sous l'angle RELATION / COMMUNICATION. Lis lib/rituals.ts, lib/nvc.ts, lib/content.ts, lib/cycle.ts. " +
      "Vérifie l'exactitude et l'attribution des approches (CNV, Gottman, FRIES), les formulations, les garde-fous (non médical/thérapeutique). " +
      'Renvoie tes constats et 3 à 5 propositions concrètes chiffrées (impact 1-5, effort 1-5).',
  },
  {
    type: 'securite-privacy',
    label: 'securite',
    prompt:
      "Audite le MVP « Nous » sous l'angle SÉCURITÉ / VIE PRIVÉE. Lis next.config.ts, lib/store.tsx, lib/seed.ts. " +
      'Vérifie le local-first, la CSP, la robustesse du stockage, l\'absence de fuite ou de secret. ' +
      'Renvoie tes constats et 3 à 5 propositions concrètes chiffrées (impact 1-5, effort 1-5).',
  },
  {
    type: 'critique-produit',
    label: 'critique',
    prompt:
      "Audite le MVP « Nous » en AVOCAT DU DIABLE. Lis le code réel. " +
      "Dis ce qui rend l'app oubliable, ce qui la rendrait inévitable, et les risques éthiques (surveillance du partenaire, culpabilisation, mésusage du cycle). " +
      'Renvoie tes constats et 3 à 5 propositions concrètes chiffrées (impact 1-5, effort 1-5).',
  },
]

phase('Audit')
const audits = await parallel(
  EXPERTS.map((e) => () =>
    agent(e.prompt, {
      agentType: e.type,
      label: e.label,
      phase: 'Audit',
      schema: AUDIT_SCHEMA,
    }),
  ),
)

const valid = audits.filter(Boolean)
log(`${valid.length}/${EXPERTS.length} audits reçus`)

phase('Synthèse')
const synthesis = await agent(
  'Tu es le SYNTHÉTISEUR du panel « Nous ». Voici les audits des experts (JSON) :\n\n' +
    JSON.stringify(valid, null, 2) +
    "\n\nProduis un backlog priorisé (P0/P1/P2) en fusionnant et dédupliquant les propositions, " +
    "en tenant compte de l'impact et de l'effort. Choisis UN incrément à construire maintenant " +
    "(topPick) : celui qui maximise la valeur pour un MVP démontrable et éthique, avec un plan " +
    "d'implémentation en étapes courtes. Liste aussi les garde-fous éthiques non négociables.",
  { label: 'synthèse', phase: 'Synthèse', schema: BACKLOG_SCHEMA },
)

return synthesis
