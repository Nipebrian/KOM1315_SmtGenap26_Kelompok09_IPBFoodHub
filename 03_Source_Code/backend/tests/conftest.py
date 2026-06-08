"""
Konfigurasi pytest untuk unit test modul keamanan IPB Food Hub.
Set env vars di module level (sebelum test collection) agar config.py tidak raise.
"""
import os
import base64
from dotenv import load_dotenv

# Load .env dari parent folder (03_Source_Code/backend/)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Fallback: jika .env tidak ada, set nilai test minimal
if not os.environ.get("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/test_ipbfoodhub"
if not os.environ.get("SECRET_KEY"):
    os.environ["SECRET_KEY"] = "test-secret-key-for-pytest-ipbfoodhub-32chars!"
if not os.environ.get("ENCRYPTION_KEY"):
    # 32 byte deterministik untuk reproducibility test
    os.environ["ENCRYPTION_KEY"] = base64.b64encode(b"ipbfoodhub-test-aes-key-32bytes!").decode()
