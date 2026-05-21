import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
const formatDate = (value) => {
    if (!value)
        return "-";
    const [year, month, day] = value.split("-");
    if (!year || !month || !day)
        return value;
    return `${day}/${month}/${year}`;
};
const formatMonth = (value) => {
    const [year, month] = value.split("-");
    if (!year || !month)
        return value;
    return `${month}/${year}`;
};
export function TransactionSummaryPanel() {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const loadSummary = async () => {
            const base = import.meta.env.VITE_API_BASE_URL ?? "";
            try {
                const res = await fetch(`${base}/api/transactions/summary`);
                if (res.ok) {
                    setSummary((await res.json()));
                }
            }
            finally {
                setLoading(false);
            }
        };
        void loadSummary();
    }, []);
    const maxMonthlyTotal = useMemo(() => {
        return Math.max(...(summary?.monthly.map((item) => item.total) ?? [0]), 1);
    }, [summary]);
    return (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Grafik Periode Transaksi" }) }), _jsxs(CardContent, { children: [loading ? _jsx("div", { className: "text-sm text-slate-500", children: "Memuat ringkasan transaksi..." }) : null, !loading && !summary ? _jsx("div", { className: "text-sm text-slate-500", children: "Ringkasan transaksi belum tersedia." }) : null, summary ? (_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "grid gap-3 sm:grid-cols-3", children: [_jsxs("div", { className: "rounded-md border bg-slate-50 p-3", children: [_jsx("div", { className: "text-xs text-slate-500", children: "Transaksi Pertama" }), _jsx("div", { className: "mt-1 text-lg font-semibold", children: formatDate(summary.firstLoanDate) })] }), _jsxs("div", { className: "rounded-md border bg-slate-50 p-3", children: [_jsx("div", { className: "text-xs text-slate-500", children: "Transaksi Terakhir" }), _jsx("div", { className: "mt-1 text-lg font-semibold", children: formatDate(summary.lastLoanDate) })] }), _jsxs("div", { className: "rounded-md border bg-slate-50 p-3", children: [_jsx("div", { className: "text-xs text-slate-500", children: "Total Transaksi" }), _jsx("div", { className: "mt-1 text-lg font-semibold", children: summary.totalTransactions.toLocaleString("id-ID") })] })] }), summary.monthly.length > 0 ? (_jsx("div", { className: "overflow-x-auto", children: _jsx("div", { className: "flex min-w-[560px] items-end gap-3 border-b border-l px-3 pt-4", children: summary.monthly.map((item) => {
                                        const height = Math.max(12, Math.round((item.total / maxMonthlyTotal) * 180));
                                        return (_jsxs("div", { className: "flex flex-1 flex-col items-center gap-2", children: [_jsx("div", { className: "text-xs font-medium", children: item.total.toLocaleString("id-ID") }), _jsx("div", { className: "w-full max-w-12 rounded-t-md bg-slate-900 transition-all", style: { height: `${height}px` }, title: `${formatMonth(item.month)}: ${item.total} transaksi` }), _jsx("div", { className: "whitespace-nowrap pb-2 text-xs text-slate-500", children: formatMonth(item.month) })] }, item.month));
                                    }) }) })) : (_jsx("div", { className: "rounded-md border border-dashed p-4 text-sm text-slate-500", children: "Belum ada transaksi untuk ditampilkan." }))] })) : null] })] }));
}
