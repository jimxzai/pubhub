#!/usr/bin/env python3
"""Install the audited local proof at its assigned path, with recovery copies."""
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[2]
NAME = "1cor-consolidated"

def main():
    subprocess.run(["python3", str(ROOT / "scripts/audit_outputs.py")], check=True)
    destination = PROJECT / "output"
    backup = Path(tempfile.mkdtemp(prefix="1cor-before-upgrade-", dir="/private/tmp"))
    print(f"Recovery copies: {backup}", flush=True)
    for extension in ("pdf", "html", "epub"):
        source = ROOT / "output" / extension / f"{NAME}.{extension}"
        target = destination / source.name
        if target.exists():
            shutil.copy2(target, backup / target.name)
        fd, temporary = tempfile.mkstemp(prefix=f".{NAME}-", dir=destination)
        os.close(fd)
        try:
            shutil.copy2(source, temporary)
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        assert hashlib.sha256(source.read_bytes()).digest() == hashlib.sha256(target.read_bytes()).digest()
        print(f"Verified: {target}")
    # Preserve the existing entry point but route it through the audited builder.
    builder = PROJECT / "scripts/build-1cor-consolidated.sh"
    if builder.exists():
        shutil.copy2(builder, backup / builder.name)
    shutil.copy2(ROOT / "scripts/build-1cor-consolidated.sh", builder)
    # Only obsolete generated intermediates from this book; no manuscript deletion.
    for name in ("1cor-combined.md", "1cor-consolidated.md", "1cor-consolidated-build.log"):
        stale = destination / name
        if stale.exists():
            shutil.move(str(stale), str(backup / name))

if __name__ == "__main__":
    main()
