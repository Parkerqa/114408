import API from "@/lib/api/api";
import { Response } from "@/lib/types/ResponseType";
import { AuthFormData } from "@/lib/types/UserAPIType";

const userAPI = {
  register: (data: AuthFormData): Promise<Response> =>
    API.post(`/register`, data, {
      headers: { "Content-Type": "application/json" },
      toast: true,
    }),
  login: (data: AuthFormData): Promise<Response> =>
    API.post("/login", data, {
      headers: { "Content-Type": "application/json" },
      toast: true,
    }),
};

export default userAPI;
