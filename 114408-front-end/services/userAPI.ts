import API from "@/lib/api/api";
import { Response } from "@/lib/api/requestType";
import { Login, Register } from "@/lib/types/UserAPIType";

const userAPI = {
  register: (data: Register): Promise<Response<any>> =>
    API.post(`/register`, data, {
      headers: { "Content-Type": "application/json" },
    }),
  login: (data: Login): Promise<any> => API.post("/login"),
};

export default userAPI;
