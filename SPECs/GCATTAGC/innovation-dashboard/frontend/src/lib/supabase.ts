/**
 * InsForge Backend Client
 * 
 * This file configures the client for our InsForge backend using the Insforge SDK.
 * 
 * Note: The export is named 'supabase' to maintain compatibility with existing code,
 * but it uses the Insforge SDK which has the same API surface.
 */
import { createClient } from '@insforge/sdk';

const insforgeUrl = import.meta.env.VITE_INSFORGE_URL;
const insforgeAnonKey = import.meta.env.VITE_INSFORGE_ANON_KEY;

if (!insforgeUrl || !insforgeAnonKey) {
  throw new Error(
    'Missing InsForge environment variables. Please check your .env file and ensure VITE_INSFORGE_URL and VITE_INSFORGE_ANON_KEY are set.'
  );
}

// Create Insforge client with the correct baseUrl
// Export as 'supabase' for compatibility with existing code
export const supabase = createClient({ baseUrl: insforgeUrl });

// Database types
export interface Project {
  id: string;
  user_id: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface StageData {
  id: string;
  project_id: string;
  stage_name: 'discovery' | 'define' | 'ideate' | 'prototype' | 'test';
  data_json: Record<string, any>;
  updated_at: string;
}


