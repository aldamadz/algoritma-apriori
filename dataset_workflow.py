from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from apriori import ItemColumnSpec, load_transactions_from_csv_multi


@dataclass(frozen=True)
class DatasetConfig:
    transaction_key_cols: tuple[str, ...]
    item_specs: tuple[ItemColumnSpec, ...]
    format_name: str


@dataclass(frozen=True)
class DatasetSummary:
    file_path: Path
    columns: tuple[str, ...]
    row_count: int
    duplicate_row_count: int
    transaction_count: int
    empty_transaction_count: int
    min_items: int
    max_items: int
    average_items: float


KNOWN_FORMATS: tuple[DatasetConfig, ...] = (
    DatasetConfig(
        transaction_key_cols=("transaction_id",),
        item_specs=(("department_code", "Jurusan"), ("book_title", "Buku")),
        format_name="dataset import perpustakaan",
    ),
    DatasetConfig(
        transaction_key_cols=("no_mhs", "tgl_pinjam"),
        item_specs=(("fakultas", "Fakultas"), ("judul", "Buku")),
        format_name="dataset peminjaman UIN",
    ),
    DatasetConfig(
        transaction_key_cols=("transaction_id",),
        item_specs=(("item", ""),),
        format_name="transaksi-item sederhana",
    ),
)


def inspect_csv(file_path: str | Path) -> tuple[tuple[str, ...], int, int]:
    path = Path(file_path)
    if path.suffix.lower() != ".csv":
        raise ValueError("Dataset harus berupa file CSV.")
    if not path.exists():
        raise FileNotFoundError(f"Dataset tidak ditemukan: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = tuple(reader.fieldnames or ())
        if not columns:
            raise ValueError("CSV tidak memiliki header kolom.")

        row_count = 0
        duplicate_count = 0
        seen_rows: set[tuple[str, ...]] = set()
        for row in reader:
            row_count += 1
            row_values = tuple((row.get(column) or "").strip() for column in columns)
            if row_values in seen_rows:
                duplicate_count += 1
            else:
                seen_rows.add(row_values)

    if row_count == 0:
        raise ValueError("CSV tidak memiliki baris data.")
    return columns, row_count, duplicate_count


def infer_dataset_config(columns: Sequence[str]) -> DatasetConfig:
    available = set(columns)
    for config in KNOWN_FORMATS:
        required = set(config.transaction_key_cols)
        required.update(column for column, _ in config.item_specs)
        if required.issubset(available):
            return config

    available_text = ", ".join(columns)
    raise ValueError(
        "Format kolom belum dikenali otomatis. Isi TRANSACTION_KEY_COLS dan ITEM_SPECS "
        f"secara manual. Kolom tersedia: {available_text}"
    )


def validate_dataset_config(
    columns: Sequence[str],
    transaction_key_cols: Sequence[str],
    item_specs: Sequence[ItemColumnSpec],
) -> None:
    if not transaction_key_cols:
        raise ValueError("Minimal satu kolom key transaksi harus dipilih.")
    if not item_specs:
        raise ValueError("Minimal satu kolom item harus dipilih.")

    available = set(columns)
    required = [*transaction_key_cols, *(column for column, _ in item_specs)]
    missing = sorted({column for column in required if column not in available})
    if missing:
        raise ValueError(
            f"Kolom konfigurasi tidak ditemukan: {', '.join(missing)}. "
            f"Kolom tersedia: {', '.join(columns)}"
        )


def prepare_dataset(
    file_path: str | Path,
    transaction_key_cols: Sequence[str] | None = None,
    item_specs: Sequence[ItemColumnSpec] | None = None,
) -> tuple[list[list[str]], DatasetConfig, DatasetSummary]:
    path = Path(file_path).resolve()
    columns, row_count, duplicate_count = inspect_csv(path)

    inferred = (
        infer_dataset_config(columns)
        if transaction_key_cols is None or item_specs is None
        else None
    )
    config = DatasetConfig(
        transaction_key_cols=tuple(
            transaction_key_cols
            if transaction_key_cols is not None
            else inferred.transaction_key_cols
        ),
        item_specs=tuple(item_specs if item_specs is not None else inferred.item_specs),
        format_name=inferred.format_name if inferred is not None else "konfigurasi manual",
    )
    validate_dataset_config(columns, config.transaction_key_cols, config.item_specs)

    transactions = load_transactions_from_csv_multi(
        file_path=path,
        transaction_key_cols=config.transaction_key_cols,
        item_specs=config.item_specs,
    )
    if not transactions:
        raise ValueError("Tidak ada transaksi valid setelah preprocessing.")

    item_counts = [len(transaction) for transaction in transactions]
    summary = DatasetSummary(
        file_path=path,
        columns=columns,
        row_count=row_count,
        duplicate_row_count=duplicate_count,
        transaction_count=len(transactions),
        empty_transaction_count=sum(1 for count in item_counts if count == 0),
        min_items=min(item_counts),
        max_items=max(item_counts),
        average_items=sum(item_counts) / len(item_counts),
    )
    return transactions, config, summary


def print_dataset_summary(config: DatasetConfig, summary: DatasetSummary) -> None:
    item_labels = [
        f"{column} -> {prefix or '(tanpa prefix)'}" for column, prefix in config.item_specs
    ]
    print("Dataset:", summary.file_path)
    print("Format:", config.format_name)
    print("Kolom:", ", ".join(summary.columns))
    print("Key transaksi:", " + ".join(config.transaction_key_cols))
    print("Kolom item:", "; ".join(item_labels))
    print("Baris CSV:", summary.row_count)
    print("Duplikat baris:", summary.duplicate_row_count)
    print("Transaksi valid:", summary.transaction_count)
    print(
        "Item per transaksi: "
        f"min={summary.min_items}, max={summary.max_items}, "
        f"rata-rata={summary.average_items:.2f}"
    )
