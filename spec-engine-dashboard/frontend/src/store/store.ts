import { configureStore } from '@reduxjs/toolkit';
import dnaReducer from './dnaSlice';
import specsReducer from './specsSlice';
import executionReducer from './executionSlice';

export const store = configureStore({
  reducer: {
    dna: dnaReducer,
    specs: specsReducer,
    execution: executionReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
