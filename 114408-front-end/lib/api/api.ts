import axios, { InternalAxiosRequestConfig, AxiosHeaders } from "axios";

const API = axios.create({ baseURL: process.env.NEXT_PUBLIC_API_URL });

API.interceptors.request.use(function (config: InternalAxiosRequestConfig) {
  if (!config.headers) {
    config.headers = new AxiosHeaders();
  }
  if (!config.headers["Content-Type"]) {
    config.headers["Content-Type"] = "application/json";
  }
  if (localStorage.getItem("token")) {
    config.headers["Authorization"] = `Bearer ${localStorage.getItem("token")}`;
  }
  return config;
});

API.interceptors.response.use(
  async (config) => {
    if (!config.data.result) {
      throw config.data;
    } else {
      if (config.headers["x-auth-token"]) {
        localStorage.setItem("token", config.headers["x-auth-token"]);
      }
    }
    return config.data;
  },
  (error) => Promise.reject(error.response.data)
);

export default API;
