import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { useRulesQuery } from "../hooks/use-rules-query";
import { toRuleText } from "../utils";
import { RuleDetailDialog } from "./rule-detail-dialog";
import { RulesFilterBar } from "./rules-filter-bar";
import { RulesSummaryCards } from "./rules-summary-cards";
import { RulesTable } from "./rules-table";
const defaultFilters = {
    page: 1,
    limit: 10,
    sortBy: "lift",
    sortDir: "desc",
    minConfidence: 0,
    minLift: 0,
};
export function RulesPage({ analysisRunId, departments = [] }) {
    const [filters, setFilters] = useState(defaultFilters);
    const [selectedRule, setSelectedRule] = useState(null);
    const [dialogOpen, setDialogOpen] = useState(false);
    const query = useRulesQuery({ analysisRunId, ...filters });
    const payload = query.data;
    const rules = payload?.data ?? [];
    const meta = payload?.meta;
    const summary = payload?.summary;
    const topRuleText = useMemo(() => {
        if (!summary?.topLiftRule)
            return undefined;
        return toRuleText(summary.topLiftRule);
    }, [summary?.topLiftRule]);
    const onReset = () => setFilters(defaultFilters);
    const openRuleDetail = (rule) => {
        setSelectedRule(rule);
        setDialogOpen(true);
    };
    return (_jsxs("div", { className: "space-y-4 p-3 sm:p-4", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-semibold", children: "Hasil Analisis Peminjaman" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Menampilkan aturan asosiasi dalam format non-teknis." })] }), _jsx(RulesSummaryCards, { totalRules: summary?.totalRules ?? 0, topLiftRule: topRuleText, dominantDepartment: summary?.dominantDepartment }), _jsx(RulesFilterBar, { filters: filters, departments: departments, onChange: setFilters, onReset: onReset }), query.isLoading ? _jsx("div", { className: "text-sm", children: "Memuat data..." }) : null, query.isError ? (_jsx("div", { className: "text-sm text-red-600", children: "Gagal memuat data. Coba ulangi." })) : null, _jsx(RulesTable, { rules: rules, page: meta?.page ?? filters.page ?? 1, limit: meta?.limit ?? filters.limit ?? 10, onViewDetail: openRuleDetail }), _jsxs("div", { className: "flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between", children: [_jsxs("div", { className: "text-sm text-muted-foreground", children: ["Halaman ", meta?.page ?? 1, " dari ", meta?.totalPages ?? 1] }), _jsxs("div", { className: "flex gap-2", children: [_jsx(Button, { variant: "outline", disabled: (meta?.page ?? 1) <= 1, onClick: () => setFilters((prev) => ({ ...prev, page: Math.max(1, (prev.page ?? 1) - 1) })), children: "Sebelumnya" }), _jsx(Button, { variant: "outline", disabled: (meta?.page ?? 1) >= (meta?.totalPages ?? 1), onClick: () => setFilters((prev) => ({
                                    ...prev,
                                    page: Math.min(meta?.totalPages ?? 1, (prev.page ?? 1) + 1),
                                })), children: "Selanjutnya" })] })] }), _jsx(RuleDetailDialog, { open: dialogOpen, onOpenChange: setDialogOpen, rule: selectedRule })] }));
}
