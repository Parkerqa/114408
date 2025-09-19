import API from "@/lib/api/api";
import { Response } from "@/lib/types/ResponseType";
import {
  ticketListType,
  editTicket,
  auditTicket,
  searchTicket,
  latestTicket,
  pendingTicket,
  multiTicket,
  multiTicketDetail,
} from "@/lib/types/TicketType";

const BASE_URL = "/ticket";

const ticketAPI = {
  getList: (mode?: number): Promise<Response<ticketListType[]>> =>
    API.get(`${BASE_URL}/list`, { params: { mode: mode } }),
  getMultiList: (data: multiTicket): Promise<Response<multiTicketDetail[]>> =>
    API.post(`${BASE_URL}/multi_list`, data, {
      headers: { "Content-Type": "application/json" },
    }),
  getTicket: (id: number): Promise<Response<ticketListType>> =>
    API.get(`${BASE_URL}/list/${id}`),
  addTicket: (data: FormData): Promise<Response<any>> =>
    API.post(`${BASE_URL}/upload`, data, {
      headers: { "Content-Type": "multipart/form-data" },
      toast: true,
    }),
  editTicket: (id: number, data: editTicket): Promise<Response<any>> =>
    API.patch(`${BASE_URL}/change/${id}`, data, {
      headers: { "Content-Type": "application/json" },
      toast: true,
    }),
  deleteTicket: (id: number): Promise<Response<any>> =>
    API.delete(`${BASE_URL}/delete/${id}`, { toast: true }),
  getUnVerifyCount: (): Promise<Response<any>> =>
    API.get(`${BASE_URL}/not_write_off`),
  getLatest: (limit?: number): Promise<Response<latestTicket[]>> =>
    API.get(`${BASE_URL}/latest_approved`, { params: { limit: limit } }),
  getPending: (limit?: number): Promise<Response<pendingTicket[]>> =>
    API.get(`${BASE_URL}/pending_reimbursements`, { params: { limit: limit } }),
  getApprove: (limit?: number): Promise<Response<any>> =>
    API.get(`${BASE_URL}/approved_records`, { params: { limit: limit } }),
  auditTicket: (data: auditTicket): Promise<Response<any>> =>
    API.patch(`${BASE_URL}/audit`, data, {
      headers: { "Content-Type": "application/json" },
      toast: true,
    }),
  searchTicket: ({
    q,
    class_info_id,
    date,
    limit,
  }: searchTicket): Promise<Response<any>> =>
    API.get(`${BASE_URL}/search`, {
      params: {
        q: q,
        class_info_id: class_info_id,
        date: date,
        limit: limit,
      },
    }),
};

export default ticketAPI;
