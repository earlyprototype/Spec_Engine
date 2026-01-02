/**
 * Shared types for Test stage
 * 
 * This file contains TypeScript interfaces used across multiple
 * Test components to avoid circular dependency issues.
 */

export interface TestSession {
  id: string;
  sessionName: string;
  date: string;
  participants: number;
  duration: number; // minutes
  methodology: string;
  status: 'planned' | 'in_progress' | 'completed';
}

export interface UserFeedback {
  id: string;
  sessionId: string;
  participantId: string;
  participantName: string;
  timestamp: string;
  satisfactionScore: number; // 1-10
  usabilityScore: number; // 1-10
  comments: string;
  painPoints: string[];
  positiveAspects: string[];
  suggestions: string[];
}

export interface MetricData {
  id: string;
  sessionId: string;
  metricName: string;
  value: number;
  unit: string;
  target?: number;
  category: 'usability' | 'performance' | 'satisfaction' | 'completion' | 'other';
}

export interface TestStageData {
  sessions: TestSession[];
  feedback: UserFeedback[];
  metrics: MetricData[];
  lastModified: string;
}

