import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
export function CsvImportPanel({ onImported }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
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
    return (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Import Dataset CSV" }) }), _jsxs(CardContent, { className: "space-y-3", children: [_jsxs("div", { className: "break-words text-xs text-slate-600", children: ["Kolom wajib: ", _jsx("code", { children: "transaction_id, student_number, department_code, loan_date, book_isbn" })] }), _jsx(Input, { type: "file", accept: ".csv", onChange: (e) => setFile(e.target.files?.[0] ?? null) }), _jsx(Button, { onClick: handleImport, disabled: loading, children: loading ? "Importing..." : "Import CSV" }), error ? _jsx("div", { className: "break-words text-sm text-red-600", children: error }) : null, result ? (_jsxs("div", { className: "space-y-1 text-sm", children: [_jsxs("div", { children: ["Total baris: ", result.totalRows] }), _jsxs("div", { children: ["Transaksi dibuat: ", result.createdTransactions] }), _jsxs("div", { children: ["Item transaksi dibuat: ", result.createdTransactionItems] }), _jsxs("div", { children: ["Department baru: ", result.createdDepartments] }), _jsxs("div", { children: ["Student baru: ", result.createdStudents] }), _jsxs("div", { children: ["Buku baru: ", result.createdBooks] }), result.errors.length > 0 ? (_jsxs("div", { className: "break-words pt-1 text-amber-700", children: ["Error baris (", result.errors.length, "): ", result.errors.slice(0, 5).join(" | ")] })) : null] })) : null] })] }));
}
