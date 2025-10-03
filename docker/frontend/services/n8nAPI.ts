import N8NAPI from "@/lib/api/n8nApi";
import { Response } from "@/lib/types/ResponseType";

const BASE_URL = "webhook-test";

const n8nAPI = {
  forgetPassword: (gmail: { email: string }): Promise<Response<any>> =>
    N8NAPI.post(
      `${BASE_URL}/forget-password`, gmail,
      { toast: true }
    ),
  getSummary: (data: { question: string }): Promise<Response<any>> =>
    N8NAPI.post(`${BASE_URL}/ask-final`, data)
};

export default n8nAPI;
