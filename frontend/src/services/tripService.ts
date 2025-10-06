import { apiClient } from './api';
import {
  Trip,
  TripCreate,
  TripUpdate,
  TripWithDetails,
  TripSummary,
} from '../types';

export class TripService {
  private static readonly BASE_URL = '/api/trips';

  static async createTrip(tripData: TripCreate): Promise<Trip> {
    return apiClient.post<Trip>(this.BASE_URL, tripData);
  }

  static async getTrips(skip = 0, limit = 100): Promise<Trip[]> {
    return apiClient.get<Trip[]>(this.BASE_URL, { skip, limit });
  }

  static async getTrip(tripId: number): Promise<TripWithDetails> {
    return apiClient.get<TripWithDetails>(`${this.BASE_URL}/${tripId}`);
  }

  static async getTripByInviteCode(inviteCode: string): Promise<Trip> {
    return apiClient.get<Trip>(`${this.BASE_URL}/invite/${inviteCode}`);
  }

  static async updateTrip(tripId: number, tripData: TripUpdate): Promise<Trip> {
    return apiClient.put<Trip>(`${this.BASE_URL}/${tripId}`, tripData);
  }

  static async deleteTrip(tripId: number): Promise<void> {
    return apiClient.delete<void>(`${this.BASE_URL}/${tripId}`);
  }

  static async getTripSummary(tripId: number): Promise<TripSummary> {
    return apiClient.get<TripSummary>(`${this.BASE_URL}/${tripId}/summary`);
  }

  static async regenerateInviteCode(tripId: number): Promise<Trip> {
    return apiClient.post<Trip>(`${this.BASE_URL}/${tripId}/regenerate-invite`);
  }
}
