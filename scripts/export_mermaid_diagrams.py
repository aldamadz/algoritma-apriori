from pathlib import Path


SOURCE = Path(r"D:\Koding\algoritma apriori\docs\Diagram_Skripsi_Apriori.md")
OUT_DIR = Path(r"D:\Koding\algoritma apriori\docs\diagrams")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    text = SOURCE.read_text(encoding="utf-8")
    marker = "```mermaid"
    pos = 0
    idx = 0
    while True:
        start = text.find(marker, pos)
        if start == -1:
            break
        content_start = start + len(marker)
        end = text.find("```", content_start)
        if end == -1:
            break
        code = text[content_start:end].strip() + "\n"
        idx += 1
        name = f"diagram_{idx:02d}"
        (OUT_DIR / f"{name}.mmd").write_text(code, encoding="utf-8")
        pos = end + 3
    print(f"Exported {idx} diagrams to {OUT_DIR}")


if __name__ == "__main__":
    main()
