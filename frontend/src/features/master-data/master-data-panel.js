import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, } from "@/components/ui/table";
const emptyMeta = { page: 1, limit: 20, total: 0, totalPages: 1 };
const endpointByTab = {
    students: "/api/students",
    books: "/api/books",
    transactions: "/api/transactions",
};
export function MasterDataPanel() {
    const [tab, setTab] = useState("students");
    const [query, setQuery] = useState("");
    const [pageByTab, setPageByTab] = useState({
        students: 1,
        books: 1,
        transactions: 1,
    });
    const [students, setStudents] = useState([]);
    const [books, setBooks] = useState([]);
    const [transactions, setTransactions] = useState([]);
    const [metaByTab, setMetaByTab] = useState({
        students: emptyMeta,
        books: emptyMeta,
        transactions: emptyMeta,
    });
    const [loading, setLoading] = useState(false);
    const [metaLoading, setMetaLoading] = useState(false);
    const activePage = pageByTab[tab];
    const activeMeta = metaByTab[tab];
    const setActivePage = (nextPage) => {
        setPageByTab((current) => ({ ...current, [tab]: nextPage }));
    };
    const load = async (targetTab = tab, targetPage = pageByTab[targetTab], targetQuery = query) => {
        const base = import.meta.env.VITE_API_BASE_URL ?? "";
        const params = new URLSearchParams({
            page: String(targetPage),
            limit: "20",
        });
        if (targetQuery.trim())
            params.set("q", targetQuery.trim());
        setLoading(true);
        try {
            const res = await fetch(`${base}${endpointByTab[targetTab]}?${params.toString()}`);
            if (!res.ok)
                return;
            if (targetTab === "students") {
                const payload = (await res.json());
                setStudents(payload.data);
                setMetaByTab((current) => ({ ...current, students: payload.meta }));
            }
            else if (targetTab === "books") {
                const payload = (await res.json());
                setBooks(payload.data);
                setMetaByTab((current) => ({ ...current, books: payload.meta }));
            }
            else {
                const payload = (await res.json());
                setTransactions(payload.data);
                setMetaByTab((current) => ({ ...current, transactions: payload.meta }));
            }
        }
        finally {
            setLoading(false);
        }
    };
    const loadAllMeta = async (targetQuery = query) => {
        const base = import.meta.env.VITE_API_BASE_URL ?? "";
        setMetaLoading(true);
        try {
            const entries = await Promise.all(Object.keys(endpointByTab).map(async (targetTab) => {
                const params = new URLSearchParams({ page: "1", limit: "1" });
                if (targetQuery.trim())
                    params.set("q", targetQuery.trim());
                const res = await fetch(`${base}${endpointByTab[targetTab]}?${params.toString()}`);
                if (!res.ok)
                    return [targetTab, emptyMeta];
                const payload = (await res.json());
                return [targetTab, payload.meta];
            }));
            setMetaByTab((current) => {
                const next = { ...current };
                for (const [targetTab, meta] of entries) {
                    next[targetTab] = meta;
                }
                return next;
            });
        }
        finally {
            setMetaLoading(false);
        }
    };
    useEffect(() => {
        void load(tab, activePage, query);
    }, [tab, activePage]);
    useEffect(() => {
        void loadAllMeta(query);
    }, []);
    const runSearch = () => {
        setPageByTab({ students: 1, books: 1, transactions: 1 });
        void loadAllMeta(query);
        void load(tab, 1, query);
    };
    const switchTab = (nextTab) => {
        setTab(nextTab);
    };
    const canPrev = activeMeta.page > 1;
    const canNext = activeMeta.page < activeMeta.totalPages;
    return (_jsxs(Card, { children: [_jsxs(CardHeader, { className: "flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between", children: [_jsxs("div", { children: [_jsx(CardTitle, { children: "Data Master" }), _jsx("div", { className: "mt-1 text-xs text-slate-600", children: "Data hasil import CSV: mahasiswa, buku, dan transaksi peminjaman." })] }), _jsxs("div", { className: "flex flex-col gap-2 sm:flex-row sm:items-center", children: [_jsx(Input, { value: query, onChange: (e) => setQuery(e.target.value), onKeyDown: (e) => {
                                    if (e.key === "Enter")
                                        runSearch();
                                }, placeholder: "Cari nama, NIM, fakultas, buku...", className: "w-full sm:w-72" }), _jsx(Button, { variant: "outline", onClick: runSearch, children: "Cari" }), _jsx(Button, { variant: "outline", onClick: () => void load(), children: loading || metaLoading ? "Memuat..." : "Refresh" })] })] }), _jsxs(CardContent, { className: "space-y-3", children: [_jsxs("div", { className: "flex flex-wrap gap-2", children: [_jsxs(Button, { size: "sm", variant: tab === "students" ? "default" : "outline", onClick: () => switchTab("students"), children: ["Mahasiswa (", metaByTab.students.total, ")"] }), _jsxs(Button, { size: "sm", variant: tab === "books" ? "default" : "outline", onClick: () => switchTab("books"), children: ["Buku (", metaByTab.books.total, ")"] }), _jsxs(Button, { size: "sm", variant: tab === "transactions" ? "default" : "outline", onClick: () => switchTab("transactions"), children: ["Transaksi (", metaByTab.transactions.total, ")"] })] }), tab === "students" ? (_jsx("div", { className: "max-h-[420px] overflow-auto rounded-md border", children: _jsxs(Table, { children: [_jsx(TableHeader, { className: "sticky top-0 z-10 bg-white", children: _jsxs(TableRow, { children: [_jsx(TableHead, { children: "NIM/NPM" }), _jsx(TableHead, { children: "Nama" }), _jsx(TableHead, { children: "Fakultas/Jurusan" })] }) }), _jsx(TableBody, { children: students.map((row) => (_jsxs(TableRow, { children: [_jsx(TableCell, { className: "whitespace-nowrap", children: row.student_number }), _jsx(TableCell, { className: "min-w-[220px]", children: row.name }), _jsx(TableCell, { className: "min-w-[180px]", children: row.department_name ?? "-" })] }, row.id))) })] }) })) : null, tab === "books" ? (_jsx("div", { className: "max-h-[420px] overflow-auto rounded-md border", children: _jsxs(Table, { children: [_jsx(TableHeader, { className: "sticky top-0 z-10 bg-white", children: _jsxs(TableRow, { children: [_jsx(TableHead, { children: "Kode/ISBN" }), _jsx(TableHead, { children: "Judul" }), _jsx(TableHead, { children: "Kategori" })] }) }), _jsx(TableBody, { children: books.map((row) => (_jsxs(TableRow, { children: [_jsx(TableCell, { className: "whitespace-nowrap", children: row.isbn }), _jsx(TableCell, { className: "min-w-[280px]", children: row.title }), _jsx(TableCell, { className: "whitespace-nowrap", children: row.category || "-" })] }, row.id))) })] }) })) : null, tab === "transactions" ? (_jsx("div", { className: "max-h-[420px] overflow-auto rounded-md border", children: _jsxs(Table, { children: [_jsx(TableHeader, { className: "sticky top-0 z-10 bg-white", children: _jsxs(TableRow, { children: [_jsx(TableHead, { children: "Tanggal" }), _jsx(TableHead, { children: "NIM/NPM" }), _jsx(TableHead, { children: "Nama" }), _jsx(TableHead, { children: "Fakultas/Jurusan" }), _jsx(TableHead, { children: "Buku Dipinjam" })] }) }), _jsx(TableBody, { children: transactions.map((row) => (_jsxs(TableRow, { children: [_jsxs(TableCell, { className: "whitespace-nowrap", children: [row.loan_date, row.return_date ? ` - ${row.return_date}` : ""] }), _jsx(TableCell, { className: "whitespace-nowrap", children: row.student_number ?? "-" }), _jsx(TableCell, { className: "min-w-[220px]", children: row.student_name ?? "-" }), _jsx(TableCell, { className: "min-w-[180px]", children: row.department_name ?? "-" }), _jsx(TableCell, { className: "min-w-[320px]", children: row.book_titles.join(", ") || "-" })] }, row.id))) })] }) })) : null, _jsxs("div", { className: "flex flex-col gap-2 text-xs text-slate-600 sm:flex-row sm:items-center sm:justify-between", children: [_jsxs("div", { children: ["Total ", activeMeta.total, " data. Halaman ", activeMeta.page, " dari ", activeMeta.totalPages, "."] }), _jsxs("div", { className: "flex gap-2", children: [_jsx(Button, { size: "sm", variant: "outline", disabled: !canPrev || loading, onClick: () => setActivePage(activePage - 1), children: "Sebelumnya" }), _jsx(Button, { size: "sm", variant: "outline", disabled: !canNext || loading, onClick: () => setActivePage(activePage + 1), children: "Berikutnya" })] })] })] })] }));
}
