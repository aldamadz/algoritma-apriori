import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
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
export function CsvImportPanel({ onImported }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [clearing, setClearing] = useState(false);
    const [stepIndex, setStepIndex] = useState(0);
    const [result, setResult] = useState(null);
    const [clearResult, setClearResult] = useState(null);
    const [error, setError] = useState("");
    useEffect(() => {
        if (!loading)
            return;
        setStepIndex(0);
        const timer = window.setInterval(() => {
            setStepIndex((current) => Math.min(current + 1, importSteps.length - 1));
        }, 900);
        return () => window.clearInterval(timer);
    }, [loading]);
    const clearDataset = async () => {
        const confirmed = window.confirm("Kosongkan semua data import dan riwayat analisis? Gunakan ini sebelum import dataset baru.");
        if (!confirmed)
            return;
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
            setClearResult((await res.json()));
            onImported?.();
        }
        catch (e) {
            setError(e instanceof Error ? e.message : "Gagal mengosongkan dataset.");
        }
        finally {
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
            const json = (await res.json());
            setResult(json);
            setStepIndex(importSteps.length - 1);
            onImported?.();
        }
        catch (e) {
            setError(e instanceof Error ? e.message : "Import gagal.");
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Import Dataset CSV" }) }), _jsxs(CardContent, { className: "space-y-3", children: [_jsxs("div", { className: "break-words text-xs text-slate-600", children: ["Kolom wajib: ", _jsx("code", { children: "transaction_id, student_number, department_code, loan_date, book_isbn" })] }), _jsx(Input, { type: "file", accept: ".csv", onChange: (e) => setFile(e.target.files?.[0] ?? null) }), _jsxs("div", { className: "flex flex-col gap-2 sm:flex-row", children: [_jsx(Button, { onClick: handleImport, disabled: loading || clearing, children: loading ? "Mengimport..." : "Import CSV" }), _jsx(Button, { variant: "outline", onClick: () => void clearDataset(), disabled: loading || clearing, children: clearing ? "Mengosongkan..." : "Kosongkan Dataset" })] }), loading ? (_jsxs("div", { className: "rounded-md border bg-slate-50 p-3 text-sm", children: [_jsx("div", { className: "font-medium", children: "Preprocessing dataset..." }), _jsx("div", { className: "mt-2 space-y-1", children: importSteps.map((step, index) => (_jsxs("div", { className: index <= stepIndex ? "text-slate-900" : "text-slate-400", children: [index < stepIndex ? "✓" : index === stepIndex ? "•" : "○", " ", step] }, step))) })] })) : null, error ? _jsx("div", { className: "break-words text-sm text-red-600", children: error }) : null, clearResult ? (_jsxs("div", { className: "space-y-1 rounded-md border bg-amber-50 p-3 text-sm text-amber-900", children: [_jsx("div", { children: "Dataset berhasil dikosongkan." }), _jsxs("div", { children: ["Transaksi dihapus: ", clearResult.deletedTransactions] }), _jsxs("div", { children: ["Buku dihapus: ", clearResult.deletedBooks] }), _jsxs("div", { children: ["Mahasiswa dihapus: ", clearResult.deletedStudents] }), _jsxs("div", { children: ["Jurusan dihapus: ", clearResult.deletedDepartments] }), _jsxs("div", { children: ["Riwayat analisis dihapus: ", clearResult.deletedAnalysisRuns] })] })) : null, result ? (_jsxs("div", { className: "space-y-1 text-sm", children: [_jsxs("div", { children: ["Total baris: ", result.totalRows] }), _jsxs("div", { children: ["Transaksi dibuat: ", result.createdTransactions] }), _jsxs("div", { children: ["Item transaksi dibuat: ", result.createdTransactionItems] }), _jsxs("div", { children: ["Department baru: ", result.createdDepartments] }), _jsxs("div", { children: ["Student baru: ", result.createdStudents] }), _jsxs("div", { children: ["Buku baru: ", result.createdBooks] }), result.errors.length > 0 ? (_jsxs("div", { className: "break-words pt-1 text-amber-700", children: ["Error baris (", result.errors.length, "): ", result.errors.slice(0, 5).join(" | ")] })) : null] })) : null] })] }));
}
