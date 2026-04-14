import os
import subprocess
from pathlib import Path


ROOT = Path(r"D:\Koding\algoritma apriori")
DIAGRAM_DIR = ROOT / "docs" / "diagrams"


def run_render(input_file: Path, output_file: Path) -> None:
    cmd = [
        "cmd",
        "/c",
        "npx",
        "@mermaid-js/mermaid-cli",
        "-i",
        str(input_file),
        "-o",
        str(output_file),
        "-b",
        "white",
    ]
    env = os.environ.copy()
    env["npm_config_cache"] = str(ROOT / ".npm-cache")
    env["npm_config_prefix"] = str(ROOT / ".npm-global")
    subprocess.run(cmd, check=True, env=env, cwd=str(ROOT))


def main() -> None:
    files = sorted(DIAGRAM_DIR.glob("diagram_*.mmd"))
    if not files:
        print("No .mmd files found.")
        return
    for f in files:
        png = f.with_suffix(".png")
        svg = f.with_suffix(".svg")
        run_render(f, png)
        run_render(f, svg)
        print(f"Rendered: {png.name}, {svg.name}")


if __name__ == "__main__":
    main()
