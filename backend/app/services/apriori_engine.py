from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from typing import Dict, FrozenSet, Iterable, Sequence, Set, Tuple

Itemset = FrozenSet[str]


@dataclass(frozen=True)
class AssociationRule:
    antecedent: Tuple[str, ...]
    consequent: Tuple[str, ...]
    support: float
    confidence: float
    lift: float
    support_count: int


def _normalize_transactions(transactions: Iterable[Iterable[str]]) -> list[Itemset]:
    normalized: list[Itemset] = []
    for txn in transactions:
        cleaned = frozenset(item.strip() for item in txn if item and item.strip())
        if cleaned:
            normalized.append(cleaned)
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
        ok = all(frozenset(subset) in prev_level for subset in combinations(candidate, k - 1))
        if ok:
            pruned.add(candidate)
    return pruned


def generate_frequent_itemsets(
    transactions: Iterable[Iterable[str]], min_support: float
) -> tuple[dict[Itemset, int], int]:
    txns = _normalize_transactions(transactions)
    if not txns:
        return {}, 0

    txn_count = len(txns)
    min_count = max(1, math.ceil(min_support * txn_count))

    item_counts: dict[Itemset, int] = defaultdict(int)
    for txn in txns:
        for item in txn:
            item_counts[frozenset([item])] += 1

    frequent_all: dict[Itemset, int] = {
        itemset: count for itemset, count in item_counts.items() if count >= min_count
    }
    current_level: set[Itemset] = set(frequent_all.keys())
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
    frequent_itemsets: dict[Itemset, int],
    transaction_count: int,
    min_confidence: float,
    min_lift: float = 0.0,
) -> list[AssociationRule]:
    if transaction_count == 0:
        return []
    rules: list[AssociationRule] = []
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
