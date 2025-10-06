// Enums
export enum CurrencyEnum {
  VND = 'VND',
  USD = 'USD',
  EUR = 'EUR',
  JPY = 'JPY',
  KRW = 'KRW',
  THB = 'THB'
}

export enum ExpenseCategoryEnum {
  FOOD = 'food',
  TRANSPORT = 'transport',
  ACCOMMODATION = 'accommodation',
  ENTERTAINMENT = 'entertainment',
  SHOPPING = 'shopping',
  OTHER = 'other'
}

// Base interfaces
export interface Trip {
  id: number;
  name: string;
  description?: string;
  destination: string;
  start_date: string;
  end_date: string;
  currency: CurrencyEnum;
  child_factor: number;
  rounding_rule: number;
  invite_code: string;
  created_at: string;
  updated_at: string;
}

export interface TripMember {
  id: number;
  trip_id: number;
  name: string;
  email?: string;
  factor: number;
  is_admin: boolean;
  created_at: string;
}

export interface Activity {
  id: number;
  trip_id: number;
  name: string;
  description?: string;
  date: string;
  location?: string;
  latitude?: number;
  longitude?: number;
  created_at: string;
  updated_at: string;
}

export interface Expense {
  id: number;
  trip_id: number;
  activity_id?: number;
  paid_by: number;
  description: string;
  amount: number;
  currency: CurrencyEnum;
  exchange_rate: number;
  category: ExpenseCategoryEnum;
  is_shared: boolean;
  date: string;
  created_at: string;
  updated_at: string;
  paid_by_member: TripMember;
}

export interface ExpenseCategory {
  id: number;
  trip_id: number;
  name: string;
  color: string;
  created_at: string;
}

// Create/Update interfaces
export interface TripCreate {
  name: string;
  description?: string;
  destination: string;
  start_date: string;
  end_date: string;
  currency?: CurrencyEnum;
  child_factor?: number;
  rounding_rule?: number;
}

export interface TripUpdate {
  name?: string;
  description?: string;
  destination?: string;
  start_date?: string;
  end_date?: string;
  currency?: CurrencyEnum;
  child_factor?: number;
  rounding_rule?: number;
}

export interface TripMemberCreate {
  name: string;
  email?: string;
  factor?: number;
}

export interface TripMemberUpdate {
  name?: string;
  email?: string;
  factor?: number;
}

export interface ActivityCreate {
  name: string;
  description?: string;
  date: string;
  location?: string;
  latitude?: number;
  longitude?: number;
}

export interface ActivityUpdate {
  name?: string;
  description?: string;
  date?: string;
  location?: string;
  latitude?: number;
  longitude?: number;
}

export interface ExpenseCreate {
  paid_by: number;
  description: string;
  amount: number;
  currency: CurrencyEnum;
  exchange_rate?: number;
  category?: ExpenseCategoryEnum;
  is_shared?: boolean;
  date: string;
  activity_id?: number;
}

export interface ExpenseUpdate {
  description?: string;
  amount?: number;
  currency?: CurrencyEnum;
  exchange_rate?: number;
  category?: ExpenseCategoryEnum;
  is_shared?: boolean;
  date?: string;
  paid_by?: number;
  activity_id?: number;
}

export interface ExpenseCategoryCreate {
  name: string;
  color?: string;
}

// Complex response types
export interface TripWithDetails extends Trip {
  members: TripMember[];
  activities: Activity[];
  expenses: Expense[];
}

export interface MemberBalance {
  member_id: number;
  member_name: string;
  total_paid: number;
  total_owed: number;
  balance: number;
}

export interface Settlement {
  from_member_id: number;
  from_member_name: string;
  to_member_id: number;
  to_member_name: string;
  amount: number;
}

export interface TripSummary {
  trip: Trip;
  total_expenses: number;
  total_shared_expenses: number;
  member_balances: MemberBalance[];
  settlements: Settlement[];
  expense_by_category: Record<string, number>;
  expense_by_date: Record<string, number>;
}

// API response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

// UI State types
export interface LoadingState {
  isLoading: boolean;
  error?: string;
}

export interface FormState<T> {
  data: T;
  errors: Record<string, string>;
  isSubmitting: boolean;
}

// Filter types
export interface ExpenseFilters {
  category?: ExpenseCategoryEnum;
  paid_by?: number;
  date_from?: string;
  date_to?: string;
  is_shared?: boolean;
}

// Map types
export interface MapLocation {
  latitude: number;
  longitude: number;
  address?: string;
}

// Theme types
export interface ThemeConfig {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  surface: string;
  text: string;
}

// Language types
export type Language = 'vi' | 'en';

export interface LanguageConfig {
  code: Language;
  name: string;
  flag: string;
}
