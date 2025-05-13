export type AuthFormData = {
  email: string;
  password: string;
};

export type EditUser = {
  email?: string;
  password?: string;
  username?: string;
  img?: File;
};
