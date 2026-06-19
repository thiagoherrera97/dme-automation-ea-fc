from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import html as html_lib
import re
from typing import Any

try:
    from playwright.sync_api import sync_playwright
except Exception:  # pragma: no cover - optional dependency in some envs
    sync_playwright = None


ROOT = Path(__file__).resolve().parent
EA_URL = "https://www.ea.com/ea-sports-fc/ultimate-team/web-app/"


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


def snapshot_ea_web_app() -> dict[str, Any]:
    if sync_playwright is None:
        raise RuntimeError("Playwright is not available")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:29229")
        context = browser.contexts[0]
        candidate_pages = [candidate for candidate in context.pages if EA_URL in candidate.url]
        page = None
        for candidate in reversed(candidate_pages):
            try:
                html = candidate.content()
            except Exception:
                continue
            if "Daily Common Gold Upgrade" in html:
                page = candidate
                break
            if page is None and "Challenge Requirements" in html and "Auto Complete" in html:
                page = candidate
        if page is None and candidate_pages:
            page = candidate_pages[-1]
        created_page = False
        if page is None:
            page = context.new_page()
            created_page = True
        try:
            if created_page:
                page.goto(EA_URL, wait_until="domcontentloaded")
                page.wait_for_timeout(3000)
            try:
                html = page.content()
            except Exception:
                page.wait_for_timeout(1000)
                html = page.content()

            title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
            nav_match = re.search(r"<nav[^>]*>(.*?)</nav>", html, re.IGNORECASE | re.DOTALL)
            buttons = [
                re.sub(r"<[^>]+>", "", text).strip()
                for text in re.findall(r"<button[^>]*>(.*?)</button>", html, re.IGNORECASE | re.DOTALL)
            ]
            nav = []
            if nav_match:
                nav = [
                    re.sub(r"<[^>]+>", "", text).strip()
                    for text in re.findall(r"<button[^>]*>(.*?)</button>", nav_match.group(1), re.IGNORECASE | re.DOTALL)
                ]
            body = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html_lib.unescape(html))).strip()
            return {
                "url": page.url,
                "title": html_lib.unescape(title_match.group(1)).strip() if title_match else "",
                "buttons": [item for item in buttons if item],
                "nav": [item for item in nav if item],
                "body_preview": body[:1200],
            }
        finally:
            if created_page:
                page.close()


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
        if self.path == "/api/ea/snapshot":
            try:
                self._send_json(snapshot_ea_web_app())
            except Exception as exc:  # pragma: no cover - live browser dependency
                self._send_json({"ok": False, "error": str(exc)}, HTTPStatus.SERVICE_UNAVAILABLE)
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
            snapshot = snapshot_ea_web_app()
            plan = {
                "name": snapshot["title"] or workflow["name"],
                "steps": [
                    f"Ler o desafio aberto no EA FC: {snapshot['title'] or workflow['name']}",
                    *workflow["safe_steps"],
                    "Capturar os botões visíveis e o estado do work area",
                    *workflow["gated_steps"],
                ],
            }
            STATE.plans.append(plan)
            STATE.last_plan = plan["name"]
            STATE.last_observation = f"Live challenge: {snapshot['title'] or workflow['name']}"
            self._send_json({"ok": True, "plan": plan, "workflow": workflow, "snapshot": snapshot}, HTTPStatus.CREATED)
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
