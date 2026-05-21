import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { BookOut, LoanTransactionOut, PaginatedResponse, PaginationMeta, StudentOut } from "@/types/api";

type TabKey = "students" | "books" | "transactions";

const emptyMeta: PaginationMeta = { page: 1, limit: 20, total: 0, totalPages: 1 };

const endpointByTab: Record<TabKey, string> = {
  students: "/api/students",
  books: "/api/books",
  transactions: "/api/transactions",
};

export function MasterDataPanel() {
  const [tab, setTab] = useState<TabKey>("students");
  const [query, setQuery] = useState("");
  const [pageByTab, setPageByTab] = useState<Record<TabKey, number>>({
    students: 1,
    books: 1,
    transactions: 1,
  });
  const [students, setStudents] = useState<StudentOut[]>([]);
  const [books, setBooks] = useState<BookOut[]>([]);
  const [transactions, setTransactions] = useState<LoanTransactionOut[]>([]);
  const [metaByTab, setMetaByTab] = useState<Record<TabKey, PaginationMeta>>({
    students: emptyMeta,
    books: emptyMeta,
    transactions: emptyMeta,
  });
  const [loading, setLoading] = useState(false);
  const [metaLoading, setMetaLoading] = useState(false);

  const activePage = pageByTab[tab];
  const activeMeta = metaByTab[tab];

  const setActivePage = (nextPage: number) => {
    setPageByTab((current) => ({ ...current, [tab]: nextPage }));
  };

  const load = async (targetTab: TabKey = tab, targetPage: number = pageByTab[targetTab], targetQuery: string = query) => {
    const base = import.meta.env.VITE_API_BASE_URL ?? "";
    const params = new URLSearchParams({
      page: String(targetPage),
      limit: "20",
    });
    if (targetQuery.trim()) params.set("q", targetQuery.trim());

    setLoading(true);
    try {
      const res = await fetch(`${base}${endpointByTab[targetTab]}?${params.toString()}`);
      if (!res.ok) return;
      if (targetTab === "students") {
        const payload = (await res.json()) as PaginatedResponse<StudentOut>;
        setStudents(payload.data);
        setMetaByTab((current) => ({ ...current, students: payload.meta }));
      } else if (targetTab === "books") {
        const payload = (await res.json()) as PaginatedResponse<BookOut>;
        setBooks(payload.data);
        setMetaByTab((current) => ({ ...current, books: payload.meta }));
      } else {
        const payload = (await res.json()) as PaginatedResponse<LoanTransactionOut>;
        setTransactions(payload.data);
        setMetaByTab((current) => ({ ...current, transactions: payload.meta }));
      }
    } finally {
      setLoading(false);
    }
  };

  const loadAllMeta = async (targetQuery: string = query) => {
    const base = import.meta.env.VITE_API_BASE_URL ?? "";
    setMetaLoading(true);
    try {
      const entries = await Promise.all(
        (Object.keys(endpointByTab) as TabKey[]).map(async (targetTab) => {
          const params = new URLSearchParams({ page: "1", limit: "1" });
          if (targetQuery.trim()) params.set("q", targetQuery.trim());
          const res = await fetch(`${base}${endpointByTab[targetTab]}?${params.toString()}`);
          if (!res.ok) return [targetTab, emptyMeta] as const;
          const payload = (await res.json()) as PaginatedResponse<unknown>;
          return [targetTab, payload.meta] as const;
        })
      );
      setMetaByTab((current) => {
        const next = { ...current };
        for (const [targetTab, meta] of entries) {
          next[targetTab] = meta;
        }
        return next;
      });
    } finally {
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

  const switchTab = (nextTab: TabKey) => {
    setTab(nextTab);
  };

  const canPrev = activeMeta.page > 1;
  const canNext = activeMeta.page < activeMeta.totalPages;

  return (
    <Card>
      <CardHeader className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <CardTitle>Data Master</CardTitle>
          <div className="mt-1 text-xs text-slate-600">
            Data hasil import CSV: mahasiswa, buku, dan transaksi peminjaman.
          </div>
        </div>
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") runSearch();
            }}
            placeholder="Cari nama, NIM, fakultas, buku..."
            className="w-full sm:w-72"
          />
          <Button variant="outline" onClick={runSearch}>
            Cari
          </Button>
          <Button variant="outline" onClick={() => void load()}>
            {loading || metaLoading ? "Memuat..." : "Refresh"}
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex flex-wrap gap-2">
          <Button size="sm" variant={tab === "students" ? "default" : "outline"} onClick={() => switchTab("students")}>
            Mahasiswa ({metaByTab.students.total})
          </Button>
          <Button size="sm" variant={tab === "books" ? "default" : "outline"} onClick={() => switchTab("books")}>
            Buku ({metaByTab.books.total})
          </Button>
          <Button size="sm" variant={tab === "transactions" ? "default" : "outline"} onClick={() => switchTab("transactions")}>
            Transaksi ({metaByTab.transactions.total})
          </Button>
        </div>

        {tab === "students" ? (
          <div className="max-h-[420px] overflow-auto rounded-md border">
            <Table>
              <TableHeader className="sticky top-0 z-10 bg-white">
                <TableRow>
                  <TableHead>NIM/NPM</TableHead>
                  <TableHead>Nama</TableHead>
                  <TableHead>Fakultas/Jurusan</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {students.map((row) => (
                  <TableRow key={row.id}>
                    <TableCell className="whitespace-nowrap">{row.student_number}</TableCell>
                    <TableCell className="min-w-[220px]">{row.name}</TableCell>
                    <TableCell className="min-w-[180px]">{row.department_name ?? "-"}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        ) : null}

        {tab === "books" ? (
          <div className="max-h-[420px] overflow-auto rounded-md border">
            <Table>
              <TableHeader className="sticky top-0 z-10 bg-white">
                <TableRow>
                  <TableHead>Kode/ISBN</TableHead>
                  <TableHead>Judul</TableHead>
                  <TableHead>Kategori</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {books.map((row) => (
                  <TableRow key={row.id}>
                    <TableCell className="whitespace-nowrap">{row.isbn}</TableCell>
                    <TableCell className="min-w-[280px]">{row.title}</TableCell>
                    <TableCell className="whitespace-nowrap">{row.category || "-"}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        ) : null}

        {tab === "transactions" ? (
          <div className="max-h-[420px] overflow-auto rounded-md border">
            <Table>
              <TableHeader className="sticky top-0 z-10 bg-white">
                <TableRow>
                  <TableHead>Tanggal</TableHead>
                  <TableHead>NIM/NPM</TableHead>
                  <TableHead>Nama</TableHead>
                  <TableHead>Fakultas/Jurusan</TableHead>
                  <TableHead>Buku Dipinjam</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {transactions.map((row) => (
                  <TableRow key={row.id}>
                    <TableCell className="whitespace-nowrap">
                      {row.loan_date}
                      {row.return_date ? ` - ${row.return_date}` : ""}
                    </TableCell>
                    <TableCell className="whitespace-nowrap">{row.student_number ?? "-"}</TableCell>
                    <TableCell className="min-w-[220px]">{row.student_name ?? "-"}</TableCell>
                    <TableCell className="min-w-[180px]">{row.department_name ?? "-"}</TableCell>
                    <TableCell className="min-w-[320px]">{row.book_titles.join(", ") || "-"}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        ) : null}

        <div className="flex flex-col gap-2 text-xs text-slate-600 sm:flex-row sm:items-center sm:justify-between">
          <div>
            Total {activeMeta.total} data. Halaman {activeMeta.page} dari {activeMeta.totalPages}.
          </div>
          <div className="flex gap-2">
            <Button size="sm" variant="outline" disabled={!canPrev || loading} onClick={() => setActivePage(activePage - 1)}>
              Sebelumnya
            </Button>
            <Button size="sm" variant="outline" disabled={!canNext || loading} onClick={() => setActivePage(activePage + 1)}>
              Berikutnya
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
