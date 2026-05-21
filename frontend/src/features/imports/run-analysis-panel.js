import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { DatePicker } from "antd";
import dayjs from "dayjs";
import "antd/dist/reset.css";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
const toDdmmyyyy = (value) => {
    const [year, month, day] = value.split("-");
    if (!year || !month || !day)
        return value;
    return `${day}${month}${year}`;
};
const buildRunName = (periodStart, periodEnd) => {
    if (!periodStart && !periodEnd)
        return "analisis-semua-data";
    if (periodStart && periodEnd && periodStart === periodEnd)
        return `analisis-${toDdmmyyyy(periodStart)}`;
    if (periodStart && periodEnd)
        return `analisis-${toDdmmyyyy(periodStart)}-sd-${toDdmmyyyy(periodEnd)}`;
    if (periodStart)
        return `analisis-mulai-${toDdmmyyyy(periodStart)}`;
    return `analisis-sampai-${toDdmmyyyy(periodEnd)}`;
};
const datePickerClass = "h-10 w-full min-w-0";
export function RunAnalysisPanel({ onRan }) {
    const [runName, setRunName] = useState("analisis-semua-data");
    const [runNameEdited, setRunNameEdited] = useState(false);
    const [minSupport, setMinSupport] = useState("0.05");
    const [minConfidence, setMinConfidence] = useState("0.3");
    const [minLift, setMinLift] = useState("1.0");
    const [periodMode, setPeriodMode] = useState("all");
    const [selectedYear, setSelectedYear] = useState(dayjs());
    const [selectedMonth, setSelectedMonth] = useState(dayjs());
    const [rangeDates, setRangeDates] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [ok, setOk] = useState("");
    const { periodStart, periodEnd } = useMemo(() => {
        if (periodMode === "all") {
            return { periodStart: "", periodEnd: "" };
        }
        if (periodMode === "year") {
            if (!selectedYear)
                return { periodStart: "", periodEnd: "" };
            return {
                periodStart: selectedYear.startOf("year").format("YYYY-MM-DD"),
                periodEnd: selectedYear.endOf("year").format("YYYY-MM-DD"),
            };
        }
        if (periodMode === "month") {
            if (!selectedMonth)
                return { periodStart: "", periodEnd: "" };
            return {
                periodStart: selectedMonth.startOf("month").format("YYYY-MM-DD"),
                periodEnd: selectedMonth.endOf("month").format("YYYY-MM-DD"),
            };
        }
        const [start, end] = rangeDates ?? [null, null];
        return {
            periodStart: start ? start.format("YYYY-MM-DD") : "",
            periodEnd: end ? end.format("YYYY-MM-DD") : "",
        };
    }, [periodMode, rangeDates, selectedMonth, selectedYear]);
    useEffect(() => {
        if (!runNameEdited) {
            setRunName(buildRunName(periodStart, periodEnd));
        }
    }, [periodStart, periodEnd, runNameEdited]);
    const handleRun = async () => {
        setLoading(true);
        setError("");
        setOk("");
        try {
            const base = import.meta.env.VITE_API_BASE_URL ?? "";
            const res = await fetch(`${base}/api/analysis/run`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    run_name: runName,
                    period_start: periodStart || null,
                    period_end: periodEnd || null,
                    min_support: Number(minSupport),
                    min_confidence: Number(minConfidence),
                    min_lift: Number(minLift),
                }),
            });
            if (!res.ok) {
                const text = await res.text();
                throw new Error(text || `HTTP ${res.status}`);
            }
            const payload = (await res.json());
            setOk(`Analisis berhasil dijalankan: ${payload.run_name ?? runName}.`);
            onRan?.();
        }
        catch (e) {
            setError(e instanceof Error ? e.message : "Analisis gagal.");
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Jalankan Analisis" }) }), _jsxs(CardContent, { className: "grid gap-3 sm:grid-cols-2 lg:grid-cols-4", children: [_jsx(Input, { value: runName, onChange: (e) => {
                            setRunNameEdited(true);
                            setRunName(e.target.value);
                        }, placeholder: "Run name" }), _jsx(Input, { value: minSupport, onChange: (e) => setMinSupport(e.target.value), placeholder: "Min support" }), _jsx(Input, { value: minConfidence, onChange: (e) => setMinConfidence(e.target.value), placeholder: "Min confidence" }), _jsx(Input, { value: minLift, onChange: (e) => setMinLift(e.target.value), placeholder: "Min lift" }), _jsxs("select", { className: "h-10 rounded-md border border-slate-300 bg-white px-3 text-sm", value: periodMode, onChange: (e) => setPeriodMode(e.target.value), title: "Pilih cakupan tanggal transaksi yang dianalisis", children: [_jsx("option", { value: "all", children: "Semua data" }), _jsx("option", { value: "year", children: "Per tahun" }), _jsx("option", { value: "month", children: "Per bulan" }), _jsx("option", { value: "range", children: "Rentang bulan" })] }), periodMode === "year" ? (_jsx(DatePicker, { picker: "year", value: selectedYear, onChange: (date) => setSelectedYear(date), className: datePickerClass, placeholder: "Pilih tahun" })) : null, periodMode === "month" ? (_jsx(DatePicker, { picker: "month", value: selectedMonth, onChange: (date) => setSelectedMonth(date), className: datePickerClass, placeholder: "Pilih bulan" })) : null, periodMode === "range" ? (_jsxs(_Fragment, { children: [_jsxs("div", { className: "grid min-w-0 gap-3 sm:hidden", children: [_jsx(DatePicker, { value: rangeDates?.[0] ?? null, onChange: (date) => setRangeDates([date, rangeDates?.[1] ?? null]), format: "DD/MM/YYYY", className: datePickerClass, popupClassName: "max-w-[calc(100vw-24px)]", placement: "bottomLeft", placeholder: "Tanggal awal" }), _jsx(DatePicker, { value: rangeDates?.[1] ?? null, onChange: (date) => setRangeDates([rangeDates?.[0] ?? null, date]), format: "DD/MM/YYYY", className: datePickerClass, popupClassName: "max-w-[calc(100vw-24px)]", placement: "bottomLeft", placeholder: "Tanggal akhir" })] }), _jsx("div", { className: "hidden min-w-0 sm:col-span-2 sm:block", children: _jsx(DatePicker.RangePicker, { value: rangeDates, onChange: (dates) => setRangeDates(dates), format: "DD/MM/YYYY", className: `${datePickerClass} max-w-full`, popupClassName: "max-w-[calc(100vw-24px)]", placement: "bottomLeft", placeholder: ["Tanggal awal", "Tanggal akhir"] }) })] })) : null, _jsx("div", { className: "flex flex-col gap-2 sm:flex-row lg:col-span-2", children: _jsx(Button, { className: "sm:whitespace-nowrap", onClick: handleRun, disabled: loading, children: loading ? "Running..." : "Run" }) }), error ? _jsx("div", { className: "md:col-span-4 text-sm text-red-600", children: error }) : null, ok ? _jsx("div", { className: "md:col-span-4 text-sm text-emerald-700", children: ok }) : null] })] }));
}
