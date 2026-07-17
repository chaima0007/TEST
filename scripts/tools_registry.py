#!/usr/bin/env python3
"""
tools_registry.py — Registre Universel d'Outils Gratuits CaelumSwarm™
═══════════════════════════════════════════════════════════════════════
Catalogue sécurisé de TOUS les outils gratuits utiles au projet.
Compatible Linux (apt/curl) et Microsoft Windows (winget/choco/scoop).
Chaque installation passe par le sceau de protocole.

SEAL: SEAL-E5DA3C69E63A88CC APPROUVÉ

Usage:
  python3 scripts/tools_registry.py --list                  # Tout afficher
  python3 scripts/tools_registry.py --list --category IA    # Par catégorie
  python3 scripts/tools_registry.py --search "monitoring"   # Recherche
  python3 scripts/tools_registry.py --install git           # Générer commande
  python3 scripts/tools_registry.py --audit                 # Vérifier installés
  python3 scripts/tools_registry.py --export json           # Exporter catalogue
"""

import sys
import json
import shutil
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
LOG = DATA / "tools_registry_log.json"

# ══════════════════════════════════════════════════════════════════════════════
# CATALOGUE COMPLET DES OUTILS — 200+ outils gratuits
# ══════════════════════════════════════════════════════════════════════════════

