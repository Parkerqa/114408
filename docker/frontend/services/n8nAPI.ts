import API from "@/lib/api/api";
import { Response } from "@/lib/types/ResponseType";

const BASE_URL = "http://localhost:5678/webhook-test";

type n8nType = {
  reminder: string;
  labels: [];
  datasets: {label: string, data: number[]}[];
};

const n8nAPI = {
  getHomeChart: (): Promise<Response<n8nType>> => API.get(`${BASE_URL}/home-chart`),
};

export default n8nAPI;
