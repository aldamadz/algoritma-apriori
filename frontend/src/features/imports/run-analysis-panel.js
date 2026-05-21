import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
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
export function RunAnalysisPanel({ onRan }) {
    const [runName, setRunName] = useState("analisis-semua-data");
    const [runNameEdited, setRunNameEdited] = useState(false);
    const [minSupport, setMinSupport] = useState("0.05");
    const [minConfidence, setMinConfidence] = useState("0.3");
    const [minLift, setMinLift] = useState("1.0");
    const [periodStart, setPeriodStart] = useState("");
    const [periodEnd, setPeriodEnd] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [ok, setOk] = useState("");
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
            if (payload.run_name && payload.run_name !== runName) {
                setRunName(payload.run_name);
            }
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
                        }, placeholder: "Run name" }), _jsx(Input, { value: minSupport, onChange: (e) => setMinSupport(e.target.value), placeholder: "Min support" }), _jsx(Input, { value: minConfidence, onChange: (e) => setMinConfidence(e.target.value), placeholder: "Min confidence" }), _jsx(Input, { value: minLift, onChange: (e) => setMinLift(e.target.value), placeholder: "Min lift" }), _jsx(Input, { type: "date", value: periodStart, onChange: (e) => setPeriodStart(e.target.value), title: "Tanggal awal transaksi yang dianalisis" }), _jsx(Input, { type: "date", value: periodEnd, onChange: (e) => setPeriodEnd(e.target.value), title: "Tanggal akhir transaksi yang dianalisis" }), _jsx("div", { className: "flex flex-col gap-2 sm:flex-row lg:col-span-2", children: _jsx(Button, { className: "sm:whitespace-nowrap", onClick: handleRun, disabled: loading, children: loading ? "Running..." : "Run" }) }), error ? _jsx("div", { className: "md:col-span-4 text-sm text-red-600", children: error }) : null, ok ? _jsx("div", { className: "md:col-span-4 text-sm text-emerald-700", children: ok }) : null] })] }));
}
