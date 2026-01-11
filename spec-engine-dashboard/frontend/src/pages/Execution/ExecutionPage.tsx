import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import {
  Box,
  Typography,
  Paper,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Divider,
  Card,
  CardContent,
} from '@mui/material';
import { PlayArrow as PlayIcon, Cancel as CancelIcon } from '@mui/icons-material';
import { startExecution } from '../../store/executionSlice';
import type { AppDispatch } from '../../store/store';

export default function ExecutionPage() {
  const { dnaCode, descriptor } = useParams<{ dnaCode: string; descriptor: string }>();
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();

  const specId = `${dnaCode}/${descriptor}`;

  const [mode, setMode] = useState('dynamic');
  const [error, setError] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);

  const handleStart = async () => {
    if (!dnaCode || !descriptor) return;

    setStarting(true);
    setError(null);

    try {
      const result = await dispatch(startExecution({ specId, mode })).unwrap();
      
      // Navigate to monitor page
      navigate(`/execute/${specId}/monitor`, {
        state: { executionId: result.executionId }
      });
    } catch (err: any) {
      setError(err.message || 'Failed to start execution');
      setStarting(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Execute SPEC: {specId}
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Select an execution mode and start the SPEC execution.
      </Typography>

      <Paper sx={{ p: 3, mt: 3, maxWidth: 800 }}>
        {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

        <Typography variant="h6" gutterBottom>
          Execution Mode
        </Typography>
        <Divider sx={{ mb: 3 }} />

        <FormControl fullWidth sx={{ mb: 3 }}>
          <InputLabel>Mode</InputLabel>
          <Select
            value={mode}
            label="Mode"
            onChange={(e) => setMode(e.target.value)}
          >
            <MenuItem value="silent">Silent - Fully autonomous</MenuItem>
            <MenuItem value="dynamic">Dynamic - Autonomous with escalation (recommended)</MenuItem>
            <MenuItem value="collaborative">Collaborative - Human-in-loop</MenuItem>
          </Select>
        </FormControl>

        <Box mb={3}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="subtitle2" gutterBottom>
                Mode Description
              </Typography>
              {mode === 'silent' && (
                <Typography variant="body2" color="text.secondary">
                  Fully autonomous execution. The system will attempt all steps and backups 
                  without human intervention, only stopping if all options are exhausted.
                </Typography>
              )}
              {mode === 'dynamic' && (
                <Typography variant="body2" color="text.secondary">
                  Recommended mode. The system operates autonomously but escalates to request 
                  human input when encountering consecutive failures or backup depletion.
                </Typography>
              )}
              {mode === 'collaborative' && (
                <Typography variant="body2" color="text.secondary">
                  Human-in-loop mode. The system pauses at key decision points to request 
                  guidance and confirmation before proceeding with critical steps.
                </Typography>
              )}
            </CardContent>
          </Card>
        </Box>

        <Box display="flex" gap={2} justifyContent="flex-end">
          <Button
            variant="outlined"
            startIcon={<CancelIcon />}
            onClick={() => navigate(-1)}
            disabled={starting}
          >
            Cancel
          </Button>
          <Button
            variant="contained"
            startIcon={<PlayIcon />}
            onClick={handleStart}
            disabled={starting}
            color="success"
          >
            {starting ? 'Starting...' : 'Start Execution'}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}
