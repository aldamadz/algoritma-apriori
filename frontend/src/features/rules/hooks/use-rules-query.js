import { useQuery } from "@tanstack/react-query";
import { fetchRules } from "../api";
export const useRulesQuery = (params) => useQuery({
    queryKey: ["rules", params],
    queryFn: () => fetchRules(params),
    staleTime: 60_000,
});
