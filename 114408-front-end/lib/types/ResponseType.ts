export type Response<T> = {
  message: string;
  state: string;
  statusCode: number;
  data?: T;
};
