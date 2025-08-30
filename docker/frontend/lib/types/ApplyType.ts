export type ApplyType = {
  Details: Detail[];
  time: string;
  type: string;
  applicant: string;
  status: number;
  file?: File;
};

type Detail = {
  title: string;
  money: number;
};
