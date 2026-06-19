from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent


@dataclass
class AppState:
    mode: str = "planning"
    approval_required: bool = True
    last_observation: str = "No observations yet"
    last_plan: str = "No plan yet"
    plans: list[dict[str, Any]] = field(default_factory=list)
    observations: list[dict[str, Any]] = field(default_factory=list)


STATE = AppState()

WORKFLOWS: dict[str, dict[str, Any]] = {
    "daily-common-gold-upgrade": {
        "name": "Daily Common Gold Upgrade",
        "mode": "sbc-specific-flow",
        "summary": "Mapeia e prepara o fluxo do upgrade diário sem concluir o envio.",
        "requirements": [
            "Bronze: Min. 5 Players",
            "Silver: Min. 5 Players",
            "Number of Players in the Squad: 10",
        ],
        "safe_steps": [
            "Ler o título e os requisitos do desafio",
            "Inspecionar o estado atual do squad",
            "Registrar a composição visível sem mover jogadores",
            "Preparar um plano de preenchimento",
        ],
        "gated_steps": [
            "Pedir autorização explícita antes de qualquer submit",
            "Parar se houver risco de consumir jogadores que o usuário quer preservar",
        ],
        "approval_preview": {
            "squad_name": "Working Area",
            "formation": "Unknown",
            "rating": "0",
            "chemistry": "0/33",
            "players": ["GK", "RB", "CB", "CB", "LB", "RM", "CM", "CM", "LM", "ST", "ST"],
        },
    }
}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        if self.path == "/api/health":
            self._send_json({"ok": True})
            return
        if self.path == "/api/state":
            self._send_json(
                {
                    "mode": STATE.mode,
                    "approval_required": STATE.approval_required,
                    "last_observation": STATE.last_observation,
                    "last_plan": STATE.last_plan,
                    "plans": STATE.plans,
                    "observations": STATE.observations,
                }
            )
            return
        if self.path == "/api/flows/daily-common-gold-upgrade":
            self._send_json(WORKFLOWS["daily-common-gold-upgrade"])
            return
        super().do_GET()

    def do_POST(self) -> None:
        if self.path == "/api/observations":
            payload = self._read_json()
            note = str(payload.get("note", "")).strip()
            observation = {
                "note": note or "Observation added",
                "source": str(payload.get("source", "frontend")),
            }
            STATE.observations.append(observation)
            STATE.last_observation = observation["note"]
            self._send_json({"ok": True, "observation": observation}, HTTPStatus.CREATED)
            return

        if self.path == "/api/plans":
            payload = self._read_json()
            plan = {
                "name": str(payload.get("name", "Untitled plan")),
                "steps": list(payload.get("steps", [])),
            }
            STATE.plans.append(plan)
            STATE.last_plan = plan["name"]
            self._send_json({"ok": True, "plan": plan}, HTTPStatus.CREATED)
            return

        if self.path == "/api/flows/daily-common-gold-upgrade/plan":
            workflow = WORKFLOWS["daily-common-gold-upgrade"]
            plan = {
                "name": workflow["name"],
                "steps": [
                    *workflow["safe_steps"],
                    *workflow["gated_steps"],
                ],
            }
            STATE.plans.append(plan)
            STATE.last_plan = plan["name"]
            self._send_json({"ok": True, "plan": plan, "workflow": workflow}, HTTPStatus.CREATED)
            return

        if self.path == "/api/approvals":
            payload = self._read_json()
            STATE.approval_required = not bool(payload.get("approved", False))
            if "note" in payload:
                STATE.last_observation = str(payload["note"])
            self._send_json({"ok": True, "approval_required": STATE.approval_required})
            return

        self._send_json({"ok": False, "error": "Not found"}, HTTPStatus.NOT_FOUND)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("Serving on http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
