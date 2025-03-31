import API from "@/lib/api/api";
import { Response } from "@/lib/api/requestType";

const userAPI = {
  'register': (): Promise<Response<any>> => API.post(`/register`),
};
