import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Button,
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
  TextField,
} from '@mui/material';
import {
  Add as AddIcon,
  Visibility as ViewIcon,
  Edit as EditIcon,
  PlayArrow as ExecuteIcon,
} from '@mui/icons-material';
import { fetchSpecs } from '../../store/specsSlice';
import type { AppDispatch, RootState } from '../../store/store';

export default function SpecsPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const dispatch = useDispatch<AppDispatch>();
  const { specs, loading, error } = useSelector((state: RootState) => state.specs);

  const dnaCodeFilter = searchParams.get('dnaCode');

  useEffect(() => {
    const filters: any = {};
    if (dnaCodeFilter) filters.dnaCode = dnaCodeFilter;
    dispatch(fetchSpecs(filters));
  }, [dispatch, dnaCodeFilter]);

  const handleCreate = () => {
    navigate('/specs/create');
  };

  const handleView = (dnaCode: string, descriptor: string) => {
    navigate(`/specs/${dnaCode}/${descriptor}`);
  };

  const handleEdit = (dnaCode: string, descriptor: string) => {
    navigate(`/specs/${dnaCode}/${descriptor}/edit`);
  };

  const handleExecute = (dnaCode: string, descriptor: string) => {
    navigate(`/execute/${dnaCode}/${descriptor}`);
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
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4">SPECs</Typography>
          {dnaCodeFilter && (
            <Typography variant="body2" color="text.secondary">
              Filtered by DNA: {dnaCodeFilter}
            </Typography>
          )}
        </Box>
        <Button variant="contained" startIcon={<AddIcon />} onClick={handleCreate}>
          Create SPEC
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      {specs.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No SPECs Found
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Create your first SPEC to define a goal and execution plan.
          </Typography>
          <Button variant="contained" startIcon={<AddIcon />} onClick={handleCreate}>
            Create First SPEC
          </Button>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell><strong>Descriptor</strong></TableCell>
                <TableCell><strong>DNA Code</strong></TableCell>
                <TableCell><strong>Goal</strong></TableCell>
                <TableCell><strong>Status</strong></TableCell>
                <TableCell align="right"><strong>Actions</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {specs.map((spec) => (
                <TableRow key={`${spec.dnaCode}/${spec.descriptor}`} hover>
                  <TableCell>
                    <Chip label={spec.descriptor} variant="outlined" size="small" />
                  </TableCell>
                  <TableCell>
                    <Chip label={spec.dnaCode} color="primary" variant="outlined" size="small" />
                  </TableCell>
                  <TableCell>{spec.goal || 'No goal specified'}</TableCell>
                  <TableCell>
                    <Chip 
                      label={spec.status} 
                      size="small"
                      color={spec.status === 'completed' ? 'success' : 'default'}
                    />
                  </TableCell>
                  <TableCell align="right">
                    <Tooltip title="View Details">
                      <IconButton
                        size="small"
                        onClick={() => handleView(spec.dnaCode, spec.descriptor)}
                        color="primary"
                      >
                        <ViewIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Edit Parameters">
                      <IconButton
                        size="small"
                        onClick={() => handleEdit(spec.dnaCode, spec.descriptor)}
                        color="secondary"
                      >
                        <EditIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Execute">
                      <IconButton
                        size="small"
                        onClick={() => handleExecute(spec.dnaCode, spec.descriptor)}
                        color="success"
                      >
                        <ExecuteIcon />
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
          Total: {specs.length} SPEC{specs.length !== 1 ? 's' : ''}
        </Typography>
      </Box>
    </Box>
  );
}
