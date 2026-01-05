import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Alert,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import { Visibility as ViewIcon } from '@mui/icons-material';
import { fetchExecutions } from '../../store/executionSlice';
import type { AppDispatch, RootState } from '../../store/store';

export default function ExecutionHistoryPage() {
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();
  const { executions, loading, error } = useSelector((state: RootState) => state.execution);

  useEffect(() => {
    dispatch(fetchExecutions());
  }, [dispatch]);

  const handleView = (executionId: string) => {
    navigate(`/results/${executionId}`);
  };

  const formatDuration = (ms?: number): string => {
    if (!ms) return 'N/A';
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) return `${hours}h ${minutes % 60}m`;
    if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
    return `${seconds}s`;
  };

  const getStatusColor = (status: string): "default" | "success" | "error" | "warning" | "info" | "primary" | "secondary" => {
    if (status === 'completed') return 'success';
    if (status === 'failed') return 'error';
    if (status === 'running') return 'primary';
    return 'default';
  };

  const getGoalStatusColor = (goalStatus?: string): "default" | "success" | "error" | "warning" => {
    if (goalStatus === 'ACHIEVED') return 'success';
    if (goalStatus === 'PARTIAL') return 'warning';
    if (goalStatus === 'NOT_ACHIEVED') return 'error';
    return 'default';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Execution History
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        View all past SPEC executions and their outcomes.
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      {executions.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No Execution History
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Execute a SPEC to see its history here.
          </Typography>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell><strong>SPEC</strong></TableCell>
                <TableCell><strong>Mode</strong></TableCell>
                <TableCell><strong>Status</strong></TableCell>
                <TableCell><strong>Goal Status</strong></TableCell>
                <TableCell><strong>Started</strong></TableCell>
                <TableCell><strong>Duration</strong></TableCell>
                <TableCell align="right"><strong>Actions</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {executions.map((execution) => (
                <TableRow key={execution.id} hover>
                  <TableCell>
                    <Chip 
                      label={(execution as any).spec?.descriptor || execution.specId} 
                      variant="outlined" 
                      size="small" 
                    />
                  </TableCell>
                  <TableCell>
                    <Chip label={execution.mode} size="small" />
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={execution.status} 
                      size="small"
                      color={getStatusColor(execution.status)}
                    />
                  </TableCell>
                  <TableCell>
                    {execution.goalStatus ? (
                      <Chip 
                        label={execution.goalStatus} 
                        size="small"
                        color={getGoalStatusColor(execution.goalStatus)}
                      />
                    ) : (
                      <Typography variant="body2" color="text.secondary">-</Typography>
                    )}
                  </TableCell>
                  <TableCell>
                    {new Date(execution.startedAt).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    {formatDuration(execution.duration)}
                  </TableCell>
                  <TableCell align="right">
                    <Tooltip title="View Results">
                      <IconButton
                        size="small"
                        onClick={() => handleView(execution.id)}
                        color="primary"
                      >
                        <ViewIcon />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <Box mt={2}>
        <Typography variant="body2" color="text.secondary">
          Total: {executions.length} execution{executions.length !== 1 ? 's' : ''}
        </Typography>
      </Box>
    </Box>
  );
}
