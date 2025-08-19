import API from "@/lib/api/api";
import { Response } from "@/lib/types/ResponseType";

const BASE_URL = "setting";

const settingAPI = {
  editTheme: ({ theme }: { theme: number }): Promise<Response<any>> =>
    API.patch(
      `${BASE_URL}/change_theme`,
      { theme },
      {
        headers: { "Content-Type": "application/json" },
      }
    ),
};

export default settingAPI;
