export interface Service {
  id: number;
  company: string;
  service_provider: string;
  recipient_address: number;
  company_card: string | null;
  title: string;
  slug: string;
  descriptions: string;
  payment_status: string;
  payment_status_display: string;
  service_status: string;
  service_status_display: string;
  is_invoiced: boolean;
  started_at: string;
  finished_at: string;
  created_at: string;
  updated_at: string;
  overall_score: number | null;
  time_elapsed: number;
  payment_method: string;
  transaction_screenshot: string;
}