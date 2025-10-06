import { apiClient } from './api';
import {
  Activity,
  ActivityCreate,
  ActivityUpdate,
} from '../types';

export class ActivityService {
  private static readonly BASE_URL = '/api/trips';

  static async createActivity(tripId: number, activityData: ActivityCreate): Promise<Activity> {
    return apiClient.post<Activity>(`${this.BASE_URL}/${tripId}/activities`, activityData);
  }

  static async getActivities(tripId: number, dateFilter?: string): Promise<Activity[]> {
    const params = dateFilter ? { date_filter: dateFilter } : undefined;
    return apiClient.get<Activity[]>(`${this.BASE_URL}/${tripId}/activities`, params);
  }

  static async getActivity(tripId: number, activityId: number): Promise<Activity> {
    return apiClient.get<Activity>(`${this.BASE_URL}/${tripId}/activities/${activityId}`);
  }

  static async updateActivity(tripId: number, activityId: number, activityData: ActivityUpdate): Promise<Activity> {
    return apiClient.put<Activity>(`${this.BASE_URL}/${tripId}/activities/${activityId}`, activityData);
  }

  static async deleteActivity(tripId: number, activityId: number): Promise<void> {
    return apiClient.delete<void>(`${this.BASE_URL}/${tripId}/activities/${activityId}`);
  }

  static async getActivitiesByDate(tripId: number): Promise<Record<string, Activity[]>> {
    return apiClient.get<Record<string, Activity[]>>(`${this.BASE_URL}/${tripId}/activities/by-date`);
  }
}
