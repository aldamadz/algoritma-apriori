import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import type { ImportCsvResult } from "@/types/api";

type Props = {
  onImported?: () => void;
};

export function CsvImportPanel({ onImported }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ImportCsvResult | null>(null);
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
        <Button onClick={handleImport} disabled={loading}>
          {loading ? "Importing..." : "Import CSV"}
        </Button>
        {error ? <div className="break-words text-sm text-red-600">{error}</div> : null}
        {result ? (
          <div className="space-y-1 text-sm">
            <div>Total baris: {result.totalRows}</div>
            <div>Transaksi dibuat: {result.createdTransactions}</div>
            <div>Item transaksi dibuat: {result.createdTransactionItems}</div>
            <div>Department baru: {result.createdDepartments}</div>
            <div>Student baru: {result.createdStudents}</div>
            <div>Buku baru: {result.createdBooks}</div>
            {result.errors.length > 0 ? (
              <div className="break-words pt-1 text-amber-700">
                Error baris ({result.errors.length}): {result.errors.slice(0, 5).join(" | ")}
              </div>
            ) : null}
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
