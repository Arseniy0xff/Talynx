import json
import base64
import hashlib
import random
import string
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

import name_space


class DSM:

    def get_all_notes_path(self):
        return [p.resolve() for p in name_space.PATH_TO_NOTES.rglob("*.json") if p.is_file()]

    def get_all_notes(self) -> list:
        l = self.get_all_notes_path()
        return [self.get_note_by_path(_) for _ in l]

    def get_note_by_path(self, path):
        if not path.is_file():
            raise FileNotFoundError(f"file not found: {path}")

        with path.open(encoding="utf-8") as f:
            return json.load(f)

    def save_dict_to_json(self, data: dict, password = ''):

        if "file_name" not in data:
            raise KeyError("not found required key: 'file_name'")

        filename = f"{data['file_name']}.json"
        file_path = name_space.PATH_TO_NOTES / filename

        if len(password) > 0:
            data = self.encrypt_dict(data, password)

        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return file_path


    def _derive_key(self, password: str, salt: bytes = b"q#Z#etn4vPD3h$qqfWZmTEJEzzRWZ2%FnXwoRYbH2U@3Tb4@") -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=200_000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_dict(self, data: dict, password: str) -> dict:
        if "content" not in data or not isinstance(data["content"], list):
            raise ValueError("key 'content' is not found")

        plain_json = json.dumps(data["content"], ensure_ascii=False).encode()
        fernet = Fernet(self._derive_key(password))
        cipher_bytes = fernet.encrypt(plain_json)
        encrypted = data.copy()

        encrypted["content"] = cipher_bytes.decode()
        return encrypted

    def decrypt_dict(self, data: dict, password: str) -> dict:
        if "content" not in data or not isinstance(data["content"], str):
            raise ValueError("key 'content' is not found")

        fernet = Fernet(self._derive_key(password))
        plain_json = fernet.decrypt(data["content"].encode())
        decrypted_content = json.loads(plain_json.decode())

        decrypted = data.copy()
        decrypted["content"] = decrypted_content
        return decrypted

    def generate_filename(self, length=16) -> str:
        chars = string.ascii_lowercase + string.digits
        return "".join(random.choices(chars, k=length))