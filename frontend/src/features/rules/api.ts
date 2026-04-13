import type { RulesApiResponse, RulesQueryParams } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

const buildQueryString = (params: RulesQueryParams): string => {
  const q = new URLSearchParams();
  if (params.departmentId) q.set("department_id", params.departmentId);
  if (params.q) q.set("q", params.q);
  if (params.minConfidence !== undefined) q.set("min_confidence", String(params.minConfidence));
  if (params.minLift !== undefined) q.set("min_lift", String(params.minLift));
  if (params.page) q.set("page", String(params.page));
  if (params.limit) q.set("limit", String(params.limit));
  if (params.sortBy) q.set("sort_by", params.sortBy);
  if (params.sortDir) q.set("sort_dir", params.sortDir);
  if (params.periodStart) q.set("period_start", params.periodStart);
  if (params.periodEnd) q.set("period_end", params.periodEnd);
  return q.toString();
};

export const fetchRules = async (params: RulesQueryParams): Promise<RulesApiResponse> => {
  const qs = buildQueryString(params);
  const url = `${API_BASE_URL}/api/analysis/runs/${params.analysisRunId}/rules${qs ? `?${qs}` : ""}`;
  const res = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    throw new Error(`Gagal mengambil data rules: HTTP ${res.status}`);
  }

  return (await res.json()) as RulesApiResponse;
};
