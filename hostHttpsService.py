"""Local HTTPS origin for hosts mode; no CONNECT, upstream proxy or system proxy."""

import base64
import hashlib
import ipaddress
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import re
import secrets
import threading
import time
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

import cv2

from hostTls import LocalCertificate
from hostsService import DOMAINS, HostsRedirect
from hostProxyBypass import ProxyBypass

log = logging.getLogger("toliss_efb.osm")


def _json(data):
    return json.dumps(data, ensure_ascii=False).encode("utf-8")


def cycle_info(today=None):
    # AIRAC 2609 began on 2026-09-03; subsequent cycles are 28 days apart.
    today = today or date.today()
    epoch = date(2026, 9, 3)
    start = epoch + timedelta(days=((today - epoch).days // 28) * 28)
    jan = date(start.year, 1, 1)
    first = epoch + timedelta(days=-((epoch - jan).days // 28) * 28)
    if first < jan:
        first += timedelta(days=28)
    cycle = int(f"{start.year % 100:02d}{(start - first).days // 28 + 1:02d}")
    return {"airac_cycle": cycle, "cycle_start_date": start.isoformat(),
            "cycle_end_date": (start + timedelta(days=28)).isoformat(),
            "import_time": start.isoformat()}


class LocalApi:
    def __init__(self, manager=None):
        self.manager = manager
        self.lock = threading.Lock()
        self.device_codes = {}
        self.refresh_tokens = set()
        self.authorization_codes = {}

    @staticmethod
    def _pkce_valid(record, form):
        if record.get("client_id") and form.get("client_id") != record["client_id"]:
            return False
        challenge = record.get("code_challenge")
        if not challenge:
            return True
        verifier = form.get("code_verifier", "")
        if not verifier:
            return False
        computed = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        return secrets.compare_digest(computed, challenge)

    def _authorize(self, form):
        uri = form.get("redirect_uri", "")
        parsed = urlsplit(uri)
        try:
            loopback = parsed.hostname == "localhost" or ipaddress.ip_address(parsed.hostname or "").is_loopback
        except ValueError:
            loopback = False
        if (parsed.scheme not in ("http", "https") or not loopback or parsed.username
                or parsed.password or parsed.fragment or "\r" in uri or "\n" in uri
                or form.get("response_type") != "code"):
            return 400, "application/json", _json({"error": "invalid_request"})
        if form.get("code_challenge_method", "S256") != "S256":
            return 400, "application/json", _json({"error": "invalid_request"})
        code = secrets.token_urlsafe(32)
        self.authorization_codes[code] = {
            "expires": time.time() + 600, "redirect_uri": uri,
            "client_id": form.get("client_id", ""),
            "code_challenge": form.get("code_challenge", ""),
        }
        query = parse_qs(parsed.query)
        query["code"] = [code]
        if "state" in form:
            query["state"] = [form["state"]]
        target = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query, doseq=True), ""))
        return 302, "text/plain; charset=utf-8", b"Local Charts sign-in completed.", {"Location": target}

    def _grant_valid(self, form):
        grant = form.get("grant_type", "")
        if grant == "refresh_token":
            token = form.get("refresh_token", "")
            return token in self.refresh_tokens or (token.startswith("toliss-efb-local-") and len(token) >= 48)
        if grant == "authorization_code":
            records, key = self.authorization_codes, form.get("code", "")
        elif grant == "urn:ietf:params:oauth:grant-type:device_code":
            records, key = self.device_codes, form.get("device_code", "")
        else:
            return False
        record = records.get(key)
        if not record or record["expires"] < time.time() or not self._pkce_valid(record, form):
            return False
        if grant == "authorization_code" and form.get("redirect_uri") != record["redirect_uri"]:
            return False
        del records[key]
        return True

    def _token(self, client_id=""):
        # Local-only identity, never forwarded to or accepted by the real service.
        now = int(time.time())
        claims = {"sub": "toliss-efb-local", "preferred_username": "Local Charts",
                  "name": "Local Charts", "iss": "toliss-efb-local",
                  "aud": "toliss-efb-local", "iat": now, "exp": now + 86400,
                  "subscriptions": ["charts"], "scope": ["openid", "userinfo", "offline_access", "charts"],
                  "nbf": now}
        if client_id:
            claims["client_id"] = client_id
        # Some EFB SDKs decode with atob(), requiring the standard Base64 alphabet.
        encode = lambda value: base64.b64encode(_json(value)).decode("ascii")
        token = encode({"alg": "none", "typ": "JWT"}) + "." + encode(claims) + "." + base64.b64encode(b"toliss-efb-local").decode("ascii")
        refresh = "toliss-efb-local-" + secrets.token_urlsafe(32)
        self.refresh_tokens.add(refresh)
        return {"access_token": token, "id_token": token, "refresh_token": refresh,
                "token_type": "Bearer", "expires_in": 86400, "scope": " ".join(claims["scope"])}

    def route(self, method, host, path, form=None):
        form = form or {}
        host = host.split(":", 1)[0].lower().rstrip(".")
        if host not in DOMAINS:
            return 421, "application/json", _json({"error": "unknown_host"})
        if host == "identity.api.navigraph.com":
            if path == "/connect/authorize" and method in ("GET", "HEAD"):
                return self._authorize(form)
            if path == "/local/device" and method in ("GET", "HEAD"):
                return 200, "text/plain; charset=utf-8", "ToLissEFB：本地航图已就绪，无需登录外网账号。".encode("utf-8")
            if path == "/connect/deviceauthorization" and method == "POST":
                code = secrets.token_urlsafe(24)
                if form.get("code_challenge_method", "S256") != "S256":
                    return 400, "application/json", _json({"error": "invalid_request"})
                self.device_codes[code] = {
                    "expires": time.time() + 600, "client_id": form.get("client_id", ""),
                    "code_challenge": form.get("code_challenge", ""),
                }
                uri = "https://identity.api.navigraph.com/local/device"
                return 200, "application/json", _json({
                    "device_code": code, "user_code": "LOCAL", "verification_uri": uri,
                    "verification_uri_complete": uri, "expires_in": 600, "interval": 1})
            if path == "/connect/token" and method == "POST":
                if not self._grant_valid(form):
                    return 400, "application/json", _json({"error": "invalid_grant"})
                return 200, "application/json", _json(self._token(form.get("client_id", "")))
            if path == "/connect/userinfo" and method in ("GET", "HEAD", "POST"):
                return 200, "application/json", _json({"sub": "toliss-efb-local",
                    "preferred_username": "Local Charts", "name": "Local Charts",
                    "subscriptions": ["charts"], "email_verified": False})
            if path == "/connect/revocation" and method == "POST":
                self.refresh_tokens.discard(form.get("token", ""))
                return 200, "application/json", b"{}"
            return 404, "application/json", _json({"error": "not_found"})
        if method not in ("GET", "HEAD"):
            return 405, "application/json", _json({"error": "method_not_allowed"})
        if ((host == "api.navigraph.com" and path == "/v1/subscriptions/valid")
                or (host == "subscriptions.api.navigraph.com" and path == "/1/subscriptions/valid")):
            now = date.today()
            return 200, "application/json", _json([{
                "type": "charts", "subscription_name": "Local Charts",
                "date_active": (now - timedelta(days=1)).isoformat() + "T00:00:00.000Z",
                "date_expiry": (now + timedelta(days=365)).isoformat() + "T23:59:59.000Z",
            }])
        if host == "charts.api.navigraph.com" and path == "/1/cycles/current":
            return 200, "application/json", _json(cycle_info())
        if host != "api.navigraph.com":
            return 404, "application/json", _json({"error": "not_found"})
        match = re.fullmatch(r"/v2/(airport|charts)/([A-Za-z]{4})/?", path)
        if match and self.manager is not None:
            kind, icao = match.groups()
            result = (self.manager.get_ap_info(icao.upper()) if kind == "airport"
                      else self.manager.get_ap_charts(icao.upper()))
            if result is not None:
                return 200, "application/json", _json(result)
        match = re.fullmatch(r"/v2/charts/([A-Za-z]{4})/([A-Za-z0-9_-]+)_([dn])\.png", path)
        if match and self.manager is not None:
            icao, chart_id, theme = match.groups()
            airport = self.manager.aps.get(icao.upper())
            if airport is not None:
                image = airport.get_pic(chart_id, theme == "n")
                if image is not None:
                    ok, encoded = cv2.imencode(".png", image)
                    if ok:
                        return 200, "image/png", encoded.tobytes()
        return 404, "application/json", _json({"error": "local_data_not_found"})


class _Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False

    def get_request(self):
        connection, address = self.socket.accept()
        connection.settimeout(10)
        try:
            return self.tls_context.wrap_socket(connection, server_side=True), address
        except Exception as exc:
            log.warning("[hosts HTTPS] TLS 握手失败，客户端=%s：%s", address[0], exc)
            connection.close()
            raise


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        # BaseHTTPServer's default includes the query; never log tokens or bodies.
        pass

    def _respond(self, status, content_type, body, extra_headers=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        origin = self.headers.get("Origin")
        self.send_header("Access-Control-Allow-Origin", origin or "*")
        if origin:
            self.send_header("Access-Control-Allow-Credentials", "true")
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Accept, Content-Type, X-Requested-With, Origin")
        self.send_header("Access-Control-Expose-Headers", "Content-Length, Content-Type")
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        # Keep the headers and a small JSON body in the same SSL write. A header-only
        # TLS record has correlated with zero-byte auth responses in ToLiss 1.3.2.
        self._headers_buffer.append(b"\r\n")
        headers = b"".join(self._headers_buffer)
        self._headers_buffer = []
        self.wfile.write(headers + (b"" if self.command == "HEAD" else body))
        self.wfile.flush()

    def do_OPTIONS(self):
        self._respond(204, "text/plain", b"")

    def _handle(self):
        parsed = urlsplit(self.path)
        path = parsed.path
        form = {k: v[0] for k, v in parse_qs(parsed.query, keep_blank_values=True).items()}
        try:
            if self.command == "POST":
                length = int(self.headers.get("Content-Length", "0"))
                if length < 0 or length > 65536 or self.headers.get("Transfer-Encoding"):
                    self.close_connection = True
                    self._respond(413, "application/json", b'{"error":"invalid_body_size"}')
                    return
                form.update({k: v[0] for k, v in parse_qs(self.rfile.read(length).decode("utf-8")).items()})
            with self.server.api.lock:
                result = self.server.api.route(self.command, self.headers.get("Host", ""), path, form)
        except (ValueError, UnicodeError):
            self.close_connection = True
            result = (400, "application/json", b'{"error":"invalid_request"}')
        except Exception:
            log.exception("[hosts HTTPS] 本地请求处理失败: %s", path)
            result = (500, "application/json", b'{"error":"local_processing_failed"}')
        agent = self.headers.get("User-Agent", "-")[:160]
        log.info("[hosts HTTPS] %s host=%s path=%s status=%s bytes=%s client=%s",
                 self.command, self.headers.get("Host", "-")[:120], path, result[0], len(result[2]), agent)
        self._respond(*result)

    do_GET = _handle
    do_HEAD = _handle
    do_POST = _handle


class HostHttpsService:
    def __init__(self, redirect=None, certificate=None, port=443, bypass=None):
        self.redirect = redirect if redirect is not None else HostsRedirect()
        self.certificate = certificate if certificate is not None else LocalCertificate()
        self.port = port
        self.bypass = bypass if bypass is not None else ProxyBypass()
        self.server = None
        self.thread = None

    def needs_restore(self):
        return self.redirect.needs_restore() or self.bypass.needs_restore()

    def start(self, manager=None, trust=True, progress=None):
        if self.server is not None:
            return
        if self.needs_restore():
            raise ValueError("检测到上次遗留的 hosts 修改，请先关闭开关恢复，再重新开启。")
        progress = progress or (lambda message: None)
        self.redirect.check_writable()
        progress("正在生成或加载 HTTPS 证书…")
        self.certificate.ensure()
        context = self.certificate.context()
        progress("正在绑定本地 HTTPS 端口…")
        server = _Server(("127.0.0.1", self.port), _Handler)
        server.tls_context = context
        server.api = LocalApi(manager)
        thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.1}, daemon=True)
        try:
            if trust:
                progress("正在安装本地 CA 信任，请留意 Windows 证书确认窗口…")
                self.certificate.trust()
            thread.start()
            progress("正在备份并修改 hosts…")
            self.redirect.enable()
            progress("正在为 Navigraph 域名设置临时直连例外…")
            self.bypass.enable()
        except Exception:
            try:
                if self.redirect.needs_restore():
                    self.redirect.disable()
                self.bypass.disable()
            except Exception:
                if thread.is_alive():
                    self.server, self.thread = server, thread
                else:
                    server.server_close()
                raise
            if thread.is_alive():
                server.shutdown()
                thread.join(timeout=12)
            server.server_close()
            raise
        self.server, self.thread = server, thread
        log.info("[hosts HTTPS] 本地服务已启动: 127.0.0.1:%s", server.server_port)

    def stop(self, restore_universal=False):
        # Restore DNS before stopping; if restoration fails, keep the server alive.
        if restore_universal:
            self.redirect.restore_universal()
        else:
            self.redirect.disable()
        self.bypass.disable()
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join(timeout=12)
            self.server = self.thread = None
        log.info("[hosts HTTPS] hosts 已恢复，本地服务已停止")
