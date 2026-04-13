import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, } from "@/components/ui/table";
const fmtDateTime = (value) => {
    const dt = new Date(value);
    if (Number.isNaN(dt.getTime()))
        return value;
    return dt.toLocaleString("id-ID");
};
export function RunsHistoryPanel({ runs, selectedRunId, onSelect, onRefresh, onDelete }) {
    const [monthFilter, setMonthFilter] = useState("");
    const filteredRuns = useMemo(() => {
        if (!monthFilter)
            return runs;
        return runs.filter((r) => {
            const dt = new Date(r.created_at);
            if (Number.isNaN(dt.getTime()))
                return false;
            const y = dt.getFullYear();
            const m = String(dt.getMonth() + 1).padStart(2, "0");
            return `${y}-${m}` === monthFilter;
        });
    }, [runs, monthFilter]);
    return (_jsxs(Card, { children: [_jsxs(CardHeader, { className: "flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between", children: [_jsx(CardTitle, { children: "Riwayat Analisis" }), _jsxs("div", { className: "flex flex-col gap-2 sm:flex-row sm:items-center", children: [_jsx(Input, { type: "month", value: monthFilter, onChange: (e) => setMonthFilter(e.target.value), className: "w-full sm:w-44" }), _jsx(Button, { variant: "outline", onClick: onRefresh, children: "Refresh" })] })] }), _jsx(CardContent, { children: _jsx("div", { className: "overflow-x-auto rounded-md border", children: _jsxs(Table, { children: [_jsx(TableHeader, { children: _jsxs(TableRow, { children: [_jsx(TableHead, { children: "ID" }), _jsx(TableHead, { children: "Run Name" }), _jsx(TableHead, { children: "Parameter" }), _jsx(TableHead, { children: "Dibuat" }), _jsx(TableHead, { children: "Status" }), _jsx(TableHead, { children: "Aksi" })] }) }), _jsxs(TableBody, { children: [filteredRuns.map((run) => (_jsxs(TableRow, { children: [_jsx(TableCell, { children: run.id }), _jsx(TableCell, { className: "whitespace-nowrap", children: run.run_name }), _jsxs(TableCell, { className: "whitespace-nowrap", children: ["s=", run.min_support, ", c=", run.min_confidence, ", lift=", run.min_lift] }), _jsx(TableCell, { className: "whitespace-nowrap", children: fmtDateTime(run.created_at) }), _jsx(TableCell, { className: "whitespace-nowrap", children: run.status }), _jsx(TableCell, { children: _jsxs("div", { className: "flex min-w-[140px] flex-col gap-2 sm:flex-row", children: [_jsx(Button, { size: "sm", variant: String(run.id) === selectedRunId ? "default" : "outline", onClick: () => onSelect(String(run.id)), children: String(run.id) === selectedRunId ? "Aktif" : "Pilih" }), _jsx(Button, { size: "sm", variant: "outline", onClick: () => {
                                                                const ok = window.confirm(`Hapus run ${run.id} (${run.run_name})?`);
                                                                if (ok)
                                                                    onDelete(String(run.id));
                                                            }, children: "Hapus" })] }) })] }, run.id))), filteredRuns.length === 0 ? (_jsx(TableRow, { children: _jsx(TableCell, { colSpan: 6, className: "text-center text-muted-foreground", children: "Tidak ada run pada filter bulan ini." }) })) : null] })] }) }) })] }));
}
