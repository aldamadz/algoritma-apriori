import tempfile
import unittest
from pathlib import Path

from dataset_workflow import infer_dataset_config, prepare_dataset


class DatasetWorkflowTests(unittest.TestCase):
    def write_csv(self, content: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "dataset.csv"
        path.write_text(content, encoding="utf-8")
        return path

    def test_infers_simple_transaction_item_format(self) -> None:
        config = infer_dataset_config(("transaction_id", "item"))

        self.assertEqual(config.transaction_key_cols, ("transaction_id",))
        self.assertEqual(config.item_specs, (("item", ""),))

    def test_prepares_library_import_format(self) -> None:
        path = self.write_csv(
            "transaction_id,department_code,book_title\n"
            "T1,TI,Python\n"
            "T1,TI,Database\n"
            "T1,TI,Python\n"
            "T2,SI,Database\n"
        )

        transactions, config, summary = prepare_dataset(path)

        self.assertEqual(config.transaction_key_cols, ("transaction_id",))
        self.assertEqual(summary.row_count, 4)
        self.assertEqual(summary.duplicate_row_count, 1)
        self.assertEqual(summary.transaction_count, 2)
        self.assertEqual(
            transactions,
            [
                ["Jurusan:TI", "Buku:Python", "Buku:Database"],
                ["Jurusan:SI", "Buku:Database"],
            ],
        )

    def test_supports_manual_column_mapping(self) -> None:
        path = self.write_csv(
            "customer,date,product\n"
            "C1,2026-01-01,Tea\n"
            "C1,2026-01-01,Cake\n"
            "C2,2026-01-02,Coffee\n"
        )

        transactions, config, summary = prepare_dataset(
            path,
            transaction_key_cols=("customer", "date"),
            item_specs=(("product", "Produk"),),
        )

        self.assertEqual(config.format_name, "konfigurasi manual")
        self.assertEqual(summary.transaction_count, 2)
        self.assertEqual(
            transactions,
            [["Produk:Tea", "Produk:Cake"], ["Produk:Coffee"]],
        )


if __name__ == "__main__":
    unittest.main()
