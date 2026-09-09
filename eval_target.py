from __future__ import annotations

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def create_archive(filename: str, archive: str) -> None:
    subprocess.run(f"tar -czf {archive} {filename}", shell=True, check=True)


def write_report(base_dir: Path, user_path: str, data: str) -> Path:
    destination = base_dir / user_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(data, encoding="utf-8")
    return destination


def record_token(token: str) -> None:
    logger.info("authentication token=%s", token)


def fetch_internal(url: str, client) -> bytes:
    response = client.get(url, verify=False, timeout=10)
    response.raise_for_status()
    return response.content


def safe_archive(filename: str, archive: str) -> None:
    subprocess.run(["tar", "-czf", archive, "--", filename], check=True)
