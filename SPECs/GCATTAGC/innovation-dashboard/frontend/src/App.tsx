import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { StageView } from './pages/StageView';
import { DiscoveryView } from './pages/DiscoveryView';
import { DefineView } from './pages/DefineView';
import { IdeateView } from './pages/IdeateView';
import { PrototypeView } from './pages/PrototypeView';
import { TestView } from './pages/TestView';
import { Landing } from './pages/Landing';
import { SummaryView } from './pages/SummaryView';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/project/:projectId/summary"
            element={
              <ProtectedRoute>
                <SummaryView />
              </ProtectedRoute>
            }
          />
          <Route
            path="/project/:projectId/define"
            element={
              <ProtectedRoute>
                <DefineView />
              </ProtectedRoute>
            }
          />
          <Route
            path="/project/:projectId/ideate"
            element={
              <ProtectedRoute>
                <IdeateView />
              </ProtectedRoute>
            }
          />
          <Route
            path="/project/:projectId/prototype"
            element={
              <ProtectedRoute>
                <PrototypeView />
              </ProtectedRoute>
            }
          />
          <Route
            path="/project/:projectId/test"
            element={
              <ProtectedRoute>
                <TestView />
              </ProtectedRoute>
            }
          />
          <Route
            path="/project/:projectId/discovery"
            element={
              <ProtectedRoute>
                <DiscoveryView />
              </ProtectedRoute>
            }
          />
          <Route
            path="/project/:projectId/:stage"
            element={
              <ProtectedRoute>
                <StageView />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