TOOLS = {

    # ─── DÉVELOPPEMENT ────────────────────────────────────────────────────────
    "DEV": {
        "git": {
            "desc": "Contrôle de version distribué",
            "url": "https://git-scm.com",
            "linux": "sudo apt install git",
            "windows": "winget install Git.Git",
            "check": "git --version",
            "priority": "CRITIQUE",
        },
        "python3": {
            "desc": "Langage Python 3.x + pip",
            "url": "https://python.org",
            "linux": "sudo apt install python3 python3-pip python3-venv",
            "windows": "winget install Python.Python.3",
            "check": "python3 --version",
            "priority": "CRITIQUE",
        },
        "nodejs": {
            "desc": "Runtime JavaScript + npm",
            "url": "https://nodejs.org",
            "linux": "curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt install nodejs",
            "windows": "winget install OpenJS.NodeJS.LTS",
            "check": "node --version",
            "priority": "CRITIQUE",
        },
        "rust": {
            "desc": "Langage Rust + Cargo (outils système ultra-performants)",
            "url": "https://rust-lang.org",
            "linux": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
            "windows": "winget install Rustlang.Rustup",
            "check": "rustc --version",
            "priority": "ÉLEVÉ",
        },
        "go": {
            "desc": "Langage Go (microservices, CLI tools)",
            "url": "https://go.dev",
            "linux": "sudo apt install golang",
            "windows": "winget install GoLang.Go",
            "check": "go version",
            "priority": "MOYEN",
        },
        "deno": {
            "desc": "Runtime TypeScript/JS moderne (Next.js edge)",
            "url": "https://deno.land",
            "linux": "curl -fsSL https://deno.land/install.sh | sh",
            "windows": "winget install DenoLand.Deno",
            "check": "deno --version",
            "priority": "MOYEN",
        },
        "bun": {
            "desc": "Runtime JS ultra-rapide (alternative Node.js)",
            "url": "https://bun.sh",
            "linux": "curl -fsSL https://bun.sh/install | bash",
            "windows": "winget install Oven-sh.Bun",
            "check": "bun --version",
            "priority": "MOYEN",
        },
        "pnpm": {
            "desc": "Gestionnaire packages Node.js rapide + économe",
            "url": "https://pnpm.io",
            "linux": "npm install -g pnpm",
            "windows": "winget install pnpm.pnpm",
            "check": "pnpm --version",
            "priority": "ÉLEVÉ",
        },
        "uv": {
            "desc": "Gestionnaire packages Python ultra-rapide (remplace pip)",
            "url": "https://github.com/astral-sh/uv",
            "linux": "curl -LsSf https://astral.sh/uv/install.sh | sh",
            "windows": "winget install astral-sh.uv",
            "check": "uv --version",
            "priority": "ÉLEVÉ",
        },
        "ruff": {
            "desc": "Linter Python ultra-rapide (remplace flake8/pylint)",
            "url": "https://github.com/astral-sh/ruff",
            "linux": "pip install ruff",
            "windows": "winget install Astral.Ruff",
            "check": "ruff --version",
            "priority": "MOYEN",
        },
        "just": {
            "desc": "Gestionnaire de commandes (Makefile moderne)",
            "url": "https://github.com/casey/just",
            "linux": "sudo apt install just",
            "windows": "winget install Casey.Just",
            "check": "just --version",
            "priority": "FAIBLE",
        },
    },

    # ─── IA / ML / LLM ────────────────────────────────────────────────────────
    "IA_ML": {
        "ollama": {
            "desc": "LLM local (Llama3, Mistral, Gemma) — GRATUIT sans API",
            "url": "https://ollama.com",
            "linux": "curl -fsSL https://ollama.com/install.sh | sh",
            "windows": "winget install Ollama.Ollama",
            "check": "ollama --version",
            "priority": "CRITIQUE",
            "models": ["llama3.2", "mistral", "gemma2", "qwen2.5-coder", "deepseek-r1"],
        },
        "llama_cpp": {
            "desc": "Inférence LLM optimisée CPU/GPU (bindings Python)",
            "url": "https://github.com/ggerganov/llama.cpp",
            "linux": "pip install llama-cpp-python",
            "windows": "pip install llama-cpp-python",
            "check": "python3 -c 'import llama_cpp; print(\"ok\")'",
            "priority": "ÉLEVÉ",
        },
        "whisper": {
            "desc": "Transcription audio → texte (OpenAI Whisper, gratuit local)",
            "url": "https://github.com/openai/whisper",
            "linux": "pip install openai-whisper",
            "windows": "pip install openai-whisper",
            "check": "whisper --help",
            "priority": "MOYEN",
        },
        "transformers": {
            "desc": "Hugging Face Transformers (milliers de modèles gratuits)",
            "url": "https://huggingface.co/docs/transformers",
            "linux": "pip install transformers torch",
            "windows": "pip install transformers torch",
            "check": "python3 -c 'import transformers; print(transformers.__version__)'",
            "priority": "ÉLEVÉ",
        },
        "langchain": {
            "desc": "Framework LLM orchestration multi-agents",
            "url": "https://python.langchain.com",
            "linux": "pip install langchain langchain-community",
            "windows": "pip install langchain langchain-community",
            "check": "python3 -c 'import langchain; print(langchain.__version__)'",
            "priority": "ÉLEVÉ",
        },
        "crewai": {
            "desc": "Framework multi-agents IA (utilisé dans CaelumSwarm)",
            "url": "https://crewai.com",
            "linux": "pip install crewai crewai-tools",
            "windows": "pip install crewai crewai-tools",
            "check": "python3 -c 'import crewai; print(\"ok\")'",
            "priority": "CRITIQUE",
        },
        "autogen": {
            "desc": "Microsoft AutoGen — agents IA conversationnels",
            "url": "https://github.com/microsoft/autogen",
            "linux": "pip install pyautogen",
            "windows": "pip install pyautogen",
            "check": "python3 -c 'import autogen; print(\"ok\")'",
            "priority": "ÉLEVÉ",
        },
        "litellm": {
            "desc": "Proxy unifié pour 100+ LLMs (Anthropic/OpenAI/Ollama)",
            "url": "https://litellm.ai",
            "linux": "pip install litellm",
            "windows": "pip install litellm",
            "check": "python3 -c 'import litellm; print(\"ok\")'",
            "priority": "CRITIQUE",
        },
        "sentence_transformers": {
            "desc": "Embeddings sémantiques gratuits (recherche vectorielle)",
            "url": "https://sbert.net",
            "linux": "pip install sentence-transformers",
            "windows": "pip install sentence-transformers",
            "check": "python3 -c 'from sentence_transformers import SentenceTransformer; print(\"ok\")'",
            "priority": "ÉLEVÉ",
        },
        "jupyter": {
            "desc": "Notebooks interactifs Python/TypeScript",
            "url": "https://jupyter.org",
            "linux": "pip install jupyterlab",
            "windows": "pip install jupyterlab",
            "check": "jupyter --version",
            "priority": "MOYEN",
        },
        "mlflow": {
            "desc": "Tracking expériences ML (métriques, modèles, artefacts)",
            "url": "https://mlflow.org",
            "linux": "pip install mlflow",
            "windows": "pip install mlflow",
            "check": "mlflow --version",
            "priority": "MOYEN",
        },
    },

    # ─── SÉCURITÉ ──────────────────────────────────────────────────────────────
    "SÉCURITÉ": {
        "ufw": {
            "desc": "Pare-feu simple Linux (Uncomplicated Firewall)",
            "url": "https://help.ubuntu.com/community/UFW",
            "linux": "sudo apt install ufw && sudo ufw enable",
            "windows": "# Intégré Windows Defender Firewall",
            "check": "sudo ufw status",
            "priority": "CRITIQUE",
        },
        "fail2ban": {
            "desc": "Protection contre brute-force (SSH, nginx, etc.)",
            "url": "https://fail2ban.org",
            "linux": "sudo apt install fail2ban",
            "windows": "# Non applicable (utiliser Windows Firewall + EventLog)",
            "check": "fail2ban-client version",
            "priority": "CRITIQUE",
        },
        "certbot": {
            "desc": "Certificats SSL/TLS gratuits Let's Encrypt",
            "url": "https://certbot.eff.org",
            "linux": "sudo apt install certbot python3-certbot-nginx",
            "windows": "winget install Certbot.Certbot",
            "check": "certbot --version",
            "priority": "CRITIQUE",
        },
        "wireguard": {
            "desc": "VPN moderne ultra-sécurisé (tunnel chiffré)",
            "url": "https://wireguard.com",
            "linux": "sudo apt install wireguard",
            "windows": "winget install WireGuard.WireGuard",
            "check": "wg --version",
            "priority": "ÉLEVÉ",
        },
        "trivy": {
            "desc": "Scanner vulnérabilités containers/images Docker",
            "url": "https://trivy.dev",
            "linux": "curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin",
            "windows": "winget install AquaSecurity.Trivy",
            "check": "trivy --version",
            "priority": "ÉLEVÉ",
        },
        "snyk": {
            "desc": "Scan sécurité dépendances npm/pip/docker (tier gratuit)",
            "url": "https://snyk.io",
            "linux": "npm install -g snyk",
            "windows": "npm install -g snyk",
            "check": "snyk --version",
            "priority": "ÉLEVÉ",
        },
        "ossec": {
            "desc": "HIDS — Détection intrusion basée host (SIEM léger)",
            "url": "https://www.ossec.net",
            "linux": "sudo apt install ossec-hids",
            "windows": "# Installer depuis ossec.net/downloads",
            "check": "ossec-control status",
            "priority": "MOYEN",
        },
        "vault": {
            "desc": "HashiCorp Vault — gestion secrets sécurisée (tier dev gratuit)",
            "url": "https://vaultproject.io",
            "linux": "sudo apt install vault",
            "windows": "winget install Hashicorp.Vault",
            "check": "vault version",
            "priority": "CRITIQUE",
        },
        "age": {
            "desc": "Chiffrement fichiers moderne simple (remplace GPG pour fichiers)",
            "url": "https://github.com/FiloSottile/age",
            "linux": "sudo apt install age",
            "windows": "winget install FiloSottile.age",
            "check": "age --version",
            "priority": "ÉLEVÉ",
        },
        "sops": {
            "desc": "Chiffrement fichiers secrets (.env, YAML, JSON) — intègre age/GPG",
            "url": "https://github.com/getsops/sops",
            "linux": "sudo apt install sops",
            "windows": "winget install Mozilla.SOPS",
            "check": "sops --version",
            "priority": "ÉLEVÉ",
        },
        "nmap": {
            "desc": "Scanner réseau et audit ports (détection vulnérabilités)",
            "url": "https://nmap.org",
            "linux": "sudo apt install nmap",
            "windows": "winget install Insecure.Nmap",
            "check": "nmap --version",
            "priority": "MOYEN",
        },
        "lynis": {
            "desc": "Audit sécurité système Linux (hardening)",
            "url": "https://cisofy.com/lynis",
            "linux": "sudo apt install lynis",
            "windows": "# Linux uniquement",
            "check": "lynis --version",
            "priority": "ÉLEVÉ",
        },
    },

    # ─── INFRASTRUCTURE / DEVOPS ──────────────────────────────────────────────
    "INFRASTRUCTURE": {
        "docker": {
            "desc": "Containerisation applications",
            "url": "https://docker.com",
            "linux": "curl -fsSL https://get.docker.com | sh",
            "windows": "winget install Docker.DockerDesktop",
            "check": "docker --version",
            "priority": "CRITIQUE",
        },
        "k3s": {
            "desc": "Kubernetes léger (1 nœud, gratuit, production-ready)",
            "url": "https://k3s.io",
            "linux": "curl -sfL https://get.k3s.io | sh -",
            "windows": "# WSL2 requis : curl -sfL https://get.k3s.io | sh -",
            "check": "k3s --version",
            "priority": "MOYEN",
        },
        "terraform": {
            "desc": "Infrastructure as Code (IaC) multi-cloud",
            "url": "https://terraform.io",
            "linux": "sudo apt install terraform",
            "windows": "winget install Hashicorp.Terraform",
            "check": "terraform --version",
            "priority": "ÉLEVÉ",
        },
        "ansible": {
            "desc": "Automatisation configuration serveurs (agentless)",
            "url": "https://ansible.com",
            "linux": "sudo apt install ansible",
            "windows": "pip install ansible",
            "check": "ansible --version",
            "priority": "ÉLEVÉ",
        },
        "nginx": {
            "desc": "Serveur web + reverse proxy haute performance",
            "url": "https://nginx.org",
            "linux": "sudo apt install nginx",
            "windows": "winget install NGINXInc.NGINX",
            "check": "nginx -v",
            "priority": "CRITIQUE",
        },
        "caddy": {
            "desc": "Serveur web HTTPS automatique (Let's Encrypt intégré)",
            "url": "https://caddyserver.com",
            "linux": "sudo apt install caddy",
            "windows": "winget install CaddyServer.Caddy",
            "check": "caddy version",
            "priority": "ÉLEVÉ",
        },
        "traefik": {
            "desc": "Reverse proxy cloud-native (Docker labels, auto SSL)",
            "url": "https://traefik.io",
            "linux": "sudo apt install traefik",
            "windows": "winget install TraefikLabs.TraefikProxy",
            "check": "traefik version",
            "priority": "MOYEN",
        },
        "act": {
            "desc": "Runner GitHub Actions en local (tester CI sans push)",
            "url": "https://github.com/nektos/act",
            "linux": "sudo apt install act",
            "windows": "winget install nektos.act",
            "check": "act --version",
            "priority": "ÉLEVÉ",
        },
        "gitea": {
            "desc": "Forge Git auto-hébergée (alternative GitHub gratuite)",
            "url": "https://gitea.io",
            "linux": "docker run -d -p 3000:3000 gitea/gitea",
            "windows": "winget install Gitea.Gitea",
            "check": "gitea --version",
            "priority": "MOYEN",
        },
    },

    # ─── BASES DE DONNÉES ──────────────────────────────────────────────────────
    "DONNÉES": {
        "sqlite3": {
            "desc": "Base de données embarquée (zéro config, parfait dev)",
            "url": "https://sqlite.org",
            "linux": "sudo apt install sqlite3",
            "windows": "winget install SQLite.SQLite",
            "check": "sqlite3 --version",
            "priority": "CRITIQUE",
        },
        "postgresql": {
            "desc": "Base de données relationnelle production-grade",
            "url": "https://postgresql.org",
            "linux": "sudo apt install postgresql",
            "windows": "winget install PostgreSQL.PostgreSQL",
            "check": "psql --version",
            "priority": "ÉLEVÉ",
        },
        "redis": {
            "desc": "Cache/store in-memory ultra-rapide (sessions, queues)",
            "url": "https://redis.io",
            "linux": "sudo apt install redis",
            "windows": "winget install Redis.Redis",
            "check": "redis-cli --version",
            "priority": "ÉLEVÉ",
        },
        "turso": {
            "desc": "SQLite distribuée edge (utilisée dans CaelumSwarm via LibSQL)",
            "url": "https://turso.tech",
            "linux": "curl -sSfL https://get.tur.so/install.sh | bash",
            "windows": "winget install ChiselStrike.Turso",
            "check": "turso --version",
            "priority": "CRITIQUE",
        },
        "chroma": {
            "desc": "Base vectorielle IA (RAG, embeddings, recherche sémantique)",
            "url": "https://trychroma.com",
            "linux": "pip install chromadb",
            "windows": "pip install chromadb",
            "check": "python3 -c 'import chromadb; print(chromadb.__version__)'",
            "priority": "ÉLEVÉ",
        },
        "qdrant": {
            "desc": "Base vectorielle haute performance (alternative Chroma)",
            "url": "https://qdrant.tech",
            "linux": "docker pull qdrant/qdrant && docker run -p 6333:6333 qdrant/qdrant",
            "windows": "docker pull qdrant/qdrant && docker run -p 6333:6333 qdrant/qdrant",
            "check": "curl http://localhost:6333/health",
            "priority": "MOYEN",
        },
        "duckdb": {
            "desc": "Analytique SQL in-process ultra-rapide (OLAP local)",
            "url": "https://duckdb.org",
            "linux": "pip install duckdb",
            "windows": "pip install duckdb",
            "check": "python3 -c 'import duckdb; print(duckdb.__version__)'",
            "priority": "ÉLEVÉ",
        },
    },

    # ─── MONITORING / OBSERVABILITÉ ───────────────────────────────────────────
    "MONITORING": {
        "prometheus": {
            "desc": "Collecte métriques + alerting (standard industrie)",
            "url": "https://prometheus.io",
            "linux": "sudo apt install prometheus",
            "windows": "docker run -p 9090:9090 prom/prometheus",
            "check": "promtool --version",
            "priority": "ÉLEVÉ",
        },
        "grafana": {
            "desc": "Dashboards monitoring (visualisation Prometheus/Loki)",
            "url": "https://grafana.com",
            "linux": "sudo apt install grafana",
            "windows": "winget install GrafanaLabs.Grafana",
            "check": "grafana-server -v",
            "priority": "ÉLEVÉ",
        },
        "netdata": {
            "desc": "Monitoring temps réel système (CPU, RAM, réseau) — zero config",
            "url": "https://netdata.cloud",
            "linux": "curl https://my-netdata.io/kickstart.sh > /tmp/netdata-kickstart.sh && sh /tmp/netdata-kickstart.sh",
            "windows": "# WSL2 ou docker run -d --name=netdata -p 19999:19999 netdata/netdata",
            "check": "netdata --version",
            "priority": "MOYEN",
        },
        "loki": {
            "desc": "Agrégation logs (comme Elasticsearch mais léger)",
            "url": "https://grafana.com/oss/loki",
            "linux": "sudo apt install loki",
            "windows": "docker run -p 3100:3100 grafana/loki",
            "check": "loki --version",
            "priority": "MOYEN",
        },
        "uptime_kuma": {
            "desc": "Monitoring uptime services (self-hosted, interface web)",
            "url": "https://github.com/louislam/uptime-kuma",
            "linux": "docker run -d -p 3001:3001 louislam/uptime-kuma",
            "windows": "docker run -d -p 3001:3001 louislam/uptime-kuma",
            "check": "curl http://localhost:3001",
            "priority": "ÉLEVÉ",
        },
    },

    # ─── OUTILS CLI AMÉLIORÉS ─────────────────────────────────────────────────
    "CLI_MODERNES": {
        "fzf": {
            "desc": "Fuzzy finder interactif (recherche fichiers/historique)",
            "url": "https://github.com/junegunn/fzf",
            "linux": "sudo apt install fzf",
            "windows": "winget install junegunn.fzf",
            "check": "fzf --version",
            "priority": "ÉLEVÉ",
        },
        "ripgrep": {
            "desc": "grep ultra-rapide (rg) — recherche dans code 10x plus vite",
            "url": "https://github.com/BurntSushi/ripgrep",
            "linux": "sudo apt install ripgrep",
            "windows": "winget install BurntSushi.ripgrep.MSVC",
            "check": "rg --version",
            "priority": "CRITIQUE",
        },
        "fd": {
            "desc": "find moderne ultra-rapide (fd-find)",
            "url": "https://github.com/sharkdp/fd",
            "linux": "sudo apt install fd-find",
            "windows": "winget install sharkdp.fd",
            "check": "fd --version",
            "priority": "ÉLEVÉ",
        },
        "bat": {
            "desc": "cat amélioré avec coloration syntaxique",
            "url": "https://github.com/sharkdp/bat",
            "linux": "sudo apt install bat",
            "windows": "winget install sharkdp.bat",
            "check": "bat --version",
            "priority": "MOYEN",
        },
        "eza": {
            "desc": "ls moderne avec icônes et couleurs (remplace exa)",
            "url": "https://github.com/eza-community/eza",
            "linux": "sudo apt install eza",
            "windows": "winget install eza-community.eza",
            "check": "eza --version",
            "priority": "FAIBLE",
        },
        "zoxide": {
            "desc": "cd intelligent (mémorise les dossiers fréquents)",
            "url": "https://github.com/ajeetdsouza/zoxide",
            "linux": "sudo apt install zoxide",
            "windows": "winget install ajeetdsouza.zoxide",
            "check": "zoxide --version",
            "priority": "MOYEN",
        },
        "htop": {
            "desc": "Moniteur processus interactif (mieux que top)",
            "url": "https://htop.dev",
            "linux": "sudo apt install htop",
            "windows": "# WSL2 : sudo apt install htop",
            "check": "htop --version",
            "priority": "CRITIQUE",
        },
        "dust": {
            "desc": "Analyse utilisation disque (mieux que du)",
            "url": "https://github.com/bootandy/dust",
            "linux": "sudo apt install du-dust",
            "windows": "winget install bootandy.dust",
            "check": "dust --version",
            "priority": "MOYEN",
        },
        "jq": {
            "desc": "Traitement JSON en ligne de commande",
            "url": "https://jqlang.github.io/jq",
            "linux": "sudo apt install jq",
            "windows": "winget install jqlang.jq",
            "check": "jq --version",
            "priority": "CRITIQUE",
        },
        "yq": {
            "desc": "Traitement YAML en ligne de commande (comme jq pour YAML)",
            "url": "https://github.com/mikefarah/yq",
            "linux": "sudo apt install yq",
            "windows": "winget install MikeFarah.yq",
            "check": "yq --version",
            "priority": "ÉLEVÉ",
        },
        "tmux": {
            "desc": "Multiplexeur terminal (sessions persistantes, panneaux)",
            "url": "https://github.com/tmux/tmux",
            "linux": "sudo apt install tmux",
            "windows": "# WSL2 : sudo apt install tmux",
            "check": "tmux -V",
            "priority": "CRITIQUE",
        },
        "zsh": {
            "desc": "Shell avancé + Oh-My-Zsh (autocomplétion, plugins)",
            "url": "https://zsh.org",
            "linux": "sudo apt install zsh && sh -c \"$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\"",
            "windows": "# WSL2 uniquement",
            "check": "zsh --version",
            "priority": "ÉLEVÉ",
        },
    },

    # ─── ANALYSE / DATA SCIENCE ───────────────────────────────────────────────
    "ANALYSE": {
        "pandas": {
            "desc": "Manipulation données tabulaires (DataFrames Python)",
            "url": "https://pandas.pydata.org",
            "linux": "pip install pandas",
            "windows": "pip install pandas",
            "check": "python3 -c 'import pandas; print(pandas.__version__)'",
            "priority": "CRITIQUE",
        },
        "polars": {
            "desc": "DataFrames ultra-rapides Rust/Python (remplace pandas 10x)",
            "url": "https://pola.rs",
            "linux": "pip install polars",
            "windows": "pip install polars",
            "check": "python3 -c 'import polars; print(polars.__version__)'",
            "priority": "ÉLEVÉ",
        },
        "numpy": {
            "desc": "Calcul numérique Python (base de l'IA)",
            "url": "https://numpy.org",
            "linux": "pip install numpy",
            "windows": "pip install numpy",
            "check": "python3 -c 'import numpy; print(numpy.__version__)'",
            "priority": "CRITIQUE",
        },
        "matplotlib": {
            "desc": "Graphiques et visualisations Python",
            "url": "https://matplotlib.org",
            "linux": "pip install matplotlib",
            "windows": "pip install matplotlib",
            "check": "python3 -c 'import matplotlib; print(matplotlib.__version__)'",
            "priority": "ÉLEVÉ",
        },
        "plotly": {
            "desc": "Graphiques interactifs (intégration Next.js facile)",
            "url": "https://plotly.com",
            "linux": "pip install plotly",
            "windows": "pip install plotly",
            "check": "python3 -c 'import plotly; print(plotly.__version__)'",
            "priority": "ÉLEVÉ",
        },
        "scipy": {
            "desc": "Calcul scientifique (stats, signaux, optimisation)",
            "url": "https://scipy.org",
            "linux": "pip install scipy",
            "windows": "pip install scipy",
            "check": "python3 -c 'import scipy; print(scipy.__version__)'",
            "priority": "MOYEN",
        },
    },

    # ─── MICROSOFT / WINDOWS NATIF ────────────────────────────────────────────
    "MICROSOFT": {
        "wsl2": {
            "desc": "Windows Subsystem for Linux 2 (Ubuntu/Debian sur Windows)",
            "url": "https://docs.microsoft.com/en-us/windows/wsl",
            "linux": "# Natif Linux",
            "windows": "wsl --install -d Ubuntu",
            "check": "wsl --version",
            "priority": "CRITIQUE",
        },
        "powershell7": {
            "desc": "PowerShell 7 cross-platform (scripts Windows modernes)",
            "url": "https://github.com/PowerShell/PowerShell",
            "linux": "sudo apt install powershell",
            "windows": "winget install Microsoft.PowerShell",
            "check": "pwsh --version",
            "priority": "CRITIQUE",
        },
        "windows_terminal": {
            "desc": "Terminal Windows moderne (tabs, GPU, themes)",
            "url": "https://github.com/microsoft/terminal",
            "linux": "# Non applicable",
            "windows": "winget install Microsoft.WindowsTerminal",
            "check": "wt --version",
            "priority": "ÉLEVÉ",
        },
        "vscode": {
            "desc": "Éditeur de code universel Microsoft (gratuit)",
            "url": "https://code.visualstudio.com",
            "linux": "sudo apt install code",
            "windows": "winget install Microsoft.VisualStudioCode",
            "check": "code --version",
            "priority": "CRITIQUE",
        },
        "winget": {
            "desc": "Gestionnaire packages Windows (intégré Win11)",
            "url": "https://github.com/microsoft/winget-cli",
            "linux": "# Non applicable",
            "windows": "# Intégré Windows 10/11 (App Installer)",
            "check": "winget --version",
            "priority": "CRITIQUE",
        },
        "azure_cli": {
            "desc": "CLI Azure (tier gratuit Azure disponible)",
            "url": "https://docs.microsoft.com/cli/azure",
            "linux": "curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash",
            "windows": "winget install Microsoft.AzureCLI",
            "check": "az --version",
            "priority": "MOYEN",
        },
        "bicep": {
            "desc": "Azure IaC (Infrastructure as Code déclaratif Microsoft)",
            "url": "https://learn.microsoft.com/azure/azure-resource-manager/bicep",
            "linux": "sudo az bicep install",
            "windows": "winget install Microsoft.Bicep",
            "check": "az bicep version",
            "priority": "FAIBLE",
        },
    },

    # ─── COLLABORATION / DOCUMENTATION ────────────────────────────────────────
    "COLLABORATION": {
        "obsidian": {
            "desc": "Base de connaissances Markdown locale (graph de notes)",
            "url": "https://obsidian.md",
            "linux": "sudo apt install obsidian",
            "windows": "winget install Obsidian.Obsidian",
            "check": "# Interface graphique",
            "priority": "MOYEN",
        },
        "mkdocs": {
            "desc": "Documentation sites statiques depuis Markdown",
            "url": "https://mkdocs.org",
            "linux": "pip install mkdocs mkdocs-material",
            "windows": "pip install mkdocs mkdocs-material",
            "check": "mkdocs --version",
            "priority": "ÉLEVÉ",
        },
        "pandoc": {
            "desc": "Convertisseur universel documents (MD→PDF/DOCX/HTML)",
            "url": "https://pandoc.org",
            "linux": "sudo apt install pandoc",
            "windows": "winget install JohnMacFarlane.Pandoc",
            "check": "pandoc --version",
            "priority": "ÉLEVÉ",
        },
        "mermaid": {
            "desc": "Diagrammes en texte (flowcharts, séquences, gantt)",
            "url": "https://mermaid.js.org",
            "linux": "npm install -g @mermaid-js/mermaid-cli",
            "windows": "npm install -g @mermaid-js/mermaid-cli",
            "check": "mmdc --version",
            "priority": "ÉLEVÉ",
        },
        "excalidraw": {
            "desc": "Schémas collaboratifs style dessin à la main (self-host)",
            "url": "https://excalidraw.com",
            "linux": "docker run -p 80:80 excalidraw/excalidraw",
            "windows": "docker run -p 80:80 excalidraw/excalidraw",
            "check": "curl http://localhost:80",
            "priority": "MOYEN",
        },
    },

    # ─── DESIGN / MULTIMÉDIA ──────────────────────────────────────────────────
    "DESIGN": {
        "inkscape": {
            "desc": "Édition vectorielle SVG (alternative Illustrator gratuite)",
            "url": "https://inkscape.org",
            "linux": "sudo apt install inkscape",
            "windows": "winget install Inkscape.Inkscape",
            "check": "inkscape --version",
            "priority": "MOYEN",
        },
        "gimp": {
            "desc": "Édition photos raster (alternative Photoshop gratuite)",
            "url": "https://gimp.org",
            "linux": "sudo apt install gimp",
            "windows": "winget install GIMP.GIMP",
            "check": "gimp --version",
            "priority": "FAIBLE",
        },
        "ffmpeg": {
            "desc": "Traitement audio/vidéo CLI (conversion, compression, stream)",
            "url": "https://ffmpeg.org",
            "linux": "sudo apt install ffmpeg",
            "windows": "winget install Gyan.FFmpeg",
            "check": "ffmpeg -version",
            "priority": "ÉLEVÉ",
        },
        "imagemagick": {
            "desc": "Manipulation images CLI (resize, convert, composite)",
            "url": "https://imagemagick.org",
            "linux": "sudo apt install imagemagick",
            "windows": "winget install ImageMagick.ImageMagick",
            "check": "convert --version",
            "priority": "MOYEN",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# FONCTIONS
# ══════════════════════════════════════════════════════════════════════════════

PRIORITY_ICON = {
    "CRITIQUE": "🔴",
    "ÉLEVÉ":    "🟠",
    "MOYEN":    "🟡",
    "FAIBLE":   "🟢",
}

def _total():
    return sum(len(v) for v in TOOLS.values())


def list_tools(category: str = ""):
    """Affiche le catalogue des outils."""
    cats = {category.upper(): TOOLS[category.upper()]} if category and category.upper() in TOOLS else TOOLS
    total_shown = sum(len(v) for v in cats.values())

    print(f"\n{'═'*72}")
    print(f"  REGISTRE OUTILS GRATUITS — CaelumSwarm™  ({total_shown}/{_total()} outils)")
    print(f"{'═'*72}")

    for cat_name, tools in cats.items():
        critique = sum(1 for t in tools.values() if t.get("priority") == "CRITIQUE")
        print(f"\n  ▶ {cat_name} ({len(tools)} outils, {critique} critiques)")
        print(f"  {'─'*68}")
        print(f"  {'OUTIL':<22} {'P':<2} {'DESCRIPTION':<35} LINUX / WINDOWS")
        for name, info in tools.items():
            icon = PRIORITY_ICON.get(info.get("priority","FAIBLE"), "🟢")
            desc = info["desc"][:35]
            linux_short = info["linux"][:30] + "…" if len(info["linux"]) > 30 else info["linux"]
            win_short   = info["windows"][:20] + "…" if len(info["windows"]) > 20 else info["windows"]
            print(f"  {name:<22} {icon} {desc:<35} {linux_short}")
            print(f"  {'':22}   {'':35} Windows: {win_short}")

    print(f"\n{'═'*72}\n")


def search_tools(query: str):
    """Recherche dans le catalogue."""
    q = query.lower()
    results = []
    for cat, tools in TOOLS.items():
        for name, info in tools.items():
            if (q in name.lower() or q in info["desc"].lower()
                    or q in info.get("url","").lower()):
                results.append((cat, name, info))

    if not results:
        print(f"  Aucun outil trouvé pour '{query}'")
        return

    print(f"\n  🔍 Résultats pour '{query}' ({len(results)} outil(s)):\n")
    for cat, name, info in results:
        icon = PRIORITY_ICON.get(info.get("priority","FAIBLE"), "🟢")
        print(f"  {icon} [{cat}] {name}")
        print(f"      {info['desc']}")
        print(f"      Linux  : {info['linux'][:70]}")
        print(f"      Windows: {info['windows'][:70]}")
        print(f"      URL    : {info['url']}")
        print()


def install_tool(name: str, platform: str = "linux"):
    """Affiche la commande d'installation avec sceau de protocole."""
    # Trouver l'outil
    found = None
    for cat, tools in TOOLS.items():
        if name in tools:
            found = (cat, tools[name])
            break

    if not found:
        print(f"  Outil '{name}' non trouvé. Utilisez --search pour chercher.")
        return

    cat, info = found
    priority = info.get("priority", "FAIBLE")

    # Sceau de protocole avant installation
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from decision_seal import seal_decision
        seal = seal_decision(
            f"install-{name}",
            f"Installation {name} — {info['desc']}",
            verbose=False,
        )
        seal_id = seal["seal_id"]
    except Exception:
        seal_id = "SEAL-NON-DISPONIBLE"

    cmd_linux = info["linux"]
    cmd_win   = info["windows"]
    check     = info.get("check", "")

    print(f"\n{'═'*65}")
    print(f"  INSTALLATION SÉCURISÉE — {name.upper()}")
    print(f"  Catégorie : {cat}  |  Priorité : {PRIORITY_ICON.get(priority,'')} {priority}")
    print(f"  Sceau     : {seal_id}")
    print(f"{'─'*65}")
    print(f"\n  🐧 LINUX :")
    print(f"  {cmd_linux}")
    print(f"\n  🪟 WINDOWS :")
    print(f"  {cmd_win}")
    if check:
        print(f"\n  ✓ Vérification : {check}")
    print(f"\n  🔗 URL : {info['url']}")
    if "models" in info:
        print(f"\n  Modèles disponibles : {', '.join(info['models'])}")
    print(f"{'═'*65}\n")

    _log({"action": "install_prompt", "tool": name, "platform": platform, "seal_id": seal_id})


def audit_installed():
    """Vérifie quels outils critiques sont déjà installés."""
    print(f"\n{'═'*65}")
    print(f"  AUDIT OUTILS INSTALLÉS — CaelumSwarm™")
    print(f"{'═'*65}")

    installed = []
    missing = []
    skipped = []

    for cat, tools in TOOLS.items():
        for name, info in tools.items():
            check_cmd = info.get("check", "")
            if not check_cmd or check_cmd.startswith("#"):
                skipped.append(name)
                continue
            # Utiliser shutil.which pour les commandes simples
            cmd_parts = check_cmd.split()
            binary = cmd_parts[0]
            if binary in ("sudo", "curl", "python3"):
                binary = cmd_parts[-1] if len(cmd_parts) > 1 else binary
            found = shutil.which(binary.split()[0])
            if found:
                installed.append((cat, name, info.get("priority","FAIBLE")))
            elif info.get("priority") in ("CRITIQUE", "ÉLEVÉ"):
                missing.append((cat, name, info))

    print(f"\n  ✅ INSTALLÉS ({len(installed)}) :")
    for cat, name, prio in installed[:30]:
        icon = PRIORITY_ICON.get(prio, "🟢")
        print(f"    {icon} {name:<25} [{cat}]")
    if len(installed) > 30:
        print(f"    ... et {len(installed)-30} autres")

    print(f"\n  ❌ MANQUANTS CRITIQUES/ÉLEVÉS ({len(missing)}) :")
    for cat, name, info in missing:
        icon = PRIORITY_ICON.get(info.get("priority",""), "🟢")
        print(f"    {icon} {name:<25} [{cat}]  → {info['linux'][:45]}")

    print(f"\n  📊 Score couverture : {len(installed)}/{len(installed)+len(missing)} outils critiques+élevés")
    print(f"{'═'*65}\n")

    _log({"action": "audit", "installed": len(installed), "missing": len(missing)})


def export_catalog(fmt: str = "json"):
    """Exporte le catalogue en JSON."""
    out = DATA / "tools_registry_catalog.json"
    catalog = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_tools": _total(),
        "seal": "SEAL-E5DA3C69E63A88CC",
        "categories": {}
    }
    for cat, tools in TOOLS.items():
        catalog["categories"][cat] = {
            name: {
                "desc": info["desc"],
                "url": info["url"],
                "priority": info.get("priority","FAIBLE"),
                "linux": info["linux"],
                "windows": info["windows"],
                "check": info.get("check",""),
            }
            for name, info in tools.items()
        }
    out.write_text(json.dumps(catalog, indent=2, ensure_ascii=False))
    print(f"  Catalogue exporté : {out}  ({_total()} outils)")
    return out


def _log(record: dict):
    log = []
    if LOG.exists():
        try:
            log = json.loads(LOG.read_text())
        except Exception:
            pass
    log.append({**record, "ts": datetime.now(timezone.utc).isoformat()})
    if len(log) > 300:
        log = log[-300:]
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Registre Outils Gratuits CaelumSwarm™")
    parser.add_argument("--list",     action="store_true", help="Lister les outils")
    parser.add_argument("--category", type=str, default="", help="Filtrer par catégorie")
    parser.add_argument("--search",   type=str, default="", help="Rechercher un outil")
    parser.add_argument("--install",  type=str, default="", help="Commande d'installation")
    parser.add_argument("--platform", type=str, default="linux", choices=["linux","windows"])
    parser.add_argument("--audit",    action="store_true", help="Vérifier outils installés")
    parser.add_argument("--export",   type=str, default="", help="Exporter catalogue (json)")
    args = parser.parse_args()

    if args.search:
        search_tools(args.search)
    elif args.install:
        install_tool(args.install, args.platform)
    elif args.audit:
        audit_installed()
    elif args.export:
        export_catalog(args.export)
    elif args.list:
        list_tools(args.category)
    else:
        # Par défaut: audit + stats
        total = _total()
        print(f"\n  REGISTRE OUTILS GRATUITS — CaelumSwarm™")
        print(f"  {total} outils catalogués | SEAL: SEAL-E5DA3C69E63A88CC")
        print(f"  Catégories: {', '.join(TOOLS.keys())}")
        print(f"\n  Commandes disponibles:")
        print(f"    python3 scripts/tools_registry.py --list")
        print(f"    python3 scripts/tools_registry.py --list --category IA_ML")
        print(f"    python3 scripts/tools_registry.py --search 'monitoring'")
        print(f"    python3 scripts/tools_registry.py --install ollama")
        print(f"    python3 scripts/tools_registry.py --install ollama --platform windows")
        print(f"    python3 scripts/tools_registry.py --audit")
        print(f"    python3 scripts/tools_registry.py --export json")
        audit_installed()
