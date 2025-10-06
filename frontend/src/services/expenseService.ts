import { apiClient } from './api';
import {
  Expense,
  ExpenseCreate,
  ExpenseUpdate,
  ExpenseCategory,
  ExpenseCategoryCreate,
  ExpenseFilters,
  ExpenseCategoryEnum,
} from '../types';

export class ExpenseService {
  private static readonly BASE_URL = '/api/trips';

  static async createExpense(tripId: number, expenseData: ExpenseCreate): Promise<Expense> {
    return apiClient.post<Expense>(`${this.BASE_URL}/${tripId}/expenses`, expenseData);
  }

  static async getExpenses(
    tripId: number,
    filters: ExpenseFilters & { skip?: number; limit?: number } = {}
  ): Promise<Expense[]> {
    const { skip = 0, limit = 100, ...filterParams } = filters;
    const params = { skip, limit, ...filterParams };
    return apiClient.get<Expense[]>(`${this.BASE_URL}/${tripId}/expenses`, params);
  }

  static async getExpense(tripId: number, expenseId: number): Promise<Expense> {
    return apiClient.get<Expense>(`${this.BASE_URL}/${tripId}/expenses/${expenseId}`);
  }

  static async updateExpense(tripId: number, expenseId: number, expenseData: ExpenseUpdate): Promise<Expense> {
    return apiClient.put<Expense>(`${this.BASE_URL}/${tripId}/expenses/${expenseId}`, expenseData);
  }

  static async deleteExpense(tripId: number, expenseId: number): Promise<void> {
    return apiClient.delete<void>(`${this.BASE_URL}/${tripId}/expenses/${expenseId}`);
  }

  static async getExpenseSummary(tripId: number): Promise<{
    by_category: Record<string, number>;
    by_date: Record<string, number>;
  }> {
    return apiClient.get(`${this.BASE_URL}/${tripId}/expenses/summary`);
  }

  static async getExpensesByMember(tripId: number): Promise<Record<string, {
    name: string;
    total_paid: number;
  }>> {
    return apiClient.get(`${this.BASE_URL}/${tripId}/expenses/by-member`);
  }

  // Expense Categories
  static async createExpenseCategory(tripId: number, categoryData: ExpenseCategoryCreate): Promise<ExpenseCategory> {
    return apiClient.post<ExpenseCategory>(`${this.BASE_URL}/${tripId}/categories`, categoryData);
  }

  static async getExpenseCategories(tripId: number): Promise<ExpenseCategory[]> {
    return apiClient.get<ExpenseCategory[]>(`${this.BASE_URL}/${tripId}/categories`);
  }

  static async deleteExpenseCategory(tripId: number, categoryId: number): Promise<void> {
    return apiClient.delete<void>(`${this.BASE_URL}/${tripId}/categories/${categoryId}`);
  }
}
