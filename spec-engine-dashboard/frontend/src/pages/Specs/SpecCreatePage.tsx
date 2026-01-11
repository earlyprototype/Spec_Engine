import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Grid,
} from '@mui/material';
import { Save as SaveIcon, Cancel as CancelIcon } from '@mui/icons-material';
import { createSpec } from '../../store/specsSlice';
import { fetchDnaProfiles } from '../../store/dnaSlice';
import type { AppDispatch, RootState } from '../../store/store';

export default function SpecCreatePage() {
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();
  const { profiles } = useSelector((state: RootState) => state.dna);

  const [formData, setFormData] = useState({
    dnaCode: '',
    descriptor: '',
    goal: '',
  });

  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    dispatch(fetchDnaProfiles());
  }, [dispatch]);

  const handleSubmit = async () => {
    if (!formData.dnaCode || !formData.descriptor || !formData.goal) {
      setError('All fields are required');
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      await dispatch(createSpec({
        dnaCode: formData.dnaCode,
        descriptor: formData.descriptor,
        goal: formData.goal,
      })).unwrap();

      navigate(`/specs/${formData.dnaCode}/${formData.descriptor}`);
    } catch (err: any) {
      setError(err.message || 'Failed to create SPEC');
      setSubmitting(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Create SPEC</Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Create a simplified SPEC from template. For complex SPECs, use Spec_Commander.md.
      </Typography>

      <Paper sx={{ p: 3, mt: 3 }}>
        {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

        <Grid container spacing={3}>
          <Grid item xs={12}>
            <FormControl fullWidth required>
              <InputLabel>DNA Profile</InputLabel>
              <Select
                value={formData.dnaCode}
                label="DNA Profile"
                onChange={(e) => setFormData({ ...formData, dnaCode: e.target.value })}
              >
                {profiles.map((profile) => (
                  <MenuItem key={profile.dnaCode} value={profile.dnaCode}>
                    {profile.dnaCode} - {profile.projectName}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Descriptor"
              required
              value={formData.descriptor}
              onChange={(e) => setFormData({ ...formData, descriptor: e.target.value.toLowerCase().replace(/\s+/g, '_') })}
              placeholder="e.g., my_spec"
              helperText="Lowercase, underscores only. Will be used in filenames."
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Goal"
              required
              multiline
              rows={3}
              value={formData.goal}
              onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
              placeholder="Describe the goal this SPEC will achieve..."
            />
          </Grid>
        </Grid>

        <Box mt={4} display="flex" gap={2} justifyContent="flex-end">
          <Button variant="outlined" startIcon={<CancelIcon />} onClick={() => navigate('/specs')} disabled={submitting}>
            Cancel
          </Button>
          <Button variant="contained" startIcon={<SaveIcon />} onClick={handleSubmit} disabled={submitting}>
            {submitting ? 'Creating...' : 'Create SPEC'}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}
