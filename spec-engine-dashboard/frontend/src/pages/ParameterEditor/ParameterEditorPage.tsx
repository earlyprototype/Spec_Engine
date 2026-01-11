import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Paper,
  Chip,
} from '@mui/material';
import { Save as SaveIcon, Cancel as CancelIcon } from '@mui/icons-material';
import Editor from '@monaco-editor/react';
import { fetchParameters, updateParameters } from '../../store/specsSlice';
import { apiService } from '../../services/api';
import type { AppDispatch, RootState } from '../../store/store';

export default function ParameterEditorPage() {
  const { dnaCode, descriptor } = useParams<{ dnaCode: string; descriptor: string }>();
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();
  const { parameters, loading } = useSelector((state: RootState) => state.specs);

  const specId = `${dnaCode}/${descriptor}`;

  const [content, setContent] = useState('');
  const [isDirty, setIsDirty] = useState(false);
  const [saving, setSaving] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    if (dnaCode && descriptor) {
      dispatch(fetchParameters(specId));
    }
  }, [dnaCode, descriptor, specId, dispatch]);

  useEffect(() => {
    if (parameters) {
      setContent(parameters);
    }
  }, [parameters]);

  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (isDirty) {
        e.preventDefault();
        e.returnValue = '';
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, [isDirty]);

  const handleEditorChange = (value: string | undefined) => {
    if (value !== undefined) {
      setContent(value);
      setIsDirty(value !== parameters);
      setSaveSuccess(false);
      
      // Debounced validation
      if (validateTimeout) clearTimeout(validateTimeout);
      validateTimeout = setTimeout(() => validateToml(value), 500);
    }
  };

  let validateTimeout: NodeJS.Timeout;

  const validateToml = async (tomlContent: string) => {
    try {
      const response = await apiService.validateToml(tomlContent);
      if (response.data.valid) {
        setValidationError(null);
      } else {
        setValidationError(response.data.errors?.join(', ') || 'Invalid TOML');
      }
    } catch (error) {
      setValidationError('Validation failed');
    }
  };

  const handleSave = async () => {
    if (!specId) return;

    setSaving(true);
    setSaveSuccess(false);

    try {
      await dispatch(updateParameters({ specId, content })).unwrap();
      setIsDirty(false);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err: any) {
      setValidationError(err.message || 'Failed to save parameters');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    if (isDirty) {
      if (window.confirm('You have unsaved changes. Are you sure you want to leave?')) {
        navigate(-1);
      }
    } else {
      navigate(-1);
    }
  };

  // Keyboard shortcut for save (Ctrl+S)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        if (isDirty && !saving) {
          handleSave();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isDirty, saving, content]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Edit Parameters: {specId}
          </Typography>
          <Box display="flex" gap={1} alignItems="center">
            {isDirty && <Chip label="Unsaved changes" color="warning" size="small" />}
            {saveSuccess && <Chip label="Saved successfully" color="success" size="small" />}
            {validationError && <Chip label="Validation error" color="error" size="small" />}
          </Box>
        </Box>
        <Box display="flex" gap={2}>
          <Button
            variant="outlined"
            startIcon={<CancelIcon />}
            onClick={handleCancel}
            disabled={saving}
          >
            Cancel
          </Button>
          <Button
            variant="contained"
            startIcon={<SaveIcon />}
            onClick={handleSave}
            disabled={!isDirty || saving || !!validationError}
          >
            {saving ? 'Saving...' : 'Save (Ctrl+S)'}
          </Button>
        </Box>
      </Box>

      {validationError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {validationError}
        </Alert>
      )}

      <Paper sx={{ height: '70vh', overflow: 'hidden' }}>
        <Editor
          height="100%"
          defaultLanguage="ini"
          theme="vs-dark"
          value={content}
          onChange={handleEditorChange}
          options={{
            minimap: { enabled: true },
            fontSize: 14,
            lineNumbers: 'on',
            rulers: [80],
            wordWrap: 'on',
            automaticLayout: true,
            scrollBeyondLastLine: false,
            tabSize: 2,
          }}
        />
      </Paper>

      <Box mt={2}>
        <Typography variant="caption" color="text.secondary">
          Press Ctrl+S (Cmd+S on Mac) to save. Validation runs automatically as you type.
        </Typography>
      </Box>
    </Box>
  );
}
