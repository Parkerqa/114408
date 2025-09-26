import API from "@/lib/api/api";
import { BudgetRow, EditBudget, SummaryRow } from "@/lib/types/BudgetType";
import { Response } from "@/lib/types/ResponseType";

const BASE_URL = "departments";

const departmentAPI = {
  addDepartment: (): Promise<Response<any>> => API.post(`${BASE_URL}/add`),
  editDepartment: (dept_id: number): Promise<Response<any>> =>
    API.patch(`${BASE_URL}/update/${dept_id}`),
  deleteDepartment: (dept_id: number): Promise<Response<any>> =>
    API.delete(`${BASE_URL}/delete/${dept_id}`),
  getDeptSummary: (): Promise<Response<SummaryRow[]>> =>
    API.get(`${BASE_URL}/budget_summary`),
  getDeptAccount: (dept_id: number): Promise<Response<BudgetRow[]>> =>
    API.get(`${BASE_URL}/${dept_id}/show_accounts`),
  editBudget: (dept_id: number, data: EditBudget): Promise<Response<any>> =>
    API.put(`${BASE_URL}/${dept_id}/accountings`, data, {
      headers: { "Content-Type": "application/json" },
      toast: true,
    }),
  getDropdown: (): Promise<Response<any>> =>
    API.get(`${BASE_URL}/with_accounts`),
};

export default departmentAPI;
