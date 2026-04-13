import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";

import { useRulesQuery } from "../hooks/use-rules-query";
import type { AssociationRule, RulesFilters } from "../types";
import { toRuleText } from "../utils";
import { RuleDetailDialog } from "./rule-detail-dialog";
import { RulesFilterBar } from "./rules-filter-bar";
import { RulesSummaryCards } from "./rules-summary-cards";
import { RulesTable } from "./rules-table";

type DepartmentOption = {
  label: string;
  value: string;
};

type Props = {
  analysisRunId: string;
  departments?: DepartmentOption[];
};

const defaultFilters: RulesFilters = {
  page: 1,
  limit: 10,
  sortBy: "lift",
  sortDir: "desc",
  minConfidence: 0,
  minLift: 0,
};

export function RulesPage({ analysisRunId, departments = [] }: Props) {
  const [filters, setFilters] = useState<RulesFilters>(defaultFilters);
  const [selectedRule, setSelectedRule] = useState<AssociationRule | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  const query = useRulesQuery({ analysisRunId, ...filters });
  const payload = query.data;
  const rules = payload?.data ?? [];
  const meta = payload?.meta;
  const summary = payload?.summary;

  const topRuleText = useMemo(() => {
    if (!summary?.topLiftRule) return undefined;
    return toRuleText(summary.topLiftRule);
  }, [summary?.topLiftRule]);

  const onReset = () => setFilters(defaultFilters);

  const openRuleDetail = (rule: AssociationRule) => {
    setSelectedRule(rule);
    setDialogOpen(true);
  };

  return (
    <div className="space-y-4 p-3 sm:p-4">
      <div>
        <h1 className="text-2xl font-semibold">Hasil Analisis Peminjaman</h1>
        <p className="text-sm text-muted-foreground">
          Menampilkan aturan asosiasi dalam format non-teknis.
        </p>
      </div>

      <RulesSummaryCards
        totalRules={summary?.totalRules ?? 0}
        topLiftRule={topRuleText}
        dominantDepartment={summary?.dominantDepartment}
      />

      <RulesFilterBar
        filters={filters}
        departments={departments}
        onChange={setFilters}
        onReset={onReset}
      />

      {query.isLoading ? <div className="text-sm">Memuat data...</div> : null}
      {query.isError ? (
        <div className="text-sm text-red-600">Gagal memuat data. Coba ulangi.</div>
      ) : null}

      <RulesTable
        rules={rules}
        page={meta?.page ?? filters.page ?? 1}
        limit={meta?.limit ?? filters.limit ?? 10}
        onViewDetail={openRuleDetail}
      />

      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div className="text-sm text-muted-foreground">
          Halaman {meta?.page ?? 1} dari {meta?.totalPages ?? 1}
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            disabled={(meta?.page ?? 1) <= 1}
            onClick={() =>
              setFilters((prev) => ({ ...prev, page: Math.max(1, (prev.page ?? 1) - 1) }))
            }
          >
            Sebelumnya
          </Button>
          <Button
            variant="outline"
            disabled={(meta?.page ?? 1) >= (meta?.totalPages ?? 1)}
            onClick={() =>
              setFilters((prev) => ({
                ...prev,
                page: Math.min(meta?.totalPages ?? 1, (prev.page ?? 1) + 1),
              }))
            }
          >
            Selanjutnya
          </Button>
        </div>
      </div>

      <RuleDetailDialog open={dialogOpen} onOpenChange={setDialogOpen} rule={selectedRule} />
    </div>
  );
}
