/**
 * Shared types for Ideate stage
 * 
 * This file contains TypeScript interfaces used across multiple
 * Ideate components to avoid circular dependency issues.
 */

export interface Idea {
  id: string;
  content: string;
  color: string;
  position: { x: number; y: number };
  clusterId?: string;
  evaluation?: {
    feasibility: number;
    impact: number;
  };
  createdAt: string;
}

export interface Cluster {
  id: string;
  name: string;
  color: string;
  ideaIds: string[];
}

export interface IdeateData {
  ideas: Idea[];
  clusters: Cluster[];
  lastModified: string;
}

