import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
const ruleText = (rule) => {
    if (!rule)
        return "-";
    return `Jika [${rule.antecedent.join(", ")}] maka [${rule.consequent.join(", ")}]`;
};
export function CompareRunsPanel({ runs }) {
    const [runA, setRunA] = useState("");
    const [runB, setRunB] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [result, setResult] = useState(null);
    useEffect(() => {
        if (runs.length >= 2) {
            setRunA(String(runs[0].id));
            setRunB(String(runs[1].id));
        }
        else if (runs.length === 1) {
            setRunA(String(runs[0].id));
            setRunB(String(runs[0].id));
        }
    }, [runs]);
    const runLabel = useMemo(() => {
        const map = new Map();
        runs.forEach((r) => map.set(String(r.id), `${r.id} - ${r.run_name}`));
        return map;
    }, [runs]);
    const compare = async () => {
        if (!runA || !runB)
            return;
        setLoading(true);
        setError("");
        setResult(null);
        try {
            const base = import.meta.env.VITE_API_BASE_URL ?? "";
            const [aRes, bRes] = await Promise.all([
                fetch(`${base}/api/analysis/runs/${runA}/rules?min_confidence=0&min_lift=0&limit=1`),
                fetch(`${base}/api/analysis/runs/${runB}/rules?min_confidence=0&min_lift=0&limit=1`),
            ]);
            if (!aRes.ok || !bRes.ok) {
                throw new Error(`Gagal membandingkan run. HTTP ${aRes.status}/${bRes.status}`);
            }
            const aJson = (await aRes.json());
            const bJson = (await bRes.json());
            setResult({
                aTotal: aJson.summary.totalRules,
                bTotal: bJson.summary.totalRules,
                delta: bJson.summary.totalRules - aJson.summary.totalRules,
                aTopRule: aJson.summary.topLiftRule,
                bTopRule: bJson.summary.topLiftRule,
                aDominantDept: aJson.summary.dominantDepartment,
                bDominantDept: bJson.summary.dominantDepartment,
            });
        }
        catch (e) {
            setError(e instanceof Error ? e.message : "Gagal membandingkan run.");
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsxs(Card, { children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Bandingkan 2 Run" }) }), _jsxs(CardContent, { className: "space-y-3", children: [_jsxs("div", { className: "grid gap-3 sm:grid-cols-2 lg:grid-cols-3", children: [_jsx("select", { className: "h-10 rounded-md border border-slate-300 bg-white px-3 text-sm", value: runA, onChange: (e) => setRunA(e.target.value), children: runs.map((r) => (_jsxs("option", { value: r.id, children: [r.id, " - ", r.run_name] }, `a-${r.id}`))) }), _jsx("select", { className: "h-10 rounded-md border border-slate-300 bg-white px-3 text-sm", value: runB, onChange: (e) => setRunB(e.target.value), children: runs.map((r) => (_jsxs("option", { value: r.id, children: [r.id, " - ", r.run_name] }, `b-${r.id}`))) }), _jsx(Button, { className: "w-full sm:w-auto", onClick: compare, disabled: loading || runs.length === 0, children: loading ? "Comparing..." : "Bandingkan" })] }), error ? _jsx("div", { className: "text-sm text-red-600", children: error }) : null, result ? (_jsxs("div", { className: "space-y-2 break-words text-sm", children: [_jsxs("div", { children: ["Total Rules: ", _jsx("strong", { children: runLabel.get(runA) }), " = ", result.aTotal, " |", " ", _jsx("strong", { children: runLabel.get(runB) }), " = ", result.bTotal] }), _jsxs("div", { children: ["Delta (B - A):", " ", _jsx("strong", { className: result.delta >= 0 ? "text-emerald-700" : "text-amber-700", children: result.delta })] }), _jsxs("div", { children: ["Top Rule A: ", ruleText(result.aTopRule)] }), _jsxs("div", { children: ["Top Rule B: ", ruleText(result.bTopRule)] }), _jsxs("div", { children: ["Jurusan Dominan A/B: ", result.aDominantDept ?? "-", " / ", result.bDominantDept ?? "-"] })] })) : null] })] }));
}
