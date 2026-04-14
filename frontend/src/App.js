import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { Helmet } from "react-helmet-async";
import { Button } from "@/components/ui/button";
import { DocumentationPage } from "@/features/docs/documentation-page";
import { CsvImportPanel } from "@/features/imports/csv-import-panel";
import { RunAnalysisPanel } from "@/features/imports/run-analysis-panel";
import { RulesPage } from "@/features/rules";
import { CompareRunsPanel } from "@/features/runs/compare-runs-panel";
import { RunsHistoryPanel } from "@/features/runs/runs-history-panel";
export function App() {
    const pathname = window.location.pathname;
    if (pathname === "/dokumentasi" || pathname.startsWith("/dokumentasi/") || pathname === "/docs" || pathname.startsWith("/docs/")) {
        return _jsx(DocumentationPage, {});
    }
    const [runId, setRunId] = useState("");
    const [runs, setRuns] = useState([]);
    const [departments, setDepartments] = useState([]);
    const [loading, setLoading] = useState(true);
    const reloadData = async () => {
        const base = import.meta.env.VITE_API_BASE_URL ?? "";
        try {
            const runsRes = await fetch(`${base}/api/analysis/runs`);
            if (runsRes.ok) {
                const rows = (await runsRes.json());
                setRuns(rows);
                if (rows.length === 0) {
                    setRunId("");
                }
                else if (!runId || !rows.some((r) => String(r.id) === runId)) {
                    setRunId(String(rows[0].id));
                }
            }
            const deptRes = await fetch(`${base}/api/departments`);
            if (deptRes.ok) {
                const rows = (await deptRes.json());
                setDepartments(rows.map((x) => ({ label: x.name, value: String(x.id) })));
            }
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        void reloadData();
    }, []);
    const deleteRun = async (targetRunId) => {
        const base = import.meta.env.VITE_API_BASE_URL ?? "";
        const res = await fetch(`${base}/api/analysis/runs/${targetRunId}`, { method: "DELETE" });
        if (!res.ok) {
            alert("Gagal menghapus run.");
            return;
        }
        await reloadData();
    };
    if (loading) {
        return (_jsxs(_Fragment, { children: [_jsxs(Helmet, { children: [_jsx("title", { children: "Apriori Engine - Analisis Peminjaman Perpustakaan" }), _jsx("meta", { name: "description", content: "Sistem analisis pola peminjaman perpustakaan berbasis Apriori." })] }), _jsx("div", { className: "p-6 text-sm", children: "Memuat data analisis..." })] }));
    }
    if (!runId) {
        return (_jsxs(_Fragment, { children: [_jsxs(Helmet, { children: [_jsx("title", { children: "Apriori Engine - Analisis Peminjaman Perpustakaan" }), _jsx("meta", { name: "description", content: "Import data transaksi dan jalankan analisis Apriori pertama." })] }), _jsxs("div", { className: "mx-auto max-w-7xl space-y-4 p-3 sm:p-4 md:p-6", children: [_jsx(CsvImportPanel, { onImported: () => void reloadData() }), _jsx(RunAnalysisPanel, { onRan: () => void reloadData() }), _jsxs("div", { className: "rounded-md border bg-white p-4 text-sm", children: ["Belum ada analysis run. Import data lalu klik panel \"Jalankan Analisis\".", _jsx(Button, { className: "mt-3", variant: "outline", onClick: () => void reloadData(), children: "Refresh" })] })] })] }));
    }
    return (_jsxs(_Fragment, { children: [_jsxs(Helmet, { children: [_jsx("title", { children: "Apriori Engine - Analisis Peminjaman Perpustakaan" }), _jsx("meta", { name: "description", content: "Dashboard analisis Apriori: import data, riwayat run, compare run, dan rules." })] }), _jsxs("div", { className: "mx-auto max-w-7xl space-y-4 p-3 sm:p-4", children: [_jsxs("div", { children: [_jsx(CsvImportPanel, { onImported: () => void reloadData() }), _jsx("div", { className: "mt-4", children: _jsx(RunAnalysisPanel, { onRan: () => void reloadData() }) }), _jsx("div", { className: "mt-4", children: _jsx(RunsHistoryPanel, { runs: runs, selectedRunId: runId, onSelect: setRunId, onRefresh: () => void reloadData(), onDelete: (id) => void deleteRun(id) }) }), _jsx("div", { className: "mt-4", children: _jsx(CompareRunsPanel, { runs: runs }) })] }), _jsx(RulesPage, { analysisRunId: runId, departments: departments })] })] }));
}
