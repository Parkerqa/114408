import API from "@/lib/api/api";
import { Response } from "@/lib/types/ResponseType";
import { AuthFormData } from "@/lib/types/UserAPIType";

const userAPI = {
  register: (data: AuthFormData): Promise<Response<any>> =>
    API.post(`/register`, data, {
      headers: { "Content-Type": "application/json" },
      toast: true,
    }),
  login: (data: AuthFormData): Promise<Response<any>> =>
    API.post("/login", data, {
      headers: { "Content-Type": "application/json" },
      toast: true,
    }),
  // verifyToken:(token:string):Promise<Response>=>
  getTheme: (): Promise<Response<any>> => API.get(``),
  getRole: (): Promise<Response<any>> => API.get(`/`),
  getUser: (): Promise<Response<any>> => API.get(`/list_user`),
};

export default userAPI;
