import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import type { ClearDatasetResult, ImportCsvResult } from "@/types/api";

type Props = {
  onImported?: () => void;
};

const importSteps = [
  "Validasi file CSV",
  "Membaca isi file",
  "Mendeteksi format kolom dataset",
  "Preprocessing: normalisasi jurusan, mahasiswa, buku, dan tanggal",
  "Mengelompokkan baris menjadi transaksi peminjaman",
  "Menyimpan data master mahasiswa, jurusan, dan buku",
  "Menyimpan transaksi peminjaman dan item buku",
  "Finalisasi hasil import",
];

export function CsvImportPanel({ onImported }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [clearing, setClearing] = useState(false);
  const [stepIndex, setStepIndex] = useState(0);
  const [result, setResult] = useState<ImportCsvResult | null>(null);
  const [clearResult, setClearResult] = useState<ClearDatasetResult | null>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    if (!loading) return;

    setStepIndex(0);
    const timer = window.setInterval(() => {
      setStepIndex((current) => Math.min(current + 1, importSteps.length - 1));
    }, 900);

    return () => window.clearInterval(timer);
  }, [loading]);

  const clearDataset = async () => {
    const confirmed = window.confirm(
      "Kosongkan semua data import dan riwayat analisis? Gunakan ini sebelum import dataset baru."
    );
    if (!confirmed) return;

    setClearing(true);
    setError("");
    setResult(null);
    setClearResult(null);
    try {
      const base = import.meta.env.VITE_API_BASE_URL ?? "";
      const res = await fetch(`${base}/api/transactions/dataset`, { method: "DELETE" });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `HTTP ${res.status}`);
      }
      setClearResult((await res.json()) as ClearDatasetResult);
      onImported?.();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Gagal mengosongkan dataset.");
    } finally {
      setClearing(false);
    }
  };

  const handleImport = async () => {
    if (!file) {
      setError("Pilih file CSV dulu.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const base = import.meta.env.VITE_API_BASE_URL ?? "";
      const formData = new FormData();
      formData.append("file", file);
      const res = await fetch(`${base}/api/transactions/import-csv`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `HTTP ${res.status}`);
      }
      const json = (await res.json()) as ImportCsvResult;
      setResult(json);
      setStepIndex(importSteps.length - 1);
      onImported?.();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Import gagal.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    const confirmed = window.confirm(
      "Hapus seluruh dataset, transaksi, buku, mahasiswa, fakultas, dan hasil analisis? Tindakan ini tidak dapat dibatalkan.",
    );
    if (!confirmed) return;

    setResetting(true);
    setError("");
    setResult(null);
    setResetResult(null);
    try {
      const base = import.meta.env.VITE_API_BASE_URL ?? "";
      const res = await fetch(`${base}/api/transactions/all-data`, {
        method: "DELETE",
        headers: { "X-Confirm-Reset": "RESET ALL DATA" },
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `HTTP ${res.status}`);
      }
      const json = (await res.json()) as ResetDataResult;
      setResetResult(json);
      setFile(null);
      onImported?.();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Reset data gagal.");
    } finally {
      setResetting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Import Dataset CSV</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="break-words text-xs text-slate-600">
          Kolom wajib: <code>transaction_id, student_number, department_code, loan_date, book_isbn</code>
        </div>
        <Input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <div className="flex flex-col gap-2 sm:flex-row">
          <Button onClick={handleImport} disabled={loading || clearing}>
            {loading ? "Mengimport..." : "Import CSV"}
          </Button>
          <Button variant="outline" onClick={() => void clearDataset()} disabled={loading || clearing}>
            {clearing ? "Mengosongkan..." : "Kosongkan Dataset"}
          </Button>
        </div>
        {loading ? (
          <div className="rounded-md border bg-slate-50 p-3 text-sm">
            <div className="font-medium">Preprocessing dataset...</div>
            <div className="mt-2 space-y-1">
              {importSteps.map((step, index) => (
                <div
                  key={step}
                  className={index <= stepIndex ? "text-slate-900" : "text-slate-400"}
                >
                  {index < stepIndex ? "✓" : index === stepIndex ? "•" : "○"} {step}
                </div>
              ))}
            </div>
          </div>
        ) : null}
        {error ? <div className="break-words text-sm text-red-600">{error}</div> : null}
        {clearResult ? (
          <div className="space-y-1 rounded-md border bg-amber-50 p-3 text-sm text-amber-900">
            <div>Dataset berhasil dikosongkan.</div>
            <div>Transaksi dihapus: {clearResult.deletedTransactions}</div>
            <div>Buku dihapus: {clearResult.deletedBooks}</div>
            <div>Mahasiswa dihapus: {clearResult.deletedStudents}</div>
            <div>Jurusan dihapus: {clearResult.deletedDepartments}</div>
            <div>Riwayat analisis dihapus: {clearResult.deletedAnalysisRuns}</div>
          </div>
        ) : null}
        {result ? (
          <div className="space-y-1 text-sm">
            <div>Total baris: {result.totalRows}</div>
            <div>Transaksi dibuat: {result.createdTransactions}</div>
            <div>Item transaksi dibuat: {result.createdTransactionItems}</div>
            <div>Department baru: {result.createdDepartments}</div>
            <div>Student baru: {result.createdStudents}</div>
            <div>Buku baru: {result.createdBooks}</div>
            <div>Transaksi duplikat dilewati: {result.skippedDuplicateTransactions}</div>
            <div>Duplikat lama dibersihkan: {result.removedDuplicateTransactions}</div>
            {result.errors.length > 0 ? (
              <div className="break-words pt-1 text-amber-700">
                Error baris ({result.errors.length}): {result.errors.slice(0, 5).join(" | ")}
              </div>
            ) : null}
          </div>
        ) : null}
        {resetResult ? (
          <div className="space-y-1 text-sm text-emerald-700">
            <div>Database berhasil dibersihkan.</div>
            <div>Transaksi dihapus: {resetResult.deletedTransactions}</div>
            <div>Item transaksi dihapus: {resetResult.deletedTransactionItems}</div>
            <div>Hasil analisis dihapus: {resetResult.deletedAnalysisRuns}</div>
            <div>Rules dihapus: {resetResult.deletedRules}</div>
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
