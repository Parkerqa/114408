import axios from "axios";
import { toast } from "sonner";
import type { AxiosRequestConfig } from "axios";

interface CustomAxiosRequestConfig extends AxiosRequestConfig {
  toast?: boolean;
}

const API = axios.create({ baseURL: process.env.NEXT_PUBLIC_API_URL });

API.interceptors.request.use((config) => {
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

API.interceptors.response.use(
  (response) => {
    const config = response.config as CustomAxiosRequestConfig;
    if (response.data?.state === "error") {
      if (config.toast) toast.error(response.data?.message || "操作失敗");
    } else {
      if (response.data.data.access_token) {
        localStorage.setItem("token", response.data.data.access_token);
      }
      if (config.toast) toast.success(response.data?.message || "操作成功");
    }
    return response.data;
  },
  (error) => {
    const config = (error?.config || {}) as CustomAxiosRequestConfig;
    if (config.toast)
      toast.error(error?.response?.data?.message || "發生錯誤，請聯繫我們處理");
    return Promise.reject(error?.response?.data || error);
  }
);

export default API;
