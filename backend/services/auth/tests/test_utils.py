import sys
from pathlib import Path

# Add repository root to the path so ``services`` can be imported as a package
ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from services.auth.app.utils import (
    hash_password,
    verify_password,
    create_access_token,
)


def test_password_hashing():
    pw = 'secret'
    hashed = hash_password(pw)
    assert verify_password(pw, hashed)


def test_access_token():
    token = create_access_token('user')
    assert token
