export type SummaryRow = {
  department_id: number;
  dept_name: string;
  total_budget: number;
};

export type BudgetRow = {
  accounting_id: number;
  account_name: string;
  budget_limit: number;
};

export type EditBudget = {
  accounting_items: {
    accounting_id: number;
    budget_limit: number;
  }[];
};
