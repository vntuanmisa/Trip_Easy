import { apiClient } from './api';
import {
  TripMember,
  TripMemberCreate,
  TripMemberUpdate,
} from '../types';

export class MemberService {
  private static readonly BASE_URL = '/api/trips';

  static async createMember(tripId: number, memberData: TripMemberCreate): Promise<TripMember> {
    return apiClient.post<TripMember>(`${this.BASE_URL}/${tripId}/members`, memberData);
  }

  static async getMembers(tripId: number): Promise<TripMember[]> {
    return apiClient.get<TripMember[]>(`${this.BASE_URL}/${tripId}/members`);
  }

  static async getMember(tripId: number, memberId: number): Promise<TripMember> {
    return apiClient.get<TripMember>(`${this.BASE_URL}/${tripId}/members/${memberId}`);
  }

  static async updateMember(tripId: number, memberId: number, memberData: TripMemberUpdate): Promise<TripMember> {
    return apiClient.put<TripMember>(`${this.BASE_URL}/${tripId}/members/${memberId}`, memberData);
  }

  static async deleteMember(tripId: number, memberId: number): Promise<void> {
    return apiClient.delete<void>(`${this.BASE_URL}/${tripId}/members/${memberId}`);
  }

  static async joinTrip(tripId: number, memberData: TripMemberCreate): Promise<TripMember> {
    return apiClient.post<TripMember>(`${this.BASE_URL}/${tripId}/join`, memberData);
  }
}
