export type AnalysisRunOut = {
  id: number;
  run_name: string;
  period_start: string | null;
  period_end: string | null;
  min_support: number;
  min_confidence: number;
  min_lift: number;
  status: string;
  created_at: string;
  finished_at: string | null;
};

export type DepartmentOut = {
  id: number;
  code: string;
  name: string;
};

export type ImportCsvResult = {
  totalRows: number;
  createdTransactions: number;
  createdTransactionItems: number;
  createdDepartments: number;
  createdStudents: number;
  createdBooks: number;
  errors: string[];
};
