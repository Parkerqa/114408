"use client";

import { createContext, useContext, useEffect, useState } from "react";
import userAPI from "@/services/userAPI";

type Role = "admin" | "user" | null;

interface UserRoleContextType {
  role: Role;
}

const UserRoleContext = createContext<UserRoleContextType>({
  role: null,
});

export const useUserRole = () => useContext(UserRoleContext);

export const UserRoleProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [role, setRole] = useState<Role>(null);

  useEffect(() => {
    const fetchRole = async () => {
      try {
        const res = await userAPI.getRole();
        setRole(res.data);
      } catch (err) {
        setRole(null);
      }
    };

    fetchRole();
  }, []);

  return (
    <UserRoleContext.Provider value={{ role }}>
      {children}
    </UserRoleContext.Provider>
  );
};
