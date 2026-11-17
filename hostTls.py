"""Certificate material for the local HTTPS origin, separate from mitmproxy."""

from datetime import datetime, timedelta
import os
from pathlib import Path
import ssl
import subprocess

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

from hostsService import DOMAINS


class LocalCertificate:
    def __init__(self, folder=None, domains=DOMAINS):
        self.folder = Path(folder) if folder else (
            Path(os.environ.get("LOCALAPPDATA", Path.home())) / "ToLissEFB" / "tls"
        )
        self.domains = tuple(domains)
        self.ca_path = self.folder / "ca.pem"
        self.ca_key_path = self.folder / "ca.key"
        self.cert_path = self.folder / "server.pem"
        self.key_path = self.folder / "server.key"

    @staticmethod
    def _write_key(path, key):
        path.write_bytes(key.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()))

    def ensure(self):
        self.folder.mkdir(parents=True, exist_ok=True)
        now = datetime.utcnow()
        if self.ca_path.exists() != self.ca_key_path.exists():
            raise ValueError("本地 CA 文件不完整，请检查 TLS 目录中的 ca.pem 和 ca.key。")
        if self.ca_path.exists():
            ca = x509.load_pem_x509_certificate(self.ca_path.read_bytes())
            ca_key = serialization.load_pem_private_key(self.ca_key_path.read_bytes(), password=None)
            if ca.public_key().public_numbers() != ca_key.public_key().public_numbers():
                raise ValueError("本地 CA 证书与私钥不匹配。")
            if ca.not_valid_after <= now + timedelta(days=30):
                raise ValueError("本地 CA 即将到期，请移除旧 CA 后重新生成。")
        else:
            ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "ToLissEFB local CA")])
            ca = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
                  .public_key(ca_key.public_key()).serial_number(x509.random_serial_number())
                  .not_valid_before(now - timedelta(days=1)).not_valid_after(now + timedelta(days=3650))
                  .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
                  .add_extension(x509.KeyUsage(False, False, False, False, False, True, True, False, False), critical=True)
                  .sign(ca_key, hashes.SHA256()))
            self._write_key(self.ca_key_path, ca_key)
            self.ca_path.write_bytes(ca.public_bytes(serialization.Encoding.PEM))

        if self.cert_path.exists() and self.key_path.exists():
            cert = x509.load_pem_x509_certificate(self.cert_path.read_bytes())
            names = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
            try:
                ca.public_key().verify(cert.signature, cert.tbs_certificate_bytes,
                                       padding.PKCS1v15(), cert.signature_hash_algorithm)
                signed_by_ca = True
            except InvalidSignature:
                signed_by_ca = False
            if (set(self.domains).issubset(names.get_values_for_type(x509.DNSName))
                    and cert.issuer == ca.subject and signed_by_ca
                    and cert.not_valid_after > now + timedelta(days=7)):
                # Also checks that the leaf and its private key match.
                self.context()
                return
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, self.domains[0])])
        cert = (x509.CertificateBuilder().subject_name(subject).issuer_name(ca.subject)
                .public_key(key.public_key()).serial_number(x509.random_serial_number())
                .not_valid_before(now - timedelta(days=1)).not_valid_after(now + timedelta(days=365))
                .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
                .add_extension(x509.SubjectAlternativeName([x509.DNSName(d) for d in self.domains]), critical=False)
                .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
                .sign(ca_key, hashes.SHA256()))
        self._write_key(self.key_path, key)
        self.cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))

    def context(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_cert_chain(self.cert_path, self.key_path)
        return context

    def trust(self):
        """Install this exact CA in the current user's Windows root store."""
        if os.name != "nt":
            raise OSError("自动信任本地证书目前仅支持 Windows。")
        result = subprocess.run(
            ["certutil.exe", "-user", "-addstore", "-f", "Root", str(self.ca_path)],
            capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=30,
        )
        if result.returncode:
            raise OSError("无法将 ToLissEFB 本地 CA 安装到当前用户的受信任根证书存储。")
