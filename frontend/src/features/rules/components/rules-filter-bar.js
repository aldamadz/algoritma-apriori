import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
export function RulesFilterBar({ filters, departments, onChange, onReset }) {
    const onQueryText = (e) => onChange({ ...filters, q: e.target.value, page: 1 });
    const onDate = (key) => (e) => onChange({ ...filters, [key]: e.target.value, page: 1 });
    return (_jsxs("div", { className: "grid gap-3 rounded-md border p-3 sm:p-4 md:grid-cols-2 xl:grid-cols-6", children: [_jsx(Input, { placeholder: "Cari jurusan/buku...", value: filters.q ?? "", onChange: onQueryText }), _jsxs("select", { className: "h-10 rounded-md border border-slate-300 bg-white px-3 text-sm", value: filters.departmentId ?? "all", onChange: (e) => onChange({
                    ...filters,
                    departmentId: e.target.value === "all" ? undefined : e.target.value,
                    page: 1,
                }), children: [_jsx("option", { value: "all", children: "Semua jurusan" }), departments.map((d) => (_jsx("option", { value: d.value, children: d.label }, d.value)))] }), _jsx(Input, { type: "number", min: 0, max: 1, step: 0.01, placeholder: "Min confidence", value: filters.minConfidence ?? "", onChange: (e) => onChange({
                    ...filters,
                    minConfidence: e.target.value === "" ? undefined : Number(e.target.value),
                    page: 1,
                }) }), _jsx(Input, { type: "number", min: 0, step: 0.01, placeholder: "Min lift", value: filters.minLift ?? "", onChange: (e) => onChange({
                    ...filters,
                    minLift: e.target.value === "" ? undefined : Number(e.target.value),
                    page: 1,
                }) }), _jsx(Input, { type: "date", value: filters.periodStart ?? "", onChange: onDate("periodStart") }), _jsxs("div", { className: "flex flex-col gap-2 sm:flex-row", children: [_jsx(Input, { type: "date", value: filters.periodEnd ?? "", onChange: onDate("periodEnd") }), _jsx(Button, { variant: "outline", onClick: onReset, children: "Reset" })] })] }));
}
