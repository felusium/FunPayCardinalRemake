from __future__ import annotations

import os
import shutil
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


REPO = "felusium/FunPayCardinalRemake"
FALLBACK_REPOS = ("felusium/FunPayCardinal_Remake",)
BRANCH = "main"
ARCHIVE_URL = f"https://github.com/{REPO}/archive/refs/heads/{BRANCH}.zip"

EXCLUDED_TOP_LEVEL = {
    ".git",
    ".github",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "configs",
    "storage",
    "plugins",
    "logs",
    "release",
    "build",
    "dist",
    "update",
}

EXCLUDED_FILES = {
    "Cardinal.ico",
    "backup.zip",
    "test.py",
}

EXCLUDED_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".log",
    ".zip",
}


def _is_excluded(path: Path) -> bool:
    name = path.name
    return name in EXCLUDED_TOP_LEVEL or name in EXCLUDED_FILES or path.suffix.lower() in EXCLUDED_SUFFIXES


def _safe_child(parent: Path, child: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def _remove_path(path: Path, root: Path) -> None:
    if not _safe_child(root, path):
        raise RuntimeError(f"Unsafe update path: {path}")
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def _copy_path(src: Path, dst: Path, root: Path) -> None:
    if not _safe_child(root, dst):
        raise RuntimeError(f"Unsafe update path: {dst}")
    if dst.exists():
        _remove_path(dst, root)
    if src.is_dir():
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "*.log", "*.zip"))
    else:
        shutil.copy2(src, dst)


def _find_source_root(extract_dir: Path) -> Path:
    dirs = [p for p in extract_dir.iterdir() if p.is_dir()]
    if len(dirs) != 1:
        raise RuntimeError("Не вдалося знайти папку проєкту в архіві.")
    source_root = dirs[0]
    if not (source_root / "main.py").exists():
        raise RuntimeError("В архиве не найден main.py.")
    return source_root


def _download_archive(repo: str, branch: str, zip_path: Path) -> str:
    archive_url = f"https://github.com/{repo}/archive/refs/heads/{branch}.zip"

    with urllib.request.urlopen(archive_url, timeout=60) as response:
        zip_path.write_bytes(response.read())

    return repo


def update_from_github(repo: str = REPO, branch: str = BRANCH) -> str:
    project_root = Path.cwd()
    repos = (repo, *FALLBACK_REPOS) if repo == REPO else (repo,)
    last_error: Exception | None = None

    with tempfile.TemporaryDirectory(prefix="fpcr-update-") as tmp:
        tmp_dir = Path(tmp)
        zip_path = tmp_dir / "source.zip"
        extract_dir = tmp_dir / "source"

        used_repo = ""
        for candidate_repo in repos:
            try:
                used_repo = _download_archive(candidate_repo, branch, zip_path)
                break
            except urllib.error.HTTPError as e:
                last_error = e
                if e.code != 404:
                    raise
            except urllib.error.URLError as e:
                last_error = e
        else:
            raise RuntimeError(f"Не удалось скачать обновление из {', '.join(repos)}: {last_error}")

        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(extract_dir)

        source_root = _find_source_root(extract_dir)
        source_names = {p.name for p in source_root.iterdir() if not _is_excluded(p)}

        for current in project_root.iterdir():
            if _is_excluded(current):
                continue
            if current.name not in source_names:
                _remove_path(current, project_root)

        for source in source_root.iterdir():
            if _is_excluded(source):
                continue
            _copy_path(source, project_root / source.name, project_root)

    return f"Обновление из {used_repo}@{branch} установлено."
