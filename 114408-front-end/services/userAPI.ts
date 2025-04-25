import API from "@/lib/api/api";
import { Response } from "@/lib/api/requestType";
import { AuthFormData } from "@/lib/types/UserAPIType";

const userAPI = {
  register: (data: AuthFormData): Promise<any> =>
    API.post(`/register`, data, {
      headers: { "Content-Type": "application/json" },
    }),
  login: (data: AuthFormData): Promise<any> =>
    API.post("/login", data, {
      headers: { "Content-Type": "application/json" },
    }),
};

export default userAPI;
