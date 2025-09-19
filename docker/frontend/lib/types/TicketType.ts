export type ticketListType = {
  id: number;
  time: string;
  type: string;
  title: string;
  invoice_number: string;
  money: number;
  state: string;
};

export type editTicket = {
  time: string;
  type: string;
  title: string;
  number: string;
  money: number;
  state: string;
};

export type auditTicket = {
  items: {
    ticket_id: number;
    status: number;
  }[];
};

export type searchTicket = {
  q?: string;
  class_info_id?: string;
  date?: string;
  limit?: number;
};

export type latestTicket = {
  title: string;
  upload_date: string;
  type: string;
  total_money: number;
};

export type pendingTicket = {
  ticket_id: number;
  upload_date: string;
  type: string;
  title: string;
  total_money: number;
  creator_name: string;
  img_url: string;
};

export type multiTicket = {
  ticket_id: number[];
};

export type multiTicketDetail = {
  ticket_id: number;
  Details: {
    title: string;
    money: number;
  }[];
  time: string;
  type: string;
  applicant: string;
  img_url: string;
  state?: number;
};
