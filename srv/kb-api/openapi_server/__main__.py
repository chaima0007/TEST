#!/usr/bin/env python3
import os
import connexion
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = connexion.App(__name__, specification_dir=os.path.join(os.path.dirname(__file__), "openapi"))
    app.add_api("openapi.yaml", pythonic_params=True, strict_validation=True)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=int(os.getenv("KB_PORT", "8080")), debug=os.getenv("DEBUG", "false").lower() == "true")
