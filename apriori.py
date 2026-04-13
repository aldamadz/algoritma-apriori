from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, List, Sequence, Set, Tuple


Itemset = FrozenSet[str]


@dataclass(frozen=True)
class FrequentItemset:
    items: Tuple[str, ...]
    support_count: int
    support: float


@dataclass(frozen=True)
class AssociationRule:
    antecedent: Tuple[str, ...]
    consequent: Tuple[str, ...]
    support: float
    confidence: float
    lift: float
    support_count: int


def _validate_threshold(name: str, value: float) -> None:
    if value <= 0 or value > 1:
        raise ValueError(f"{name} must be in (0, 1]. Got {value}.")


def _normalize_transactions(transactions: Iterable[Iterable[str]]) -> List[Itemset]:
    normalized: List[Itemset] = []
    for txn in transactions:
        cleaned = frozenset(item.strip() for item in txn if item and item.strip())
        if cleaned:
            normalized.append(cleaned)
    if not normalized:
        raise ValueError("No valid transactions found.")
    return normalized


def _support_count(candidates: Set[Itemset], transactions: Sequence[Itemset]) -> Dict[Itemset, int]:
    counts: Dict[Itemset, int] = defaultdict(int)
    for txn in transactions:
        for candidate in candidates:
            if candidate.issubset(txn):
                counts[candidate] += 1
    return counts


def _join_step(prev_level: Set[Itemset], k: int) -> Set[Itemset]:
    candidates: Set[Itemset] = set()
    prev_list = list(prev_level)
    for i in range(len(prev_list)):
        for j in range(i + 1, len(prev_list)):
            union = prev_list[i] | prev_list[j]
            if len(union) == k:
                candidates.add(union)
    return candidates


def _prune_candidates(candidates: Set[Itemset], prev_level: Set[Itemset], k: int) -> Set[Itemset]:
    pruned: Set[Itemset] = set()
    for candidate in candidates:
        all_subsets_frequent = all(
            frozenset(subset) in prev_level for subset in combinations(candidate, k - 1)
        )
        if all_subsets_frequent:
            pruned.add(candidate)
    return pruned


def generate_frequent_itemsets(
    transactions: Iterable[Iterable[str]],
    min_support: float,
) -> Tuple[Dict[Itemset, int], int]:
    _validate_threshold("min_support", min_support)
    txns = _normalize_transactions(transactions)
    txn_count = len(txns)
    min_count = max(1, math.ceil(min_support * txn_count))

    # L1
    item_counts: Dict[Itemset, int] = defaultdict(int)
    for txn in txns:
        for item in txn:
            item_counts[frozenset([item])] += 1

    frequent_all: Dict[Itemset, int] = {
        itemset: count for itemset, count in item_counts.items() if count >= min_count
    }
    current_level: Set[Itemset] = set(frequent_all.keys())
    k = 2

    while current_level:
        candidates = _join_step(current_level, k)
        if not candidates:
            break
        candidates = _prune_candidates(candidates, current_level, k)
        if not candidates:
            break

        candidate_counts = _support_count(candidates, txns)
        next_level = {
            itemset for itemset, count in candidate_counts.items() if count >= min_count
        }
        for itemset in next_level:
            frequent_all[itemset] = candidate_counts[itemset]
        current_level = next_level
        k += 1

    return frequent_all, txn_count


