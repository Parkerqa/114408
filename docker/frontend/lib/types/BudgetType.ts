export type BudgetRow = {
  department: string;
  account: string;
  limit: number | string;
};

export type FormValues = { budgets: BudgetRow[] };
