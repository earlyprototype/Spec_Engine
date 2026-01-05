import { useEffect, useState } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  LinearProgress,
  Alert,
  Chip,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';
import { CheckCircle, Error, PlayArrow } from '@mui/icons-material';
import { socketService } from '../../services/socket';

interface ProgressState {
  status: string;
  currentTask?: number;
  currentStep?: number;
  totalTasks?: number;
  totalSteps?: number;
  goalAchievementStatus?: string;
  tasks?: any[];
}

export default function ExecutionMonitorPage() {
  const { specId } = useParams<{ specId: string }>();
  const location = useLocation();
  const executionId = (location.state as any)?.executionId;

  const [progress, setProgress] = useState<ProgressState | null>(null);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Connect to WebSocket
    socketService.connect();
    setConnected(socketService.isConnected());

    // Subscribe to progress updates
    if (specId) {
      const progressHandler = (progressData: any) => {
        console.log('Progress update received:', progressData);
        setProgress(progressData);
      };

      socketService.subscribeToProgress(specId, progressHandler);

      // Cleanup
      return () => {
        socketService.unsubscribeFromProgress(specId, progressHandler);
      };
    }
  }, [specId]);

  const getStatusIcon = (status: string) => {
    if (status === 'completed' || status === 'success') {
      return <CheckCircle color="success" />;
    } else if (status === 'failed' || status === 'error') {
      return <Error color="error" />;
    } else {
      return <PlayArrow color="primary" />;
    }
  };

  const getStatusColor = (status: string): "default" | "success" | "error" | "warning" | "info" | "primary" | "secondary" => {
    if (status === 'completed' || status === 'success') return 'success';
    if (status === 'failed' || status === 'error') return 'error';
    if (status === 'running' || status === 'in_progress') return 'primary';
    return 'default';
  };

  const calculateProgress = (): number => {
    if (!progress || !progress.totalTasks) return 0;
    const current = progress.currentTask || 0;
    return Math.round((current / progress.totalTasks) * 100);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Monitor Execution: {specId}
      </Typography>
      
      {executionId && (
        <Typography variant="body2" color="text.secondary" paragraph>
          Execution ID: {executionId}
        </Typography>
      )}

      {!connected && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          WebSocket not connected. Real-time updates unavailable.
        </Alert>
      )}

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      {/* Overall Progress */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">Overall Progress</Typography>
          {progress && (
            <Chip 
              label={progress.status || 'pending'} 
              color={getStatusColor(progress.status)}
            />
          )}
        </Box>
        <LinearProgress 
          variant="determinate" 
          value={calculateProgress()} 
          sx={{ height: 10, borderRadius: 1 }}
        />
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          {calculateProgress()}% complete
          {progress?.currentTask && progress?.totalTasks && (
            <> - Task {progress.currentTask} of {progress.totalTasks}</>
          )}
        </Typography>
      </Paper>

      {/* Current Task/Step */}
      {progress && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Current Progress
          </Typography>
          <Divider sx={{ mb: 2 }} />
          
          <Box display="flex" gap={2} mb={2}>
            <Card variant="outlined" sx={{ flex: 1 }}>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary">
                  Current Task
                </Typography>
                <Typography variant="h5">
                  {progress.currentTask || '-'}
                </Typography>
              </CardContent>
            </Card>
            <Card variant="outlined" sx={{ flex: 1 }}>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary">
                  Current Step
                </Typography>
                <Typography variant="h5">
                  {progress.currentStep || '-'}
                </Typography>
              </CardContent>
            </Card>
            {progress.goalAchievementStatus && (
              <Card variant="outlined" sx={{ flex: 1 }}>
                <CardContent>
                  <Typography variant="subtitle2" color="text.secondary">
                    Goal Status
                  </Typography>
                  <Chip 
                    label={progress.goalAchievementStatus}
                    color={
                      progress.goalAchievementStatus === 'ACHIEVED' ? 'success' :
                      progress.goalAchievementStatus === 'PARTIAL' ? 'warning' : 'error'
                    }
                  />
                </CardContent>
              </Card>
            )}
          </Box>
        </Paper>
      )}

      {/* Task List */}
      {progress?.tasks && progress.tasks.length > 0 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Tasks
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <List>
            {progress.tasks.map((task: any, index: number) => (
              <ListItem key={index} sx={{ borderBottom: '1px solid #eee' }}>
                <Box mr={2}>
                  {getStatusIcon(task.status)}
                </Box>
                <ListItemText
                  primary={`Task ${task.id || index + 1}: ${task.name || 'Unnamed task'}`}
                  secondary={`Status: ${task.status || 'pending'} | Steps: ${task.stepsCompleted || 0}/${task.totalSteps || 0}`}
                />
                <Chip 
                  label={task.status || 'pending'}
                  size="small"
                  color={getStatusColor(task.status)}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}

      {!progress && (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="body1" color="text.secondary">
            Waiting for execution to start...
          </Typography>
        </Paper>
      )}
    </Box>
  );
}
