import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Chip,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import { 
  CheckCircle, 
  Cancel, 
  Warning,
  Info,
} from '@mui/icons-material';
import { apiService } from '../../services/api';

export default function ResultsPage() {
  const { executionId } = useParams<{ executionId: string }>();
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResults = async () => {
      if (!executionId) return;
      
      try {
        const response = await apiService.getExecutionResults(executionId);
        setResults(response.data);
      } catch (err: any) {
        setError(err.response?.data?.message || 'Failed to load results');
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [executionId]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  const goalStatus = results?.goalStatus || results?.execution?.goalStatus;
  const completionVerification = results?.completionVerification || {};
  const postAnalysis = results?.postExecutionAnalysis || {};

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Execution Results
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Execution ID: {executionId}
      </Typography>

      {/* Goal Achievement Status */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Goal Achievement Status
        </Typography>
        <Divider sx={{ mb: 3 }} />
        
        <Box display="flex" alignItems="center" gap={2}>
          {goalStatus === 'ACHIEVED' && <CheckCircle sx={{ fontSize: 48, color: 'success.main' }} />}
          {goalStatus === 'PARTIAL' && <Warning sx={{ fontSize: 48, color: 'warning.main' }} />}
          {goalStatus === 'NOT_ACHIEVED' && <Cancel sx={{ fontSize: 48, color: 'error.main' }} />}
          {!goalStatus && <Info sx={{ fontSize: 48, color: 'info.main' }} />}
          
          <Box>
            <Chip 
              label={goalStatus || 'Unknown'} 
              color={
                goalStatus === 'ACHIEVED' ? 'success' :
                goalStatus === 'PARTIAL' ? 'warning' :
                goalStatus === 'NOT_ACHIEVED' ? 'error' : 'default'
              }
              sx={{ fontSize: '1.2rem', py: 2, px: 1 }}
            />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              {goalStatus === 'ACHIEVED' && 'All completion criteria met successfully'}
              {goalStatus === 'PARTIAL' && 'Core deliverable exists but some quality standards not met'}
              {goalStatus === 'NOT_ACHIEVED' && 'Primary deliverable missing or verification failed'}
              {!goalStatus && 'Goal status not yet determined'}
            </Typography>
          </Box>
        </Box>
      </Paper>

      {/* Completion Verification */}
      {completionVerification && Object.keys(completionVerification).length > 0 && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Completion Verification
          </Typography>
          <Divider sx={{ mb: 2 }} />
          
          <List>
            {Object.entries(completionVerification).map(([key, value]: [string, any]) => (
              <ListItem key={key}>
                <ListItemIcon>
                  {value === true || value === 'passed' ? (
                    <CheckCircle color="success" />
                  ) : (
                    <Cancel color="error" />
                  )}
                </ListItemIcon>
                <ListItemText
                  primary={key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  secondary={typeof value === 'string' ? value : (value ? 'Passed' : 'Failed')}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}

      {/* Post-Execution Analysis */}
      {postAnalysis && Object.keys(postAnalysis).length > 0 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Post-Execution Analysis
          </Typography>
          <Divider sx={{ mb: 2 }} />
          
          <Box display="flex" gap={2} flexWrap="wrap">
            {postAnalysis.failureRate !== undefined && (
              <Card variant="outlined" sx={{ flex: 1, minWidth: 200 }}>
                <CardContent>
                  <Typography variant="subtitle2" color="text.secondary">
                    Failure Rate
                  </Typography>
                  <Typography variant="h5">
                    {Math.round(postAnalysis.failureRate * 100)}%
                  </Typography>
                </CardContent>
              </Card>
            )}
            
            {postAnalysis.backupsUsed !== undefined && (
              <Card variant="outlined" sx={{ flex: 1, minWidth: 200 }}>
                <CardContent>
                  <Typography variant="subtitle2" color="text.secondary">
                    Backups Used
                  </Typography>
                  <Typography variant="h5">
                    {postAnalysis.backupsUsed}
                  </Typography>
                </CardContent>
              </Card>
            )}
            
            {postAnalysis.complianceScore !== undefined && (
              <Card variant="outlined" sx={{ flex: 1, minWidth: 200 }}>
                <CardContent>
                  <Typography variant="subtitle2" color="text.secondary">
                    Compliance Score
                  </Typography>
                  <Typography variant="h5">
                    {postAnalysis.complianceScore}/100
                  </Typography>
                </CardContent>
              </Card>
            )}
          </Box>

          {postAnalysis.recommendations && postAnalysis.recommendations.length > 0 && (
            <Box mt={3}>
              <Typography variant="subtitle2" gutterBottom>
                Recommendations
              </Typography>
              <List dense>
                {postAnalysis.recommendations.map((rec: string, index: number) => (
                  <ListItem key={index}>
                    <ListItemText primary={rec} />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </Paper>
      )}

      {!progress && !loading && (
        <Alert severity="info">
          No progress data available yet. Execution may not have started.
        </Alert>
      )}
    </Box>
  );
}
