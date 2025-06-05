export type ticketListType = {
  id: number;
  time: string;
  type: string;
  title: string;
  invoice_number: string;
  money: number;
  state: string;
};

export type editBilling = {
  time: string;
  type: string;
  title: string;
  number: string;
  money: number;
  state: string;
};
