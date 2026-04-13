import { useEffect, useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { AnalysisRunOut } from "@/types/api";

type RuleLite = {
  antecedent: string[];
  consequent: string[];
  support: number;
  confidence: number;
  lift: number;
};

type RulesSummaryResponse = {
  summary: {
    totalRules: number;
    topLiftRule: RuleLite | null;
    dominantDepartment: string | null;
  };
};

type CompareResult = {
  aTotal: number;
  bTotal: number;
  delta: number;
  aTopRule: RuleLite | null;
  bTopRule: RuleLite | null;
  aDominantDept: string | null;
  bDominantDept: string | null;
};

type Props = {
  runs: AnalysisRunOut[];
};

const ruleText = (rule: RuleLite | null): string => {
  if (!rule) return "-";
  return `Jika [${rule.antecedent.join(", ")}] maka [${rule.consequent.join(", ")}]`;
};

export function CompareRunsPanel({ runs }: Props) {
  const [runA, setRunA] = useState<string>("");
  const [runB, setRunB] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<CompareResult | null>(null);

  useEffect(() => {
    if (runs.length >= 2) {
      setRunA(String(runs[0].id));
      setRunB(String(runs[1].id));
    } else if (runs.length === 1) {
      setRunA(String(runs[0].id));
      setRunB(String(runs[0].id));
    }
  }, [runs]);

  const runLabel = useMemo(() => {
    const map = new Map<string, string>();
    runs.forEach((r) => map.set(String(r.id), `${r.id} - ${r.run_name}`));
    return map;
  }, [runs]);

  const compare = async () => {
    if (!runA || !runB) return;
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
      const aJson = (await aRes.json()) as RulesSummaryResponse;
      const bJson = (await bRes.json()) as RulesSummaryResponse;

      setResult({
        aTotal: aJson.summary.totalRules,
        bTotal: bJson.summary.totalRules,
        delta: bJson.summary.totalRules - aJson.summary.totalRules,
        aTopRule: aJson.summary.topLiftRule,
        bTopRule: bJson.summary.topLiftRule,
        aDominantDept: aJson.summary.dominantDepartment,
        bDominantDept: bJson.summary.dominantDepartment,
      });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Gagal membandingkan run.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Bandingkan 2 Run</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <select
            className="h-10 rounded-md border border-slate-300 bg-white px-3 text-sm"
            value={runA}
            onChange={(e) => setRunA(e.target.value)}
          >
            {runs.map((r) => (
              <option key={`a-${r.id}`} value={r.id}>
                {r.id} - {r.run_name}
              </option>
            ))}
          </select>
          <select
            className="h-10 rounded-md border border-slate-300 bg-white px-3 text-sm"
            value={runB}
            onChange={(e) => setRunB(e.target.value)}
          >
            {runs.map((r) => (
              <option key={`b-${r.id}`} value={r.id}>
                {r.id} - {r.run_name}
              </option>
            ))}
          </select>
          <Button className="w-full sm:w-auto" onClick={compare} disabled={loading || runs.length === 0}>
            {loading ? "Comparing..." : "Bandingkan"}
          </Button>
        </div>

        {error ? <div className="text-sm text-red-600">{error}</div> : null}

        {result ? (
          <div className="space-y-2 break-words text-sm">
            <div>
              Total Rules: <strong>{runLabel.get(runA)}</strong> = {result.aTotal} |{" "}
              <strong>{runLabel.get(runB)}</strong> = {result.bTotal}
            </div>
            <div>
              Delta (B - A):{" "}
              <strong className={result.delta >= 0 ? "text-emerald-700" : "text-amber-700"}>
                {result.delta}
              </strong>
            </div>
            <div>Top Rule A: {ruleText(result.aTopRule)}</div>
            <div>Top Rule B: {ruleText(result.bTopRule)}</div>
            <div>
              Jurusan Dominan A/B: {result.aDominantDept ?? "-"} / {result.bDominantDept ?? "-"}
            </div>
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
