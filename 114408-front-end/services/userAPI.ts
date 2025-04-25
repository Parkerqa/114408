import API from "@/lib/api/api";
import { AuthFormData } from "@/lib/types/UserAPIType";

const userAPI = {
  register: (data: AuthFormData): Promise<any> =>
    API.post(`/register`, data, {
      headers: { "Content-Type": "application/json" },
      toast: true,
    }),
  login: (data: AuthFormData): Promise<any> =>
    API.post("/login", data, {
      headers: { "Content-Type": "application/json" },
    }),
};

export default userAPI;
