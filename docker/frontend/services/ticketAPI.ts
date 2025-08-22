import API from "@/lib/api/api";
import { Response } from "@/lib/types/ResponseType";
import { ticketListType, editBilling } from "@/lib/types/TicketType";

const BASE_URL = "/ticket";

const ticketAPI = {
  getList: (mode?: number): Promise<Response<ticketListType[]>> =>
    API.get(`${BASE_URL}/list`, { params: { mode: mode } }),
  getBilling: (id: number): Promise<Response<ticketListType>> =>
    API.get(`${BASE_URL}/list/${id}`),
  addBilling: (data: FormData): Promise<Response<any>> =>
    API.post(`${BASE_URL}/upload`, data, {
      headers: { "Content-Type": "multipart/form-data" },
      toast: true,
    }),
  editBilling: (id: number, data: editBilling): Promise<Response<any>> =>
    API.patch(`${BASE_URL}/change/${id}`, data, {
      headers: { "Content-Type": "application/json" },
      toast: true,
    }),
  deleteBilling: (id: number): Promise<Response<any>> =>
    API.delete(`${BASE_URL}/delete/${id}`, { toast: true }),
  getUnVerifyCount: (): Promise<Response<any>> =>
    API.get(`${BASE_URL}/unaudited_invoices`),
};

export default ticketAPI;
