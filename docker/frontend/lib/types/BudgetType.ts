export type SummaryRow = {
  department: string;
  limit: number;
};

export type BudgetRow = {
  department: string;
  account: string;
  limit: number;
};

export type FormValues = { budgets: BudgetRow[] };
