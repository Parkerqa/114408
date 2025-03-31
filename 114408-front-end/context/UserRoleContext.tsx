"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { UserRoleContextType, Role } from "@/lib/types/UserRoleContext";

const UserRoleContext = createContext<UserRoleContextType>({
  role: null,
  loading: true,
});

export const useUserRole = () => useContext(UserRoleContext);

export function UserRoleProvider({ children }: { children: React.ReactNode }) {
  const [role, setRole] = useState<Role | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // api請求權限
    const fetchRole = async () => {
      try {
        setRole("user");
      } finally {
        setLoading(false);
      }
    };

    fetchRole();
  }, []);

  return (
    <UserRoleContext.Provider value={{ role, loading }}>
      {children}
    </UserRoleContext.Provider>
  );
}
