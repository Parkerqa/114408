"use client";

import { createContext, useContext, useEffect, useState } from "react";
import userAPI from "@/services/userAPI";

type Role = "admin" | "user" | null;
type Theme = 0 | 1;

interface UserRoleContextType {
  role: Role;
  theme: number;
}

const UserRoleContext = createContext<UserRoleContextType>({
  role: null,
  theme: 0,
});

export const useUserRole = () => useContext(UserRoleContext);

export const UserRoleProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [role, setRole] = useState<Role>(null);
  const [theme, setTheme] = useState<Theme>(0);

  useEffect(() => {
    const fetch = async () => {
      try {
        const [res1, res2] = await Promise.all([
          userAPI.getRole(),
          userAPI.getTheme(),
        ]);
        setRole(res1.data);
        setTheme(res2.data);
      } catch (err) {
        setRole(null);
        setTheme(0);
      }
    };

    fetch();
  }, []);

  return (
    <UserRoleContext.Provider value={{ role, theme }}>
      {children}
    </UserRoleContext.Provider>
  );
};
