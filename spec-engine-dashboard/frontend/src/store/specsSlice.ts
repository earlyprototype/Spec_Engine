import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiService } from '../services/api';

export interface Spec {
  id: string;
  descriptor: string;
  dnaCode: string;
  goal: string;
  status: string;
  filePath: string;
  createdAt: string;
  updatedAt: string;
}

interface SpecsState {
  specs: Spec[];
  currentSpec: Spec | null;
  parameters: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: SpecsState = {
  specs: [],
  currentSpec: null,
  parameters: null,
  loading: false,
  error: null,
};

// Async thunks
export const fetchSpecs = createAsyncThunk(
  'specs/fetchSpecs',
  async (filters?: { dnaCode?: string; status?: string; search?: string }) => {
    const response = await apiService.listSpecs(filters);
    return response.data.specs; // Extract specs array
  }
);

export const fetchSpec = createAsyncThunk(
  'specs/fetchSpec',
  async (specId: string) => {
    const response = await apiService.getSpec(specId);
    return response.data;
  }
);

export const fetchParameters = createAsyncThunk(
  'specs/fetchParameters',
  async (specId: string) => {
    const response = await apiService.getParameters(specId);
    return response.data.content;
  }
);

export const updateParameters = createAsyncThunk(
  'specs/updateParameters',
  async ({ specId, content }: { specId: string; content: string }) => {
    const response = await apiService.updateParameters(specId, content);
    return response.data;
  }
);

export const createSpec = createAsyncThunk(
  'specs/createSpec',
  async (data: { dnaCode: string; descriptor: string; goal: string; tasks?: string[] }) => {
    const response = await apiService.createSpec(data);
    return response.data.spec; // Extract spec object
  }
);

// Slice
const specsSlice = createSlice({
  name: 'specs',
  initialState,
  reducers: {
    clearCurrentSpec: (state) => {
      state.currentSpec = null;
      state.parameters = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch specs
      .addCase(fetchSpecs.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSpecs.fulfilled, (state, action) => {
        state.loading = false;
        state.specs = action.payload;
      })
      .addCase(fetchSpecs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch SPECs';
      })
      // Fetch single spec
      .addCase(fetchSpec.fulfilled, (state, action) => {
        state.currentSpec = action.payload;
      })
      // Fetch parameters
      .addCase(fetchParameters.fulfilled, (state, action) => {
        state.parameters = action.payload;
      })
      // Create spec
      .addCase(createSpec.fulfilled, (state, action) => {
        state.specs.push(action.payload);
        state.currentSpec = action.payload;
      });
  },
});

export const { clearCurrentSpec, clearError } = specsSlice.actions;
export default specsSlice.reducer;
