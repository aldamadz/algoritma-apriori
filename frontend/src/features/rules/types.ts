export type AssociationRule = {
  id: string;
  antecedent: string[];
  consequent: string[];
  support: number;
  confidence: number;
  lift: number;
  supportCount: number;
};

export type RulesQueryParams = {
  analysisRunId: string;
  departmentId?: string;
  q?: string;
  minConfidence?: number;
  minLift?: number;
  page?: number;
  limit?: number;
  sortBy?: "lift" | "confidence" | "support";
  sortDir?: "asc" | "desc";
  periodStart?: string;
  periodEnd?: string;
};

export type RulesApiResponse = {
  data: AssociationRule[];
  meta: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
  summary: {
    totalRules: number;
    topLiftRule?: AssociationRule;
    dominantDepartment?: string;
  };
};

export type RulesFilters = Omit<RulesQueryParams, "analysisRunId">;
