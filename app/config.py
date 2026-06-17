import json
import os
import sys
import hashlib
import secrets


def _get_app_dir():
    """Return a persistent, writable directory for app data.

    When running as a PyInstaller --onefile bundle, __file__ points to a
    temporary extraction folder that is deleted on exit.  Instead, use the
    directory that contains the .exe so settings survive between runs.
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(__file__))


SETTINGS_PATH = os.path.join(_get_app_dir(), "settings.json")

DEFAULTS = {
    "business_name":    "MY BUSINESS",
    "business_address": "123 Business Street, Algiers, Algeria",
    "business_phone":   "+213 XX XX XX XX",
    "business_email":   "",
    "currency":         "DA",
    "low_stock_threshold": 5,
    "tva_rate":         19.0,  # TVA rate in percentage
    "language":         "en",
    "username":         "admin",
    "password":         "1337",
}


# ── Password hashing ─────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    """Hash a password with PBKDF2-HMAC-SHA256 and a random salt.
    Returns a string in the format: pbkdf2:salt_hex:hash_hex
    """
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt, 260_000)
    return f"pbkdf2:{salt.hex()}:{dk.hex()}"


def verify_password(plain: str, stored: str) -> bool:
    """Verify a plain password against a stored hash.
    Also accepts plain-text passwords (for backward compatibility during migration).
    """
    if stored.startswith("pbkdf2:"):
        _, salt_hex, hash_hex = stored.split(":", 2)
        salt = bytes.fromhex(salt_hex)
        dk = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt, 260_000)
        return dk.hex() == hash_hex
    # Fallback: plain-text comparison (pre-migration)
    return plain == stored


def _migrate_plaintext_password(cfg: dict) -> dict:
    """If the stored password is still plain text, hash it and save."""
    pwd = cfg.get("password", "")
    if pwd and not pwd.startswith("pbkdf2:"):
        cfg["password"] = hash_password(pwd)
        save_settings(cfg)
    return cfg


# ── Settings I/O ─────────────────────────────────────────────────────────────

def load_settings() -> dict:
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            cfg = {**DEFAULTS, **data}
            return _migrate_plaintext_password(cfg)
        except Exception:
            pass
    cfg = dict(DEFAULTS)
    return _migrate_plaintext_password(cfg)


def save_settings(data: dict) -> None:
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get(key: str):
    return load_settings().get(key, DEFAULTS.get(key))
