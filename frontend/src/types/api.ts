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

export type StudentOut = {
  id: number;
  student_number: string;
  name: string;
  department_id: number;
  department_name: string | null;
};

export type BookOut = {
  id: number;
  isbn: string;
  title: string;
  author: string;
  category: string;
};

export type LoanTransactionOut = {
  id: number;
  student_id: number;
  student_number: string | null;
  student_name: string | null;
  department_name: string | null;
  loan_date: string;
  return_date: string | null;
  book_ids: number[];
  book_titles: string[];
};

export type PaginationMeta = {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
};

export type PaginatedResponse<T> = {
  data: T[];
  meta: PaginationMeta;
};

export type ImportCsvResult = {
  totalRows: number;
  createdTransactions: number;
  createdTransactionItems: number;
  createdDepartments: number;
  createdStudents: number;
  createdBooks: number;
  skippedDuplicateTransactions: number;
  removedDuplicateTransactions: number;
  errors: string[];
};

export type MonthlyTransactionSummary = {
  month: string;
  total: number;
};

export type TransactionSummary = {
  firstLoanDate: string | null;
  lastLoanDate: string | null;
  totalTransactions: number;
  monthly: MonthlyTransactionSummary[];
};

export type ResetDataResult = {
  deletedRules: number;
  deletedAnalysisRuns: number;
  deletedTransactionItems: number;
  deletedTransactions: number;
  deletedBooks: number;
  deletedStudents: number;
  deletedDepartments: number;
};
