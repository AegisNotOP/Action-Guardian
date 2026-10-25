"""
ActionGuardian Backend & HTTP Server
Zero-external-dependency local web app powered by Python's built-in http.server.
Handles:
- Safety Simulation & Threat Prediction
- Recipient Genuineness Verification (DNS check)
- AI Auto-Rewrite (Self-Correction)
- Real Email Dispatch via SMTP using fixed config.py
"""
import os
import sys
import json
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

from agent.guardian import (
    ActionGuardian,
    DirectCommitNotAllowedError,
    ActionBlockedError,
    HumanConfirmationRequiredError,
    GuardianException
)
from agent.models import ActionCandidate, DomainType
from agent.mailer import MailEngine
from evaluate import run_benchmark


class GuardianRequestHandler(BaseHTTPRequestHandler):
    guardian = ActionGuardian()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    web_dir = os.path.join(base_dir, "web")

    def log_message(self, format, *args):
        # Clean custom terminal logger
        sys.stdout.write(f"[{self.log_date_time_string()}] {self.command} {self.path} -> {args[1]}\n")
        sys.stdout.flush()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ["/", "/index.html"]:
            self._serve_file(os.path.join(self.web_dir, "index.html"), "text/html; charset=utf-8")
        elif path == "/api/benchmark":
            self._handle_get_benchmark()
        elif path == "/api/sender":
            self._send_json(MailEngine.get_sender_info(), status=200)
        else:
            self._send_json({"error": "Endpoint Not Found"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/verify_email":
            self._handle_verify_email()
        elif path == "/api/preview":
            self._handle_post_preview()
        elif path == "/api/rewrite":
            self._handle_post_rewrite()
        elif path == "/api/send":
            self._handle_post_send()
        elif path == "/api/commit":
            self._handle_post_commit()
        else:
            self._send_json({"error": "Endpoint not found"}, status=404)

    def _serve_file(self, filepath: str, content_type: str):
        if not os.path.exists(filepath):
            self._send_json({"error": "File not found"}, status=404)
            return

        with open(filepath, "rb") as f:
            content = f.read()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        raw = self.rfile.read(content_length)
        return json.loads(raw.decode("utf-8"))

    def _handle_verify_email(self):
        try:
            body = self._read_json_body()
            email = body.get("email", "")
            verification = MailEngine.verify_recipient(email)
            self._send_json(verification, status=200)
        except Exception as e:
            self._send_json({
                "is_valid": False,
                "domain_exists": False,
                "error": f"Verification error: {str(e)}"
            }, status=200)

    def _handle_post_preview(self):
        try:
            body = self._read_json_body()
            target = body.get("target", "").strip()
            subject = body.get("subject", "").strip()
            content = body.get("content", "").strip()

            candidate = ActionCandidate(
                domain=DomainType.EMAIL,
                target=target,
                action_type="SEND_EMAIL",
                content=content,
                parameters={"subject": subject}
            )

            result = self.guardian.preview(candidate)

            # Safely verify recipient domain
            try:
                verification = MailEngine.verify_recipient(target) if target else {"is_valid": False, "error": "No email entered"}
            except Exception:
                verification = {"is_valid": True, "domain_exists": True, "message": "Format accepted."}

            result["recipient_verification"] = verification
            self._send_json(result, status=200)

        except Exception as e:
            self._send_json({"error": f"Simulation failed: {str(e)}"}, status=500)

    def _handle_post_rewrite(self):
        try:
            body = self._read_json_body()
            subject = body.get("subject", "").strip()
            content = body.get("content", "").strip()
            target = body.get("target", "").strip()

            # Call safe rewriter
            rewrite_res = self.guardian.predictor.rewrite_email_safely(subject, content)

            # Re-simulate the improved draft
            clean_candidate = ActionCandidate(
                domain=DomainType.EMAIL,
                target=target,
                action_type="SEND_EMAIL",
                content=rewrite_res["remediated_content"],
                parameters={"subject": rewrite_res["remediated_subject"]}
            )
            clean_preview = self.guardian.preview(clean_candidate)
            rewrite_res["clean_preview"] = clean_preview

            self._send_json(rewrite_res, status=200)
        except Exception as e:
            self._send_json({"error": f"Rewrite failed: {str(e)}"}, status=500)

    def _handle_post_send(self):
        try:
            body = self._read_json_body()
            preview_id = body.get("preview_id", "").strip()
            recipient = body.get("recipient", "").strip()
            subject = body.get("subject", "").strip()
            email_body = body.get("content", "").strip()
            override = bool(body.get("user_override", False))

            # 1. Enforce Preview Verification
            if not preview_id or preview_id not in self.guardian.preview_cache:
                self._send_json({
                    "status": "FAILED",
                    "error": "Direct execution forbidden. You must first simulate and scan the email before sending."
                }, status=403)
                return

            preview_entry = self.guardian.preview_cache[preview_id]
            sim = preview_entry["result"]

            # 2. Safety block checks
            if sim.is_blocked and not override:
                self._send_json({
                    "status": "FAILED",
                    "error": "Sending blocked due to high-risk threats. Click 'Auto-Improve' to remove risks, or authorize override."
                }, status=422)
                return

            # 3. Commit through Guardian
            self.guardian.commit(preview_id, user_override=override)

            # 4. Dispatch Email via MailEngine (uses config.py)
            send_result = MailEngine.send_email(
                recipient=recipient,
                subject=subject,
                body=email_body
            )

            self._send_json(send_result, status=200 if send_result["status"] == "SENT" else 400)

        except Exception as e:
            self._send_json({"status": "FAILED", "error": f"Send failed: {str(e)}"}, status=500)

    def _handle_post_commit(self):
        try:
            body = self._read_json_body()
            preview_id = body.get("preview_id", "")
            override = bool(body.get("user_override", False))
            receipt = self.guardian.commit(preview_id, user_override=override)
            self._send_json(receipt.to_dict(), status=200)
        except Exception as e:
            self._send_json({"error": str(e)}, status=400)

    def _handle_get_benchmark(self):
        try:
            metrics = run_benchmark()
            self._send_json(metrics, status=200)
        except Exception as e:
            self._send_json({"error": f"Benchmark error: {str(e)}"}, status=500)


def find_free_port(starting_port=8000) -> int:
    port = starting_port
    while port < 65535:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if s.connect_ex(("127.0.0.1", port)) != 0:
                    return port
        except Exception:
            return port
        port += 1
    return 8000


def main():
    port = find_free_port(8000)
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, GuardianRequestHandler)

    print("\n" + "=" * 70, flush=True)
    print(" [+] ACTIONGUARDIAN EMAIL SAFETY GATEWAY IS LIVE!", flush=True)
    print("=" * 70, flush=True)
    print(f" Web Interface  : http://localhost:{port}", flush=True)
    print(f" Fixed Config   : Configured via config.py", flush=True)
    print("=" * 70, flush=True)
    print(" Press Ctrl+C in your terminal to stop the server.\n", flush=True)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping ActionGuardian server gracefully...", flush=True)
        httpd.server_close()


if __name__ == "__main__":
    main()
