export type ticketListType = {
  id: number;
  Details: {
    title: string;
    money: number;
  }[];
  time: string;
  type: string;
  invoice_number: string;
  total_money: number;
  status: string;
};

export type editTicket = {
  Details: {
    td_id: number;
    title: string;
    money: number;
  }[];
  type: number;
  invoice_number: string;
  total_money: number;
};

export type auditTicket = {
  items: {
    ticket_id: number;
    status: number;
  }[];
};

export type searchTicket = {
  status: number | number[];
  q?: string;
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

export type daily_amounts = {
  id: number;
  money: number;
};

export type bar_chart = {
  account_class: string;
  total_budget: number;
  total_amount: number;
};

export type report_ticket = {
  ticket_id: number;
  upload_date: string;
  type: string;
  title: string;
  total_money: number;
  creator_name: string;
  check_date: string;
  check_man: string;
  img_url: string;
};

export type report = {
  tickets: report_ticket[];
  top_accounts: bar_chart[];
  daily_amounts: daily_amounts[];
};
