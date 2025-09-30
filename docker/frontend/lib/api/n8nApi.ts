import axios from "axios";
import { toast } from "sonner";
import type { AxiosRequestConfig } from "axios";

interface CustomAxiosRequestConfig extends AxiosRequestConfig {
  toast?: boolean;
}

const N8NAPI = axios.create({ baseURL: process.env.NEXT_PUBLIC_N8NAPI_URL });

N8NAPI.interceptors.request.use((config) => {
  config.headers = config.headers || {};
  if (!config.headers["Content-Type"]) {
    config.headers["Content-Type"] = "application/json";
  }
  const token = localStorage.getItem("token");
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

N8NAPI.interceptors.response.use(
  (response) => {
    const config = response.config as CustomAxiosRequestConfig;

    const isError =
      response.data?.state === "error" || response.data?.statusCode >= 400;

    if (isError) {
      if (config.toast) {
        toast.error(response.data?.message || "操作失敗");
      }
    } else {
      if (response.data?.data?.access_token) {
        localStorage.setItem("token", response.data.data.access_token);
      }
      if (config.toast) {
        toast.success(response.data?.message || "操作成功");
      }
    }

    return response.data;
  },

  (error) => {
    const config = error.config as CustomAxiosRequestConfig;

    if (config?.toast) {
      const message =
        error?.response?.data?.message || error.message || "操作失敗";
      toast.error(message);
    }

    return Promise.reject(error);
  }
);

export default N8NAPI;
