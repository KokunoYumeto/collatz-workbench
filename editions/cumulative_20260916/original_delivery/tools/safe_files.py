"""Small add-only file writer. No Git command or overwrite operation is used."""
from __future__ import annotations
from pathlib import Path, PurePosixPath
from typing import Mapping
import os


def destination_path(root: Path, name: str) -> Path:
    p = PurePosixPath(name)
    if not name or p.is_absolute() or '..' in p.parts or '.git' in p.parts or '\\' in name:
        raise ValueError(f'Unsafe relative path: {name!r}')
    root = root.absolute()
    # Reject symlinks, including a symlink at or above the target root.
    for item in (root, *root.parents):
        if item.is_symlink():
            raise ValueError(f'Symlink ancestor: {item}')
    target = root.joinpath(*p.parts)
    for item in (target, *target.parents):
        if item == root.parent:
            break
        if item.is_symlink():
            raise ValueError(f'Symlink destination: {item}')
    return target


def preflight(root: Path, payload: Mapping[str, bytes]) -> dict:
    added, identical = [], []
    for name, data in sorted(payload.items()):
        target = destination_path(root, name)
        for parent in target.parents:
            if parent.exists() and not parent.is_dir():
                raise ValueError(f'Non-directory parent: {parent}')
            if parent == root.absolute():
                break
        if target.exists():
            if not target.is_file() or target.read_bytes() != data:
                raise ValueError(f'Conflicting existing destination: {target}')
            identical.append(name)
        else:
            added.append(name)
    return {'add': added, 'identical': identical}


def apply_additions(root: Path, payload: Mapping[str, bytes], *, apply: bool) -> dict:
    plan = preflight(root, payload)  # ALL destinations checked before any write.
    if not apply:
        return {**plan, 'written': 0, 'dry_run': True}
    for name in plan['add']:
        target = destination_path(root, name)  # recheck; exclusive-create refuses races.
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as f:
            f.write(payload[name])
    return {**plan, 'written': len(plan['add']), 'dry_run': False}
