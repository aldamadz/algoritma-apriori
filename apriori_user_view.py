from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from apriori import AssociationRule, apriori, load_transactions_from_csv


def _fmt_items(items: tuple[str, ...]) -> str:
    return ", ".join(items)


def _print_rules_table(rules: List[AssociationRule], top_n: int) -> None:
    selected = rules[:top_n] if top_n > 0 else rules
    if not selected:
        print("Tidak ada rule yang lolos threshold.")
        return

    headers = ["No", "Rule", "Support", "Confidence", "Lift"]
    rows = []
    for i, rule in enumerate(selected, start=1):
        rule_text = f"IF [{_fmt_items(rule.antecedent)}] THEN [{_fmt_items(rule.consequent)}]"
        rows.append(
            [
                str(i),
                rule_text,
                f"{rule.support:.4f}",
                f"{rule.confidence:.4f}",
                f"{rule.lift:.4f}",
            ]
        )

    widths = [len(h) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(cell))

    def line(sep: str = "-") -> str:
        return "+" + "+".join(sep * (w + 2) for w in widths) + "+"

    print(line("-"))
    print("| " + " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers))) + " |")
    print(line("="))
    for row in rows:
        print("| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(row))) + " |")
    print(line("-"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Apriori output untuk user (tabel + JSON opsional).")
    parser.add_argument("--csv", required=True, help="Path CSV transaksi (long format).")
    parser.add_argument("--min-support", type=float, required=True, help="Nilai support (0-1).")
    parser.add_argument("--min-confidence", type=float, required=True, help="Nilai confidence (0-1).")
    parser.add_argument("--min-lift", type=float, default=0.0, help="Nilai minimum lift.")
    parser.add_argument("--top-n", type=int, default=20, help="Tampilkan top N rule di terminal (0 = semua).")
    parser.add_argument("--transaction-id-col", default="transaction_id", help="Nama kolom transaction id.")
    parser.add_argument("--item-col", default="item", help="Nama kolom item.")
    parser.add_argument("--json-out", default="", help="Simpan output JSON untuk backend.")
    args = parser.parse_args()

    transactions = load_transactions_from_csv(
        file_path=args.csv,
        transaction_id_col=args.transaction_id_col,
        item_col=args.item_col,
    )

    frequent_itemsets, rules = apriori(
        transactions=transactions,
        min_support=args.min_support,
        min_confidence=args.min_confidence,
        min_lift=args.min_lift,
    )

    print(f"Total frequent itemsets: {len(frequent_itemsets)}")
    print(f"Total association rules: {len(rules)}")
    print()
    _print_rules_table(rules, top_n=args.top_n)

    if args.json_out:
        payload = {
            "summary": {
                "frequent_itemsets_count": len(frequent_itemsets),
                "association_rules_count": len(rules),
                "min_support": args.min_support,
                "min_confidence": args.min_confidence,
                "min_lift": args.min_lift,
            },
            "association_rules": [
                {
                    "antecedent": list(rule.antecedent),
                    "consequent": list(rule.consequent),
                    "support": round(rule.support, 6),
                    "confidence": round(rule.confidence, 6),
                    "lift": round(rule.lift, 6),
                    "support_count": rule.support_count,
                }
                for rule in rules
            ],
        }
        output_path = Path(args.json_out)
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nJSON backend disimpan ke: {output_path}")


if __name__ == "__main__":
    main()
