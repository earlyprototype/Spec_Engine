import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { apiService } from '../services/api';

export interface DnaProfile {
  id: string;
  dnaCode: string;
  projectName: string;
  testing: string;
  risk: string;
  autonomy: string;
  customTools?: string;
  constraints?: string;
  createdAt: string;
  updatedAt: string;
}

interface DnaState {
  profiles: DnaProfile[];
  currentProfile: DnaProfile | null;
  loading: boolean;
  error: string | null;
}

const initialState: DnaState = {
  profiles: [],
  currentProfile: null,
  loading: false,
  error: null,
};

// Async thunks
export const fetchDnaProfiles = createAsyncThunk(
  'dna/fetchProfiles',
  async () => {
    const response = await apiService.listDnaProfiles();
    console.log('[DNA Slice] API Response:', response.data);
    console.log('[DNA Slice] Profiles extracted:', response.data.profiles || []);
    return response.data.profiles || []; // Extract profiles array
  }
);

export const fetchDnaProfile = createAsyncThunk(
  'dna/fetchProfile',
  async (dnaCode: string) => {
    const response = await apiService.getDnaProfile(dnaCode);
    return response.data.profile; // Extract profile object
  }
);

export const createDnaProfile = createAsyncThunk(
  'dna/createProfile',
  async (data: Omit<DnaProfile, 'id' | 'createdAt' | 'updatedAt'>) => {
    const response = await apiService.createDnaProfile(data);
    return response.data.profile || response.data; // Extract profile object
  }
);

export const updateDnaProfile = createAsyncThunk(
  'dna/updateProfile',
  async ({ dnaCode, data }: { dnaCode: string; data: Partial<DnaProfile> }) => {
    const response = await apiService.updateDnaProfile(dnaCode, data);
    return response.data.profile; // Extract profile object
  }
);

// Slice
const dnaSlice = createSlice({
  name: 'dna',
  initialState,
  reducers: {
    clearCurrentProfile: (state) => {
      state.currentProfile = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch profiles
      .addCase(fetchDnaProfiles.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDnaProfiles.fulfilled, (state, action) => {
        state.loading = false;
        state.profiles = action.payload;
      })
      .addCase(fetchDnaProfiles.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch DNA profiles';
      })
      // Fetch single profile
      .addCase(fetchDnaProfile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDnaProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.currentProfile = action.payload;
      })
      .addCase(fetchDnaProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch DNA profile';
      })
      // Create profile
      .addCase(createDnaProfile.fulfilled, (state, action) => {
        state.profiles.push(action.payload);
        state.currentProfile = action.payload;
      })
      // Update profile
      .addCase(updateDnaProfile.fulfilled, (state, action) => {
        const index = state.profiles.findIndex(p => p.dnaCode === action.payload.dnaCode);
        if (index !== -1) {
          state.profiles[index] = action.payload;
        }
        if (state.currentProfile?.dnaCode === action.payload.dnaCode) {
          state.currentProfile = action.payload;
        }
      });
  },
});

export const { clearCurrentProfile, clearError } = dnaSlice.actions;
export default dnaSlice.reducer;
