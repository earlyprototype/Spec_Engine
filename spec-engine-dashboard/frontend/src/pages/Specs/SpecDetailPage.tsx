import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Paper,
  Button,
  CircularProgress,
  Alert,
  Chip,
  Card,
  CardContent,
  Divider,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import {
  Edit as EditIcon,
  PlayArrow as ExecuteIcon,
  Description as DescriptionIcon,
} from '@mui/icons-material';
import { fetchSpec } from '../../store/specsSlice';
import type { AppDispatch, RootState } from '../../store/store';

export default function SpecDetailPage() {
  const { dnaCode, descriptor } = useParams<{ dnaCode: string; descriptor: string }>();
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();
  const { currentSpec, loading, error } = useSelector((state: RootState) => state.specs);

  const specId = `${dnaCode}/${descriptor}`;

  useEffect(() => {
    if (dnaCode && descriptor) {
      dispatch(fetchSpec(specId));
    }
  }, [dnaCode, descriptor, specId, dispatch]);

  const handleEdit = () => {
    navigate(`/specs/${dnaCode}/${descriptor}/edit`);
  };

  const handleExecute = () => {
    navigate(`/execute/${dnaCode}/${descriptor}`);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !currentSpec) {
    return (
      <Box>
        <Alert severity="error">{error || 'SPEC not found'}</Alert>
        <Button onClick={() => navigate('/specs')} sx={{ mt: 2 }}>
          Back to SPECs
        </Button>
      </Box>
    );
  }

  const structure = (currentSpec as any).structure || {};
  const tasks = structure.tasks || [];

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            {currentSpec.descriptor}
          </Typography>
          <Chip label={currentSpec.dnaCode} color="primary" variant="outlined" />
          <Chip label={currentSpec.status} sx={{ ml: 1 }} />
        </Box>
        <Box display="flex" gap={2}>
          <Button variant="outlined" startIcon={<EditIcon />} onClick={handleEdit}>
            Edit Parameters
          </Button>
          <Button variant="contained" color="success" startIcon={<ExecuteIcon />} onClick={handleExecute}>
            Execute
          </Button>
        </Box>
      </Box>

      {/* Goal */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Goal
        </Typography>
        <Divider sx={{ mb: 2 }} />
        <Typography variant="body1">
          {currentSpec.goal || 'No goal specified'}
        </Typography>
      </Paper>

      {/* Tasks */}
      {tasks.length > 0 && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Tasks ({tasks.length})
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <List>
            {tasks.map((task: any) => (
              <ListItem key={task.id}>
                <ListItemText
                  primary={`Task ${task.id}: ${task.name}`}
                  secondary={task.purpose || 'No purpose specified'}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}

      {/* File Paths */}
      <Card variant="outlined">
        <CardContent>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            File Locations
          </Typography>
          <Typography variant="body2" sx={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>
            Spec: {currentSpec.filePath}
          </Typography>
          <Typography variant="body2" sx={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>
            Parameters: {(currentSpec as any).parametersPath}
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}
