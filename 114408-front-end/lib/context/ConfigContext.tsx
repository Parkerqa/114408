"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

import { UserInfo } from "@/lib/types/UserAPIType";
import userAPI from "@/services/userAPI";

type Role = 0 | 1;
type Theme = 0 | 1;

type ConfigContextType = {
  role: number;
  theme: number;
  setTheme: (theme: Theme) => void;
  fetchUser: () => void;
  user?: UserInfo;
};

const ConfigContext = createContext<ConfigContextType>({
  role: 0,
  theme: 0,
  user: undefined,
  setTheme: () => {},
  fetchUser: () => {},
});

export const useConfig = () => useContext(ConfigContext);

export const ConfigProvider = ({ children }: { children: React.ReactNode }) => {
  const route = useRouter();
  const [role, setRole] = useState<Role>(0);
  const [theme, setTheme] = useState<Theme>(0);
  const [user, setUser] = useState<UserInfo>();

  const fetchUser = async () => {
    try {
      const res = await userAPI.getUser();
      setUser(res.data);
    } catch {}
  };

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await userAPI.getConfig();
        setRole(res.data.priority);
        const theme = res.data.theme;
        setTheme(theme);
        document.body.setAttribute(
          "data-theme",
          theme === 1 ? "dark" : "light"
        );
      } catch (err) {
        setRole(0);
        setTheme(0);
        document.body.setAttribute("data-theme", "light");
        // route.push("/auth");
        toast.error("登入期限過期，請重新登入");
      }
    };

    fetch();
  }, []);

  useEffect(() => {
    fetchUser();
  }, []);

  return (
    <ConfigContext.Provider value={{ role, theme, setTheme, user, fetchUser }}>
      {children}
    </ConfigContext.Provider>
  );
};
