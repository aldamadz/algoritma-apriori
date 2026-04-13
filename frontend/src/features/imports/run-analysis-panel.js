import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
export function RunAnalysisPanel({ onRan }) {
    const [runName, setRunName] = useState("manual-run");
    const [minSupport, setMinSupport] = useState("0.05");
    const [minConfidence, setMinConfidence] = useState("0.3");
    const [minLift, setMinLift] = useState("1.0");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [ok, setOk] = useState("");
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
                    min_support: Number(minSupport),
                    min_confidence: Number(minConfidence),
                    min_lift: Number(minLift),
                }),
            });
            if (!res.ok) {
                const text = await res.text();
                throw new Error(text || `HTTP ${res.status}`);
            }
            setOk("Analisis berhasil dijalankan.");
            onRan?.();
        }
        catch (e) {
            setError(e instanceof Error ? e.message : "Analisis gagal.");
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Jalankan Analisis" }) }), _jsxs(CardContent, { className: "grid gap-3 sm:grid-cols-2 lg:grid-cols-4", children: [_jsx(Input, { value: runName, onChange: (e) => setRunName(e.target.value), placeholder: "Run name" }), _jsx(Input, { value: minSupport, onChange: (e) => setMinSupport(e.target.value), placeholder: "Min support" }), _jsx(Input, { value: minConfidence, onChange: (e) => setMinConfidence(e.target.value), placeholder: "Min confidence" }), _jsxs("div", { className: "flex flex-col gap-2 sm:flex-row", children: [_jsx(Input, { value: minLift, onChange: (e) => setMinLift(e.target.value), placeholder: "Min lift" }), _jsx(Button, { className: "sm:whitespace-nowrap", onClick: handleRun, disabled: loading, children: loading ? "Running..." : "Run" })] }), error ? _jsx("div", { className: "md:col-span-4 text-sm text-red-600", children: error }) : null, ok ? _jsx("div", { className: "md:col-span-4 text-sm text-emerald-700", children: ok }) : null] })] }));
}
