import { useMemo, useState } from "react";

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
import type { AnalysisRunOut } from "@/types/api";

type Props = {
  runs: AnalysisRunOut[];
  selectedRunId?: string;
  onSelect: (runId: string) => void;
  onRefresh: () => void;
  onDelete: (runId: string) => void;
};

const fmtDateTime = (value: string): string => {
  const dt = new Date(value);
  if (Number.isNaN(dt.getTime())) return value;
  return dt.toLocaleString("id-ID");
};

export function RunsHistoryPanel({ runs, selectedRunId, onSelect, onRefresh, onDelete }: Props) {
  const [monthFilter, setMonthFilter] = useState("");

  const filteredRuns = useMemo(() => {
    if (!monthFilter) return runs;
    return runs.filter((r) => {
      const dt = new Date(r.created_at);
      if (Number.isNaN(dt.getTime())) return false;
      const y = dt.getFullYear();
      const m = String(dt.getMonth() + 1).padStart(2, "0");
      return `${y}-${m}` === monthFilter;
    });
  }, [runs, monthFilter]);

  return (
    <Card>
      <CardHeader className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <CardTitle>Riwayat Analisis</CardTitle>
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
          <Input
            type="month"
            value={monthFilter}
            onChange={(e) => setMonthFilter(e.target.value)}
            className="w-full sm:w-44"
          />
          <Button variant="outline" onClick={onRefresh}>
            Refresh
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Run Name</TableHead>
                <TableHead>Parameter</TableHead>
                <TableHead>Dibuat</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Aksi</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredRuns.map((run) => (
                <TableRow key={run.id}>
                  <TableCell>{run.id}</TableCell>
                  <TableCell className="whitespace-nowrap">{run.run_name}</TableCell>
                  <TableCell className="whitespace-nowrap">
                    s={run.min_support}, c={run.min_confidence}, lift={run.min_lift}
                  </TableCell>
                  <TableCell className="whitespace-nowrap">{fmtDateTime(run.created_at)}</TableCell>
                  <TableCell className="whitespace-nowrap">{run.status}</TableCell>
                  <TableCell>
                    <div className="flex min-w-[140px] flex-col gap-2 sm:flex-row">
                      <Button
                        size="sm"
                        variant={String(run.id) === selectedRunId ? "default" : "outline"}
                        onClick={() => onSelect(String(run.id))}
                      >
                        {String(run.id) === selectedRunId ? "Aktif" : "Pilih"}
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => {
                          const ok = window.confirm(`Hapus run ${run.id} (${run.run_name})?`);
                          if (ok) onDelete(String(run.id));
                        }}
                      >
                        Hapus
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
              {filteredRuns.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center text-muted-foreground">
                    Tidak ada run pada filter bulan ini.
                  </TableCell>
                </TableRow>
              ) : null}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}
