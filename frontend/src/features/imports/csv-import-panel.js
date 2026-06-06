import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
export function CsvImportPanel({ onImported }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [resetting, setResetting] = useState(false);
    const [result, setResult] = useState(null);
    const [resetResult, setResetResult] = useState(null);
    const [error, setError] = useState("");
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
            const json = (await res.json());
            setResult(json);
            onImported?.();
        }
        catch (e) {
            setError(e instanceof Error ? e.message : "Import gagal.");
        }
        finally {
            setLoading(false);
        }
    };
    const handleReset = async () => {
        const confirmed = window.confirm("Hapus seluruh dataset, transaksi, buku, mahasiswa, fakultas, dan hasil analisis? Tindakan ini tidak dapat dibatalkan.");
        if (!confirmed)
            return;
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
            setResetResult(await res.json());
            setFile(null);
            onImported?.();
        }
        catch (e) {
            setError(e instanceof Error ? e.message : "Reset data gagal.");
        }
        finally {
            setResetting(false);
        }
    };
    return (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Import Dataset CSV" }) }), _jsxs(CardContent, { className: "space-y-3", children: [_jsxs("div", { className: "break-words text-xs text-slate-600", children: ["Kolom wajib: ", _jsx("code", { children: "transaction_id, student_number, department_code, loan_date, book_isbn" })] }), _jsx(Input, { type: "file", accept: ".csv", onChange: (e) => setFile(e.target.files?.[0] ?? null) }), _jsxs("div", { className: "flex flex-wrap gap-2", children: [_jsx(Button, { onClick: handleImport, disabled: loading || resetting, children: loading ? "Importing..." : "Import CSV" }), _jsx(Button, { variant: "outline", onClick: handleReset, disabled: loading || resetting, children: resetting ? "Membersihkan..." : "Bersihkan Semua Data" })] }), error ? _jsx("div", { className: "break-words text-sm text-red-600", children: error }) : null, result ? (_jsxs("div", { className: "space-y-1 text-sm", children: [_jsxs("div", { children: ["Total baris: ", result.totalRows] }), _jsxs("div", { children: ["Transaksi dibuat: ", result.createdTransactions] }), _jsxs("div", { children: ["Item transaksi dibuat: ", result.createdTransactionItems] }), _jsxs("div", { children: ["Department baru: ", result.createdDepartments] }), _jsxs("div", { children: ["Student baru: ", result.createdStudents] }), _jsxs("div", { children: ["Buku baru: ", result.createdBooks] }), _jsxs("div", { children: ["Transaksi duplikat dilewati: ", result.skippedDuplicateTransactions] }), _jsxs("div", { children: ["Duplikat lama dibersihkan: ", result.removedDuplicateTransactions] }), result.errors.length > 0 ? (_jsxs("div", { className: "break-words pt-1 text-amber-700", children: ["Error baris (", result.errors.length, "): ", result.errors.slice(0, 5).join(" | ")] })) : null] })) : null, resetResult ? (_jsxs("div", { className: "space-y-1 text-sm text-emerald-700", children: [_jsx("div", { children: "Database berhasil dibersihkan." }), _jsxs("div", { children: ["Transaksi dihapus: ", resetResult.deletedTransactions] }), _jsxs("div", { children: ["Item transaksi dihapus: ", resetResult.deletedTransactionItems] }), _jsxs("div", { children: ["Hasil analisis dihapus: ", resetResult.deletedAnalysisRuns] }), _jsxs("div", { children: ["Rules dihapus: ", resetResult.deletedRules] })] })) : null] })] }));
}
