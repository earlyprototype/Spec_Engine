import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { apiService } from '../services/api';

export interface Execution {
  id: string;
  specId: string;
  mode: string;
  status: string;
  goalStatus?: string;
  startedAt: string;
  completedAt?: string;
  duration?: number;
  errorMessage?: string;
}

interface ExecutionState {
  executions: Execution[];
  currentExecution: Execution | null;
  progress: any;
  loading: boolean;
  error: string | null;
}

const initialState: ExecutionState = {
  executions: [],
  currentExecution: null,
  progress: null,
  loading: false,
  error: null,
};

// Async thunks
export const fetchExecutions = createAsyncThunk(
  'execution/fetchExecutions',
  async (filters?: { specId?: string; status?: string }) => {
    const response = await apiService.listExecutions(filters);
    return response.data.executions; // Extract executions array
  }
);

export const fetchExecution = createAsyncThunk(
  'execution/fetchExecution',
  async (executionId: string) => {
    const response = await apiService.getExecution(executionId);
    return response.data.execution; // Extract execution object
  }
);

export const startExecution = createAsyncThunk(
  'execution/startExecution',
  async (data: { specId: string; mode: string }) => {
    const response = await apiService.startExecution(data);
    return response.data.execution; // Extract execution object
  }
);

export const stopExecution = createAsyncThunk(
  'execution/stopExecution',
  async (executionId: string) => {
    const response = await apiService.stopExecution(executionId);
    return response.data;
  }
);

// Slice
const executionSlice = createSlice({
  name: 'execution',
  initialState,
  reducers: {
    updateProgress: (state, action) => {
      state.progress = action.payload;
    },
    clearCurrentExecution: (state) => {
      state.currentExecution = null;
      state.progress = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch executions
      .addCase(fetchExecutions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchExecutions.fulfilled, (state, action) => {
        state.loading = false;
        state.executions = action.payload;
      })
      .addCase(fetchExecutions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch executions';
      })
      // Fetch single execution
      .addCase(fetchExecution.fulfilled, (state, action) => {
        state.currentExecution = action.payload;
      })
      // Start execution
      .addCase(startExecution.fulfilled, (state, action) => {
        state.currentExecution = action.payload;
        state.executions.unshift(action.payload);
      });
  },
});

export const { updateProgress, clearCurrentExecution, clearError } = executionSlice.actions;
export default executionSlice.reducer;
