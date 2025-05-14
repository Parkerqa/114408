import API from "@/lib/api/api";
import { Response } from "@/lib/types/ResponseType";
import { AuthFormData, EditUser } from "@/lib/types/UserAPIType";

const BASE_URL = "user";

const userAPI = {
  register: (data: AuthFormData): Promise<Response<any>> =>
    API.post(`${BASE_URL}/register`, data, {
      headers: { "Content-Type": "application/json" },
      toast: true,
    }),
  login: (data: AuthFormData): Promise<Response<any>> =>
    API.post(`${BASE_URL}/login`, data, {
      headers: { "Content-Type": "application/json" },
      toast: true,
    }),
  getConfig: (): Promise<Response<any>> => API.get(`${BASE_URL}/me_config`),
  getUser: (): Promise<Response<any>> => API.get(`${BASE_URL}/me`),
  editUser: (data: EditUser): Promise<Response<any>> =>
    API.patch(`${BASE_URL}/change_user_info`, data, {
      headers: { "Content-Type": "application/json" },
      toast: true,
    }),
};

export default userAPI;
