export type Response<T> = {
  message: string;
  state: string;
  data?: T;
};
