import os
from pathlib import Path
from fastapi import UploadFile
from datetime import datetime
from typing import Optional

# Configurações
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
UPLOADS_DIR = STATIC_DIR / "uploads"

# Garante que os diretórios existam
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
(UPLOADS_DIR / "categorias").mkdir(exist_ok=True)
(UPLOADS_DIR / "produtos").mkdir(exist_ok=True)
(UPLOADS_DIR / "temp").mkdir(exist_ok=True)


class LocalStorage:
    @staticmethod
    def save_upload(file: UploadFile, destination: str, prefix: str = "") -> str:
        """Salva um arquivo enviado no sistema de arquivos local"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{prefix}{timestamp}_{file.filename}"
        filepath = UPLOADS_DIR / destination / filename

        with open(filepath, "wb") as buffer:
            buffer.write(file.file.read())

        return f"/static/uploads/{destination}/{filename}"

    @staticmethod
    def delete_file(file_url: str) -> bool:
        """Remove um arquivo do sistema de arquivos local"""
        if not file_url.startswith("/static/uploads/"):
            return False

        relative_path = file_url[len("/static/uploads/"):]
        filepath = UPLOADS_DIR / relative_path

        try:
            os.remove(filepath)
            return True
        except FileNotFoundError:
            return False


# Implementação futura para AWS S3
class S3Storage:
    pass  # Implementar conforme necessidade