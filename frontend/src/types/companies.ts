export interface ValidationStatus {
  id: number;
  validated_by: string;
  business_license: string | null;
  business_license_status: boolean;
  overall_status: string;
  validated_at: string; // ISO date string (UTC)
  validation_notes: string;
  created_at: string;
  updated_at: string;
  company: number;
}

export interface FirstItem {
  id: number;
  icon: string | null;
  name: string;
  slug: string;
}

export interface SecondItem {
  id: number;
  icon: string | null;
  name: string;
  slug: string;
}

export interface CompanyFirstItem {
  id: number;
  first_item: FirstItem;
  compay: number; // note: using "compay" as provided, even if it might be a typo for "company"
}

export interface CompanySecondItem {
  id: number;
  second_item: SecondItem;
  compay: number;
}

// New interface for a workday
export interface Workday {
  company: number;
  day_of_week: string;         // e.g. "monday"
  day_of_week_display: string; // e.g. "دوشنبه"
  open_time: string;           // e.g. "17:38:48"
  close_time: string;          // e.g. "17:38:49"
  is_closed: boolean;
  time_range: string;          // e.g. "17:38 - 17:38"
  is_open_now: boolean;
}

export interface Company {
  id: number;
  logo: string | null;
  banner: string;
  intro_video: string | null;
  validation_status: ValidationStatus;
  workdays: Workday[]; // updated to use Workday[]
  companies_first_item: CompanyFirstItem[];
  companies_second_item: CompanySecondItem[];
  name: string;
  slug: string;
  description: string;
  website: string | null;
  email: string;
  phone_number: string;
  postal_code: string;
  founded_date: string; // use Date type if you later convert to a Date object
  linkedin: string | null;
  twitter: string | null;
  instagram: string | null;
  service_type: string;
  is_validated: boolean;
  is_off_season: boolean;
  created_at: string;
  updated_at: string;
  employer: number;
  industry: number;
}
