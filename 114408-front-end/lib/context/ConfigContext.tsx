"use client";

import { createContext, useContext, useEffect, useState } from "react";
import userAPI from "@/services/userAPI";

type Role = 0 | 1;
type Theme = 0 | 1;

type ConfigContextType = {
  role: number;
  theme: number;
};

const ConfigContext = createContext<ConfigContextType>({
  role: 0,
  theme: 0,
});

export const useConfig = () => useContext(ConfigContext);

export const ConfigProvider = ({ children }: { children: React.ReactNode }) => {
  const [role, setRole] = useState<Role>(0);
  const [theme, setTheme] = useState<Theme>(0);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await userAPI.getConfig();
        setRole(res.data.priority);
        setTheme(res.data.theme);
      } catch (err) {
        setRole(0);
        setTheme(0);
      }
    };

    fetch();
  }, []);

  return (
    <ConfigContext.Provider value={{ role, theme }}>
      {children}
    </ConfigContext.Provider>
  );
};
