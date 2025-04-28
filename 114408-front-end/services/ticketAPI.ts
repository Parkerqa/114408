import API from "@/lib/api/api";

const ticketAPI = {
  getList: (): Promise<any> => API.get("/list_ticket"),
};

export default ticketAPI;
