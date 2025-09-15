import API from "@/lib/api/api";
import { BudgetRow, SummaryRow } from "@/lib/types/BudgetType";
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
    API.get(`${BASE_URL}/${dept_id}/accounts`),
};

export default departmentAPI;
