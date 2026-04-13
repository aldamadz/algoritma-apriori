from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
from time import perf_counter
from typing import List

from apriori import apriori, load_transactions_from_csv


def _parse_float_list(value: str) -> List[float]:
    parts = [p.strip() for p in value.split(",") if p.strip()]
    if not parts:
        raise ValueError("Daftar nilai tidak boleh kosong.")
    return [float(p) for p in parts]


def run_experiment(
    csv_path: str,
    supports: List[float],
    confidences: List[float],
    min_lift: float,
    transaction_id_col: str,
    item_col: str,
) -> List[dict]:
    transactions = load_transactions_from_csv(
        file_path=csv_path,
        transaction_id_col=transaction_id_col,
        item_col=item_col,
    )
    rows: List[dict] = []
    for s in supports:
        for c in confidences:
            t0 = perf_counter()
            frequent_itemsets, rules = apriori(
                transactions=transactions,
                min_support=s,
                min_confidence=c,
                min_lift=min_lift,
            )
            duration_ms = (perf_counter() - t0) * 1000
            rows.append(
                {
                    "min_support": s,
                    "min_confidence": c,
                    "min_lift": min_lift,
                    "frequent_itemsets_count": len(frequent_itemsets),
                    "rules_count": len(rules),
                    "max_lift": round(max((r.lift for r in rules), default=0.0), 6),
                    "avg_lift": round(
                        (sum(r.lift for r in rules) / len(rules)) if rules else 0.0, 6
                    ),
                    "runtime_ms": round(duration_ms, 3),
                }
            )
    return rows


def save_csv(rows: List[dict], output_file: Path) -> None:
    if not rows:
        return
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def try_plot(rows: List[dict], output_dir: Path) -> bool:
    mpl_cache = output_dir / ".mplconfig"
    mpl_cache.mkdir(parents=True, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(mpl_cache.resolve())

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    output_dir.mkdir(parents=True, exist_ok=True)

    x = [f"s={r['min_support']}, c={r['min_confidence']}" for r in rows]
    y_rules = [r["rules_count"] for r in rows]
    y_time = [r["runtime_ms"] for r in rows]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(x, y_rules, color="#0ea5e9")
    ax.set_title("Jumlah Rules per Kombinasi Parameter")
    ax.set_ylabel("Rules Count")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(output_dir / "rules_count.png", dpi=140)
    plt.close(fig)

    fig2, ax2 = plt.subplots(figsize=(12, 5))
    ax2.plot(x, y_time, marker="o", color="#f97316")
    ax2.set_title("Runtime Apriori per Kombinasi Parameter")
    ax2.set_ylabel("Runtime (ms)")
    ax2.tick_params(axis="x", rotation=45)
    fig2.tight_layout()
    fig2.savefig(output_dir / "runtime_ms.png", dpi=140)
    plt.close(fig2)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Eksperimen Apriori (parameter sweep + plot).")
    parser.add_argument("--csv", required=True, help="Path CSV transaksi (long format).")
    parser.add_argument("--supports", default="0.1,0.2,0.3", help="Daftar min_support, dipisah koma.")
    parser.add_argument("--confidences", default="0.5,0.6,0.7", help="Daftar min_confidence, dipisah koma.")
    parser.add_argument("--min-lift", type=float, default=0.0, help="Nilai minimum lift.")
    parser.add_argument("--transaction-id-col", default="transaction_id", help="Nama kolom transaction id.")
    parser.add_argument("--item-col", default="item", help="Nama kolom item.")
    parser.add_argument("--out-dir", default="experiment_output", help="Folder output eksperimen.")
    args = parser.parse_args()

    supports = _parse_float_list(args.supports)
    confidences = _parse_float_list(args.confidences)

    rows = run_experiment(
        csv_path=args.csv,
        supports=supports,
        confidences=confidences,
        min_lift=args.min_lift,
        transaction_id_col=args.transaction_id_col,
        item_col=args.item_col,
    )

    out_dir = Path(args.out_dir)
    csv_path = out_dir / "experiment_summary.csv"
    save_csv(rows, csv_path)
    print(f"Ringkasan eksperimen disimpan: {csv_path}")

    plotted = try_plot(rows, out_dir)
    if plotted:
        print(f"Grafik tersimpan di: {out_dir}")
    else:
        print("matplotlib tidak tersedia, grafik tidak dibuat.")


if __name__ == "__main__":
    main()
