import API from "@/lib/api/api";
import { Response } from "@/lib/types/ResponseType";

const BASE_URL = "accounting";

const accountingAPI = {
  getTopThree: (): Promise<Response<any>> =>
    API.get(`${BASE_URL}/list_class_info`),
};

export default accountingAPI;
