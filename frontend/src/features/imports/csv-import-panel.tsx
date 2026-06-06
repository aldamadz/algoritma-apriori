import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import type { ImportCsvResult, ResetDataResult } from "@/types/api";

type Props = {
  onImported?: () => void;
};

export function CsvImportPanel({ onImported }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [resetting, setResetting] = useState(false);
  const [result, setResult] = useState<ImportCsvResult | null>(null);
  const [resetResult, setResetResult] = useState<ResetDataResult | null>(null);
  const [error, setError] = useState<string>("");

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
        <div className="flex flex-wrap gap-2">
          <Button onClick={handleImport} disabled={loading || resetting}>
            {loading ? "Importing..." : "Import CSV"}
          </Button>
          <Button variant="outline" onClick={handleReset} disabled={loading || resetting}>
            {resetting ? "Membersihkan..." : "Bersihkan Semua Data"}
          </Button>
        </div>
        {error ? <div className="break-words text-sm text-red-600">{error}</div> : null}
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
