import base64
import json
import hashlib
from typing import Any, Dict

class Base64DataHandler:
    """Handles encoding and decoding of JSON data to/from Base64."""
    
    @staticmethod
    def encode(data: Any) -> str:
        """Encodes Python object to Base64 JSON string."""
        json_str = json.dumps(data)
        return base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def decode(b64_str: str) -> Any:
        """Decodes Base64 JSON string to Python object."""
        try:
            json_str = base64.b64decode(b64_str).decode('utf-8')
            return json.loads(json_str)
        except Exception:
            return None

def hash_password(password: str) -> str:
    """Simple SHA-256 password hashing with a static salt for demo purposes.
    In a real official app, use bcrypt or Argon2.
    """
    salt = "vehicle_tracking_secret_salt"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verifies a password against its hash."""
    return hash_password(password) == hashed
