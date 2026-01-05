import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Paper,
  Button,
  Grid,
  Chip,
  Divider,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  Edit as EditIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
  Description as DescriptionIcon,
} from '@mui/icons-material';
import { fetchDnaProfile, updateDnaProfile } from '../../store/dnaSlice';
import type { AppDispatch, RootState } from '../../store/store';

export default function DnaDetailPage() {
  const { dnaCode } = useParams<{ dnaCode: string }>();
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();
  const { currentProfile, loading, error } = useSelector((state: RootState) => state.dna);

  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    projectName: '',
    testing: '',
    risk: '',
    autonomy: '',
    customTools: '',
    constraints: '',
  });

  useEffect(() => {
    if (dnaCode) {
      dispatch(fetchDnaProfile(dnaCode));
    }
  }, [dnaCode, dispatch]);

  useEffect(() => {
    if (currentProfile) {
      setFormData({
        projectName: currentProfile.projectName,
        testing: currentProfile.testing,
        risk: currentProfile.risk,
        autonomy: currentProfile.autonomy,
        customTools: currentProfile.customTools || '',
        constraints: currentProfile.constraints || '',
      });
    }
  }, [currentProfile]);

  const handleEdit = () => {
    setEditMode(true);
  };

  const handleCancel = () => {
    if (currentProfile) {
      setFormData({
        projectName: currentProfile.projectName,
        testing: currentProfile.testing,
        risk: currentProfile.risk,
        autonomy: currentProfile.autonomy,
        customTools: currentProfile.customTools || '',
        constraints: currentProfile.constraints || '',
      });
    }
    setEditMode(false);
  };

  const handleSave = async () => {
    if (!dnaCode) return;

    try {
      await dispatch(updateDnaProfile({
        dnaCode,
        data: formData,
      })).unwrap();
      setEditMode(false);
    } catch (err) {
      console.error('Failed to update DNA profile:', err);
    }
  };

  const handleViewSpecs = () => {
    navigate(`/specs?dnaCode=${dnaCode}`);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !currentProfile) {
    return (
      <Box>
        <Alert severity="error">
          {error || 'DNA Profile not found'}
        </Alert>
        <Button onClick={() => navigate('/dna-profiles')} sx={{ mt: 2 }}>
          Back to DNA Profiles
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            DNA Profile: {currentProfile.dnaCode}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Project: {currentProfile.projectName}
          </Typography>
        </Box>
        <Box display="flex" gap={2}>
          {!editMode ? (
            <>
              <Button
                variant="outlined"
                startIcon={<DescriptionIcon />}
                onClick={handleViewSpecs}
              >
                View SPECs
              </Button>
              <Button
                variant="contained"
                startIcon={<EditIcon />}
                onClick={handleEdit}
              >
                Edit
              </Button>
            </>
          ) : (
            <>
              <Button
                variant="outlined"
                startIcon={<CancelIcon />}
                onClick={handleCancel}
              >
                Cancel
              </Button>
              <Button
                variant="contained"
                startIcon={<SaveIcon />}
                onClick={handleSave}
              >
                Save Changes
              </Button>
            </>
          )}
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Main Information */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Configuration
            </Typography>
            <Divider sx={{ mb: 3 }} />

            {!editMode ? (
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Project Name
                  </Typography>
                  <Typography variant="body1">{currentProfile.projectName}</Typography>
                </Grid>

                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Testing Approach
                  </Typography>
                  <Chip
                    label={currentProfile.testing}
                    color={currentProfile.testing === 'comprehensive' ? 'success' : 'default'}
                    sx={{ mt: 1 }}
                  />
                </Grid>

                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Risk Tolerance
                  </Typography>
                  <Chip
                    label={currentProfile.risk}
                    color={
                      currentProfile.risk === 'low' ? 'success' :
                      currentProfile.risk === 'high' ? 'error' : 'warning'
                    }
                    sx={{ mt: 1 }}
                  />
                </Grid>

                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Autonomy Level
                  </Typography>
                  <Chip
                    label={currentProfile.autonomy}
                    color={currentProfile.autonomy === 'high' ? 'primary' : 'default'}
                    sx={{ mt: 1 }}
                  />
                </Grid>

                {currentProfile.customTools && (
                  <Grid item xs={12}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Custom Tools
                    </Typography>
                    <Typography variant="body1">{currentProfile.customTools}</Typography>
                  </Grid>
                )}

                {currentProfile.constraints && (
                  <Grid item xs={12}>
                    <Typography variant="subtitle2" color="text.secondary">
                      Constraints
                    </Typography>
                    <Typography variant="body1">{currentProfile.constraints}</Typography>
                  </Grid>
                )}
              </Grid>
            ) : (
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Project Name"
                    value={formData.projectName}
                    onChange={(e) => setFormData({ ...formData, projectName: e.target.value })}
                  />
                </Grid>

                <Grid item xs={12} md={4}>
                  <FormControl fullWidth>
                    <InputLabel>Testing</InputLabel>
                    <Select
                      value={formData.testing}
                      label="Testing"
                      onChange={(e) => setFormData({ ...formData, testing: e.target.value })}
                    >
                      <MenuItem value="basic">Basic</MenuItem>
                      <MenuItem value="standard">Standard</MenuItem>
                      <MenuItem value="comprehensive">Comprehensive</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12} md={4}>
                  <FormControl fullWidth>
                    <InputLabel>Risk</InputLabel>
                    <Select
                      value={formData.risk}
                      label="Risk"
                      onChange={(e) => setFormData({ ...formData, risk: e.target.value })}
                    >
                      <MenuItem value="low">Low</MenuItem>
                      <MenuItem value="medium">Medium</MenuItem>
                      <MenuItem value="high">High</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12} md={4}>
                  <FormControl fullWidth>
                    <InputLabel>Autonomy</InputLabel>
                    <Select
                      value={formData.autonomy}
                      label="Autonomy"
                      onChange={(e) => setFormData({ ...formData, autonomy: e.target.value })}
                    >
                      <MenuItem value="low">Low</MenuItem>
                      <MenuItem value="medium">Medium</MenuItem>
                      <MenuItem value="high">High</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Custom Tools"
                    multiline
                    rows={2}
                    value={formData.customTools}
                    onChange={(e) => setFormData({ ...formData, customTools: e.target.value })}
                  />
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Constraints"
                    multiline
                    rows={3}
                    value={formData.constraints}
                    onChange={(e) => setFormData({ ...formData, constraints: e.target.value })}
                  />
                </Grid>
              </Grid>
            )}
          </Paper>
        </Grid>

        {/* Stats Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Statistics
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Box mb={2}>
                <Typography variant="body2" color="text.secondary">
                  DNA Code
                </Typography>
                <Chip label={currentProfile.dnaCode} color="primary" sx={{ mt: 0.5 }} />
              </Box>
              <Box mb={2}>
                <Typography variant="body2" color="text.secondary">
                  SPECs Under This DNA
                </Typography>
                <Typography variant="h4">
                  {(currentProfile as any).specs?.length || 0}
                </Typography>
              </Box>
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Created
                </Typography>
                <Typography variant="body1">
                  {currentProfile.createdAt 
                    ? new Date(currentProfile.createdAt).toLocaleDateString()
                    : 'N/A'}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
