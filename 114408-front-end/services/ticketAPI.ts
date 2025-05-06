import API from "@/lib/api/api";
import { ticketListType } from "@/lib/types/TicketType";
import { Response } from "@/lib/types/ResponseType";

const ticketAPI = {
  getList: (): Promise<Response<ticketListType[]>> => API.get("/list_ticket"),
};

export default ticketAPI;
