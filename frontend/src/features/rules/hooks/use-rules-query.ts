import { useQuery } from "@tanstack/react-query";

import { fetchRules } from "../api";
import type { RulesQueryParams } from "../types";

export const useRulesQuery = (params: RulesQueryParams) =>
  useQuery({
    queryKey: ["rules", params],
    queryFn: () => fetchRules(params),
    staleTime: 60_000,
  });
