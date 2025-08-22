import API from "@/lib/api/api";
import { Response } from "@/lib/types/ResponseType";

const BASE_URL = "https://senichini.app.n8n.cloud/webhook-test";

type n8nType = {
  reminder: string;
  labels: [];
  datasets: {label: string, data: number[]}[];
};

const n8nAPI = {
  getHome: (): Promise<Response<n8nType>> => API.get(`${BASE_URL}/admin-home`),
};

export default n8nAPI;
