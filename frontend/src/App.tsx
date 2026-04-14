import { useEffect, useState } from "react";
import { Helmet } from "react-helmet-async";

import { Button } from "@/components/ui/button";
import { DocumentationPage } from "@/features/docs/documentation-page";
import { CsvImportPanel } from "@/features/imports/csv-import-panel";
import { RunAnalysisPanel } from "@/features/imports/run-analysis-panel";
import { RulesPage } from "@/features/rules";
import { CompareRunsPanel } from "@/features/runs/compare-runs-panel";
import { RunsHistoryPanel } from "@/features/runs/runs-history-panel";
import type { AnalysisRunOut, DepartmentOut } from "@/types/api";

export function App() {
  const pathname = window.location.pathname;
  if (pathname === "/dokumentasi" || pathname.startsWith("/dokumentasi/") || pathname === "/docs" || pathname.startsWith("/docs/")) {
    return <DocumentationPage />;
  }

  const [runId, setRunId] = useState<string>("");
  const [runs, setRuns] = useState<AnalysisRunOut[]>([]);
  const [departments, setDepartments] = useState<Array<{ label: string; value: string }>>([]);
  const [loading, setLoading] = useState(true);

  const reloadData = async () => {
    const base = import.meta.env.VITE_API_BASE_URL ?? "";
    try {
      const runsRes = await fetch(`${base}/api/analysis/runs`);
      if (runsRes.ok) {
        const rows = (await runsRes.json()) as AnalysisRunOut[];
        setRuns(rows);
        if (rows.length === 0) {
          setRunId("");
        } else if (!runId || !rows.some((r) => String(r.id) === runId)) {
          setRunId(String(rows[0].id));
        }
      }
      const deptRes = await fetch(`${base}/api/departments`);
      if (deptRes.ok) {
        const rows = (await deptRes.json()) as DepartmentOut[];
        setDepartments(rows.map((x) => ({ label: x.name, value: String(x.id) })));
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void reloadData();
  }, []);

  const deleteRun = async (targetRunId: string) => {
    const base = import.meta.env.VITE_API_BASE_URL ?? "";
    const res = await fetch(`${base}/api/analysis/runs/${targetRunId}`, { method: "DELETE" });
    if (!res.ok) {
      alert("Gagal menghapus run.");
      return;
    }
    await reloadData();
  };

  if (loading) {
    return (
      <>
        <Helmet>
          <title>Apriori Engine - Analisis Peminjaman Perpustakaan</title>
          <meta name="description" content="Sistem analisis pola peminjaman perpustakaan berbasis Apriori." />
        </Helmet>
        <div className="p-6 text-sm">Memuat data analisis...</div>
      </>
    );
  }

  if (!runId) {
    return (
      <>
        <Helmet>
          <title>Apriori Engine - Analisis Peminjaman Perpustakaan</title>
          <meta name="description" content="Import data transaksi dan jalankan analisis Apriori pertama." />
        </Helmet>
        <div className="mx-auto max-w-7xl space-y-4 p-3 sm:p-4 md:p-6">
          <CsvImportPanel onImported={() => void reloadData()} />
          <RunAnalysisPanel onRan={() => void reloadData()} />
          <div className="rounded-md border bg-white p-4 text-sm">
            Belum ada analysis run. Import data lalu klik panel "Jalankan Analisis".
            <Button className="mt-3" variant="outline" onClick={() => void reloadData()}>
              Refresh
            </Button>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Helmet>
        <title>Apriori Engine - Analisis Peminjaman Perpustakaan</title>
        <meta name="description" content="Dashboard analisis Apriori: import data, riwayat run, compare run, dan rules." />
      </Helmet>
      <div className="mx-auto max-w-7xl space-y-4 p-3 sm:p-4">
        <div>
          <CsvImportPanel onImported={() => void reloadData()} />
          <div className="mt-4">
            <RunAnalysisPanel onRan={() => void reloadData()} />
          </div>
          <div className="mt-4">
            <RunsHistoryPanel
              runs={runs}
              selectedRunId={runId}
              onSelect={setRunId}
              onRefresh={() => void reloadData()}
              onDelete={(id) => void deleteRun(id)}
            />
          </div>
          <div className="mt-4">
            <CompareRunsPanel runs={runs} />
          </div>
        </div>
        <RulesPage analysisRunId={runId} departments={departments} />
      </div>
    </>
  );
}
