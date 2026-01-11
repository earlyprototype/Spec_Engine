import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
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
} from '@mui/material';
import {
  Add as AddIcon,
  Visibility as ViewIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { fetchDnaProfiles } from '../../store/dnaSlice';
import type { AppDispatch, RootState } from '../../store/store';

export default function DnaProfilesPage() {
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();
  const { profiles, loading, error } = useSelector((state: RootState) => state.dna);

  useEffect(() => {
    dispatch(fetchDnaProfiles());
  }, [dispatch]);

  const handleCreate = () => {
    navigate('/dna-profiles/create');
  };

  const handleView = (dnaCode: string) => {
    navigate(`/dna-profiles/${dnaCode}`);
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
        <Typography variant="h4">DNA Profiles</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreate}
        >
          Create DNA Profile
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {profiles.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No DNA Profiles Found
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Create your first DNA profile to configure project-level preferences for your SPECs.
          </Typography>
          <Button variant="contained" startIcon={<AddIcon />} onClick={handleCreate}>
            Create First DNA Profile
          </Button>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell><strong>DNA Code</strong></TableCell>
                <TableCell><strong>Project Name</strong></TableCell>
                <TableCell><strong>Testing</strong></TableCell>
                <TableCell><strong>Risk Tolerance</strong></TableCell>
                <TableCell><strong>Autonomy Level</strong></TableCell>
                <TableCell><strong>SPECs</strong></TableCell>
                <TableCell align="right"><strong>Actions</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {profiles.map((profile) => (
                <TableRow key={profile.dnaCode} hover>
                  <TableCell>
                    <Chip 
                      label={profile.dnaCode} 
                      color="primary" 
                      variant="outlined"
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{profile.projectName}</TableCell>
                  <TableCell>
                    <Chip 
                      label={profile.testing} 
                      size="small"
                      color={profile.testing === 'comprehensive' ? 'success' : 'default'}
                    />
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={profile.risk} 
                      size="small"
                      color={
                        profile.risk === 'low' ? 'success' :
                        profile.risk === 'high' ? 'error' : 'warning'
                      }
                    />
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={profile.autonomy} 
                      size="small"
                      color={profile.autonomy === 'high' ? 'primary' : 'default'}
                    />
                  </TableCell>
                  <TableCell>
                    {(profile as any).specCount || 0} SPECs
                  </TableCell>
                  <TableCell align="right">
                    <Tooltip title="View Details">
                      <IconButton
                        size="small"
                        onClick={() => handleView(profile.dnaCode)}
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
          Total: {profiles.length} DNA profile{profiles.length !== 1 ? 's' : ''}
        </Typography>
      </Box>
    </Box>
  );
}
