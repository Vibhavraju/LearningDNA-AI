import axios from 'axios';

// In dev the Vite proxy forwards /api -> http://localhost:8000. Docker/production can set VITE_API_URL.
const API_BASE_URL: string = import.meta.env.VITE_API_URL || '/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 8000,
  headers: { 'Content-Type': 'application/json' },
});

/** Learner context the backend tutor uses to adapt its answer. */
export interface TutorProfile {
  pace: string;
  preferred_format: string;
  attention: number;
  weak_topics: string[];
}

export interface TutorReply {
  response: string;
  sources: string[];
}

// Demo learner id used by the backend's simulated data (the app has no login).
const DEMO_USER_ID = 1;

export const tutorChat = async (message: string, profile: TutorProfile): Promise<TutorReply> => {
  const { data } = await apiClient.post<TutorReply>('/tutor/chat', { message, profile }, { params: { user_id: DEMO_USER_ID } });
  return { response: data.response, sources: data.sources ?? [] };
};

export const checkBackend = async (): Promise<boolean> => {
  try {
    await apiClient.get('/health', { timeout: 2500 });
    return true;
  } catch {
    return false;
  }
};
