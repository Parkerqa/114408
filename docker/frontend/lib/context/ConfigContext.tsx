"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

import { UserInfo } from "@/lib/types/UserAPIType";
import userAPI from "@/services/userAPI";

type Role = 0 | 1 | 2 | 3;
type Theme = 0 | 1;

type ConfigContextType = {
  role: number | undefined;
  theme: number;
  setTheme: (theme: Theme) => void;
  fetchUser: () => void;
  user?: UserInfo | null | undefined;
};

const ConfigContext = createContext<ConfigContextType>({
  role: undefined,
  theme: 0,
  user: undefined,
  setTheme: () => {},
  fetchUser: () => {},
});

export const useConfig = () => useContext(ConfigContext);

export const ConfigProvider = ({ children }: { children: React.ReactNode }) => {
  const route = useRouter();
  const [role, setRole] = useState<Role | undefined>(undefined);
  const [theme, setTheme] = useState<Theme>(0);
  const [user, setUser] = useState<UserInfo | null | undefined>(undefined);

  const fetchUser = async () => {
    try {
      const res = await userAPI.getUser();
      setUser(res.data);
    } catch {
      setUser(null);
      route.push("/auth");
    }
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
        setRole(undefined);
        setTheme(0);
        document.body.setAttribute("data-theme", "light");
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
