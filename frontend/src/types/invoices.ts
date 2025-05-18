interface InvoiceItem {
  service: string;
  amount: number;
  created_at: string;
}

export interface Invoice {
  id: string;
  company: string;
  total_amount: number;
  is_paid: boolean;
  deadline: string;
  deadline_status: string;
  created_at: string;
  updated_at: string;
  items: InvoiceItem[];
}
