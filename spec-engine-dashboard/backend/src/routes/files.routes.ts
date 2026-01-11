import { Router, Request, Response } from 'express';
import TOML from '@iarna/toml';
import { specFilesService } from '../services/spec-files.service';

const router = Router();

// POST /api/files/validate/toml - Validate TOML content
router.post('/validate/toml', async (req: Request, res: Response) => {
  try {
    const { content } = req.body;
    
    if (!content) {
      return res.status(400).json({ 
        valid: false, 
        errors: ['No content provided'] 
      });
    }
    
    try {
      // Try to parse TOML
      TOML.parse(content);
      
      res.json({ 
        valid: true, 
        errors: [] 
      });
    } catch (parseError: any) {
      res.json({ 
        valid: false, 
        errors: [parseError.message || 'Invalid TOML syntax'] 
      });
    }
  } catch (error: any) {
    console.error('Error validating TOML:', error);
    res.status(500).json({ 
      valid: false,
      errors: ['Validation service error']
    });
  }
});

// GET /api/files/progress/:specId - Get progress file content
router.get('/progress/:specId', async (req: Request, res: Response) => {
  try {
    const { specId } = req.params;
    const [dnaCode, descriptor] = specId.split('/');
    
    const progress = await specFilesService.readProgress(dnaCode, descriptor);
    
    if (!progress) {
      return res.status(404).json({ 
        error: 'Progress file not found',
        message: 'Execution may not have started yet'
      });
    }
    
    res.json({ progress });
  } catch (error: any) {
    console.error('Error fetching progress:', error);
    res.status(500).json({ 
      error: 'Failed to fetch progress file',
      message: error.message 
    });
  }
});

export default router;
