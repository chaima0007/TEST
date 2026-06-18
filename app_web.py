import os
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgentClaude Solutions</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0f1117; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; min-height: 100vh; }
        header { background: #1a1d2e; padding: 24px 40px; border-bottom: 1px solid #2a2d3e; }
        header h1 { font-size: 1.8rem; color: #7c9ef8; letter-spacing: 1px; }
        header p { color: #8888aa; margin-top: 4px; font-size: 0.9rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; padding: 40px; }
        .card { background: #1a1d2e; border: 1px solid #2a2d3e; border-radius: 12px; padding: 28px; transition: border-color 0.2s; }
        .card:hover { border-color: #7c9ef8; }
        .card-icon { font-size: 2rem; margin-bottom: 12px; }
        .card h2 { font-size: 1.1rem; color: #c0d0ff; margin-bottom: 8px; }
        .card p { font-size: 0.85rem; color: #8888aa; line-height: 1.5; margin-bottom: 20px; }
        .btn { background: #7c9ef8; color: #0f1117; border: none; padding: 10px 20px; border-radius: 8px;
               cursor: pointer; font-weight: 600; font-size: 0.85rem; width: 100%; transition: background 0.2s; }
        .btn:hover { background: #9ab4ff; }
        .result-box { margin-top: 12px; background: #0f1117; border: 1px solid #2a2d3e; border-radius: 8px;
                      padding: 12px; font-size: 0.8rem; color: #aaddaa; display: none; white-space: pre-wrap; max-height: 160px; overflow-y: auto; }
        textarea { width: 100%; background: #0f1117; border: 1px solid #2a2d3e; border-radius: 8px;
                   color: #e0e0e0; padding: 10px; font-size: 0.82rem; resize: vertical; margin-bottom: 10px; }
        footer { text-align: center; padding: 20px; color: #444466; font-size: 0.78rem; border-top: 1px solid #1a1d2e; }
    </style>
</head>
<body>
<header>
    <h1>AgentClaude Solutions</h1>
    <p>Plateforme d'agents IA — Tableau de bord</p>
</header>
<div class="grid">

    <div class="card">
        <div class="card-icon">🧠</div>
        <h2>Orchestrateur</h2>
        <p>Coordonne les agents et analyse les requêtes complexes via le moteur IA central.</p>
        <textarea id="orch-input" rows="3" placeholder="Entrez votre requête..."></textarea>
        <button class="btn" onclick="callAgent('/orchestrateur', {query: document.getElementById('orch-input').value}, 'orch-result')">Lancer</button>
        <div class="result-box" id="orch-result"></div>
    </div>

    <div class="card">
        <div class="card-icon">💼</div>
        <h2>Agent Commercial</h2>
        <p>Analyse les opportunités commerciales, rédige des propositions et qualifie les prospects.</p>
        <textarea id="comm-input" rows="3" placeholder="Décrivez le besoin commercial..."></textarea>
        <button class="btn" onclick="callAgent('/commercial', {message: document.getElementById('comm-input').value}, 'comm-result')">Analyser</button>
        <div class="result-box" id="comm-result"></div>
    </div>

    <div class="card">
        <div class="card-icon">🔐</div>
        <h2>Agent Sécurité</h2>
        <p>Analyse le code soumis pour détecter les vulnérabilités et failles de sécurité.</p>
        <textarea id="sec-input" rows="3" placeholder="Collez votre code ici..."></textarea>
        <button class="btn" onclick="callAgent('/securite', {code: document.getElementById('sec-input').value}, 'sec-result')">Scanner</button>
        <div class="result-box" id="sec-result"></div>
    </div>

    <div class="card">
        <div class="card-icon">📋</div>
        <h2>Mémoire Clients</h2>
        <p>Consulte la base de données clients, historiques et statistiques de la plateforme.</p>
        <button class="btn" onclick="callAgent('/memoire', null, 'mem-result', 'GET')">Consulter</button>
        <div class="result-box" id="mem-result"></div>
    </div>

</div>
<footer>AgentClaude Solutions &copy; 2025 — Propulsé par Gemini AI</footer>
<script>
async function callAgent(url, body, resultId, method) {
    const box = document.getElementById(resultId);
    box.style.display = 'block';
    box.textContent = 'Chargement...';
    try {
        const opts = method === 'GET'
            ? { method: 'GET' }
            : { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body) };
        const res = await fetch(url, opts);
        const data = await res.json();
        box.textContent = JSON.stringify(data, null, 2);
    } catch(e) {
        box.textContent = 'Erreur: ' + e.message;
    }
}
</script>
</body>
</html>
"""


def _creer_model(model_name=None, system_instruction="", generation_config=None, **kwargs):
    """Compatibilité: retourne un proxy GenerativeModel pour google.genai."""
    class _ModelProxy:
        def __init__(self, mn, si, cfg):
            self.model_name = mn or MODEL
            self.system_instruction = si
            self.config = cfg or types.GenerateContentConfig(temperature=0.3, max_output_tokens=2000)
            if isinstance(self.config, types.GenerateContentConfig):
                self.config = types.GenerateContentConfig(
                    system_instruction=si,
                    temperature=self.config.temperature if hasattr(self.config, 'temperature') else 0.3,
                    max_output_tokens=self.config.max_output_tokens if hasattr(self.config, 'max_output_tokens') else 2000,
                )
        def generate_content(self, prompt, stream=False):
            if stream:
                return client.models.generate_content_stream(
                    model=self.model_name, contents=prompt, config=self.config)
            return client.models.generate_content(
                model=self.model_name, contents=prompt, config=self.config)
    config = generation_config
    if config and not isinstance(config, types.GenerateContentConfig):
        config = types.GenerateContentConfig(
            temperature=getattr(config, 'temperature', 0.3),
            max_output_tokens=getattr(config, 'max_output_tokens', 2000),
        )
    return _ModelProxy(model_name, system_instruction, config)


def _gemini_generate(prompt: str) -> str:
    try:
        from google import genai
from google.genai import types
        genai.configure(api_key=GEMINI_API_KEY)
        model = _creer_model("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erreur IA: {str(e)}"


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/")
def dashboard():
    return render_template_string(DASHBOARD_HTML)


@app.post("/orchestrateur")
def orchestrateur_route():
    try:
        from orchestrateur import orchestrateur
        data = request.get_json(silent=True) or {}
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Paramètre 'query' manquant"}), 400
        result = orchestrateur(query)
        return jsonify({"result": result})
    except ImportError:
        query = (request.get_json(silent=True) or {}).get("query", "")
        result = _gemini_generate(f"En tant qu'orchestrateur IA, traite cette requête:\n{query}")
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/commercial")
def commercial_route():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "")
        if not message:
            return jsonify({"error": "Paramètre 'message' manquant"}), 400
        prompt = (
            "Tu es un agent commercial expert. Analyse la demande suivante et propose "
            "une stratégie commerciale avec qualification du prospect et prochaines étapes:\n"
            f"{message}"
        )
        result = _gemini_generate(prompt)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/securite")
def securite_route():
    try:
        data = request.get_json(silent=True) or {}
        code = data.get("code", "")
        if not code:
            return jsonify({"error": "Paramètre 'code' manquant"}), 400
        prompt = (
            "Tu es un expert en cybersécurité. Analyse ce code et liste les vulnérabilités "
            "détectées (injections, secrets exposés, mauvaises pratiques, CVE connues). "
            "Sois précis et concis:\n\n"
            f"```\n{code}\n```"
        )
        result = _gemini_generate(prompt)
        return jsonify({"vulnerabilities": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/memoire")
def memoire_route():
    try:
        from memoire import get_all_clients, get_stats
        clients = get_all_clients()
        stats = get_stats()
        return jsonify({"clients": clients, "stats": stats})
    except ImportError:
        return jsonify({
            "clients": [],
            "stats": {"total": 0, "message": "Module memoire non disponible"},
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
