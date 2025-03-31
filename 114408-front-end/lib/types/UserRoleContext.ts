export type Role = "admin" | "user";

export type UserRoleContextType = {
  role: Role | null;
  loading: boolean;
};
