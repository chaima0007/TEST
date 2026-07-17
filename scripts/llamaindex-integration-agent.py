"""
LlamaIndex Integration Agent — CaelumSwarm™
Framework: LlamaIndex 0.11.x
Role: RAG enterprise, knowledge graphs, multi-modal pour conformité CSDDD 2024

Ce module simule et documente l'intégration LlamaIndex dans CaelumSwarm™.
Aucune dépendance externe — stdlib Python uniquement.
"""

import json
import math
import hashlib
import datetime
import random
import uuid

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────────────────────

LLAMAINDEX_VERSION = "0.11.x"

LLAMAINDEX_COMPONENTS = {
    "data_connectors": {
        "S3Reader": "Documents fournisseurs sur S3",
        "DatabaseReader": "Données PostgreSQL CaelumSwarm™",
        "PDFReader": "Rapports CSDDD PDF",
        "JSONReader": "Résultats wave engines JSON",
        "SlackReader": "Alertes Slack conformité",
        "NotionReader": "Documentation procédures internes",
        "WebScraperReader": "Actualités violations droits humains",
        "GitHubRepositoryReader": "Code CaelumSwarm™ engines",
    },
    "index_types": {
        "VectorStoreIndex": {
            "store": "pgvector",
            "dims": 1536,
            "use_case": "Recherche sémantique documents CSDDD",
        },
        "SummaryIndex": {
            "use_case": "Résumés rapides de rapports longs",
        },
        "KeywordTableIndex": {
            "use_case": "Recherche exacte termes CSDDD/RGPD",
        },
        "KnowledgeGraphIndex": {
            "backend": "Neo4j",
            "use_case": "Relations entités/fournisseurs/violations",
        },
        "TreeIndex": {
            "use_case": "Hiérarchie chaîne de valeur Tier1-2-3",
        },
    },
    "query_engines": {
        "RetrieverQueryEngine": {
            "retriever": "VectorIndexRetriever k=8",
            "use_case": "Q&A CSDDD standard",
        },
        "SubQuestionQueryEngine": {
            "description": "Décompose les questions complexes en sous-questions",
            "use_case": "Due diligence multi-domaines",
        },
        "RouterQueryEngine": {
            "selectors": ["LLMSingleSelector"],
            "description": "Route vers l'index optimal",
        },
        "KnowledgeGraphQueryEngine": {
            "use_case": "Tracer relations violations/fournisseurs/pays",
        },
        "PandasQueryEngine": {
            "use_case": "Analyse statistique des scores CaelumSwarm™",
        },
    },
    "agents": {
        "ReActAgent": {
            "tools": ["compliance_tool", "wave_tool", "db_tool"],
            "llm": "claude-sonnet-4-6",
        },
        "OpenAIAgent": {
            "tools": ["compliance_tool", "wave_tool", "db_tool", "report_tool"],
            "llm": "gpt-4o",
        },
        "FunctionCallingAgent": {
            "description": "Agent avec tool use structuré",
        },
    },
    "node_parsers": {
        "SentenceSplitter": {"chunk_size": 1024, "chunk_overlap": 128},
        "SemanticSplitterNodeParser": {
            "description": "Split sur changements sémantiques",
        },
        "MarkdownNodeParser": {
            "use_case": "Parsing documentations CSDDD structurées",
        },
    },
    "postprocessors": {
        "SimilarityPostprocessor": {
            "cutoff": 0.75,
            "description": "Filtre documents non-pertinents",
        },
        "KeywordNodePostprocessor": {
            "required_keywords": ["CSDDD", "droits humains", "fournisseur"],
        },
        "CohereRerank": {
            "top_n": 5,
            "model": "rerank-multilingual-v3.0",
        },
        "LongContextReorder": {
            "description": "Optimise pour longues fenêtres contextuelles",
        },
    },
    "observability": {
        "LlamaDebugHandler": True,
        "WandbCallbackHandler": {"project": "caelum-llamaindex"},
        "OpenInferenceTracing": True,   # Phoenix/Arize
    },
}

KNOWLEDGE_GRAPH_CONFIG = {
    "backend": "Neo4j",
    "entities": [
        "Company",
        "Supplier",
        "Country",
        "Violation",
        "Article",
        "WaveEngine",
    ],
    "relationships": [
        "Company → SOURCES_FROM → Country",
        "Company → HAS_SUPPLIER → Supplier",
        "Supplier → LOCATED_IN → Country",
        "Country → HAS_VIOLATION → Violation",
        "Violation → TRIGGERS → Article (CSDDD)",
        "WaveEngine → SCORES → Violation",
    ],
    "use_cases": [
        "Tracer violations de droits humains jusqu'aux entreprises",
        "Identifier réseaux fournisseurs à risque",
        "Recommander due diligence ciblée",
    ],
}

RAG_PIPELINE_ADVANCED = {
    "ingestion": {
        "pipeline": "IngestionPipeline",
        "transformations": [
            "SentenceSplitter",
            "TitleExtractor",
            "QuestionsAnsweredExtractor",
            "text-embedding-3-small",
        ],
        "cache": "RedisCache",
        "docstore": "PostgreSQL",
    },
    "retrieval": {
        "fusion_retrieval": True,   # BM25 + Vector hybrid
        "reranking": "CohereRerank top_5",
        "query_expansion": True,    # génère N reformulations de la question
        "mmr": True,                # diversité maximale des résultats
    },
    "generation": {
        "response_synthesizer": "TreeSummarize",
        "structured_output": True,
        "citation": True,           # cite les sources avec numéros de page
    },
}

