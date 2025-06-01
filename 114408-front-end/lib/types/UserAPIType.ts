export type AuthFormData = {
  username: string;
  email: string;
  password: string;
};

export type Login = {
  email: string;
  password: string;
};

export type EditUser = {
  email?: string;
  password?: string;
  username?: string;
  img?: File;
};
