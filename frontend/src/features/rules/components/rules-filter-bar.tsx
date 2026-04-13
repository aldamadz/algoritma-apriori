import { ChangeEvent } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import type { RulesFilters } from "../types";

type DepartmentOption = {
  label: string;
  value: string;
};

type Props = {
  filters: RulesFilters;
  departments: DepartmentOption[];
  onChange: (next: RulesFilters) => void;
  onReset: () => void;
};

export function RulesFilterBar({ filters, departments, onChange, onReset }: Props) {
  const onQueryText = (e: ChangeEvent<HTMLInputElement>) =>
    onChange({ ...filters, q: e.target.value, page: 1 });

  const onDate = (key: "periodStart" | "periodEnd") => (e: ChangeEvent<HTMLInputElement>) =>
    onChange({ ...filters, [key]: e.target.value, page: 1 });

  return (
    <div className="grid gap-3 rounded-md border p-3 sm:p-4 md:grid-cols-2 xl:grid-cols-6">
      <Input placeholder="Cari jurusan/buku..." value={filters.q ?? ""} onChange={onQueryText} />

      <select
        className="h-10 rounded-md border border-slate-300 bg-white px-3 text-sm"
        value={filters.departmentId ?? "all"}
        onChange={(e) =>
          onChange({
            ...filters,
            departmentId: e.target.value === "all" ? undefined : e.target.value,
            page: 1,
          })
        }
      >
        <option value="all">Semua jurusan</option>
        {departments.map((d) => (
          <option key={d.value} value={d.value}>
            {d.label}
          </option>
        ))}
      </select>

      <Input
        type="number"
        min={0}
        max={1}
        step={0.01}
        placeholder="Min confidence"
        value={filters.minConfidence ?? ""}
        onChange={(e) =>
          onChange({
            ...filters,
            minConfidence: e.target.value === "" ? undefined : Number(e.target.value),
            page: 1,
          })
        }
      />
      <Input
        type="number"
        min={0}
        step={0.01}
        placeholder="Min lift"
        value={filters.minLift ?? ""}
        onChange={(e) =>
          onChange({
            ...filters,
            minLift: e.target.value === "" ? undefined : Number(e.target.value),
            page: 1,
          })
        }
      />
      <Input type="date" value={filters.periodStart ?? ""} onChange={onDate("periodStart")} />
      <div className="flex flex-col gap-2 sm:flex-row">
        <Input type="date" value={filters.periodEnd ?? ""} onChange={onDate("periodEnd")} />
        <Button variant="outline" onClick={onReset}>
          Reset
        </Button>
      </div>
    </div>
  );
}
