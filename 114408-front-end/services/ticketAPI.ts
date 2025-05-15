import API from "@/lib/api/api";
import { ticketListType } from "@/lib/types/TicketType";
import { Response } from "@/lib/types/ResponseType";

const BASE_URL = "/ticket";

const ticketAPI = {
  getList: (): Promise<Response<ticketListType[]>> =>
    API.get(`${BASE_URL}/list`),
  addBilling: (data: FormData): Promise<Response<any>> =>
    API.post(`${BASE_URL}/upload`, data, {
      headers: { "Content-Type": "multipart/form-data" },
      toast: true,
    }),
};

export default ticketAPI;
