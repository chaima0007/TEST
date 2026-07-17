#!/usr/bin/env python3
"""Database Schema Agent — CaelumSwarm™ Dev Support
Génère et valide les schémas de données Prisma/TypeScript depuis les engines Python.
Assure la cohérence entre les structures de données Python et TypeScript.
"""
import re
import json
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "DatabaseSchemaAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def extract_entity_fields(engine_source: str) -> list[str]:
    """Extrait les noms de champs des entités depuis le code Python."""
    fields = set()
    # Patterns de champs dans les ENTITIES
    key_patterns = re.findall(r'"([a-z_]+)":\s*(?:\d+|"[^"]*"|\[[^\]]*\])', engine_source)
    for key in key_patterns:
        if not key.startswith("id") and len(key) > 2:
            fields.add(key)
    return sorted(list(fields))


def generate_typescript_interface(engine_name: str, fields: list[str]) -> str:
    """Génère une interface TypeScript depuis les champs Python."""
    type_map = {
        "score": "number",
        "index": "number",
        "id": "string",
        "name": "string",
        "level": "string",
        "severity": "string",
        "risk_level": "string",
        "country": "string",
        "description": "string",
        "pattern": "string",
        "timestamp": "string",
    }

    interface_name = "".join(w.capitalize() for w in engine_name.replace("_engine", "").split("_")) + "Entity"
    lines = [f"export interface {interface_name} {{"]

    for field in fields:
        ts_type = "string"
        for key, t in type_map.items():
            if key in field:
                ts_type = t
                break
        lines.append(f"  {field}: {ts_type};")

    lines.append("}")
    return "\n".join(lines)


def generate_prisma_schema(engines: list[Path]) -> str:
    """Génère un schéma Prisma pour stocker les résultats d'engines."""
    models = []

    for engine_path in engines[:5]:  # Limiter à 5 pour l'exemple
        source = engine_path.read_text(encoding="utf-8", errors="ignore")
        engine_name = engine_path.stem
        model_name = "".join(w.capitalize() for w in engine_name.replace("_engine", "").split("_"))

        model = f"""model {model_name}Result {{
  id          String   @id @default(cuid())
  entityName  String
  engineSlug  String   @default("{engine_name.replace("_", "-")}")
  composite   Float
  level       String
  index       Float
  waveNumber  Int
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@index([engineSlug, level])
  @@index([createdAt])
}}"""
        models.append(model)

    schema = """// prisma/schema.prisma — CaelumSwarm™ Auto-généré
// Généré par DatabaseSchemaAgent v""" + VERSION + """

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// ─── Core Models ───────────────────────────────────────────

model EngineRun {{
  id          String   @id @default(cuid())
  engineSlug  String
  waveNumber  Int
  avgComposite Float
  confidence  Float    @default(0.85)
  entityCount Int      @default(8)
  runAt       DateTime @default(now())

  @@index([engineSlug])
  @@index([runAt])
}}

model CSDDDAlert {{
  id          String   @id @default(cuid())
  entityName  String
  engineSlug  String
  alertType   String   // "critique" | "élevé"
  articuleCSDDD String @default("Art.8")
  resolvedAt  DateTime?
  createdAt   DateTime @default(now())

  @@index([engineSlug, alertType])
}}

""" + "\n\n".join(models)

    return schema


def run_schema_agent(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}CaelumSwarm™ Database Schema Agent v{VERSION}{RESET}\n")

    engine_files = sorted((root / "swarm" / "intelligence").glob("*_engine.py"))
    print(f"Analyse de {len(engine_files)} engines pour extraction de schémas...\n")

    # Générer les interfaces TypeScript
    interfaces_dir = root / "lib" / "types"
    interfaces_dir.mkdir(parents=True, exist_ok=True)

    all_interfaces = [
        "// lib/types/engine-entities.ts — Auto-généré par DatabaseSchemaAgent",
        f"// {datetime.now(timezone.utc).strftime('%Y-%m-%d')} | NE PAS MODIFIER MANUELLEMENT",
        "",
        "export interface BaseEntity {",
        "  id: string;",
        "  name: string;",
        "  composite_score: number;",
        "  level: string;",
        "  risk_level?: string;",
        "  severity?: string;",
        "}",
        "",
        "export interface EngineResponse {",
        "  engine: string;",
        "  entities: BaseEntity[];",
        "  avg_composite?: number;",
        "  confidence_score?: number;",
        "  data_sources?: string[];",
        "  critical_alerts?: string[];",
        "}",
        "",
    ]

    generated_interfaces = []
    for engine_path in engine_files[:10]:
        source = engine_path.read_text(encoding="utf-8", errors="ignore")
        fields = extract_entity_fields(source)
        if fields:
            interface = generate_typescript_interface(engine_path.stem, fields)
            all_interfaces.append(interface)
            all_interfaces.append("")
            generated_interfaces.append(engine_path.stem)

    interfaces_file = interfaces_dir / "engine-entities.ts"
    interfaces_file.write_text("\n".join(all_interfaces), encoding="utf-8")
    print(f"  {GREEN}✓{RESET} {interfaces_file} ({len(generated_interfaces)} interfaces)")

    # Générer le schéma Prisma (optionnel)
    prisma_dir = root / "prisma"
    prisma_dir.mkdir(parents=True, exist_ok=True)
    prisma_schema_path = prisma_dir / "schema.prisma"
    if not prisma_schema_path.exists():
        schema_content = generate_prisma_schema(engine_files)
        prisma_schema_path.write_text(schema_content, encoding="utf-8")
        print(f"  {GREEN}✓{RESET} {prisma_schema_path} (schéma Prisma généré)")
    else:
        print(f"  {YELLOW}⚠{RESET} {prisma_schema_path} existe déjà — non écrasé")

    print(f"\n{GREEN}✓ Schémas générés avec succès{RESET}\n")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "interfaces_generated": len(generated_interfaces),
        "interfaces_file": str(interfaces_file),
        "prisma_schema": str(prisma_schema_path),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_schema_agent(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