def generate_association_rules(
    frequent_itemsets: Dict[Itemset, int],
    transaction_count: int,
    min_confidence: float,
    min_lift: float = 0.0,
) -> List[AssociationRule]:
    _validate_threshold("min_confidence", min_confidence)
    if min_lift < 0:
        raise ValueError(f"min_lift must be >= 0. Got {min_lift}.")

    rules: List[AssociationRule] = []
    for itemset, itemset_count in frequent_itemsets.items():
        if len(itemset) < 2:
            continue

        for size in range(1, len(itemset)):
            for antecedent_tuple in combinations(itemset, size):
                antecedent = frozenset(antecedent_tuple)
                consequent = itemset - antecedent

                antecedent_count = frequent_itemsets.get(antecedent)
                consequent_count = frequent_itemsets.get(consequent)
                if not antecedent_count or not consequent_count:
                    continue

                support = itemset_count / transaction_count
                confidence = itemset_count / antecedent_count
                consequent_support = consequent_count / transaction_count
                if consequent_support == 0:
                    continue
                lift = confidence / consequent_support

                if confidence >= min_confidence and lift >= min_lift:
                    rules.append(
                        AssociationRule(
                            antecedent=tuple(sorted(antecedent)),
                            consequent=tuple(sorted(consequent)),
                            support=support,
                            confidence=confidence,
                            lift=lift,
                            support_count=itemset_count,
                        )
                    )

    rules.sort(key=lambda r: (r.lift, r.confidence, r.support), reverse=True)
    return rules


def apriori(
    transactions: Iterable[Iterable[str]],
    min_support: float,
    min_confidence: float,
    min_lift: float = 0.0,
) -> Tuple[List[FrequentItemset], List[AssociationRule]]:
    frequent_raw, txn_count = generate_frequent_itemsets(transactions, min_support=min_support)
    frequent_list = [
        FrequentItemset(
            items=tuple(sorted(itemset)),
            support_count=count,
            support=count / txn_count,
        )
        for itemset, count in frequent_raw.items()
    ]
    frequent_list.sort(key=lambda x: (len(x.items), x.support, x.items), reverse=False)

    rules = generate_association_rules(
        frequent_itemsets=frequent_raw,
        transaction_count=txn_count,
        min_confidence=min_confidence,
        min_lift=min_lift,
    )
    return frequent_list, rules


def load_transactions_from_csv(
    file_path: str | Path,
    transaction_id_col: str = "transaction_id",
    item_col: str = "item",
) -> List[List[str]]:
    grouped: Dict[str, List[str]] = defaultdict(list)
    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if transaction_id_col not in (reader.fieldnames or []):
            raise ValueError(f"Column '{transaction_id_col}' not found in CSV.")
        if item_col not in (reader.fieldnames or []):
            raise ValueError(f"Column '{item_col}' not found in CSV.")
        for row in reader:
            txn_id = (row.get(transaction_id_col) or "").strip()
            item = (row.get(item_col) or "").strip()
            if txn_id and item:
                grouped[txn_id].append(item)

    return [items for _, items in sorted(grouped.items(), key=lambda x: x[0])]


def _to_jsonable(frequent: List[FrequentItemset], rules: List[AssociationRule]) -> dict:
    return {
        "frequent_itemsets": [
            {
                "items": list(fi.items),
                "support_count": fi.support_count,
                "support": round(fi.support, 6),
            }
            for fi in frequent
        ],
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Apriori association rule miner.")
    parser.add_argument("--csv", required=True, help="Path CSV transaksi (long format).")
    parser.add_argument("--min-support", type=float, required=True, help="Nilai support (0-1).")
    parser.add_argument("--min-confidence", type=float, required=True, help="Nilai confidence (0-1).")
    parser.add_argument("--min-lift", type=float, default=0.0, help="Nilai minimum lift (default 0).")
    parser.add_argument("--transaction-id-col", default="transaction_id", help="Nama kolom transaction id.")
    parser.add_argument("--item-col", default="item", help="Nama kolom item.")
    parser.add_argument("--output", default="", help="Path output JSON (opsional).")
    args = parser.parse_args()

    transactions = load_transactions_from_csv(
        file_path=args.csv,
        transaction_id_col=args.transaction_id_col,
        item_col=args.item_col,
    )
    frequent, rules = apriori(
        transactions=transactions,
        min_support=args.min_support,
        min_confidence=args.min_confidence,
        min_lift=args.min_lift,
    )
    result = _to_jsonable(frequent, rules)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
