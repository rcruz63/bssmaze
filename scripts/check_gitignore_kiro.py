"""Falla si `.kiro` queda ignorado por git (riesgo de descalificación en el hackathon)."""

import subprocess
import sys

# Rutas representativas: si alguna se ignora, el contenido de `.kiro/` no se subiría.
PROBE_PATHS = [".kiro", ".kiro/steering/product.md", ".kiro/specs/telnet-tales/tasks.md"]


def ignored_paths(paths: list[str]) -> list[str]:
    """Devuelve las rutas que git ignora (check-ignore sale con 1 si no ignora ninguna)."""
    result = subprocess.run(
        ["git", "check-ignore", *paths], capture_output=True, text=True, check=False
    )
    return result.stdout.split()


def main() -> int:
    ignored = ignored_paths(PROBE_PATHS)
    for path in ignored:
        print(f"ERROR: git ignora {path}; .kiro debe estar versionado")
    return 1 if ignored else 0


if __name__ == "__main__":
    sys.exit(main())
