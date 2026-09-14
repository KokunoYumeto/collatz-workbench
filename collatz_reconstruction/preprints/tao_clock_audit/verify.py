"""Verify the portable preprint's exact sources and finite certificate."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    files = manifest["files"]
    paths = [entry["path"] for entry in files]
    require(len(paths) == len(set(paths)), "Duplicate manifest path")
    for entry in files:
        relative = PurePosixPath(entry["path"])
        require(not relative.is_absolute() and ".." not in relative.parts and ":" not in str(relative), "Unsafe path")
        data = (ROOT / str(relative)).read_bytes()
        require(len(data) == entry["bytes"], "Length mismatch: " + str(relative))
        require(hashlib.sha256(data).hexdigest() == entry["sha256"], "Hash mismatch: " + str(relative))
    texts = {path: (ROOT / path).read_text(encoding="utf-8") for path in paths if path.endswith(".tex")}
    joined = "\n".join(texts.values())
    require(not re.search(r"(?<![A-Za-z])[A-Za-z]:/|file://|[A-Za-z]:\\(?:Users|user|Windows)\\", joined), "Nonportable TeX path")
    for text in texts.values():
        for name in re.findall(r"\\(?:input|include)\{([^}]+)\}", text):
            require(name + ".tex" in texts or name in texts, "Missing TeX input: " + name)
    labels = re.findall(r"\\label\{([^}]+)\}", joined)
    require(len(labels) == len(set(labels)), "Duplicate TeX label")
    refs = re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", joined)
    require(set(refs) <= set(labels), "Unresolved source labels: " + str(set(refs) - set(labels)))
    bib = set(re.findall(r"\\bibitem\{([^}]+)\}", joined))
    cites = set()
    for group in re.findall(r"\\cite(?:\[[^]]*\])?\{([^}]+)\}", joined):
        cites.update(group.split(","))
    require(cites <= bib, "Missing bibliographic keys")
    registry = json.loads((ROOT / "proof_registry.json").read_text(encoding="utf-8"))
    ids = {claim["id"] for claim in registry["claims"]}
    for claim in registry["claims"]:
        require(claim["tex_label"] in labels, "Missing proof location: " + claim["id"])
        require(set(claim["dependencies"]) <= ids, "Missing claim dependency: " + claim["id"])
    certificate = subprocess.run([sys.executable, str(ROOT / "certificates/check_finite.py")],
        capture_output=True, text=True, encoding="utf-8", check=True)
    result = json.loads(certificate.stdout)
    require(result["status"] == "PASS", "Finite certificate did not pass")
    print(json.dumps({"status": "PASS", "source_files": len(files), "tex_labels": len(labels),
        "bibliographic_keys_used": len(cites), "proof_records": len(ids), "finite_certificate": result}, indent=2))


if __name__ == "__main__":
    main()
