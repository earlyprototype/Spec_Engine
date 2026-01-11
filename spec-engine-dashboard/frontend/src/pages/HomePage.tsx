import { Typography, Box, Grid, Paper } from '@mui/material';

export default function HomePage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        SPEC Engine Dashboard
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Welcome to the SPEC Engine Dashboard. Manage your DNA profiles, SPECs, and executions from here.
      </Typography>
      
      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">DNA Profiles</Typography>
            <Typography>Manage project configurations</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">SPECs</Typography>
            <Typography>Browse and create specifications</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">Executions</Typography>
            <Typography>Monitor SPEC execution status</Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
