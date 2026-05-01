"""render_plantuml.py — minimal PlantUML CLI invoker.

Renders PlantUML source to PNG via `plantuml.jar` (Java) or the `plantuml`
shell wrapper. Detects availability lazily so import never fails when Java
or the jar is missing.

Layout: the engine writes the source to a temp `.puml` file, calls
`java -jar plantuml.jar -tpng -o <abs_out_dir> <input.puml>`, then moves
the resulting `<stem>.png` to the requested output path.

PlantUML produces dramatically cleaner architecture / network / sequence
diagrams than Mermaid (graphviz dot layout) — recommended for any
diagram with >10 nodes or layered structure.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

# Common locations the jar may be installed to (Debian/Ubuntu apt installs
# under /usr/share/plantuml/plantuml.jar; we also support an env-var
# override + a local download next to the package).
_DEFAULT_JAR_PATHS = (
    "/usr/share/plantuml/plantuml.jar",
    "/opt/plantuml/plantuml.jar",
    "/app/plantuml.jar",
)


def find_plantuml() -> dict | None:
    """Return {'mode': 'cli'|'jar', 'cmd': [...]} or None if unavailable.

    Detection order:
      1. ``PLANTUML_JAR`` env var → use ``java -jar <path>``
      2. ``plantuml`` on PATH (Debian wrapper) → ``plantuml`` command
      3. Default jar paths → ``java -jar <path>``
    """
    env_jar = os.environ.get("PLANTUML_JAR")
    if env_jar and Path(env_jar).is_file():
        java = shutil.which("java")
        if java:
            return {"mode": "jar", "cmd": [java, "-Djava.awt.headless=true", "-jar", env_jar]}

    cli = shutil.which("plantuml")
    if cli:
        return {"mode": "cli", "cmd": [cli]}

    for jar in _DEFAULT_JAR_PATHS:
        if Path(jar).is_file():
            java = shutil.which("java")
            if java:
                return {"mode": "jar", "cmd": [java, "-Djava.awt.headless=true", "-jar", jar]}

    return None


def check_plantuml() -> dict | None:
    """Lightweight availability probe — same return shape as find_plantuml.

    Kept separate so callers can cache the result without re-scanning paths.
    """
    return find_plantuml()


def render_one(plantuml_spec: dict, source: str, out_png: Path) -> tuple[bool, str]:
    """Render one PlantUML source string to ``out_png``.

    The source MUST start with ``@startuml`` (or any other ``@start*`` PlantUML
    directive — ``@startmindmap``, ``@startgantt``, ``@startwbs``, etc.). If
    not present the function wraps it implicitly so authors can omit the
    boilerplate when emitting via JSON.

    Returns (ok, error_message).
    """
    if not plantuml_spec:
        return False, "PlantUML not available (no jar / cli detected)"

    src = (source or "").strip()
    if not src:
        return False, "Empty PlantUML source"

    # Wrap if author omitted @start...@end markers. Default to @startuml.
    if not src.startswith("@start"):
        src = f"@startuml\n{src}\n@enduml\n"
    elif not any(end in src for end in ("@enduml", "@endmindmap", "@endgantt", "@endwbs", "@endsalt", "@endjson", "@endyaml")):
        # Has @start but missing end → close with the matching @end{kind}
        first_line = src.splitlines()[0].strip()
        kind = first_line.replace("@start", "")
        src = f"{src.rstrip()}\n@end{kind}\n"

    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        in_file = td_path / f"{out_png.stem}.puml"
        in_file.write_text(src, encoding="utf-8")

        # Force PNG output, charset utf-8 (Vietnamese diacritics), output dir = td
        cmd = list(plantuml_spec["cmd"]) + [
            "-charset", "UTF-8",
            "-tpng",
            "-failfast2",
            "-o", str(td_path),
            str(in_file),
        ]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )
        except (FileNotFoundError, OSError) as exc:
            return False, f"PlantUML invocation failed: {exc}"
        except subprocess.TimeoutExpired:
            return False, "PlantUML timed out (>120s)"

        if proc.returncode != 0:
            err = (proc.stderr or proc.stdout or "").strip()[:500]
            return False, f"PlantUML exit {proc.returncode}: {err}"

        produced = td_path / f"{in_file.stem}.png"
        if not produced.exists():
            # PlantUML may emit different filename if @startgantt / wbs etc.
            # Fall back to first .png in td_path.
            pngs = sorted(td_path.glob("*.png"))
            if not pngs:
                return False, "PlantUML produced no PNG output"
            produced = pngs[0]

        try:
            shutil.copyfile(produced, out_png)
        except OSError as exc:
            return False, f"Cannot copy output: {exc}"

    return True, ""


__all__ = ["find_plantuml", "check_plantuml", "render_one"]
