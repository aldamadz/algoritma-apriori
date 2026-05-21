import { useEffect, useMemo, useState } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { TransactionSummary } from "@/types/api";

const formatDate = (value: string | null): string => {
  if (!value) return "-";
  const [year, month, day] = value.split("-");
  if (!year || !month || !day) return value;
  return `${day}/${month}/${year}`;
};

const formatMonth = (value: string): string => {
  const [year, month] = value.split("-");
  if (!year || !month) return value;
  return `${month}/${year}`;
};

export function TransactionSummaryPanel() {
  const [summary, setSummary] = useState<TransactionSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadSummary = async () => {
      const base = import.meta.env.VITE_API_BASE_URL ?? "";
      try {
        const res = await fetch(`${base}/api/transactions/summary`);
        if (res.ok) {
          setSummary((await res.json()) as TransactionSummary);
        }
      } finally {
        setLoading(false);
      }
    };

    void loadSummary();
  }, []);

  const maxMonthlyTotal = useMemo(() => {
    return Math.max(...(summary?.monthly.map((item) => item.total) ?? [0]), 1);
  }, [summary]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Grafik Periode Transaksi</CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? <div className="text-sm text-slate-500">Memuat ringkasan transaksi...</div> : null}
        {!loading && !summary ? <div className="text-sm text-slate-500">Ringkasan transaksi belum tersedia.</div> : null}
        {summary ? (
          <div className="space-y-4">
            <div className="grid gap-3 sm:grid-cols-3">
              <div className="rounded-md border bg-slate-50 p-3">
                <div className="text-xs text-slate-500">Transaksi Pertama</div>
                <div className="mt-1 text-lg font-semibold">{formatDate(summary.firstLoanDate)}</div>
              </div>
              <div className="rounded-md border bg-slate-50 p-3">
                <div className="text-xs text-slate-500">Transaksi Terakhir</div>
                <div className="mt-1 text-lg font-semibold">{formatDate(summary.lastLoanDate)}</div>
              </div>
              <div className="rounded-md border bg-slate-50 p-3">
                <div className="text-xs text-slate-500">Total Transaksi</div>
                <div className="mt-1 text-lg font-semibold">{summary.totalTransactions.toLocaleString("id-ID")}</div>
              </div>
            </div>

            {summary.monthly.length > 0 ? (
              <div className="overflow-x-auto">
                <div className="flex min-w-[560px] items-end gap-3 border-b border-l px-3 pt-4">
                  {summary.monthly.map((item) => {
                    const height = Math.max(12, Math.round((item.total / maxMonthlyTotal) * 180));
                    return (
                      <div key={item.month} className="flex flex-1 flex-col items-center gap-2">
                        <div className="text-xs font-medium">{item.total.toLocaleString("id-ID")}</div>
                        <div
                          className="w-full max-w-12 rounded-t-md bg-slate-900 transition-all"
                          style={{ height: `${height}px` }}
                          title={`${formatMonth(item.month)}: ${item.total} transaksi`}
                        />
                        <div className="whitespace-nowrap pb-2 text-xs text-slate-500">{formatMonth(item.month)}</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="rounded-md border border-dashed p-4 text-sm text-slate-500">
                Belum ada transaksi untuk ditampilkan.
              </div>
            )}
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