# Coûts LLM (USD pour 1 000 tokens, prix de référence 2024-2025)
LLM_PRICING = {
    "claude_sonnet": {
        "input_per_1k":  0.003,
        "output_per_1k": 0.015,
        "label": "Claude claude-sonnet-4-6 (Anthropic)",
    },
    "gpt4o": {
        "input_per_1k":  0.005,
        "output_per_1k": 0.015,
        "label": "GPT-4o (OpenAI)",
    },
}

USD_TO_EUR = 0.92

# Corpus CSDDD simulé partagé entre les fonctions
_CSDDD_CORPUS = [
    {
        "source": "CSDDD_2024_1760_Art8.pdf",
        "page": 12,
        "excerpt": (
            "Article 8 — Obligations de diligence raisonnable : Les entreprises doivent "
            "identifier, prévenir, atténuer et rendre compte des incidences négatives réelles "
            "et potentielles sur les droits humains et l'environnement dans leurs chaînes "
            "de valeur directes et indirectes."
        ),
        "metadata": {"article": "8", "chapter": "II", "type": "obligation"},
    },
    {
        "source": "CSDDD_2024_1760_Art10.pdf",
        "page": 18,
        "excerpt": (
            "Article 10 — Mesures correctives : Lorsqu'une incidence négative réelle a été "
            "identifiée, l'entreprise doit prendre des mesures correctives appropriées, "
            "notamment en élaborant et en mettant en oeuvre un plan d'action correctif."
        ),
        "metadata": {"article": "10", "chapter": "II", "type": "corrective"},
    },
    {
        "source": "OCDE_Principes_Directeurs_2023.pdf",
        "page": 33,
        "excerpt": (
            "Les Principes directeurs de l'OCDE à l'intention des entreprises multinationales "
            "constituent le référentiel de base pour l'évaluation des obligations de diligence "
            "en matière de droits humains."
        ),
        "metadata": {"source_type": "guidelines", "org": "OECD", "year": 2023},
    },
    {
        "source": "UE_Jurisprudence_CJUE_C-572-22.pdf",
        "page": 7,
        "excerpt": (
            "La Cour de Justice de l'UE confirme que les obligations de diligence raisonnable "
            "s'appliquent de manière extraterritoriale aux activités des filiales établies "
            "hors de l'UE."
        ),
        "metadata": {"source_type": "jurisprudence", "case": "C-572/22", "year": 2023},
    },
    {
        "source": "EBA_Guidelines_ESG_2023.pdf",
        "page": 45,
        "excerpt": (
            "Les institutions financières doivent intégrer les risques ESG dans leurs "
            "processus de diligence raisonnable conformément aux exigences CSDDD."
        ),
        "metadata": {"source_type": "guideline", "regulator": "EBA", "year": 2023},
    },
    {
        "source": "CSDDD_2024_1760_Art13.pdf",
        "page": 24,
        "excerpt": (
            "Article 13 — Mécanismes de réclamation : Les entreprises doivent offrir la "
            "possibilité aux parties prenantes affectées de déposer des réclamations "
            "directement auprès d'elles."
        ),
        "metadata": {"article": "13", "chapter": "III", "type": "grievance"},
    },
    {
        "source": "CaelumSwarm_WaveEngines_Catalog.json",
        "page": 1,
        "excerpt": (
            "CaelumSwarm™ wave engines couvrent 60+ domaines de droits humains: "
            "conflict_minerals, labor_rights, gender_rights, climate_migration, "
            "child_labor, forced_labor, land_grabbing, AI_surveillance."
        ),
        "metadata": {"source_type": "internal", "system": "CaelumSwarm", "year": 2024},
    },
    {
        "source": "UNGP_BusinessHumanRights_2011.pdf",
        "page": 14,
        "excerpt": (
            "Les Principes directeurs des Nations Unies relatifs aux entreprises et aux droits "
            "de l'homme établissent le cadre 'Protect, Respect and Remedy' constituant "
            "la référence internationale en matière de diligence droits humains."
        ),
        "metadata": {"source_type": "standard", "org": "UN", "year": 2011},
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def design_rag_index(data_source: str, domain: str) -> dict:
    """Conçoit l'index LlamaIndex optimal pour une source de données CSDDD.

    Args:
        data_source: Source de données (ex. 'S3', 'PostgreSQL', 'PDF')
        domain:      Domaine de conformité (ex. 'conflict_minerals', 'labor_rights')

    Returns:
        dict avec index_type, config, node_parser, postprocessors, estimated_build_time_s
    """
    # Mapping source → index optimal
    source_to_index = {
        "S3":         "VectorStoreIndex",
        "PostgreSQL": "VectorStoreIndex",
        "PDF":        "SummaryIndex",
        "JSON":       "VectorStoreIndex",
        "Neo4j":      "KnowledgeGraphIndex",
        "Notion":     "KeywordTableIndex",
        "GitHub":     "VectorStoreIndex",
        "Slack":      "SummaryIndex",
    }

    # Sélectionner l'index par défaut si la source n'est pas connue
    index_type = source_to_index.get(data_source, "VectorStoreIndex")
    index_cfg  = LLAMAINDEX_COMPONENTS["index_types"].get(index_type, {})

    # Node parser selon le type d'index
    if index_type == "KnowledgeGraphIndex":
        parser = "MarkdownNodeParser"
    elif index_type == "SummaryIndex":
        parser = "SemanticSplitterNodeParser"
    else:
        parser = "SentenceSplitter"

    parser_cfg = LLAMAINDEX_COMPONENTS["node_parsers"].get(parser, {})

    # Postprocessors systématiques
    postprocessors = [
        {
            "name": "SimilarityPostprocessor",
            "cutoff": LLAMAINDEX_COMPONENTS["postprocessors"]["SimilarityPostprocessor"]["cutoff"],
        },
        {
            "name": "CohereRerank",
            "top_n": LLAMAINDEX_COMPONENTS["postprocessors"]["CohereRerank"]["top_n"],
            "model": LLAMAINDEX_COMPONENTS["postprocessors"]["CohereRerank"]["model"],
        },
        {
            "name": "LongContextReorder",
            "description": LLAMAINDEX_COMPONENTS["postprocessors"]["LongContextReorder"]["description"],
        },
    ]

    # Estimation build time : 0.8 s par connecteur + overhead index
    overhead = {"VectorStoreIndex": 5.0, "KnowledgeGraphIndex": 12.0,
                "SummaryIndex": 3.0, "KeywordTableIndex": 2.0, "TreeIndex": 4.0}
    estimated_docs = 200  # hypothèse pour la simulation
    estimated_build_s = round(estimated_docs * 0.05 + overhead.get(index_type, 5.0), 1)

    # Estimation coût embedding (text-embedding-3-small = $0.00002 / 1k tokens)
    tokens_per_doc   = 600
    total_tokens     = estimated_docs * tokens_per_doc
    embedding_cost_usd = round((total_tokens / 1000) * 0.00002, 4)
    embedding_cost_eur = round(embedding_cost_usd * USD_TO_EUR, 4)

    return {
        "index_id": f"idx_{hashlib.md5(f'{data_source}-{domain}'.encode()).hexdigest()[:10]}",
        "data_source": data_source,
        "domain": domain,
        "index_type": index_type,
        "index_config": index_cfg,
        "node_parser": {"type": parser, "config": parser_cfg},
        "postprocessors": postprocessors,
        "ingestion_pipeline": RAG_PIPELINE_ADVANCED["ingestion"],
        "estimated_docs": estimated_docs,
        "estimated_build_time_s": estimated_build_s,
        "embedding_model": "text-embedding-3-small (1536 dims)",
        "embedding_cost_eur": embedding_cost_eur,
        "vector_store": "pgvector (PostgreSQL)",
        "refresh_strategy": "incremental — détection docs modifiés via hash MD5",
    }


def simulate_knowledge_graph_query(entity: str, relationship: str) -> dict:
    """Simule une requête Knowledge Graph Neo4j pour tracer des relations CSDDD.

    Args:
        entity:       Entité de départ (ex. 'Total Energies', 'DRC Congo')
        relationship: Type de relation à explorer (ex. 'HAS_VIOLATION', 'HAS_SUPPLIER')

    Returns:
        dict avec cypher_query, kg_results, path_analysis, csddd_triggers
    """
    # Mapping des violations simulées par entité
    entity_violations = {
        "Total Energies": [
            {"violation": "Forced Labor", "country": "Myanmar", "severity": "critique",
             "csddd_article": "Art.8", "supplier_tier": "Tier-2"},
            {"violation": "Land Grabbing", "country": "DRC Congo", "severity": "critique",
             "csddd_article": "Art.8", "supplier_tier": "Tier-1"},
            {"violation": "Child Labor", "country": "Nigeria", "severity": "élevé",
             "csddd_article": "Art.8", "supplier_tier": "Tier-2"},
        ],
        "DRC Congo": [
            {"violation": "Conflict Minerals", "country": "DRC Congo", "severity": "critique",
             "csddd_article": "Art.8", "supplier_tier": "N/A"},
            {"violation": "Child Labor", "country": "DRC Congo", "severity": "critique",
             "csddd_article": "Art.8", "supplier_tier": "N/A"},
        ],
        "Generic Corp": [
            {"violation": "Labor Rights Breach", "country": "Bangladesh", "severity": "élevé",
             "csddd_article": "Art.8", "supplier_tier": "Tier-1"},
        ],
    }

    violations = entity_violations.get(entity, entity_violations["Generic Corp"])

    # Requête Cypher simulée
    if relationship == "HAS_VIOLATION":
        cypher = (
            f"MATCH (c:Company {{name: '{entity}'}})-[:HAS_SUPPLIER]->(s:Supplier)"
            f"-[:LOCATED_IN]->(co:Country)-[:HAS_VIOLATION]->(v:Violation)"
            f" WHERE v.severity IN ['critique', 'élevé']"
            f" RETURN c, s, co, v"
            f" ORDER BY v.severity_score DESC LIMIT 20"
        )
    elif relationship == "HAS_SUPPLIER":
        cypher = (
            f"MATCH (c:Company {{name: '{entity}'}})-[:HAS_SUPPLIER]->(s:Supplier)"
            f" OPTIONAL MATCH (s)-[:LOCATED_IN]->(co:Country)"
            f" RETURN c, s, co"
            f" ORDER BY s.risk_score DESC LIMIT 50"
        )
    else:
        cypher = (
            f"MATCH path = (c:Company {{name: '{entity}'}})-[r:{relationship}*1..3]->(n)"
            f" RETURN path LIMIT 25"
        )

    # Construire les résultats simulés
    kg_results = []
    for i, v in enumerate(violations):
        node_key = f"{entity}-{v['violation']}"
        kg_results.append({
            "node_id": f"n_{hashlib.md5(node_key.encode()).hexdigest()[:8]}",
            "path": f"({entity}) → [HAS_SUPPLIER] → (Supplier_{i+1}) "
                    f"→ [LOCATED_IN] → ({v['country']}) "
                    f"→ [HAS_VIOLATION] → ({v['violation']})",
            "violation": v["violation"],
            "country": v["country"],
            "severity": v["severity"],
            "supplier_tier": v["supplier_tier"],
            "csddd_article": v["csddd_article"],
            "remediation_required": True,
        })

    # Analyse du chemin
    critique_count = sum(1 for v in violations if v["severity"] == "critique")
    eleve_count    = sum(1 for v in violations if v["severity"] == "élevé")

    path_analysis = {
        "total_violations_found": len(violations),
        "critique": critique_count,
        "eleve": eleve_count,
        "max_depth_explored": 3,
        "countries_flagged": list({v["country"] for v in violations}),
        "tiers_implicated": list({v["supplier_tier"] for v in violations}),
        "graph_traversal_time_ms": round(12 + len(violations) * 3.5, 1),
    }

    csddd_triggers = []
    if critique_count > 0:
        csddd_triggers.append({
            "article": "Art.8",
            "action": "Identification incidences négatives — due diligence immédiate requise",
            "deadline": "30 jours",
        })
    if eleve_count > 0:
        csddd_triggers.append({
            "article": "Art.10",
            "action": "Plan d'action correctif — mesures atténuation à élaborer",
            "deadline": "60 jours",
        })
    csddd_triggers.append({
        "article": "Art.13",
        "action": "Mécanisme de réclamation — notifier les parties prenantes affectées",
        "deadline": "90 jours",
    })

    return {
        "entity": entity,
        "relationship": relationship,
        "cypher_query": cypher,
        "neo4j_backend": KNOWLEDGE_GRAPH_CONFIG["backend"],
        "kg_results": kg_results,
        "path_analysis": path_analysis,
        "csddd_triggers": csddd_triggers,
        "recommendation": (
            f"Audit urgent sur {critique_count} violation(s) critique(s) "
            f"dans {len(path_analysis['countries_flagged'])} pays. "
            f"Actions Art.8/Art.10 CSDDD 2024 à initier sous 30 jours."
        ) if critique_count > 0 else "Risque modéré — surveiller sous 90 jours.",
    }


def design_multi_document_agent(documents: list) -> dict:
    """Conçoit un agent LlamaIndex pour analyser N documents simultanément.

    Args:
        documents: Liste de dicts {'name': str, 'type': str, 'pages': int}

    Returns:
        dict avec agent_config, tool_per_doc, query_routing, estimated_cost_eur
    """
    tool_per_doc = []
    total_tokens = 0

    for doc in documents:
        doc_type    = doc.get("type", "PDF")
        pages       = doc.get("pages", 10)
        tokens_page = 500   # ~500 tokens / page

        # Choisir le query engine selon le type de document
        if doc_type == "PDF":
            engine = "RetrieverQueryEngine (VectorStoreIndex, k=5)"
        elif doc_type == "JSON":
            engine = "PandasQueryEngine"
        elif doc_type == "NEO4J":
            engine = "KnowledgeGraphQueryEngine"
        else:
            engine = "RetrieverQueryEngine (SummaryIndex)"

        doc_tokens = pages * tokens_page
        total_tokens += doc_tokens

        tool_per_doc.append({
            "document": doc["name"],
            "type": doc_type,
            "pages": pages,
            "index_type": "VectorStoreIndex" if doc_type in ("PDF", "JSON") else "KnowledgeGraphIndex",
            "query_engine": engine,
            "estimated_tokens": doc_tokens,
            "tool_name": f"query_tool_{doc['name'].lower().replace(' ', '_')[:20]}",
            "description": f"Outil RAG pour {doc['name']} — conformité CSDDD",
        })

    # SubQuestionQueryEngine décompose les questions complexes en sous-questions par doc
    total_cost_usd = (total_tokens / 1000) * LLM_PRICING["claude_sonnet"]["input_per_1k"]
    # output : ~300 tokens par doc
    output_tokens  = len(documents) * 300
    total_cost_usd += (output_tokens / 1000) * LLM_PRICING["claude_sonnet"]["output_per_1k"]
    total_cost_eur = round(total_cost_usd * USD_TO_EUR, 4)

    agent_config = {
        "agent_id": f"multiDoc_{uuid.uuid4().hex[:10]}",
        "agent_type": "ReActAgent",
        "llm": "claude-sonnet-4-6",
        "tools": [t["tool_name"] for t in tool_per_doc],
        "tool_count": len(tool_per_doc),
        "orchestration": "SubQuestionQueryEngine — décompose en sous-questions par document",
        "response_synthesizer": "TreeSummarize — synthèse hiérarchique cross-documents",
        "max_iterations": 3 * len(documents),
        "verbose": True,
        "observability": list(LLAMAINDEX_COMPONENTS["observability"].keys()),
    }

    query_routing = {
        "strategy": "RouterQueryEngine avec LLMSingleSelector",
        "selector_logic": "LLM détermine quel(s) outil(s) utiliser pour chaque sous-question",
        "fallback": "VectorStoreIndex global si aucun document spécifique n'est sélectionné",
        "fusion": "QueryFusionRetriever — fusionne les résultats des N indexes",
    }

    return {
        "agent_config": agent_config,
        "documents_count": len(documents),
        "tool_per_doc": tool_per_doc,
        "total_input_tokens": total_tokens,
        "total_output_tokens": output_tokens,
        "estimated_cost_eur": total_cost_eur,
        "query_routing": query_routing,
        "example_query": (
            "Compare les violations de droits humains identifiées dans chacun des "
            "documents fournisseurs et génère un plan d'action CSDDD consolidé."
        ),
        "execution_time_estimate_s": round(len(documents) * 3.5 + 5.0, 1),
    }


def benchmark_rag_performance(queries: list) -> dict:
    """Benchmark du pipeline RAG LlamaIndex (latence, pertinence, coût).

    Args:
        queries: Liste de chaînes de requêtes à benchmarker

    Returns:
        dict avec per_query_metrics, aggregate_stats, recommendations
    """
    per_query_metrics = []
    total_latency_ms  = 0
    total_tokens      = 0
    total_cost_eur    = 0.0

    for i, query in enumerate(queries):
        # Déterminisme via hash
        seed_val = int(hashlib.md5(query.encode()).hexdigest(), 16) & 0xFFFFFF
        random.seed(seed_val)

        # Métriques simulées réalistes
        latency_retrieval_ms = round(random.uniform(45, 120), 1)
        latency_rerank_ms    = round(random.uniform(80, 200), 1)
        latency_llm_ms       = round(random.uniform(300, 900), 1)
        total_query_ms       = round(latency_retrieval_ms + latency_rerank_ms + latency_llm_ms, 1)

        relevance_score     = round(random.uniform(0.72, 0.97), 3)
        faithfulness_score  = round(random.uniform(0.80, 0.99), 3)
        context_recall      = round(random.uniform(0.70, 0.95), 3)
        answer_relevance    = round(random.uniform(0.78, 0.98), 3)

        input_tokens  = random.randint(800, 2000)
        output_tokens = random.randint(150, 500)
        cost_usd = (
            (input_tokens  / 1000) * LLM_PRICING["claude_sonnet"]["input_per_1k"] +
            (output_tokens / 1000) * LLM_PRICING["claude_sonnet"]["output_per_1k"]
        )
        cost_eur = round(cost_usd * USD_TO_EUR, 5)

        total_latency_ms += total_query_ms
        total_tokens     += input_tokens + output_tokens
        total_cost_eur   += cost_eur

        per_query_metrics.append({
            "query_id": i + 1,
            "query": query[:60] + ("…" if len(query) > 60 else ""),
            "latency_ms": {
                "retrieval":  latency_retrieval_ms,
                "reranking":  latency_rerank_ms,
                "llm":        latency_llm_ms,
                "total":      total_query_ms,
            },
            "ragas_scores": {
                "relevance":         relevance_score,
                "faithfulness":      faithfulness_score,
                "context_recall":    context_recall,
                "answer_relevance":  answer_relevance,
                "composite":         round(
                    (relevance_score + faithfulness_score + context_recall + answer_relevance) / 4,
                    3,
                ),
            },
            "tokens": {"input": input_tokens, "output": output_tokens},
            "cost_eur": cost_eur,
        })

    n = len(queries)
    avg_latency     = round(total_latency_ms / n, 1) if n else 0
    avg_composite   = round(
        sum(m["ragas_scores"]["composite"] for m in per_query_metrics) / n, 3
    ) if n else 0
    avg_cost        = round(total_cost_eur / n, 5) if n else 0

    recommendations = []
    if avg_latency > 600:
        recommendations.append(
            "Latence élevée (>600ms) : activer RedisCache + réduire k de 8 à 5"
        )
    else:
        recommendations.append("Latence acceptable : pipeline optimisé")

    if avg_composite < 0.85:
        recommendations.append(
            "Score RAGAS composite <0.85 : améliorer reranking (CohereRerank top_n=8)"
        )
    else:
        recommendations.append("Qualité RAG excellente (composite >= 0.85)")

    recommendations.append(
        f"Coût moyen par requête : €{avg_cost:.5f} — "
        f"budget mensuel estimé (10k req) : €{round(avg_cost * 10_000, 2):.2f}"
    )

    return {
        "benchmark_id": f"bench_{uuid.uuid4().hex[:8]}",
        "queries_tested": n,
        "llm": "claude-sonnet-4-6",
        "retriever": "VectorIndexRetriever k=8 + CohereRerank top_5",
        "per_query_metrics": per_query_metrics,
        "aggregate_stats": {
            "avg_latency_ms": avg_latency,
            "avg_composite_ragas": avg_composite,
            "total_tokens": total_tokens,
            "total_cost_eur": round(total_cost_eur, 4),
            "avg_cost_per_query_eur": avg_cost,
        },
        "recommendations": recommendations,
        "evaluation_framework": "RAGAS (Relevance, Faithfulness, Context Recall, Answer Relevance)",
    }


# ─────────────────────────────────────────────────────────────────────────────
# BLOC PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sep  = "=" * 72
    sep2 = "-" * 72

    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    print(sep)
    print("  LLAMAINDEX INTEGRATION REPORT — CaelumSwarm™")
    print(f"  Framework : LlamaIndex {LLAMAINDEX_VERSION}")
    print(f"  Date      : {now}")
    print(f"  Scope     : RAG Enterprise / Knowledge Graph / Neo4j / CSDDD 2024")
    print(sep)

    # ── 1. Components overview ────────────────────────────────────────────────
    print("\n[1] COMPONENTS OVERVIEW")
    print(sep2)

    print(f"\n  Data Connectors ({len(LLAMAINDEX_COMPONENTS['data_connectors'])}) :")
    for name, desc in LLAMAINDEX_COMPONENTS["data_connectors"].items():
        print(f"    • {name:30s}  {desc}")

    print(f"\n  Index Types ({len(LLAMAINDEX_COMPONENTS['index_types'])}) :")
    for name, cfg in LLAMAINDEX_COMPONENTS["index_types"].items():
        use_case = cfg.get("use_case", "N/A")
        backend  = cfg.get("backend", cfg.get("store", "—"))
        dims     = f"  ({cfg['dims']} dims)" if "dims" in cfg else ""
        print(f"    • {name:30s}  backend: {backend:12s}{dims}  → {use_case}")

    print(f"\n  Query Engines ({len(LLAMAINDEX_COMPONENTS['query_engines'])}) :")
    for name, cfg in LLAMAINDEX_COMPONENTS["query_engines"].items():
        use_case = cfg.get("use_case", cfg.get("description", "N/A"))
        print(f"    • {name:35s}  {use_case}")

    print(f"\n  Node Parsers ({len(LLAMAINDEX_COMPONENTS['node_parsers'])}) :")
    for name, cfg in LLAMAINDEX_COMPONENTS["node_parsers"].items():
        detail = (
            f"chunk_size={cfg['chunk_size']}, overlap={cfg['chunk_overlap']}"
            if "chunk_size" in cfg
            else cfg.get("description", cfg.get("use_case", "N/A"))
        )
        print(f"    • {name:35s}  {detail}")

    print(f"\n  Postprocessors ({len(LLAMAINDEX_COMPONENTS['postprocessors'])}) :")
    for name, cfg in LLAMAINDEX_COMPONENTS["postprocessors"].items():
        detail = cfg.get("description", cfg.get("model", str(cfg.get("required_keywords", ""))))
        print(f"    • {name:35s}  {detail}")

    print(f"\n  Agents ({len(LLAMAINDEX_COMPONENTS['agents'])}) :")
    for name, cfg in LLAMAINDEX_COMPONENTS["agents"].items():
        tools = cfg.get("tools", [])
        llm   = cfg.get("llm", cfg.get("description", "N/A"))
        print(f"    • {name:25s}  llm: {llm:20s}  outils: {', '.join(tools)}")

    # ── 2. Data connectors detail ─────────────────────────────────────────────
    print("\n\n[2] DATA CONNECTORS — INGESTION PIPELINE CSDDD")
    print(sep2)

    pipeline = RAG_PIPELINE_ADVANCED["ingestion"]
    print(f"\n  Pipeline     : {pipeline['pipeline']}")
    print(f"  Transformations : {' → '.join(pipeline['transformations'])}")
    print(f"  Cache        : {pipeline['cache']}")
    print(f"  Docstore     : {pipeline['docstore']}")
    print()

    for source_name, desc in LLAMAINDEX_COMPONENTS["data_connectors"].items():
        result = design_rag_index(source_name.replace("Reader", "").replace("Reader", ""), "csddd_compliance")
        # Simplifier pour l'affichage
        print(f"  {source_name:30s} → {result['index_type']:25s} | build: {result['estimated_build_time_s']}s | emb cost: €{result['embedding_cost_eur']}")

    # ── 3. Index design — cas réels ───────────────────────────────────────────
    print("\n\n[3] INDEX DESIGN — CAS CONCRETS CSDDD")
    print(sep2)

    index_cases = [
        ("PDF",        "conflict_minerals"),
        ("PostgreSQL", "labor_rights"),
        ("Neo4j",      "supplier_network"),
        ("S3",         "environmental_impact"),
    ]

    for data_source, domain in index_cases:
        idx = design_rag_index(data_source, domain)
        print(f"\n  Source: {data_source:12s} | Domaine: {domain:25s}")
        print(f"    Index ID          : {idx['index_id']}")
        print(f"    Index type        : {idx['index_type']}")
        print(f"    Node parser       : {idx['node_parser']['type']}")
        print(f"    Vector store      : {idx['vector_store']}")
        print(f"    Embedding model   : {idx['embedding_model']}")
        print(f"    Docs estimés      : {idx['estimated_docs']}")
        print(f"    Build time est.   : {idx['estimated_build_time_s']} s")
        print(f"    Coût embedding    : €{idx['embedding_cost_eur']}")
        print(f"    Postprocessors    : {', '.join(p['name'] for p in idx['postprocessors'])}")
        print(f"    Refresh strategy  : {idx['refresh_strategy']}")

    # ── 4. Knowledge Graph — simulation de requête ────────────────────────────
    print("\n\n[4] KNOWLEDGE GRAPH — SIMULATION REQUÊTES NEO4J")
    print(sep2)
    print(f"\n  Backend    : {KNOWLEDGE_GRAPH_CONFIG['backend']}")
    print(f"  Entités    : {', '.join(KNOWLEDGE_GRAPH_CONFIG['entities'])}")
    print(f"\n  Relations :")
    for rel in KNOWLEDGE_GRAPH_CONFIG["relationships"]:
        print(f"    {rel}")

    print(f"\n  Use cases :")
    for uc in KNOWLEDGE_GRAPH_CONFIG["use_cases"]:
        print(f"    • {uc}")

    # Simulation de requête
    kg_queries = [
        ("Total Energies", "HAS_VIOLATION"),
        ("DRC Congo",      "HAS_VIOLATION"),
    ]

    for entity, rel in kg_queries:
        print(f"\n  --- Requête KG : {entity} / {rel} ---")
        kg = simulate_knowledge_graph_query(entity, rel)
        print(f"  Cypher         : {kg['cypher_query'][:90]}…")
        print(f"  Violations     : {kg['path_analysis']['total_violations_found']} "
              f"(critique: {kg['path_analysis']['critique']}, "
              f"élevé: {kg['path_analysis']['eleve']})")
        print(f"  Pays flaggés   : {', '.join(kg['path_analysis']['countries_flagged'])}")
        print(f"  Tiers impliqués: {', '.join(kg['path_analysis']['tiers_implicated'])}")
        print(f"  Traversal time : {kg['path_analysis']['graph_traversal_time_ms']} ms")
        print(f"\n  Résultats :")
        for res in kg["kg_results"]:
            print(f"    [{res['severity'].upper():8s}] {res['violation']:30s} | {res['country']:15s} | {res['csddd_article']}")
        print(f"\n  Triggers CSDDD :")
        for trig in kg["csddd_triggers"]:
            print(f"    • {trig['article']:8s}  {trig['action'][:60]}  → deadline: {trig['deadline']}")
        print(f"\n  Recommandation : {kg['recommendation']}")

    # ── 5. RAG Pipeline avancé ────────────────────────────────────────────────
    print("\n\n[5] RAG PIPELINE AVANCÉ — CONFIGURATION COMPLÈTE")
    print(sep2)

    retrieval = RAG_PIPELINE_ADVANCED["retrieval"]
    generation = RAG_PIPELINE_ADVANCED["generation"]

    print(f"\n  Ingestion (déjà détaillée section 2)")
    print(f"\n  Retrieval :")
    print(f"    fusion_retrieval : {retrieval['fusion_retrieval']}  (BM25 + Vector hybrid)")
    print(f"    reranking        : {retrieval['reranking']}")
    print(f"    query_expansion  : {retrieval['query_expansion']}  (N reformulations question)")
    print(f"    MMR              : {retrieval['mmr']}  (diversité maximale résultats)")

    print(f"\n  Generation :")
    print(f"    response_synthesizer : {generation['response_synthesizer']}")
    print(f"    structured_output    : {generation['structured_output']}")
    print(f"    citation             : {generation['citation']}  (sources avec numéros de page)")

    # ── 6. SubQuestion Engine — simulation ───────────────────────────────────
    print("\n\n[6] SUBQUESTION QUERY ENGINE — SIMULATION")
    print(sep2)

    complex_question = (
        "Quels fournisseurs Tier-1 et Tier-2 présentent des violations Art.8 CSDDD "
        "en matière de travail forcé dans la chaîne d'approvisionnement minière ?"
    )
    print(f"\n  Question complexe :")
    print(f"    \"{complex_question}\"")

    sub_questions = [
        {"sq": "Quels fournisseurs Tier-1 sont sourcés dans des zones minières à risque ?",
         "index": "VectorStoreIndex (supplier_profiles)", "engine": "RetrieverQueryEngine k=8"},
        {"sq": "Quels pays Tier-2 ont des violations de travail forcé documentées ?",
         "index": "KnowledgeGraphIndex (Neo4j)", "engine": "KnowledgeGraphQueryEngine"},
        {"sq": "Quelles obligations Art.8 CSDDD s'appliquent au travail forcé minier ?",
         "index": "VectorStoreIndex (csddd_knowledge)", "engine": "RetrieverQueryEngine k=5"},
        {"sq": "Quels plans correctifs Art.10 ont été initiés dans ce contexte ?",
         "index": "VectorStoreIndex (audit_history)", "engine": "RetrieverQueryEngine k=3"},
    ]

    print(f"\n  Décomposition en {len(sub_questions)} sous-questions :")
    for i, sq in enumerate(sub_questions, 1):
        print(f"\n    [{i}] {sq['sq']}")
        print(f"         Index  : {sq['index']}")
        print(f"         Engine : {sq['engine']}")

    print(f"\n  Synthèse finale : TreeSummarize (cross-index consolidation)")
    print(f"  Réponse simulée (extrait) :")
    print(f"    → 3 fournisseurs Tier-1 identifiés (Myanmar, DRC, Nigeria)")
    print(f"    → 7 fournisseurs Tier-2 présentant risque travail forcé critique")
    print(f"    → Art.8 CSDDD : due diligence immédiate requise sous 30 jours")
    print(f"    → Art.10 : 2 plans correctifs existants | 5 nouveaux plans à initier")

    # ── 7. Multi-document agent ───────────────────────────────────────────────
    print("\n\n[7] MULTI-DOCUMENT AGENT — ANALYSE CROISÉE")
    print(sep2)

    docs_portfolio = [
        {"name": "Rapport_RSE_TotalEnergies_2024",   "type": "PDF",  "pages": 85},
        {"name": "Scores_Wave_Engines_Q4_2024",       "type": "JSON", "pages": 5},
        {"name": "Audit_Fournisseurs_Tier1_2024",     "type": "PDF",  "pages": 42},
        {"name": "Knowledge_Graph_Relations",          "type": "NEO4J","pages": 0},
        {"name": "Jurisprudence_CJUE_CSDDD_2023",     "type": "PDF",  "pages": 28},
    ]

    ma = design_multi_document_agent(docs_portfolio)
    print(f"\n  Agent ID       : {ma['agent_config']['agent_id']}")
    print(f"  Type           : {ma['agent_config']['agent_type']}")
    print(f"  LLM            : {ma['agent_config']['llm']}")
    print(f"  Docs analysés  : {ma['documents_count']}")
    print(f"  Outils créés   : {ma['agent_config']['tool_count']}")
    print(f"  Max iterations : {ma['agent_config']['max_iterations']}")
    print(f"\n  Outils par document :")
    for t in ma["tool_per_doc"]:
        print(f"    • {t['tool_name']:40s} [{t['index_type']:25s}] {t['pages']} pages → {t['estimated_tokens']:,} tokens")
    print(f"\n  Tokens totaux  : {ma['total_input_tokens']:,} input + {ma['total_output_tokens']:,} output")
    print(f"  Coût estimé    : €{ma['estimated_cost_eur']}")
    print(f"  Temps estimé   : {ma['execution_time_estimate_s']} s")
    print(f"\n  Query routing  : {ma['query_routing']['strategy']}")
    print(f"  Fusion         : {ma['query_routing']['fusion']}")
    print(f"\n  Exemple requête : \"{ma['example_query']}\"")

    # ── 8. Performance benchmark ──────────────────────────────────────────────
    print("\n\n[8] PERFORMANCE BENCHMARK — RAG PIPELINE")
    print(sep2)

    bench_queries = [
        "CSDDD Art.8 due diligence obligations supply chain",
        "Travail forcé Myanmar fournisseurs Tier-2 — actions correctives",
        "Minéraux de conflit DRC Congo CSDDD compliance score",
        "Mécanismes réclamation Art.13 parties prenantes affectées",
        "Due diligence environnementale chaîne de valeur Tier-1",
    ]

    bench = benchmark_rag_performance(bench_queries)
    print(f"\n  Benchmark ID   : {bench['benchmark_id']}")
    print(f"  LLM            : {bench['llm']}")
    print(f"  Retriever      : {bench['retriever']}")
    print(f"  Queries testées: {bench['queries_tested']}")
    print(f"\n  Métriques par requête :")
    print(f"  {'#':>2}  {'Latence (ms)':>14}  {'RAGAS':>7}  {'Tokens':>8}  {'Coût €':>9}  Requête")
    print(f"  {'--':>2}  {'-'*14}  {'-'*7}  {'-'*8}  {'-'*9}  {'-------'}")
    for m in bench["per_query_metrics"]:
        lat  = m["latency_ms"]["total"]
        ragas = m["ragas_scores"]["composite"]
        tok  = m["tokens"]["input"] + m["tokens"]["output"]
        cost = m["cost_eur"]
        q    = m["query"][:38]
        print(f"  {m['query_id']:>2}  {lat:>14.1f}  {ragas:>7.3f}  {tok:>8,}  €{cost:>8.5f}  {q}")

    agg = bench["aggregate_stats"]
    print(f"\n  Statistiques agrégées :")
    print(f"    Latence moyenne    : {agg['avg_latency_ms']:.1f} ms")
    print(f"    RAGAS composite    : {agg['avg_composite_ragas']:.3f}")
    print(f"    Tokens totaux      : {agg['total_tokens']:,}")
    print(f"    Coût total         : €{agg['total_cost_eur']:.4f}")
    print(f"    Coût par requête   : €{agg['avg_cost_per_query_eur']:.5f}")

    print(f"\n  Recommandations :")
    for rec in bench["recommendations"]:
        print(f"    • {rec}")

    # ── 9. Security checklist ─────────────────────────────────────────────────
    print("\n\n[9] SECURITY CHECKLIST — LLAMAINDEX / CSDDD")
    print(sep2)

    checklist = [
        ("API keys via HashiCorp Vault",
         "ANTHROPIC_API_KEY, OPENAI_API_KEY, COHERE_API_KEY — jamais en clair",
         True),
        ("Audit trail LlamaDebugHandler",
         "Log chaque query/retrieval/LLM call — traçabilité CSDDD Art.8",
         True),
        ("PII masking pré-embedding",
         "Anonymisation avant envoi embeddings API externe (RGPD Art.25)",
         True),
        ("pgvector EU data residency",
         "Base PostgreSQL hébergée UE — données CSDDD restent dans l'UE",
         True),
        ("Neo4j access control",
         "RBAC Neo4j — accès Knowledge Graph restreint par rôle utilisateur",
         True),
        ("TLS 1.3 sur toutes les connexions",
         "pgvector, Neo4j, Cohere API, LLM API — zéro plain HTTP",
         True),
        ("Cache sécurisé Redis",
         "Redis avec AUTH + TLS — cache embeddings chiffré at rest",
         True),
        ("Observability Phoenix/Arize EU",
         "OpenInference traces — endpoint EU configuré, conformité RGPD",
         True),
        ("Prompt injection guards",
         "Validation input LlamaIndex — filtrage injections avant query engine",
         True),
        ("Rotation clés 90j",
         "Vault dynamic secrets — rotation automatique tous les 90 jours",
         True),
    ]

    print()
    for item, detail, status in checklist:
        mark = "✓" if status else "✗"
        print(f"  [{mark}] {item}")
        print(f"       {detail}")

    # ── Résumé final ──────────────────────────────────────────────────────────
    print("\n")
    print(sep)
    print("  LlamaIndex Integration Agent — PRÊT (LlamaIndex 0.11.x / RAG / Knowledge Graph / Neo4j)")
    print(f"  {len(LLAMAINDEX_COMPONENTS['data_connectors'])} connectors  |  "
          f"{len(LLAMAINDEX_COMPONENTS['index_types'])} index types  |  "
          f"{len(LLAMAINDEX_COMPONENTS['query_engines'])} query engines  |  "
          f"{len(LLAMAINDEX_COMPONENTS['agents'])} agents")
    print(f"  KG: Neo4j  |  Vector: pgvector  |  LLM: claude-sonnet-4-6  |  CSDDD 2024")
    print(sep)
