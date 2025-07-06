import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'app'))

from utils import hash_password, verify_password, create_access_token


def test_password_hashing():
    pw = 'secret'
    hashed = hash_password(pw)
    assert verify_password(pw, hashed)


def test_access_token():
    token = create_access_token('user')
    assert token
