import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { Provider } from 'react-redux';
import { store } from './store/store';
import AppLayout from './components/layout/AppLayout';
import HomePage from './pages/HomePage';
import DnaProfilesPage from './pages/DnaProfiles/DnaProfilesPage';
import DnaCreatePage from './pages/DnaProfiles/DnaCreatePage';
import DnaDetailPage from './pages/DnaProfiles/DnaDetailPage';
import SpecsPage from './pages/Specs/SpecsPage';
import SpecDetailPage from './pages/Specs/SpecDetailPage';
import SpecCreatePage from './pages/Specs/SpecCreatePage';
import ParameterEditorPage from './pages/ParameterEditor/ParameterEditorPage';
import ExecutionPage from './pages/Execution/ExecutionPage';
import ExecutionMonitorPage from './pages/Execution/ExecutionMonitorPage';
import ResultsPage from './pages/Results/ResultsPage';
import ExecutionHistoryPage from './pages/Results/ExecutionHistoryPage';
import SettingsPage from './pages/SettingsPage';

// Create MUI theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
  },
});

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Routes>
            <Route path="/" element={<AppLayout />}>
              <Route index element={<HomePage />} />
              
              {/* DNA Profiles */}
              <Route path="dna-profiles" element={<DnaProfilesPage />} />
              <Route path="dna-profiles/create" element={<DnaCreatePage />} />
              <Route path="dna-profiles/:dnaCode" element={<DnaDetailPage />} />
              
              {/* SPECs */}
              <Route path="specs" element={<SpecsPage />} />
              <Route path="specs/create" element={<SpecCreatePage />} />
              <Route path="specs/:dnaCode/:descriptor" element={<SpecDetailPage />} />
              <Route path="specs/:dnaCode/:descriptor/edit" element={<ParameterEditorPage />} />
              
              {/* Execution */}
              <Route path="execute/:dnaCode/:descriptor" element={<ExecutionPage />} />
              <Route path="execute/:specId/monitor" element={<ExecutionMonitorPage />} />
              
              {/* Results */}
              <Route path="results/:executionId" element={<ResultsPage />} />
              <Route path="executions" element={<ExecutionHistoryPage />} />
              
              {/* Settings */}
              <Route path="settings" element={<SettingsPage />} />
              
              {/* Fallback */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </Router>
      </ThemeProvider>
    </Provider>
  );
}

export default App;
